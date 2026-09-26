"""
Northeast Indian Recipe-Aware Nutrition & Calorie Estimation Engine (Part 7)
Implements Sections 52, 53, 63, 64, 65, 66, 86, 87 of Part 7 Master Training Specification.

Guarantees:
- Recipe-level variation modeling (pork fat, oil-free boiling, steaming, smoking, black sesame)
- Strict compliance with Section 87 No-Hallucination Rule
- Uncertainty-aware calorie ranges (min, expected, max)
- Standardized Section 86 Model Output schema compliance:
  food_name, canonical_food_id, state, region_community, food_category,
  vegetarian, ingredients, cooking_method, count, portion, estimated_weight_g,
  calories_kcal {min, expected, max}, protein_g, carbs_g, fat_g, fiber_g,
  confidence, uncertainty, user_confirmation_required.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

from app.food_ai.taxonomy.northeast_indian_master_taxonomy import (
    NORTHEAST_TAXONOMY_REGISTRY,
    get_northeast_food_class,
    resolve_northeast_food_by_name
)
from app.food_ai.portion_engine.northeast_indian_portions import (
    NortheastCountableDetector,
    NortheastFatLevelEstimator
)

# =============================================================================
# 1. SECTION 74, 78, 82, AND 86 MODEL OUTPUT SCHEMAS
# =============================================================================

class Section74SingleFoodJSON(BaseModel):
    """
    Implements Section 74: Single Food Output JSON Schema.
    """
    food_name: str
    region: str = "Northeast India"
    state: str
    count: int = 1
    estimated_weight_g: float
    cooking_method: str
    confidence: float
    nutrition: Dict[str, Optional[float]] = Field(default_factory=lambda: {
        "calories_kcal": None,
        "protein_g": None,
        "carbohydrates_g": None,
        "fat_g": None
    })

class Section78UnknownFoodOutput(BaseModel):
    """
    Implements Section 78: Unknown Food System Output.
    """
    food_name: str = "Unknown Northeast Indian Food"
    specific_dish: str = "Unknown"
    confidence: float = 0.24
    action: str = "Ask user for confirmation"

class Section82ItemOutput(BaseModel):
    food_name: str
    weight_g: float
    confidence: float

class Section82ModelOutput(BaseModel):
    """
    Implements Section 82: Final Multi-Food Model Output Example Schema.
    """
    meal_region: str = "Northeast India"
    confidence: float
    items: List[Section82ItemOutput]
    nutrition_status: str = "Estimate using verified database and recipe variation"

class NortheastCalorieRange(BaseModel):
    min: float
    expected: float
    max: float

class Section86ModelOutput(BaseModel):
    food_name: str
    canonical_food_id: str
    region: str = "Northeast India"
    state: str
    region_community: str
    food_category: str
    vegetarian: bool
    ingredients: List[str] = Field(default_factory=list)
    cooking_method: str
    food_state: str
    count: int = 1
    portion: str
    estimated_weight_g: float
    calories_kcal: NortheastCalorieRange
    protein_g: float
    carbs_g: float
    fat_g: float
    fiber_g: float
    confidence: float
    uncertainty: str
    user_confirmation_required: bool = False


# =============================================================================
# 2. RECIPE VARIATION DATABASE (Section 65, 66)
# =============================================================================

NORTHEAST_RECIPES_DATABASE: Dict[str, Dict[str, Any]] = {
    "ML_RICE_JADOH_PORK": {
        "recipe_name": "Khasi Jadoh with Pork",
        "base_cals_per_100g": 195.0,
        "protein_per_100g": 8.5,
        "carbs_per_100g": 25.0,
        "fat_per_100g": 7.2,
        "fiber_per_100g": 1.2,
        "variation_pct": 0.15,
        "cooking_method": "dum_braised",
        "food_state": "cooked_grain_and_meat"
    },
    "ML_MEAT_DOHNEIIHONG": {
        "recipe_name": "Khasi Pork with Black Sesame (Dohneiihong)",
        "base_cals_per_100g": 275.0,
        "protein_per_100g": 15.2,
        "carbs_per_100g": 4.5,
        "fat_per_100g": 22.0,
        "fiber_per_100g": 2.8,
        "variation_pct": 0.16,
        "cooking_method": "slow_braised",
        "food_state": "cooked_in_sesame_gravy"
    },
    "AS_FISH_MASOR_TENGA": {
        "recipe_name": "Assamese Masor Tenga",
        "base_cals_per_100g": 98.0,
        "protein_per_100g": 10.5,
        "carbs_per_100g": 3.2,
        "fat_per_100g": 4.8,
        "fiber_per_100g": 0.8,
        "variation_pct": 0.12,
        "cooking_method": "simmered_sour_broth",
        "food_state": "cooked_in_broth"
    },
    "AS_KHAR_OMITA": {
        "recipe_name": "Assamese Raw Papaya Khar",
        "base_cals_per_100g": 55.0,
        "protein_per_100g": 1.2,
        "carbs_per_100g": 7.5,
        "fat_per_100g": 2.2,
        "fiber_per_100g": 2.8,
        "variation_pct": 0.10,
        "cooking_method": "alkaline_stewed",
        "food_state": "cooked_stew"
    },
    "NL_MEAT_SMOKED_PORK_AXONE": {
        "recipe_name": "Naga Smoked Pork with Axone",
        "base_cals_per_100g": 290.0,
        "protein_per_100g": 17.5,
        "carbs_per_100g": 3.8,
        "fat_per_100g": 23.0,
        "fiber_per_100g": 1.8,
        "variation_pct": 0.18,
        "cooking_method": "wood_smoked_simmered",
        "food_state": "cooked_meat"
    },
    "NL_RICE_GALHO": {
        "recipe_name": "Naga Galho with Greens",
        "base_cals_per_100g": 125.0,
        "protein_per_100g": 5.8,
        "carbs_per_100g": 18.0,
        "fat_per_100g": 3.5,
        "fiber_per_100g": 1.8,
        "variation_pct": 0.14,
        "cooking_method": "boiled_soup",
        "food_state": "cooked_porridge"
    },
    "MZ_STEW_BAI": {
        "recipe_name": "Mizo Boiled Vegetable Bai",
        "base_cals_per_100g": 52.0,
        "protein_per_100g": 2.4,
        "carbs_per_100g": 6.8,
        "fat_per_100g": 1.5,
        "fiber_per_100g": 2.6,
        "variation_pct": 0.10,
        "cooking_method": "boiled",
        "food_state": "boiled_stew"
    },
    "MZ_RICE_SAWHCHIAR": {
        "recipe_name": "Mizo Sawhchiar",
        "base_cals_per_100g": 140.0,
        "protein_per_100g": 7.2,
        "carbs_per_100g": 19.5,
        "fat_per_100g": 3.8,
        "fiber_per_100g": 0.8,
        "variation_pct": 0.12,
        "cooking_method": "boiled_porridge",
        "food_state": "cooked_porridge"
    },
    "MN_CHUTNEY_EROMBA": {
        "recipe_name": "Manipuri Potato & Bamboo Shoot Eromba",
        "base_cals_per_100g": 75.0,
        "protein_per_100g": 3.8,
        "carbs_per_100g": 11.5,
        "fat_per_100g": 1.2,
        "fiber_per_100g": 2.4,
        "variation_pct": 0.12,
        "cooking_method": "boiled_mashed",
        "food_state": "mashed"
    },
    "MN_SALAD_SINGJU": {
        "recipe_name": "Manipuri Singju Salad",
        "base_cals_per_100g": 85.0,
        "protein_per_100g": 4.5,
        "carbs_per_100g": 11.8,
        "fat_per_100g": 2.2,
        "fiber_per_100g": 3.8,
        "variation_pct": 0.10,
        "cooking_method": "raw_tossed",
        "food_state": "raw_salad"
    },
    "TR_STEW_CHAKHWI": {
        "recipe_name": "Tripuri Bamboo Shoot Chakhwi",
        "base_cals_per_100g": 65.0,
        "protein_per_100g": 2.2,
        "carbs_per_100g": 9.8,
        "fat_per_100g": 1.8,
        "fiber_per_100g": 3.2,
        "variation_pct": 0.12,
        "cooking_method": "alkaline_stewed",
        "food_state": "cooked_stew"
    },
    "SK_MEAT_PHAGSHAPA": {
        "recipe_name": "Sikkimese Phagshapa (Pork with Radish)",
        "base_cals_per_100g": 260.0,
        "protein_per_100g": 13.8,
        "carbs_per_100g": 3.8,
        "fat_per_100g": 21.5,
        "fiber_per_100g": 1.2,
        "variation_pct": 0.16,
        "cooking_method": "stewed",
        "food_state": "cooked_meat_stew"
    },
    "SK_STEW_GUNDRUK": {
        "recipe_name": "Sikkimese Gundruk Jhol",
        "base_cals_per_100g": 58.0,
        "protein_per_100g": 3.2,
        "carbs_per_100g": 7.5,
        "fat_per_100g": 1.8,
        "fiber_per_100g": 3.8,
        "variation_pct": 0.10,
        "cooking_method": "boiled",
        "food_state": "cooked_soup"
    },
    "NE_MOMO_PORK_STEAMED": {
        "recipe_name": "Steamed Pork Momo",
        "base_cals_per_100g": 215.0,
        "protein_per_100g": 11.2,
        "carbs_per_100g": 24.5,
        "fat_per_100g": 8.2,
        "fiber_per_100g": 1.0,
        "variation_pct": 0.12,
        "cooking_method": "steamed",
        "food_state": "steamed_dumpling"
    },
    "NE_THUKPA_CHICKEN": {
        "recipe_name": "Chicken Thukpa",
        "base_cals_per_100g": 95.0,
        "protein_per_100g": 6.8,
        "carbs_per_100g": 12.5,
        "fat_per_100g": 2.2,
        "fiber_per_100g": 1.2,
        "variation_pct": 0.12,
        "cooking_method": "boiled_soup",
        "food_state": "noodle_soup"
    }
}

# =============================================================================
# 3. RECIPE-AWARE CALCULATION PIPELINE (Sections 52, 53, 64, 86, 87)
# =============================================================================

class NortheastRecipeNutritionCalculator:
    """
    Implements Section 86 output and Section 87 no-hallucination rules.
    Calculates calorie ranges, portions, counts, and macros.
    """
    @staticmethod
    def calculate_dish_nutrition(
        food_identifier: str,
        visual_cues: Optional[Dict[str, Any]] = None,
        custom_weight_g: Optional[float] = None,
        count: Optional[int] = None,
        occlusion_factor: float = 0.0
    ) -> Section86ModelOutput:
        visual_cues = visual_cues or {}
        food_cls = resolve_northeast_food_by_name(food_identifier)
        if not food_cls:
            food_cls = get_northeast_food_class(food_identifier)

        if not food_cls:
            return Section86ModelOutput(
                food_name="Unknown Northeast Food / Needs Confirmation",
                canonical_food_id="NORTHEAST_INDIAN_UNKNOWN",
                region="Northeast India",
                state="Unknown",
                region_community="Uncertain",
                food_category="Unknown",
                vegetarian=True,
                ingredients=[],
                cooking_method="unknown",
                food_state="unknown",
                count=1,
                portion="unknown",
                estimated_weight_g=0.0,
                calories_kcal=NortheastCalorieRange(min=0.0, expected=0.0, max=0.0),
                protein_g=0.0,
                carbs_g=0.0,
                fat_g=0.0,
                fiber_g=0.0,
                confidence=0.25,
                uncertainty="Unable to identify this food confidently from visual evidence alone (enforcing Section 87 No-Hallucination Rule).",
                user_confirmation_required=True
            )

        cid = food_cls.canonical_food_id

        # Determine count and weight
        countable_res = NortheastCountableDetector.estimate_count_and_weight(
            food_id=cid,
            visible_count=count if count is not None else 1,
            occlusion_factor=occlusion_factor
        )

        if custom_weight_g is not None and custom_weight_g > 0:
            final_weight_g = custom_weight_g
            portion_str = f"Custom portion ({round(final_weight_g, 1)}g)"
            item_count = count or 1
        elif countable_res.is_countable:
            final_weight_g = countable_res.total_estimated_weight_g
            item_count = countable_res.estimated_total_count
            portion_str = f"{item_count} {countable_res.unit_name}(s) ({round(final_weight_g, 1)}g)"
        else:
            final_weight_g = food_cls.default_serving_weight_g
            item_count = 1
            portion_str = food_cls.hierarchy.default_portion

        # Retrieve Recipe Baseline or Taxonomy Baseline
        rec = NORTHEAST_RECIPES_DATABASE.get(cid)
        if rec:
            base_cals_100g = rec["base_cals_per_100g"]
            p_100g = rec["protein_per_100g"]
            cb_100g = rec["carbs_per_100g"]
            f_100g = rec["fat_per_100g"]
            fib_100g = rec["fiber_per_100g"]
            var_pct = rec["variation_pct"]
            cooking_meth = rec["cooking_method"]
            f_state = rec["food_state"]
        else:
            nutr = food_cls.nutrition_per_100g
            base_cals_100g = nutr.get("calories", 130.0)
            p_100g = nutr.get("protein_g", 5.0)
            cb_100g = nutr.get("carbs_g", 18.0)
            f_100g = nutr.get("fat_g", 4.0)
            fib_100g = nutr.get("fiber_g", 1.5)
            var_pct = 0.15
            cooking_meth = food_cls.hierarchy.level8_cooking_method[0] if food_cls.hierarchy.level8_cooking_method else "cooked"
            f_state = "cooked"

        # Apply Visual Fat Estimation Multiplier (Section 66)
        fat_est = NortheastFatLevelEstimator.estimate_fat(visual_cues)
        f_mult = fat_est["fat_multiplier"]

        factor = final_weight_g / 100.0
        exp_cals = round(base_cals_100g * factor * f_mult, 1)
        min_cals = round(exp_cals * (1.0 - var_pct), 1)
        max_cals = round(exp_cals * (1.0 + var_pct), 1)

        exp_p = round(p_100g * factor, 1)
        exp_cb = round(cb_100g * factor, 1)
        exp_f = round(f_100g * factor * f_mult, 1)
        exp_fib = round(fib_100g * factor, 1)

        conf = 0.94 if cid in NORTHEAST_RECIPES_DATABASE else 0.88
        unc_notes = f"Estimated range [±{int(var_pct * 100)}%] calibrated for regional cooking ({cooking_meth}) and fat level ({fat_est['fat_level']})."

        return Section86ModelOutput(
            food_name=food_cls.canonical_name,
            canonical_food_id=cid,
            region="Northeast India",
            state=food_cls.state,
            region_community=food_cls.region_community,
            food_category=food_cls.food_category,
            vegetarian=food_cls.vegetarian,
            ingredients=list(food_cls.key_ingredients),
            cooking_method=cooking_meth,
            food_state=f_state,
            count=item_count,
            portion=portion_str,
            estimated_weight_g=round(final_weight_g, 1),
            calories_kcal=NortheastCalorieRange(min=min_cals, expected=exp_cals, max=max_cals),
            protein_g=exp_p,
            carbs_g=exp_cb,
            fat_g=exp_f,
            fiber_g=exp_fib,
            confidence=conf,
            uncertainty=unc_notes,
            user_confirmation_required=False
        )

    @classmethod
    def generate_section_74_single_food(
        cls,
        food_identifier: str,
        count: int = 8,
        cooking_method: str = "steamed"
    ) -> Section74SingleFoodJSON:
        """
        Implements Section 74: Single Food Output JSON Schema.
        Example: Chicken Momo, 8 pieces, 320g, confidence 0.94, nutrition from verified db.
        """
        food_cls = resolve_northeast_food_by_name(food_identifier)
        if not food_cls:
            food_cls = get_northeast_food_class(food_identifier)

        food_name = food_cls.canonical_name if food_cls else food_identifier
        state = food_cls.state if food_cls else "Northeast India"
        unit_wt = 40.0
        if food_cls:
            if "momo" in food_cls.canonical_name.lower():
                unit_wt = 40.0
            else:
                unit_wt = food_cls.default_serving_weight_g / max(1, count)
        est_wt = round(count * unit_wt, 1)

        return Section74SingleFoodJSON(
            food_name=food_name,
            region="Northeast India",
            state=state,
            count=count,
            estimated_weight_g=est_wt,
            cooking_method=cooking_method,
            confidence=0.94 if food_cls else 0.80,
            nutrition={
                "calories_kcal": None,
                "protein_g": None,
                "carbohydrates_g": None,
                "fat_g": None
            }
        )

    @classmethod
    def generate_section_78_unknown_fallback(
        cls,
        confidence: float = 0.24
    ) -> Section78UnknownFoodOutput:
        """
        Implements Section 78: Unknown Food System Fallback Schema.
        """
        return Section78UnknownFoodOutput(
            food_name="Unknown Northeast Indian Food",
            specific_dish="Unknown",
            confidence=confidence,
            action="Ask user for confirmation"
        )

    @classmethod
    def generate_section_82_multi_food(
        cls,
        meal_region: str = "Northeast India",
        items_spec: Optional[List[Dict[str, Any]]] = None
    ) -> Section82ModelOutput:
        """
        Implements Section 82: Final Model Output Example Schema for multi-food plate.
        Example: Rice (220g, 0.99), Pork Preparation (150g, 0.86), Bamboo Shoot (65g, 0.79), Chutney (20g, 0.73).
        """
        if items_spec is None:
            items_spec = [
                {"food_name": "Rice", "weight_g": 220.0, "confidence": 0.99},
                {"food_name": "Pork Preparation", "weight_g": 150.0, "confidence": 0.86},
                {"food_name": "Bamboo Shoot Preparation", "weight_g": 65.0, "confidence": 0.79},
                {"food_name": "Chutney", "weight_g": 20.0, "confidence": 0.73}
            ]

        item_objs = [
            Section82ItemOutput(
                food_name=it["food_name"],
                weight_g=float(it["weight_g"]),
                confidence=float(it["confidence"])
            ) for it in items_spec
        ]

        avg_conf = round(sum(it.confidence for it in item_objs) / len(item_objs), 2) if item_objs else 0.85

        return Section82ModelOutput(
            meal_region=meal_region,
            confidence=avg_conf,
            items=item_objs,
            nutrition_status="Estimate using verified database and recipe variation"
        )

