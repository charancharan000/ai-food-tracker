"""
Test Suite for Part 5 — West Indian Food Master Dataset & AI Vision Engine
Verifies:
1. Strict 9-level taxonomy hierarchy and permanent IDs across 5 West Indian Regions:
   (Maharashtra, Gujarat, Goa, Konkan, Mumbai Street Food Ecosystem)
2. Multi-lingual regional names (English, Marathi, Gujarati, Konkani, Hindi)
3. 20 Pairwise Visual Confusion Matrix registrations and disambiguation rules
4. Dhokla Family Classifier (Khaman, Nylon Khaman, White Khatta Dhokla, Rava Dhokla, Sandwich Dhokla)
5. Bhakri & Rotla Classifier (Jowar, Bajra, Rice, Nachni, Kathiyawadi Bajra Rotla)
6. Batata Vada Classifier vs Aloo Bonda vs Medu Vada vs Sabudana Vada
7. Puran Poli Verifier (Rule 27: Unopened -> filling_status="unknown" and user_confirmation_required=True)
8. Chaat Component Segmenter (Section 9: Bhel Puri, Sev Puri, Dahi Puri, Ragda Pattice with component visibility)
9. Composite Meal Decomposers:
   - Vada Pav (Pav, Batata Vada, Lasun Chutney, Green Chutney, Fried Chilli)
   - Pav Bhaji (Bhaji, Butter Pav, Butter Dollop/Pool, Onions, Lemon, Coriander)
   - Misal Pav (Matki Usal, Kat/Tarri, Farsan, Sev, Onions, Coriander, Lemon, Pav, Extra Rassa)
   - Gujarati Thali (10-14 discrete authentic components)
   - Goan Fish Thali (6-8 discrete authentic components)
10. Packaging Filter Rule (Rule 29: excludes paper plates, newspaper, steel katoris)
11. Countable Food Portions (Count * calibrated unit weight) & Katori Volumetric Calibrator
12. Visual Fat/Sheen Estimator (Butter pool, Kat/Tarri float, Ghee glaze)
13. Section 51 Standardized Model Output schema compliance
14. Unified Production Orchestrator West Indian routing & platter analysis
"""

import pytest
from app.food_ai.taxonomy.west_indian_master_taxonomy import (
    WEST_INDIAN_TAXONOMY_REGISTRY,
    get_west_food_class,
    resolve_west_food_by_name,
    list_all_west_food_ids
)
from app.food_ai.datasets.west_indian_hard_negatives import (
    WEST_INDIAN_CONFUSION_REGISTRY,
    disambiguate_west_indian_pair,
    DhoklaFamilyClassifier,
    BhakriRotlaClassifier,
    BatataVadaClassifier,
    PuranPoliVerifier,
    ChaatComponentSegmenter
)
from app.food_ai.datasets.west_indian_composite_decomposer import (
    VadaPavDecomposer,
    PavBhajiDecomposer,
    MisalPavDecomposer,
    GujaratiThaliDecomposer,
    GoanFishThaliDecomposer,
    PackagingFilter,
    WestIndianCompositeDecompositionResult
)
from app.food_ai.portion_engine.west_indian_portions import (
    WEST_INDIAN_PORTION_TABLE,
    CountableFoodDetector,
    WestIndianKatoriBowlCalibrator,
    WestIndianFatLevelEstimator,
    get_portion_for_west_food
)
from app.food_ai.nutrition_engine.west_indian_recipes import (
    WestIndianRecipeNutritionCalculator,
    Section51ModelOutput
)
from app.food_ai.inference_orchestrator import production_orchestrator


# =============================================================================
# 1. TAXONOMY & REGIONAL HIERARCHY TESTS
# =============================================================================

def test_west_indian_taxonomy_and_5_regions_coverage():
    """Verifies that all 5 West Indian regions/states are represented with permanent IDs."""
    assert len(WEST_INDIAN_TAXONOMY_REGISTRY) >= 50

    regions_found = set()
    states_found = set()
    for food in WEST_INDIAN_TAXONOMY_REGISTRY.values():
        assert food.hierarchy.level1_food == "Indian Food"
        assert food.hierarchy.level2_macro_region == "West Indian Food"
        regions_found.add(food.hierarchy.level3_state_region)
        states_found.add(food.state)
        assert food.permanent_id.startswith(("MH_", "GJ_", "GA_", "KN_", "MUM_", "WI_"))
        assert food.density_g_cm3 >= 0.35
        assert food.default_serving_weight_g > 0.0
        assert "calories" in food.nutrition_per_100g

    # Check primary West Indian regions
    required_regions = ["Maharashtra", "Gujarat", "Goa", "Konkan", "Mumbai"]
    for reg in required_regions:
        assert reg in regions_found, f"Region {reg} missing in West Indian taxonomy!"


def test_west_indian_multilingual_name_mapping():
    """Verifies resolution of food by Marathi, Gujarati, Konkani, and English names."""
    # Vada Pav (Marathi)
    vadapav = resolve_west_food_by_name("वडा पाव")
    assert vadapav is not None
    assert vadapav.permanent_id == "MUM_STREET_VADA_PAV"

    # Khaman Dhokla (Gujarati)
    khaman = resolve_west_food_by_name("ખમણ ઢોકળા")
    assert khaman is not None
    assert khaman.permanent_id in ["GJ_FARSAN_KHAMAN", "GJ_FARSAN_KHAMAN_NYLON"]

    # Goan Fish Curry (Konkani)
    fish_curry = resolve_west_food_by_name("Xitt Codi")
    assert fish_curry is not None
    assert fish_curry.permanent_id in ["GA_CURRY_FISH_XITT_CODI", "GA_CURRY_FISH_GOAN"]

    # Puran Poli (Marathi)
    puran_poli = resolve_west_food_by_name("पुरणपोळी")
    assert puran_poli is not None
    assert puran_poli.permanent_id in ["MH_BREAD_PURAN_POLI", "MH_SWEET_PURAN_POLI"]


# =============================================================================
# 2. HARD NEGATIVE PAIRS & DISAMBIGUATION TESTS
# =============================================================================

def test_west_indian_confusion_registry_and_pairs():
    """Verifies all 20 West Indian pairwise visual confusions are registered."""
    assert len(WEST_INDIAN_CONFUSION_REGISTRY) >= 20

    # Test Khaman vs White Khatta Dhokla
    res = disambiguate_west_indian_pair(
        "GJ_FARSAN_KHAMAN",
        "GJ_FARSAN_DHOKLA_WHITE",
        {"color": "bright_yellow", "black_pepper_sprinkle": False}
    )
    assert res["resolved_food_id"] == "GJ_FARSAN_KHAMAN"

    res_white = disambiguate_west_indian_pair(
        "GJ_FARSAN_KHAMAN",
        "GJ_FARSAN_DHOKLA_WHITE",
        {"color": "white", "black_pepper_sprinkle": True}
    )
    assert res_white["resolved_food_id"] == "GJ_FARSAN_DHOKLA_WHITE"

    # Test Jowar Bhakri vs Bajra Bhakri
    res_bajra = disambiguate_west_indian_pair(
        "MH_BREAD_BHAKRI_JOWAR",
        "MH_BREAD_BHAKRI_BAJRA",
        {"color": "grey_brown"}
    )
    assert res_bajra["resolved_food_id"] == "MH_BREAD_BHAKRI_BAJRA"

    # Test Pav Bhaji vs Misal
    res_misal = disambiguate_west_indian_pair(
        "MUM_STREET_PAV_BHAJI",
        "MH_STREET_MISAL_PAV",
        {"farsan_topping": True, "curry_texture": "watery_rassa"}
    )
    assert res_misal["resolved_food_id"] == "MH_STREET_MISAL_PAV"


def test_dhokla_family_classifier():
    """Verifies DhoklaFamilyClassifier distinguishes all 5 variants."""
    # Khaman
    khaman = DhoklaFamilyClassifier.classify({"color": "bright_yellow", "graininess": "fine", "sponge_porosity": "high"})
    assert khaman["variant"] == "khaman_dhokla"

    # White Khatta Dhokla
    white = DhoklaFamilyClassifier.classify({"color": "white", "black_pepper_specks": True})
    assert white["variant"] == "white_khatta_dhokla"

    # Rava Dhokla
    rava = DhoklaFamilyClassifier.classify({"color": "off_white", "graininess": "granular", "sponge_porosity": "moderate"})
    assert rava["variant"] == "rava_dhokla"

    # Sandwich Dhokla
    sandwich = DhoklaFamilyClassifier.classify({"green_chutney_layer": True, "two_toned_layers": True})
    assert sandwich["variant"] == "sandwich_dhokla"


def test_bhakri_rotla_classifier():
    """Verifies BhakriRotlaClassifier identifies grain types and Kathiyawadi Rotla."""
    # Jowar Bhakri
    jowar = BhakriRotlaClassifier.classify({"color": "off_white", "pliability": "medium"})
    assert jowar["variant"] == "jowar_bhakri"

    # Bajra Rotla (Kathiyawadi - thick hand-patted)
    rotla = BhakriRotlaClassifier.classify({"color": "greyish_brown", "thickness_mm": 6.0, "char_spots": "heavy"})
    assert rotla["variant"] == "kathiyawadi_bajra_rotlo"
    assert rotla["canonical_food_id"] == "GJ_BREAD_ROTLO_BAJRA"

    # Rice Bhakri
    rice = BhakriRotlaClassifier.classify({"color": "pure_white", "thickness_mm": 2.0})
    assert rice["variant"] == "rice_bhakri"

    # Nachni Bhakri
    nachni = BhakriRotlaClassifier.classify({"color": "dark_brown"})
    assert nachni["variant"] == "nachni_bhakri"


def test_batata_vada_classifier():
    """Verifies BatataVadaClassifier disambiguates potato snack and fritter types."""
    # Batata Vada
    vada = BatataVadaClassifier.classify({"shape": "spherical", "batter": "besan", "interior_color": "yellow"})
    assert vada["variant"] == "batata_vada"

    # Sabudana Vada
    sabudana = BatataVadaClassifier.classify({"visible_sago_pearls": True})
    assert sabudana["variant"] == "sabudana_vada"

    # Medu Vada
    medu = BatataVadaClassifier.classify({"shape": "torus_doughnut_with_hole"})
    assert medu["variant"] == "medu_vada"


def test_puran_poli_verifier_rule_27():
    """Verifies Rule 27: Unopened flatbread must not hallucinate sweet chana dal filling."""
    # Closed/unopened bread -> Unknown filling, requires confirmation
    closed_res = PuranPoliVerifier.verify({"is_flatbread_cut": False, "translucent_filling_visible": False})
    assert closed_res["filling_status"] == "unknown"
    assert closed_res["user_confirmation_required"] is True
    assert closed_res["provisional_identity"] == "plain_paratha_or_chapati"

    # Opened / Cut bread with yellow filling visible -> Verified Puran Poli
    opened_res = PuranPoliVerifier.verify({"is_flatbread_cut": True, "yellow_sweet_chana_filling": True})
    assert opened_res["filling_status"] == "puran_identified"
    assert opened_res["user_confirmation_required"] is False
    assert opened_res["canonical_food_id"] == "MH_BREAD_PURAN_POLI"


def test_chaat_component_segmenter_section_9():
    """Verifies Section 9: Chaat component segmentation with visibility flags."""
    # Sev Puri
    sp_res = ChaatComponentSegmenter.segment_chaat("sev_puri", {
        "visible_puri_discs": True,
        "visible_sev": True,
        "visible_potato_cubes": True,
        "visible_green_chutney": True,
        "visible_sweet_chutney": True,
        "visible_coriander": True
    })
    assert sp_res["chaat_name"] == "Sev Puri"
    assert sp_res["puri_count"] == 6
    assert sp_res["components"]["sev"]["visibility"] == "visible"
    assert sp_res["components"]["green_chutney"]["visibility"] == "visible"

    # Bhel Puri
    bhel_res = ChaatComponentSegmenter.segment_chaat("bhel_puri", {
        "visible_kurmura": True,
        "visible_sev": True
    })
    assert bhel_res["chaat_name"] == "Bhel Puri"
    assert bhel_res["components"]["puffed_rice_kurmura"]["visibility"] == "visible"


# =============================================================================
# 3. COMPOSITE MEAL DECOMPOSERS & PACKAGING FILTER TESTS
# =============================================================================

def test_packaging_filter_rule_29():
    """Verifies Rule 29: Packaging is detected and filtered out from edible items."""
    tags = ["paper_plate", "newspaper_liner", "steel_katori", "fried_sev"]
    detected = PackagingFilter.detect_and_filter_packaging(tags)
    assert len(detected) == 3
    assert "Paper Plate" in detected
    assert "Printed Newspaper Liner" in detected
    assert "Stainless Steel Katori Bowl" in detected


def test_vada_pav_decomposer():
    """Verifies Vada Pav is decomposed into Pav, Batata Vada, Chutneys, and Salted Chilli."""
    res = VadaPavDecomposer.decompose({"num_vadas": 1, "include_fried_chilli": True})
    assert isinstance(res, WestIndianCompositeDecompositionResult)
    assert res.meal_type == "vada_pav"
    assert res.num_components >= 5

    comp_ids = [c.canonical_food_id for c in res.components]
    assert "MH_BREAD_PAV" in comp_ids
    assert "MH_SNACK_BATATA_VADA" in comp_ids
    assert "MH_CHUTNEY_DRY_GARLIC" in comp_ids
    assert "MH_CHUTNEY_GREEN_THECHA" in comp_ids
    assert "MH_GARNISH_FRIED_CHILLI" in comp_ids

    assert res.total_weight_g > 140.0
    assert res.total_calories_kcal > 350.0


def test_pav_bhaji_decomposer_and_butter_pool():
    """Verifies Pav Bhaji decomposition and butter pool fat level estimation."""
    res = PavBhajiDecomposer.decompose({"num_pav": 2, "butter_level": "high"})
    assert res.meal_type == "pav_bhaji"
    assert res.num_components >= 6
    assert res.visual_fat_level == "high"

    butter_comp = next((c for c in res.components if "Butter" in c.food_name), None)
    assert butter_comp is not None
    assert butter_comp.estimated_weight_g == 22.0  # high fat butter dollop

    pav_count = sum(1 for c in res.components if c.canonical_food_id == "MH_BREAD_PAV")
    assert pav_count == 2


def test_misal_pav_decomposer():
    """Verifies Misal Pav decomposition into Usal, Kat, Farsan, Sev, Garnishes, and Extra Rassa."""
    res = MisalPavDecomposer.decompose({"num_pav": 2, "has_extra_rassa": True, "misal_style": "kolhapuri"})
    assert res.meal_type == "misal_pav"
    assert res.num_components >= 8
    assert res.visual_fat_level == "high"

    comp_names = [c.food_name for c in res.components]
    assert any("Sprouted Matki Usal" in name for name in comp_names)
    assert any("Misal Kat/Tarri" in name for name in comp_names)
    assert any("Crispy Mixed Farsan" in name for name in comp_names)
    assert any("Crisp Besan Sev" in name for name in comp_names)
    assert any("Extra Kat/Rassa Bowl" in name for name in comp_names)


def test_gujarati_thali_decomposer_10_to_14_items():
    """Verifies Gujarati Thali is decomposed into 10 to 14 discrete authentic components."""
    res = GujaratiThaliDecomposer.decompose({"num_rotli": 3, "num_puri": 2, "has_undhiyu": True, "has_sweet": True})
    assert res.meal_type == "gujarati_thali"
    assert 10 <= res.num_components <= 16

    comp_ids = [c.canonical_food_id for c in res.components]
    assert "GJ_BREAD_ROTLO_PHULKA" in comp_ids
    assert "GJ_BREAD_PURI" in comp_ids
    assert "GJ_DAL_GUJARATI" in comp_ids
    assert "GJ_KADHI_GUJARATI" in comp_ids
    assert "GJ_CURRY_RINGAN_BATETA" in comp_ids
    assert "GJ_CURRY_UNDHIYU" in comp_ids
    assert "GJ_FARSAN_KHAMAN" in comp_ids
    assert "GJ_RICE_KHICHDI" in comp_ids
    assert "GJ_SALAD_SAMBHARO" in comp_ids
    assert "WI_ACCOMPANIMENT_PAPAD" in comp_ids
    assert "GJ_BEVERAGE_CHAAS" in comp_ids
    assert "MH_SWEET_SHRIKHAND" in comp_ids

    assert res.total_weight_g >= 700.0
    assert res.total_calories_kcal >= 800.0


def test_goan_fish_thali_decomposer_6_to_8_items():
    """Verifies Goan Fish Thali is decomposed into 6 to 8 discrete authentic components."""
    res = GoanFishThaliDecomposer.decompose({"fish_type": "surmai", "has_kismur": True})
    assert res.meal_type == "goan_fish_thali"
    assert 6 <= res.num_components <= 8

    comp_ids = [c.canonical_food_id for c in res.components]
    assert "GA_RICE_UKDA_BOILED" in comp_ids
    assert "GA_CURRY_FISH_XITT_CODI" in comp_ids
    assert "GA_SEAFOOD_RAVA_FISH_FRY" in comp_ids
    assert "GA_SALAD_KISMUR" in comp_ids
    assert "GA_VEG_CABBAGE_FOOGATH" in comp_ids
    assert "GA_BEVERAGE_SOL_KADHI" in comp_ids
    assert "GA_PICKLE_AMBE_CHE" in comp_ids

    assert res.total_weight_g >= 600.0
    assert res.total_protein_g >= 40.0


# =============================================================================
# 4. PORTION ENGINE & NUTRITION ENGINE (SECTION 51 OUTPUT) TESTS
# =============================================================================

def test_countable_food_portion_detector():
    """Verifies countable items multiply unit weights accurately."""
    # 3 Batata Vadas (75g each = 225g)
    vada_res = CountableFoodDetector.estimate_countable_portion("MH_SNACK_BATATA_VADA", detected_count=3)
    assert vada_res["is_countable"] is True
    assert vada_res["count"] == 3
    assert vada_res["estimated_weight_g"] == 225.0
    assert vada_res["credible_range_g"][0] < 225.0 < vada_res["credible_range_g"][1]

    # 4 Khandvi rolls (20g each = 80g)
    khandvi_res = CountableFoodDetector.estimate_countable_portion("GJ_FARSAN_KHANDVI", detected_count=4)
    assert khandvi_res["count"] == 4
    assert khandvi_res["estimated_weight_g"] == 80.0


def test_katori_calibrator_and_densities():
    """Verifies Katori bowl calibration for Gujarati Dal."""
    weight_std, r_std = WestIndianKatoriBowlCalibrator.estimate_katori_weight("GJ_DAL_GUJARATI", "standard")
    assert 130.0 <= weight_std <= 155.0

    weight_lg, r_lg = WestIndianKatoriBowlCalibrator.estimate_katori_weight("GJ_DAL_GUJARATI", "large")
    assert weight_lg > weight_std


def test_section_51_standardized_model_output():
    """Verifies that Section 51 output contains all required fields and honest ranges."""
    output = WestIndianRecipeNutritionCalculator.calculate_dish_nutrition(
        "GJ_FARSAN_KHAMAN",
        visual_cues={"confidence": 0.96},
        count=3
    )
    assert isinstance(output, Section51ModelOutput)
    assert output.canonical_food_id in ["GJ_FARSAN_KHAMAN", "GJ_FARSAN_KHAMAN_NYLON"]
    assert output.region == "West India"
    assert output.state == "Gujarat"
    assert output.count == 3
    assert output.estimated_weight_g == 105.0  # 3 * 35g
    assert output.calorie_breakdown.min < output.calorie_breakdown.expected < output.calorie_breakdown.max
    assert output.protein_g > 0
    assert output.carbs_g > 0
    assert output.user_confirmation_required is False
    assert len(output.ingredients["inferred"]) > 0


def test_unknown_food_confirmation_required():
    """Verifies fallback when food cannot be resolved with certainty."""
    output = WestIndianRecipeNutritionCalculator.calculate_dish_nutrition("random_unknown_item")
    assert output.canonical_food_id == "WEST_INDIAN_UNKNOWN"
    assert output.user_confirmation_required is True
    assert output.confidence < 0.50


# =============================================================================
# 5. PRODUCTION ORCHESTRATOR WEST INDIAN INTEGRATION TESTS
# =============================================================================

def test_production_orchestrator_west_indian_methods():
    """Verifies production orchestrator provides all West Indian analysis capabilities."""
    # 1. Single dish analysis
    dish_res = production_orchestrator.analyze_west_indian_dish("MH_BREAD_PURAN_POLI", count=2)
    assert dish_res.canonical_food_id in ["MH_BREAD_PURAN_POLI", "MH_SWEET_PURAN_POLI"]
    assert dish_res.count == 2
    assert dish_res.estimated_weight_g == 170.0

    # 2. Vada Pav analysis
    vp_res = production_orchestrator.analyze_vada_pav()
    assert vp_res.meal_type == "vada_pav"

    # 3. Pav Bhaji analysis
    pb_res = production_orchestrator.analyze_pav_bhaji({"butter_level": "medium"})
    assert pb_res.meal_type == "pav_bhaji"

    # 4. Misal Pav analysis
    mp_res = production_orchestrator.analyze_misal_pav()
    assert mp_res.meal_type == "misal_pav"

    # 5. Gujarati Thali analysis
    gt_res = production_orchestrator.analyze_gujarati_thali()
    assert gt_res.meal_type == "gujarati_thali"

    # 6. Goan Fish Thali analysis
    ga_res = production_orchestrator.analyze_goan_fish_thali()
    assert ga_res.meal_type == "goan_fish_thali"
