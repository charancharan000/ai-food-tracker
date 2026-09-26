"""
Test Suite for Part 7 — Northeast India Food Master Dataset & AI Vision Engine
Verifies:
1. Strict 9-level taxonomy hierarchy and permanent IDs across all 8 Northeast Indian States:
   (Assam, Meghalaya, Manipur, Mizoram, Nagaland, Tripura, Arunachal Pradesh, Sikkim)
2. Multi-lingual regional names (English, Assamese, Khasi, Manipuri, Mizo, Nagamese, Kokborok, Nepali)
3. Northeast Rice-Meat Discriminator (Jadoh vs Galho vs Sawhchiar vs Pulao vs Khichdi)
4. Fermented Soybean Discriminator (Axone vs Tungrymbai vs Kinema)
5. Mashed Vegetable & Fermented Fish Discriminator (Aloo Pitika vs Eromba vs Mosdeng vs Singju)
6. Wood-Smoked Meat Verifier (Smoke ring & cured amber fat vs fried or charred meat)
7. Momo & Thukpa Cross-State Classifiers with count, occlusion, and variant detection
8. Tripuri Mui Borok Meal Decomposer (Section 29: component decomposition, never monolithic 800 kcal)
9. Assamese Thali, Meghalaya Jadoh, Naga Platter, and Sikkim Meal Decomposers
10. Packaging & Vessel Invariance (bell-metal kanh, banana leaf, bamboo cooking pipe)
11. Visual Fat Estimator for Northeast Cooking (pork belly fat vs oil-free boiled broth)
12. Section 86 Standardized Model Output Schema compliance & Calorie Ranges
13. Section 87 No-Hallucination Rule & Unknown Fallback (NORTHEAST_INDIAN_UNKNOWN)
14. Unified Production Orchestrator Northeast Indian routing
"""

import pytest
from app.food_ai.taxonomy.northeast_indian_master_taxonomy import (
    NORTHEAST_TAXONOMY_REGISTRY,
    get_northeast_food_class,
    resolve_northeast_food_by_name,
    list_all_northeast_food_ids
)
from app.food_ai.datasets.northeast_indian_hard_negatives import (
    NORTHEAST_CONFUSION_REGISTRY,
    disambiguate_northeast_pair,
    NortheastRiceMeatDiscriminator,
    FermentedSoybeanDiscriminator,
    MashedVegetableChutneyDiscriminator,
    SmokedMeatVerifier
)
from app.food_ai.datasets.northeast_indian_composite_decomposer import (
    AssameseThaliDecomposer,
    MeghalayaJadohPlatterDecomposer,
    NagaPlatterDecomposer,
    TripuriMuiBorokDecomposer,
    SikkimMealDecomposer,
    ManipuriMealDecomposer,
    MizoMealDecomposer,
    ArunachalMealDecomposer,
    NortheastPackagingFilter,
    NortheastCompositeDecompositionResult
)
from app.food_ai.portion_engine.northeast_indian_portions import (
    NortheastCountableDetector,
    NortheastFatLevelEstimator,
    NortheastPortionTiers
)
from app.food_ai.nutrition_engine.northeast_indian_recipes import (
    NortheastRecipeNutritionCalculator,
    Section74SingleFoodJSON,
    Section78UnknownFoodOutput,
    Section82ModelOutput,
    Section86ModelOutput
)
from app.food_ai.inference_orchestrator import production_orchestrator


# =============================================================================
# 1. TAXONOMY & REGIONAL HIERARCHY TESTS
# =============================================================================

def test_northeast_indian_taxonomy_and_8_states_coverage():
    """Verifies that all 8 Northeast Indian states are represented with permanent IDs."""
    assert len(NORTHEAST_TAXONOMY_REGISTRY) >= 20

    states_found = set()
    for food in NORTHEAST_TAXONOMY_REGISTRY.values():
        assert food.hierarchy.level1_food == "Indian Food"
        assert food.hierarchy.level2_macro_region == "Northeast Indian Food"
        states_found.add(food.state)
        assert food.canonical_food_id.startswith(("AS_", "ML_", "MN_", "MZ_", "NL_", "TR_", "AR_", "SK_", "NE_", "NORTHEAST_"))
        assert food.density_g_cm3 >= 0.40
        assert food.default_serving_weight_g > 0.0

    required_states = [
        "Assam", "Meghalaya", "Manipur", "Mizoram",
        "Nagaland", "Tripura", "Arunachal Pradesh", "Sikkim"
    ]
    for st in required_states:
        assert st in states_found, f"State {st} missing in Northeast Indian taxonomy!"



def test_northeast_multilingual_name_mapping():
    """Verifies resolution of food by Assamese, Khasi, Manipuri, Mizo, Nagamese, Kokborok, Nepali names."""
    # Assamese: Masor Tenga
    tenga = resolve_northeast_food_by_name("মাছৰ টেঙা")
    assert tenga is not None
    assert tenga.canonical_food_id == "AS_FISH_MASOR_TENGA"

    # Khasi: Ja Doh
    jadoh = resolve_northeast_food_by_name("Ja Doh")
    assert jadoh is not None
    assert jadoh.canonical_food_id == "ML_RICE_JADOH_PORK"

    # Manipuri: Eromba
    eromba = resolve_northeast_food_by_name("ইৰোম্বা")
    assert eromba is not None
    assert eromba.canonical_food_id == "MN_CHUTNEY_EROMBA"

    # Mizo: Bai
    bai = resolve_northeast_food_by_name("Bai")
    assert bai is not None
    assert bai.canonical_food_id == "MZ_STEW_BAI"

    # Nagamese: Axone
    axone = resolve_northeast_food_by_name("अखुनी")
    assert axone is not None
    assert axone.canonical_food_id == "NL_FERMENTED_AXONE"

    # Kokborok: Chakhwi
    chakhwi = resolve_northeast_food_by_name("Chakhwi")
    assert chakhwi is not None
    assert chakhwi.canonical_food_id == "TR_STEW_CHAKHWI"

    # Nepali: Gundruk
    gundruk = resolve_northeast_food_by_name("गुन्द्रुक")
    assert gundruk is not None
    assert gundruk.canonical_food_id == "SK_STEW_GUNDRUK"


# =============================================================================
# 2. RICE-MEAT DISCRIMINATOR (Sections 11, 22, 26, 48)
# =============================================================================

def test_northeast_rice_meat_discriminator():
    """Verifies distinction between Jadoh, Galho, Sawhchiar, and generic pulao."""
    # Jadoh: dry pilaf with pork fat
    jadoh_cues = {"is_dry_pilaf": True, "has_pork_fat": True, "is_soupy_porridge": False}
    j_res = NortheastRiceMeatDiscriminator.classify(jadoh_cues)
    assert j_res["dish_name"] == "Jadoh"
    assert j_res["state"] == "Meghalaya"

    # Galho: soupy with leafy greens and axone
    galho_cues = {"is_soupy_porridge": True, "has_leafy_greens": True, "has_axone": True}
    g_res = NortheastRiceMeatDiscriminator.classify(galho_cues)
    assert g_res["dish_name"] == "Galho"
    assert g_res["state"] == "Nagaland"

    # Sawhchiar: pale creamy meat and rice porridge
    sawh_cues = {"is_soupy_porridge": True, "has_creamy_shredded_meat": True, "has_axone": False}
    s_res = NortheastRiceMeatDiscriminator.classify(sawh_cues)
    assert s_res["dish_name"] == "Sawhchiar"
    assert s_res["state"] == "Mizoram"


# =============================================================================
# 3. FERMENTED SOYBEAN DISCRIMINATOR (Sections 13, 25, 39, 42)
# =============================================================================

def test_fermented_soybean_discriminator():
    """Disambiguates Axone (Nagaland) vs Tungrymbai (Meghalaya) vs Kinema (Sikkim)."""
    # Tungrymbai: black sesame
    t_cues = {"has_black_sesame": True, "color": "charcoal_black"}
    t_res = FermentedSoybeanDiscriminator.classify(t_cues)
    assert t_res["fermented_product"] == "Tungrymbai"
    assert t_res["state"] == "Meghalaya"

    # Kinema: sticky whole beans in tomato curry
    k_cues = {"is_sticky_whole_bean": True, "in_tomato_curry": True}
    k_res = FermentedSoybeanDiscriminator.classify(k_cues)
    assert k_res["fermented_product"] == "Kinema"
    assert k_res["state"] == "Sikkim"

    # Axone: brown paste
    a_cues = {"has_black_sesame": False, "is_sticky_whole_bean": False, "color": "brown"}
    a_res = FermentedSoybeanDiscriminator.classify(a_cues)
    assert a_res["fermented_product"] == "Axone / Akhuni"
    assert a_res["state"] == "Nagaland"


# =============================================================================
# 4. MASHED VEGETABLES & SALADS (Sections 8, 16, 17, 31, 46)
# =============================================================================

def test_mashed_vegetable_chutney_discriminator():
    """Disambiguates Aloo Pitika vs Eromba vs Mosdeng vs Singju."""
    # Singju: raw shredded salad
    singju_cues = {"is_raw_shredded_salad": True}
    s_res = MashedVegetableChutneyDiscriminator.classify(singju_cues)
    assert s_res["dish_name"] == "Manipuri Singju"
    assert s_res["state"] == "Manipur"

    # Eromba: fermented fish without roasted tomatoes
    eromba_cues = {"has_fermented_fish": True, "has_roasted_tomatoes": False}
    e_res = MashedVegetableChutneyDiscriminator.classify(eromba_cues)
    assert e_res["dish_name"] == "Manipuri Eromba"
    assert e_res["state"] == "Manipur"

    # Mosdeng Serma: charred tomatoes with fermented fish
    mosdeng_cues = {"has_fermented_fish": True, "has_roasted_tomatoes": True}
    m_res = MashedVegetableChutneyDiscriminator.classify(mosdeng_cues)
    assert m_res["dish_name"] == "Mosdeng Serma"
    assert m_res["state"] == "Tripura"

    # Aloo Pitika: raw mustard oil, no fish
    pitika_cues = {"has_raw_mustard_oil": True, "has_fermented_fish": False}
    p_res = MashedVegetableChutneyDiscriminator.classify(pitika_cues)
    assert p_res["dish_name"] == "Assamese Aloo Pitika"
    assert p_res["state"] == "Assam"


# =============================================================================
# 5. WOOD-SMOKED MEAT VERIFIER (Section 43)
# =============================================================================

def test_smoked_meat_verifier():
    """Verifies traditional wood-smoked meat vs fried or charred meat."""
    # Authentic smoked pork
    smoked_cues = {"has_cured_smoke_ring": True, "has_cured_amber_fat": True, "has_wood_smoke_texture": True}
    s_res = SmokedMeatVerifier.verify(smoked_cues)
    assert s_res["is_smoked"] is True
    assert s_res["category"] == "authentic_wood_smoked_meat"

    # Batter fried meat
    fried_cues = {"is_batter_fried": True}
    f_res = SmokedMeatVerifier.verify(fried_cues)
    assert f_res["is_smoked"] is False
    assert f_res["category"] == "deep_fried_meat"

    # Charred/burnt meat without cured fat
    burnt_cues = {"is_freshly_charred_or_burnt": True, "has_cured_amber_fat": False}
    b_res = SmokedMeatVerifier.verify(burnt_cues)
    assert b_res["is_smoked"] is False
    assert b_res["category"] == "charred_or_burnt_meat"


# =============================================================================
# 6. COUNTABLE ITEMS & OCCLUSION (Sections 40, 55, 71, 72)
# =============================================================================

def test_countable_food_detector_and_momo_occlusion():
    """Section 40 & 55: Momos counting, handling partial occlusion."""
    # 6 visible momos with 0% occlusion
    res_clean = NortheastCountableDetector.estimate_count_and_weight("NE_MOMO_PORK_STEAMED", 6, 0.0)
    assert res_clean.is_countable is True
    assert res_clean.visible_count == 6
    assert res_clean.estimated_total_count == 6
    assert res_clean.total_estimated_weight_g == 180.0

    # 6 visible momos with 25% occlusion factor (partially overlapping plate)
    res_occluded = NortheastCountableDetector.estimate_count_and_weight("NE_MOMO_PORK_STEAMED", 6, 0.25)
    assert res_occluded.visible_count == 6
    assert res_occluded.estimated_total_count >= 8
    assert res_occluded.occluded_count >= 2
    assert res_occluded.total_estimated_weight_g >= 240.0

    # Sel Roti (Sikkim)
    sel_res = NortheastCountableDetector.estimate_count_and_weight("SK_BREAD_SEL_ROTI", 2)
    assert sel_res.unit_name == "sel_roti_ring"
    assert sel_res.total_estimated_weight_g == 120.0


# =============================================================================
# 7. COMPOSITE MEAL DECOMPOSERS (Sections 29, 56, 73)
# =============================================================================

def test_tripuri_mui_borok_decomposer_never_returns_monolithic_calories():
    """Section 29: Never return only Mui Borok = 800 kcal without component segmentation."""
    res = TripuriMuiBorokDecomposer.decompose()
    assert isinstance(res, NortheastCompositeDecompositionResult)
    assert res.total_components_detected == 4

    names = [it.name for it in res.items]
    assert "Plain Steamed Rice" in names
    assert "Tripuri Chakhwi" in names
    assert "Mosdeng Serma" in names
    assert "Gudok" in names
    assert res.total_edible_weight_g >= 400.0
    assert res.total_calories > 400.0


def test_assamese_thali_decomposer():
    """Section 73: Decomposes Assamese Thali into Joha Rice, Khar, Tenga, Pitika, Dal."""
    res = AssameseThaliDecomposer.decompose()
    assert res.total_components_detected == 6

    names = [it.name for it in res.items]
    assert "Assamese Joha Rice" in names
    assert "Amitar Khar" in names
    assert "Masor Tenga" in names
    assert "Aloo Pitika" in names
    assert "Mati Mahor Dal" in names


def test_meghalaya_jadoh_platter_decomposer():
    """Section 11 & 73: Decomposes Jadoh plate into Jadoh, Dohneiihong, Doh Khlieh, Tungrymbai."""
    res = MeghalayaJadohPlatterDecomposer.decompose()
    assert res.total_components_detected == 5

    names = [it.name for it in res.items]
    assert "Khasi Jadoh" in names
    assert "Dohneiihong" in names
    assert "Doh Khlieh" in names
    assert "Tungrymbai" in names


def test_naga_platter_and_sikkim_meal_decomposers():
    """Section 73: Decomposes Naga Feast and Sikkim Meal."""
    naga = NagaPlatterDecomposer.decompose()
    assert naga.total_components_detected == 4
    n_names = [it.name for it in naga.items]
    assert "Smoked Pork with Axone" in n_names
    assert "Raja Mircha Chutney" in n_names

    sikkim = SikkimMealDecomposer.decompose()
    assert sikkim.total_components_detected == 5
    s_names = [it.name for it in sikkim.items]
    assert "Gundruk Jhol" in s_names
    assert "Phagshapa" in s_names
    assert "Kinema Curry" in s_names
    assert "Sel Roti" in s_names


def test_northeast_packaging_filter():
    """Section 57: Filters out bell-metal kanh platters, banana leaves, and bamboo pipes."""
    detections = [
        {"label": "bell_metal_kanh_platter"},
        {"label": "banana_leaf"},
        {"label": "bamboo_pipe_cooking_tube"},
        {"label": "AS_FISH_MASOR_TENGA"}
    ]
    filtered = NortheastPackagingFilter.filter_non_food_detections(detections)
    assert len(filtered) == 1
    assert filtered[0]["label"] == "AS_FISH_MASOR_TENGA"


# =============================================================================
# 8. VISUAL FAT ESTIMATOR (Sections 52, 66)
# =============================================================================

def test_northeast_fat_level_estimator():
    """Sections 52 & 66: Heavy pork belly fat vs oil-free boiled stews."""
    pork_fat = NortheastFatLevelEstimator.estimate_fat({"has_heavy_pork_fat": True})
    assert pork_fat["fat_level"] == "high"
    assert pork_fat["fat_multiplier"] > 1.2

    boiled_greens = NortheastFatLevelEstimator.estimate_fat({"is_oil_free_boiled": True})
    assert boiled_greens["fat_level"] == "very_low"
    assert boiled_greens["fat_multiplier"] < 0.8


# =============================================================================
# 9. SECTION 86 MODEL OUTPUT & SECTION 87 NO-HALLUCINATION RULE
# =============================================================================

def test_section_86_standardized_model_output_schema():
    """Section 86: Full model output compliance with uncertainty calorie ranges."""
    out = NortheastRecipeNutritionCalculator.calculate_dish_nutrition(
        food_identifier="ML_RICE_JADOH_PORK",
        visual_cues={"has_heavy_pork_fat": True}
    )
    assert isinstance(out, Section86ModelOutput)
    assert out.food_name == "Jadoh (Pork)"
    assert out.canonical_food_id == "ML_RICE_JADOH_PORK"
    assert out.state == "Meghalaya"
    assert out.region_community == "Khasi Hills"
    assert out.vegetarian is False
    assert out.calories_kcal.min < out.calories_kcal.expected < out.calories_kcal.max
    assert out.confidence >= 0.90
    assert out.user_confirmation_required is False


def test_section_87_no_hallucination_rule_unknown_fallback():
    """Section 87: Refuses to hallucinate when visual evidence is insufficient."""
    out = NortheastRecipeNutritionCalculator.calculate_dish_nutrition(
        food_identifier="unrecognized_tribal_leaf_stew_xyz"
    )
    assert out.canonical_food_id == "NORTHEAST_INDIAN_UNKNOWN"
    assert out.confidence < 0.35
    assert out.user_confirmation_required is True
    assert "Unable to identify" in out.uncertainty


# =============================================================================
# 10. UNIFIED PRODUCTION ORCHESTRATOR ROUTING
# =============================================================================

def test_production_orchestrator_northeast_indian_methods():
    """Verifies that production_orchestrator exposes and executes all Northeast Indian methods."""
    # Single dish
    dish_res = production_orchestrator.analyze_northeast_indian_dish("AS_FISH_MASOR_TENGA")
    assert dish_res.canonical_food_id == "AS_FISH_MASOR_TENGA"
    assert dish_res.state == "Assam"

    # Assamese Thali
    a_res = production_orchestrator.analyze_assamese_thali()
    assert a_res.platter_type == "thali"

    # Meghalaya Jadoh
    j_res = production_orchestrator.analyze_meghalaya_jadoh_platter()
    assert j_res.platter_type == "meal_plate"

    # Naga Platter
    n_res = production_orchestrator.analyze_naga_platter()
    assert n_res.platter_type == "meal_plate"

    # Tripuri Mui Borok
    t_res = production_orchestrator.analyze_tripuri_mui_borok()
    assert t_res.platter_type == "mui_borok_meal"

    # Sikkim Meal
    s_res = production_orchestrator.analyze_sikkim_meal()
    assert s_res.platter_type == "thali"

    # Manipuri Meal
    m_res = production_orchestrator.analyze_manipuri_meal()
    assert m_res.platter_type == "meal_plate"
    assert m_res.state == "Manipur"

    # Mizo Meal
    mz_res = production_orchestrator.analyze_mizo_meal()
    assert mz_res.platter_type == "meal_plate"
    assert mz_res.state == "Mizoram"

    # Arunachal Meal
    ar_res = production_orchestrator.analyze_arunachal_meal()
    assert ar_res.platter_type == "thali"
    assert ar_res.state == "Arunachal Pradesh"


# =============================================================================
# 11. ARUNACHAL PRADESH DEDICATED DATASET & ALL 8 STATES DECOMPOSITION
# =============================================================================

def test_arunachal_pradesh_food_classes():
    """Sections 31-33: Verifies Arunachal Pradesh classes with permanent AR_* IDs."""
    ar_ids = [
        "AR_MOMO_PORK_STEAMED",
        "AR_MOMO_VEG_STEAMED",
        "AR_THUKPA_CHICKEN",
        "AR_BREAD_KHURA",
        "AR_STEW_ZAN",
        "AR_BAMBOO_EKUNG_PORK",
        "AR_FERMENTED_CHHURPI_SOUP",
        "AR_THALI_ARUNACHAL"
    ]
    for cid in ar_ids:
        food = get_northeast_food_class(cid)
        assert food is not None, f"Missing Arunachal food class: {cid}"
        assert food.state == "Arunachal Pradesh"
        assert food.hierarchy.level3_state == "Arunachal Pradesh"
        assert len(food.key_ingredients) > 0


def test_all_8_northeast_states_meal_decomposers():
    """Section 54: Verifies full meal decomposition across all 8 Northeast states."""
    decomposers = [
        (AssameseThaliDecomposer, "Assam"),
        (MeghalayaJadohPlatterDecomposer, "Meghalaya"),
        (NagaPlatterDecomposer, "Nagaland"),
        (TripuriMuiBorokDecomposer, "Tripura"),
        (SikkimMealDecomposer, "Sikkim"),
        (ManipuriMealDecomposer, "Manipur"),
        (MizoMealDecomposer, "Mizoram"),
        (ArunachalMealDecomposer, "Arunachal Pradesh")
    ]
    assert len(decomposers) == 8

    for dec, expected_state in decomposers:
        res = dec.decompose()
        assert isinstance(res, NortheastCompositeDecompositionResult)
        assert res.state == expected_state
        assert res.total_components_detected >= 4
        assert res.total_calories > 250.0
        assert res.total_edible_weight_g > 300.0


# =============================================================================
# 12. SECTION 74, 78 & 82 STANDARDIZED SCHEMAS & SECTION 80 QUALITY RULES
# =============================================================================

def test_section_74_single_food_json_schema():
    """Section 74: Verifies Single Food JSON Schema exact specification."""
    single = production_orchestrator.generate_northeast_section_74_single_food(
        food_identifier="NE_MOMO_PORK_STEAMED",
        count=8,
        cooking_method="steamed"
    )
    assert isinstance(single, Section74SingleFoodJSON)
    assert single.food_name == "Steamed Pork Momo"
    assert single.region == "Northeast India"
    assert single.count == 8
    assert single.estimated_weight_g > 200.0
    assert single.cooking_method == "steamed"
    assert single.confidence >= 0.90
    assert "calories_kcal" in single.nutrition
    assert "protein_g" in single.nutrition
    assert "carbohydrates_g" in single.nutrition
    assert "fat_g" in single.nutrition


def test_section_78_unknown_food_fallback():
    """Section 78: Verifies Unknown Food Fallback Schema."""
    unknown = production_orchestrator.generate_northeast_section_78_unknown_fallback(confidence=0.24)
    assert isinstance(unknown, Section78UnknownFoodOutput)
    assert unknown.food_name == "Unknown Northeast Indian Food"
    assert unknown.specific_dish == "Unknown"
    assert unknown.confidence == 0.24
    assert unknown.action == "Ask user for confirmation"


def test_section_82_multi_food_model_output():
    """Section 82: Verifies Multi-Food Model Output Example Schema."""
    multi = production_orchestrator.generate_northeast_section_82_multi_food()
    assert isinstance(multi, Section82ModelOutput)
    assert multi.meal_region == "Northeast India"
    assert multi.confidence >= 0.80
    assert len(multi.items) == 4

    item_names = [it.food_name for it in multi.items]
    assert "Rice" in item_names
    assert "Pork Preparation" in item_names
    assert "Bamboo Shoot Preparation" in item_names
    assert "Chutney" in item_names
    assert multi.nutrition_status == "Estimate using verified database and recipe variation"


def test_section_80_quality_rules_enforcement():
    """Section 80: Quality Rules (never infer biryani from meat+rice, dumpling from momo alone, etc.)."""
    # 1. Jadoh vs Biryani
    jadoh_check = disambiguate_northeast_pair(
        pair_id="CONF_JADOH_VS_PULAO_KHICHDI",
        visual_features={"grain_type": "short_bold_indigenous_rice", "cooking_fat": "pork_fat_rendered"}
    )
    assert jadoh_check["selected_class_id"] == "ML_RICE_JADOH_PORK"
    assert "Jadoh" in jadoh_check["resolution_notes"]

    # 2. Galho vs Khichdi
    galho_check = disambiguate_northeast_pair(
        pair_id="CONF_JADOH_VS_GALHO",
        visual_features={"consistency": "soupy_porridge", "has_axone": True, "has_leafy_greens": True}
    )
    assert galho_check["selected_class_id"] == "NL_RICE_GALHO"

    # 3. Pitika vs Eromba
    pitika_check = disambiguate_northeast_pair(
        pair_id="CONF_ALOO_PITIKA_VS_EROMBA_MOSDENG",
        visual_features={"has_ngari_fermented_fish": False, "oil_type": "raw_mustard_oil"}
    )
    assert pitika_check["selected_class_id"] == "AS_VEG_ALOO_PITIKA"

