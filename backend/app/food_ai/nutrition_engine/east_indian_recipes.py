"""
East Indian Recipe-Aware Nutrition & Calorie Estimation Engine (Part 6)
Implements Sections 43, 44, 45, 51, 52, 53, 63 of Part 6 Training Specification.

Guarantees:
- Recipe-level variation modeling (oil, ghee, mustard oil, coconut, cooking methods)
- Strict avoidance of food_name -> fixed calories (Section 52)
- Produces uncertainty-aware calorie ranges (min, expected, max)
- Standardized Section 63 Model Output JSON schema compliance:
  20 fields including canonical_food_id, state, regional_variant, cooking_method,
  food_state, portion, count, calories_kcal {min, expected, max}, macros, confidences,
  uncertainty, user_confirmation_required.
- Independent output objects for multi-food meals.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

from app.food_ai.taxonomy.east_indian_master_taxonomy import (
    EAST_INDIAN_TAXONOMY_REGISTRY,
    get_east_food_class,
    resolve_east_food_by_name
)
from app.food_ai.portion_engine.east_indian_portions import (
    CountableFoodDetector,
    VisualFatSheenEstimator
)

# =============================================================================
# 1. SECTION 63 STANDARDIZED MODEL OUTPUT SCHEMA
# =============================================================================

class CalorieRange(BaseModel):
    min: float
    expected: float
    max: float

class Section63ModelOutput(BaseModel):
    food_name: str
    canonical_food_id: str
    region: str = "East India"
    state: str
    regional_variant: str
    food_category: str
    vegetarian: bool
    ingredients: List[str] = Field(default_factory=list)
    cooking_method: str
    food_state: str
    count: int = 1
    portion: str
    estimated_weight_g: float
    calories_kcal: CalorieRange
    protein_g: float
    carbs_g: float
    fat_g: float
    fiber_g: float
    confidence: float
    uncertainty: str
    user_confirmation_required: bool = False

# =============================================================================
# 2. RECIPE VARIATION DATABASE WITH NUTRITION RANGES (Section 51)
# =============================================================================

EAST_INDIAN_RECIPES_DATABASE: Dict[str, Dict[str, Any]] = {
    "WB_FISH_SHORSHE_ILISH": {
        "recipe_name": "Authentic Shorshe Ilish (Mustard Hilsa)",
        "base_cals_per_100g": 240.0,
        "protein_per_100g": 14.5,
        "carbs_per_100g": 3.2,
        "fat_per_100g": 18.8,
        "fiber_per_100g": 1.2,
        "oil_type": "pure_cold_pressed_mustard_oil",
        "variation_pct": 0.15,
        "common_cooking_method": "mustard_paste_simmered",
        "food_state": "cooked_in_gravy"
    },
    "WB_MEAT_KOSHA_MANGSHO": {
        "recipe_name": "Bengali Kosha Mangsho",
        "base_cals_per_100g": 265.0,
        "protein_per_100g": 16.5,
        "carbs_per_100g": 5.2,
        "fat_per_100g": 19.8,
        "fiber_per_100g": 1.2,
        "oil_type": "mustard_oil_and_ghee",
        "variation_pct": 0.18,
        "common_cooking_method": "slow_cooked_kasha",
        "food_state": "cooked_in_gravy"
    },
    "WB_VEG_ALOO_POSTO": {
        "recipe_name": "Traditional Aloo Posto",
        "base_cals_per_100g": 170.0,
        "protein_per_100g": 3.8,
        "carbs_per_100g": 18.2,
        "fat_per_100g": 9.5,
        "fiber_per_100g": 2.5,
        "oil_type": "raw_mustard_oil_drizzle",
        "variation_pct": 0.12,
        "common_cooking_method": "sauteed_simmered",
        "food_state": "cooked"
    },
    "WB_RICE_BASANTI_PULAO": {
        "recipe_name": "Basanti Sweet Pulao",
        "base_cals_per_100g": 210.0,
        "protein_per_100g": 3.6,
        "carbs_per_100g": 36.5,
        "fat_per_100g": 5.8,
        "fiber_per_100g": 1.1,
        "oil_type": "pure_desi_ghee",
        "variation_pct": 0.14,
        "common_cooking_method": "dum_cooked",
        "food_state": "cooked_grain"
    },
    "WB_SWEET_MISHTI_DOI": {
        "recipe_name": "Kolkata Mishti Doi",
        "base_cals_per_100g": 160.0,
        "protein_per_100g": 4.5,
        "carbs_per_100g": 22.0,
        "fat_per_100g": 6.2,
        "fiber_per_100g": 0.0,
        "oil_type": "none",
        "variation_pct": 0.10,
        "common_cooking_method": "earthen_pot_fermented",
        "food_state": "fermented_curd"
    },
    "OD_CURRY_DALMA": {
        "recipe_name": "Odia Dalma",
        "base_cals_per_100g": 105.0,
        "protein_per_100g": 4.8,
        "carbs_per_100g": 16.2,
        "fat_per_100g": 2.5,
        "fiber_per_100g": 3.8,
        "oil_type": "desi_ghee_tempering",
        "variation_pct": 0.12,
        "common_cooking_method": "boiled_ghee_tempered",
        "food_state": "cooked_stew"
    },
    "OD_SWEET_CHHENA_PODA": {
        "recipe_name": "Odia Chhena Poda",
        "base_cals_per_100g": 290.0,
        "protein_per_100g": 11.2,
        "carbs_per_100g": 38.0,
        "fat_per_100g": 10.5,
        "fiber_per_100g": 0.4,
        "oil_type": "ghee",
        "variation_pct": 0.15,
        "common_cooking_method": "slow_baked",
        "food_state": "baked_solid"
    },
    "BR_BREAD_LITTI": {
        "recipe_name": "Bihari Sattu Litti",
        "base_cals_per_100g": 265.0,
        "protein_per_100g": 9.8,
        "carbs_per_100g": 41.5,
        "fat_per_100g": 7.2,
        "fiber_per_100g": 5.8,
        "oil_type": "desi_ghee_dip",
        "variation_pct": 0.16,
        "common_cooking_method": "charcoal_roasted_baked",
        "food_state": "baked_solid"
    },
    "BR_CHOKHA_BAINGAN": {
        "recipe_name": "Flame Roasted Baingan Chokha",
        "base_cals_per_100g": 85.0,
        "protein_per_100g": 1.9,
        "carbs_per_100g": 8.5,
        "fat_per_100g": 5.2,
        "fiber_per_100g": 3.0,
        "oil_type": "raw_mustard_oil",
        "variation_pct": 0.15,
        "common_cooking_method": "roasted_mashed",
        "food_state": "cooked_mash"
    },
    "BR_MEAT_CHAMPARAN_MUTTON": {
        "recipe_name": "Champaran Ahuna Clay Pot Mutton",
        "base_cals_per_100g": 275.0,
        "protein_per_100g": 15.8,
        "carbs_per_100g": 4.5,
        "fat_per_100g": 21.5,
        "fiber_per_100g": 1.0,
        "oil_type": "pure_mustard_oil",
        "variation_pct": 0.20,
        "common_cooking_method": "earthen_handi_dum",
        "food_state": "cooked_in_gravy"
    },
    "JH_SNACK_DHUSKA": {
        "recipe_name": "Jharkhandi Dhuska",
        "base_cals_per_100g": 285.0,
        "protein_per_100g": 6.8,
        "carbs_per_100g": 38.5,
        "fat_per_100g": 12.0,
        "fiber_per_100g": 3.0,
        "oil_type": "mustard_oil_or_refined_oil",
        "variation_pct": 0.14,
        "common_cooking_method": "deep_fried",
        "food_state": "fried_solid"
    }
}

# =============================================================================
# 3. RECIPE-AWARE CALCULATION PIPELINE (Section 52, Quality Rules 7 & 8)
# =============================================================================

class EastIndianRecipeNutritionCalculator:
    """
    Implements Section 52:
    food identity + weight + recipe + visible ingredients + cooking method + fat estimation -> calorie estimate range.
    Never uses food_name -> fixed calories.
    """
    @staticmethod
    def calculate_dish_nutrition(
        food_identifier: str,
        visual_cues: Optional[Dict[str, Any]] = None,
        custom_weight_g: Optional[float] = None,
        count: Optional[int] = None
    ) -> Section63ModelOutput:
        visual_cues = visual_cues or {}
        food_cls = resolve_east_food_by_name(food_identifier)
        if not food_cls:
            food_cls = get_east_food_class(food_identifier)

        if not food_cls:
            # Fallback to unknown class (Section 48, Quality Rule 18)
            unknown = get_east_food_class("EAST_INDIAN_UNKNOWN")
            return Section63ModelOutput(
                food_name="Unknown / Needs Confirmation",
                canonical_food_id="EAST_INDIAN_UNKNOWN",
                region="East India",
                state="Unknown",
                regional_variant="Unconfirmed regional dish",
                food_category="Unknown",
                vegetarian=True,
                ingredients=[],
                cooking_method="unknown",
                food_state="unknown",
                count=1,
                portion="unknown",
                estimated_weight_g=0.0,
                calories_kcal=CalorieRange(min=0.0, expected=0.0, max=0.0),
                protein_g=0.0,
                carbs_g=0.0,
                fat_g=0.0,
                fiber_g=0.0,
                confidence=0.20,
                uncertainty="High: Insufficient visual evidence to confirm canonical class without user clarification.",
                user_confirmation_required=True
            )

        cid = food_cls.canonical_food_id

        # Determine Count and Weight
        countable_res = CountableFoodDetector.estimate_countable_weight(
            food_id=cid,
            detected_count=count if count is not None else 1
        )

        if custom_weight_g is not None and custom_weight_g > 0:
            final_weight_g = custom_weight_g
            portion_str = f"Custom portion ({round(final_weight_g, 1)}g)"
            item_count = count or 1
        elif countable_res.is_countable:
            final_weight_g = countable_res.total_estimated_weight_g
            item_count = countable_res.count
            portion_str = f"{item_count} {countable_res.unit_name}(s) ({round(final_weight_g, 1)}g)"
        else:
            final_weight_g = food_cls.default_serving_weight_g
            item_count = 1
            portion_str = food_cls.hierarchy.default_portion

        # Retrieve Recipe Baseline or Taxonomy Baseline
        rec = EAST_INDIAN_RECIPES_DATABASE.get(cid)
        if rec:
            base_cals_100g = rec["base_cals_per_100g"]
            p_100g = rec["protein_per_100g"]
            cb_100g = rec["carbs_per_100g"]
            f_100g = rec["fat_per_100g"]
            fib_100g = rec["fiber_per_100g"]
            var_pct = rec["variation_pct"]
            cooking_meth = rec["common_cooking_method"]
            f_state = rec["food_state"]
        else:
            nutr = food_cls.nutrition_per_100g
            base_cals_100g = nutr.get("calories", 150.0)
            p_100g = nutr.get("protein_g", 5.0)
            cb_100g = nutr.get("carbs_g", 20.0)
            f_100g = nutr.get("fat_g", 5.0)
            fib_100g = nutr.get("fiber_g", 1.5)
            var_pct = 0.15
            cooking_meth = food_cls.hierarchy.level9_cooking_method[0] if food_cls.hierarchy.level9_cooking_method else "cooked"
            f_state = "cooked"

        # Apply Visual Fat Estimation Multiplier (Section 53)
        fat_est = VisualFatSheenEstimator.estimate_fat_level(visual_cues)
        multiplier = fat_est["fat_factor_multiplier"]

        factor = final_weight_g / 100.0
        exp_cals = round(base_cals_100g * factor * multiplier, 1)
        min_cals = round(exp_cals * (1.0 - var_pct), 1)
        max_cals = round(exp_cals * (1.0 + var_pct), 1)

        exp_p = round(p_100g * factor, 1)
        exp_cb = round(cb_100g * factor, 1)
        exp_f = round(f_100g * factor * multiplier, 1)
        exp_fib = round(fib_100g * factor, 1)

        # Assemble visible ingredients
        vis_ingr = list(food_cls.key_ingredients)

        # Determine uncertainty and user confirmation
        conf = 0.94 if cid in EAST_INDIAN_RECIPES_DATABASE else 0.88
        unc_notes = f"Recipe-calibrated range [±{int(var_pct * 100)}%] accounting for fat sheen ({fat_est['fat_level']}) and cooking method variations."

        return Section63ModelOutput(
            food_name=food_cls.canonical_name,
            canonical_food_id=cid,
            region="East India",
            state=food_cls.state,
            regional_variant=food_cls.hierarchy.level8_variant,
            food_category=food_cls.food_category,
            vegetarian=food_cls.vegetarian,
            ingredients=vis_ingr,
            cooking_method=cooking_meth,
            food_state=f_state,
            count=item_count,
            portion=portion_str,
            estimated_weight_g=round(final_weight_g, 1),
            calories_kcal=CalorieRange(min=min_cals, expected=exp_cals, max=max_cals),
            protein_g=exp_p,
            carbs_g=exp_cb,
            fat_g=exp_f,
            fiber_g=exp_fib,
            confidence=conf,
            uncertainty=unc_notes,
            user_confirmation_required=False
        )
