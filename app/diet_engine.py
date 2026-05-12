import requests
import random
import os
import json
from google import genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def lookup_food_calories(food_name):
    """
    Queries OpenFoodFacts API for calorie information.
    Returns calories per 100g/serving or None if not found.
    """
    url = f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={food_name}&search_simple=1&action=process&json=1"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("products"):
                product = data["products"][0]
                nutriments = product.get("nutriments", {})
                # Try to get energy-kcal_100g
                kcal = nutriments.get("energy-kcal_100g")
                if kcal:
                    return float(kcal)
    except Exception as e:
        print(f"Error fetching food data: {e}")
    return None

def generate_diet_plan(tdee):
    """
    Generates a simple diet plan based on TDEE.
    Uses Gemini API if API key is provided, otherwise falls back to a template list.
    """
    # Calorie distribution
    breakfast_cal = int(tdee * 0.25)
    lunch_cal = int(tdee * 0.35)
    dinner_cal = int(tdee * 0.30)
    snack_cal = int(tdee * 0.10)
    
    plan = {
        "targets": {
            "total": tdee,
            "breakfast": breakfast_cal,
            "lunch": lunch_cal,
            "dinner": dinner_cal,
            "snacks": snack_cal
        },
        "meals": {}
    }

    if GEMINI_API_KEY:
        try:
            client = genai.Client(api_key=GEMINI_API_KEY)
            prompt = f"""
Generate a healthy daily diet plan for a person with a Total Daily Energy Expenditure (TDEE) of {tdee} calories.
The calories should be roughly distributed as:
- Breakfast: ~{breakfast_cal} calories
- Lunch: ~{lunch_cal} calories
- Dinner: ~{dinner_cal} calories
- Snacks: ~{snack_cal} calories

Respond ONLY with a valid JSON format perfectly matching this exact structure, with no markdown tags or other text.
{{
    "breakfast": {{"name": "Food name here", "cal": {breakfast_cal}}},
    "lunch": {{"name": "Food name here", "cal": {lunch_cal}}},
    "dinner": {{"name": "Food name here", "cal": {dinner_cal}}},
    "snacks": {{"name": "Food name here", "cal": {snack_cal}}}
}}
"""
            response = client.models.generate_content(model='gemini-1.5-flash', contents=prompt)
            response_text = response.text.strip()
            # Clean up potential markdown from the response
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            
            meals = json.loads(response_text.strip())
            
            # Basic validation
            if all(k in meals for k in ["breakfast", "lunch", "dinner", "snacks"]):
                plan["meals"] = meals
                return plan
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            print("Falling back to standard generation.")

    # Placeholder food database (fallback)
    foods = {
        "breakfast": [
            {"name": "Oatmeal with Berries", "cal": 350},
            {"name": "Scrambled Eggs & Toast", "cal": 400},
            {"name": "Greek Yogurt Parfait", "cal": 300}
        ],
        "lunch": [
            {"name": "Grilled Chicken Salad", "cal": 450},
            {"name": "Turkey Sandwich", "cal": 500},
            {"name": "Quinoa Bowl", "cal": 550}
        ],
        "dinner": [
            {"name": "Salmon with Veggies", "cal": 600},
            {"name": "Pasta Primavera", "cal": 550},
            {"name": "Stir-fry Tofu", "cal": 500}
        ],
        "snacks": [
            {"name": "Apple & Almonds", "cal": 200},
            {"name": "Protein Bar", "cal": 250},
            {"name": "Carrot Sticks with Hummus", "cal": 150}
        ]
    }
    
    plan["meals"]["breakfast"] = random.choice(foods["breakfast"])
    plan["meals"]["lunch"] = random.choice(foods["lunch"])
    plan["meals"]["dinner"] = random.choice(foods["dinner"])
    plan["meals"]["snacks"] = random.choice(foods["snacks"])
        
    return plan

def get_random_meal(meal_type):
    """
    Returns a random meal for the specified type (breakfast, lunch, dinner, snacks).
    """
    foods = {
        "breakfast": [
            {"name": "Oatmeal with Berries", "cal": 350},
            {"name": "Scrambled Eggs & Toast", "cal": 400},
            {"name": "Greek Yogurt Parfait", "cal": 300},
             {"name": "Avocado Toast", "cal": 380},
             {"name": "Protein Pancakes", "cal": 420}
        ],
        "lunch": [
            {"name": "Grilled Chicken Salad", "cal": 450},
            {"name": "Turkey Sandwich", "cal": 500},
            {"name": "Quinoa Bowl", "cal": 550},
             {"name": "Tuna Wrap", "cal": 480},
             {"name": "Lentil Soup & Bread", "cal": 420},
        ],
        "dinner": [
            {"name": "Salmon with Veggies", "cal": 600},
            {"name": "Pasta Primavera", "cal": 550},
            {"name": "Stir-fry Tofu", "cal": 500},
            {"name": "Grilled Steak & Asparagus", "cal": 650},
            {"name": "Chicken Curry & Rice", "cal": 620}
        ],
        "snacks": [
            {"name": "Apple & Almonds", "cal": 200},
            {"name": "Protein Bar", "cal": 250},
            {"name": "Carrot Sticks with Hummus", "cal": 150},
            {"name": "Greek Yogurt", "cal": 180},
            {"name": "Hard Boiled Eggs", "cal": 140}
        ]
    }
    
    meal_list = foods.get(meal_type.lower())
    if meal_list:
        return random.choice(meal_list)
    return None
