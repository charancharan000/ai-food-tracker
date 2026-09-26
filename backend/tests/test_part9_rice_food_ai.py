"""
Comprehensive Test Suite for Indian Rice & Biryani Food AI Engine (Part 9)
Tests:
- Master Rice Taxonomy & Hierarchical Traversal across 13 Families (Section 1, 5, 21, 28, 36, 70, 77)
- Multilingual Synonym Resolution (Hindi, Tamil, Telugu, Kannada, Bengali, Urdu)
- Hard Negative Disambiguation across High-Confusion Pairs (Section 20, 57, 76):
  * Biryani vs Pulao (marbled orange-white grains & birista vs uniform pale absorption)
  * Biryani vs Fried Rice (slow dum aromatics vs wok stir-fry & soy/scallions)
  * Khichdi vs Pongal (turmeric & cumin vs rich desi ghee, whole peppercorns & cashews)
  * Lemon Rice vs Yellow Pulao (mustard, curry leaves, roasted peanuts & chana dal)
  * Tomato Rice vs Biryani (homogeneous tomato tempering vs multi-layer meat masala)
  * Curd Rice vs Plain Rice with Curd on Side
- Plain Rice + Curry Discriminator (Section 60 & Rule 80):
  * Plain White Rice + Chicken Curry must NEVER be classified as Chicken Biryani
  * Plain White Rice + Dal must NEVER be classified as Khichdi
- Handi / Pot Biryani Detection (Section 52):
  * Detects whole handi/degchi vessel, flags that it is NOT a single personal serving, prompts user
- Biryani Meat & Egg Counting (Sections 18 & 45):
  * Counts visible chicken pieces, mutton chunks, and eggs without assuming hidden pieces
- Composite Meal Decomposers (Sections 43, 44, 46, 58, 59):
  * Biryani Plate: isolates rice, meat, egg, birista, raita, and salan (sides excluded from core)
  * South Indian Full Rice Meal: rice, sambar, rasam, poriyal, curd, appalam (never monolithic 900 kcal)
  * Biryani Feast Combo Meal: biryani, chicken 65, egg, raita, salan, soft drink
- Portion Engine & Rice-to-Meat Ratio (Sections 46, 47, 48, 49, 50):
  * Small, Medium, Large, Extra Large calibrated portions
  * Explicit rice-to-meat mass split
  * Ghee/fat estimation: Low, Medium, High, Unknown (never claims exact grams)
  * Birista and fried cashew/raisin additions
- Section 78 & 80 Production Orchestrator Compliance:
  * Emits calibrated ranges (e.g., 700–850 kcal, never fake 731 kcal)
  * Unknown Rice Dish fallback with Low confidence when visual evidence is insufficient (Rule 80)
"""

import pytest
from app.food_ai.taxonomy.rice_master_taxonomy import (
    RICE_TAXONOMY_REGISTRY,
    get_rice_food_class,
    resolve_rice_food_by_name,
    filter_rice_foods_by_family
)
from app.food_ai.datasets.rice_hard_negatives import (
    RICE_CONFUSION_REGISTRY,
    disambiguate_rice_pair,
    PlainRiceCurryVsBiryaniDiscriminator,
    HandiPotDetector,
    BiryaniMeatEggCounter,
    Section74AntiBiasVerifier
)
from app.food_ai.datasets.rice_composite_decomposer import (
    BiryaniPlateDecomposer,
    SouthIndianRiceMealDecomposer,
    BiryaniComboMealDecomposer,
    RiceCompositeDecompositionResult
)
from app.food_ai.portion_engine.rice_portions import (
    RICE_PORTION_DATABASE,
    RiceToMeatRatioEstimator,
    RiceOilGheeEstimator,
    RiceGarnishCalculator
)
from app.food_ai.nutrition_engine.rice_recipes import (
    RiceRecipeNutritionCalculator,
    Section78RiceSingleOutput,
    Section78RiceMultiOutput,
    Section60UnknownRiceOutput,
    Section68BiryaniOutput,
    Section69VarietyRiceOutput,
    Section70PlateItem,
    Section70MultiFoodPlateOutput
)
from app.food_ai.inference_orchestrator import production_orchestrator


# =============================================================================
# 1. TAXONOMY & HIERARCHY TESTS (Sections 1, 5, 21, 28, 36, 70, 77)
# =============================================================================

def test_rice_taxonomy_registered_and_traversal():
    """Verifies master taxonomy registration, hierarchical path, and canonical IDs."""
    assert len(RICE_TAXONOMY_REGISTRY) >= 12
    hyd_rec = get_rice_food_class("BIRYANI_HYDERABADI_CHICKEN")
    assert hyd_rec is not None
    assert hyd_rec.hierarchy.level1_food == "Indian Food"
    assert hyd_rec.hierarchy.level2_macro_category == "Rice-Based Food"
    assert hyd_rec.hierarchy.level3_rice_family == "Biryani"
    assert hyd_rec.hierarchy.level4_sub_family == "Chicken Biryani"
    assert hyd_rec.hierarchy.level5_canonical_food == "Hyderabadi Biryani"
    assert hyd_rec.hierarchy.level7_grain_type == "long_grain_basmati"
    assert hyd_rec.hierarchy.level8_cooking_state == "Dum Cooked"
    assert hyd_rec.regional_style == "Hyderabadi"


def test_multilingual_synonym_resolution():
    """Verifies lookup via English, Hindi, Tamil, Telugu, and Kannada synonyms."""
    # Hindi "हैदराबादी चिकन बिरयानी"
    rec_hindi = resolve_rice_food_by_name("हैदराबादी चिकन बिरयानी")
    assert rec_hindi is not None
    assert rec_hindi.canonical_food_id == "BIRYANI_HYDERABADI_CHICKEN"

    # Tamil "ஆம்பூர் மட்டன் பிரியாணி"
    rec_tamil = resolve_rice_food_by_name("ஆம்பூர் மட்டன் பிரியாணி")
    assert rec_tamil is not None
    assert rec_tamil.canonical_food_id == "BIRYANI_AMBUR_MUTTON"

    # Telugu "హైదరాబాదీ చికెన్ బిర్యానీ"
    rec_telugu = resolve_rice_food_by_name("హైదరాబాదీ చికెన్ బిర్యానీ")
    assert rec_telugu is not None
    assert rec_telugu.canonical_food_id == "BIRYANI_HYDERABADI_CHICKEN"

    # Kannada "ಚಿತ್ರಾನ್ನ"
    rec_kannada = resolve_rice_food_by_name("ಚಿತ್ರಾನ್ನ")
    assert rec_kannada is not None
    assert rec_kannada.canonical_food_id == "VARIETY_RICE_LEMON"

    # Tamil "தயிர் சாதம்"
    rec_thayir = resolve_rice_food_by_name("தயிர் சாதம்")
    assert rec_thayir is not None
    assert rec_thayir.canonical_food_id == "CURD_RICE_TRADITIONAL"


def test_filter_by_rice_family():
    """Verifies retrieval by master rice families."""
    biryanis = filter_rice_foods_by_family("Biryani")
    assert len(biryanis) >= 7
    b_names = [b.canonical_name for b in biryanis]
    assert "Hyderabadi Chicken Dum Biryani" in b_names
    assert "Ambur Mutton Biryani" in b_names
    assert "Dindigul Mutton Biryani" in b_names
    assert "Thalassery Chicken Biryani" in b_names
    assert "Kolkata Chicken Biryani with Aloo & Egg" in b_names


# =============================================================================
# 2. HARD NEGATIVE DISAMBIGUATION TESTS (Sections 20, 57, 76)
# =============================================================================

def test_biryani_vs_pulao_disambiguation():
    """Verifies Biryani vs Pulao based on grain color marbling, marinade, and birista."""
    # Biryani cues
    cues_biryani = {
        "grain_color_pattern": "marbled_orange_white",
        "marinade_intensity": "heavy_caramelized",
        "birista": "present_dark_fried"
    }
    winner_b, conf_b, reason_b = disambiguate_rice_pair("Biryani", "Pulao", cues_biryani)
    assert "Biryani" in winner_b
    assert conf_b >= 0.85
    assert "marbled" in reason_b.lower()

    # Pulao cues
    cues_pulao = {
        "grain_color_pattern": "uniform_pale_or_yellow",
        "marinade_intensity": "mild_absorption",
        "birista": "absent_or_light"
    }
    winner_p, conf_p, _ = disambiguate_rice_pair("Biryani", "Pulao", cues_pulao)
    assert "Pulao" in winner_p
    assert conf_p >= 0.85


def test_khichdi_vs_pongal_disambiguation():
    """Verifies Khichdi vs Ven Pongal based on turmeric vs whole peppercorns and ghee cashews."""
    # Ven Pongal cues
    cues_pongal = {
        "color": "pale_ivory_cream",
        "peppercorns": "visible_whole_black",
        "cashews": "golden_fried_halves",
        "sheen": "heavy_desi_ghee"
    }
    winner_pongal, conf_po, reason_po = disambiguate_rice_pair("Moong Dal Khichdi", "Ven Pongal", cues_pongal)
    assert winner_pongal == "Ven Pongal"
    assert conf_po >= 0.88
    assert "peppercorn" in reason_po.lower() or "cashew" in reason_po.lower()

    # Khichdi cues
    cues_khichdi = {"color": "turmeric_yellow", "peppercorns": "absent", "cashews": "absent", "temper": "cumin_onion"}
    winner_kh, conf_kh, _ = disambiguate_rice_pair("Moong Dal Khichdi", "Ven Pongal", cues_khichdi)
    assert winner_kh == "Moong Dal Khichdi"
    assert conf_kh >= 0.88


def test_lemon_rice_vs_yellow_pulao_disambiguation():
    """Verifies Lemon Rice vs Yellow Pulao based on roasted peanuts, chana dal & mustard seeds."""
    cues_lemon = {
        "nuts_legumes": ["roasted_peanuts", "chana_dal", "urad_dal"],
        "tempering": ["mustard_seeds", "curry_leaves"]
    }
    winner_l, conf_l, _ = disambiguate_rice_pair("South Indian Lemon Rice", "Yellow Pulao", cues_lemon)
    assert winner_l == "South Indian Lemon Rice"
    assert conf_l >= 0.85


def test_curd_rice_vs_plain_rice_yogurt_disambiguation():
    """Verifies Curd Rice vs Plain Rice with Curd on side."""
    cues_curd_rice = {
        "structure": "homogeneous_creamy_mash",
        "tempering": ["mustard", "curry_leaves", "ginger_chillies"]
    }
    winner_cr, conf_cr, _ = disambiguate_rice_pair("Traditional Curd Rice", "Plain White Rice with Curd", cues_curd_rice)
    assert winner_cr == "Traditional Curd Rice (Thayir Sadam)"
    assert conf_cr >= 0.85


# =============================================================================
# 3. SECTION 60 & RULE 80: PLAIN RICE + CURRY DISCRIMINATOR
# =============================================================================

def test_plain_rice_plus_chicken_curry_never_classified_as_biryani():
    """CRITICAL RULE: Plain white rice + chicken curry must NEVER be classified as Chicken Biryani (Section 60 & 80)."""
    meta = {
        "has_separated_white_rice_mound": True,
        "adjacent_curry_type": "chicken_curry",
        "has_marbled_grains": False
    }
    result = PlainRiceCurryVsBiryaniDiscriminator.evaluate(meta)
    assert result.is_composite_rice_and_curry is True
    assert result.is_biryani is False
    assert result.rice_type == "Plain Steamed White Rice"
    assert result.curry_detected == "Chicken Curry"
    assert "Rule 60/80" in result.warning_rule_applied


def test_plain_rice_plus_dal_never_classified_as_khichdi():
    """CRITICAL RULE: Plain white rice + dal must NEVER be classified as Khichdi (Section 60 & 80)."""
    meta = {
        "has_separated_white_rice_mound": True,
        "adjacent_curry_type": "dal",
        "is_soft_porridge_mash": False
    }
    result = PlainRiceCurryVsBiryaniDiscriminator.evaluate(meta)
    assert result.is_composite_rice_and_curry is True
    assert result.is_khichdi is False
    assert result.curry_detected == "Dal"


def test_genuine_biryani_grain_marbling():
    """Verifies genuine biryani with marbled dum grains is classified correctly."""
    meta = {
        "has_separated_white_rice_mound": False,
        "has_marbled_grains": True
    }
    result = PlainRiceCurryVsBiryaniDiscriminator.evaluate(meta)
    assert result.is_biryani is True
    assert result.is_composite_rice_and_curry is False


# =============================================================================
# 4. SECTION 52: HANDI / POT BIRYANI DETECTION
# =============================================================================

def test_handi_pot_detection_prevents_single_serving_error():
    """Verifies that large earthen handi/pot is flagged as container-level, prompting user (Section 52)."""
    visual_cues = {
        "vessel_type": "clay_handi",
        "rim_diameter_cm": 22.0,
        "has_deep_walls": True,
        "is_clay_pot": True
    }
    res = HandiPotDetector.detect_vessel(visual_cues)
    assert res.is_container_level_vessel is True
    assert res.is_single_personal_serving is False
    assert res.estimated_vessel_capacity_grams >= 950.0
    assert res.requires_user_portion_prompt is True
    assert "How much did you consume?" in res.prompt_message


def test_individual_plate_detection():
    """Verifies normal individual plate serving does not trigger container warning."""
    visual_cues = {
        "vessel_type": "steel_plate",
        "rim_diameter_cm": 26.0,
        "has_deep_walls": False,
        "is_clay_pot": False
    }
    res = HandiPotDetector.detect_vessel(visual_cues)
    assert res.is_container_level_vessel is False
    assert res.is_single_personal_serving is True
    assert res.requires_user_portion_prompt is False


# =============================================================================
# 5. SECTIONS 18 & 45: PROTEIN & EGG COUNTING
# =============================================================================

def test_biryani_meat_egg_counting_no_hidden_assumption():
    """Verifies pieces are counted and zero hidden pieces are assumed (Section 18 & 45)."""
    detected_pieces = [
        {"class": "chicken_piece"},
        {"class": "chicken_piece"},
        {"class": "chicken_piece"},
        {"class": "boiled_egg"}
    ]
    res = BiryaniMeatEggCounter.count_protein_pieces(protein_type="chicken", detected_pieces=detected_pieces)
    assert res.visible_meat_pieces_count == 3
    assert res.visible_eggs_count == 1
    assert res.hidden_pieces_assumed is False
    assert res.estimated_meat_mass_g == 165.0  # 3 * 55g
    assert res.estimated_egg_mass_g == 50.0


# =============================================================================
# 6. COMPOSITE MEAL DECOMPOSERS (Sections 43, 44, 46, 58, 59)
# =============================================================================

def test_biryani_plate_decomposer():
    """Verifies biryani plate segregates rice, meat, egg, birista, raita, and salan (Section 43, 44, 46)."""
    res = BiryaniPlateDecomposer.decompose(
        style="Hyderabadi",
        protein_type="chicken",
        rice_mass_g=320.0,
        meat_pieces_count=2,
        has_egg=True,
        has_raita=True,
        has_salan=True
    )
    assert len(res.components) >= 5
    comp_names = [c.name for c in res.components]
    assert any("Biryani Rice" in n for n in comp_names)
    assert any("Chicken Pieces" in n for n in comp_names)
    assert any("Hard-Boiled Egg" in n for n in comp_names)
    assert any("Birista" in n for n in comp_names)
    assert any("Raita" in n for n in comp_names)
    assert any("Salan" in n for n in comp_names)
    assert res.total_mass_g > 500.0  # complete platter
    assert res.total_calories_range["low"] < res.total_calories_range["expected"] < res.total_calories_range["high"]


def test_south_indian_rice_meal_decomposer():
    """Verifies South Indian full meals decomposed into rice, sambar, rasam, poriyal, curd, appalam (Section 58)."""
    res = SouthIndianRiceMealDecomposer.decompose(
        rice_portion_g=240.0,
        has_sambar=True,
        has_rasam=True,
        has_poriyal=True,
        has_curd=True,
        has_appalam=True
    )
    assert len(res.components) == 6
    comp_names = [c.name for c in res.components]
    assert "Steamed White Rice" in comp_names
    assert "Toor Dal Vegetable Sambar" in comp_names
    assert "Tamarind Pepper Tomato Rasam" in comp_names
    assert "Green Beans & Coconut Poriyal" in comp_names
    assert "Fresh Plain Curd (Dahi)" in comp_names
    assert "Crisp Fried Appalam / Papad" in comp_names
    assert res.total_calories_range["expected"] > 450.0


def test_biryani_combo_meal_decomposer():
    """Verifies Biryani + Chicken 65 + Egg + Raita + Salan + Drink combo (Section 59)."""
    res = BiryaniComboMealDecomposer.decompose_combo(
        biryani_mass_g=350.0,
        chicken_65_pieces=4,
        include_egg=True,
        include_drink=True
    )
    assert len(res.components) == 6
    comp_names = [c.name for c in res.components]
    assert any("Chicken Dum Biryani" in n for n in comp_names)
    assert any("Chicken 65" in n for n in comp_names)
    assert any("Hard-Boiled Egg" in n for n in comp_names)
    assert any("Soft Drink" in n for n in comp_names)
    assert res.total_calories_range["expected"] > 900.0


# =============================================================================
# 7. PORTION, RATIO & GHEE ESTIMATOR TESTS (Sections 46, 47, 48, 49, 50)
# =============================================================================

def test_rice_portion_database_configs():
    """Verifies food-specific portion database differentiates Biryani, Plain Rice, and Curd Rice (Section 50)."""
    biryani_cfg = RICE_PORTION_DATABASE["biryani"]
    plain_cfg = RICE_PORTION_DATABASE["plain_rice"]
    curd_cfg = RICE_PORTION_DATABASE["curd_rice"]

    # Biryani medium is 380g; Plain rice medium is 240g
    assert biryani_cfg.medium.typical_grams == 380.0
    assert plain_cfg.medium.typical_grams == 240.0
    assert curd_cfg.medium.typical_grams == 280.0


def test_rice_to_meat_ratio_split():
    """Verifies explicit rice and meat mass computation (Section 46)."""
    split = RiceToMeatRatioEstimator.estimate_split(total_mass_g=420.0, protein_type="chicken", visible_meat_pieces=2)
    assert split.meat_pieces_count == 2
    assert split.meat_mass_g == 110.0  # 2 * 55g
    assert split.rice_mass_g == 310.0
    assert split.total_biryani_mass_g == 420.0


def test_rice_oil_ghee_estimator():
    """Verifies ghee estimator handles high glaze vs dry steamed without asserting exact grams (Section 47)."""
    fat_high = RiceOilGheeEstimator.estimate_fat(dish_family="biryani", surface_sheen="heavy_ghee_glaze", has_birista=True)
    assert fat_high.fat_level == "High"
    assert fat_high.fat_multiplier >= 1.25
    assert fat_high.uncertainty_spread_pct >= 15.0

    fat_low = RiceOilGheeEstimator.estimate_fat(dish_family="plain_rice", surface_sheen="matte_dry")
    assert fat_low.fat_level == "Low"
    assert fat_low.fat_multiplier < 1.0


# =============================================================================
# 8. SECTION 78 & 80 PRODUCTION ORCHESTRATOR TESTS
# =============================================================================

def test_orchestrator_analyze_dindigul_mutton_biryani():
    """Verifies Section 78 single dish output format with calibrated ranges."""
    res: Section78RiceSingleOutput = production_orchestrator.analyze_rice_dish(
        food_identifier="Dindigul Mutton Biryani",
        custom_weight_g=420.0,
        visible_meat_pieces=3,
        ghee_override="High"
    )
    assert res.food_name == "Dindigul Mutton Biryani"
    assert res.regional_style == "Dindigul"
    assert res.estimated_portion_g == 420.0
    assert "–" in res.estimated_calories_range  # calibrated range
    assert "–" in res.protein_range_g
    assert "–" in res.carbohydrates_range_g
    assert "–" in res.fat_range_g
    assert res.calories_low < res.calories_expected < res.calories_high
    assert res.confidence == "High"


def test_orchestrator_unknown_rice_fallback_rule_80():
    """Verifies Section 80 Rule: unknown rice dish fallback with Low confidence when evidence is insufficient."""
    res: Section78RiceSingleOutput = production_orchestrator.analyze_rice_dish(
        food_identifier="Unidentified Mystery Grains",
        visual_cues={"low_visual_evidence": True}
    )
    assert res.food_name == "Unknown Rice Dish"
    assert res.canonical_id == "RICE_UNKNOWN"
    assert res.confidence == "Low"
    assert res.confidence_score <= 0.40
    assert res.requires_user_confirmation is True
    assert "Could you specify" in res.confirmation_prompt


def test_orchestrator_multi_food_rice_plate_analysis():
    """Verifies Section 78 multi-food plate analysis."""
    items = [
        {"name": "Steamed White Rice", "estimated_weight_g": 240.0},
        {"name": "Hyderabadi Chicken Dum Biryani", "estimated_weight_g": 380.0, "meat_pieces": 2}
    ]
    res: Section78RiceMultiOutput = production_orchestrator.analyze_rice_composite_plate(
        plate_title="Weekend Rice Buffet",
        items=items
    )
    assert len(res.detected_items) == 2
    assert res.total_estimated_weight_g == 620.0
    assert "–" in res.total_estimated_calories_range
    assert res.total_calories_low < res.total_calories_expected < res.total_calories_high
    assert res.overall_confidence == "High"


# =============================================================================
# 9. SECTIONS 60, 68, 69, 70, 74 SPECIFICATION VERIFICATION TESTS
# =============================================================================

def test_section_68_biryani_output_unknown_vs_exact_style():
    """
    Verifies Section 68 Final Output Example — Biryani:
    - If regional style cannot be proven with high confidence (>= 0.85),
      it MUST fall back to 'Regional Style Unknown'.
    - If style evidence is strong (e.g. Hyderabadi), style is emitted.
    - Accurately reports meat_piece_count, calorie_range_kcal, protein_range_g.
    """
    # Case 1: Ambiguous style evidence (< 0.85) -> "Regional Style Unknown"
    res_unknown_style: Section68BiryaniOutput = production_orchestrator.generate_rice_section_68_biryani(
        food_name="Mutton Biryani",
        style="Hyderabadi",
        style_confidence=0.62,  # Insufficient evidence
        estimated_weight_g=420.0,
        meat_piece_count=3,
        overall_confidence=0.91
    )
    assert res_unknown_style.food_name == "Mutton Biryani"
    assert res_unknown_style.style == "Regional Style Unknown"
    assert res_unknown_style.estimated_weight_g == 420.0
    assert res_unknown_style.meat_piece_count == 3
    assert res_unknown_style.confidence == 0.91
    assert len(res_unknown_style.calorie_range_kcal) == 2
    assert res_unknown_style.calorie_range_kcal[0] < res_unknown_style.calorie_range_kcal[1]
    assert len(res_unknown_style.protein_range_g) == 2

    # Case 2: Strong style evidence (>= 0.85) -> "Hyderabadi"
    res_proven_style: Section68BiryaniOutput = production_orchestrator.generate_rice_section_68_biryani(
        food_name="Chicken Biryani",
        style="Hyderabadi",
        style_confidence=0.94,
        estimated_weight_g=450.0,
        meat_piece_count=2,
        overall_confidence=0.95
    )
    assert res_proven_style.food_name == "Chicken Biryani"
    assert res_proven_style.style == "Hyderabadi"
    assert res_proven_style.meat_piece_count == 2
    assert res_proven_style.confidence == 0.95


def test_section_69_variety_rice_output_lemon_rice():
    """
    Verifies Section 69 Final Output Example — Variety Rice:
    food_name: "Lemon Rice", estimated_weight_g: 280, confidence: 0.88,
    components: ["rice", "lemon-based seasoning", "peanuts", "curry leaves"].
    """
    res: Section69VarietyRiceOutput = production_orchestrator.generate_rice_section_69_variety_rice(
        food_name="Lemon Rice",
        estimated_weight_g=280.0,
        confidence=0.88
    )
    assert res.food_name == "Lemon Rice"
    assert res.estimated_weight_g == 280.0
    assert res.confidence == 0.88
    assert "rice" in res.components
    assert "lemon-based seasoning" in res.components
    assert "peanuts" in res.components
    assert "curry leaves" in res.components


def test_section_70_multi_food_plate_never_converted_to_biryani():
    """
    Verifies Section 70 Final Output — Multi-Food Plate:
    Steamed Rice 250g, Fish Curry 140g, Dal 100g, Vegetable Poriyal 80g.
    Strictly never converts or collapses this meal into Fish Biryani!
    """
    res: Section70MultiFoodPlateOutput = production_orchestrator.generate_rice_section_70_multi_food_plate(
        meal_type="Indian Rice Meal",
        items_spec=[
            {"food_name": "Steamed Rice", "weight_g": 250.0, "confidence": 0.99},
            {"food_name": "Fish Curry", "weight_g": 140.0, "confidence": 0.88},
            {"food_name": "Dal", "weight_g": 100.0, "confidence": 0.91},
            {"food_name": "Vegetable Poriyal", "weight_g": 80.0, "confidence": 0.78}
        ]
    )
    assert res.meal_type == "Indian Rice Meal"
    assert len(res.items) == 4
    assert res.items[0].food_name == "Steamed Rice"
    assert res.items[0].weight_g == 250.0
    assert res.items[1].food_name == "Fish Curry"
    assert res.items[1].weight_g == 140.0
    assert res.total_weight_g == 570.0
    assert res.non_monolithic_rule_enforced is True


def test_section_60_unknown_rice_food_system_fallback():
    """
    Verifies Section 60: Unknown Rice Food System Fallback
    If uncertain, outputs:
    food_family: "Rice-Based Food"
    specific_dish: "Unknown"
    confidence: 0.29
    """
    res: Section60UnknownRiceOutput = production_orchestrator.generate_rice_section_60_unknown_fallback(
        confidence=0.29
    )
    assert res.food_family == "Rice-Based Food"
    assert res.specific_dish == "Unknown"
    assert res.confidence == 0.29
    assert "User confirmation" in res.user_action_required


def test_section_74_non_negotiable_anti_bias_rules():
    """
    Verifies Section 74 Non-Negotiable Rules:
    - Never classify yellow rice as lemon rice purely from color
    - Never classify green rice as mint rice purely from color
    - Never classify red rice as tomato rice purely from color
    - Never classify creamy rice as kheer purely from creaminess
    - Never classify rice + meat curry as biryani
    - Never classify rice + dal as khichdi
    """
    # 1. Yellow rice without peanuts/mustard seeds rejected for lemon rice
    ok, reason = Section74AntiBiasVerifier.verify_color_dish_hypothesis(
        color_detected="yellow",
        hypothesized_dish="Lemon Rice",
        visual_cues={"has_peanuts": False, "has_mustard_seeds": False}
    )
    assert ok is False
    assert "Yellow color alone is insufficient" in reason

    # 2. Green rice without mint leaf bits rejected for mint rice
    ok, reason = Section74AntiBiasVerifier.verify_color_dish_hypothesis(
        color_detected="green",
        hypothesized_dish="Mint Rice",
        visual_cues={"has_mint_leaf_bits": False}
    )
    assert ok is False
    assert "Green color alone is insufficient" in reason

    # 3. Red rice without tomato pieces or tempering rejected for tomato rice
    ok, reason = Section74AntiBiasVerifier.verify_color_dish_hypothesis(
        color_detected="red",
        hypothesized_dish="Tomato Rice",
        visual_cues={"has_tomato_pieces": False, "has_mustard_curry_leaf_tempering": False}
    )
    assert ok is False
    assert "Red color alone is insufficient" in reason

    # 4. Creamy rice without sweet dessert profile rejected for kheer
    ok, reason = Section74AntiBiasVerifier.verify_color_dish_hypothesis(
        color_detected="creamy",
        hypothesized_dish="Rice Kheer",
        visual_cues={"is_sweet_dessert": False, "has_nuts_saffron": False}
    )
    assert ok is False
    assert "Creamy texture alone is insufficient" in reason

    # 5. Plain rice + chicken curry rejected from being collapsed into biryani
    ok, reason = Section74AntiBiasVerifier.verify_rice_and_curry_meal(
        has_separated_rice=True,
        has_separated_curry=True,
        curry_type="chicken curry"
    )
    assert ok is False
    assert "must never be classified as Biryani" in reason

    # 6. Plain rice + dal rejected from being collapsed into khichdi
    ok, reason = Section74AntiBiasVerifier.verify_rice_and_curry_meal(
        has_separated_rice=True,
        has_separated_curry=True,
        curry_type="dal"
    )
    assert ok is False
    assert "must never be classified as Khichdi" in reason

