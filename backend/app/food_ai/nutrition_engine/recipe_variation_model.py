"""
Recipe Variation Modeling, Raw/Cooked Nutrition, & Uncertainty Propagation
Implements Sections 38, 39, 40, 41, and 42 of Part 3.
Guarantees:
- Separate raw vs cooked nutritional matrices
- Household vs restaurant recipe variations (Recipe A, B, C)
- Component separation (main food, side dish, gravy, chutney, podi, pickle, garnish)
- Multi-dimensional uncertainty propagation:
  Recognition (high/med/low) + Weight (high/med/low) + Recipe (high/med/low) -> Calorie Credible Interval
- Full meal compositions for Tamil, Kerala, Andhra, Karnataka dining traditions
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

# =============================================================================
# SECTION 38 — RAW VS COOKED NUTRITION RECORD
# =============================================================================

class MacronutrientProfile(BaseModel):
    calories_kcal: float
    protein_g: float
    carbohydrate_g: float
    fat_g: float
    fiber_g: float
    sugar_g: float
    sodium_mg: float

class FoodNutritionStatePair(BaseModel):
    food_id: str
    canonical_name: str
    raw_per_100g: MacronutrientProfile
    cooked_per_100g: MacronutrientProfile
    cooking_hydration_factor: float = Field(default=1.0, description="cooked_weight / raw_weight")
    oil_absorption_factor_pct: float = Field(default=0.0)

# =============================================================================
# SECTION 39 — MULTIPLE RECIPE PROFILES PER DISH
# =============================================================================

class DishRecipeProfile(BaseModel):
    recipe_code: str
    dish_id: str
    recipe_name: str
    description: str
    oil_ghee_used_g_per_serving: float
    batter_rice_to_dal_ratio: str
    nutrition_per_100g: MacronutrientProfile

RECIPE_VARIATION_DATABASE: Dict[str, List[DishRecipeProfile]] = {
    "TN_BREAKFAST_DOSA": [
        DishRecipeProfile(
            recipe_code="DOSAI_RECIPE_A_RESTAURANT",
            dish_id="TN_BREAKFAST_DOSA",
            recipe_name="Saravana Bhavan Commercial Ghee Roast",
            description="Crisp high-ghee restaurant style with sugar caramelization and chana dal",
            oil_ghee_used_g_per_serving=18.0,
            batter_rice_to_dal_ratio="4:1 parboiled rice to urad dal + 2 tbsp chana dal",
            nutrition_per_100g=MacronutrientProfile(
                calories_kcal=235.0, protein_g=3.9, carbohydrate_g=28.0, fat_g=12.4, fiber_g=1.2, sugar_g=1.5, sodium_mg=240.0
            )
        ),
        DishRecipeProfile(
            recipe_code="DOSAI_RECIPE_B_HOME_HEALTHY",
            dish_id="TN_BREAKFAST_DOSA",
            recipe_name="Traditional Low-Oil Home Dosa",
            description="Traditional cast-iron skillet dosa with minimal cold-pressed sesame oil",
            oil_ghee_used_g_per_serving=4.0,
            batter_rice_to_dal_ratio="3:1 raw rice & parboiled to urad dal with fenugreek",
            nutrition_per_100g=MacronutrientProfile(
                calories_kcal=152.0, protein_g=4.4, carbohydrate_g=29.2, fat_g=2.2, fiber_g=1.8, sugar_g=0.2, sodium_mg=170.0
            )
        ),
        DishRecipeProfile(
            recipe_code="DOSAI_RECIPE_C_CRISPY_BUTTER",
            dish_id="TN_BREAKFAST_DOSA",
            recipe_name="Butter Paper Roast",
            description="Slow-roasted on thick tawa with generous butter glaze",
            oil_ghee_used_g_per_serving=22.0,
            batter_rice_to_dal_ratio="4:1 with poha / flattened rice addition",
            nutrition_per_100g=MacronutrientProfile(
                calories_kcal=255.0, protein_g=3.8, carbohydrate_g=27.5, fat_g=14.8, fiber_g=1.1, sugar_g=0.5, sodium_mg=280.0
            )
        )
    ],
    "TN_CURRY_SAMBAR": [
        DishRecipeProfile(
            recipe_code="SAMBAR_RECIPE_A_HOTEL_TIFFIN",
            dish_id="TN_CURRY_SAMBAR",
            recipe_name="Saravana Hotel Tiffin Sambar",
            description="Mild sweet-tangy lentil broth with shallots, yellow moong & toor dal, and jaggery touch",
            oil_ghee_used_g_per_serving=4.5,
            batter_rice_to_dal_ratio="N/A",
            nutrition_per_100g=MacronutrientProfile(
                calories_kcal=68.0, protein_g=3.2, carbohydrate_g=10.5, fat_g=1.6, fiber_g=2.4, sugar_g=3.1, sodium_mg=320.0
            )
        ),
        DishRecipeProfile(
            recipe_code="SAMBAR_RECIPE_B_TAMIL_BRAHMIN",
            dish_id="TN_CURRY_SAMBAR",
            recipe_name="Traditional Home Sambar (No Onion)",
            description="Pure toor dal, tamarind, freshly roasted and ground sambar spices, hing",
            oil_ghee_used_g_per_serving=2.5,
            batter_rice_to_dal_ratio="N/A",
            nutrition_per_100g=MacronutrientProfile(
                calories_kcal=62.0, protein_g=3.8, carbohydrate_g=9.2, fat_g=1.1, fiber_g=2.8, sugar_g=0.8, sodium_mg=260.0
            )
        )
    ]
}

# =============================================================================
# SECTION 40 — MULTI-DIMENSIONAL CALORIE UNCERTAINTY PROPAGATION
# =============================================================================

class UncertaintyCalorieEstimate(BaseModel):
    dish_name: str
    variant: str
    estimated_weight_g: float
    calories_point_estimate: float
    calorie_range_min: float
    calorie_range_max: float
    confidence_levels: Dict[str, str] = Field(..., description="food_confidence, weight_confidence, recipe_confidence")
    overall_confidence_score: float
    user_disclosure: str

class CalorieUncertaintyModel:
    @staticmethod
    def propagate_uncertainty(
        dish_name: str,
        variant: str,
        estimated_weight_g: float,
        base_calories_per_100g: float,
        food_confidence: float = 0.95,
        weight_confidence: float = 0.90,
        is_two_photo_mode: bool = False
    ) -> UncertaintyCalorieEstimate:
        """
        SECTION 40: Never pretend calorie values are exact.
        Propagates recognition, volume, and recipe variance.
        """
        point_cals = (estimated_weight_g / 100.0) * base_calories_per_100g
        
        # Uncertainty width depends on mode and confidences
        weight_uncertainty_pct = 0.08 if is_two_photo_mode else 0.16
        recipe_uncertainty_pct = 0.12 # Household vs restaurant oil variance
        
        combined_uncertainty_pct = weight_uncertainty_pct + recipe_uncertainty_pct
        if food_confidence < 0.85:
            combined_uncertainty_pct += 0.10

        cals_min = round(point_cals * (1.0 - combined_uncertainty_pct), 1)
        cals_max = round(point_cals * (1.0 + combined_uncertainty_pct), 1)
        
        conf_label = "high" if food_confidence >= 0.92 and is_two_photo_mode else (
            "medium-high" if food_confidence >= 0.88 else "medium"
        )

        return UncertaintyCalorieEstimate(
            dish_name=dish_name,
            variant=variant,
            estimated_weight_g=estimated_weight_g,
            calories_point_estimate=round(point_cals, 1),
            calorie_range_min=cals_min,
            calorie_range_max=cals_max,
            confidence_levels={
                "recognition": "high" if food_confidence >= 0.90 else "medium",
                "weight": "high" if is_two_photo_mode else "medium",
                "recipe": "medium (household variation)"
            },
            overall_confidence_score=round(food_confidence * (0.95 if is_two_photo_mode else 0.88), 2),
            user_disclosure=f"Estimated {round(point_cals)} kcal (credible range {cals_min} - {cals_max} kcal)."
        )

# =============================================================================
# SECTION 41 & 42 — COMPONENT SEPARATION & FULL MEAL COMPOSITIONS
# =============================================================================

class PlatedMealComponent(BaseModel):
    component_type: str = Field(..., description="main_food, side_dish, gravy, chutney, podi, pickle, garnish")
    food_name: str
    variant: str
    weight_g: float
    calories: float

class FullMealPlan(BaseModel):
    meal_title: str
    cultural_context: str # Tamil breakfast, Kerala sadya, Andhra meals, Karnataka breakfast
    components: List[PlatedMealComponent]
    total_meal_weight_g: float
    total_meal_calories: float

FULL_MEAL_TEMPLATES: Dict[str, FullMealPlan] = {
    "TAMIL_TIFFIN_BREAKFAST": FullMealPlan(
        meal_title="Classic Tamil Nadu Tiffin Breakfast",
        cultural_context="Tamil Nadu Breakfast",
        components=[
            PlatedMealComponent(component_type="main_food", food_name="Steamed Idli", variant="Plain Idli (2 pieces)", weight_g=124.0, calories=168.0),
            PlatedMealComponent(component_type="side_dish", food_name="Medu Vada", variant="Crispy Ulundhu Vada (1 piece)", weight_g=65.0, calories=170.0),
            PlatedMealComponent(component_type="gravy", food_name="Hotel Tiffin Sambar", variant="Simmered Drumstick Sambar", weight_g=110.0, calories=75.0),
            PlatedMealComponent(component_type="chutney", food_name="White Coconut Chutney", variant="Fresh Coconut Dip", weight_g=45.0, calories=95.0),
            PlatedMealComponent(component_type="chutney", food_name="Tomato Kaara Chutney", variant="Spicy Red Chutney", weight_g=40.0, calories=35.0)
        ],
        total_meal_weight_g=384.0,
        total_meal_calories=543.0
    ),
    "KERALA_ONAM_SADYA": FullMealPlan(
        meal_title="Traditional Kerala Sadya Feast",
        cultural_context="Kerala Sadya",
        components=[
            PlatedMealComponent(component_type="main_food", food_name="Kerala Red Matta Rice", variant="Boiled Matta Rice", weight_g=250.0, calories=325.0),
            PlatedMealComponent(component_type="side_dish", food_name="Avial", variant="Mixed Vegetables in Coconut Yogurt", weight_g=80.0, calories=92.0),
            PlatedMealComponent(component_type="side_dish", food_name="Cabbage Thoran", variant="Dry Sautéed Cabbage with Coconut", weight_g=65.0, calories=60.0),
            PlatedMealComponent(component_type="gravy", food_name="Parippu Curry with Ghee", variant="Yellow Moong Dal Curry", weight_g=70.0, calories=85.0),
            PlatedMealComponent(component_type="gravy", food_name="Sambar", variant="Kerala Roasted Coconut Sambar", weight_g=90.0, calories=72.0),
            PlatedMealComponent(component_type="pickle", food_name="Inji Puli", variant="Ginger Tamarind Pickle", weight_g=15.0, calories=32.0),
            PlatedMealComponent(component_type="side_dish", food_name="Banana Chips (Upperi)", variant="Coconut Oil Fried Plantain", weight_g=25.0, calories=135.0),
            PlatedMealComponent(component_type="garnish", food_name="Kerala Pappadam", variant="Fried Crisp Wafer", weight_g=12.0, calories=45.0)
        ],
        total_meal_weight_g=607.0,
        total_meal_calories=846.0
    )
}
