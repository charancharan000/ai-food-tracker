"""
Recipe-Aware Nutrition Pipeline & Anti-Hallucination Gate
Implements Section 40, Section 41, and Section 42 of Part 2.
Enforces the mandatory rule: calories = weight * nutrition_per_gram (recipe-aware).
Enforces the no-hallucination ambiguity preserver.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class RecipeNutritionalProfile(BaseModel):
    recipe_id: str
    dish_name: str
    variant: str
    cooking_method: str
    oil_ghee_level: str = Field(default="standard", description="low, standard, high_restaurant")
    base_calories_per_100g: float
    protein_per_100g: float
    carbs_per_100g: float
    fat_per_100g: float
    fiber_per_100g: float
    sodium_per_100g: float
    key_ingredients_weights: Dict[str, float] = Field(default_factory=dict)

# Recipe-Aware Profiles with Cooking Method & Oil Variance
RECIPE_AWARE_DATABASE: Dict[str, RecipeNutritionalProfile] = {
    "plain_idli_home": RecipeNutritionalProfile(
        recipe_id="plain_idli_home",
        dish_name="Idli",
        variant="Plain Idli (Home Recipe)",
        cooking_method="steam_cooked",
        oil_ghee_level="low",
        base_calories_per_100g=136.0,
        protein_per_100g=4.2,
        carbs_per_100g=28.5,
        fat_per_100g=0.6,
        fiber_per_100g=1.4,
        sodium_per_100g=180.0
    ),
    "ghee_podi_idli_restaurant": RecipeNutritionalProfile(
        recipe_id="ghee_podi_idli_restaurant",
        dish_name="Podi Idli",
        variant="Ghee Milagai Podi Idli (Restaurant Style)",
        cooking_method="steamed_then_ghee_tossed",
        oil_ghee_level="high_restaurant",
        base_calories_per_100g=210.0,
        protein_per_100g=5.4,
        carbs_per_100g=26.5,
        fat_per_100g=9.5,
        fiber_per_100g=2.8,
        sodium_per_100g=380.0
    ),
    "tiffin_sambar_restaurant": RecipeNutritionalProfile(
        recipe_id="tiffin_sambar_restaurant",
        dish_name="Sambar",
        variant="Hotel Tiffin Sambar",
        cooking_method="boiled_simmered",
        oil_ghee_level="standard",
        base_calories_per_100g=68.0,
        protein_per_100g=3.2,
        carbs_per_100g=10.5,
        fat_per_100g=1.6,
        fiber_per_100g=2.4,
        sodium_per_100g=320.0
    ),
    "white_coconut_chutney_standard": RecipeNutritionalProfile(
        recipe_id="white_coconut_chutney_standard",
        dish_name="Coconut Chutney",
        variant="Fresh White Coconut Chutney",
        cooking_method="raw_ground_tempered",
        oil_ghee_level="standard",
        base_calories_per_100g=210.0,
        protein_per_100g=3.0,
        carbs_per_100g=7.5,
        fat_per_100g=19.2,
        fiber_per_100g=3.5,
        sodium_per_100g=260.0
    ),
    "tomato_kaara_chutney_standard": RecipeNutritionalProfile(
        recipe_id="tomato_kaara_chutney_standard",
        dish_name="Tomato Chutney",
        variant="Spicy Tomato Kaara Chutney",
        cooking_method="sautéed_and_ground",
        oil_ghee_level="standard",
        base_calories_per_100g=88.0,
        protein_per_100g=1.8,
        carbs_per_100g=9.8,
        fat_per_100g=4.2,
        fiber_per_100g=1.9,
        sodium_per_100g=340.0
    ),
    "chicken_biryani_dindigul": RecipeNutritionalProfile(
        recipe_id="chicken_biryani_dindigul",
        dish_name="Chicken Biryani",
        variant="Dindigul Seeraga Samba Chicken Dum Biryani",
        cooking_method="dum_pot_cooked",
        oil_ghee_level="high_restaurant",
        base_calories_per_100g=175.0,
        protein_per_100g=11.2,
        carbs_per_100g=21.5,
        fat_per_100g=5.8,
        fiber_per_100g=1.1,
        sodium_per_100g=320.0
    ),
    "mutton_biryani_dindigul": RecipeNutritionalProfile(
        recipe_id="mutton_biryani_dindigul",
        dish_name="Mutton Biryani",
        variant="Dindigul Thalappakatti Mutton Biryani (Seeraga Samba)",
        cooking_method="dum_pot_cooked",
        oil_ghee_level="high_restaurant",
        base_calories_per_100g=205.0,
        protein_per_100g=11.5,
        carbs_per_100g=20.5,
        fat_per_100g=8.2,
        fiber_per_100g=1.1,
        sodium_per_100g=330.0
    )
}

# =============================================================================
# SECTION 40 — NO-HALLUCINATION AMBIGUITY GATE
# =============================================================================

class AntiHallucinationGate:
    @staticmethod
    def evaluate_steamed_white_food(
        feature_scores: Dict[str, float]
    ) -> Dict[str, Any]:
        """
        SECTION 40 RULE: If the model sees white round steamed food,
        it must NOT automatically say 'idli'.
        It must evaluate idli, rava idli, dhokla, paniyaram, other steamed food.
        """
        idli_score = feature_scores.get("idli_porosity", 0.0)
        rava_score = feature_scores.get("granular_crumb", 0.0)
        dhokla_score = feature_scores.get("yellow_sugar_sponge", 0.0)
        paniyaram_score = feature_scores.get("crisp_crust_sphere", 0.0)

        # Clear winner with confidence > 0.85
        if idli_score >= 0.85 and rava_score < 0.40 and dhokla_score < 0.20:
            return {"status": "resolved", "class_name": "Idli", "variant": "Plain Idli", "confidence": idli_score}
        elif rava_score >= 0.80:
            return {"status": "resolved", "class_name": "Rava Idli", "variant": "Semolina Rava Idli", "confidence": rava_score}
        elif dhokla_score >= 0.80:
            return {"status": "resolved", "class_name": "Dhokla", "variant": "Khaman Dhokla", "confidence": dhokla_score}
        elif paniyaram_score >= 0.80:
            return {"status": "resolved", "class_name": "Paniyaram", "variant": "Plain Kuzhi Paniyaram", "confidence": paniyaram_score}
        else:
            # Honest ambiguity preservation
            return {
                "status": "ambiguous",
                "class_name": "Steamed food detected",
                "variant": "Steamed food detected — exact type uncertain",
                "possible_candidates": ["Plain Idli", "Rava Idli", "Dhokla", "Kuzhi Paniyaram"],
                "confidence": 0.65,
                "notes": "Visual evidence insufficient to definitively confirm Idli over Dhokla or Paniyaram."
            }

    @staticmethod
    def evaluate_red_liquid(
        feature_scores: Dict[str, float]
    ) -> Dict[str, Any]:
        """
        SECTION 40 RULE: If red liquid is detected, do not automatically say sambar.
        Evaluate sambar, rasam, tomato gravy, dal, other curry.
        """
        sambar_score = feature_scores.get("sambar_veg_dal", 0.0)
        rasam_score = feature_scores.get("rasam_thin_pepper", 0.0)
        gravy_score = feature_scores.get("curry_gravy", 0.0)

        if sambar_score >= 0.85 and rasam_score < 0.40:
            return {"status": "resolved", "class_name": "Sambar", "variant": "Tiffin Sambar", "confidence": sambar_score}
        elif rasam_score >= 0.85:
            return {"status": "resolved", "class_name": "Rasam", "variant": "Tomato Pepper Rasam", "confidence": rasam_score}
        else:
            return {
                "status": "ambiguous",
                "class_name": "South Indian gravy detected",
                "variant": "South Indian gravy detected — exact type uncertain",
                "possible_candidates": ["Sambar", "Rasam", "Tomato Gravy / Salna", "Dal"],
                "confidence": 0.62,
                "notes": "Liquid broth detected; exact lentil/tamarind composition requires user confirmation."
            }

    @staticmethod
    def evaluate_chutney(
        feature_scores: Dict[str, float]
    ) -> Dict[str, Any]:
        """
        SECTION 19 & 40 RULE: If exact chutney cannot be visually determined,
        return 'Chutney detected — exact type uncertain.' Never invent an ingredient.
        """
        coconut_score = feature_scores.get("coconut_fiber", 0.0)
        peanut_score = feature_scores.get("peanut_smooth", 0.0)
        tomato_score = feature_scores.get("tomato_red", 0.0)

        if tomato_score >= 0.85:
            return {"status": "resolved", "class_name": "Tomato Chutney", "variant": "Spicy Kaara Chutney", "confidence": tomato_score}
        elif coconut_score >= 0.88 and peanut_score < 0.35:
            return {"status": "resolved", "class_name": "Coconut Chutney", "variant": "Fresh White Coconut Chutney", "confidence": coconut_score}
        else:
            return {
                "status": "ambiguous",
                "class_name": "Chutney",
                "variant": "Chutney detected — exact type uncertain",
                "possible_candidates": ["White Coconut Chutney", "Peanut Groundnut Chutney", "Sesame Chutney"],
                "confidence": 0.70,
                "notes": "Chutney detected — exact type uncertain. Visual inspection cannot distinguish pure coconut from peanut or sesame without taste."
            }

# =============================================================================
# SECTION 41 & 42 — CALORIE CALCULATION & STANDARDIZED OUTPUT MODEL
# =============================================================================

class FoodItemOutput(BaseModel):
    name: str
    variant: str
    count: Optional[int] = None
    estimated_weight: str
    estimated_weight_g: float
    calories: float
    confidence: float

class TotalNutritionSummary(BaseModel):
    calories: float
    protein: float
    carbs: float
    fat: float

class StandardizedModelOutput(BaseModel):
    items: List[FoodItemOutput]
    total: TotalNutritionSummary

class RecipeAwareCalorieCalculator:
    @staticmethod
    def calculate_calories(
        dish_name: str,
        variant: str,
        estimated_weight_g: float,
        recipe_key: Optional[str] = None
    ) -> Dict[str, float]:
        """
        Computes calories = weight * nutrition_per_gram based on recipe database.
        """
        profile = None
        if recipe_key and recipe_key in RECIPE_AWARE_DATABASE:
            profile = RECIPE_AWARE_DATABASE[recipe_key]
        else:
            # Fallback match by dish name
            for prof in RECIPE_AWARE_DATABASE.values():
                if prof.dish_name.lower() in dish_name.lower() or prof.variant.lower() in variant.lower():
                    profile = prof
                    break

        if not profile:
            # Conservative standard reference (160 kcal / 100g)
            cals_100 = 160.0
            prot_100 = 4.0
            carb_100 = 25.0
            fat_100 = 5.0
        else:
            cals_100 = profile.base_calories_per_100g
            prot_100 = profile.protein_per_100g
            carb_100 = profile.carbs_per_100g
            fat_100 = profile.fat_per_100g

        scale = estimated_weight_g / 100.0
        return {
            "calories": round(cals_100 * scale, 1),
            "protein": round(prot_100 * scale, 1),
            "carbs": round(carb_100 * scale, 1),
            "fat": round(fat_100 * scale, 1)
        }

    @staticmethod
    def generate_section42_output(
        item_detections: List[Dict[str, Any]]
    ) -> StandardizedModelOutput:
        """
        Generates the exact output format prescribed in Section 42:
        Food 1: Name: Idli, Variant: Plain Idli, Count: 3, Estimated Weight: 180g, Calories: ..., Confidence: ...
        Food 2: Name: Sambar, Estimated Weight: 110g, Calories: ..., Confidence: ...
        ...
        Total: Calories: ..., Protein: ..., Carbs: ..., Fat: ...
        """
        output_items: List[FoodItemOutput] = []
        tot_cals = 0.0
        tot_prot = 0.0
        tot_carbs = 0.0
        tot_fat = 0.0

        for it in item_detections:
            w_g = it.get("estimated_weight_g", 100.0)
            nutr = RecipeAwareCalorieCalculator.calculate_calories(
                dish_name=it.get("name", "South Indian Dish"),
                variant=it.get("variant", "Standard"),
                estimated_weight_g=w_g,
                recipe_key=it.get("recipe_key")
            )
            cals = nutr["calories"]
            tot_cals += cals
            tot_prot += nutr["protein"]
            tot_carbs += nutr["carbs"]
            tot_fat += nutr["fat"]

            output_items.append(FoodItemOutput(
                name=it.get("name", "Food Item"),
                variant=it.get("variant", "Standard"),
                count=it.get("count"),
                estimated_weight=f"{round(w_g, 1)}g",
                estimated_weight_g=round(w_g, 1),
                calories=cals,
                confidence=it.get("confidence", 0.95)
            ))

        return StandardizedModelOutput(
            items=output_items,
            total=TotalNutritionSummary(
                calories=round(tot_cals, 1),
                protein=round(tot_prot, 1),
                carbs=round(tot_carbs, 1),
                fat=round(tot_fat, 1)
            )
        )
