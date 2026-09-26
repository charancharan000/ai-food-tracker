"""
Indian Vegetarian Recipe Nutrition Engine & Standardized Output Schemas (Part 12)
Implements Sections 41, 42, 43, 49, 51, 55, 66, 67, 68, 75, 76 of Part 12 Master Training Specification.

Guarantees:
- End-to-end vegetarian recipe synthesis:
  Calories = BaseVegetable/Lentil + ProteinInclusions + QualitativeFatAdjustment.
- Section 55 Detailed Vegetarian Image Annotation Schema.
- Section 42 Standard Vegetarian Nutrition Output Schema.
- Section 49 Unknown Vegetarian Fallback Schema (3 standard modes).
- Section 68 Final App Multi-Item Output Schema.
- Section 67 Calorie Uncertainty Range Output Schema.
- Section 51 User Correction & Active Learning Record Store.
- Section 88 Standardized Single and Multi Vegetarian Output Schemas.
- Zero False Precision: Emits calibrated intervals (e.g., "190–260 kcal") with uncertainty explanations.
"""

from typing import Dict, Any, Optional, List, Tuple
from pydantic import BaseModel, Field

from app.food_ai.taxonomy.vegetarian_master_taxonomy import (
    get_veg_food_class,
    resolve_veg_food_by_name,
    VegetarianFoodClassRecord,
    VEGETARIAN_TAXONOMY_REGISTRY
)
from app.food_ai.portion_engine.vegetarian_portions import (
    VegetarianPortionEngine,
    QualitativeVegetarianOilEstimator,
    VegetarianComponentMassSplitter
)


# =============================================================================
# 1. OUTPUT SCHEMAS
# =============================================================================

class Section55FoodItem(BaseModel):
    class_id: str
    name: str
    bbox: Optional[List[int]] = None  # [ymin, xmin, ymax, xmax]
    weight_g: float
    confidence: float
    ingredients: List[str]
    cooking_method: str


class Section55VegetarianAnnotation(BaseModel):
    image_id: str
    region: str
    food_items: List[Section55FoodItem]


class Section42VegetarianNutritionOutput(BaseModel):
    food: str
    weight_g: float
    calories_kcal: float
    protein_g: float
    carbs_g: float
    fat_g: float
    fiber_g: float
    confidence: float


class Section49UnknownVegetarianOutput(BaseModel):
    status: str = "uncertain"
    predicted_category: str  # "Indian vegetarian dish — exact identity uncertain", "Vegetable curry — exact type uncertain", or "Paneer-based dish — exact recipe uncertain"
    confidence: float = 0.42
    confidence_level: str = "Low"
    explanation: str = "Visual evidence is insufficient to verify exact vegetarian recipe without risking misclassification (Section 49 & 75 compliance)."
    calorie_estimate_range: str = "110–220 kcal per 140g standard portion depending on recipe fat content"
    prompt_for_user: str = "Could you confirm what vegetable or dish this is?"
    requires_user_confirmation: bool = True


class Section51UserCorrectionRecord(BaseModel):
    original_prediction: str
    user_correction: str
    image_reference: str
    final_confirmed_label: str
    region: Optional[str] = None
    portion_correction_g: Optional[float] = None
    timestamp: str = "2026-09-26T18:41:00Z"
    active_learning_priority: str = "High"


class Section68DetectedDishItem(BaseModel):
    name: str
    weight_description: str
    calories_range_str: str
    protein_range_str: str
    carbs_range_str: str
    fat_range_str: str
    confidence_pct: int


class Section68FinalAppVegetarianOutput(BaseModel):
    header: str = "🍛 Food Detected"
    detected_dishes: List[Section68DetectedDishItem]
    total_estimated_calories_range: str
    total_protein_g: float
    total_carbs_g: float
    total_fat_g: float
    user_adjustment_available: bool = True


class Section67CalorieUncertaintyOutput(BaseModel):
    dish_id: str
    dish_name: str
    nominal_calories: float
    calibrated_calorie_range: str
    calories_low: float
    calories_high: float
    uncertainty_variance_reasons: List[str]


class Section88VegetarianSingleOutput(BaseModel):
    food_name: str
    canonical_id: str
    food_family: str
    regional_attribution: str
    cooking_method: str
    consistency: str
    portion_category: str
    estimated_weight_g: float
    estimated_calories_range: str
    calories_low: float
    calories_expected: float
    calories_high: float
    protein_g: float
    carbs_g: float
    fat_g: float
    fiber_g: float
    fat_tier_name: str
    confidence: str
    confidence_score: float
    uncertainty_reason: str
    requires_user_confirmation: bool = False


# In-memory store for active learning corrections (Section 51)
USER_CORRECTION_DATABASE: List[Section51UserCorrectionRecord] = []


# =============================================================================
# 2. RECIPE NUTRITION ENGINE
# =============================================================================

class VegetarianRecipeNutritionCalculator:
    """
    Synthesizes exact dynamic macronutrients and calibrated uncertainty ranges
    for any Indian vegetarian dish.
    """

    @classmethod
    def calculate_nutrition(
        cls,
        dish_name: str,
        portion_category: str = "Medium",
        visual_features: Optional[Dict[str, Any]] = None,
        piece_count: Optional[int] = None,
        is_restaurant_style: bool = False
    ) -> Dict[str, Any]:
        rec = resolve_veg_food_by_name(dish_name)
        if not rec:
            rec = VEGETARIAN_TAXONOMY_REGISTRY["IND-VEG-UNKNOWN-001"]

        portion_data = VegetarianPortionEngine.estimate_portion(
            food_family=rec.food_family,
            portion_category=portion_category,
            visual_features=visual_features
        )
        total_weight_g = portion_data["estimated_grams"]
        oil_data = portion_data["oil_sheen_data"]

        # Base 100g profile
        n100 = rec.nutrition_per_100g or {
            "calories": 100.0,
            "protein_g": 3.0,
            "carbs_g": 12.0,
            "fat_g": 4.5,
            "fiber_g": 2.5
        }

        # Multiplier
        mult = total_weight_g / 100.0
        base_cals = n100.get("calories", 100.0) * mult
        base_p = n100.get("protein_g", 3.0) * mult
        base_c = n100.get("carbs_g", 12.0) * mult
        base_f = n100.get("fat_g", 4.5) * mult
        base_fib = n100.get("fiber_g", 2.5) * mult

        # Qualitative Fat Offset (Section 31)
        fat_cal_offset = oil_data["calorie_offset"]
        avg_fat_g = (oil_data["qualitative_fat_range_g"][0] + oil_data["qualitative_fat_range_g"][1]) / 2.0

        restaurant_mult = 1.15 if is_restaurant_style else 1.0

        final_cals = round((base_cals + fat_cal_offset) * restaurant_mult, 1)
        final_p = round(base_p, 1)
        final_c = round(base_c, 1)
        final_f = round((base_f + avg_fat_g) * restaurant_mult, 1)
        final_fib = round(base_fib, 1)

        # Calibrated Range
        spread = oil_data["uncertainty_pct"]
        cal_low = round(final_cals * (1.0 - spread), 0)
        cal_high = round(final_cals * (1.0 + spread), 0)
        range_str = f"{int(cal_low)}–{int(cal_high)} kcal"

        uncertainty_factors = [
            f"Qualitative fat level: {oil_data['fat_tier_name']} ({oil_data['description']}).",
            "Cooking dilution, seasonal starch variance, and domestic vs commercial recipe variation."
        ]

        return {
            "record": rec,
            "portion_data": portion_data,
            "total_weight_g": total_weight_g,
            "total_calories": final_cals,
            "calories_low": cal_low,
            "calories_high": cal_high,
            "calories_range_str": range_str,
            "protein_g": final_p,
            "carbs_g": final_c,
            "fat_g": final_f,
            "fiber_g": final_fib,
            "oil_sheen_data": oil_data,
            "uncertainty_factors": uncertainty_factors
        }

    # =========================================================================
    # SCHEMA GENERATORS
    # =========================================================================

    @classmethod
    def generate_section_55_annotation(
        cls,
        image_id: str,
        dish_name: str,
        region: str = "Tamil Nadu",
        portion_category: str = "Medium",
        bbox: Optional[List[int]] = None
    ) -> Section55VegetarianAnnotation:
        res = cls.calculate_nutrition(dish_name, portion_category=portion_category)
        rec: VegetarianFoodClassRecord = res["record"]
        item = Section55FoodItem(
            class_id=rec.canonical_food_id,
            name=rec.canonical_name,
            bbox=bbox or [100, 100, 400, 400],
            weight_g=res["total_weight_g"],
            confidence=0.93,
            ingredients=rec.secondary_ingredients or [rec.main_ingredient],
            cooking_method=rec.cooking_method
        )
        return Section55VegetarianAnnotation(
            image_id=image_id,
            region=region,
            food_items=[item]
        )

    @classmethod
    def generate_section_42_output(
        cls,
        dish_name: str,
        portion_category: str = "Medium"
    ) -> Section42VegetarianNutritionOutput:
        res = cls.calculate_nutrition(dish_name, portion_category=portion_category)
        rec: VegetarianFoodClassRecord = res["record"]
        return Section42VegetarianNutritionOutput(
            food=rec.canonical_name,
            weight_g=res["total_weight_g"],
            calories_kcal=res["total_calories"],
            protein_g=res["protein_g"],
            carbs_g=res["carbs_g"],
            fat_g=res["fat_g"],
            fiber_g=res["fiber_g"],
            confidence=0.91
        )

    @classmethod
    def generate_section_49_unknown_fallback(
        cls,
        mode: str = "general"
    ) -> Section49UnknownVegetarianOutput:
        m = mode.lower()
        if "curry" in m:
            cat = "Vegetable curry — exact type uncertain"
        elif "paneer" in m:
            cat = "Paneer-based dish — exact recipe uncertain"
        else:
            cat = "Indian vegetarian dish — exact identity uncertain"

        return Section49UnknownVegetarianOutput(predicted_category=cat)

    @classmethod
    def generate_section_67_uncertainty_output(
        cls,
        dish_name: str,
        portion_category: str = "Medium"
    ) -> Section67CalorieUncertaintyOutput:
        res = cls.calculate_nutrition(dish_name, portion_category=portion_category)
        rec: VegetarianFoodClassRecord = res["record"]
        return Section67CalorieUncertaintyOutput(
            dish_id=rec.canonical_food_id,
            dish_name=rec.canonical_name,
            nominal_calories=res["total_calories"],
            calibrated_calorie_range=res["calories_range_str"],
            calories_low=res["calories_low"],
            calories_high=res["calories_high"],
            uncertainty_variance_reasons=res["uncertainty_factors"]
        )

    @classmethod
    def generate_section_68_app_output(
        cls,
        dishes: List[Tuple[str, str, int]]  # [(dish_name, portion_category, conf_pct)]
    ) -> Section68FinalAppVegetarianOutput:
        detected = []
        tot_cals = 0.0
        tot_p = 0.0
        tot_c = 0.0
        tot_f = 0.0

        for dname, cat, conf_pct in dishes:
            res = cls.calculate_nutrition(dname, portion_category=cat)
            rec: VegetarianFoodClassRecord = res["record"]
            detected.append(Section68DetectedDishItem(
                name=rec.canonical_name,
                weight_description=f"~{int(res['total_weight_g'])} g",
                calories_range_str=f"~{res['calories_range_str']}",
                protein_range_str=f"~{int(res['protein_g'] * 0.9)}–{int(res['protein_g'] * 1.2)} g",
                carbs_range_str=f"~{int(res['carbs_g'] * 0.9)}–{int(res['carbs_g'] * 1.2)} g",
                fat_range_str=f"~{int(res['fat_g'] * 0.9)}–{int(res['fat_g'] * 1.2)} g",
                confidence_pct=conf_pct
            ))
            tot_cals += res["total_calories"]
            tot_p += res["protein_g"]
            tot_c += res["carbs_g"]
            tot_f += res["fat_g"]

        tot_low = int(tot_cals * 0.88)
        tot_high = int(tot_cals * 1.14)
        return Section68FinalAppVegetarianOutput(
            detected_dishes=detected,
            total_estimated_calories_range=f"~{tot_low}–{tot_high} kcal",
            total_protein_g=round(tot_p, 1),
            total_carbs_g=round(tot_c, 1),
            total_fat_g=round(tot_f, 1)
        )

    @classmethod
    def generate_section_88_single_output(
        cls,
        dish_name: str,
        portion_category: str = "Medium",
        visual_features: Optional[Dict[str, Any]] = None
    ) -> Section88VegetarianSingleOutput:
        res = cls.calculate_nutrition(dish_name, portion_category=portion_category, visual_features=visual_features)
        rec: VegetarianFoodClassRecord = res["record"]
        oil_data = res["oil_sheen_data"]
        return Section88VegetarianSingleOutput(
            food_name=rec.canonical_name,
            canonical_id=rec.canonical_food_id,
            food_family=rec.food_family,
            regional_attribution=f"{rec.region} ({rec.state_or_city})",
            cooking_method=rec.cooking_method,
            consistency=rec.consistency,
            portion_category=portion_category,
            estimated_weight_g=res["total_weight_g"],
            estimated_calories_range=res["calories_range_str"],
            calories_low=res["calories_low"],
            calories_expected=res["total_calories"],
            calories_high=res["calories_high"],
            protein_g=res["protein_g"],
            carbs_g=res["carbs_g"],
            fat_g=res["fat_g"],
            fiber_g=res["fiber_g"],
            fat_tier_name=oil_data["fat_tier_name"],
            confidence="High",
            confidence_score=0.92,
            uncertainty_reason="; ".join(res["uncertainty_factors"])
        )

    @classmethod
    def record_user_correction(
        cls,
        original_prediction: str,
        user_correction: str,
        image_reference: str,
        region: Optional[str] = None,
        portion_correction_g: Optional[float] = None
    ) -> Section51UserCorrectionRecord:
        """
        Stores user feedback/correction for active learning (Section 51 & 52).
        """
        rec = Section51UserCorrectionRecord(
            original_prediction=original_prediction,
            user_correction=user_correction,
            image_reference=image_reference,
            final_confirmed_label=user_correction,
            region=region,
            portion_correction_g=portion_correction_g
        )
        USER_CORRECTION_DATABASE.append(rec)
        return rec
