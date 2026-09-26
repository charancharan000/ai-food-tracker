"""
Nutrition Uncertainty and Confidence Calibration Engine
Computes honest confidence scores and realistic min/best/max nutritional intervals
derived from physical weight error distributions and recipe variance.
"""

from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

class CalibratedNutritionEstimate(BaseModel):
    dish_name: str
    estimated_weight_g: float
    weight_range_g: Dict[str, float] = Field(..., description="min, best, max physical weight")
    
    calories_best: float
    calories_low: float
    calories_high: float

    protein_g: float
    carbs_g: float
    fat_g: float
    fiber_g: float
    sodium_mg: float

    food_confidence: float = Field(..., ge=0.0, le=1.0)
    weight_confidence: float = Field(..., ge=0.0, le=1.0)
    nutrition_confidence: float = Field(..., ge=0.0, le=1.0)
    overall_confidence: float = Field(..., ge=0.0, le=1.0)
    explanation: str

def compute_calibrated_bounds(
    dish_name: str,
    base_weight_g: float,
    calories_per_100g_best: float,
    calories_per_100g_low: float,
    calories_per_100g_high: float,
    protein_per_100g: float,
    carbs_per_100g: float,
    fat_per_100g: float,
    fiber_per_100g: float,
    sodium_per_100g: float,
    has_reference_object: bool = False,
    is_multi_view: bool = False,
    raw_classifier_confidence: float = 0.95
) -> CalibratedNutritionEstimate:
    """
    Computes rigorous uncertainty bounds.
    - If user provides two views + reference plate, weight variance is narrowed from +-14% to +-5%.
    - If single photo, honest dispersion is preserved.
    """
    if is_multi_view and has_reference_object:
        weight_err_pct = 0.05
        weight_conf = 0.94
    elif has_reference_object:
        weight_err_pct = 0.09
        weight_conf = 0.88
    elif is_multi_view:
        weight_err_pct = 0.10
        weight_conf = 0.84
    else:
        weight_err_pct = 0.14
        weight_conf = 0.78

    w_min = round(base_weight_g * (1.0 - weight_err_pct), 1)
    w_best = round(base_weight_g, 1)
    w_max = round(base_weight_g * (1.0 + weight_err_pct), 1)

    cals_low = round((w_min * calories_per_100g_low) / 100.0, 1)
    cals_best = round((w_best * calories_per_100g_best) / 100.0, 1)
    cals_high = round((w_max * calories_per_100g_high) / 100.0, 1)

    # Calibrate overall score
    food_conf = min(0.99, max(0.40, raw_classifier_confidence))
    nutrition_conf = 0.92 if calories_per_100g_best > 0 else 0.70
    overall = round((food_conf * 0.40) + (weight_conf * 0.35) + (nutrition_conf * 0.25), 2)

    mode_str = "Two-View Scaled" if is_multi_view else "Single-View"
    ref_str = "with Reference Scale" if has_reference_object else "standard perspective estimation"

    return CalibratedNutritionEstimate(
        dish_name=dish_name,
        estimated_weight_g=w_best,
        weight_range_g={"min": w_min, "best": w_best, "max": w_max},
        calories_best=cals_best,
        calories_low=cals_low,
        calories_high=cals_high,
        protein_g=round((w_best * protein_per_100g) / 100.0, 1),
        carbs_g=round((w_best * carbs_per_100g) / 100.0, 1),
        fat_g=round((w_best * fat_per_100g) / 100.0, 1),
        fiber_g=round((w_best * fiber_per_100g) / 100.0, 1),
        sodium_mg=round((w_best * sodium_per_100g) / 100.0, 1),
        food_confidence=round(food_conf, 2),
        weight_confidence=round(weight_conf, 2),
        nutrition_confidence=round(nutrition_conf, 2),
        overall_confidence=overall,
        explanation=f"{mode_str} analysis ({ref_str}). Calorie interval covers ±{int(weight_err_pct*100)}% portion variance and household-to-restaurant cooking oil recipes."
    )
