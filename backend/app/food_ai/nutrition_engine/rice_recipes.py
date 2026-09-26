"""
Rice & Biryani Recipe Nutrition Engine & Section 78 Output Engine (Part 9)
Implements Sections 62, 63, 64, 65, 78, 80 of Part 9 Master Training Specification.

Guarantees:
- End-to-end recipe synthesis:
  Calories = RiceBase + MeatProtein + GheeOilAdjustment + BiristaGarnish + Nuts/DriedFruits.
- Section 78 Standardized Single Dish & Composite Output Schemas:
  * Single Dish: Food name, portion (g), calories range (e.g. 700–850 kcal), protein range, carbs range, fat range, confidence.
  * Composite Plate: Itemized constituent list with independent weights and calories, plus aggregated range.
- Section 65 & 80 Non-Negotiable Rules:
  * Calibrated ranges instead of false precision (never 731 kcal).
  * Never classifies every mixed rice as biryani or every yellow rice as lemon rice.
  * Fallback to 'Unknown Rice Dish' with Low confidence when visual evidence is insufficient.
"""

from typing import Dict, Any, Optional, List, Tuple
from pydantic import BaseModel, Field

from app.food_ai.taxonomy.rice_master_taxonomy import (
    get_rice_food_class,
    resolve_rice_food_by_name,
    RiceFoodClassRecord
)
from app.food_ai.portion_engine.rice_portions import (
    RICE_PORTION_DATABASE,
    RiceToMeatRatioEstimator,
    RiceOilGheeEstimator,
    RiceGarnishCalculator,
    RiceFatEstimationResult
)


class Section78RiceSingleOutput(BaseModel):
    food_name: str
    canonical_id: str
    regional_style: str
    estimated_portion_g: float
    estimated_calories_range: str  # e.g., "700–850 kcal"
    calories_low: float
    calories_expected: float
    calories_high: float
    protein_range_g: str           # e.g., "30–40 g"
    protein_g: float
    carbohydrates_range_g: str     # e.g., "80–100 g"
    carbs_g: float
    fat_range_g: str               # e.g., "25–35 g"
    fat_g: float
    fiber_g: float
    confidence: str                # "High", "Medium", "Low"
    confidence_score: float
    fat_level_estimate: str        # "Low", "Medium", "High", "Unknown"
    uncertainty_reason: str
    requires_user_confirmation: bool = False
    confirmation_prompt: Optional[str] = None


class Section78DetectedRiceItem(BaseModel):
    item_index: int
    name: str
    count: Optional[int] = None
    estimated_weight_g: float
    calories_expected: float


class Section78RiceMultiOutput(BaseModel):
    plate_title: str
    detected_items: List[Section78DetectedRiceItem]
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


class RiceRecipeNutritionCalculator:
    """
    Implements Sections 64, 65, 78:
    Calculates component-wise nutrition with calibrated uncertainty ranges.
    """
    @classmethod
    def calculate_single_dish(
        cls,
        food_identifier: str,
        visual_cues: Optional[Dict[str, Any]] = None,
        custom_weight_g: Optional[float] = None,
        portion_size: Optional[str] = None,  # "Small", "Medium", "Large", "Extra Large"
        visible_meat_pieces: Optional[int] = None,
        ghee_override: Optional[str] = None,
        has_extra_birista: bool = False,
        has_cashews_raisins: bool = False
    ) -> Section78RiceSingleOutput:
        cues = visual_cues or {}

        # 1. Resolve canonical record
        record: Optional[RiceFoodClassRecord] = get_rice_food_class(food_identifier)
        if not record:
            record = resolve_rice_food_by_name(food_identifier)

        # Fallback to UNKNOWN if not resolved or low evidence (Section 80)
        if not record or cues.get("low_visual_evidence", False) or cues.get("is_unknown", False):
            return Section78RiceSingleOutput(
                food_name="Unknown Rice Dish",
                canonical_id="RICE_UNKNOWN",
                regional_style="Unknown",
                estimated_portion_g=custom_weight_g or 300.0,
                estimated_calories_range="380–520 kcal",
                calories_low=380.0,
                calories_expected=450.0,
                calories_high=520.0,
                protein_range_g="6–14 g",
                protein_g=10.0,
                carbohydrates_range_g="60–85 g",
                carbs_g=72.0,
                fat_range_g="8–18 g",
                fat_g=13.0,
                fiber_g=2.0,
                confidence="Low",
                confidence_score=0.38,
                fat_level_estimate="Unknown",
                uncertainty_reason="Visual evidence is insufficient to verify specific regional rice preparation without risking hallucination (Rule 80).",
                requires_user_confirmation=True,
                confirmation_prompt="Could you specify which rice dish this is? (e.g., Chicken Biryani, Veg Pulao, Curd Rice)"
            )

        # 2. Determine portion grams
        if custom_weight_g and custom_weight_g > 0:
            total_mass = custom_weight_g
        elif portion_size and record.rice_family.lower() in RICE_PORTION_DATABASE:
            cfg = RICE_PORTION_DATABASE[record.rice_family.lower()]
            ps = portion_size.lower()
            if "small" in ps:
                total_mass = cfg.small.typical_grams
            elif "large" in ps:
                total_mass = cfg.large.typical_grams
            elif "extra" in ps:
                total_mass = cfg.extra_large.typical_grams
            else:
                total_mass = cfg.medium.typical_grams
        else:
            total_mass = record.default_portion_grams

        # 3. Rice-to-Meat Ratio Split (Section 46)
        is_biryani = "biryani" in record.rice_family.lower()
        if is_biryani and record.protein_type in ("chicken", "mutton", "prawn"):
            split = RiceToMeatRatioEstimator.estimate_split(
                total_mass_g=total_mass,
                protein_type=record.protein_type,
                visible_meat_pieces=visible_meat_pieces
            )
            rice_g = split.rice_mass_g
            meat_g = split.meat_mass_g
        else:
            rice_g = total_mass
            meat_g = 0.0

        # Base nutrition per 100g
        n100 = record.nutrition_per_100g
        base_cals = (total_mass / 100.0) * n100.get("calories", 180.0)
        base_pro = (total_mass / 100.0) * n100.get("protein_g", 8.0)
        base_carb = (total_mass / 100.0) * n100.get("carbs_g", 23.0)
        base_fat = (total_mass / 100.0) * n100.get("fat_g", 6.0)
        base_fib = (total_mass / 100.0) * n100.get("fiber_g", 1.2)

        # 4. Ghee & Oil Estimator (Section 47)
        sheen = cues.get("surface_sheen")
        has_b = has_extra_birista or cues.get("has_birista", False)

        if ghee_override:
            fat_res = RiceFatEstimationResult(
                fat_level=ghee_override,
                fat_multiplier=1.30 if ghee_override == "High" else (0.85 if ghee_override == "Low" else 1.10),
                uncertainty_spread_pct=15.0,
                notes=f"Fat level set to {ghee_override}."
            )
        else:
            fat_res = RiceOilGheeEstimator.estimate_fat(
                dish_family=record.rice_family,
                surface_sheen=sheen,
                has_birista=has_b
            )

        adj_fat = base_fat * fat_res.fat_multiplier
        fat_diff_cals = (adj_fat - base_fat) * 9.0
        exp_cals = base_cals + fat_diff_cals

        # 5. Garnishes: Birista & Nuts/Raisins
        extra_cals = 0.0
        extra_pro = 0.0
        extra_carb = 0.0
        extra_fat = 0.0

        if has_extra_birista:
            bg = RiceGarnishCalculator.calculate_birista()
            extra_cals += bg.calories
            extra_pro += bg.protein_g
            extra_carb += bg.carbs_g
            extra_fat += bg.fat_g

        if has_cashews_raisins or "thalassery" in record.regional_style.lower() or "kashmiri" in record.canonical_name.lower():
            ng = RiceGarnishCalculator.calculate_nuts_and_raisins()
            extra_cals += ng.calories
            extra_pro += ng.protein_g
            extra_carb += ng.carbs_g
            extra_fat += ng.fat_g

        final_cals = exp_cals + extra_cals
        final_pro = base_pro + extra_pro
        final_carb = base_carb + extra_carb
        final_fat = adj_fat + extra_fat

        # 6. Calibrated Uncertainty Range (Section 65 & 78)
        spread = fat_res.uncertainty_spread_pct
        if meat_g > 0 and visible_meat_pieces is None:
            spread += 4.0

        cals_low = round(final_cals * (1.0 - (spread / 100.0)), 0)
        cals_high = round(final_cals * (1.0 + (spread / 100.0)), 0)

        pro_low = max(2.0, round(final_pro * 0.85, 0))
        pro_high = round(final_pro * 1.15, 0)

        carb_low = max(5.0, round(final_carb * 0.88, 0))
        carb_high = round(final_carb * 1.14, 0)

        fat_low = max(1.0, round(final_fat * 0.82, 0))
        fat_high = round(final_fat * 1.22, 0)

        conf_score = cues.get("confidence", 0.93)
        conf_str = "High" if conf_score >= 0.85 else ("Medium" if conf_score >= 0.70 else "Low")

        reason = f"Ghee/oil level ({fat_res.fat_level}) and rice-to-protein ratio introduce natural variance."
        if has_cashews_raisins:
            reason += " Fried cashews and raisins add localized caloric density."

        return Section78RiceSingleOutput(
            food_name=record.canonical_name,
            canonical_id=record.canonical_food_id,
            regional_style=record.regional_style,
            estimated_portion_g=round(total_mass, 1),
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
            fat_level_estimate=fat_res.fat_level,
            uncertainty_reason=reason
        )

    @classmethod
    def calculate_composite_plate(
        cls,
        plate_title: str,
        items: List[Dict[str, Any]]
    ) -> Section78RiceMultiOutput:
        detected_list: List[Section78DetectedRiceItem] = []
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
                portion_size=it.get("portion_size"),
                visible_meat_pieces=it.get("meat_pieces"),
                ghee_override=it.get("ghee_level")
            )

            detected_list.append(Section78DetectedRiceItem(
                item_index=idx,
                name=single.food_name,
                count=it.get("count"),
                estimated_weight_g=single.estimated_portion_g,
                calories_expected=single.calories_expected
            ))

            total_mass += single.estimated_portion_g
            tot_cals_exp += single.calories_expected
            tot_cals_low += single.calories_low
            tot_cals_high += single.calories_high
            tot_pro += single.protein_g
            tot_carb += single.carbs_g
            tot_fat += single.fat_g
            tot_fib += single.fiber_g

        return Section78RiceMultiOutput(
            plate_title=plate_title,
            detected_items=detected_list,
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
            overall_confidence_score=0.93
        )
