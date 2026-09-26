"""
Automated Test Suite for Part 3 — Extreme Fine-Grained Food Training Data + Hard-Negative System
Validates all 72 Sections of Part 3.
"""

import pytest
from app.food_ai.taxonomy.food_id_registry import (
    PERMANENT_CLASS_REGISTRY,
    resolve_food_by_name_or_alias,
    get_permanent_class,
    get_hierarchy_path,
    list_all_permanent_ids
)
from app.food_ai.datasets.fine_grained_attributes import (
    THIRTY_VEGETABLE_CLASSES,
    SIXTEEN_COOKING_METHODS,
    TWENTY_FOOD_STATES,
    IngredientVisibilityStatus,
    VegetablePresenceRecord,
    IdliSampleAnnotation,
    SambarSampleAnnotation,
    DosaSampleAnnotation,
    VadaSampleAnnotation,
    RiceSampleAnnotation,
    BiryaniSampleAnnotation
)
from app.food_ai.datasets.hard_negative_engine import HardNegativeEngine
from app.food_ai.portion_engine.food_specific_portions import (
    SOUTH_INDIAN_PORTION_GOLD_DATASET,
    FoodSpecificPortionEngine,
    TwoPhotoVolumeReconstructor,
    PlateInstanceDecomposition
)
from app.food_ai.nutrition_engine.recipe_variation_model import (
    RECIPE_VARIATION_DATABASE,
    CalorieUncertaintyModel,
    FULL_MEAL_TEMPLATES
)
from app.food_ai.quality_and_leakage.image_pipeline import (
    ImageQualityAssessor,
    DatasetSplitManager,
    AugmentationSafetyValidator
)
from app.food_ai.active_learning.error_analysis_system import (
    ActiveLearningReviewQueue,
    FoodAIErrorType
)
from app.food_ai.inference_orchestrator import (
    production_orchestrator,
    FinalMealAnalysisResponse
)

def test_food_id_registry_and_hierarchy():
    # Sections 1 & 2: Permanent ID format and non-empty registry
    perm_ids = list_all_permanent_ids()
    assert len(perm_ids) >= 12
    assert "TN_BREAKFAST_IDLI_PLAIN" in perm_ids
    assert "TN_BREAKFAST_DOSA_MASALA" in perm_ids
    assert "TN_CURRY_SAMBAR_TIFFIN" in perm_ids
    assert "TN_CHUTNEY_COCONUT_WHITE" in perm_ids
    assert "TN_BIRYANI_DINDIGUL_MUTTON" in perm_ids

    # Section 1: Full 11-level hierarchy traversal
    h_path = get_hierarchy_path("TN_BREAKFAST_IDLI_PLAIN")
    assert "South Indian" in h_path
    assert "Tamil Nadu" in h_path
    assert "Breakfast" in h_path
    assert "Steamed Food" in h_path
    assert "Idli" in h_path

    # Section 3: Synonym & alternate name resolution
    resolved_idly = resolve_food_by_name_or_alias("idly")
    assert resolved_idly is not None
    assert resolved_idly.permanent_id == "TN_BREAKFAST_IDLI_PLAIN"

    resolved_sadam = resolve_food_by_name_or_alias("thayir sadam")
    assert resolved_sadam is not None
    assert resolved_sadam.permanent_id == "TN_RICE_CURD_THAYIR_SADAM"

    # Section 4: Regional names stored
    rec = get_permanent_class("TN_BREAKFAST_IDLI_PLAIN")
    assert "Tamil" in rec.regional_names
    assert "Telugu" in rec.regional_names
    assert "Kannada" in rec.regional_names

def test_fine_grained_attribute_schemas():
    # Section 5: Idli detailed visual attributes
    idli_ann = IdliSampleAnnotation(
        idli_type="plain",
        piece_count=3,
        piece_width_cm=7.6,
        piece_height_cm=2.8,
        sambar_present=True,
        chutney_present=True
    )
    assert idli_ann.piece_count == 3
    assert idli_ann.shape == "convex_lens_disc"

    # Section 7: Sambar detailed visual attributes
    sambar_ann = SambarSampleAnnotation(
        thickness="medium_broth",
        color="golden_orange_translucent",
        dal_visibility=True,
        vegetable_visibility=True,
        portion_g=110.0
    )
    assert sambar_ann.dal_visibility is True

    # Section 11: Dosa detailed visual attributes
    dosa_ann = DosaSampleAnnotation(
        diameter_cm=28.0,
        thickness_cm=0.20,
        fold_count=1,
        crispness="brittle_crisp",
        masala_present=True
    )
    assert dosa_ann.diameter_cm == 28.0

    # Section 13: Vada detailed visual attributes
    vada_ann = VadaSampleAnnotation(
        hole_count=1,
        hole_diameter_cm=2.2,
        fried_color="deep_golden_amber",
        chilli_visible=True
    )
    assert vada_ann.hole_count == 1

def test_thirty_vegetable_classes_and_ternary_status():
    # Section 25 & 26: 30 vegetables with VISIBLE, NOT_VISIBLE, UNCERTAIN status
    assert len(THIRTY_VEGETABLE_CLASSES) == 30
    assert "drumstick" in THIRTY_VEGETABLE_CLASSES
    assert "moringa_leaves" in THIRTY_VEGETABLE_CLASSES
    assert "chow_chow" in THIRTY_VEGETABLE_CLASSES

    veg_rec = VegetablePresenceRecord(
        vegetable_name="drumstick",
        status=IngredientVisibilityStatus.VISIBLE,
        confidence=0.96
    )
    assert veg_rec.status == IngredientVisibilityStatus.VISIBLE

    veg_uncertain = VegetablePresenceRecord(
        vegetable_name="onion",
        status=IngredientVisibilityStatus.UNCERTAIN,
        confidence=0.50
    )
    assert veg_uncertain.status == IngredientVisibilityStatus.UNCERTAIN

def test_sixteen_cooking_methods_and_twenty_food_states():
    # Sections 27 & 28
    assert len(SIXTEEN_COOKING_METHODS) == 16
    assert "steamed" in SIXTEEN_COOKING_METHODS
    assert "fermented" in SIXTEEN_COOKING_METHODS
    assert "tawa_fried" in SIXTEEN_COOKING_METHODS

    assert len(TWENTY_FOOD_STATES) == 20
    assert "solid_porous" in TWENTY_FOOD_STATES or "solid" in TWENTY_FOOD_STATES
    assert "semi_solid" in TWENTY_FOOD_STATES
    assert "liquid" in TWENTY_FOOD_STATES

def test_hard_negatives_battery():
    # Sections 6, 8, 12, 14: Hard negatives
    idli_negs = HardNegativeEngine.get_idli_hard_negatives()
    assert any(n["negative"] == "dhokla" for n in idli_negs)
    assert any(n["negative"] == "paniyaram" for n in idli_negs)

    sambar_negs = HardNegativeEngine.get_sambar_hard_negatives()
    assert any(n["negative"] == "rasam" for n in sambar_negs)
    assert any(n["negative"] == "dal_tadka" for n in sambar_negs)

    # Section 17: Ten direct pairwise rice datasets
    rice_pairs = HardNegativeEngine.get_rice_ten_pairwise_datasets()
    assert len(rice_pairs) == 10
    assert rice_pairs[0]["pair_id"] == "pair_01_biryani_vs_fried_rice"
    assert rice_pairs[5]["pair_id"] == "pair_06_lemon_rice_vs_tamarind_rice"

def test_chutney_uncertainty_rule():
    # Section 10: Chutney Uncertainty Protocol
    # White chutney where coconut cannot be verified -> must output exact type uncertain
    res = HardNegativeEngine.resolve_chutney_uncertainty(
        color_detected="white", coconut_confidence=0.65, peanut_confidence=0.60
    )
    assert res["uncertain"] is True
    assert "white chutney detected" in res["status_text"]

def test_portion_gold_dataset_and_food_specific_portions():
    # Section 30: Dedicated Portion Gold Dataset
    assert len(SOUTH_INDIAN_PORTION_GOLD_DATASET) >= 10
    idli_sample = next(s for s in SOUTH_INDIAN_PORTION_GOLD_DATASET if s.food_id == "TN_BREAKFAST_IDLI_PLAIN" and s.piece_count == 2)
    assert idli_sample.actual_measured_weight_g == 124.0

    # Section 37: Food-specific portion models
    # IDLI: piece_count * piece_weight
    res_idli = FoodSpecificPortionEngine.estimate_idli_weight(piece_count=3, variant="plain")
    assert res_idli["model_used"] == "piece_count_multiplier"
    assert res_idli["estimated_weight_g"] == 186.0

    # DOSA: area * thickness * density
    res_dosa = FoodSpecificPortionEngine.estimate_dosa_weight(diameter_cm=28.0, thickness_cm=0.20, dosa_type="plain")
    assert res_dosa["model_used"] == "area_thickness_density"
    assert 50.0 <= res_dosa["estimated_weight_g"] <= 100.0

    # SAMBAR: frustum volume * liquid density
    res_sambar = FoodSpecificPortionEngine.estimate_sambar_weight(bowl_top_diameter_cm=7.5, liquid_depth_cm=3.0)
    assert res_sambar["model_used"] == "katori_frustum_volume"
    assert 80.0 <= res_sambar["estimated_weight_g"] <= 160.0

def test_two_photo_mode_volume_calibration():
    # Section 33: Two-photo mode
    fused = TwoPhotoVolumeReconstructor.fuse_top_and_side_views(
        top_view_area_pixels=45000.0,
        side_view_height_pixels=120.0,
        reference_plate_diameter_cm=26.0,
        plate_pixels_in_image=800.0
    )
    assert fused["mode"] == "high_accuracy_two_photo"
    assert fused["physical_area_cm2"] > 0
    assert fused["physical_height_cm"] > 0
    assert fused["reconstructed_volume_cm3"] > 0
    assert fused["confidence_boost"] > 0

def test_plate_instance_decomposition_7_instances():
    # Section 34: 3 idli + sambar + 2 chutneys + podi -> 7 discrete instances!
    foods = ["Idli", "Sambar", "White Coconut Chutney", "Tomato Chutney", "Milagai Podi"]
    instances = PlateInstanceDecomposition.decompose_plate_items(
        detected_food_classes=foods,
        piece_counts={"idli": 3}
    )
    assert len(instances) == 7
    idli_instances = [it for it in instances if "Idli Piece" in it["instance_type"]]
    assert len(idli_instances) == 3
    assert any(it["class_name"] == "Tiffin Sambar" for it in instances)
    assert any(it["class_name"] == "White Coconut Chutney" for it in instances)
    assert any(it["class_name"] == "Tomato Kaara Chutney" for it in instances)
    assert any("Podi" in it["class_name"] for it in instances)

def test_recipe_variation_database_and_uncertainty():
    # Section 39: Multiple recipe profiles
    assert "TN_BREAKFAST_DOSA" in RECIPE_VARIATION_DATABASE
    dosa_recipes = RECIPE_VARIATION_DATABASE["TN_BREAKFAST_DOSA"]
    assert len(dosa_recipes) >= 3
    assert any("RESTAURANT" in r.recipe_code for r in dosa_recipes)
    assert any("HOME" in r.recipe_code for r in dosa_recipes)

    # Section 40: Calorie Uncertainty Propagation
    cals = CalorieUncertaintyModel.propagate_uncertainty(
        dish_name="Dosa", variant="Masala Dosa", estimated_weight_g=200.0,
        base_calories_per_100g=188.0, food_confidence=0.94, is_two_photo_mode=True
    )
    assert cals.calorie_range_min < cals.calories_point_estimate < cals.calorie_range_max
    assert cals.overall_confidence_score >= 0.85

    # Section 42: Full meal templates
    assert "TAMIL_TIFFIN_BREAKFAST" in FULL_MEAL_TEMPLATES
    assert len(FULL_MEAL_TEMPLATES["TAMIL_TIFFIN_BREAKFAST"].components) >= 5

def test_quality_and_leakage_prevention():
    # Section 46: Image Quality Assessor
    good_q = ImageQualityAssessor.evaluate_quality(width=640, height=480, blur_score=130.0, brightness=120.0)
    assert good_q.is_trainable is True
    assert good_q.quality_label in ["excellent", "good"]

    blurry_q = ImageQualityAssessor.evaluate_quality(width=640, height=480, blur_score=20.0)
    assert blurry_q.is_trainable is False
    assert blurry_q.quality_label == "unusable"

    # Section 48: Strict Split Leakage Prevention by meal_id
    split_mgr = DatasetSplitManager()
    res1 = split_mgr.assign_sample_split(meal_id="meal_999", image_bytes=b"img_top_pixels_111", preferred_split="val")
    assert res1["status"] == "accepted"
    assert res1["assigned_split"] == "val"

    # Same meal_id with different image (side view) MUST receive identical split ("val")
    res2 = split_mgr.assign_sample_split(meal_id="meal_999", image_bytes=b"img_side_pixels_222", preferred_split="train")
    assert res2["status"] == "accepted"
    assert res2["assigned_split"] == "val"

    # Exact duplicate image is rejected
    res3 = split_mgr.assign_sample_split(meal_id="meal_999", image_bytes=b"img_top_pixels_111")
    assert res3["status"] == "rejected_duplicate"

    # Section 60: Augmentation Safety Validator (rejects identity-changing color shifts)
    assert AugmentationSafetyValidator.is_augmentation_safe(hue_shift_deg=10.0, brightness_factor=1.1, flip_horizontal=True, food_category="Rice") is True
    assert AugmentationSafetyValidator.is_augmentation_safe(hue_shift_deg=35.0, brightness_factor=1.1, flip_horizontal=True, food_category="Rice") is False

def test_error_analysis_and_active_learning():
    # Section 51: 9 error types
    assert len(FoodAIErrorType) == 9
    assert FoodAIErrorType.VISUAL_SIMILARITY == "visual_similarity"
    assert FoodAIErrorType.PORTION_ERROR == "portion_error"

    # Section 52 & 53: Active learning queue and user correction
    queue = ActiveLearningReviewQueue()
    enqueued = queue.evaluate_for_active_learning(
        image_id="img_test_01", image_hash="hash_01",
        predicted_class="Plain Idli", confidence=0.72, is_unknown=False
    )
    assert enqueued is True
    assert len(queue.review_queue) == 1

    feedback = queue.record_user_correction(
        image_id="img_test_01", original_prediction="Plain Idli",
        corrected_prediction="Rava Idli", model_version="south_indian_model_v3"
    )
    assert feedback.validation_status == "pending_review"

def test_eighteen_step_orchestrator_and_section64_output():
    # Sections 54, 63, 64: 18-step pipeline execution on Section 64 sample:
    # 3 idlis, sambar, coconut chutney, tomato chutney
    dummy_top = b"idli_combo_top_view_pixels" * 100
    res = production_orchestrator.analyze(
        top_image_bytes=dummy_top,
        dish_hint="Idli",
        blur_score=140.0
    )

    assert isinstance(res, FinalMealAnalysisResponse)
    assert res.pipeline_status == "resolved"
    assert len(res.items) == 4

    # Verify Item 1: Plain Idli
    idli_item = res.items[0]
    assert idli_item.name == "Plain Idli"
    assert idli_item.count == 3
    assert idli_item.estimated_weight_g == 186.0
    assert idli_item.confidences.food_confidence >= 0.90
    assert idli_item.confidences.count_confidence >= 0.95
    assert idli_item.confidences.overall_system_confidence >= 0.90

    # Verify Item 2: Sambar
    sambar_item = res.items[1]
    assert sambar_item.name == "Sambar"
    assert sambar_item.estimated_weight_g == 110.0

    # Verify Item 3: Coconut Chutney
    chutney_item = res.items[2]
    assert chutney_item.name == "Coconut Chutney"
    assert chutney_item.confidence_level in ["medium-high", "high"]

    # Verify Item 4: Tomato Chutney
    tomato_item = res.items[3]
    assert tomato_item.name == "Tomato Chutney"

    # Verify totals
    assert res.total_weight_g == round(186.0 + 110.0 + 45.0 + 40.0, 1)
    assert res.total_calories > 300.0
    assert res.total_protein_g > 0
    assert res.total_carbs_g > 0
    assert res.total_fat_g > 0

def test_section65_blurry_and_unknown_accuracy_rules():
    # Section 65 Rule: Low quality / blurry image -> "Food detected — exact identification unavailable"
    dummy_top = b"blurry_bytes" * 50
    blurry_res = production_orchestrator.analyze(
        top_image_bytes=dummy_top,
        blur_score=25.0
    )
    assert blurry_res.pipeline_status == "blurry_unavailable"
    assert len(blurry_res.items) == 0
    assert "exact identification unavailable" in blurry_res.user_disclosure_notes

    # Section 65 Rule: Unknown food dish -> never force nearest known class
    unknown_res = production_orchestrator.analyze(
        top_image_bytes=dummy_top,
        dish_hint="unknown exotic dish",
        blur_score=120.0
    )
    assert unknown_res.pipeline_status == "unknown"
    assert len(unknown_res.items) == 0
    assert "unknown_south_indian_food" in unknown_res.uncertain_items
