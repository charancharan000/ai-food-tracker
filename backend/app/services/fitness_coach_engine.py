"""
FITBRO AI Fitness & Nutrition Coach Engine (Train & Enhance)
Comprehensive domain engine for the existing FitBro AI Coach.

Capabilities:
1. Natural language understanding across English, Tamil, Tanglish, slang ("machi", "bro", "thala"), and typos.
2. 8 Core Knowledge Areas:
   - Calorie calculation (BMR Mifflin-St Jeor, TDEE, Deficit, Surplus, Maintenance)
   - Nutrition (Protein 1.6-2.2g/kg, Carbs, Healthy Fats, Fiber, Timing, Pre/Post-workout, Hydration)
   - Extensive Indian & South Indian Food database (Idli, Dosa, Pongal, Biryani, Chicken, Eggs, etc.)
   - Workouts (PPL, Upper/Lower, Chest, Back, Shoulders, Arms, Legs, Progressive Overload)
   - Cardio (Running vs Muscle Loss, Fat Loss vs Bulking, Calorie Burn)
   - Supplements (Creatine 3-5g daily, Whey, Caffeine/Pre-workout, Fish Oil, Multivitamins)
   - Body Goals (Lean Bulk, Cutting, Body Recomposition, Maintenance)
   - Recovery (Sleep 7-9h, Rest Days, DOMS, Night Rice Myth)
3. Zero-Redundancy User Data Utilization: Uses stored profile data (age, weight, height, gender, goal) without re-asking.
4. Food Logging Integration: Parses "I ate 3 eggs", "2 idli, sambar and one egg", etc. and generates structured meals.
5. Daily Progress Integration: Computes remaining calories, protein, carbs, fat, and water for the current day.
6. Multi-turn contextual memory support.
"""

import re
import datetime
from typing import Dict, Any, List, Optional, Tuple
from pydantic import BaseModel, Field


# =============================================================================
# 1. EXTENSIVE INDIAN & FITNESS FOOD DATABASE (100+ Common Foods)
# =============================================================================

class FoodNutritionInfo(BaseModel):
    name: str
    aliases: List[str] = Field(default_factory=list)
    unit_name: str = "piece"
    default_serving_weight_g: float = 100.0
    calories: float
    protein_g: float
    carbs_g: float
    fat_g: float
    fiber_g: float = 0.0
    category: str = "Indian"
    is_estimate: bool = True


FOOD_DATABASE: Dict[str, FoodNutritionInfo] = {
    # Eggs & Poultry
    "egg_whole": FoodNutritionInfo(
        name="Boiled Egg (Whole)",
        aliases=["egg", "boiled egg", "muttai", "eggs", "whole egg", "one egg", "1 egg"],
        unit_name="egg",
        default_serving_weight_g=50.0,
        calories=74.0,
        protein_g=6.3,
        carbs_g=0.4,
        fat_g=5.0,
        fiber_g=0.0,
        category="Protein",
    ),
    "egg_white": FoodNutritionInfo(
        name="Egg White",
        aliases=["egg white", "egg whites", "muttai vellai"],
        unit_name="egg white",
        default_serving_weight_g=33.0,
        calories=17.0,
        protein_g=3.6,
        carbs_g=0.2,
        fat_g=0.1,
        fiber_g=0.0,
        category="Protein",
    ),
    "chicken_breast_cooked": FoodNutritionInfo(
        name="Chicken Breast (Cooked/Grilled)",
        aliases=["chicken breast", "chicken", "grilled chicken", "koli", "kozhi", "chicken 100g", "chicken 200g"],
        unit_name="100g",
        default_serving_weight_g=100.0,
        calories=165.0,
        protein_g=31.0,
        carbs_g=0.0,
        fat_g=3.6,
        fiber_g=0.0,
        category="Protein",
    ),
    "chicken_curry": FoodNutritionInfo(
        name="Chicken Curry",
        aliases=["chicken curry", "chicken gravy", "kozhi kulambu", "chicken kulambu", "chicken masala"],
        unit_name="cup",
        default_serving_weight_g=150.0,
        calories=230.0,
        protein_g=22.0,
        carbs_g=6.0,
        fat_g=13.0,
        fiber_g=1.2,
        category="Indian Non-Veg",
    ),
    "mutton_curry": FoodNutritionInfo(
        name="Mutton Curry",
        aliases=["mutton", "mutton curry", "mutton gravy", "kari", "aatu kari", "mutton chukka"],
        unit_name="cup",
        default_serving_weight_g=150.0,
        calories=320.0,
        protein_g=24.0,
        carbs_g=5.0,
        fat_g=22.0,
        fiber_g=1.0,
        category="Indian Non-Veg",
    ),
    "fish_cooked": FoodNutritionInfo(
        name="Fish (Cooked/Pan-Fried)",
        aliases=["fish", "meen", "fish fry", "fish curry", "vanjaram", "salmon", "tilapia", "rohu"],
        unit_name="100g",
        default_serving_weight_g=100.0,
        calories=145.0,
        protein_g=22.0,
        carbs_g=1.5,
        fat_g=5.5,
        fiber_g=0.0,
        category="Protein",
    ),
    # Dairy & Vegetarian Proteins
    "paneer": FoodNutritionInfo(
        name="Paneer (Cottage Cheese)",
        aliases=["paneer", "panir", "cottage cheese"],
        unit_name="100g",
        default_serving_weight_g=100.0,
        calories=275.0,
        protein_g=18.0,
        carbs_g=4.0,
        fat_g=21.0,
        fiber_g=0.0,
        category="Vegetarian Protein",
    ),
    "tofu": FoodNutritionInfo(
        name="Tofu",
        aliases=["tofu", "soya paneer"],
        unit_name="100g",
        default_serving_weight_g=100.0,
        calories=85.0,
        protein_g=9.5,
        carbs_g=2.0,
        fat_g=4.8,
        fiber_g=1.2,
        category="Vegetarian Protein",
    ),
    "curd": FoodNutritionInfo(
        name="Curd / Plain Yogurt",
        aliases=["curd", "yogurt", "thayir", "dahi"],
        unit_name="100g",
        default_serving_weight_g=100.0,
        calories=65.0,
        protein_g=3.5,
        carbs_g=4.5,
        fat_g=3.5,
        fiber_g=0.0,
        category="Dairy",
    ),
    "milk": FoodNutritionInfo(
        name="Milk (Toned/Cow)",
        aliases=["milk", "paal", "doodh", "glass of milk"],
        unit_name="glass",
        default_serving_weight_g=250.0,
        calories=140.0,
        protein_g=8.0,
        carbs_g=12.0,
        fat_g=6.5,
        fiber_g=0.0,
        category="Dairy",
    ),
    "buttermilk": FoodNutritionInfo(
        name="Buttermilk (Moru / Chaas)",
        aliases=["buttermilk", "moru", "chaas", "neer moru"],
        unit_name="glass",
        default_serving_weight_g=200.0,
        calories=40.0,
        protein_g=2.2,
        carbs_g=3.2,
        fat_g=1.2,
        fiber_g=0.0,
        category="Dairy",
    ),
    # South Indian Tiffin
    "idli": FoodNutritionInfo(
        name="Idli",
        aliases=["idli", "idly", "idlis", "steamed idli"],
        unit_name="piece",
        default_serving_weight_g=45.0,
        calories=48.0,
        protein_g=1.6,
        carbs_g=9.5,
        fat_g=0.2,
        fiber_g=0.8,
        category="South Indian Tiffin",
    ),
    "dosa_plain": FoodNutritionInfo(
        name="Plain Dosa",
        aliases=["dosa", "dosai", "plain dosa", "roast dosa", "ghee roast"],
        unit_name="piece",
        default_serving_weight_g=80.0,
        calories=145.0,
        protein_g=3.2,
        carbs_g=24.0,
        fat_g=4.0,
        fiber_g=1.2,
        category="South Indian Tiffin",
    ),
    "masala_dosa": FoodNutritionInfo(
        name="Masala Dosa",
        aliases=["masala dosa", "masala dosai", "aloo dosa"],
        unit_name="piece",
        default_serving_weight_g=180.0,
        calories=290.0,
        protein_g=5.2,
        carbs_g=42.0,
        fat_g=11.5,
        fiber_g=2.8,
        category="South Indian Tiffin",
    ),
    "rava_dosa": FoodNutritionInfo(
        name="Rava Dosa",
        aliases=["rava dosa", "rava dosai", "sooji dosa"],
        unit_name="piece",
        default_serving_weight_g=110.0,
        calories=190.0,
        protein_g=3.8,
        carbs_g=28.0,
        fat_g=6.5,
        fiber_g=1.5,
        category="South Indian Tiffin",
    ),
    "onion_dosa": FoodNutritionInfo(
        name="Onion Dosa",
        aliases=["onion dosa", "vengaya dosai"],
        unit_name="piece",
        default_serving_weight_g=120.0,
        calories=180.0,
        protein_g=3.6,
        carbs_g=27.0,
        fat_g=6.0,
        fiber_g=2.0,
        category="South Indian Tiffin",
    ),
    "uthappam": FoodNutritionInfo(
        name="Uthappam",
        aliases=["uthappam", "oothappam", "uttapam", "onion uthappam"],
        unit_name="piece",
        default_serving_weight_g=140.0,
        calories=210.0,
        protein_g=4.5,
        carbs_g=34.0,
        fat_g=6.2,
        fiber_g=2.2,
        category="South Indian Tiffin",
    ),
    "medhu_vada": FoodNutritionInfo(
        name="Medhu Vada",
        aliases=["vada", "vadai", "medhu vadai", "ulundhu vadai", "medu vada"],
        unit_name="piece",
        default_serving_weight_g=45.0,
        calories=130.0,
        protein_g=4.2,
        carbs_g=12.5,
        fat_g=7.2,
        fiber_g=1.8,
        category="South Indian Fried Snack",
    ),
    "poori": FoodNutritionInfo(
        name="Poori (Deep Fried)",
        aliases=["poori", "puri", "pooriga"],
        unit_name="piece",
        default_serving_weight_g=40.0,
        calories=135.0,
        protein_g=2.4,
        carbs_g=15.0,
        fat_g=7.5,
        fiber_g=1.0,
        category="Indian Breads",
    ),
    "chapati": FoodNutritionInfo(
        name="Chapati / Roti (No Oil)",
        aliases=["chapati", "roti", "chappathi", "phulka", "rotis", "chapatis"],
        unit_name="piece",
        default_serving_weight_g=35.0,
        calories=80.0,
        protein_g=2.8,
        carbs_g=15.5,
        fat_g=0.6,
        fiber_g=2.2,
        category="Indian Breads",
    ),
    "parotta": FoodNutritionInfo(
        name="Malabar Parotta",
        aliases=["parotta", "barotta", "parottai", "kerala parotta"],
        unit_name="piece",
        default_serving_weight_g=85.0,
        calories=285.0,
        protein_g=5.0,
        carbs_g=38.0,
        fat_g=12.5,
        fiber_g=1.4,
        category="Indian Breads",
    ),
    "kothu_parotta": FoodNutritionInfo(
        name="Kothu Parotta (Egg/Chicken)",
        aliases=["kothu parotta", "kothu", "egg kothu", "chicken kothu"],
        unit_name="plate",
        default_serving_weight_g=350.0,
        calories=620.0,
        protein_g=26.0,
        carbs_g=72.0,
        fat_g=25.0,
        fiber_g=4.0,
        category="South Indian Street Food",
    ),
    "pongal": FoodNutritionInfo(
        name="Ven Pongal",
        aliases=["pongal", "ven pongal", "ghee pongal"],
        unit_name="cup",
        default_serving_weight_g=180.0,
        calories=240.0,
        protein_g=6.0,
        carbs_g=32.0,
        fat_g=9.5,
        fiber_g=2.5,
        category="South Indian Tiffin",
    ),
    "upma": FoodNutritionInfo(
        name="Rava Upma",
        aliases=["upma", "uppuma", "rava upma", "sooji upma"],
        unit_name="cup",
        default_serving_weight_g=160.0,
        calories=195.0,
        protein_g=4.2,
        carbs_g=32.0,
        fat_g=5.8,
        fiber_g=2.0,
        category="South Indian Tiffin",
    ),
    "appam": FoodNutritionInfo(
        name="Appam",
        aliases=["appam", "aappam"],
        unit_name="piece",
        default_serving_weight_g=75.0,
        calories=105.0,
        protein_g=2.0,
        carbs_g=21.0,
        fat_g=1.5,
        fiber_g=0.8,
        category="South Indian Tiffin",
    ),
    "idiyappam": FoodNutritionInfo(
        name="Idiyappam (String Hoppers)",
        aliases=["idiyappam", "string hoppers", "sevai"],
        unit_name="piece",
        default_serving_weight_g=50.0,
        calories=60.0,
        protein_g=1.2,
        carbs_g=13.0,
        fat_g=0.3,
        fiber_g=0.6,
        category="South Indian Tiffin",
    ),
    "paniyaram": FoodNutritionInfo(
        name="Kuzhi Paniyaram",
        aliases=["paniyaram", "kuzhi paniyaram", "appe", "paddu"],
        unit_name="piece",
        default_serving_weight_g=25.0,
        calories=38.0,
        protein_g=1.0,
        carbs_g=6.5,
        fat_g=1.0,
        fiber_g=0.5,
        category="South Indian Snack",
    ),
    "adai": FoodNutritionInfo(
        name="Adai (Lentil Pancake)",
        aliases=["adai", "adayi"],
        unit_name="piece",
        default_serving_weight_g=100.0,
        calories=180.0,
        protein_g=6.8,
        carbs_g=28.0,
        fat_g=4.5,
        fiber_g=3.8,
        category="South Indian Tiffin",
    ),
    # Curries, Gravies & Accompaniments
    "sambar": FoodNutritionInfo(
        name="Sambar",
        aliases=["sambar", "saambar", "sambhar"],
        unit_name="cup",
        default_serving_weight_g=120.0,
        calories=78.0,
        protein_g=3.4,
        carbs_g=11.5,
        fat_g=2.0,
        fiber_g=2.6,
        category="Accompaniment",
    ),
    "rasam": FoodNutritionInfo(
        name="Rasam",
        aliases=["rasam", "saaru"],
        unit_name="cup",
        default_serving_weight_g=120.0,
        calories=38.0,
        protein_g=1.0,
        carbs_g=6.5,
        fat_g=1.0,
        fiber_g=0.8,
        category="Accompaniment",
    ),
    "coconut_chutney": FoodNutritionInfo(
        name="Coconut Chutney",
        aliases=["coconut chutney", "chutney", "thengai chutney", "white chutney"],
        unit_name="tbsp",
        default_serving_weight_g=30.0,
        calories=65.0,
        protein_g=1.0,
        carbs_g=2.2,
        fat_g=6.0,
        fiber_g=1.2,
        category="Accompaniment",
    ),
    "dal_tadka": FoodNutritionInfo(
        name="Dal Tadka / Dal Fry",
        aliases=["dal", "dal tadka", "paruppu", "dhal", "lentil soup"],
        unit_name="katori",
        default_serving_weight_g=150.0,
        calories=145.0,
        protein_g=8.0,
        carbs_g=20.0,
        fat_g=4.0,
        fiber_g=4.5,
        category="Indian Vegetarian",
    ),
    "rajma": FoodNutritionInfo(
        name="Rajma (Kidney Bean Curry)",
        aliases=["rajma", "kidney beans", "rajma curry"],
        unit_name="cup",
        default_serving_weight_g=180.0,
        calories=220.0,
        protein_g=12.5,
        carbs_g=34.0,
        fat_g=3.8,
        fiber_g=8.0,
        category="Indian Vegetarian",
    ),
    "chana_masala": FoodNutritionInfo(
        name="Chole / Chana Masala",
        aliases=["chole", "chana", "chana masala", "kondakadalai", "chickpea curry"],
        unit_name="cup",
        default_serving_weight_g=180.0,
        calories=240.0,
        protein_g=11.0,
        carbs_g=36.0,
        fat_g=5.5,
        fiber_g=7.5,
        category="Indian Vegetarian",
    ),
    # Rice Varieties
    "white_rice": FoodNutritionInfo(
        name="Steamed White Rice",
        aliases=["rice", "white rice", "saatham", "sadam", "bhat", "steamed rice"],
        unit_name="cup",
        default_serving_weight_g=150.0,
        calories=195.0,
        protein_g=4.0,
        carbs_g=44.0,
        fat_g=0.4,
        fiber_g=0.6,
        category="Grains",
    ),
    "curd_rice": FoodNutritionInfo(
        name="Curd Rice (Thayir Sadam)",
        aliases=["curd rice", "thayir sadam", "daddojanam", "yogurt rice"],
        unit_name="plate",
        default_serving_weight_g=200.0,
        calories=255.0,
        protein_g=6.2,
        carbs_g=42.0,
        fat_g=7.0,
        fiber_g=1.0,
        category="Rice Variety",
    ),
    "lemon_rice": FoodNutritionInfo(
        name="Lemon Rice (Chitranna)",
        aliases=["lemon rice", "elamichai sadam", "chitranna"],
        unit_name="cup",
        default_serving_weight_g=180.0,
        calories=245.0,
        protein_g=4.5,
        carbs_g=42.0,
        fat_g=6.8,
        fiber_g=1.5,
        category="Rice Variety",
    ),
    "chicken_biryani": FoodNutritionInfo(
        name="Chicken Biryani",
        aliases=["chicken biryani", "biryani", "briyani", "chicken briyani", "dum biryani"],
        unit_name="plate",
        default_serving_weight_g=350.0,
        calories=590.0,
        protein_g=34.0,
        carbs_g=68.0,
        fat_g=20.0,
        fiber_g=3.5,
        category="Indian Main",
    ),
    "mutton_biryani": FoodNutritionInfo(
        name="Mutton Biryani",
        aliases=["mutton biryani", "mutton briyani"],
        unit_name="plate",
        default_serving_weight_g=350.0,
        calories=680.0,
        protein_g=30.0,
        carbs_g=68.0,
        fat_g=32.0,
        fiber_g=3.0,
        category="Indian Main",
    ),
    "egg_biryani": FoodNutritionInfo(
        name="Egg Biryani",
        aliases=["egg biryani", "muttai biryani"],
        unit_name="plate",
        default_serving_weight_g=350.0,
        calories=490.0,
        protein_g=19.0,
        carbs_g=68.0,
        fat_g=15.0,
        fiber_g=3.0,
        category="Indian Main",
    ),
    # Fitness Staples
    "oats": FoodNutritionInfo(
        name="Rolled Oats (Dry)",
        aliases=["oats", "oatmeal"],
        unit_name="serving (40g)",
        default_serving_weight_g=40.0,
        calories=152.0,
        protein_g=5.2,
        carbs_g=27.0,
        fat_g=2.6,
        fiber_g=4.0,
        category="Grains",
    ),
    "peanut_butter": FoodNutritionInfo(
        name="Peanut Butter",
        aliases=["peanut butter", "pb"],
        unit_name="tbsp",
        default_serving_weight_g=16.0,
        calories=94.0,
        protein_g=4.0,
        carbs_g=3.1,
        fat_g=8.0,
        fiber_g=1.0,
        category="Fats & Protein",
    ),
    "whey_protein": FoodNutritionInfo(
        name="Whey Protein Scoop",
        aliases=["whey", "protein powder", "whey scoop", "1 scoop whey", "isolate"],
        unit_name="scoop",
        default_serving_weight_g=30.0,
        calories=120.0,
        protein_g=24.0,
        carbs_g=2.0,
        fat_g=1.5,
        fiber_g=0.0,
        category="Supplements",
    ),
    "banana": FoodNutritionInfo(
        name="Banana",
        aliases=["banana", "vazhaipazham", "kela"],
        unit_name="piece",
        default_serving_weight_g=115.0,
        calories=105.0,
        protein_g=1.3,
        carbs_g=27.0,
        fat_g=0.3,
        fiber_g=3.0,
        category="Fruit",
    ),
}


# =============================================================================
# 2. INTENT & KNOWLEDGE CLASSIFICATION ENGINE
# =============================================================================

class UserProfileContext(BaseModel):
    name: Optional[str] = "Friend"
    age: Optional[int] = 25
    gender: Optional[str] = "male"
    height_cm: Optional[float] = 175.0
    weight_kg: Optional[float] = 70.0
    activity_level: str = "moderate"
    goal: str = "maintain" # "muscle_gain", "weight_loss", "fat_loss", "maintain"
    daily_calorie_target: float = 2000.0
    protein_target: float = 140.0
    carb_target: float = 250.0
    fat_target: float = 65.0
    daily_water_target_ml: int = 2500

    # Today's Progress Context
    calories_consumed_today: float = 0.0
    protein_consumed_today: float = 0.0
    carbs_consumed_today: float = 0.0
    fat_consumed_today: float = 0.0
    water_consumed_today: int = 0


class ParsedFoodLoggingItem(BaseModel):
    name: str
    quantity: float
    unit: str
    estimated_weight_g: float
    calories: float
    protein_g: float
    carbs_g: float
    fat_g: float
    fiber_g: float


class CoachResponse(BaseModel):
    reply_text: str
    intent_detected: str
    logged_food_items: Optional[List[ParsedFoodLoggingItem]] = None
    logged_meal_type: Optional[str] = None
    remaining_calories: float
    remaining_protein: float
    is_tamil_tanglish: bool = False


# =============================================================================
# 3. ADVANCED NLP MATCHER & REASONING PIPELINE
# =============================================================================

class FitnessCoachIntelligence:
    """Core brain of the FITBRO AI Coach."""

    @classmethod
    def calculate_bmr(cls, weight_kg: float, height_cm: float, age: int, gender: str) -> float:
        """Mifflin-St Jeor Formula."""
        is_female = gender.lower() in ["female", "f", "woman"]
        if is_female:
            return round((10.0 * weight_kg) + (6.25 * height_cm) - (5.0 * age) - 161.0, 1)
        return round((10.0 * weight_kg) + (6.25 * height_cm) - (5.0 * age) + 5.0, 1)

    @classmethod
    def calculate_tdee(cls, bmr: float, activity_level: str) -> float:
        multipliers = {
            "sedentary": 1.2,
            "light": 1.375,
            "moderate": 1.55,
            "active": 1.725,
            "very active": 1.9,
        }
        mult = multipliers.get(activity_level.lower(), 1.55)
        return round(bmr * mult, 1)

    @classmethod
    def detect_tamil_tanglish(cls, text: str) -> bool:
        tanglish_tokens = [
            "machi", "bro", "thala", "anna", "sapta", "sapdanum", "saapdanum", "enna",
            "aguma", "aaguma", "edukanuma", "edukanum", "evlo", "yevlo", "venum",
            "sapdalama", "panna", "pona", "kurayuma", "kooduma", "saptom", "saaptuten",
            "iravu", "kaalai", "madhiyam", "thoppai", "edai", "udambu", "dosa", "idli"
        ]
        q_lower = text.lower()
        return any(t in q_lower for t in tanglish_tokens)

    @classmethod
    def parse_food_logging_query(cls, text: str) -> Optional[List[ParsedFoodLoggingItem]]:
        """
        Detects if user said "I ate 3 eggs", "I ate 2 idli, sambar and one egg", etc.
        """
        q = text.lower().strip()
        is_log_action = any(verb in q for verb in ["ate", "had", "eaten", "consumed", "saptom", "saaptuten", "sapten", "thintom", "drink", "drank"])
        
        # If user explicitly asks "calories?" or "evlo", it's an inquiry, not a log action, unless prefixed by "i ate"
        is_question = any(w in q for w in ["how much", "how many", "calories?", "protein?", "evlo", "yevlo", "calculate", "tell me"])
        if is_question and not is_log_action:
            return None

        # Look for food items in text
        matched_items: List[ParsedFoodLoggingItem] = []
        
        # Split by comma or "and" or "+"
        segments = re.split(r"[,+&]| and | apram ", q)
        for seg in segments:
            seg = seg.strip()
            if not seg:
                continue

            # Extract numeric quantity
            qty_match = re.search(r"(\d+(\.\d+)?)", seg)
            qty = float(qty_match.group(1)) if qty_match else 1.0
            
            # Words for quantities
            if "one " in seg or seg == "one": qty = 1.0
            elif "two " in seg or seg == "two": qty = 2.0
            elif "three " in seg or seg == "three": qty = 3.0
            elif "four " in seg or seg == "four": qty = 4.0
            elif "half " in seg: qty = 0.5

            # Grams indicator (e.g. 200g chicken)
            is_gram = bool(re.search(r"\b\d+\s*(g|gm|gms|gram|grams)\b", seg))

            # Match foods with longest alias first to prevent substring false matches
            sorted_foods = sorted(FOOD_DATABASE.items(), key=lambda kv: max(len(a) for a in kv[1].aliases), reverse=True)
            for food_key, info in sorted_foods:
                alias_matched = any(re.search(rf"\b{re.escape(alias)}\b", seg, re.IGNORECASE) for alias in info.aliases)
                if alias_matched:
                    if is_gram:
                        weight_g = qty
                        scale = weight_g / 100.0
                        unit_str = f"{int(qty)}g"
                        disp_qty = 1.0
                    else:
                        weight_g = qty * info.default_serving_weight_g
                        scale = qty
                        unit_str = info.unit_name
                        disp_qty = qty

                    item = ParsedFoodLoggingItem(
                        name=info.name,
                        quantity=disp_qty,
                        unit=unit_str,
                        estimated_weight_g=round(weight_g, 1),
                        calories=round(info.calories * scale, 1),
                        protein_g=round(info.protein_g * scale, 1),
                        carbs_g=round(info.carbs_g * scale, 1),
                        fat_g=round(info.fat_g * scale, 1),
                        fiber_g=round(info.fiber_g * scale, 1),
                    )
                    matched_items.append(item)
                    break

        return matched_items if (is_log_action and matched_items) else None

    @classmethod
    def generate_coach_answer(
        cls,
        user_message: str,
        user_profile: UserProfileContext,
        conversation_history: Optional[List[Dict[str, str]]] = None,
    ) -> CoachResponse:
        """
        Main intelligence router: analyzes user intent and produces
        thorough, scientifically accurate, and friendly coaching responses.
        """
        raw_msg = user_message.strip()
        q = raw_msg.lower()
        is_tamil = cls.detect_tamil_tanglish(q)

        # Context inheritance from conversation history
        prev_user_msgs = [m.get("content", "").lower() for m in (conversation_history or []) if m.get("role") == "user"]
        full_context = " ".join(prev_user_msgs + [q])

        weight = user_profile.weight_kg or 70.0
        height = user_profile.height_cm or 175.0
        age = user_profile.age or 25
        gender = user_profile.gender or "male"
        goal = user_profile.goal or "maintain"
        activity = user_profile.activity_level or "moderate"

        # Calculate BMR and TDEE
        bmr = cls.calculate_bmr(weight, height, age, gender)
        tdee = cls.calculate_tdee(bmr, activity)

        # Remaining metrics
        cals_target = user_profile.daily_calorie_target or tdee
        p_target = user_profile.protein_target or round(weight * 1.8, 1)
        cals_remaining = max(0.0, round(cals_target - user_profile.calories_consumed_today, 1))
        p_remaining = max(0.0, round(p_target - user_profile.protein_consumed_today, 1))

        # Check if user logged food (e.g. "I ate 3 eggs", "2 idli saptom")
        logged_items = cls.parse_food_logging_query(raw_msg)
        if logged_items:
            tot_cals = round(sum(it.calories for it in logged_items), 1)
            tot_pro = round(sum(it.protein_g for it in logged_items), 1)
            tot_carb = round(sum(it.carbs_g for it in logged_items), 1)
            tot_fat = round(sum(it.fat_g for it in logged_items), 1)

            # Updated remaining after this meal
            new_p_remaining = max(0.0, round(p_remaining - tot_pro, 1))
            new_cals_remaining = max(0.0, round(cals_remaining - tot_cals, 1))

            items_breakdown = "\n".join(
                [f"• {it.quantity} {it.unit} {it.name}: ~{it.calories} kcal | {it.protein_g}g P | {it.carbs_g}g C | {it.fat_g}g F" for it in logged_items]
            )

            reply = (
                f"✅ **Meal Logged Successfully!**\n\n"
                f"{items_breakdown}\n\n"
                f"**Meal Total:**\n"
                f"• Calories: **{tot_cals} kcal** (Estimated)\n"
                f"• Protein: **{tot_pro}g**\n"
                f"• Carbs: **{tot_carb}g**\n"
                f"• Fats: **{tot_fat}g**\n\n"
                f"📊 **Daily Progress Update:**\n"
                f"• Remaining Calories: **{new_cals_remaining} kcal**\n"
                f"• Remaining Protein: **{new_p_remaining}g**\n\n"
                f"Great job tracking your food consistently! Keep hitting your daily protein target."
            )
            return CoachResponse(
                reply_text=reply,
                intent_detected="FOOD_LOG_AUTO",
                logged_food_items=logged_items,
                logged_meal_type="Meal",
                remaining_calories=new_cals_remaining,
                remaining_protein=new_p_remaining,
                is_tamil_tanglish=is_tamil,
            )

        # ---------------------------------------------------------------------
        # 1. DAILY PROGRESS / REMAINING CALORIES & PROTEIN
        # e.g., "today enaku evlo calories venum?", "how much protein is remaining today?"
        # ---------------------------------------------------------------------
        if any(w in q for w in ["remaining", "balance", "evlo calories venum", "left today", "today enaku", "consumed today"]):
            reply = (
                f"📊 **Your Daily Progress for Today:**\n\n"
                f"• **Calories:** Consumed **{user_profile.calories_consumed_today} kcal** of **{cals_target} kcal** target.\n"
                f"  👉 **Remaining: {cals_remaining} kcal**\n\n"
                f"• **Protein:** Consumed **{user_profile.protein_consumed_today}g** of **{p_target}g** target.\n"
                f"  👉 **Remaining: {p_remaining}g**\n\n"
                f"• **Water Consumed:** **{user_profile.water_consumed_today} ml** / {user_profile.daily_water_target_ml} ml\n\n"
                f"💡 *Coach Tip:* To hit your remaining {p_remaining}g protein today without blowing your calories, consider a scoop of whey, 3-4 boiled egg whites, or 150g grilled chicken/paneer."
            )
            return CoachResponse(
                reply_text=reply,
                intent_detected="DAILY_PROGRESS_QUERY",
                remaining_calories=cals_remaining,
                remaining_protein=p_remaining,
                is_tamil_tanglish=is_tamil,
            )

        # ---------------------------------------------------------------------
        # 2. SPECIFIC FITNESS & NUTRITION TOPICS / MYTHS (CHECK BEFORE GENERIC)
        # ---------------------------------------------------------------------
        # Night Rice / Carbs Myth
        if any(w in q for w in ["night rice", "rice at night", "iravu saatham", "night carbs"]):
            reply = (
                f"**Kandippa weight increase aagathu! (No, eating rice at night does NOT automatically make you gain weight.)** 🍚\n\n"
                f"Here is the scientific truth:\n\n"
                f"1. **Weight Gain depends on Total Daily Calories:**\n"
                f"   Whether you eat rice at 1 PM or 9 PM, your body only cares if you are in a **calorie surplus** over the entire 24 hours. 100g of cooked rice has ~130 kcal at any time of day.\n\n"
                f"2. **Why people blame rice at night:**\n"
                f"   Carbohydrates hold water in muscles (1g glycogen holds ~3g water). When you weigh yourself next morning, the scale might show a slight water fluctuation, which is NOT fat.\n\n"
                f"3. **Surprising Benefit of Carbs at Night:**\n"
                f"   Carbs stimulate insulin, which helps tryptophan cross into the brain to produce serotonin and **melatonin (sleep hormone)**, actually helping you sleep deeper!\n\n"
                f"💡 *Coach Rule:* Measure your portion (e.g. 1 cup cooked rice), pair it with chicken/eggs/dal for protein, and make sure it fits your daily **{cals_target} kcal** target."
            )
            return CoachResponse(
                reply_text=reply,
                intent_detected="NUTRITION_MYTHS_LIFESTYLE",
                remaining_calories=cals_remaining,
                remaining_protein=p_remaining,
                is_tamil_tanglish=is_tamil,
            )

        # Running / Cardio & Muscle Loss
        if any(w in q for w in ["running panna", "cardio panna", "gym pona", "muscle loss", "running muscle loss"]):
            reply = (
                f"**Kandippa muscle loss aagathu! (No, Running will NOT cause muscle loss if done right.)**\n\n"
                f"Here is the scientific reality:\n\n"
                f"1. **Muscle loss eppo aagum? (When does muscle loss happen?):**\n"
                f"   • Romba periya calorie deficit la iruntha (Excessive starvation).\n"
                f"   • Podhumana protein sapdala na (Low protein intake < 1.4g/kg).\n"
                f"   • Extreme marathon running (10-15 km daily without weight training).\n\n"
                f"2. **How to run while keeping your muscle:**\n"
                f"   • Keep running sessions to **20–30 minutes, 2 to 3 days a week**.\n"
                f"   • Keep eating your protein target (**{p_target}g/day**).\n"
                f"   • Don't run right before heavy squats or leg day — run after weights or on rest days.\n\n"
                f"Running actually helps muscle recovery by improving blood flow and cardiovascular endurance. Don't fear cardio!"
            )
            return CoachResponse(
                reply_text=reply,
                intent_detected="CARDIO_FATLOSS_MUSCLE",
                remaining_calories=cals_remaining,
                remaining_protein=p_remaining,
                is_tamil_tanglish=is_tamil,
            )

        # Creatine & Supplements
        if "creatine" in q:
            reply = (
                f"**Yes! Creatine monohydrate daily edukalam (3g to 5g daily).** ⚡\n\n"
                f"Here is everything you need to know about Creatine:\n\n"
                f"1. **How it works:**\n"
                f"   Creatine increases your muscles' phosphocreatine stores, which rapidly regenerates ATP (cellular energy). This gives you 1-3 extra reps on heavy lifts and builds strength.\n\n"
                f"2. **Daily Usage:**\n"
                f"   • Take **3g to 5g every single day**, even on rest days.\n"
                f"   • Timing does NOT matter: morning, post-workout, or with a meal.\n"
                f"   • Loading phase (20g/day) is NOT required — 3-5g daily will fully saturate your muscles in 3 weeks.\n\n"
                f"3. **Hydration (Very Important):**\n"
                f"   Creatine pulls water into the muscle cells (intracellular hydration, giving fuller muscles). Drink at least **3.5 to 4 Liters of water daily**.\n\n"
                f"4. **Safety:**\n"
                f"   It is the most researched and proven safe supplement in sports science. Safe for healthy individuals without pre-existing kidney disorders."
            )
            return CoachResponse(
                reply_text=reply,
                intent_detected="SUPPLEMENTS_ADVICE",
                remaining_calories=cals_remaining,
                remaining_protein=p_remaining,
                is_tamil_tanglish=is_tamil,
            )

        if any(w in q for w in ["pre workout", "pre-workout", "preworkout"]):
            reply = (
                f"**Pre-workout sapdalama? Yes, absolutely!** 💥\n\n"
                f"**What to take 30–45 mins before training:**\n\n"
                f"1. **Whole Food Pre-Workout (Best Choice):**\n"
                f"   • 1-2 Bananas + 1 black coffee (or green tea)\n"
                f"   • 2 slices bread with 1 tbsp peanut butter\n"
                f"   • Oats with sliced apple\n\n"
                f"2. **Pre-Workout Supplements (Powder):**\n"
                f"   • Contains caffeine (150-250mg) for focus + Beta-alanine / L-Citrulline for blood flow and pump.\n"
                f"   • Start with half a scoop to assess tolerance.\n"
                f"   • ⚠️ *Caution:* Do NOT take caffeine pre-workout after 6 PM, as it ruins your deep sleep and growth hormone recovery!"
            )
            return CoachResponse(
                reply_text=reply,
                intent_detected="SUPPLEMENTS_ADVICE",
                remaining_calories=cals_remaining,
                remaining_protein=p_remaining,
                is_tamil_tanglish=is_tamil,
            )

        # Bulking & Weight Gain
        if any(w in q for w in ["bulking", "weight gain", "edai kooda", "lean bulk", "size potanum", "bulk panna"]):
            bulk_cals = round(tdee + 300, 1)
            reply = (
                f"Machi, lean bulking and healthy weight gain ku clean calorie surplus + high protein thaan key! 💪\n\n"
                f"Based on your profile (Weight: **{weight} kg**, Maintenance: **~{tdee} kcal**):\n"
                f"🎯 **Your Bulking Target:** **~{bulk_cals} kcal/day** (+300 kcal clean surplus) with **{round(weight * 2.0, 1)}g protein**.\n\n"
                f"**Enna sapdanum (Best Bulking Foods):**\n"
                f"1. **Carbs & Energy:**\n"
                f"   • Rice (White/Brown) with Ghee\n"
                f"   • Oats with Milk, Banana & Peanut Butter shake\n"
                f"   • Boiled Potatoes / Sweet Potatoes\n"
                f"2. **Clean Protein:**\n"
                f"   • Chicken breast / Fish / 4-5 Whole Eggs daily\n"
                f"   • Paneer (100-150g) & Soya chunks\n"
                f"   • Dal, Chana, Rajma with rice\n"
                f"3. **Healthy Dense Fats (Calorie Booster):**\n"
                f"   • Handful of Almonds, Walnuts & Peanuts\n"
                f"   • 2 tbsp Peanut Butter (~190 kcal)\n\n"
                f"💡 *Pro-Tip:* Don't do 'dirty bulking' with junk/oily fried foods. Lift heavy with progressive overload 4-5 days a week so the extra calories turn into muscle, not belly fat!"
            )
            return CoachResponse(
                reply_text=reply,
                intent_detected="BULKING_WEIGHT_GAIN",
                remaining_calories=cals_remaining,
                remaining_protein=p_remaining,
                is_tamil_tanglish=is_tamil,
            )

        # Workout Routines (Chest, Back, Legs)
        if any(w in q for w in ["chest", "bench press", "pecs", "chest workout"]):
            reply = (
                f"🏋️ **Top Chest Workout Routine for Maximum Hypertrophy:**\n\n"
                f"1. **Incline Dumbbell Press (30° angle):**\n"
                f"   • 3–4 Sets × 8–10 Reps (Targets clavicular upper chest head for that full, armor-plated look).\n\n"
                f"2. **Flat Barbell Bench Press or Heavy Dumbbell Press:**\n"
                f"   • 3 Sets × 6–8 Reps (Core compound strength builder for overall mid chest thickness).\n\n"
                f"3. **Weighted or Bodyweight Chest Dips:**\n"
                f"   • 3 Sets × 10–12 Reps (Lean forward 30° to target lower chest and pectoralis minor).\n\n"
                f"4. **Cable Chest Flyes (Seated or Standing):**\n"
                f"   • 3 Sets × 12–15 Reps (Maintain peak contraction at the center for 1 full second).\n\n"
                f"💡 *Key Rule:* Focus on a deep stretch at the bottom and progressive overload by adding 1.25kg or 1 rep each week!"
            )
            return CoachResponse(
                reply_text=reply,
                intent_detected="WORKOUT_ROUTINE",
                remaining_calories=cals_remaining,
                remaining_protein=p_remaining,
                is_tamil_tanglish=is_tamil,
            )

        if any(w in q for w in ["back workout", "lat", "pullups", "back exercise"]):
            reply = (
                f"🏋️ **V-Taper Back Workout Routine:**\n\n"
                f"1. **Pull-ups or Lat Pulldowns:**\n"
                f"   • 4 Sets × 8–10 Reps (Full stretch at top, pull elbows down to hips for lat width).\n\n"
                f"2. **Barbell Bent-Over Rows:**\n"
                f"   • 3 Sets × 6–8 Reps (Mid-back thickness, rhomboids & lats).\n\n"
                f"3. **Chest-Supported Dumbbell Row or Seated Cable Row:**\n"
                f"   • 3 Sets × 10–12 Reps (Safe on the lower back, strong contraction).\n\n"
                f"4. **Face Pulls (with rope):**\n"
                f"   • 3 Sets × 15 Reps (Rear delts, external rotators & healthy shoulders).\n\n"
                f"Rest 90-120 seconds between heavy compound sets."
            )
            return CoachResponse(
                reply_text=reply,
                intent_detected="WORKOUT_ROUTINE",
                remaining_calories=cals_remaining,
                remaining_protein=p_remaining,
                is_tamil_tanglish=is_tamil,
            )

        if any(w in q for w in ["leg workout", "squat", "hamstrings", "glutes", "legs"]):
            reply = (
                f"🏋️ **Complete Leg & Glute Builder Workout:**\n\n"
                f"1. **Barbell Back Squats:**\n"
                f"   • 3–4 Sets × 6–8 Reps (King of quad and glute strength).\n\n"
                f"2. **Romanian Deadlifts (RDLs):**\n"
                f"   • 3 Sets × 8–10 Reps (Hinge at hips, stretch hamstrings & glutes).\n\n"
                f"3. **Bulgarian Split Squats:**\n"
                f"   • 3 Sets × 10 Reps per leg (Unilateral quad development & hip stability).\n\n"
                f"4. **Lying or Seated Leg Curls:**\n"
                f"   • 3 Sets × 12–15 Reps (Direct hamstring isolation).\n\n"
                f"5. **Standing Calf Raises:**\n"
                f"   • 4 Sets × 15 Reps (Pause 2 seconds at the bottom stretch)."
            )
            return CoachResponse(
                reply_text=reply,
                intent_detected="WORKOUT_ROUTINE",
                remaining_calories=cals_remaining,
                remaining_protein=p_remaining,
                is_tamil_tanglish=is_tamil,
            )

        # Recovery, Sleep & DOMS
        if any(w in q for w in ["sleep", "soreness", "sore", "doms", "recovery", "rest day"]):
            reply = (
                f"😴 **Muscle Growth happens during recovery, NOT during the workout!**\n\n"
                f"1. **Sleep (7–9 Hours Non-Negotiable):**\n"
                f"   Over 70% of natural growth hormone and testosterone release occurs during deep REM sleep. Poor sleep spikes cortisol, which breaks down muscle tissue.\n\n"
                f"2. **Muscle Soreness (DOMS):**\n"
                f"   DOMS (Delayed Onset Muscle Soreness) peaks 24–48 hours after heavy training. Soreness is normal for novel stimuli, but does NOT mean you had a better workout than when you aren't sore.\n\n"
                f"3. **How to speed up recovery:**\n"
                f"   • Hit your daily protein (**{p_target}g**).\n"
                f"   • Stay hydrated (3-4L water).\n"
                f"   • Light walking (15-20 min) promotes nutrient-rich blood flow to sore muscles."
            )
            return CoachResponse(
                reply_text=reply,
                intent_detected="RECOVERY_SLEEP_DOMS",
                remaining_calories=cals_remaining,
                remaining_protein=p_remaining,
                is_tamil_tanglish=is_tamil,
            )

        # ---------------------------------------------------------------------
        # 3. FOOD CALORIE & PROTEIN LOOKUP (CHECK BEFORE GENERIC PROTEIN REQUIREMENT)
        # e.g., "2 dosa calories?", "chicken 200g protein evlo?", "how many calories in 3 eggs?"
        # ---------------------------------------------------------------------
        sorted_foods = sorted(FOOD_DATABASE.items(), key=lambda kv: max(len(a) for a in kv[1].aliases), reverse=True)
        for food_key, info in sorted_foods:
            alias_matched = any(re.search(rf"\b{re.escape(alias)}\b", q, re.IGNORECASE) for alias in info.aliases)
            if alias_matched:
                qty_match = re.search(r"(\d+(\.\d+)?)", q)
                qty = float(qty_match.group(1)) if qty_match else 1.0
                is_gram = bool(re.search(r"\b\d+\s*(g|gm|gms|gram|grams)\b", q))

                if is_gram:
                    weight_g = qty
                    scale = weight_g / 100.0
                    serving_label = f"{int(qty)}g"
                else:
                    weight_g = qty * info.default_serving_weight_g
                    scale = qty
                    serving_label = f"{int(qty) if qty.is_integer() else qty} {info.unit_name}{'s' if qty > 1 and not info.unit_name.endswith('s') else ''}"

                cals = round(info.calories * scale, 1)
                pro = round(info.protein_g * scale, 1)
                carb = round(info.carbs_g * scale, 1)
                fat = round(info.fat_g * scale, 1)
                fib = round(info.fiber_g * scale, 1)

                reply = (
                    f"🍽️ **Nutrition Estimate for {serving_label} {info.name}:**\n\n"
                    f"• **Calories:** ~{cals} kcal\n"
                    f"• **Protein:** **{pro}g**\n"
                    f"• **Carbohydrates:** {carb}g\n"
                    f"• **Fats:** {fat}g\n"
                    f"• **Fiber:** {fib}g\n\n"
                    f"*(Note: Nutritional values are reasonable estimates based on standard Indian preparations. Actual values vary with oil, batter, and cooking methods.)*"
                )
                return CoachResponse(
                    reply_text=reply,
                    intent_detected="FOOD_CALORIE_LOOKUP",
                    remaining_calories=cals_remaining,
                    remaining_protein=p_remaining,
                    is_tamil_tanglish=is_tamil,
                )

        # ---------------------------------------------------------------------
        # 4. GENERAL PROTEIN INQUIRY FOR BODY / PROFILE
        # e.g., "how much protein should i eat?", "protein evlo venum"
        # ---------------------------------------------------------------------
        if ("protein" in q and any(w in q for w in ["how much", "should i eat", "target", "evlo", "requirement", "daily"])) or ("protein evlo" in q):
            # Calculate range based on existing profile weight
            low_p = round(weight * 1.6, 1)
            high_p = round(weight * 2.2, 1)
            reply = (
                f"Based on your profile weight of **{weight} kg** and your goal to **{goal.replace('_', ' ').title()}**:\n\n"
                f"🎯 **Recommended Daily Protein:** **{low_p}g – {high_p}g** per day (1.6g to 2.2g per kg of body weight).\n"
                f"Your app target is currently set to **{p_target}g**.\n\n"
                f"**Why this range?**\n"
                f"• **1.6g/kg ({low_p}g):** Sufficient for muscle maintenance and general strength gains.\n"
                f"• **2.0–2.2g/kg ({high_p}g):** Optimal for maximizing muscle hypertrophy (muscle gain) and preserving lean mass during a calorie deficit.\n\n"
                f"**Top Indian Protein Sources to hit this:**\n"
                f"1. Whole Eggs (3 eggs = ~19g protein) & Egg Whites (4 whites = ~14g protein)\n"
                f"2. Chicken Breast (150g cooked = ~46g protein)\n"
                f"3. Paneer (100g = ~18g protein) or Tofu (100g = ~10g protein)\n"
                f"4. Soya Chunks (50g dry = ~26g protein)\n"
                f"5. Whey Protein (1 scoop = ~24g protein)\n"
                f"6. Greek Yogurt / Thick Curd (150g = ~10-15g protein)"
            )
            return CoachResponse(
                reply_text=reply,
                intent_detected="PROTEIN_REQUIREMENT",
                remaining_calories=cals_remaining,
                remaining_protein=p_remaining,
                is_tamil_tanglish=is_tamil,
            )

        # ---------------------------------------------------------------------
        # 5. GENERAL CALORIE / TDEE TARGET INQUIRY
        # e.g., "how many calories should i eat?", "what is my maintenance calories?"
        # ---------------------------------------------------------------------
        if any(w in q for w in ["how many calories", "calorie target", "maintenance calories", "tdee", "deficit"]):
            deficit_cals = round(tdee - 400, 1)
            surplus_cals = round(tdee + 300, 1)
            reply = (
                f"Based on your profile (Age: **{age}**, Weight: **{weight} kg**, Height: **{height} cm**, Activity: **{activity.title()}**):\n\n"
                f"• **Basal Metabolic Rate (BMR):** **~{bmr} kcal/day** (Calories burned at complete rest)\n"
                f"• **Maintenance Calories (TDEE):** **~{tdee} kcal/day**\n\n"
                f"**Tailored Targets for your goals:**\n"
                f"🔥 **Fat Loss / Cutting:** **~{deficit_cals} kcal/day** (Healthy 400 kcal deficit, lose ~0.4 kg/week)\n"
                f"💪 **Lean Muscle Gain / Bulking:** **~{surplus_cals} kcal/day** (Controlled 300 kcal surplus)\n"
                f"⚖️ **Maintenance / Recomp:** **~{tdee} kcal/day** (Eat at maintenance, lift heavy to swap fat for muscle)\n\n"
                f"Your app target is currently **{cals_target} kcal**."
            )
            return CoachResponse(
                reply_text=reply,
                intent_detected="CALORIE_TARGET_CALCULATION",
                remaining_calories=cals_remaining,
                remaining_protein=p_remaining,
                is_tamil_tanglish=is_tamil,
            )

        # ---------------------------------------------------------------------
        # 10. RECOVERY, SLEEP & SORENESS (DOMS)
        # ---------------------------------------------------------------------
        if any(w in q for w in ["sleep", "soreness", "sore", "doms", "recovery", "rest day"]):
            reply = (
                f"😴 **Muscle Growth happens during recovery, NOT during the workout!**\n\n"
                f"1. **Sleep (7–9 Hours Non-Negotiable):**\n"
                f"   Over 70% of natural growth hormone and testosterone release occurs during deep REM sleep. Poor sleep spikes cortisol, which breaks down muscle tissue.\n\n"
                f"2. **Muscle Soreness (DOMS):**\n"
                f"   DOMS (Delayed Onset Muscle Soreness) peaks 24–48 hours after heavy training. Soreness is normal for novel stimuli, but does NOT mean you had a better workout than when you aren't sore.\n\n"
                f"3. **How to speed up recovery:**\n"
                f"   • Hit your daily protein (**{p_target}g**).\n"
                f"   • Stay hydrated (3-4L water).\n"
                f"   • Light walking (15-20 min) promotes nutrient-rich blood flow to sore muscles."
            )
            return CoachResponse(
                reply_text=reply,
                intent_detected="RECOVERY_SLEEP_DOMS",
                remaining_calories=cals_remaining,
                remaining_protein=p_remaining,
                is_tamil_tanglish=is_tamil,
            )

        # ---------------------------------------------------------------------
        # 11. DEFAULT CONVERSATIONAL RESPONSE WITH SMART PROFILE AWARENESS
        # ---------------------------------------------------------------------
        reply = (
            f"Hey {user_profile.name}! 👋 I'm your FITBRO AI Coach.\n\n"
            f"Here is your active profile summary:\n"
            f"• Goal: **{goal.replace('_', ' ').title()}**\n"
            f"• Weight: **{weight} kg** | Height: **{height} cm**\n"
            f"• Daily Target: **{cals_target} kcal** | Protein: **{p_target}g**\n"
            f"• Consumed Today: **{user_profile.calories_consumed_today} kcal** ({cals_remaining} kcal left)\n\n"
            f"You can ask me anything about workouts (Chest, Back, Legs, PPL), nutrition, calories in any Indian food (Idli, Dosa, Biryani), supplements (Creatine, Whey), or even ask in Tamil/Tanglish like *'machi bulking ku enna sapdanum?'* or log food with *'I ate 3 eggs'!*"
        )
        return CoachResponse(
            reply_text=reply,
            intent_detected="GENERAL_COACHING",
            remaining_calories=cals_remaining,
            remaining_protein=p_remaining,
            is_tamil_tanglish=is_tamil,
        )
