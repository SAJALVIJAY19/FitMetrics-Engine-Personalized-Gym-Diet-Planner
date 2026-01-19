import requests
import random

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
    """
    # Calorie distribution
    breakfast_cal = tdee * 0.25
    lunch_cal = tdee * 0.35
    dinner_cal = tdee * 0.30
    snack_cal = tdee * 0.10
    
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
    
    plan = {
        "targets": {
            "total": tdee,
            "breakfast": int(breakfast_cal),
            "lunch": int(lunch_cal),
            "dinner": int(dinner_cal),
            "snacks": int(snack_cal)
        },
        "meals": {
            "breakfast": random.choice(foods["breakfast"]),
            "lunch": random.choice(foods["lunch"]),
            "dinner": random.choice(foods["dinner"]),
            "snacks": random.choice(foods["snacks"])
        }
    }
    
    # Try to enhance with OpenFoodFacts for one item (demo purpose)
    # real_cal = lookup_food_calories("apple")
    # if real_cal:
    #     plan["meals"]["snacks"]["note"] = f"OpenFoodFacts says Apple is ~{real_cal} kcal/100g"
        
    return plan

def get_random_meal(meal_type):
    """
    Returns a random meal for the specified type (breakfast, lunch, dinner, snacks).
    """
    # Placeholder food database (duplicated for scope, ideally should be a constant or class)
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
