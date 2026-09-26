"""
Indian Snacks & Tiffin Recipe-Aware Nutrition Engine & Calorie Pipeline (Part 15)
Implements Sections 42, 43, 44, 51, 52, 53, 63, 64 of Part 15 Specification.

Features:
- Section 63 Dataset Annotation Schema (Standardized training annotation).
- Section 64 Multi-Food JSON Schema (Separate component instance detection).
- Section 51 Unknown Fallback System (Calibrated uncertain fallbacks with user question prompts).
- Section 53 User Correction Store (Audit trail of user overrides for active learning).
- Section 43 Calorie Estimation Pipeline with Recipe Variation factors (frying absorption, ghee brushing, accompaniments).
"""

from typing import Dict, Any, List, Optional, Tuple
from pydantic import BaseModel, Field
import datetime

from app.food_ai.taxonomy.snacks_tiffin_master_taxonomy import (
    SNACKS_TAXONOMY_REGISTRY,
    get_snack_record_by_id,
    resolve_snack_alias,
)


class Section63SnackAnnotation(BaseModel):
    """Dataset Annotation Schema per Section 63."""
    image_id: str
    region: str
    state: str
    food_category: str = "Snack"
    food_family: str
    canonical_name: str
    aliases: List[str] = Field(default_factory=list)
    variant: str
    main_ingredient: str
    cooking_method: str
    count: Optional[int] = None
    estimated_weight_g: float
    portion_confidence: float = 0.85
    food_confidence: float = 0.95
    components: List[Dict[str, Any]] = Field(default_factory=list)
    accompaniments: List[str] = Field(default_factory=list)
    image_quality: str = "good_quality" # sharp, slightly_blurry, blurry, dark, good_quality
    user_verified: bool = True


class Section64MultiFoodItem(BaseModel):
    """Single food item within Section 64 Multi-Food JSON schema."""
    name: str
    canonical_id: Optional[str] = None
    count: Optional[int] = None
    estimated_weight_g: float
    calories: Optional[float] = None
    protein_g: Optional[float] = None
    carbs_g: Optional[float] = None
    fat_g: Optional[float] = None
    fiber_g: Optional[float] = None


class Section64MultiFoodOutput(BaseModel):
    """Multi-Food JSON container conforming directly to Section 64."""
    foods: List[Section64MultiFoodItem]
    total_estimated_weight_g: float
    total_calories: float
    zero_monolithic_guarantee: bool = True


class Section51UnknownSnackFallback(BaseModel):
    """Fallback schema per Section 51 when confidence is below threshold."""
    is_uncertain: bool = True
    uncertain_label: str # e.g. "Indian fried snack — exact type uncertain"
    fallback_class_id: str # e.g. "IND-SNK-FRIED-UNKNOWN-001"
    confidence: float
    candidate_options: List[str]
    prompt_question: str = "Can you select the food from these options?"


class Section53SnackUserCorrectionRecord(BaseModel):
    """User correction audit trail schema per Section 53."""
    correction_id: str
    image_uri: str
    original_prediction_id: str
    original_prediction_name: str
    original_confidence: float
    user_corrected_id: str
    user_corrected_name: str
    portion_count: Optional[int] = None
    portion_weight_g: float
    region: Optional[str] = None
    timestamp: str = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    model_version: str = "v15.0.0-prod"


USER_CORRECTION_AUDIT_LOG: List[Section53SnackUserCorrectionRecord] = []


class SnackRecipeNutritionCalculator:
    """
    Implements Section 43 & 44 Calorie Estimation Pipeline:
    Food identity -> Variant -> Cooking method -> Portion/count -> Estimated weight ->
    Filling -> Toppings -> Accompaniments -> Recipe variation -> Nutrition database -> Estimated calories with uncertainty.
    """

    @classmethod
    def calculate_nutrition(
        cls,
        food_id_or_name: str,
        piece_count: Optional[int] = None,
        weight_grams: Optional[float] = None,
        preparation_style: str = "commercial", # "homemade", "commercial", "street_vendor"
        include_accompaniments: bool = True,
        accompaniment_list: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        record = get_snack_record_by_id(food_id_or_name) or resolve_snack_alias(food_id_or_name)
        if not record:
            record = SNACKS_TAXONOMY_REGISTRY["IND-SNK-UNKNOWN-001"]

        # 1. Resolve mass in grams
        if piece_count and piece_count > 0:
            std_wt = record.piece_weight_typical_g or 50.0
            total_snack_mass_g = piece_count * std_wt
            effective_count = piece_count
        elif weight_grams and weight_grams > 0:
            total_snack_mass_g = weight_grams
            std_wt = record.piece_weight_typical_g or 50.0
            effective_count = max(1, int(round(weight_grams / std_wt))) if record.is_countable else None
        else:
            total_snack_mass_g = record.default_portion_grams
            effective_count = record.piece_count_expected

        # 2. Recipe variation multipliers (Section 44)
        # Commercial / Halwai / Street foods typically have higher oil uptake & denser fillings
        if preparation_style == "street_vendor":
            fat_mult = 1.20
            cal_mult = 1.12
        elif preparation_style == "commercial":
            fat_mult = 1.10
            cal_mult = 1.06
        else: # homemade
            fat_mult = 0.90
            cal_mult = 0.95

        n_per_100 = record.nutrition_per_100g
        scale = total_snack_mass_g / 100.0

        snack_cals = round(scale * n_per_100.get("calories", 250.0) * cal_mult, 1)
        snack_pro = round(scale * n_per_100.get("protein", 6.0), 1)
        snack_carb = round(scale * n_per_100.get("carbs", 35.0), 1)
        snack_fat = round(scale * n_per_100.get("fat", 10.0) * fat_mult, 1)
        snack_fib = round(scale * n_per_100.get("fiber", 3.0), 1)

        # 3. Accompaniment calculation (Section 39) - Kept separate
        accompaniment_breakdown = []
        acc_total_cals = 0.0
        acc_total_weight_g = 0.0

        target_accs = accompaniment_list if accompaniment_list is not None else record.common_accompaniments
        if include_accompaniments and target_accs:
            for acc in target_accs:
                acc_lower = acc.lower()
                if "coconut" in acc_lower:
                    acc_wt = 35.0
                    acc_cal = 67.0
                elif "sambar" in acc_lower:
                    acc_wt = 100.0
                    acc_cal = 65.0
                elif "mint" in acc_lower or "green" in acc_lower:
                    acc_wt = 20.0
                    acc_cal = 10.0
                elif "tamarind" in acc_lower or "saunth" in acc_lower:
                    acc_wt = 25.0
                    acc_cal = 30.0
                elif "chole" in acc_lower:
                    acc_wt = 80.0
                    acc_cal = 104.0
                elif "pav" in acc_lower:
                    acc_wt = 55.0
                    acc_cal = 145.0
                else:
                    acc_wt = 20.0
                    acc_cal = 25.0

                accompaniment_breakdown.append({
                    "name": acc,
                    "weight_g": acc_wt,
                    "calories": acc_cal,
                })
                acc_total_cals += acc_cal
                acc_total_weight_g += acc_wt

        total_system_cals = round(snack_cals + acc_total_cals, 1)
        total_system_mass = round(total_snack_mass_g + acc_total_weight_g, 1)

        # Calorie uncertainty range (Section 43)
        lower_bound = round(total_system_cals * 0.88, 1)
        upper_bound = round(total_system_cals * 1.15, 1)

        return {
            "canonical_food_id": record.canonical_food_id,
            "canonical_name": record.canonical_name,
            "region": record.region,
            "state": record.state_or_city,
            "snack_family": record.snack_family,
            "cooking_method": record.cooking_method,
            "piece_count": effective_count,
            "snack_weight_g": round(total_snack_mass_g, 1),
            "snack_nutrition": {
                "calories": snack_cals,
                "protein_g": snack_pro,
                "carbs_g": snack_carb,
                "fat_g": snack_fat,
                "fiber_g": snack_fib,
            },
            "accompaniments_breakdown": accompaniment_breakdown,
            "accompaniments_weight_g": round(acc_total_weight_g, 1),
            "accompaniments_calories": round(acc_total_cals, 1),
            "total_plate_weight_g": total_system_mass,
            "total_plate_calories": total_system_cals,
            "calorie_uncertainty_range": (lower_bound, upper_bound),
            "preparation_style": preparation_style,
            "zero_monolithic_guarantee": True,
        }

    @classmethod
    def record_user_correction(
        cls,
        image_uri: str,
        predicted_id: str,
        predicted_name: str,
        confidence: float,
        corrected_id: str,
        corrected_name: str,
        portion_weight_g: float,
        region: Optional[str] = None,
    ) -> Section53SnackUserCorrectionRecord:
        """Stores user corrections for Active Learning loop (Sections 53 & 54)."""
        import uuid
        record = Section53SnackUserCorrectionRecord(
            correction_id=f"corr-snk-{uuid.uuid4().hex[:8]}",
            image_uri=image_uri,
            original_prediction_id=predicted_id,
            original_prediction_name=predicted_name,
            original_confidence=confidence,
            user_corrected_id=corrected_id,
            user_corrected_name=corrected_name,
            portion_weight_g=portion_weight_g,
            region=region,
        )
        USER_CORRECTION_AUDIT_LOG.append(record)
        return record
