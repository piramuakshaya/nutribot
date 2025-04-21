import streamlit as st
import pandas as pd
import random
import json
from datetime import datetime
import os

# Set page configuration
st.set_page_config(
    page_title="NutriBot - AI Nutrition Advisor",
    page_icon="🥗",
    layout="wide"
)

# Load data (would normally come from external sources)
@st.cache_data
def load_food_data():
    # This is a simplified dataset - in a real app, you'd use a more comprehensive database
    foods = {
        "apple": {"calories": 95, "protein": 0.5, "carbs": 25, "fat": 0.3, "fiber": 4, "category": "fruit"},
        "banana": {"calories": 105, "protein": 1.3, "carbs": 27, "fat": 0.4, "fiber": 3.1, "category": "fruit"},
        "spinach": {"calories": 23, "protein": 2.9, "carbs": 3.6, "fat": 0.4, "fiber": 2.2, "category": "vegetable"},
        "salmon": {"calories": 208, "protein": 20, "carbs": 0, "fat": 13, "fiber": 0, "category": "protein"},
        "chicken breast": {"calories": 165, "protein": 31, "carbs": 0, "fat": 3.6, "fiber": 0, "category": "protein"},
        "brown rice": {"calories": 216, "protein": 5, "carbs": 45, "fat": 1.8, "fiber": 3.5, "category": "grain"},
        "quinoa": {"calories": 222, "protein": 8, "carbs": 39, "fat": 3.6, "fiber": 5, "category": "grain"},
        "avocado": {"calories": 240, "protein": 3, "carbs": 12, "fat": 22, "fiber": 10, "category": "fruit"},
        "greek yogurt": {"calories": 130, "protein": 17, "carbs": 6, "fat": 4, "fiber": 0, "category": "dairy"},
        "almonds": {"calories": 164, "protein": 6, "carbs": 6, "fat": 14, "fiber": 3.5, "category": "nuts"},
        "oats": {"calories": 389, "protein": 16.9, "carbs": 66.3, "fat": 6.9, "fiber": 10.6, "category": "grain"},
        "sweet potato": {"calories": 86, "protein": 1.6, "carbs": 20.1, "fat": 0.1, "fiber": 3, "category": "vegetable"},
        "lentils": {"calories": 116, "protein": 9, "carbs": 20, "fat": 0.4, "fiber": 8, "category": "legume"},
        "broccoli": {"calories": 55, "protein": 3.7, "carbs": 11.2, "fat": 0.6, "fiber": 5.1, "category": "vegetable"},
        "eggs": {"calories": 78, "protein": 6.3, "carbs": 0.6, "fat": 5.3, "fiber": 0, "category": "protein"},
    }
    return foods

@st.cache_data
def load_nutrition_facts():
    nutrition_facts = {
        "protein": "Essential for muscle building, immune function, and enzyme production. Recommended intake varies based on weight and activity level.",
        "carbs": "Primary energy source for the body. Complex carbs like whole grains provide sustained energy.",
        "fat": "Essential for hormone production, vitamin absorption, and brain function. Focus on healthy fats like omega-3s.",
        "fiber": "Supports digestive health, helps maintain steady blood sugar, and contributes to feelings of fullness.",
        "magnesium": "Essential for muscle and nerve function, blood glucose control, and bone health.",
        "vitamin C": "Supports immune function, collagen production, and acts as an antioxidant.",
        "iron": "Critical for oxygen transport in the blood and energy metabolism.",
        "calcium": "Essential for bone health, muscle function, and nerve signaling.",
        "quinoa": "Quinoa is gluten-free and a complete protein, containing all nine essential amino acids.",
        "probiotics": "Live beneficial bacteria that support gut health and may boost immune function.",
        "keto diet": "A high-fat, very low-carbohydrate diet that forces the body to burn fats rather than carbs.",
        "intermittent fasting": "An eating pattern that cycles between periods of eating and fasting, often used for weight management.",
        "carbs": "Carbohydrates are not inherently 'bad'. They're the body's primary energy source. Focus on complex carbs like whole grains.",
    }
    return nutrition_facts

@st.cache_data
def load_recipes():
    recipes = [
        {
            "name": "Quinoa Salad",
            "ingredients": ["1 cup quinoa", "2 cups water", "1 cucumber, diced", "1 bell pepper, diced", "1/4 cup olive oil", "2 tbsp lemon juice", "Salt and pepper to taste"],
            "instructions": "1. Cook quinoa in water according to package instructions\n2. Mix with diced vegetables\n3. Dress with olive oil and lemon juice\n4. Season with salt and pepper",
            "nutritional_info": "Calories: 350, Protein: 10g, Carbs: 42g, Fat: 16g, Fiber: 7g",
            "diet_types": ["vegetarian", "vegan", "gluten-free"],
            "meal_type": "lunch",
        },
        {
            "name": "Grilled Chicken with Roasted Vegetables",
            "ingredients": ["2 chicken breasts", "2 cups mixed vegetables (bell peppers, zucchini, onions)", "2 tbsp olive oil", "2 cloves garlic, minced", "1 tsp Italian herbs", "Salt and pepper to taste"],
            "instructions": "1. Marinate chicken with olive oil, garlic, and herbs\n2. Grill chicken until cooked through\n3. Toss vegetables in olive oil, salt, and pepper\n4. Roast vegetables at 425°F for 20 minutes",
            "nutritional_info": "Calories: 320, Protein: 35g, Carbs: 12g, Fat: 15g, Fiber: 4g",
            "diet_types": ["keto", "paleo", "gluten-free"],
            "meal_type": "dinner",
        },
        {
            "name": "Berry Protein Smoothie",
            "ingredients": ["1 cup mixed berries", "1 scoop protein powder", "1 cup almond milk", "1/2 banana", "1 tbsp chia seeds", "Ice cubes"],
            "instructions": "Blend all ingredients until smooth.",
            "nutritional_info": "Calories: 250, Protein: 20g, Carbs: 30g, Fat: 5g, Fiber: 8g",
            "diet_types": ["vegetarian", "gluten-free"],
            "meal_type": "breakfast",
        },
        {
            "name": "Lentil Soup",
            "ingredients": ["1 cup dry lentils", "1 onion, chopped", "2 carrots, diced", "2 celery stalks, diced", "4 cups vegetable broth", "2 cloves garlic, minced", "1 tsp cumin", "Salt and pepper to taste"],
            "instructions": "1. Sauté onion, carrots, celery, and garlic\n2. Add lentils, broth, and spices\n3. Simmer for 30 minutes or until lentils are tender",
            "nutritional_info": "Calories: 200, Protein: 12g, Carbs: 35g, Fat: 1g, Fiber: 15g",
            "diet_types": ["vegetarian", "vegan", "gluten-free"],
            "meal_type": "lunch",
        },
        {
            "name": "Avocado Toast with Egg",
            "ingredients": ["1 slice whole grain bread", "1/2 avocado", "1 egg", "Red pepper flakes", "Salt and pepper to taste"],
            "instructions": "1. Toast bread\n2. Mash avocado and spread on toast\n3. Top with fried or poached egg\n4. Season with salt, pepper, and red pepper flakes",
            "nutritional_info": "Calories: 300, Protein: 12g, Carbs: 20g, Fat: 18g, Fiber: 7g",
            "diet_types": ["vegetarian"],
            "meal_type": "breakfast",
        }
    ]
    return recipes

@st.cache_data
def load_meal_plans():
    meal_plans = {
        "weight_loss": {
            "name": "Weight Loss Plan",
            "description": "A balanced plan with calorie deficit to promote healthy weight loss",
            "daily_calories": 1500,
            "macros": {"protein": "30%", "carbs": "40%", "fat": "30%"},
            "sample_day": {
                "breakfast": "Greek yogurt with berries and honey",
                "lunch": "Grilled chicken salad with olive oil dressing",
                "dinner": "Baked salmon with steamed vegetables",
                "snacks": ["Apple with almond butter", "Carrot sticks with hummus"]
            }
        },
        "muscle_gain": {
            "name": "Muscle Building Plan",
            "description": "Higher protein and calories to support muscle growth",
            "daily_calories": 2800,
            "macros": {"protein": "35%", "carbs": "45%", "fat": "20%"},
            "sample_day": {
                "breakfast": "Oatmeal with protein powder, banana, and peanut butter",
                "lunch": "Chicken breast with brown rice and vegetables",
                "dinner": "Steak with sweet potato and broccoli",
                "snacks": ["Protein shake with fruit", "Greek yogurt with nuts"]
            }
        },
        "maintenance": {
            "name": "Balanced Maintenance Plan",
            "description": "Well-rounded nutrition to maintain current weight and support overall health",
            "daily_calories": 2000,
            "macros": {"protein": "25%", "carbs": "50%", "fat": "25%"},
            "sample_day": {
                "breakfast": "Scrambled eggs with toast and avocado",
                "lunch": "Quinoa salad with vegetables and chickpeas",
                "dinner": "Baked fish with roasted vegetables and brown rice",
                "snacks": ["Fruit smoothie", "Mixed nuts"]
            }
        },
        "vegetarian": {
            "name": "Vegetarian Plan",
            "description": "Plant-based proteins and balanced nutrition without meat",
            "daily_calories": 1800,
            "macros": {"protein": "20%", "carbs": "55%", "fat": "25%"},
            "sample_day": {
                "breakfast": "Smoothie with plant-based protein, berries, and spinach",
                "lunch": "Lentil soup with whole grain bread",
                "dinner": "Tofu stir-fry with vegetables and brown rice",
                "snacks": ["Hummus with vegetable sticks", "Trail mix"]
            }
        },
        "keto": {
            "name": "Ketogenic Plan",
            "description": "Very low carb, high fat to promote ketosis",
            "daily_calories": 1800,
            "macros": {"protein": "20%", "carbs": "5%", "fat": "75%"},
            "sample_day": {
                "breakfast": "Avocado and eggs with cheese",
                "lunch": "Spinach salad with grilled chicken, olive oil, and nuts",
                "dinner": "Baked salmon with asparagus and butter",
                "snacks": ["Cheese cubes", "Olives"]
            }
        }
    }
    return meal_plans

# Load data
food_data = load_food_data()
nutrition_facts = load_nutrition_facts()
recipes = load_recipes()
meal_plans = load_meal_plans()

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'user_info' not in st.session_state:
    st.session_state.user_info = {
        "name": "",
        "dietary_preferences": [],
        "allergies": [],
        "goal": "",
        "height": "",
        "weight": "",
        "activity_level": "",
        "onboarded": False
    }

if 'water_tracker' not in st.session_state:
    st.session_state.water_tracker = {
        "today": datetime.now().strftime("%Y-%m-%d"),
        "glasses": 0
    }

# Utility functions
def generate_meal_plan(goal, preferences=None, allergies=None):
    """Generate a personalized meal plan based on user preferences"""
    if not preferences:
        preferences = []
    if not allergies:
        allergies = []
    
    # Select appropriate base plan
    if goal.lower() == "weight loss":
        base_plan = meal_plans["weight_loss"]
    elif goal.lower() == "muscle gain":
        base_plan = meal_plans["muscle_gain"]
    elif "vegetarian" in preferences:
        base_plan = meal_plans["vegetarian"]
    elif "keto" in preferences:
        base_plan = meal_plans["keto"]
    else:
        base_plan = meal_plans["maintenance"]
    
    # Filter recipes based on preferences and allergies
    suitable_recipes = []
    for recipe in recipes:
        compatible = True
        # Check for dietary preferences
        if preferences:
            has_matching_diet = False
            for diet in recipe["diet_types"]:
                if diet in preferences:
                    has_matching_diet = True
                    break
            if preferences and not has_matching_diet:
                compatible = False
        
        # Check for allergies (very simplified)
        if compatible and allergies:
            for ingredient in recipe["ingredients"]:
                for allergy in allergies:
                    if allergy.lower() in ingredient.lower():
                        compatible = False
                        break
        
        if compatible:
            suitable_recipes.append(recipe)
    
    # Create a meal plan (simplified)
    breakfast_options = [r for r in suitable_recipes if r["meal_type"] == "breakfast"]
    lunch_options = [r for r in suitable_recipes if r["meal_type"] == "lunch"]
    dinner_options = [r for r in suitable_recipes if r["meal_type"] == "dinner"]
    
    # If no specific meal type recipes available, use any suitable recipe
    if not breakfast_options:
        breakfast_options = suitable_recipes
    if not lunch_options:
        lunch_options = suitable_recipes
    if not dinner_options:
        dinner_options = suitable_recipes
        
    # Create 3-day meal plan
    meal_plan = {
        "goal": goal,
        "daily_calories": base_plan["daily_calories"],
        "macros": base_plan["macros"],
        "days": []
    }
    
    for day in range(1, 4):
        day_plan = {
            "day": day,
            "breakfast": random.choice(breakfast_options)["name"] if breakfast_options else "Custom breakfast based on preferences",
            "lunch": random.choice(lunch_options)["name"] if lunch_options else "Custom lunch based on preferences",
            "dinner": random.choice(dinner_options)["name"] if dinner_options else "Custom dinner based on preferences",
            "snacks": ["Fruit and nuts", "Yogurt"] if goal != "weight loss" else ["Celery with hummus"]
        }
        meal_plan["days"].append(day_plan)
    
    return meal_plan

def get_chatbot_response(user_input):
    """Generate responses for user questions"""
    user_input = user_input.lower()
    
    # Meal plan request
    if "meal plan" in user_input or "plan for" in user_input:
        goal = st.session_state.user_info["goal"] if st.session_state.user_info["goal"] else "maintenance"
        preferences = st.session_state.user_info["dietary_preferences"]
        allergies = st.session_state.user_info["allergies"]
        meal_plan = generate_meal_plan(goal, preferences, allergies)
        
        response = f"Here's a meal plan tailored for your {goal} goal:\n\n"
        response += f"Daily target: ~{meal_plan['daily_calories']} calories\n"
        response += f"Macros: {meal_plan['macros']['protein']} protein, {meal_plan['macros']['carbs']} carbs, {meal_plan['macros']['fat']} fat\n\n"
        
        for day in meal_plan["days"]:
            response += f"Day {day['day']}:\n"
            response += f"- Breakfast: {day['breakfast']}\n"
            response += f"- Lunch: {day['lunch']}\n"
            response += f"- Dinner: {day['dinner']}\n"
            response += f"- Snacks: {', '.join(day['snacks'])}\n\n"
        
        return response
    
    # Recipe request
    elif "recipe" in user_input:
        diet_type = None
        for diet in ["vegetarian", "vegan", "keto", "paleo", "gluten-free"]:
            if diet in user_input:
                diet_type = diet
                break
        
        filtered_recipes = recipes
        if diet_type:
            filtered_recipes = [r for r in recipes if diet_type in r["diet_types"]]
        
        if not filtered_recipes:
            return "I don't have any recipes matching those criteria. Try asking for a different type of recipe."
        
        chosen_recipe = random.choice(filtered_recipes)
        
        response = f"Here's a {diet_type + ' ' if diet_type else ''}recipe you might enjoy:\n\n"
        response += f"**{chosen_recipe['name']}**\n\n"
        response += "**Ingredients:**\n"
        for ingredient in chosen_recipe['ingredients']:
            response += f"- {ingredient}\n"
        
        response += "\n**Instructions:**\n"
        response += chosen_recipe['instructions']
        
        response += f"\n\n**Nutritional Information:**\n{chosen_recipe['nutritional_info']}"
        return response
    
    # Nutrition information
    elif any(nutrient in user_input for nutrient in nutrition_facts.keys()):
        for nutrient, info in nutrition_facts.items():
            if nutrient in user_input:
                if "what is" in user_input or "tell me about" in user_input or "benefits" in user_input:
                    return f"**{nutrient.capitalize()}**: {info}"
        
        # If we get here, we found a keyword but not a direct question
        return "I can provide information about various nutrients and foods. Could you ask more specifically what you'd like to know?"
    
    # Food information
    elif any(food in user_input for food in food_data.keys()):
        for food, info in food_data.items():
            if food in user_input:
                response = f"**Nutritional information for {food}**:\n"
                response += f"- Calories: {info['calories']}\n"
                response += f"- Protein: {info['protein']}g\n"
                response += f"- Carbs: {info['carbs']}g\n"
                response += f"- Fat: {info['fat']}g\n"
                response += f"- Fiber: {info['fiber']}g\n"
                return response
    
    # Dietary questions
    elif "diet" in user_input or "weight loss" in user_input or "protein" in user_input:
        if "how much protein" in user_input:
            return "A general guideline is to consume 0.8-1g of protein per pound of body weight if you're active, or 0.36g per pound for sedentary individuals. Athletes may need up to 1.2-2g per pound depending on training intensity."
        
        elif "lose weight" in user_input:
            return "Weight loss requires creating a calorie deficit through diet and exercise. Focus on whole foods, plenty of protein and fiber, and reduce processed foods and added sugars. A sustainable approach is aiming for 0.5-1 pound of weight loss per week."
        
        elif "keto" in user_input:
            return "The ketogenic diet is very low in carbohydrates (typically <50g per day), moderate in protein, and high in fat. It forces your body to burn fats rather than carbohydrates for energy. While effective for some, it's restrictive and not suitable for everyone."
    
    # General healthy eating
    elif "healthy eating" in user_input or "healthy diet" in user_input:
        return "A healthy diet includes a variety of fruits, vegetables, whole grains, lean proteins, and healthy fats. Minimize processed foods, added sugars, and excessive sodium. Stay hydrated and practice portion control. Consistency is more important than perfection."
    
    # Water tracking
    elif "water" in user_input and ("track" in user_input or "log" in user_input or "add" in user_input):
        st.session_state.water_tracker["glasses"] += 1
        return f"Great job staying hydrated! I've logged another glass of water. You've had {st.session_state.water_tracker['glasses']} glasses today."
    
    # Add this condition in the get_chatbot_response function
    elif "breakfast" in user_input or "morning meal" in user_input:
        if "weight loss" in user_input or "diet" in user_input:
            response = "Here are some healthy breakfast options for weight loss:\n\n"
            response += "1. Greek yogurt with berries and a sprinkle of nuts (300 calories)\n"
            response += "2. Veggie omelet with 2 eggs and spinach (250 calories)\n"
            response += "3. Overnight oats with almond milk and chia seeds (350 calories)\n"
            response += "4. Protein smoothie with spinach, banana, and protein powder (300 calories)\n"
            response += "5. Avocado toast on whole grain bread with a boiled egg (340 calories)\n\n"
            response += "These options are high in protein and fiber to keep you full longer while maintaining a calorie deficit."
            return response
    
    # Fallback response
    else:
        return "I'm your nutrition advisor. I can help with meal planning, provide nutrition information, suggest recipes, or answer questions about healthy eating. What would you like to know?"

# UI Components
def render_sidebar():
    with st.sidebar:
        st.title("🥗 NutriBot")
        st.markdown("Your AI Nutrition Advisor")
        
        st.subheader("About Me")
        if st.session_state.user_info["onboarded"]:
            st.write(f"**Name:** {st.session_state.user_info['name']}")
            st.write(f"**Goal:** {st.session_state.user_info['goal']}")
            if st.session_state.user_info["dietary_preferences"]:
                st.write(f"**Preferences:** {', '.join(st.session_state.user_info['dietary_preferences'])}")
            if st.session_state.user_info["allergies"]:
                st.write(f"**Allergies:** {', '.join(st.session_state.user_info['allergies'])}")
            
            # Water tracker
            st.subheader("💧 Water Tracker")
            st.write(f"Today's count: {st.session_state.water_tracker['glasses']} glasses")
            if st.button("Add a glass"):
                st.session_state.water_tracker["glasses"] += 1
                st.rerun()
        
        st.subheader("Quick Actions")
        if st.button("Generate Meal Plan"):
            user_message = "Can you create a meal plan for me?"
            st.session_state.chat_history.append({"role": "user", "content": user_message})
            bot_response = get_chatbot_response(user_message)
            st.session_state.chat_history.append({"role": "assistant", "content": bot_response})
            st.rerun()
        
        if st.button("Random Healthy Recipe"):
            user_message = "Give me a healthy recipe"
            st.session_state.chat_history.append({"role": "user", "content": user_message})
            bot_response = get_chatbot_response(user_message)
            st.session_state.chat_history.append({"role": "assistant", "content": bot_response})
            st.rerun()
        
        st.markdown("---")
        if st.button("Reset Profile"):
            st.session_state.user_info = {
                "name": "",
                "dietary_preferences": [],
                "allergies": [],
                "goal": "",
                "height": "",
                "weight": "",
                "activity_level": "",
                "onboarded": False
            }
            st.session_state.chat_history = []
            st.rerun()

def show_onboarding():
    st.title("🥗 Welcome to NutriBot")
    st.write("Let's set up your profile to provide personalized nutrition advice.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Your Name", key="name_input")
        goal = st.selectbox(
            "What's your primary goal?",
            ["Weight Loss", "Muscle Gain", "Maintenance", "Improved Energy", "Better Nutrition"],
            key="goal_select"
        )
        dietary_preferences = st.multiselect(
            "Dietary Preferences",
            ["Vegetarian", "Vegan", "Keto", "Paleo", "Gluten-Free", "Dairy-Free", "Low Carb", "Mediterranean"],
            key="diet_multi"
        )
    
    with col2:
        allergies = st.text_input("Any allergies or intolerances? (comma separated)", key="allergies_input")
        height = st.text_input("Height (optional)", key="height_input")
        weight = st.text_input("Weight (optional)", key="weight_input")
        activity_level = st.select_slider(
            "Activity Level",
            options=["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extremely Active"],
            value="Moderately Active",
            key="activity_slider"
        )
    
    if st.button("Save Profile"):
        st.session_state.user_info = {
            "name": name,
            "dietary_preferences": dietary_preferences,
            "allergies": allergies.split(", ") if allergies else [],
            "goal": goal,
            "height": height,
            "weight": weight,
            "activity_level": activity_level,
            "onboarded": True
        }
        
        # Add welcome message to chat
        welcome_message = f"Hi {name}! I'm your personal nutrition advisor. I can help you with meal plans, recipes, and nutrition information to support your {goal.lower()} goal. What would you like help with today?"
        st.session_state.chat_history.append({"role": "assistant", "content": welcome_message})
        st.rerun()

def render_chat_interface():
    st.title("🥗 NutriBot Chat")
    
    # Display chat messages
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # User input
    user_input = st.chat_input("Ask about nutrition, recipes, meal planning...")
    if user_input:
        # Add user message to chat
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = get_chatbot_response(user_input)
                st.markdown(response)
                st.session_state.chat_history.append({"role": "assistant", "content": response})

def main():
    render_sidebar()
    
    if not st.session_state.user_info["onboarded"]:
        show_onboarding()
    else:
        render_chat_interface()

if __name__ == "__main__":
    main()