import pytest
from app.services.nutrition_calc import (
    scale_nutrition_by_weight,
    scale_nutrition_by_servings,
    calculate_meal_totals,
    calculate_daily_calorie_and_macro_targets
)

def test_exact_proportional_weight_scaling():
    res = scale_nutrition_by_weight(
        original_weight_g=300.0,
        new_weight_g=450.0,
        calories=600.0,
        protein_g=30.0,
        carbs_g=80.0,
        fat_g=15.0,
        fiber_g=4.0,
        sugar_g=6.0,
        sodium_mg=500.0
    )
    assert res["calories"] == 900.0
    assert res["protein_g"] == 45.0
    assert res["carbs_g"] == 120.0
    assert res["fat_g"] == 22.5
    assert res["fiber_g"] == 6.0
    assert res["sugar_g"] == 9.0
    assert res["sodium_mg"] == 750.0

def test_servings_scaling():
    res = scale_nutrition_by_servings(
        original_servings=1.0,
        new_servings=2.5,
        calories=200.0,
        protein_g=10.0,
        carbs_g=25.0,
        fat_g=5.0
    )
    assert res["calories"] == 500.0
    assert res["protein_g"] == 25.0
    assert res["carbs_g"] == 62.5
    assert res["fat_g"] == 12.5

def test_calculate_meal_totals():
    items = [
        {"name": "Rice", "calories": 285.0, "protein_g": 5.8, "carbs_g": 62.0, "fat_g": 0.6, "fiber_g": 1.2, "sugar_g": 0.2, "sodium_mg": 15.0},
        {"name": "Chicken", "calories": 280.0, "protein_g": 26.0, "carbs_g": 8.0, "fat_g": 16.0, "fiber_g": 2.1, "sugar_g": 3.0, "sodium_mg": 620.0},
        {"name": "Dal", "calories": 140.0, "protein_g": 8.5, "carbs_g": 20.0, "fat_g": 3.2, "fiber_g": 4.5, "sugar_g": 1.5, "sodium_mg": 450.0},
        {"name": "Salad", "calories": 35.0, "protein_g": 1.5, "carbs_g": 7.0, "fat_g": 0.3, "fiber_g": 2.5, "sugar_g": 3.2, "sodium_mg": 25.0},
    ]
    totals = calculate_meal_totals(items)
    assert totals["calories"] == 740.0
    assert totals["protein_g"] == 41.8
    assert totals["carbs_g"] == 97.0
    assert totals["fat_g"] == 20.1

def test_calculate_daily_calorie_and_macro_targets():
    targets = calculate_daily_calorie_and_macro_targets(
        age=28,
        gender="male",
        height_cm=178.0,
        weight_kg=75.0,
        activity_level="moderate",
        goal="maintain"
    )
    assert targets["daily_calorie_target"] > 2000
    assert targets["protein_target"] >= 150
    assert targets["carb_target"] > 0
    assert targets["fat_target"] > 0
    assert targets["daily_water_target_ml"] >= 2000
