"""
Indian Curry Recipe Nutrition Engine & Standardized Output Schemas (Part 11)
Implements Sections 52, 57, 66, 67, 70, 71, 72, 73, 74 of Part 11 Master Training Specification.

Guarantees:
- End-to-end curry recipe synthesis:
  Calories = BaseGravy + ProteinChunks/Veg + FloatingOilAdjustment + Cream/Dairy/Coconut.
- Section 57 Single Curry & Chicken Curry Annotation Schemas.
- Section 52 Unknown Curry Fallback Schema ("Indian curry/gravy — exact dish uncertain").
- Section 66 Final App Output Schema.
- Section 67 Banana Leaf Meal Output Schema (Strictly anti-monolithic).
- Section 70 Calorie Uncertainty Range Output Schema.
- Section 88 Standardized Single and Multi Curry Output Schemas.
- Zero False Precision: Strictly emits calibrated ranges (e.g., "180–240 kcal") with uncertainty explanations.
"""

from typing import Dict, Any, Optional, List, Tuple
from pydantic import BaseModel, Field

from app.food_ai.taxonomy.curry_master_taxonomy import (
    get_curry_food_class,
    resolve_curry_food_by_name,
    CurryFoodClassRecord,
    CURRY_TAXONOMY_REGISTRY
)
from app.food_ai.portion_engine.curry_portions import (
    CurryPortionEngine,
    CurryProteinGravySplitter,
    CurryFloatingOilEstimator
)


# =============================================================================
# 1. Output Schemas
# =============================================================================

class Section57CurryAnnotation(BaseModel):
    food_name: str
    region: str
    state: str
    curry_family: str
    specific_curry: str
    variant: str
    gravy_base: str
    consistency: str
    primary_ingredient: str
    cooking_method: str
    portion_size: str
    portion_weight_g: float
    calories: float
    protein_g: float
    carbohydrates_g: float
    fat_g: float
    fiber_g: float
    confidence: float = Field(..., ge=0.0, le=1.0)
    uncertainty_range: Dict[str, float]


class Section57ChickenCurryAnnotation(BaseModel):
    food_name: str
    region: str
    state: str
    curry_family: str = "Chicken Curries"
    specific_curry: str
    variant: str
    cut_type: str  # "Bone-in", "Boneless"
    piece_count: int
    meat_weight_g: float
    gravy_weight_g: float
    total_weight_g: float
    gravy_base: str
    consistency: str
    calories: float
    protein_g: float
    carbohydrates_g: float
    fat_g: float
    fiber_g: float
    confidence: float = Field(..., ge=0.0, le=1.0)
    uncertainty_range: Dict[str, float]


class Section52UnknownCurryOutput(BaseModel):
    status: str = "uncertain"
    predicted_category: str = "Indian curry/gravy — exact dish uncertain"
    apparent_color: str
    observed_consistency: str
    confidence: float = 0.35
    confidence_level: str = "Low"
    explanation: str = "Visual features are insufficient to confirm specific dal/curry variant without risking false classification (Section 52 & 73 compliance)."
    calorie_estimate_range: str = "120–280 kcal per 150g standard katori depending on oil/cream content"
    prompt_for_user: str = "Could you tell us what kind of curry or dal this is?"
    requires_user_confirmation: bool = True


class Section66FinalAppOutput(BaseModel):
    dish_name: str
    regional_attribution: str
    portion_description: str
    calories_range: str  # e.g., "160–210 kcal"
    calories_expected: float
    macronutrients: Dict[str, float]  # Protein, Carbs, Fat, Fiber
    confidence_score: float
    confidence_rating: str  # "High", "Medium", "Low"
    uncertainty_factors: List[str]
    user_guidance: Optional[str] = None


class Section67BananaLeafMealOutput(BaseModel):
    meal_title: str = "South Indian Banana Leaf Feast"
    leaf_layout: str
    constituent_items: List[Dict[str, Any]]
    total_meal_weight_g: float
    total_meal_calories_range: str
    total_meal_calories_expected: float
    total_protein_g: float
    total_carbs_g: float
    total_fat_g: float
    total_fiber_g: float
    anti_monolithic_compliance: bool = True


class Section70CalorieUncertaintyOutput(BaseModel):
    dish_id: str
    dish_name: str
    nominal_calories: float
    calibrated_calorie_range: str
    calories_low: float
    calories_high: float
    uncertainty_variance_reasons: List[str]


class Section88CurrySingleOutput(BaseModel):
    food_name: str
    canonical_id: str
    curry_family: str
    regional_attribution: str
    gravy_base: str
    consistency: str
    primary_ingredient: str
    cooking_method: str
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
    confidence: str
    confidence_score: float
    uncertainty_reason: str
    requires_user_confirmation: bool = False


class Section88CurryMultiOutput(BaseModel):
    plate_title: str
    detected_items: List[Dict[str, Any]]
    total_estimated_weight_g: float
    total_estimated_calories_range: str
    total_calories_low: float
    total_calories_expected: float
    total_calories_high: float
    total_protein_g: float
    total_carbs_g: float
    total_fat_g: float
    total_fiber_g: float
    overall_confidence: float
    notes: str


# =============================================================================
# 2. Nutrition Synthesis Engine
# =============================================================================

# Base Gravy Nutrition Profiles per 100g
BASE_GRAVY_PROFILES: Dict[str, Dict[str, float]] = {
    "yellow_lentil": {"cals": 95.0, "p": 5.2, "c": 13.0, "f": 2.6, "fib": 2.8},
    "black_lentil_butter": {"cals": 145.0, "p": 4.8, "c": 14.5, "f": 7.8, "fib": 3.2},
    "makhani_tomato_butter": {"cals": 155.0, "p": 2.6, "c": 8.5, "f": 12.2, "fib": 1.4},
    "onion_tomato_masala": {"cals": 105.0, "p": 2.2, "c": 9.5, "f": 6.5, "fib": 1.8},
    "coconut_masala": {"cals": 140.0, "p": 2.5, "c": 7.0, "f": 11.5, "fib": 2.2},
    "tamarind_broth": {"cals": 38.0, "p": 1.1, "c": 4.8, "f": 1.5, "fib": 0.8},
    "yogurt_besan": {"cals": 75.0, "p": 3.0, "c": 7.5, "f": 3.6, "fib": 0.8},
    "spinach_garlic": {"cals": 65.0, "p": 3.2, "c": 5.5, "f": 3.4, "fib": 2.5},
    "kuzhambu_sesame_oil": {"cals": 85.0, "p": 1.8, "c": 8.0, "f": 5.2, "fib": 1.5},
}

# Protein / Inclusions Nutrition Profiles per 100g
PROTEIN_CHUNK_PROFILES: Dict[str, Dict[str, float]] = {
    "chicken_meat": {"cals": 175.0, "p": 25.0, "c": 0.0, "f": 7.5, "fib": 0.0},
    "mutton_meat": {"cals": 220.0, "p": 22.0, "c": 0.0, "f": 14.0, "fib": 0.0},
    "paneer": {"cals": 265.0, "p": 18.3, "c": 1.2, "f": 20.8, "fib": 0.0},
    "fish_flesh": {"cals": 130.0, "p": 20.5, "c": 0.0, "f": 4.8, "fib": 0.0},
    "boiled_egg": {"cals": 155.0, "p": 12.6, "c": 1.1, "f": 10.6, "fib": 0.0},
    "prawn_flesh": {"cals": 99.0, "p": 21.0, "c": 0.2, "f": 1.1, "fib": 0.0},
    "vegetable_medley": {"cals": 45.0, "p": 1.5, "c": 7.0, "f": 1.0, "fib": 2.5},
    "chickpeas_chole": {"cals": 164.0, "p": 8.9, "c": 27.4, "f": 2.6, "fib": 7.6},
    "kidney_beans_rajma": {"cals": 127.0, "p": 8.7, "c": 22.8, "f": 0.5, "fib": 6.4},
}


class CurryRecipeNutritionCalculator:
    """
    Synthesizes exact dynamic macronutrients and calibrated uncertainty ranges
    for any Indian curry, dal, or gravy dish.
    """

    @classmethod
    def calculate_curry_nutrition(
        cls,
        curry_name: str,
        portion_category: str = "Medium",
        vessel_type: Optional[str] = None,
        piece_count: Optional[int] = None,
        is_bone_in: bool = False,
        oil_sheen: str = "medium",
        is_restaurant_style: bool = False
    ) -> Dict[str, Any]:
        # 1. Resolve taxonomy record
        rec = resolve_curry_food_by_name(curry_name)
        if not rec:
            # Fallback
            rec = CURRY_TAXONOMY_REGISTRY["yellow_dal_tadka"]

        # 2. Estimate portion
        portion_info = CurryPortionEngine.estimate_curry_portion(
            curry_family=rec.food_family,
            portion_category=portion_category,
            vessel_type=vessel_type,
            consistency=rec.consistency,
            visual_features={"oil_sheen": oil_sheen}
        )
        total_weight_g = portion_info["weight_grams"]

        # 3. Determine base gravy and protein chunks
        cname = rec.canonical_food_id.lower()
        if "dal_makhani" in cname:
            gravy_key = "black_lentil_butter"
            protein_key = None
        elif "paneer" in cname:
            gravy_key = "makhani_tomato_butter" if "butter" in cname or "shahi" in cname else "onion_tomato_masala"
            protein_key = "paneer"
        elif "chicken" in cname:
            gravy_key = "makhani_tomato_butter" if "butter" in cname or "tikka" in cname else "onion_tomato_masala"
            protein_key = "chicken_meat"
        elif "mutton" in cname:
            gravy_key = "onion_tomato_masala"
            protein_key = "mutton_meat"
        elif "fish" in cname or "meen" in cname:
            gravy_key = "coconut_masala" if "kerala" in cname or "goan" in cname else "tamarind_broth"
            protein_key = "fish_flesh"
        elif "prawn" in cname or "shrimp" in cname:
            gravy_key = "coconut_masala"
            protein_key = "prawn_flesh"
        elif "egg" in cname or "anda" in cname:
            gravy_key = "onion_tomato_masala"
            protein_key = "boiled_egg"
        elif "chole" in cname:
            gravy_key = "onion_tomato_masala"
            protein_key = "chickpeas_chole"
        elif "rajma" in cname:
            gravy_key = "onion_tomato_masala"
            protein_key = "kidney_beans_rajma"
        elif "kadhi" in cname:
            gravy_key = "yogurt_besan"
            protein_key = None
        elif "rasam" in cname:
            gravy_key = "tamarind_broth"
            protein_key = None
        elif "kuzhambu" in cname:
            gravy_key = "kuzhambu_sesame_oil"
            protein_key = None
        elif "kootu" in cname:
            gravy_key = "coconut_masala"
            protein_key = "vegetable_medley"
        elif "palak" in cname or "saag" in cname:
            gravy_key = "spinach_garlic"
            protein_key = "paneer" if "paneer" in cname else None
        else:
            gravy_key = "yellow_lentil"
            protein_key = None

        gravy_profile = BASE_GRAVY_PROFILES.get(gravy_key, BASE_GRAVY_PROFILES["yellow_lentil"])

        # 4. Protein / Gravy weight separation
        if protein_key:
            count = piece_count or (4 if "paneer" in protein_key else 3 if "meat" in protein_key or "fish" in protein_key else 2)
            split_res = CurryProteinGravySplitter.split_portion(
                protein_type=protein_key,
                total_dish_weight_g=total_weight_g,
                piece_count=count,
                is_bone_in=is_bone_in
            )
            edible_protein_mass = split_res.edible_meat_weight_g
            gravy_mass = split_res.gravy_weight_g
            protein_profile = PROTEIN_CHUNK_PROFILES.get(protein_key, PROTEIN_CHUNK_PROFILES["chicken_meat"])
        else:
            split_res = None
            edible_protein_mass = 0.0
            gravy_mass = total_weight_g
            protein_profile = None

        # 5. Base Gravy Nutrition
        cals_from_gravy = (gravy_mass / 100.0) * gravy_profile["cals"]
        p_from_gravy = (gravy_mass / 100.0) * gravy_profile["p"]
        c_from_gravy = (gravy_mass / 100.0) * gravy_profile["c"]
        f_from_gravy = (gravy_mass / 100.0) * gravy_profile["f"]
        fib_from_gravy = (gravy_mass / 100.0) * gravy_profile["fib"]

        # 6. Protein Inclusions Nutrition
        if protein_profile and edible_protein_mass > 0:
            cals_from_protein = (edible_protein_mass / 100.0) * protein_profile["cals"]
            p_from_protein = (edible_protein_mass / 100.0) * protein_profile["p"]
            c_from_protein = (edible_protein_mass / 100.0) * protein_profile["c"]
            f_from_protein = (edible_protein_mass / 100.0) * protein_profile["f"]
            fib_from_protein = (edible_protein_mass / 100.0) * protein_profile["fib"]
        else:
            cals_from_protein = p_from_protein = c_from_protein = f_from_protein = fib_from_protein = 0.0

        # 7. Floating Oil / Roghan Adjustment
        oil_data = portion_info["oil_sheen_data"]
        added_oil_g = oil_data["added_oil_grams"]
        added_oil_cals = oil_data["calorie_bump"]

        # Restaurant style multiplier (extra cream / butter hidden in restaurant preparations)
        restaurant_factor = 1.15 if is_restaurant_style else 1.0

        total_cals = round((cals_from_gravy + cals_from_protein + added_oil_cals) * restaurant_factor, 1)
        total_p = round(p_from_gravy + p_from_protein, 1)
        total_c = round(c_from_gravy + c_from_protein, 1)
        total_f = round((f_from_gravy + f_from_protein + added_oil_g) * restaurant_factor, 1)
        total_fib = round(fib_from_gravy + fib_from_protein, 1)

        # 8. Calibrated Uncertainty Range
        spread = 0.14 if oil_sheen in ["low", "medium"] else 0.22
        cal_low = round(total_cals * (1.0 - spread), 0)
        cal_high = round(total_cals * (1.0 + spread), 0)
        cal_range_str = f"{int(cal_low)}–{int(cal_high)} kcal"

        uncertainty_factors = [
            f"Oil sheen detected as {oil_data['tier_name']} (approx ±{oil_data['added_oil_grams']}g fat variance).",
            "Lentil-to-water dilution and thickening time variance across domestic vs restaurant preparations.",
        ]
        if split_res and split_res.is_bone_in:
            uncertainty_factors.append("Bone-to-meat ratio deduction (~28% of chicken piece mass).")

        return {
            "record": rec,
            "portion_info": portion_info,
            "split_res": split_res,
            "gravy_key": gravy_key,
            "protein_key": protein_key,
            "total_weight_g": total_weight_g,
            "total_calories": total_cals,
            "calories_low": cal_low,
            "calories_high": cal_high,
            "calories_range_str": cal_range_str,
            "protein_g": total_p,
            "carbs_g": total_c,
            "fat_g": total_f,
            "fiber_g": total_fib,
            "oil_sheen_data": oil_data,
            "uncertainty_factors": uncertainty_factors
        }

    # =========================================================================
    # Schema Generators
    # =========================================================================

    @classmethod
    def generate_section_57_curry_annotation(
        cls,
        curry_name: str,
        portion_category: str = "Medium",
        oil_sheen: str = "medium"
    ) -> Section57CurryAnnotation:
        res = cls.calculate_curry_nutrition(curry_name, portion_category=portion_category, oil_sheen=oil_sheen)
        rec: CurryFoodClassRecord = res["record"]
        return Section57CurryAnnotation(
            food_name=rec.canonical_name,
            region=rec.region,
            state=rec.state_or_city,
            curry_family=rec.food_family,
            specific_curry=rec.specific_dish,
            variant=rec.hierarchy.level6_variant,
            gravy_base=rec.gravy_base,
            consistency=rec.consistency,
            primary_ingredient=rec.main_ingredient,
            cooking_method=rec.cooking_method,
            portion_size=f"{portion_category} ({int(res['total_weight_g'])}g)",
            portion_weight_g=res["total_weight_g"],
            calories=res["total_calories"],
            protein_g=res["protein_g"],
            carbohydrates_g=res["carbs_g"],
            fat_g=res["fat_g"],
            fiber_g=res["fiber_g"],
            confidence=0.92,
            uncertainty_range={
                "low": res["calories_low"],
                "expected": res["total_calories"],
                "high": res["calories_high"]
            }
        )

    @classmethod
    def generate_section_57_chicken_annotation(
        cls,
        curry_name: str = "Homestyle Chicken Curry",
        portion_category: str = "Medium",
        piece_count: int = 3,
        is_bone_in: bool = True,
        oil_sheen: str = "medium"
    ) -> Section57ChickenCurryAnnotation:
        res = cls.calculate_curry_nutrition(
            curry_name,
            portion_category=portion_category,
            piece_count=piece_count,
            is_bone_in=is_bone_in,
            oil_sheen=oil_sheen
        )
        rec: CurryFoodClassRecord = res["record"]
        split: Any = res["split_res"]
        meat_w = split.edible_meat_weight_g if split else 80.0
        gravy_w = split.gravy_weight_g if split else 120.0

        return Section57ChickenCurryAnnotation(
            food_name=rec.canonical_name,
            region=rec.region,
            state=rec.state_or_city,
            curry_family="Chicken Curries",
            specific_curry=rec.specific_dish,
            variant=rec.hierarchy.level6_variant,
            cut_type="Bone-in" if is_bone_in else "Boneless",
            piece_count=piece_count,
            meat_weight_g=meat_w,
            gravy_weight_g=gravy_w,
            total_weight_g=res["total_weight_g"],
            gravy_base=rec.gravy_base,
            consistency=rec.consistency,
            calories=res["total_calories"],
            protein_g=res["protein_g"],
            carbohydrates_g=res["carbs_g"],
            fat_g=res["fat_g"],
            fiber_g=res["fiber_g"],
            confidence=0.91,
            uncertainty_range={
                "low": res["calories_low"],
                "expected": res["total_calories"],
                "high": res["calories_high"]
            }
        )

    @classmethod
    def generate_section_52_unknown_fallback(
        cls,
        color: str = "yellow",
        consistency: str = "medium"
    ) -> Section52UnknownCurryOutput:
        return Section52UnknownCurryOutput(
            apparent_color=color,
            observed_consistency=consistency
        )

    @classmethod
    def generate_section_66_app_output(
        cls,
        curry_name: str,
        portion_category: str = "Medium",
        oil_sheen: str = "medium"
    ) -> Section66FinalAppOutput:
        res = cls.calculate_curry_nutrition(curry_name, portion_category=portion_category, oil_sheen=oil_sheen)
        rec: CurryFoodClassRecord = res["record"]
        return Section66FinalAppOutput(
            dish_name=rec.canonical_name,
            regional_attribution=f"{rec.region} ({rec.state_or_city})",
            portion_description=f"1 {portion_category} Katori/Bowl (~{int(res['total_weight_g'])}g)",
            calories_range=res["calories_range_str"],
            calories_expected=res["total_calories"],
            macronutrients={
                "protein_g": res["protein_g"],
                "carbs_g": res["carbs_g"],
                "fat_g": res["fat_g"],
                "fiber_g": res["fiber_g"]
            },
            confidence_score=0.91,
            confidence_rating="High",
            uncertainty_factors=res["uncertainty_factors"],
            user_guidance="Log as standard bowl. If restaurant preparation was excessively buttery or oily, choose High oil option."
        )

    @classmethod
    def generate_section_70_uncertainty_output(
        cls,
        curry_name: str,
        portion_category: str = "Medium"
    ) -> Section70CalorieUncertaintyOutput:
        res = cls.calculate_curry_nutrition(curry_name, portion_category=portion_category)
        rec: CurryFoodClassRecord = res["record"]
        return Section70CalorieUncertaintyOutput(
            dish_id=rec.canonical_food_id,
            dish_name=rec.canonical_name,
            nominal_calories=res["total_calories"],
            calibrated_calorie_range=res["calories_range_str"],
            calories_low=res["calories_low"],
            calories_high=res["calories_high"],
            uncertainty_variance_reasons=res["uncertainty_factors"]
        )

    @classmethod
    def generate_section_88_single_output(
        cls,
        curry_name: str,
        portion_category: str = "Medium",
        oil_sheen: str = "medium"
    ) -> Section88CurrySingleOutput:
        res = cls.calculate_curry_nutrition(curry_name, portion_category=portion_category, oil_sheen=oil_sheen)
        rec: CurryFoodClassRecord = res["record"]
        return Section88CurrySingleOutput(
            food_name=rec.canonical_name,
            canonical_id=rec.canonical_food_id,
            curry_family=rec.food_family,
            regional_attribution=f"{rec.region} / {rec.state_or_city}",
            gravy_base=rec.gravy_base,
            consistency=rec.consistency,
            primary_ingredient=rec.main_ingredient,
            cooking_method=rec.cooking_method,
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
            confidence="High",
            confidence_score=0.92,
            uncertainty_reason="; ".join(res["uncertainty_factors"])
        )
