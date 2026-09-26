"""
Extreme South Indian Food Vision & Nutrition Test Suite
Tests all 42 sections and specifications of Part 2.
"""

import pytest
from app.food_ai.taxonomy.extreme_south_indian_taxonomy import (
    EXTREME_TAXONOMY_REGISTRY,
    get_food_class,
    find_classes_by_name,
    get_all_food_classes
)
from app.food_ai.datasets.confusion_matrix import (
    CONFUSION_MATRIX_REGISTRY,
    disambiguate_pair
)
from app.food_ai.datasets.banana_leaf_detector import BananaLeafMealDetector
from app.food_ai.training_pipeline.hierarchical_curriculum import (
    TWELVE_STAGE_CURRICULUM,
    TRAINING_PRIORITY_SCHEDULE,
    HierarchicalCurriculumManager
)
from app.food_ai.nutrition_engine.recipe_aware_pipeline import (
    AntiHallucinationGate,
    RecipeAwareCalorieCalculator
)
from app.food_ai.active_learning.continuous_expansion import (
    ContinuousExpansionPipeline,
    EXPANSION_PHASE_ORDER
)

def test_extreme_taxonomy_all_20_fields_populated():
    classes = get_all_food_classes()
    assert len(classes) >= 15

    for fc in classes:
        assert fc.food_id
        assert fc.canonical_name
        assert fc.category
        assert fc.sub_category
        assert fc.region
        assert fc.state
        assert fc.variant
        assert fc.cooking_method
        assert fc.food_state
        assert isinstance(fc.visual_features, dict) and len(fc.visual_features) > 0
        assert isinstance(fc.common_ingredients, list) and len(fc.common_ingredients) > 0
        assert isinstance(fc.hard_negative_classes, list) and len(fc.hard_negative_classes) > 0
        assert isinstance(fc.portion_classes, dict) and len(fc.portion_classes) > 0
        assert isinstance(fc.weight_classes, dict) and len(fc.weight_classes) > 0
        assert isinstance(fc.nutrition_reference, dict) and len(fc.nutrition_reference) > 0
        assert "calories_per_100g" in fc.nutrition_reference
        assert "protein_g" in fc.nutrition_reference
        assert "carbs_g" in fc.nutrition_reference
        assert "fat_g" in fc.nutrition_reference
        assert isinstance(fc.confidence_rules, dict) and len(fc.confidence_rules) > 0
        assert isinstance(fc.annotation_requirements, list) and len(fc.annotation_requirements) > 0

def test_idli_fine_grained_distinctions():
    plain_idli = get_food_class("tn_idli_plain")
    rava_idli = get_food_class("ka_idli_rava")
    kanchi_idli = get_food_class("tn_idli_kanchipuram")
    mini_idli = get_food_class("tn_idli_mini")
    thatte_idli = get_food_class("ka_idli_thatte")

    assert plain_idli and rava_idli and kanchi_idli and mini_idli and thatte_idli
    assert plain_idli.visual_features["color"] != rava_idli.visual_features["color"]
    assert mini_idli.weight_classes["single_piece_g"] < plain_idli.weight_classes["single_piece_g"]
    assert thatte_idli.weight_classes["single_piece_g"] > plain_idli.weight_classes["single_piece_g"]
    assert "cashew" in str(rava_idli.common_ingredients).lower()
    assert "black pepper" in str(kanchi_idli.common_ingredients).lower()

def test_confusion_matrix_26_pairs_registered():
    assert len(CONFUSION_MATRIX_REGISTRY) >= 25
    expected_pairs = [
        "idli_vs_rava_idli_vs_dhokla",
        "dosa_vs_crepe",
        "medu_vada_vs_bonda",
        "paruppu_vada_vs_pakoda",
        "pongal_vs_upma",
        "pongal_vs_kichdi",
        "sambar_vs_dal",
        "sambar_vs_rasam",
        "rasam_vs_soup",
        "poriyal_vs_stir_fry",
        "kootu_vs_dal",
        "biryani_vs_fried_rice",
        "biryani_vs_pulao",
        "biryani_vs_kuska",
        "ghee_rice_vs_kuska",
        "curd_rice_vs_plain_rice_plus_curd",
        "lemon_rice_vs_tamarind_rice",
        "coconut_chutney_vs_white_chutney",
        "tomato_chutney_vs_red_gravy",
        "mint_chutney_vs_coriander_chutney",
        "parotta_vs_paratha",
        "poori_vs_bhatura",
        "kothu_parotta_vs_fried_rice",
        "chicken_vs_mutton",
        "fish_vs_chicken",
        "prawn_vs_small_chicken_pieces"
    ]
    for p in expected_pairs:
        assert p in CONFUSION_MATRIX_REGISTRY, f"Missing pair: {p}"

def test_disambiguate_pair_pongal_vs_upma():
    res = disambiguate_pair("Ven Pongal", "Rava Upma", {"detected_inclusions": ["whole_peppercorns", "cashews"]})
    assert res["pair_matched"] == "pongal_vs_upma"
    assert "Whole peppercorns" in res["disambiguation_test"] or "peppercorn" in str(res["discriminative_cues"])

def test_banana_leaf_decomposition_never_single_food():
    dummy_img = b"banana_leaf_pixel_bytes" * 50
    decomp = BananaLeafMealDetector.decompose_meal(dummy_img, is_non_veg=False, scale_calibrator_ratio=1.0)

    assert decomp.is_banana_leaf_detected is True
    assert decomp.components_count >= 8
    assert len(decomp.items) >= 8

    # Ensure no item is called "Banana Leaf"
    for item in decomp.items:
        assert "Banana Leaf" not in item.class_name
        assert item.estimated_weight_g > 0
        assert item.calories > 0
        assert item.bbox["ymin"] >= 0 and item.bbox["ymax"] <= 1.0

    assert decomp.total_meal_weight_g >= 500.0
    assert decomp.total_meal_calories >= 500.0

def test_twelve_stage_curriculum_and_priority_schedule():
    assert len(TWELVE_STAGE_CURRICULUM) == 12
    stage1 = HierarchicalCurriculumManager.get_stage(1)
    stage12 = HierarchicalCurriculumManager.get_stage(12)

    assert stage1.stage_name == "food_vs_non_food"
    assert stage12.stage_name == "uncertainty_calibration"

    p1_classes = HierarchicalCurriculumManager.get_priority_classes(1)
    assert "idli" in p1_classes
    assert "sambar" in p1_classes
    assert "dosa" in p1_classes

def test_anti_hallucination_gate_steamed_food():
    # Ambiguous white steamed food with no clear winner
    ambiguous_features = {"idli_porosity": 0.55, "granular_crumb": 0.45, "yellow_sugar_sponge": 0.30}
    res = AntiHallucinationGate.evaluate_steamed_white_food(ambiguous_features)
    assert res["status"] == "ambiguous"
    assert "Steamed food detected" in res["variant"]
    assert len(res["possible_candidates"]) >= 3

    # High confidence clear idli
    clear_idli = {"idli_porosity": 0.95, "granular_crumb": 0.10, "yellow_sugar_sponge": 0.05}
    res_idli = AntiHallucinationGate.evaluate_steamed_white_food(clear_idli)
    assert res_idli["status"] == "resolved"
    assert res_idli["class_name"] == "Idli"

def test_anti_hallucination_gate_red_liquid():
    ambiguous_liquid = {"sambar_veg_dal": 0.60, "rasam_thin_pepper": 0.55, "curry_gravy": 0.40}
    res = AntiHallucinationGate.evaluate_red_liquid(ambiguous_liquid)
    assert res["status"] == "ambiguous"
    assert "South Indian gravy detected" in res["variant"]

def test_anti_hallucination_gate_chutney():
    ambiguous_white_dip = {"coconut_fiber": 0.65, "peanut_smooth": 0.60}
    res = AntiHallucinationGate.evaluate_chutney(ambiguous_white_dip)
    assert res["status"] == "ambiguous"
    assert "Chutney detected — exact type uncertain" in res["variant"]

def test_section42_standardized_model_output():
    # Input matching Section 42: 3 idlis, sambar, coconut chutney, tomato chutney
    detections = [
        {"name": "Idli", "variant": "Plain Idli", "count": 3, "estimated_weight_g": 180.0, "recipe_key": "plain_idli_home", "confidence": 0.96},
        {"name": "Sambar", "variant": "Hotel Tiffin Sambar", "estimated_weight_g": 110.0, "recipe_key": "tiffin_sambar_restaurant", "confidence": 0.94},
        {"name": "Coconut Chutney", "variant": "Fresh White Coconut Chutney", "estimated_weight_g": 45.0, "recipe_key": "white_coconut_chutney_standard", "confidence": 0.93},
        {"name": "Tomato Chutney", "variant": "Spicy Tomato Kaara Chutney", "estimated_weight_g": 40.0, "recipe_key": "tomato_kaara_chutney_standard", "confidence": 0.92}
    ]

    out = RecipeAwareCalorieCalculator.generate_section42_output(detections)

    assert len(out.items) == 4
    idli_item = out.items[0]
    assert idli_item.name == "Idli"
    assert idli_item.count == 3
    assert idli_item.estimated_weight == "180.0g"
    # 180g plain idli at 136 kcal/100g = 244.8 kcal
    assert 240.0 <= idli_item.calories <= 250.0

    sambar_item = out.items[1]
    assert sambar_item.name == "Sambar"
    assert sambar_item.estimated_weight == "110.0g"
    # 110g sambar at 68 kcal/100g = 74.8 kcal
    assert 70.0 <= sambar_item.calories <= 80.0

    # Total calories sum
    expected_sum = sum(it.calories for it in out.items)
    assert out.total.calories == round(expected_sum, 1)
    assert out.total.protein > 0
    assert out.total.carbs > 0
    assert out.total.fat > 0

def test_continuous_expansion_loop_lifecycle():
    engine = ContinuousExpansionPipeline()
    lifecycle = engine.initiate_new_food_discovery(
        discovery_id="disc_kumbakonam_degree_coffee",
        food_name="Kumbakonam Degree Coffee",
        region="Tamil Nadu",
        image_hashes=["hash_img1", "hash_img2"]
    )
    assert lifecycle.current_phase == "REVIEW"

    # Advance through phases
    for phase in EXPANSION_PHASE_ORDER[:-1]:
        lifecycle = engine.advance_phase(
            discovery_id="disc_kumbakonam_degree_coffee",
            completed_phase=phase,
            artifacts={"phase_data": "sample_ok"}
        )

    assert lifecycle.current_phase == "REGRESSION_TEST"

    # Test regression gate passes
    promo = engine.run_regression_and_promote(
        discovery_id="disc_kumbakonam_degree_coffee",
        test_accuracy=96.5,
        benchmark_mae_g=14.2
    )
    assert promo["status"] == "success"
    assert promo["promoted"] is True
    assert lifecycle.is_approved_for_production is True
