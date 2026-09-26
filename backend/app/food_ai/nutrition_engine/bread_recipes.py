"""
Indian Bread Recipe Nutrition Engine & Section 82 Output Schemas (Part 10)
Implements Sections 64, 65, 78, 81, 82, 84, 85 of Part 10 Master Training Specification.

Guarantees:
- End-to-end bread recipe synthesis:
  Calories = BaseBreadDough + StuffingCore + CookingFatAdjustment + SurfaceGlaze (butter/ghee).
- Section 82 Standardized Single Bread & Composite Output Schemas:
  * Single Bread: Canonical name, family, flour, method, stuffing, piece count, portion (g),
    calibrated calorie range (e.g., "520–680 kcal"), protein, carbs, fat, fiber, fat level, confidence.
  * Composite Plate: Itemized constituent list with independent weights and calories, plus aggregated range.
- Section 84 & 85 Non-Negotiable Rules:
  * Calibrated ranges instead of false precision (never 287 kcal).
  * Never classifies every round bread as chapati or oval as naan.
  * Never assumes butter from shine alone.
  * Fallback to 'Indian bread detected — specific type uncertain' (BREAD_UNKNOWN_001) with Low confidence
    when visual evidence is insufficient.
"""

from typing import Dict, Any, Optional, List, Tuple
from pydantic import BaseModel, Field

from app.food_ai.taxonomy.bread_master_taxonomy import (
    get_bread_food_class,
    resolve_bread_food_by_name,
    BreadFoodClassRecord,
    BREAD_TAXONOMY_REGISTRY
)
from app.food_ai.portion_engine.bread_portions import (
    resolve_bread_portion,
    BreadFatEstimator,
    BreadStuffingDoughRatioEstimator,
    BreadFatEstimationResult
)


class Section82BreadSingleOutput(BaseModel):
    food_name: str
    canonical_id: str
    bread_family: str
    flour_type: str
    cooking_method: str
    stuffing_type: str
    piece_count: int
    estimated_portion_g: float
    estimated_calories_range: str  # e.g., "520–680 kcal"
    calories_low: float
    calories_expected: float
    calories_high: float
    protein_range_g: str           # e.g., "12–16 g"
    protein_g: float
    carbohydrates_range_g: str     # e.g., "75–95 g"
    carbs_g: float
    fat_range_g: str               # e.g., "18–26 g"
    fat_g: float
    fiber_g: float
    confidence: str                # "High", "Medium", "Low"
    confidence_score: float
    fat_level_estimate: str        # "Very Low", "Low", "Medium", "High", "Very High", "Unknown"
    uncertainty_reason: str
    requires_user_confirmation: bool = False
    confirmation_prompt: Optional[str] = None


class Section82DetectedBreadItem(BaseModel):
    item_index: int
    name: str
    count: Optional[int] = None
    estimated_weight_g: float
    calories_expected: float
    item_type: str = "bread"  # "bread", "curry", "accompaniment"


class Section82BreadMultiOutput(BaseModel):
    plate_title: str
    detected_items: List[Section82DetectedBreadItem]
    total_estimated_weight_g: float
    total_estimated_calories_range: str  # e.g., "650–850 kcal"
    total_calories_low: float
    total_calories_expected: float
    total_calories_high: float
    total_protein_g: float
    total_carbs_g: float
    total_fat_g: float
    total_fiber_g: float
    overall_confidence: str              # "High", "Medium", "Low"
    overall_confidence_score: float


class BreadRecipeNutritionCalculator:
    """
    Implements Sections 64, 65, 82, 84, 85:
    Calculates component-wise nutrition with calibrated uncertainty ranges.
    """

    @classmethod
    def calculate_single_dish(
        cls,
        food_identifier: str,
        visual_cues: Optional[Dict[str, Any]] = None,
        custom_weight_g: Optional[float] = None,
        piece_count: int = 1,
        portion_category: str = "Medium",
        diameter_cm: Optional[float] = None,
        has_butter_slab: bool = False,
        fat_override: Optional[str] = None
    ) -> Section82BreadSingleOutput:
        cues = visual_cues or {}
        if has_butter_slab:
            cues["butter_slab_present"] = True

        # Resolve bread class
        rec = resolve_bread_food_by_name(food_identifier)
        if not rec:
            rec = get_bread_food_class("BREAD_UNKNOWN_001")

        if not rec:
            # Absolute fallback
            rec = BREAD_TAXONOMY_REGISTRY["BREAD_UNKNOWN_001"]

        # Check for Section 84/85 unknown fallback condition
        is_unknown = (
            rec.canonical_food_id == "BREAD_UNKNOWN_001"
            or cues.get("low_visual_evidence", False)
            or cues.get("classification_ambiguous", False)
        )

        if is_unknown:
            confidence = "Low"
            conf_score = 0.45
            uncertainty_reason = "Visual evidence insufficient or bread family ambiguous; defaulting to broad Indian bread range per Rule 85."
            requires_confirm = True
            confirm_prompt = "Is this Chapati, Tandoori Roti, Paratha, or another regional Indian bread?"
        else:
            confidence = cues.get("override_confidence", "High")
            conf_score = cues.get("override_confidence_score", 0.92)
            uncertainty_reason = "Identified with high confidence using fine-grained morphological cues."
            requires_confirm = False
            confirm_prompt = None

        # Portion calculation
        count = max(1, piece_count)
        if custom_weight_g:
            total_mass_g = custom_weight_g
            mass_min = round(custom_weight_g * 0.85, 1)
            mass_max = round(custom_weight_g * 1.15, 1)
        else:
            total_mass_g, (mass_min, mass_max) = resolve_bread_portion(
                bread_type=rec.canonical_food_id,
                portion_category=portion_category,
                count=count,
                diameter_cm=diameter_cm
            )

        # Fat estimation
        fat_res = BreadFatEstimator.estimate_fat(
            bread_canonical_name=rec.canonical_name,
            cooking_method=rec.cooking_method,
            surface_cues=cues
        )
        if fat_override:
            fat_level = fat_override
        else:
            fat_level = fat_res.fat_level

        # Baseline nutrition per 100g from verified taxonomy record
        base_cal_100g = rec.nutrition_per_100g.get("calories", 260.0)
        base_pro_100g = rec.nutrition_per_100g.get("protein_g", 7.0)
        base_carb_100g = rec.nutrition_per_100g.get("carbs_g", 48.0)
        base_fat_100g = rec.nutrition_per_100g.get("fat_g", 4.0)
        base_fib_100g = rec.nutrition_per_100g.get("fiber_g", 4.0)

        # Raw dough/stuffing baseline
        scale_factor = total_mass_g / 100.0
        cal_base = base_cal_100g * scale_factor
        pro_base = base_pro_100g * scale_factor
        carb_base = base_carb_100g * scale_factor
        fat_base = base_fat_100g * scale_factor
        fib_base = base_fib_100g * scale_factor

        # Added fat adjustments (butter slab / heavy ghee glaze)
        added_fat_g = fat_res.added_fat_typical_g * count
        added_fat_cal = added_fat_g * 9.0

        cal_expected = round(cal_base + added_fat_cal, 1)
        fat_expected = round(fat_base + added_fat_g, 1)
        pro_expected = round(pro_base, 1)
        carb_expected = round(carb_base, 1)
        fib_expected = round(fib_base, 1)

        # Range width calculation (Section 84: wider for high fat or unknown, never fake precision)
        if is_unknown or fat_level in ["High", "Very High", "Unknown"]:
            spread_factor = 0.18
        else:
            spread_factor = 0.12

        cal_low = round((cal_expected * (1.0 - spread_factor)) / 10.0) * 10
        cal_high = round((cal_expected * (1.0 + spread_factor)) / 10.0) * 10
        cal_range_str = f"{int(cal_low)}–{int(cal_high)} kcal"

        pro_low = max(1.0, round(pro_expected * 0.85))
        pro_high = round(pro_expected * 1.15)
        pro_range_str = f"{int(pro_low)}–{int(pro_high)} g"

        carb_low = max(5.0, round(carb_expected * 0.88))
        carb_high = round(carb_expected * 1.12)
        carb_range_str = f"{int(carb_low)}–{int(carb_high)} g"

        fat_low = max(0.5, round(fat_expected * 0.82))
        fat_high = round(fat_expected * 1.18)
        fat_range_str = f"{int(fat_low)}–{int(fat_high)} g"

        return Section82BreadSingleOutput(
            food_name=rec.canonical_name,
            canonical_id=rec.canonical_food_id,
            bread_family=rec.bread_family,
            flour_type=rec.flour_type,
            cooking_method=rec.cooking_method,
            stuffing_type=rec.stuffing_type,
            piece_count=count,
            estimated_portion_g=total_mass_g,
            estimated_calories_range=cal_range_str,
            calories_low=float(cal_low),
            calories_expected=cal_expected,
            calories_high=float(cal_high),
            protein_range_g=pro_range_str,
            protein_g=pro_expected,
            carbohydrates_range_g=carb_range_str,
            carbs_g=carb_expected,
            fat_range_g=fat_range_str,
            fat_g=fat_expected,
            fiber_g=fib_expected,
            confidence=confidence,
            confidence_score=conf_score,
            fat_level_estimate=fat_level,
            uncertainty_reason=uncertainty_reason,
            requires_user_confirmation=requires_confirm,
            confirmation_prompt=confirm_prompt
        )

    @classmethod
    def calculate_composite_plate(
        cls,
        plate_title: str,
        items: List[Dict[str, Any]]
    ) -> Section82BreadMultiOutput:
        """
        Decomposes full bread meals (e.g. 2 Roti + Dal Tadka + Sabzi, Paratha Thali, Chole Bhature).
        Itemizes each component independently.
        """
        detected_items: List[Section82DetectedBreadItem] = []
        total_weight = 0.0
        tot_cal_exp = 0.0
        tot_pro = 0.0
        tot_carb = 0.0
        tot_fat = 0.0
        tot_fib = 0.0
        conf_scores: List[float] = []

        for idx, item in enumerate(items, start=1):
            name = item.get("name", "Unknown Item")
            weight_g = float(item.get("weight_g", 100.0))
            cal_exp = float(item.get("calories", 0.0))
            pro_g = float(item.get("protein_g", 0.0))
            carb_g = float(item.get("carbs_g", 0.0))
            fat_g = float(item.get("fat_g", 0.0))
            fib_g = float(item.get("fiber_g", 0.0))
            count = item.get("count")
            itype = item.get("type", "bread")

            # If calories not provided directly, calculate via single bread
            if cal_exp == 0.0:
                calc = cls.calculate_single_dish(
                    food_identifier=name,
                    custom_weight_g=weight_g,
                    piece_count=count or 1
                )
                cal_exp = calc.calories_expected
                pro_g = calc.protein_g
                carb_g = calc.carbs_g
                fat_g = calc.fat_g
                fib_g = calc.fiber_g
                conf_scores.append(calc.confidence_score)
            else:
                conf_scores.append(item.get("confidence_score", 0.90))

            detected_items.append(Section82DetectedBreadItem(
                item_index=idx,
                name=name,
                count=count,
                estimated_weight_g=round(weight_g, 1),
                calories_expected=round(cal_exp, 1),
                item_type=itype
            ))

            total_weight += weight_g
            tot_cal_exp += cal_exp
            tot_pro += pro_g
            tot_carb += carb_g
            tot_fat += fat_g
            tot_fib += fib_g

        # Aggregated calibrated range
        tot_cal_low = round((tot_cal_exp * 0.88) / 10.0) * 10
        tot_cal_high = round((tot_cal_exp * 1.12) / 10.0) * 10
        cal_range_str = f"{int(tot_cal_low)}–{int(tot_cal_high)} kcal"

        avg_conf = sum(conf_scores) / len(conf_scores) if conf_scores else 0.85
        if avg_conf >= 0.85:
            overall_conf = "High"
        elif avg_conf >= 0.70:
            overall_conf = "Medium"
        else:
            overall_conf = "Low"

        return Section82BreadMultiOutput(
            plate_title=plate_title,
            detected_items=detected_items,
            total_estimated_weight_g=round(total_weight, 1),
            total_estimated_calories_range=cal_range_str,
            total_calories_low=float(tot_cal_low),
            total_calories_expected=round(tot_cal_exp, 1),
            total_calories_high=float(tot_cal_high),
            total_protein_g=round(tot_pro, 1),
            total_carbs_g=round(tot_carb, 1),
            total_fat_g=round(tot_fat, 1),
            total_fiber_g=round(tot_fib, 1),
            overall_confidence=overall_conf,
            overall_confidence_score=round(avg_conf, 2)
        )
