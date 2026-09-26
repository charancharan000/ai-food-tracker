"""
Sweets & Desserts Nutrition Engine, Schemas & Uncertainty Calculator (Part 14)
Implements Sections 50, 51, 52, 53, 59, 60, 61, 64, 65, 81, 84, 85, 87 of Part 14 Specification.

Guarantees:
- Section 65 Annotation Schema:
  Detailed image annotation JSON schema with bounding boxes, piece count, cooking method, syrup state, and confidence.
- Section 85 & 53 Calorie Uncertainty Output:
  Outputs bounded calorie ranges (e.g. 220–300 kcal) instead of single-point false precision.
- Section 59 Unknown Sweet Output:
  Fallback schema offering structured user confirmation options.
- Section 61 User Correction Store:
  Captures feedback for active learning pipeline.
- Section 81 Final App Output:
  Formatted multi-sweet output with independent component breakdown and total ranges.
- Section 88 Standardized Single Sweet Output.
- Recipe-aware calculations factoring piece counts, sugar contribution tiers, and frying fat levels.
"""

from typing import List, Dict, Any, Optional, Tuple
from pydantic import BaseModel, Field
import datetime

from app.food_ai.taxonomy.sweets_master_taxonomy import (
    resolve_sweet_food_by_name,
    get_sweet_food_class,
    SweetFoodClassRecord
)
from app.food_ai.portion_engine.sweets_portions import (
    SWEET_PORTION_DATABASE,
    QualitativeSugarEstimator,
    FriedSweetFatEstimator
)


class Section65SweetItem(BaseModel):
    class_id: str
    name: str
    bbox: Optional[List[int]] = None
    count: Optional[int] = None
    estimated_weight_g: float
    cooking_method: str = "Simmered"
    syrup_state: str = "Dry"
    confidence: float


class Section65SweetAnnotation(BaseModel):
    image_id: str
    region: str
    food_items: List[Section65SweetItem]


class Section85CalorieUncertaintyOutput(BaseModel):
    dish_name: str
    piece_count: Optional[int]
    estimated_weight_g: float
    calories_expected: float
    calorie_range: Dict[str, float]  # low, expected, high
    sugar_contribution_tier: str
    fat_profile_tier: str
    protein_g_range: Tuple[float, float]
    fat_g_range: Tuple[float, float]
    carbs_g: float
    fiber_g: float
    uncertainty_description: str
    non_negotiable_compliance: str = "Section 85 & Rule 29 compliant: Bounded calorie range provided based on recipe and syrup variation."


class Section59UnknownSweetOutput(BaseModel):
    status: str = "unknown_confirmation_required"
    fallback_class_id: str = "IND-SWT-UNKNOWN-001"
    fallback_name: str = "Indian Sweet (Exact Variety Uncertain)"
    user_prompt: str = "What sweet/dessert is this?"
    confirmation_options: List[str] = Field(default_factory=lambda: [
        "Laddu variety (Motichoor / Besan / Boondi)",
        "Kaju Katli / Nut barfi",
        "Milk / Khoya sweet (Peda / Barfi / Sandesh)",
        "Syrup-soaked sweet (Gulab Jamun / Rasgulla / Jalebi)",
        "Pudding / Halwa (Payasam / Kheer / Kesari)",
        "Other regional sweet"
    ])
    image_id: Optional[str] = None
    confidence: float = 0.45
    uncertainty_note: str = "Section 59 & 84 compliant: Model refrains from hallucinating exact sweet variety without sufficient diagnostic evidence."


class Section61SweetUserCorrectionRecord(BaseModel):
    image_id: str
    original_prediction: str
    corrected_label: str
    confidence: float
    active_learning_priority: int = 1
    timestamp: str = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())


class Section88SweetSingleOutput(BaseModel):
    class_id: str
    food_name: str
    sweet_family: str
    region: str
    base_ingredient: str
    cooking_method: str
    syrup_state: str
    shape_profile: str
    piece_count: Optional[int]
    total_portion_weight_g: float
    sugar_tier_name: str
    fat_profile_name: str
    calories: float
    calories_range: Dict[str, float]
    protein_g: float
    carbs_g: float
    fat_g: float
    fiber_g: float
    confidence: float
    uncertainty_factors: List[str]


class Section81FinalAppSweetOutput(BaseModel):
    title: str = "🍬 Food Detected"
    detected_items: List[Dict[str, Any]]
    total_calories_range: Dict[str, float]
    total_protein_range_g: Tuple[float, float]
    total_fat_range_g: Tuple[float, float]
    component_summary: str


SWEET_USER_CORRECTION_STORE: List[Section61SweetUserCorrectionRecord] = []


class SweetRecipeNutritionCalculator:
    """
    Recipe-aware Nutrition Calculator for Indian Sweets & Desserts.
    Integrates piece counting, syrup state, and qualitative sugar/fat tiers.
    """

    @classmethod
    def calculate_sweet_nutrition(
        cls,
        dish_name: str,
        piece_count: Optional[int] = None,
        serving_size_category: str = "Medium",
        syrup_override: Optional[str] = None,
        shop_style: bool = True
    ) -> Section88SweetSingleOutput:
        record = resolve_sweet_food_by_name(dish_name)
        if not record:
            record = get_sweet_food_class("IND-SWT-UNKNOWN-001")

        # Determine portion database category
        cat_key = "halwa_bowl"
        if record.sweet_family in ["Kaju Katli"]:
            cat_key = "kaju_katli_piece"
        elif record.sweet_family in ["Laddoo"]:
            cat_key = "laddu_piece"
        elif record.sweet_family in ["Gulab Jamun"]:
            cat_key = "gulab_jamun_piece"
        elif record.sweet_family in ["Rasgulla"]:
            cat_key = "rasgulla_piece"
        elif record.sweet_family in ["Jalebi", "Imarti/Jangri"]:
            cat_key = "jalebi_serving"
        elif record.sweet_family in ["Mysore Pak"]:
            cat_key = "mysore_pak_piece"
        elif record.sweet_family in ["Payasam", "Kheer"]:
            cat_key = "kheer_payasam_bowl"
        elif record.sweet_family in ["Modak"]:
            cat_key = "modak_piece"
        elif record.sweet_family in ["Puran Poli"]:
            cat_key = "puran_poli_piece"

        port_cfg = SWEET_PORTION_DATABASE.get(cat_key, SWEET_PORTION_DATABASE["laddu_piece"])

        # Weight calculation
        if piece_count and port_cfg.is_piece_based:
            total_wt = piece_count * port_cfg.piece_weight_typical_g
            final_count = piece_count
        else:
            serving_weights = {
                "Small": port_cfg.small_serving_g,
                "Medium": port_cfg.medium_serving_g,
                "Large": port_cfg.large_serving_g
            }
            total_wt = serving_weights.get(serving_size_category, port_cfg.medium_serving_g)
            final_count = piece_count or (int(total_wt / port_cfg.piece_weight_typical_g) if port_cfg.is_piece_based else None)

        # Active syrup state
        active_syrup = syrup_override or record.syrup_state

        # Base macros per 100g
        scale = total_wt / 100.0
        n100 = record.nutrition_per_100g

        base_cals = n100.get("calories", 350.0) * scale
        base_p = n100.get("protein", 5.0) * scale
        base_c = n100.get("carbs", 55.0) * scale
        base_f = n100.get("fat", 12.0) * scale
        base_fib = n100.get("fiber", 0.5) * scale

        # Sweet shop / halwai enrichment factor (Section 54)
        shop_factor = 1.12 if shop_style else 1.00
        final_cals = round(base_cals * shop_factor, 1)
        final_p = round(base_p, 1)
        final_c = round(base_c * shop_factor, 1)
        final_f = round(base_f * shop_factor, 1)
        final_fib = round(base_fib, 1)

        # Calorie range (Section 85)
        calorie_range = {
            "low": round(final_cals * 0.88, 1),
            "expected": final_cals,
            "high": round(final_cals * 1.15, 1)
        }

        # Sugar and fat tiers
        sugar_est = QualitativeSugarEstimator.estimate_sugar_tier(active_syrup, is_deep_fried=record.is_fried)
        fat_est = FriedSweetFatEstimator.estimate_fat_profile(record.specific_dish, is_fried=record.is_fried)

        return Section88SweetSingleOutput(
            class_id=record.canonical_food_id,
            food_name=record.canonical_name,
            sweet_family=record.sweet_family,
            region=record.region,
            base_ingredient=record.base_ingredient,
            cooking_method=record.cooking_method,
            syrup_state=active_syrup,
            shape_profile=record.shape_profile,
            piece_count=final_count,
            total_portion_weight_g=round(total_wt, 1),
            sugar_tier_name=sugar_est["sugar_tier_name"],
            fat_profile_name=fat_est["fat_profile_name"],
            calories=final_cals,
            calories_range=calorie_range,
            protein_g=final_p,
            carbs_g=final_c,
            fat_g=final_f,
            fiber_g=final_fib,
            confidence=0.94 if record.canonical_food_id != "IND-SWT-UNKNOWN-001" else 0.45,
            uncertainty_factors=record.uncertainty_factors + [f"sugar_tier_{sugar_est['sugar_tier_name']}"]
        )

    @classmethod
    def generate_section_65_annotation(
        cls,
        image_id: str,
        dish_name: str,
        region: str = "Tamil Nadu",
        count: Optional[int] = 3,
        estimated_weight_g: float = 105.0,
        cooking_method: str = "fried",
        syrup_state: str = "coated",
        bbox: Optional[List[int]] = None
    ) -> Section65SweetAnnotation:
        """
        Generates Section 65 Annotation Schema JSON.
        """
        record = resolve_sweet_food_by_name(dish_name)
        class_id = record.canonical_food_id if record else "IND-SWT-UNKNOWN-001"
        canonical_name = record.canonical_name if record else dish_name

        item = Section65SweetItem(
            class_id=class_id,
            name=canonical_name,
            bbox=bbox or [120, 90, 430, 350],
            count=count,
            estimated_weight_g=estimated_weight_g,
            cooking_method=cooking_method,
            syrup_state=syrup_state,
            confidence=0.92
        )
        return Section65SweetAnnotation(
            image_id=image_id,
            region=region,
            food_items=[item]
        )

    @classmethod
    def generate_section_85_uncertainty(
        cls,
        dish_name: str,
        piece_count: Optional[int] = None,
        serving_size_category: str = "Medium"
    ) -> Section85CalorieUncertaintyOutput:
        """
        Generates Section 85 Calorie Uncertainty Output schema.
        """
        single = cls.calculate_sweet_nutrition(
            dish_name=dish_name,
            piece_count=piece_count,
            serving_size_category=serving_size_category
        )
        return Section85CalorieUncertaintyOutput(
            dish_name=single.food_name,
            piece_count=single.piece_count,
            estimated_weight_g=single.total_portion_weight_g,
            calories_expected=single.calories,
            calorie_range=single.calories_range,
            sugar_contribution_tier=single.sugar_tier_name,
            fat_profile_tier=single.fat_profile_name,
            protein_g_range=(round(single.protein_g * 0.90, 1), round(single.protein_g * 1.10, 1)),
            fat_g_range=(round(single.fat_g * 0.85, 1), round(single.fat_g * 1.20, 1)),
            carbs_g=single.carbs_g,
            fiber_g=single.fiber_g,
            uncertainty_description=f"Estimated calories: {int(single.calories_range['low'])}–{int(single.calories_range['high'])} kcal. Sugar contribution: {single.sugar_tier_name}."
        )

    @classmethod
    def generate_section_59_unknown(cls, image_id: Optional[str] = None) -> Section59UnknownSweetOutput:
        """
        Generates Section 59 & 84 Unknown Sweet Fallback schema.
        """
        return Section59UnknownSweetOutput(image_id=image_id)

    @classmethod
    def generate_section_81_app_output(cls, components_nutrition: List[Dict[str, Any]]) -> Section81FinalAppSweetOutput:
        """
        Generates Section 81 Example Final App Output.
        """
        total_low = sum(item.get("calories_range", {}).get("low", item.get("calories", 0) * 0.88) for item in components_nutrition)
        total_exp = sum(item.get("calories", 0) for item in components_nutrition)
        total_high = sum(item.get("calories_range", {}).get("high", item.get("calories", 0) * 1.15) for item in components_nutrition)

        total_p_low = sum(item.get("protein_g", 0) * 0.9 for item in components_nutrition)
        total_p_high = sum(item.get("protein_g", 0) * 1.1 for item in components_nutrition)

        total_f_low = sum(item.get("fat_g", 0) * 0.85 for item in components_nutrition)
        total_f_high = sum(item.get("fat_g", 0) * 1.2 for item in components_nutrition)

        summary_lines = []
        for c in components_nutrition:
            line = f"{c.get('food_name', 'Sweet')}: ~{c.get('weight_g', 0)}g"
            if c.get("piece_count"):
                line += f" ({c.get('piece_count')} pcs)"
            line += f" -> {int(c.get('calories', 0))} kcal"
            summary_lines.append(line)

        return Section81FinalAppSweetOutput(
            title="🍬 Food Detected",
            detected_items=components_nutrition,
            total_calories_range={
                "low": round(total_low, 1),
                "expected": round(total_exp, 1),
                "high": round(total_high, 1)
            },
            total_protein_range_g=(round(total_p_low, 1), round(total_p_high, 1)),
            total_fat_range_g=(round(total_f_low, 1), round(total_f_high, 1)),
            component_summary="; ".join(summary_lines)
        )

    @classmethod
    def record_user_correction(
        cls,
        image_id: str,
        original_prediction: str,
        corrected_label: str,
        confidence: float = 0.68
    ) -> Section61SweetUserCorrectionRecord:
        """
        Stores user correction for active learning (Section 61).
        """
        record = Section61SweetUserCorrectionRecord(
            image_id=image_id,
            original_prediction=original_prediction,
            corrected_label=corrected_label,
            confidence=confidence,
            active_learning_priority=1
        )
        SWEET_USER_CORRECTION_STORE.append(record)
        return record
