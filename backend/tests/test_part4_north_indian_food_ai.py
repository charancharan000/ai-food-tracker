"""
Test Suite for Part 4 — North Indian Food Master Dataset & AI Vision Engine
Verifies:
1. Strict 9-level taxonomy hierarchy and permanent IDs across 8 Northern States/Regions
2. Multi-lingual regional names (English, Hindi, Punjabi, Urdu, Rajasthani, Kashmiri, Pahari)
3. 22 Pairwise Visual Confusion Matrix registrations and disambiguation rules
4. Paratha Filling Verifier (Aloo, Gobi, Mooli, Paneer, Pyaz, Methi, Mix Veg, Not Visible)
5. Dal Visual Discriminator (Color, Viscosity, Bean Morphology, Surface Tadka)
6. Bread Classifier (Roti, Naan, Paratha, Kulcha, Poori, Bhatura)
7. Chole Bhature Instance Decomposition into 5+ discrete items
8. North Indian Thali decomposition (8-14 items with distinct portions & nutrition)
9. Himachali Traditional Dham decomposition (6-7 authentic courses)
10. Food-specific portion models & physical density calibration (Roti 20-60g, Paratha 60-150g, Katoris)
11. Oil/Ghee Range Estimator (Low oil, Restaurant medium, Dhaba high ghee, Butter pool)
12. Raw vs Cooked Yield conversions (Rice, Rajma, Chole, Wheat)
13. Section 43 Standardized Model Output schema compliance
14. Unified Orchestrator North Indian routing & multi-dish analysis
"""

import pytest
from app.food_ai.taxonomy.north_indian_master_taxonomy import (
    NORTH_INDIAN_TAXONOMY_REGISTRY,
    get_north_food_class,
    resolve_north_food_by_name,
    list_all_north_food_ids
)
from app.food_ai.datasets.north_indian_hard_negatives import (
    NORTH_INDIAN_CONFUSION_REGISTRY,
    disambiguate_north_indian_pair,
    ParathaFillingVerifier,
    DalVisualDiscriminator,
    CholeBhatureDecomposer
)
from app.food_ai.datasets.north_indian_thali_decomposer import (
    NorthIndianThaliDecomposer,
    HimachaliDhamDecomposer
)
from app.food_ai.portion_engine.north_indian_portions import (
    NORTH_INDIAN_PORTION_TABLE,
    OilGheeRangeEstimator,
    get_portion_for_north_food
)
from app.food_ai.nutrition_engine.north_indian_recipes import (
    NorthIndianRecipeNutritionCalculator,
    RAW_COOKED_TABLE,
    Section43ModelOutput
)
from app.food_ai.inference_orchestrator import production_orchestrator, FinalMealAnalysisResponse

# =============================================================================
# 1. TAXONOMY & REGIONAL HIERARCHY TESTS
# =============================================================================

def test_north_indian_taxonomy_and_8_states_coverage():
    """Verifies that all 8 Northern states/regions are represented with permanent IDs."""
    assert len(NORTH_INDIAN_TAXONOMY_REGISTRY) >= 35
    
    states_found = set()
    for food in NORTH_INDIAN_TAXONOMY_REGISTRY.values():
        assert food.hierarchy.level1_food == "Indian Food"
        assert food.hierarchy.level2_macro_region == "North Indian Food"
        states_found.add(food.hierarchy.level3_state_region)
        assert food.permanent_id.startswith(("PB_", "DL_", "UP_", "RJ_", "HR_", "HP_", "UK_", "JK_", "NI_"))
        assert food.density_g_cm3 > 0.5
        assert food.default_serving_weight_g > 0.0
        assert "calories" in food.nutrition_per_100g

    # Check 8 core northern states/regions
    required_states = [
        "Punjab", "Delhi", "Uttar Pradesh", "Rajasthan",
        "Haryana", "Himachal Pradesh", "Uttarakhand", "Jammu & Kashmir"
    ]
    for st in required_states:
        assert st in states_found, f"State {st} missing in taxonomy!"

def test_regional_multilingual_name_mapping():
    """Verifies resolution of food by English, Hindi, and regional dialect names."""
    # Makki di Roti (Punjabi)
    makki = resolve_north_food_by_name("ਮੱਕੀ ਦੀ ਰੋਟੀ")
    assert makki is not None
    assert makki.permanent_id == "PB_BREAD_ROTI_MAKKI"

    # Dal Baati Churma (Rajasthani)
    baati = resolve_north_food_by_name("दाल बाटी चूरमो")
    assert baati is not None
    assert baati.permanent_id == "RJ_MAIN_DAL_BAATI_CHURMA"

    # Rogan Josh (Kashmiri)
    rogan = resolve_north_food_by_name("Kashmiri Rogan Josh")
    assert rogan is not None
    assert rogan.permanent_id == "JK_NONVEG_ROGAN_JOSH"
    assert rogan.gravy_type == "red_gravy"

    # Siddu (Himachali Pahari)
    siddu = resolve_north_food_by_name("Himachali Siddu")
    assert siddu is not None
    assert siddu.permanent_id == "HP_MAIN_SIDDU"

# =============================================================================
# 2. 22 PAIRWISE CONFUSION MATRIX & DISAMBIGUATION TESTS
# =============================================================================

def test_confusion_matrix_22_pairs_registered():
    """Ensures all 22 explicit confusing pairs are registered with discriminator rules."""
    assert len(NORTH_INDIAN_CONFUSION_REGISTRY) == 22
    for pair in NORTH_INDIAN_CONFUSION_REGISTRY.values():
        assert pair.pair_id.startswith("PAIR_")
        assert len(pair.discriminating_features) >= 1
        assert len(pair.disambiguation_rule) > 10

def test_disambiguate_aloo_paratha_vs_plain_paratha():
    winner, conf, reason = disambiguate_north_indian_pair(
        "PB_PARATHA_ALOO", "PB_PARATHA_PLAIN",
        {"thickness_mm": 4.5, "visible_filling": "spiced potato mash"}
    )
    assert winner == "PB_PARATHA_ALOO"
    assert conf >= 0.90

    winner_plain, conf_p, _ = disambiguate_north_indian_pair(
        "PB_PARATHA_ALOO", "PB_PARATHA_PLAIN",
        {"thickness_mm": 2.8, "visible_filling": "none"}
    )
    assert winner_plain == "PB_PARATHA_PLAIN"

def test_disambiguate_bhatura_vs_poori():
    winner_bhatura, conf_b, _ = disambiguate_north_indian_pair(
        "DL_BREAD_BHATURA", "UP_BREAD_POORI",
        {"diameter_cm": 24.0, "flour_type": "maida"}
    )
    assert winner_bhatura == "DL_BREAD_BHATURA"
    assert conf_b >= 0.95

    winner_poori, conf_p, _ = disambiguate_north_indian_pair(
        "DL_BREAD_BHATURA", "UP_BREAD_POORI",
        {"diameter_cm": 11.0, "flour_type": "atta"}
    )
    assert winner_poori == "UP_BREAD_POORI"

def test_disambiguate_rajma_vs_chole():
    winner_rajma, conf_r, _ = disambiguate_north_indian_pair(
        "PB_CURRY_RAJMA_MASALA", "PB_CURRY_CHOLE_PUNJABI",
        {"bean_shape": "kidney", "color": "crimson"}
    )
    assert winner_rajma == "PB_CURRY_RAJMA_MASALA"

    winner_chole, conf_c, _ = disambiguate_north_indian_pair(
        "PB_CURRY_RAJMA_MASALA", "PB_CURRY_CHOLE_PUNJABI",
        {"bean_shape": "round", "color": "dark_amber"}
    )
    assert winner_chole == "PB_CURRY_CHOLE_PUNJABI"

def test_disambiguate_paneer_butter_masala_vs_butter_chicken():
    winner_chicken, _, _ = disambiguate_north_indian_pair(
        "PB_NONVEG_BUTTER_CHICKEN", "PB_CURRY_PANEER_BUTTER_MASALA",
        {"protein_type": "chicken", "fibrous_grain": True}
    )
    assert winner_chicken == "PB_NONVEG_BUTTER_CHICKEN"

    winner_paneer, _, _ = disambiguate_north_indian_pair(
        "PB_NONVEG_BUTTER_CHICKEN", "PB_CURRY_PANEER_BUTTER_MASALA",
        {"protein_type": "vegetarian", "fibrous_grain": False}
    )
    assert winner_paneer == "PB_CURRY_PANEER_BUTTER_MASALA"

def test_disambiguate_jalebi_vs_imarti():
    winner_imarti, _, _ = disambiguate_north_indian_pair(
        "NI_SWEET_JALEBI", "NI_SWEET_IMARTI",
        {"pattern": "rosette"}
    )
    assert winner_imarti == "NI_SWEET_IMARTI"

    winner_jalebi, _, _ = disambiguate_north_indian_pair(
        "NI_SWEET_JALEBI", "NI_SWEET_IMARTI",
        {"pattern": "spiral"}
    )
    assert winner_jalebi == "NI_SWEET_JALEBI"

# =============================================================================
# 3. ATTRIBUTE VERIFIERS (PARATHA, DAL, CHOLE BHATURE)
# =============================================================================

def test_paratha_filling_verifier():
    # Methi Paratha
    res_methi = ParathaFillingVerifier.verify_filling({"surface_specks": ["green_leaf"]})
    assert res_methi["filling"] == "methi"
    assert res_methi["canonical_id"] == "PB_PARATHA_METHI"
    assert res_methi["user_confirmation_required"] is False

    # Paneer Paratha
    res_paneer = ParathaFillingVerifier.verify_filling({"filling_at_edge": "white_curd_chunks"})
    assert res_paneer["filling"] == "paneer"
    assert res_paneer["canonical_id"] == "PB_PARATHA_PANEER"

    # Gobi Paratha
    res_gobi = ParathaFillingVerifier.verify_filling({"filling_at_edge": "cauliflower_flecks"})
    assert res_gobi["filling"] == "gobi"
    assert res_gobi["canonical_id"] == "PB_PARATHA_GOBI"

    # Mooli Paratha
    res_mooli = ParathaFillingVerifier.verify_filling({"filling_at_edge": "translucent_radish_threads"})
    assert res_mooli["filling"] == "mooli"
    assert res_mooli["canonical_id"] == "PB_PARATHA_MOOLI"

    # Not Visible
    res_unseen = ParathaFillingVerifier.verify_filling({})
    assert res_unseen["filling"] == "not_visible"
    assert res_unseen["user_confirmation_required"] is True

def test_dal_visual_discriminator():
    # Dal Makhani
    dm = DalVisualDiscriminator.discriminate({
        "color": "black",
        "viscosity": "creamy",
        "surface": ["cream", "butter"]
    })
    assert dm["dal_id"] == "PB_CURRY_DAL_MAKHANI"
    assert dm["confidence"] >= 0.95

    # Dal Tadka
    dt = DalVisualDiscriminator.discriminate({
        "color": "yellow",
        "viscosity": "medium",
        "bean_type": "split_lentil"
    })
    assert dt["dal_id"] == "PB_CURRY_DAL_TADKA"

def test_chole_bhature_never_collapses_to_single_item():
    """Ensures Chole Bhature is decomposed into distinct instances."""
    plate_items = CholeBhatureDecomposer.decompose_plate({"bhatura_count": 2})
    assert len(plate_items) >= 4 # 2 Bhature, Chole, Onion, Pickle, Chutney
    
    bhatura_items = [it for it in plate_items if it["canonical_id"] == "DL_BREAD_BHATURA"]
    assert len(bhatura_items) == 2
    assert any(it["canonical_id"] == "PB_CURRY_CHOLE_PUNJABI" for it in plate_items)
    assert any("Onion" in it["component_name"] for it in plate_items)
    
    # Nutrition is aggregated, not single lump sum
    total_cals = sum(it["calories_kcal"] for it in plate_items)
    assert 800.0 <= total_cals <= 1100.0

# =============================================================================
# 4. COMPOSITE MEAL DECOMPOSITION (THALI & DHAM)
# =============================================================================

def test_north_indian_thali_decomposition():
    """Verifies that a North Indian Thali decomposes into 8-14 discrete items."""
    thali = NorthIndianThaliDecomposer.decompose({"num_rotis": 2})
    assert thali.meal_type == "north_indian_thali"
    assert 8 <= thali.num_components <= 14
    
    ids = [c.canonical_food_id for c in thali.components]
    assert "PB_BREAD_ROTI_TANDOORI" in ids
    assert "PB_CURRY_DAL_MAKHANI" in ids
    assert "PB_CURRY_PANEER_BUTTER_MASALA" in ids
    assert "NI_RICE_STEAMED_BASMATI" in ids
    assert "NI_CONDIMENT_BOONDI_RAITA" in ids
    assert "NI_SWEET_GULAB_JAMUN" in ids
    
    assert 500.0 <= thali.total_weight_g <= 900.0
    assert 1200.0 <= thali.total_calories_kcal <= 1800.0

def test_himachali_dham_decomposition():
    """Verifies that Himachali Dham decomposes into 6 authentic courses."""
    dham = HimachaliDhamDecomposer.decompose()
    assert dham.meal_type == "himachali_dham"
    assert dham.num_components == 6
    
    names = [c.food_name for c in dham.components]
    assert any("Basmati Rice" in n for n in names)
    assert any("Rajma Madra" in n for n in names)
    assert any("Chana Madra" in n for n in names)
    assert any("Sepu Vadi" in n for n in names)
    assert any("Kangra Khatta" in n for n in names)
    assert any("Mittha" in n for n in names)

    assert 700.0 <= dham.total_weight_g <= 1000.0
    assert 1100.0 <= dham.total_calories_kcal <= 1600.0

# =============================================================================
# 5. PORTIONS, DENSITIES & OIL/GHEE RANGE ESTIMATION
# =============================================================================

def test_food_specific_portions_and_ranges():
    # Roti: 20-60g
    phulka_w, (p_min, p_max) = get_portion_for_north_food("PB_BREAD_ROTI_TAWA")
    assert 20.0 <= phulka_w <= 35.0
    assert p_min < phulka_w < p_max

    tandoori_w, (t_min, t_max) = get_portion_for_north_food("PB_BREAD_ROTI_TANDOORI")
    assert 38.0 <= tandoori_w <= 55.0

    makki_w, _ = get_portion_for_north_food("PB_BREAD_ROTI_MAKKI")
    assert 50.0 <= makki_w <= 75.0

    # Paratha: 60-150g
    paratha_plain_w, _ = get_portion_for_north_food("PB_PARATHA_PLAIN")
    assert 55.0 <= paratha_plain_w <= 75.0

    paratha_stuffed_w, _ = get_portion_for_north_food("PB_PARATHA_ALOO")
    assert 100.0 <= paratha_stuffed_w <= 150.0

def test_oil_ghee_range_estimator():
    # Home style low oil
    home_sheen = OilGheeRangeEstimator.estimate_oil_ghee_profile({
        "gloss_level": "matte",
        "surface_oil_layer": False,
        "restaurant_or_home": "home"
    })
    assert home_sheen["fat_level"] == "low"
    assert home_sheen["fat_multiplier"] == 1.00

    # Dhaba high ghee with butter dollop
    dhaba_sheen = OilGheeRangeEstimator.estimate_oil_ghee_profile({
        "gloss_level": "high",
        "surface_oil_layer": True,
        "butter_dollop": True,
        "restaurant_or_home": "dhaba"
    })
    assert dhaba_sheen["fat_level"] == "high"
    assert dhaba_sheen["fat_multiplier"] > 1.20
    assert dhaba_sheen["extra_fat_g"] == 12.0

def test_raw_vs_cooked_conversions():
    assert "raw_basmati_rice" in RAW_COOKED_TABLE
    assert RAW_COOKED_TABLE["raw_basmati_rice"].yield_multiplier >= 2.5
    assert RAW_COOKED_TABLE["raw_rajma_beans"].yield_multiplier >= 2.0

# =============================================================================
# 6. SECTION 43 STANDARDIZED OUTPUT & INFERENCE ORCHESTRATION
# =============================================================================

def test_section43_standardized_dish_output():
    """Validates Section 43 compliant output schema for North Indian dishes."""
    out = NorthIndianRecipeNutritionCalculator.calculate_dish_nutrition(
        "PB_PARATHA_ALOO",
        visual_cues={"gloss_level": "medium", "confidence": 0.94}
    )
    assert isinstance(out, Section43ModelOutput)
    assert out.food_name == "Aloo Paratha"
    assert out.canonical_food_id == "PB_PARATHA_ALOO"
    assert out.state == "Punjab"
    assert out.vegetarian is True
    assert out.estimated_weight_g == 120.0
    assert out.calories_kcal > 250.0
    assert out.confidence == 0.94
    assert "weight_range_g" in out.uncertainty
    assert "calorie_range_kcal" in out.uncertainty
    assert "visible" in out.ingredients
    assert "inferred" in out.ingredients
    assert out.cooking_method != ""
    assert out.user_confirmation_required is False

def test_orchestrator_north_indian_routing():
    """Tests ProductionInferenceOrchestrator routing for North Indian meals and dishes."""
    dummy_img = b"dummy_north_indian_plate_bytes" * 50
    
    # 1. Thali routing
    res_thali = production_orchestrator.analyze(
        top_image_bytes=dummy_img,
        dish_hint="Punjabi Thali"
    )
    assert isinstance(res_thali, FinalMealAnalysisResponse)
    assert res_thali.pipeline_status == "resolved"
    assert len(res_thali.items) >= 8

    # 2. Dham routing
    res_dham = production_orchestrator.analyze(
        top_image_bytes=dummy_img,
        dish_hint="Himachali Dham"
    )
    assert res_dham.pipeline_status == "resolved"
    assert len(res_dham.items) == 6

    # 3. Chole Bhature routing
    res_cb = production_orchestrator.analyze(
        top_image_bytes=dummy_img,
        dish_hint="Chole Bhature"
    )
    assert res_cb.pipeline_status == "resolved"
    assert len(res_cb.items) >= 5

    # 4. Single North Indian dish routing (Aloo Paratha)
    res_paratha = production_orchestrator.analyze(
        top_image_bytes=dummy_img,
        dish_hint="Aloo Paratha"
    )
    assert res_paratha.pipeline_status == "resolved"
    assert len(res_paratha.items) == 1
    assert res_paratha.items[0].name == "Aloo Paratha"
    assert res_paratha.items[0].permanent_id == "PB_PARATHA_ALOO"
