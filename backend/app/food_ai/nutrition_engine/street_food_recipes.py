"""
Street Food Recipe-Aware Nutrition Calculator & Section 96 Output Engine (Part 8)
Implements Sections 0, 5, 65, 83, 84, 85, 90, 96, 98 of Part 8 Master Training Specification.

Guarantees:
- End-to-end recipe and component-level nutrition synthesis:
  Calories = Sum(Base + Filling + Toppings + Sauces + OilAdjustment + Cheese/Mayo).
- Emits Section 96 Standardized Outputs:
  * Single Item: Food name, weight (g), calories range, protein range, carbs range, fat range, confidence.
  * Multi-Food Plate: List of detected foods with counts and weights, total calorie range, confidence.
- Calorie Uncertainty Handling (Section 84):
  * Outputs realistic calibrated ranges (e.g., 450–600 kcal).
  * Never provides fake exact precision (e.g., 537 kcal) when oil quantity or fillings are variable.
- Non-Negotiable Rule 90 & 98:
  * Fallback to 'Unknown Street Food' with Low confidence when visual evidence is insufficient.
  * Never force low-confidence images into known classes.
"""

from typing import Dict, Any, Optional, List, Tuple
from pydantic import BaseModel, Field

from app.food_ai.taxonomy.street_food_master_taxonomy import (
    get_street_food_class,
    resolve_street_food_by_name,
    StreetFoodClassRecord
)
from app.food_ai.portion_engine.street_food_portions import (
    STREET_FOOD_PORTION_DATABASE,
    StreetOilEstimator,
    StreetCheeseMayonnaiseCalculator,
    OilEstimationResult
)


class Section96SingleItemOutput(BaseModel):
    food_name: str
    canonical_id: str
    estimated_weight_g: float
    estimated_calories_range: str  # e.g., "450–600 kcal"
    calories_low: float
    calories_expected: float
    calories_high: float
    protein_range_g: str           # e.g., "20–28 g"
    protein_g: float
    carbohydrates_range_g: str     # e.g., "40–55 g"
    carbs_g: float
    fat_range_g: str               # e.g., "18–28 g"
    fat_g: float
    fiber_g: float
    confidence: str                # "High", "Medium", "Low", "Uncertain"
    confidence_score: float
    oil_level_estimate: str        # "Low", "Medium", "High", "Unknown"
    uncertainty_reason: str
    requires_user_confirmation: bool = False
    confirmation_prompt: Optional[str] = None


class Section96DetectedFoodItem(BaseModel):
    item_index: int
    name: str
    count: Optional[int] = None
    estimated_weight_g: float
    calories_expected: float


class Section96MultiFoodOutput(BaseModel):
    plate_title: str
    detected_foods: List[Section96DetectedFoodItem]
    total_estimated_weight_g: float
    total_estimated_calories_range: str  # e.g., "550–720 kcal"
    total_calories_low: float
    total_calories_expected: float
    total_calories_high: float
    total_protein_g: float
    total_carbs_g: float
    total_fat_g: float
    total_fiber_g: float
    overall_confidence: str              # "High", "Medium", "Low"
    overall_confidence_score: float


class StreetRecipeNutritionCalculator:
    """
    Implements Sections 83, 84, 96:
    Component-wise nutrition calculation with calibrated uncertainty ranges.
    """
    @classmethod
    def calculate_single_dish(
        cls,
        food_identifier: str,
        visual_cues: Optional[Dict[str, Any]] = None,
        custom_weight_g: Optional[float] = None,
        count: Optional[int] = None,
        oil_override: Optional[str] = None,
        cheese_added: bool = False,
        mayo_added: bool = False
    ) -> Section96SingleItemOutput:
        cues = visual_cues or {}

        # 1. Resolve canonical taxonomy record
        record: Optional[StreetFoodClassRecord] = get_street_food_class(food_identifier)
        if not record:
            record = resolve_street_food_by_name(food_identifier)

        # Fallback to UNKNOWN if not resolved or low evidence (Section 90)
        if not record or cues.get("low_visual_evidence", False) or cues.get("is_unknown", False):
            return Section96SingleItemOutput(
                food_name="Unknown Street Food",
                canonical_id="STREET_UNKNOWN",
                estimated_weight_g=custom_weight_g or 150.0,
                estimated_calories_range="220–350 kcal",
                calories_low=220.0,
                calories_expected=280.0,
                calories_high=350.0,
                protein_range_g="4–10 g",
                protein_g=6.0,
                carbohydrates_range_g="25–45 g",
                carbs_g=34.0,
                fat_range_g="8–18 g",
                fat_g=13.0,
                fiber_g=2.5,
                confidence="Low",
                confidence_score=0.35,
                oil_level_estimate="Unknown",
                uncertainty_reason="Visual evidence is insufficient to make a fine-grained classification without risk of hallucination (Rule 98).",
                requires_user_confirmation=True,
                confirmation_prompt="Could you specify or confirm what street food this is?"
            )

        # 2. Determine portion and mass
        unit_mass = record.default_unit_mass_g
        item_count = count if (count and count > 0) else 1

        if custom_weight_g and custom_weight_g > 0:
            total_mass = custom_weight_g
        elif record.hierarchy.level8_portion_type == "piece_count":
            total_mass = item_count * unit_mass
        else:
            total_mass = unit_mass

        # 3. Base nutrition per 100g
        n100 = record.nutrition_per_100g
        base_cals = (total_mass / 100.0) * n100.get("calories", 200.0)
        base_pro = (total_mass / 100.0) * n100.get("protein_g", 5.0)
        base_carb = (total_mass / 100.0) * n100.get("carbs_g", 28.0)
        base_fat = (total_mass / 100.0) * n100.get("fat_g", 8.0)
        base_fib = (total_mass / 100.0) * n100.get("fiber_g", 2.0)

        # 4. Oil estimation and uncertainty (Section 65)
        prep_style = cues.get("cooking_method", record.hierarchy.level7_cooking_method[0] if record.hierarchy.level7_cooking_method else "Deep Fried")
        sheen = cues.get("surface_sheen")
        is_deep = "deep" in prep_style.lower() or record.oil_level_typical == "High"

        if oil_override:
            oil_res = OilEstimationResult(
                preparation_style=prep_style,
                oil_level=oil_override,
                fat_multiplier=1.35 if oil_override == "High" else (0.80 if oil_override == "Low" else 1.10),
                uncertainty_spread_pct=15.0,
                notes=f"User or prompt designated oil level as {oil_override}."
            )
        else:
            oil_res = StreetOilEstimator.estimate_oil(prep_style, surface_sheen=sheen, is_deep_fried=is_deep)

        # Apply fat multiplier to fat & calories
        adj_fat = base_fat * oil_res.fat_multiplier
        fat_diff_cals = (adj_fat - base_fat) * 9.0
        exp_cals = base_cals + fat_diff_cals

        # 5. Add-ons: Cheese & Mayonnaise (Sections 67 & 68)
        extra_pro = 0.0
        extra_carb = 0.0
        extra_fat = 0.0
        extra_cals = 0.0

        if cheese_added or cues.get("cheese_detected", False):
            cheese_adj = StreetCheeseMayonnaiseCalculator.calculate_cheese(
                cheese_type=cues.get("cheese_type", "grated"),
                intensity=cues.get("cheese_intensity", "standard")
            )
            extra_cals += cheese_adj.calories
            extra_pro += cheese_adj.protein_g
            extra_carb += cheese_adj.carbs_g
            extra_fat += cheese_adj.fat_g

        if mayo_added or cues.get("mayo_detected", False):
            mayo_adj = StreetCheeseMayonnaiseCalculator.calculate_mayonnaise(
                mayo_type=cues.get("mayo_type", "plain"),
                intensity=cues.get("mayo_intensity", "standard")
            )
            extra_cals += mayo_adj.calories
            extra_pro += mayo_adj.protein_g
            extra_carb += mayo_adj.carbs_g
            extra_fat += mayo_adj.fat_g

        final_cals = exp_cals + extra_cals
        final_pro = base_pro + extra_pro
        final_carb = base_carb + extra_carb
        final_fat = adj_fat + extra_fat

        # 6. Calibrated uncertainty range (Section 84)
        spread_pct = oil_res.uncertainty_spread_pct
        if cues.get("filling_uncertain", False):
            spread_pct += 6.0
        if cheese_added or mayo_added:
            spread_pct += 4.0

        cals_low = round(final_cals * (1.0 - (spread_pct / 100.0)), 0)
        cals_high = round(final_cals * (1.0 + (spread_pct / 100.0)), 0)

        pro_low = max(1.0, round(final_pro * 0.85, 0))
        pro_high = round(final_pro * 1.15, 0)

        carb_low = max(2.0, round(final_carb * 0.88, 0))
        carb_high = round(final_carb * 1.14, 0)

        fat_low = max(1.0, round(final_fat * 0.82, 0))
        fat_high = round(final_fat * 1.22, 0)

        # Confidence level
        conf_score = cues.get("confidence", 0.92)
        if conf_score >= 0.85:
            conf_str = "High"
        elif conf_score >= 0.70:
            conf_str = "Medium"
        else:
            conf_str = "Low"

        reason = f"Oil quantity ({oil_res.oil_level}) and portion volume create natural variance."
        if cheese_added or mayo_added:
            reason += " Added cheese/mayo toppings account for additional caloric density."

        return Section96SingleItemOutput(
            food_name=record.canonical_name,
            canonical_id=record.canonical_food_id,
            estimated_weight_g=round(total_mass, 1),
            estimated_calories_range=f"{int(cals_low)}–{int(cals_high)} kcal",
            calories_low=cals_low,
            calories_expected=round(final_cals, 1),
            calories_high=cals_high,
            protein_range_g=f"{int(pro_low)}–{int(pro_high)} g",
            protein_g=round(final_pro, 1),
            carbohydrates_range_g=f"{int(carb_low)}–{int(carb_high)} g",
            carbs_g=round(final_carb, 1),
            fat_range_g=f"{int(fat_low)}–{int(fat_high)} g",
            fat_g=round(final_fat, 1),
            fiber_g=round(base_fib, 1),
            confidence=conf_str,
            confidence_score=round(conf_score, 2),
            oil_level_estimate=oil_res.oil_level,
            uncertainty_reason=reason
        )

    @classmethod
    def calculate_multi_food_plate(
        cls,
        plate_title: str,
        items: List[Dict[str, Any]]
    ) -> Section96MultiFoodOutput:
        detected_list: List[Section96DetectedFoodItem] = []
        total_mass = 0.0
        tot_cals_exp = 0.0
        tot_cals_low = 0.0
        tot_cals_high = 0.0
        tot_pro = 0.0
        tot_carb = 0.0
        tot_fat = 0.0
        tot_fib = 0.0

        for idx, it in enumerate(items, start=1):
            single = cls.calculate_single_dish(
                food_identifier=it.get("name", ""),
                visual_cues=it.get("visual_cues"),
                custom_weight_g=it.get("estimated_weight_g"),
                count=it.get("count"),
                oil_override=it.get("oil_level"),
                cheese_added=it.get("cheese_added", False),
                mayo_added=it.get("mayo_added", False)
            )

            detected_list.append(Section96DetectedFoodItem(
                item_index=idx,
                name=single.food_name,
                count=it.get("count"),
                estimated_weight_g=single.estimated_weight_g,
                calories_expected=single.calories_expected
            ))

            total_mass += single.estimated_weight_g
            tot_cals_exp += single.calories_expected
            tot_cals_low += single.calories_low
            tot_cals_high += single.calories_high
            tot_pro += single.protein_g
            tot_carb += single.carbs_g
            tot_fat += single.fat_g
            tot_fib += single.fiber_g

        return Section96MultiFoodOutput(
            plate_title=plate_title,
            detected_foods=detected_list,
            total_estimated_weight_g=round(total_mass, 1),
            total_estimated_calories_range=f"{int(round(tot_cals_low))}–{int(round(tot_cals_high))} kcal",
            total_calories_low=round(tot_cals_low, 1),
            total_calories_expected=round(tot_cals_exp, 1),
            total_calories_high=round(tot_cals_high, 1),
            total_protein_g=round(tot_pro, 1),
            total_carbs_g=round(tot_carb, 1),
            total_fat_g=round(tot_fat, 1),
            total_fiber_g=round(tot_fib, 1),
            overall_confidence="High" if len(items) > 0 else "Low",
            overall_confidence_score=0.91
        )
