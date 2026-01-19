import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
import joblib
import os
import json
from datetime import datetime

def generate_synthetic_data(n_samples=2000):
    np.random.seed(42)
    
    data = {
        "age": np.random.randint(18, 70, n_samples),
        "gender_code": np.random.randint(0, 2, n_samples), # 0: Female, 1: Male
        "height_cm": np.random.normal(170, 10, n_samples),
        "weight_kg": np.random.normal(70, 15, n_samples),
        "activity_level_code": np.random.randint(1, 6, n_samples) # 1-5
    }
    
    df = pd.DataFrame(data)
    
    # Realistic formula for calories burned per hour (base) + noise
    # Base formula approximation: BMR/24 * activity_factor
    # Simplified logic for "calories burned per hour during exercise"
    
    def calculate_target(row):
        # Base metabolic rate proxy
        bmr = 10 * row["weight_kg"] + 6.25 * row["height_cm"] - 5 * row["age"]
        if row["gender_code"] == 1:
            bmr += 5
        else:
            bmr -= 161
            
        # Activity multiplier effect on hourly burn
        activity_mult = 1.0 + (row["activity_level_code"] * 0.1)
        
        # Base hourly burn (sedentary)
        base_hourly = (bmr * 1.2) / 24
        
        # Target: Active burn per hour (e.g. for a workout session)
        # This is what we want to predict: "How many calories will I burn in an hour of exercise?"
        # We'll assume higher weight/height/activity level = higher burn
        
        active_hourly = base_hourly * activity_mult * 2.0 # Factor 2.0 for exercise intensity
        
        # Add noise
        noise = np.random.normal(0, 20)
        return max(100, active_hourly + noise)

    df["calories_per_hour"] = df.apply(calculate_target, axis=1)
    
    return df

def train_and_save():
    print("Generating synthetic data...")
    df = generate_synthetic_data()
    
    X = df[["age", "gender_code", "height_cm", "weight_kg", "activity_level_code"]]
    y = df["calories_per_hour"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training RandomForestRegressor...")
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    
    print(f"Model Evaluation:\nR2 Score: {r2:.4f}\nRMSE: {rmse:.4f}")
    
    # Save model
    output_dir = os.path.join(os.path.dirname(__file__), "..", "ML")
    os.makedirs(output_dir, exist_ok=True)
    model_path = os.path.join(output_dir, "model.pkl")
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")
    
    # Save metadata
    metadata = {
        "features": list(X.columns),
        "training_date": datetime.now().isoformat(),
        "metrics": {"r2": r2, "rmse": rmse}
    }
    with open(os.path.join(output_dir, "model_metadata.json"), "w") as f:
        json.dump(metadata, f, indent=2)

if __name__ == "__main__":
    train_and_save()
