from typing import List, Dict, Any, Optional

def scale_nutrition_by_weight(
    original_weight_g: float,
    new_weight_g: float,
    calories: float,
    protein_g: float,
    carbs_g: float,
    fat_g: float,
    fiber_g: float = 0.0,
    sugar_g: float = 0.0,
    sodium_mg: float = 0.0,
) -> Dict[str, float]:
    ratio = 1.0 if original_weight_g <= 0 else max(0.0, new_weight_g / original_weight_g)
    return {
        "calories": round(calories * ratio, 1),
        "protein_g": round(protein_g * ratio, 1),
        "carbs_g": round(carbs_g * ratio, 1),
        "fat_g": round(fat_g * ratio, 1),
        "fiber_g": round(fiber_g * ratio, 1),
        "sugar_g": round(sugar_g * ratio, 1),
        "sodium_mg": round(sodium_mg * ratio, 1),
    }

def scale_nutrition_by_servings(
    original_servings: float,
    new_servings: float,
    calories: float,
    protein_g: float,
    carbs_g: float,
    fat_g: float,
    fiber_g: float = 0.0,
    sugar_g: float = 0.0,
    sodium_mg: float = 0.0,
) -> Dict[str, float]:
    ratio = 1.0 if original_servings <= 0 else max(0.0, new_servings / original_servings)
    return {
        "calories": round(calories * ratio, 1),
        "protein_g": round(protein_g * ratio, 1),
        "carbs_g": round(carbs_g * ratio, 1),
        "fat_g": round(fat_g * ratio, 1),
        "fiber_g": round(fiber_g * ratio, 1),
        "sugar_g": round(sugar_g * ratio, 1),
        "sodium_mg": round(sodium_mg * ratio, 1),
    }

def calculate_meal_totals(food_items: List[Any]) -> Dict[str, float]:
    total = {
        "calories": 0.0,
        "protein_g": 0.0,
        "carbs_g": 0.0,
        "fat_g": 0.0,
        "fiber_g": 0.0,
        "sugar_g": 0.0,
        "sodium_mg": 0.0,
    }
    for item in food_items:
        calories = getattr(item, "calories", 0.0) if hasattr(item, "calories") else item.get("calories", 0.0)
        protein = getattr(item, "protein_g", 0.0) if hasattr(item, "protein_g") else item.get("protein_g", 0.0)
        carbs = getattr(item, "carbs_g", 0.0) if hasattr(item, "carbs_g") else item.get("carbs_g", 0.0)
        fat = getattr(item, "fat_g", 0.0) if hasattr(item, "fat_g") else item.get("fat_g", 0.0)
        fiber = getattr(item, "fiber_g", 0.0) if hasattr(item, "fiber_g") else item.get("fiber_g", 0.0)
        sugar = getattr(item, "sugar_g", 0.0) if hasattr(item, "sugar_g") else item.get("sugar_g", 0.0)
        sodium = getattr(item, "sodium_mg", 0.0) if hasattr(item, "sodium_mg") else item.get("sodium_mg", 0.0)

        total["calories"] += float(calories)
        total["protein_g"] += float(protein)
        total["carbs_g"] += float(carbs)
        total["fat_g"] += float(fat)
        total["fiber_g"] += float(fiber)
        total["sugar_g"] += float(sugar)
        total["sodium_mg"] += float(sodium)

    return {k: round(v, 1) for k, v in total.items()}

def calculate_daily_calorie_and_macro_targets(
    age: Optional[int],
    gender: Optional[str],
    height_cm: Optional[float],
    weight_kg: Optional[float],
    activity_level: str = "moderate",
    goal: str = "maintain",
) -> Dict[str, float]:
    w = weight_kg or 70.0
    h = height_cm or 170.0
    a = age or 28
    g = (gender or "other").lower()

    if g == "male":
        bmr = 10.0 * w + 6.25 * h - 5.0 * a + 5.0
    elif g == "female":
        bmr = 10.0 * w + 6.25 * h - 5.0 * a - 161.0
    else:
        bmr = 10.0 * w + 6.25 * h - 5.0 * a - 78.0

    activity_multipliers = {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.725,
        "very_active": 1.9,
    }
    multiplier = activity_multipliers.get(activity_level.lower(), 1.55)
    tdee = bmr * multiplier

    goal_lower = goal.lower()
    if "lose" in goal_lower:
        target_calories = max(1200.0, tdee - 500.0)
    elif "gain" in goal_lower:
        target_calories = tdee + 400.0
    else:
        target_calories = tdee

    protein_g = max(60.0, min(w * 2.0, target_calories * 0.35 / 4.0))
    fat_g = max(40.0, (target_calories * 0.25) / 9.0)
    remaining_cals = max(0.0, target_calories - (protein_g * 4.0 + fat_g * 9.0))
    carb_g = max(50.0, remaining_cals / 4.0)

    water_ml = int(round(w * 35.0 / 250.0) * 250)
    water_ml = max(2000, min(water_ml, 4000))

    return {
        "daily_calorie_target": round(target_calories),
        "protein_target": round(protein_g),
        "carb_target": round(carb_g),
        "fat_target": round(fat_g),
        "daily_water_target_ml": water_ml,
    }
