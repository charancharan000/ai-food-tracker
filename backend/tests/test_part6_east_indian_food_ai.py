"""
Test Suite for Part 6 — East Indian Food Master Dataset & AI Vision Engine
Verifies:
1. Strict 9-level taxonomy hierarchy and permanent IDs across all 4 East Indian States:
   (West Bengal, Odisha, Bihar, Jharkhand)
2. Multi-lingual regional names (English, Bengali বাংলা, Odia ଓଡ଼ିଆ, Hindi/Bhojpuri/Maithili)
3. Fish Species Separate Confidence vs Dish Confidence (Quality Rule 3 & Section 3, 37)
4. Mustard Fish (Shorshe) Detector vs Yellow / Coconut / Tomato Curry (Section 4, 38)
5. Sweets Hard Negatives: Rasgulla vs Gulab Jamun, Sandesh vs Peda, Mishti Doi vs Yogurt,
   Chhena Poda vs Cake, Thekua vs Cookie, Khaja vs Pastry (Section 39)
6. Bread Hard Negatives: Luchi vs Puri, Radha Ballavi vs Kachori, Sattu Paratha vs Aloo Paratha,
   Dhuska vs Vada, Chilka Roti vs Dosa (Section 40)
7. Champaran Ahuna Mutton Verifier (clay handi, intact whole garlic bulb, mustard oil float) (Section 28)
8. Wild Leafy Saag Verifier: never force exact species under ambiguous cues (Section 32)
9. Dahibara Aloodum 8-Component Segmenter vs generic Dahi Vada (Section 35)
10. Litti Chokha Decomposer (never classifies whole plate as single food) (Section 24, Rule 4)
11. Luchi Alur Dom Breakfast Decomposer (food_1 = Luchi, food_2 = Alur Dom) (Section 8)
12. Dhuska Ghugni Breakfast Decomposer (Section 31)
13. Puri Jagannath Mahaprasad Decomposer (system of preparations, not homogeneous food) (Section 21, Rule 5)
14. Bengali & Odia Thali Decomposers (Section 33, Rule 4)
15. Countable Food Portions (Count * calibrated unit weight) (Section 42)
16. Visual Fat Sheen Estimator (mustard oil float, ghee sheen) (Section 53)
17. Unknown / Low-evidence fallback: EAST_INDIAN_UNKNOWN (Section 48, Rule 18)
18. Section 63 Standardized Model Output Schema compliance & Calorie Ranges (Section 52, 63)
19. Unified Production Orchestrator East Indian routing
"""

import pytest
from app.food_ai.taxonomy.east_indian_master_taxonomy import (
    EAST_INDIAN_TAXONOMY_REGISTRY,
    get_east_food_class,
    resolve_east_food_by_name,
    list_all_east_food_ids
)
from app.food_ai.datasets.east_indian_hard_negatives import (
    EAST_INDIAN_CONFUSION_REGISTRY,
    disambiguate_east_indian_pair,
    FishSpeciesClassifier,
    MustardFishDetector,
    DahibaraAloodumSegmenter,
    ChamparanMuttonDetector,
    LeafyGreenSaagVerifier
)
from app.food_ai.datasets.east_indian_composite_decomposer import (
    BengaliThaliDecomposer,
    OdiaThaliDecomposer,
    LittiChokhaDecomposer,
    DahibaraAloodumDecomposer,
    LuchiAlurDomDecomposer,
    DhuskaGhugniDecomposer,
    MahaprasadTempleDecomposer,
    PackagingFilter,
    EastIndianCompositeDecompositionResult
)
from app.food_ai.portion_engine.east_indian_portions import (
    CountableFoodDetector,
    EastIndianPortionClassifier,
    PortionReferenceScaler,
    VisualFatSheenEstimator
)
from app.food_ai.nutrition_engine.east_indian_recipes import (
    EastIndianRecipeNutritionCalculator,
    Section63ModelOutput
)
from app.food_ai.inference_orchestrator import production_orchestrator


# =============================================================================
# 1. TAXONOMY & REGIONAL HIERARCHY TESTS
# =============================================================================

def test_east_indian_taxonomy_and_4_states_coverage():
    """Verifies that all 4 East Indian states are represented with permanent IDs."""
    assert len(EAST_INDIAN_TAXONOMY_REGISTRY) >= 45

    states_found = set()
    for food in EAST_INDIAN_TAXONOMY_REGISTRY.values():
        assert food.hierarchy.level1_food == "Indian Food"
        assert food.hierarchy.level2_macro_region == "East Indian Food"
        states_found.add(food.state)
        assert food.canonical_food_id.startswith(("WB_", "OD_", "BR_", "JH_", "EI_", "EAST_"))
        assert food.density_g_cm3 >= 0.40
        assert food.default_serving_weight_g > 0.0

    required_states = ["West Bengal", "Odisha", "Bihar", "Jharkhand"]
    for st in required_states:
        assert st in states_found, f"State {st} missing in East Indian taxonomy!"


def test_east_indian_multilingual_name_mapping():
    """Verifies resolution of food by Bengali, Odia, Hindi/Bhojpuri, and English names."""
    # Shorshe Ilish (Bengali)
    ilish = resolve_east_food_by_name("সর্ষে ইলিশ")
    assert ilish is not None
    assert ilish.canonical_food_id == "WB_FISH_SHORSHE_ILISH"

    # Chhena Poda (Odia)
    chhenapoda = resolve_east_food_by_name("ଛେନାପୋଡ଼")
    assert chhenapoda is not None
    assert chhenapoda.canonical_food_id == "OD_SWEET_CHHENA_PODA"

    # Litti (Hindi/Bhojpuri)
    litti = resolve_east_food_by_name("लिट्टी")
    assert litti is not None
    assert litti.canonical_food_id == "BR_BREAD_LITTI"

    # Dhuska (Jharkhandi)
    dhuska = resolve_east_food_by_name("धुस्का")
    assert dhuska is not None
    assert dhuska.canonical_food_id == "JH_SNACK_DHUSKA"

    # English Alias
    mishti_doi = resolve_east_food_by_name("bengali sweet curd")
    assert mishti_doi is not None
    assert mishti_doi.canonical_food_id == "WB_SWEET_MISHTI_DOI"


# =============================================================================
# 2. FISH SPECIES CLASSIFIER & CONFIDENCE SEPARATION (Section 3, 37, Rule 3)
# =============================================================================

def test_fish_species_separate_confidence_when_evidence_sufficient():
    """Verifies species classification separated from dish classification when clear anatomical cues exist."""
    cues = {
        "is_submerged": False,
        "visible_anatomy": ["hilsa_broad_herring_cross_section", "ilish_silvery_fine_texture"],
        "steak_shape": "broad_peti"
    }
    res = FishSpeciesClassifier.classify_fish_and_species(cues, "Shorshe Ilish")
    assert res.dish_name == "Shorshe Ilish"
    assert res.dish_confidence >= 0.90
    assert res.fish_species == "Hilsa"
    assert res.fish_species_confidence >= 0.90
    assert res.visual_evidence_sufficient is True


def test_fish_species_quality_rule_3_unknown_when_submerged_or_obscured():
    """Quality Rule 3: Never identify fish species when visual evidence is insufficient."""
    cues_submerged = {
        "is_submerged": True,
        "visible_anatomy": [],
        "steak_shape": "obscured"
    }
    res = FishSpeciesClassifier.classify_fish_and_species(cues_submerged, "Macher Jhol")
    assert res.dish_name == "Macher Jhol"
    assert res.dish_confidence >= 0.85 # Dish is still detected!
    assert res.fish_species == "unknown" # Species is unknown!
    assert res.fish_species_confidence < 0.40 # Species confidence is low
    assert res.visual_evidence_sufficient is False
    assert "Quality Rule 3" in res.evidence_notes


def test_fish_species_prawn_and_crab_recognition():
    """Verifies recognition of distinct seafood anatomies."""
    prawn_cues = {"is_submerged": False, "visible_anatomy": ["prawn_curled_tail"], "steak_shape": "curled"}
    p_res = FishSpeciesClassifier.classify_fish_and_species(prawn_cues, "Chingri Malai Curry")
    assert p_res.fish_species == "Prawn"

    crab_cues = {"is_submerged": False, "visible_anatomy": ["crab_claws"], "steak_shape": "whole_carapace"}
    c_res = FishSpeciesClassifier.classify_fish_and_species(crab_cues, "Kankada Jhola")
    assert c_res.fish_species == "Crab"


# =============================================================================
# 3. MUSTARD FISH DETECTOR (Section 4, 38)
# =============================================================================

def test_mustard_fish_detector_vs_hard_negatives():
    """Verifies Shorshe Maach disambiguation against yellow, coconut, and tomato curries."""
    # Authentic Shorshe
    shorshe_cues = {
        "mustard_paste_texture": True,
        "slit_green_chillies": True,
        "mustard_oil_sheen": True,
        "coconut_milk_base": False,
        "tomato_red_base": False
    }
    s_res = MustardFishDetector.evaluate(shorshe_cues)
    assert s_res["is_mustard_fish"] is True
    assert s_res["category"] == "shorshe_maach"

    # Coconut Curry Hard Negative
    coconut_cues = {
        "mustard_paste_texture": False,
        "coconut_milk_base": True,
        "tomato_red_base": False
    }
    c_res = MustardFishDetector.evaluate(coconut_cues)
    assert c_res["is_mustard_fish"] is False
    assert c_res["category"] == "coconut_fish_curry"

    # Tomato Curry Hard Negative
    tomato_cues = {
        "mustard_paste_texture": False,
        "coconut_milk_base": False,
        "tomato_red_base": True
    }
    t_res = MustardFishDetector.evaluate(tomato_cues)
    assert t_res["is_mustard_fish"] is False
    assert t_res["category"] == "tomato_fish_curry"


# =============================================================================
# 4. SWEETS & BREAD HARD NEGATIVES (Sections 39, 40, 55)
# =============================================================================

def test_sweets_hard_negative_registry_entries():
    """Verifies all mandatory Section 39 sweet confusion pairs are registered."""
    pairs = [
        "CONF_RASGULLA_VS_GULAB_JAMUN",
        "CONF_SANDESH_VS_PEDA",
        "CONF_MISHTI_DOI_VS_YOGURT_KHEER",
        "CONF_CHHENA_PODA_VS_CAKE",
        "CONF_PATISHAPTA_VS_CREPE",
        "CONF_MALPUA_VS_PANCAKE",
        "CONF_THEKUA_VS_COOKIE",
        "CONF_KHAJA_VS_PASTRY"
    ]
    for cid in pairs:
        pair = disambiguate_east_indian_pair(cid)
        assert pair is not None, f"Missing sweet confusion pair: {cid}"
        assert len(pair.discriminating_visual_features) >= 2


def test_bread_hard_negative_registry_entries():
    """Verifies all mandatory Section 40 bread confusion pairs are registered."""
    pairs = [
        "CONF_LUCHI_VS_PURI",
        "CONF_RADHA_BALLAVI_VS_KACHORI",
        "CONF_SATTU_PARATHA_VS_ALOO_PARATHA",
        "CONF_DHUSKA_VS_VADA",
        "CONF_CHILKA_ROTI_VS_DOSA"
    ]
    for cid in pairs:
        pair = disambiguate_east_indian_pair(cid)
        assert pair is not None, f"Missing bread confusion pair: {cid}"
        assert len(pair.discriminating_visual_features) >= 2


# =============================================================================
# 5. SPECIALIZED DETECTORS (Sections 28, 32, 35)
# =============================================================================

def test_champaran_ahuna_mutton_detector():
    """Section 28: Earthen pot + whole intact garlic bulb + mustard oil float."""
    # Positive case: Clay handi + intact garlic
    pos_cues = {
        "earthen_clay_pot_visible": True,
        "whole_intact_garlic_bulb_visible": True,
        "heavy_mustard_oil_float": True,
        "whole_peppercorn_cloves_visible": True
    }
    pos_res = ChamparanMuttonDetector.verify(pos_cues)
    assert pos_res["is_champaran_ahuna_mutton"] is True
    assert pos_res["whole_garlic_detected"] is True

    # Negative case: Just a dark curry in a bowl without garlic bulb
    neg_cues = {
        "earthen_clay_pot_visible": False,
        "whole_intact_garlic_bulb_visible": False,
        "heavy_mustard_oil_float": False,
        "whole_peppercorn_cloves_visible": False
    }
    neg_res = ChamparanMuttonDetector.verify(neg_cues)
    assert neg_res["is_champaran_ahuna_mutton"] is False


def test_leafy_green_saag_ambiguity_rule():
    """Section 32: Do not force exact species identification if visual evidence is insufficient."""
    # Exact cues available: bifid leaves -> Koinar
    koinar_cues = {"leaf_shape": "bifid_folded", "is_dry_bhaji": True}
    k_res = LeafyGreenSaagVerifier.identify_saag(koinar_cues)
    assert k_res["is_species_exact"] is True
    assert "Koinar Saag" in k_res["possible_species"][0]

    # Ambiguous cues: finely chopped leaves -> broad dish output
    chopped_cues = {"leaf_shape": "chopped_fine", "is_dry_bhaji": True}
    c_res = LeafyGreenSaagVerifier.identify_saag(chopped_cues)
    assert c_res["is_species_exact"] is False
    assert c_res["leafy_green_dish"] == "East Indian Saag Bhaja"
    assert len(c_res["possible_species"]) >= 3


def test_dahibara_aloodum_component_segmenter():
    """Section 35: Detects 8 discrete components of Cuttack Dahibara Aloodum."""
    cues = {
        "has_soaked_urad_vadas": True,
        "has_dark_spiced_potato_curry": True,
        "has_yellow_pea_curry": True,
        "has_thin_buttermilk_liquid": True,
        "has_sweet_tangy_chutney": True,
        "has_fine_crisp_sev": True,
        "has_raw_onions": True,
        "has_fresh_coriander": True
    }
    res = DahibaraAloodumSegmenter.segment_components(cues)
    assert res["is_dahibara_aloodum"] is True
    assert res["component_coverage_score"] == 1.0


# =============================================================================
# 6. COMPOSITE MEAL DECOMPOSERS (Sections 8, 21, 24, 31, 33, 35)
# =============================================================================

def test_litti_chokha_decomposer_never_classifies_as_single_food():
    """Section 24 & Quality Rule 4: Litti plate decomposed into discrete components."""
    res = LittiChokhaDecomposer.decompose({"litti_count": 2, "has_dal": True})
    assert isinstance(res, EastIndianCompositeDecompositionResult)
    assert res.total_components_detected >= 6

    names = [it.name for it in res.items]
    assert "Sattu Stuffed Litti" in names
    assert "Baingan Chokha" in names
    assert "Aloo Chokha" in names
    assert "Pure Desi Ghee Dip" in names
    assert res.total_edible_weight_g > 300.0
    assert res.total_calories > 400.0


def test_luchi_alur_dom_breakfast_decomposer():
    """Section 8: Luchi + Alur Dom must produce food_1 = Luchi, food_2 = Alur Dom, not generic breakfast."""
    res = LuchiAlurDomDecomposer.decompose({"luchi_count": 4})
    assert len(res.items) == 2
    assert res.items[0].name == "Luchi"
    assert res.items[0].is_countable is True
    assert res.items[0].count == 4
    assert res.items[1].name == "Bengali Alur Dom"
    assert res.items[1].estimated_weight_g == 150.0


def test_dhuska_ghugni_breakfast_decomposer():
    """Section 31: Dhuska + Ghugni decomposed into fried bread count + ghugni + chutney."""
    res = DhuskaGhugniDecomposer.decompose({"dhuska_count": 3})
    assert len(res.items) == 3
    assert res.items[0].name == "Jharkhandi Dhuska"
    assert res.items[0].count == 3
    assert "Ghugni" in res.items[1].name


def test_mahaprasad_temple_decomposer_quality_rule_5():
    """Section 21 & Quality Rule 5: Mahaprasad is a system of multiple dishes, never treated as homogeneous food."""
    res = MahaprasadTempleDecomposer.decompose()
    assert res.total_components_detected == 8

    dish_names = [it.name for it in res.items]
    assert "Kanika" in dish_names
    assert "Khechudi" in dish_names
    assert "Temple Dalma" in dish_names
    assert "Mahaprasad Besara" in dish_names
    assert "Puri Jagannath Khaja" in dish_names
    assert res.total_edible_weight_g >= 600.0


def test_bengali_and_odia_thali_decomposers():
    """Section 33: Multi-course Bengali and Odia Thalis decomposed into individual items."""
    b_thali = BengaliThaliDecomposer.decompose({"has_fish": True})
    assert b_thali.total_components_detected >= 7
    b_names = [it.name for it in b_thali.items]
    assert "Shukto" in b_names
    assert "Aloo Posto" in b_names
    assert "Mishti Doi" in b_names

    o_thali = OdiaThaliDecomposer.decompose()
    assert o_thali.total_components_detected >= 7
    o_names = [it.name for it in o_thali.items]
    assert "Odia Dalma" in o_names
    assert "Santula" in o_names
    assert "Chhena Poda" in o_names


def test_packaging_filter_rule():
    """Verifies exclusion of non-food objects (earthen pots, sal leaf dona, banana leaves)."""
    raw_detections = [
        {"label": "earthen_clay_bhar", "confidence": 0.95},
        {"label": "sal_leaf_dona", "confidence": 0.90},
        {"label": "WB_SWEET_MISHTI_DOI", "confidence": 0.94},
        {"label": "banana_leaf", "confidence": 0.98}
    ]
    filtered = PackagingFilter.filter_non_food_detections(raw_detections)
    assert len(filtered) == 1
    assert filtered[0]["label"] == "WB_SWEET_MISHTI_DOI"


# =============================================================================
# 7. PORTIONS, COUNTS & FAT ESTIMATION (Sections 41, 42, 50, 53)
# =============================================================================

def test_countable_food_detector():
    """Section 42: Count * average unit weight = total weight."""
    # Luchi (4 pieces * 30g = 120g)
    l_res = CountableFoodDetector.estimate_countable_weight("WB_BREAD_LUCHI", 4)
    assert l_res.is_countable is True
    assert l_res.count == 4
    assert l_res.total_estimated_weight_g == 120.0

    # Litti (2 pieces * 75g = 150g)
    lit_res = CountableFoodDetector.estimate_countable_weight("BR_BREAD_LITTI", 2)
    assert lit_res.is_countable is True
    assert lit_res.total_estimated_weight_g == 150.0


def test_portion_tiers_and_reference_scaler():
    """Sections 41 & 50: Discrete tiers and reference object scale calibration."""
    tier_wt, label = EastIndianPortionClassifier.match_rice_tier(192.0)
    assert tier_wt == 200.0
    assert "200g" in label

    # Scale calibration with katori
    cal = PortionReferenceScaler.calibrate_scale("katori", 170.0)
    assert cal["has_reference_object"] is True
    assert cal["reference_true_dimension_cm"] == 8.5
    assert cal["portion_confidence_penalty"] == 0.0

    # Fallback without reference
    cal_none = PortionReferenceScaler.calibrate_scale(None, None)
    assert cal_none["has_reference_object"] is False
    assert cal_none["portion_confidence_penalty"] > 0.0


def test_visual_fat_sheen_estimator():
    """Section 53: Visual fat levels: low, medium, high, unknown."""
    high_fat = VisualFatSheenEstimator.estimate_fat_level({"mustard_oil_float": True})
    assert high_fat["fat_level"] == "high"
    assert high_fat["fat_factor_multiplier"] > 1.0

    low_fat = VisualFatSheenEstimator.estimate_fat_level({"is_steamed_or_boiled": True})
    assert low_fat["fat_level"] == "low"
    assert low_fat["fat_factor_multiplier"] < 1.0


# =============================================================================
# 8. SECTION 63 STANDARDIZED MODEL OUTPUT & CALORIE RANGES (Sections 52, 63)
# =============================================================================

def test_section_63_standardized_model_output_schema():
    """Section 63: Full 20-field model output compliance and uncertainty calorie ranges."""
    out = EastIndianRecipeNutritionCalculator.calculate_dish_nutrition(
        food_identifier="WB_FISH_SHORSHE_ILISH",
        visual_cues={"mustard_oil_float": True}
    )
    assert isinstance(out, Section63ModelOutput)
    assert out.food_name == "Shorshe Ilish"
    assert out.canonical_food_id == "WB_FISH_SHORSHE_ILISH"
    assert out.region == "East India"
    assert out.state == "West Bengal"
    assert out.regional_variant == "Shorshe Ilish"
    assert out.vegetarian is False
    assert out.calories_kcal.min < out.calories_kcal.expected < out.calories_kcal.max
    assert out.protein_g > 0.0
    assert out.fat_g > 0.0
    assert out.confidence >= 0.90
    assert out.user_confirmation_required is False


def test_east_indian_unknown_class_fallback():
    """Section 48 & Quality Rule 18: If visual evidence is insufficient, return UNKNOWN with user confirmation."""
    out = EastIndianRecipeNutritionCalculator.calculate_dish_nutrition(
        food_identifier="completely_unrecognized_east_dish_xyz"
    )
    assert out.canonical_food_id == "EAST_INDIAN_UNKNOWN"
    assert out.user_confirmation_required is True
    assert out.confidence <= 0.30
    assert "High" in out.uncertainty


# =============================================================================
# 9. UNIFIED PRODUCTION ORCHESTRATOR ROUTING
# =============================================================================

def test_production_orchestrator_east_indian_methods():
    """Verifies that production_orchestrator exposes and executes all East Indian dish and platter pipelines."""
    # Single dish evaluation
    dish_res = production_orchestrator.analyze_east_indian_dish("OD_SWEET_CHHENA_PODA")
    assert dish_res.canonical_food_id == "OD_SWEET_CHHENA_PODA"
    assert dish_res.state == "Odisha"

    # Bengali Thali
    b_res = production_orchestrator.analyze_bengali_thali()
    assert b_res.platter_type == "thali"

    # Litti Chokha
    l_res = production_orchestrator.analyze_litti_chokha()
    assert l_res.platter_type == "litti_platter"

    # Dahibara Aloodum
    d_res = production_orchestrator.analyze_dahibara_aloodum()
    assert d_res.platter_type == "street_chaat"

    # Mahaprasad
    m_res = production_orchestrator.analyze_mahaprasad()
    assert m_res.platter_type == "temple_mahaprasad"
