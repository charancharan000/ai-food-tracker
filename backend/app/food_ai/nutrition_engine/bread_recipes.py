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


# =============================================================================
# SECTIONS 50, 51, 62 — SPEC-ALIGNED SCHEMAS
# =============================================================================

class Section50BreadSingleAnnotation(BaseModel):
    """
    Section 50: Image Annotation Schema (Single Bread Image)
    """
    food_category: str = "bread"
    region: str = "north_indian"
    food_name: str = "aloo_paratha"
    variant: str = "stuffed"
    flour: str = "wheat"
    cooking_method: str = "tawa"
    stuffing: List[str] = Field(default_factory=lambda: ["potato"])
    toppings: List[str] = Field(default_factory=lambda: ["butter"])
    count: int = 2
    estimated_weight_g: float = 180.0
    confidence: float = 0.91


class Section50FoodItem(BaseModel):
    name: str
    count: Optional[int] = None
    estimated_weight_g: float


class Section50MultiFoodAnnotation(BaseModel):
    """
    Section 50: Multi-Food Annotation Schema
    """
    foods: List[Section50FoodItem]


class Section51UnknownBreadOutput(BaseModel):
    """
    Section 51: Unknown Bread System Fallback
    If uncertain, do NOT force 'Roti'. Instead return:
    'Indian flatbread — exact type uncertain' or
    'Bread-like food — insufficient visual evidence'
    """
    status: str = "uncertain"
    food_category: str = "bread"
    prediction: str = "Indian flatbread — exact type uncertain"
    fallback_alternative: str = "Bread-like food — insufficient visual evidence"
    confidence: float = 0.38
    user_confirmation_required: bool = True
    prompt: str = "Could you specify which Indian bread this is? (e.g. Chapati, Naan, Paratha, Kulcha)"


class Section62DetectedItem(BaseModel):
    food_name: str
    quantity: int = 1
    estimated_weight_g: float
    calorie_range_kcal: List[int]
    protein_range_g: List[int]
    carbs_range_g: Optional[List[int]] = None
    fat_range_g: Optional[List[int]] = None
    confidence: str = "High"
    editable_fields: List[str] = Field(default_factory=lambda: ["food", "quantity", "weight", "recipe", "oil_ghee", "toppings"])


class Section62FinalAppOutput(BaseModel):
    """
    Section 62: Final App Output
    Example:
    Detected Foods:
    Aloo Paratha (Quantity: 2, Weight: 180g, Calories: range, Confidence: High)
    Curd (Weight: 100g, Calories: range, Confidence: Medium)
    Pickle (Weight: 15g, Calories: range, Confidence: Medium)
    Allows user to edit: food, quantity, weight, recipe, oil/ghee, toppings.
    """
    meal_title: str
    detected_foods: List[Section62DetectedItem]
    total_estimated_weight_g: float
    total_estimated_calories_range: str
    user_can_edit: bool = True


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

    @classmethod
    def generate_section_50_single_annotation(
        cls,
        food_category: str = "bread",
        region: str = "north_indian",
        food_name: str = "aloo_paratha",
        variant: str = "stuffed",
        flour: str = "wheat",
        cooking_method: str = "tawa",
        stuffing: Optional[List[str]] = None,
        toppings: Optional[List[str]] = None,
        count: int = 2,
        estimated_weight_g: float = 180.0,
        confidence: float = 0.91
    ) -> Section50BreadSingleAnnotation:
        """
        Generates Section 50 compliant Image Annotation Schema for Single Food.
        """
        return Section50BreadSingleAnnotation(
            food_category=food_category,
            region=region,
            food_name=food_name,
            variant=variant,
            flour=flour,
            cooking_method=cooking_method,
            stuffing=stuffing or ["potato"],
            toppings=toppings or ["butter"],
            count=count,
            estimated_weight_g=round(estimated_weight_g, 1),
            confidence=round(confidence, 2)
        )

    @classmethod
    def generate_section_50_multi_annotation(
        cls,
        foods_spec: Optional[List[Dict[str, Any]]] = None
    ) -> Section50MultiFoodAnnotation:
        """
        Generates Section 50 compliant Multi-Food Annotation Schema.
        """
        if foods_spec is None:
            foods_spec = [
                {"name": "chapati", "count": 3, "estimated_weight_g": 120.0},
                {"name": "dal", "estimated_weight_g": 150.0},
                {"name": "vegetable_curry", "estimated_weight_g": 100.0}
            ]
        items = [
            Section50FoodItem(
                name=f["name"],
                count=f.get("count"),
                estimated_weight_g=float(f["estimated_weight_g"])
            )
            for f in foods_spec
        ]
        return Section50MultiFoodAnnotation(foods=items)

    @classmethod
    def generate_section_51_unknown_fallback(
        cls,
        prediction: str = "Indian flatbread — exact type uncertain",
        fallback_alternative: str = "Bread-like food — insufficient visual evidence",
        confidence: float = 0.38
    ) -> Section51UnknownBreadOutput:
        """
        Generates Section 51 compliant Unknown Bread System Fallback.
        """
        return Section51UnknownBreadOutput(
            status="uncertain",
            food_category="bread",
            prediction=prediction,
            fallback_alternative=fallback_alternative,
            confidence=round(confidence, 2),
            user_confirmation_required=True,
            prompt="Could you specify which Indian bread this is? (e.g. Chapati, Naan, Paratha, Kulcha)"
        )

    @classmethod
    def generate_section_62_final_app_output(
        cls,
        meal_title: str = "Paratha Breakfast Platter",
        paratha_count: int = 2,
        paratha_weight_g: float = 180.0,
        has_curd: bool = True,
        curd_weight_g: float = 100.0,
        has_pickle: bool = True,
        pickle_weight_g: float = 15.0
    ) -> Section62FinalAppOutput:
        """
        Generates Section 62 Final App Output Example:
        - Aloo Paratha (Quantity: 2, Weight: 180g, Calories range, Confidence: High)
        - Curd (Weight: 100g, Calories range, Confidence: Medium)
        - Pickle (Weight: 15g, Calories range, Confidence: Medium)
        - Full editing metadata enabled.
        """
        paratha_calc = cls.calculate_single_dish(
            food_identifier="Aloo Paratha",
            custom_weight_g=paratha_weight_g,
            piece_count=paratha_count
        )
        cals_low = int(round(paratha_calc.calories_low / 10.0) * 10)
        cals_high = int(round(paratha_calc.calories_high / 10.0) * 10)

        items: List[Section62DetectedItem] = [
            Section62DetectedItem(
                food_name="Aloo Paratha",
                quantity=paratha_count,
                estimated_weight_g=round(paratha_weight_g, 1),
                calorie_range_kcal=[cals_low, cals_high],
                protein_range_g=[int(round(paratha_calc.protein_g * 0.85)), int(round(paratha_calc.protein_g * 1.15))],
                carbs_range_g=[int(round(paratha_calc.carbs_g * 0.85)), int(round(paratha_calc.carbs_g * 1.15))],
                fat_range_g=[int(round(paratha_calc.fat_g * 0.85)), int(round(paratha_calc.fat_g * 1.15))],
                confidence="High",
                editable_fields=["food", "quantity", "weight", "recipe", "oil_ghee", "toppings"]
            )
        ]

        total_weight = paratha_weight_g
        tot_cals_min = cals_low
        tot_cals_max = cals_high

        if has_curd:
            items.append(Section62DetectedItem(
                food_name="Curd",
                quantity=1,
                estimated_weight_g=round(curd_weight_g, 1),
                calorie_range_kcal=[60, 80],
                protein_range_g=[3, 5],
                carbs_range_g=[4, 6],
                fat_range_g=[3, 5],
                confidence="Medium",
                editable_fields=["food", "quantity", "weight"]
            ))
            total_weight += curd_weight_g
            tot_cals_min += 60
            tot_cals_max += 80

        if has_pickle:
            items.append(Section62DetectedItem(
                food_name="Pickle",
                quantity=1,
                estimated_weight_g=round(pickle_weight_g, 1),
                calorie_range_kcal=[15, 25],
                protein_range_g=[0, 1],
                carbs_range_g=[1, 3],
                fat_range_g=[1, 2],
                confidence="Medium",
                editable_fields=["food", "quantity", "weight"]
            ))
            total_weight += pickle_weight_g
            tot_cals_min += 15
            tot_cals_max += 25

        return Section62FinalAppOutput(
            meal_title=meal_title,
            detected_foods=items,
            total_estimated_weight_g=round(total_weight, 1),
            total_estimated_calories_range=f"{tot_cals_min}–{tot_cals_max} kcal",
            user_can_edit=True
        )

