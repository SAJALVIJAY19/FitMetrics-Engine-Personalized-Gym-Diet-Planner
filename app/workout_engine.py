import random

def generate_workout_plan(bmi, predicted_calories_burn, weight_kg):
    """
    Generates a workout plan based on user metrics and ML prediction.
    predicted_calories_burn: The ML model's prediction for calories burned per hour of exercise.
    """
    
    intensity = "Moderate"
    duration = 45
    level = "Intermediate"
    
    if bmi > 30:
        level = "Beginner"
        intensity = "Low Impact"
        duration = 30
    elif bmi < 18.5:
        level = "Beginner"
        intensity = "Strength Focus" # Build muscle
        duration = 45
    elif predicted_calories_burn > 500:
        level = "Advanced"
        intensity = "High Intensity"
        duration = 60
        
    exercises_pool = {
        "Beginner": ["Walking", "Bodyweight Squats", "Wall Pushups", "Plank (Modified)", "Step-ups"],
        "Intermediate": ["Jogging", "Pushups", "Lunges", "Plank", "Dumbbell Rows"],
        "Advanced": ["Running", "Burpees", "Jump Squats", "Pull-ups", "HIIT Circuits"]
    }
    
    selected_exercises = random.sample(exercises_pool.get(level, exercises_pool["Intermediate"]), 3)
    
    # Calculate target calories for this session
    # predicted_calories_burn is per hour
    target_burn = (predicted_calories_burn * (duration / 60))
    
    return {
        "level": level,
        "intensity": intensity,
        "duration_minutes": duration,
        "calories_target": int(target_burn),
        "exercises": selected_exercises,
        "ml_prediction_hourly": predicted_calories_burn
    }
