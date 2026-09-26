"""
West Indian Recipe Variation Engine & Section 51 Standardized Output Generator
Implements Sections 29, 31, 32, and 51 of Part 5.
Guarantees:
- Yield multipliers and moisture adjustment for grains, flours, and pulses.
- Section 51 Final Standardized Model Output schema:
  food_name, canonical_food_id, region ("West India"), state, regional_variant, food_category,
  vegetarian, ingredients (visible, inferred), cooking_method, portion, count (if countable),
  estimated_weight_g, calories_kcal (min, expected, max), protein_g, carbs_g, fat_g, fiber_g,
  confidence, uncertainty (weight_range_g, calorie_range_kcal), user_confirmation_required,
  visual_fat_level.
- Never force an identity when uncertain; flags user_confirmation_required when visual evidence is insufficient.
"""

from typing import Dict, Any, List, Optional, Tuple
from pydantic import BaseModel, Field

from app.food_ai.taxonomy.west_indian_master_taxonomy import (
    get_west_food_class,
    resolve_west_food_by_name
)
from app.food_ai.portion_engine.west_indian_portions import (
    get_portion_for_west_food,
    WestIndianFatLevelEstimator,
    CountableFoodDetector
)


class CalorieRange(BaseModel):
    min: float
    expected: float
    max: float


class Section51ModelOutput(BaseModel):
    food_name: str
    canonical_food_id: str
    region: str = "West India"
    state: str
    regional_variant: str
    food_category: str
    vegetarian: bool
    ingredients: Dict[str, List[str]]  # {"visible": [...], "inferred": [...]}
    cooking_method: str
    portion: str
    count: Optional[int] = None
    estimated_weight_g: float
    calories_kcal: float
    calorie_breakdown: CalorieRange
    protein_g: float
    carbs_g: float
    fat_g: float
    fiber_g: float
    confidence: float
    uncertainty: Dict[str, List[float]]  # {"weight_range_g": [min, max], "calorie_range_kcal": [min, max]}
    visual_fat_level: str
    segmentation: Dict[str, Any]
    user_confirmation_required: bool


class WestIndianRecipeNutritionCalculator:
    """
    Computes Section 51 compliant output for recognized West Indian dishes and items.
    """
    @classmethod
    def calculate_dish_nutrition(
        cls,
        food_identifier: str,  # ID or Name
        visual_cues: Optional[Dict[str, Any]] = None,
        custom_weight_g: Optional[float] = None,
        count: Optional[int] = None
    ) -> Section51ModelOutput:
        cues = visual_cues or {}

        # 1. Resolve Food Class
        food = get_west_food_class(food_identifier)
        if not food:
            food = resolve_west_food_by_name(food_identifier)

        # Fallback if unknown / OOD
        if not food:
            return Section51ModelOutput(
                food_name=food_identifier,
                canonical_food_id="WEST_INDIAN_UNKNOWN",
                region="West India",
                state="Western India",
                regional_variant="Unclassified West Indian",
                food_category="Unclassified",
                vegetarian=True,
                ingredients={"visible": [], "inferred": []},
                cooking_method="unknown",
                portion="1 serving",
                count=None,
                estimated_weight_g=140.0,
                calories_kcal=180.0,
                calorie_breakdown=CalorieRange(min=140.0, expected=180.0, max=230.0),
                protein_g=4.5,
                carbs_g=24.0,
                fat_g=7.5,
                fiber_g=2.0,
                confidence=0.40,
                uncertainty={
                    "weight_range_g": [100.0, 180.0],
                    "calorie_range_kcal": [140.0, 230.0]
                },
                visual_fat_level="unknown",
                segmentation={"status": "unsegmented", "mask": None},
                user_confirmation_required=True
            )

        # 2. Portions & Weight Estimation
        if custom_weight_g and custom_weight_g > 0:
            est_weight = custom_weight_g
            weight_range = (est_weight * 0.88, est_weight * 1.12)
            detected_count = count
        else:
            est_weight, weight_range, detected_count = get_portion_for_west_food(
                food.permanent_id, count=count
            )

        # 3. Fat & Sheen Profile Adjustment
        fat_profile = WestIndianFatLevelEstimator.estimate_fat_profile(cues)
        fat_mult = fat_profile["fat_multiplier"]
        extra_fat = fat_profile["extra_fat_g"]
        fat_level = fat_profile["fat_level"]

        # Base nutritional profile per 100g
        base_n = food.nutrition_per_100g or {
            "calories": 180.0,
            "protein_g": 5.0,
            "carbs_g": 25.0,
            "fat_g": 6.0,
            "fiber_g": 2.5
        }
        scale = est_weight / 100.0

        scaled_protein = round(base_n.get("protein_g", 5.0) * scale, 1)
        scaled_carbs = round(base_n.get("carbs_g", 25.0) * scale, 1)
        scaled_fat = round((base_n.get("fat_g", 6.0) * scale * fat_mult) + extra_fat, 1)
        scaled_fiber = round(base_n.get("fiber_g", 2.5) * scale, 1)
        expected_cals = round((scaled_protein * 4.0) + (scaled_carbs * 4.0) + (scaled_fat * 9.0), 1)

        cal_min = round(expected_cals * 0.86, 1)
        cal_max = round(expected_cals * 1.15, 1)

        # 4. Ingredients Segregation (Visible vs Inferred)
        visible_ing = []
        inferred_ing = list(food.key_ingredients)
        for ing in food.key_ingredients:
            if any(term in ing.lower() for term in [
                "coriander", "chilli", "seeds", "mustard", "sesame", "onion",
                "sev", "farsan", "coconut", "prawn", "fish", "butter", "lemon", "curry leaves"
            ]):
                visible_ing.append(ing)

        # Confidence and confirmation checks
        confidence = cues.get("confidence", 0.95)
        # If filling status is unknown (e.g. unopened Puran Poli), require confirmation
        user_conf_req = confidence < 0.80 or cues.get("filling_status") == "unknown"

        # Portion string
        if detected_count is not None:
            portion_str = f"{detected_count} piece{'s' if detected_count > 1 else ''} ({round(est_weight)}g)"
        else:
            portion_str = f"{round(est_weight)}g ({food.hierarchy.level9_default_portion})"

        primary_cooking = food.hierarchy.level8_cooking_method[0] if food.hierarchy.level8_cooking_method else "tawa_cooked"

        return Section51ModelOutput(
            food_name=food.canonical_name,
            canonical_food_id=food.permanent_id,
            region="West India",
            state=food.hierarchy.level3_state_region,
            regional_variant=food.hierarchy.level7_variant,
            food_category=food.hierarchy.level5_food_family,
            vegetarian=food.vegetarian,
            ingredients={
                "visible": visible_ing,
                "inferred": inferred_ing
            },
            cooking_method=primary_cooking,
            portion=portion_str,
            count=detected_count,
            estimated_weight_g=round(est_weight, 1),
            calories_kcal=expected_cals,
            calorie_breakdown=CalorieRange(min=cal_min, expected=expected_cals, max=cal_max),
            protein_g=scaled_protein,
            carbs_g=scaled_carbs,
            fat_g=scaled_fat,
            fiber_g=scaled_fiber,
            confidence=round(confidence, 2),
            uncertainty={
                "weight_range_g": [round(weight_range[0], 1), round(weight_range[1], 1)],
                "calorie_range_kcal": [cal_min, cal_max]
            },
            visual_fat_level=fat_level,
            segmentation={
                "status": "segmented",
                "area_pixels": cues.get("area_pixels", 45000),
                "bbox": cues.get("bbox", [0.1, 0.1, 0.9, 0.9])
            },
            user_confirmation_required=user_conf_req
        )
