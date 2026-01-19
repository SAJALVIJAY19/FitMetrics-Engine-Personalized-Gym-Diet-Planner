import joblib
import os
import pandas as pd
from .utils import map_activity_level

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "ML", "model.pkl")
_model = None

def load_model():
    global _model
    if _model is None:
        if os.path.exists(MODEL_PATH):
            _model = joblib.load(MODEL_PATH)
        else:
            print("WARNING: Model not found at", MODEL_PATH)
            return None
    return _model

def predict_calories(age, gender, height_cm, weight_kg, activity_level_str):
    model = load_model()
    if model is None:
        return 0.0
    
    # Prepare input dataframe matching training features
    # Features: age, gender_code, height_cm, weight_kg, activity_level_code
    
    gender_code = 1 if gender.lower() == "male" else 0
    activity_level_map = {
        "sedentary": 1,
        "lightly_active": 2,
        "moderately_active": 3,
        "very_active": 4,
        "super_active": 5
    }
    activity_code = activity_level_map.get(activity_level_str.lower(), 1)
    
    input_data = pd.DataFrame([{
        "age": age,
        "gender_code": gender_code,
        "height_cm": height_cm,
        "weight_kg": weight_kg,
        "activity_level_code": activity_code
    }])
    
    prediction = model.predict(input_data)[0]
    return round(prediction, 2)
