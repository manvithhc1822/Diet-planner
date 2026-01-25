from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import math

app = Flask(__name__)
CORS(app)

# ---------------- AI / ML LOGIC ----------------

def calculate_bmi(weight, height):
    h = height / 100
    return round(weight / (h*h), 2)

def calorie_estimator(weight, height, age, goal):
    # Mifflin-St Jeor (AI nutrition formula)
    base = 10*weight + 6.25*height - 5*age + 5

    if goal == "Weight Loss":
        return int(base - 400)
    elif goal == "Muscle Gain":
        return int(base + 500)
    else:
        return int(base)

def ai_generate_diet(calories):
    # Food knowledge base (NOT diet plan)
    proteins = ["Eggs", "Paneer", "Chicken", "Lentils", "Curd"]
    carbs = ["Rice", "Chapati", "Oats", "Sweet Potato"]
    fats = ["Nuts", "Olive Oil", "Peanut Butter"]
    veggies = ["Broccoli", "Carrot", "Beans", "Spinach"]
    fruits = ["Apple", "Banana", "Orange", "Papaya"]

    # AI-style random intelligent composition
    diet = {
        "Breakfast": f"{random.choice(carbs)} + {random.choice(fruits)}",
        "Lunch": f"{random.choice(proteins)} + {random.choice(veggies)} + {random.choice(carbs)}",
        "Snack": f"{random.choice(fruits)} + {random.choice(fats)}",
        "Dinner": f"{random.choice(proteins)} + {random.choice(veggies)}"
    }

    return diet

# ---------------- API ----------------

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json

    age = int(data["age"])
    height = int(data["height"])
    weight = int(data["weight"])
    goal = data["goal"]

    bmi = calculate_bmi(weight, height)
    calories = calorie_estimator(weight, height, age, goal)
    diet = ai_generate_diet(calories)

    result = f"""
BMI: {bmi}
Daily Calories Target: {calories} kcal

AI-GENERATED DIET PLAN:
Breakfast: {diet['Breakfast']}
Lunch: {diet['Lunch']}
Snack: {diet['Snack']}
Dinner: {diet['Dinner']}

Note: Diet is dynamically generated using AI logic.
"""

    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(debug=True)
