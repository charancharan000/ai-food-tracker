"""
Comprehensive Test Suite for Indian Street Food AI Engine (Part 8)
Tests:
- Master Street Food Taxonomy & Hierarchical Traversal across 18 Sub-Families (Section 1, 91, 93)
- Pani Puri Counting & Occlusion-Aware Piece Estimator (Section 3, 4, 5)
- Component-Wise Pani Puri Calorie Decomposer (Never flat plate calories - Section 5)
- Hard Negative Disambiguation across 27+ Confusion Pairs (Section 75, 95)
  * Pani Puri vs Puchka
  * Bhel Puri vs Jhalmuri (Mustard oil sheen & chanachur vs wet chutneys)
  * Sev Puri vs Dahi Puri
  * Samosa vs Kachori
  * Batata Vada vs Aloo Bonda
  * Kathi Roll vs Frankie vs Shawarma (Paratha vs Roti vs Pita with mayo/fries)
  * Hakka Noodles vs Masala Maggi vs Thukpa (Wok straight vs curly wavy vs soup broth)
  * Vada Pav vs Kutchi Dabeli
  * Jalebi vs Imarti
- Composite Meal Decomposers:
  * Samosa Chaat (underlying samosa identified separately - Section 11)
  * Vada Pav Platter (Section 21)
  * Pav Bhaji Platter (Section 22)
  * Momos Platter with Counting & Mayo (Section 46)
  * Multi-Food Street Combo Meal with Packaging Filter (Section 79, 80, 81)
- Oil Uncertainty Estimator (Low / Medium / High / Unknown - Section 65)
- Cheese & Mayonnaise Add-on Calibration (Section 67 & 68)
- Beverage Sugar Handling & User Confirmation Prompts (Section 61 & 62)
- Section 96 Standardized Single Item & Multi-Food Outputs with Calibrated Calorie Ranges (Section 84, 96)
- Section 98 Non-Negotiable Rules & Unknown Street Food Fallback (Section 90, 98)
"""

import pytest
from app.food_ai.taxonomy.street_food_master_taxonomy import (
    STREET_FOOD_TAXONOMY_REGISTRY,
    get_street_food_class,
    resolve_street_food_by_name,
    filter_street_foods_by_family
)
from app.food_ai.datasets.street_food_hard_negatives import (
    STREET_FOOD_CONFUSION_REGISTRY,
    disambiguate_street_food_pair,
    PaniPuriCountingDiscriminator,
    StreetRollDiscriminator,
    NoodleDiscriminator,
    StreetPackagingFilter
)
from app.food_ai.datasets.street_food_composite_decomposer import (
    PaniPuriCompositeDecomposer,
    SamosaChaatCompositeDecomposer,
    VadaPavCompositeDecomposer,
    PavBhajiCompositeDecomposer,
    MomosPlatterCompositeDecomposer,
    MultiFoodStreetComboDecomposer
)
from app.food_ai.portion_engine.street_food_portions import (
    STREET_FOOD_PORTION_DATABASE,
    StreetOilEstimator,
    StreetCheeseMayonnaiseCalculator,
    BeverageSugarHandler
)
from app.food_ai.nutrition_engine.street_food_recipes import (
    StreetRecipeNutritionCalculator,
    Section5PaniPuriComponents,
    Section26IdliVadaCombo,
    Section72UnknownStreetFood,
    Section75MultiFoodOutput,
    Section96SingleItemOutput,
    Section96MultiFoodOutput
)
from app.food_ai.inference_orchestrator import production_orchestrator


# =============================================================================
# 1. TAXONOMY & HIERARCHY TESTS (Section 1, 91, 93)
# =============================================================================

def test_street_food_taxonomy_registered_and_traversal():
    """Verifies master taxonomy registration, hierarchical path, and canonical IDs."""
    assert len(STREET_FOOD_TAXONOMY_REGISTRY) >= 15
    mumbai_pp = get_street_food_class("CHAAT_PANI_PURI_MUMBAI")
    assert mumbai_pp is not None
    assert mumbai_pp.hierarchy.level1_food == "Indian Food"
    assert mumbai_pp.hierarchy.level2_macro_category == "Indian Street Food"
    assert mumbai_pp.hierarchy.level3_food_family == "Chaat"
    assert mumbai_pp.hierarchy.level4_sub_family == "Pani Puri"
    assert mumbai_pp.hierarchy.level5_canonical_food == "Pani Puri"
    assert "Warm Ragda" in mumbai_pp.hierarchy.level6_variant


def test_multilingual_synonym_resolution():
    """Verifies lookup via English, Hindi, Bengali, Marathi, and Tamil synonyms."""
    # Hindi "गोलगप्पा"
    rec_hindi = resolve_street_food_by_name("गोलगप्पा")
    assert rec_hindi is not None
    assert rec_hindi.canonical_food_id == "CHAAT_GOLGAPPA_DELHI"

    # Bengali "ফুচকা"
    rec_bengali = resolve_street_food_by_name("ফুচকা")
    assert rec_bengali is not None
    assert rec_bengali.canonical_food_id == "CHAAT_PUCHKA_KOLKATA"

    # Marathi "वडा पाव"
    rec_marathi = resolve_street_food_by_name("वडा पाव")
    assert rec_marathi is not None
    assert rec_marathi.canonical_food_id == "PAV_VADA_PAV_CLASSIC"

    # Tamil "முட்டை கொத்து பரோட்டா"
    rec_tamil = resolve_street_food_by_name("முட்டை கொத்து பரோட்டா")
    assert rec_tamil is not None
    assert rec_tamil.canonical_food_id == "SOUTH_STREET_KOTHU_PAROTTA_EGG"


def test_filter_by_food_family():
    """Verifies retrieval by 18 master food families."""
    chaats = filter_street_foods_by_family("Chaat")
    assert len(chaats) >= 6
    names = [c.canonical_name for c in chaats]
    assert "Mumbai Pani Puri" in names
    assert "Delhi Golgappa" in names
    assert "Kolkata Puchka" in names
    assert "Mumbai Bhel Puri" in names
    assert "Classic Sev Puri" in names


# =============================================================================
# 2. PANI PURI COUNTING & OCCLUSION (Section 3, 4, 5)
# =============================================================================

def test_pani_puri_counting_clear_visibility():
    """Tests counting whole, filled, empty, and broken puris with high visibility."""
    detections = [
        {"state": "filled", "is_overlapped": False},
        {"state": "filled", "is_overlapped": False},
        {"state": "filled", "is_overlapped": False},
        {"state": "filled", "is_overlapped": False},
        {"state": "filled", "is_overlapped": False},
        {"state": "empty", "is_overlapped": False},
        {"state": "empty", "is_overlapped": False},
    ]
    res = PaniPuriCountingDiscriminator.count_puris(detections)
    assert res.visible_total_puris == 7
    assert res.filled_puris == 5
    assert res.empty_puris == 2
    assert res.estimated_total_range == "7"
    assert res.confidence == "High"


def test_pani_puri_counting_high_occlusion_range():
    """Verifies that high occlusion emits an estimated range rather than false precision (Section 4)."""
    detections = [
        {"state": "filled", "is_overlapped": True},
        {"state": "filled", "is_overlapped": True},
        {"state": "filled", "is_overlapped": True},
        {"state": "filled", "is_overlapped": True},
        {"state": "filled", "is_overlapped": False},
        {"state": "empty", "is_overlapped": False},
    ]
    res = PaniPuriCountingDiscriminator.count_puris(detections)
    assert res.visible_total_puris == 6
    assert res.occlusion_percentage > 30.0
    # Should emit a range like "6–9"
    assert "–" in res.estimated_total_range
    assert res.confidence in ("Medium", "Low")


def test_pani_puri_component_calorie_decomposition():
    """Verifies Pani Puri calories are calculated from puris + filling + water + toppings (never flat plate cals)."""
    # 6 puris with ragda
    res_6 = PaniPuriCompositeDecomposer.decompose(puri_count=6, filling_type="ragda", include_sweet_chutney=True, include_sev=True)
    assert res_6.total_mass_g > 200.0
    assert len(res_6.components) >= 4
    assert res_6.total_calories_range["expected"] > 250.0

    # 10 puris with potato mash (should scale proportionally)
    res_10 = PaniPuriCompositeDecomposer.decompose(puri_count=10, filling_type="kolkata_potato_mash", include_sweet_chutney=False, include_sev=False)
    assert res_10.total_mass_g > res_6.total_mass_g
    assert res_10.total_calories_range["expected"] != res_6.total_calories_range["expected"]


# =============================================================================
# 3. HARD NEGATIVES & FINE-GRAINED DISAMBIGUATION (Section 75, 95)
# =============================================================================

def test_bhel_puri_vs_jhalmuri_discriminator():
    """Verifies Bhel Puri vs Jhalmuri disambiguation based on raw mustard oil sheen & chanachur vs wet chutneys."""
    # Jhalmuri evidence
    cues_jhalmuri = {
        "oil": "raw_mustard_oil_yellow_sheen",
        "ingredients": ["chanachur", "coconut_slivers"],
        "masala": "dry_bhaja_powder"
    }
    winner, conf, reason = disambiguate_street_food_pair("Bhel Puri", "Jhalmuri", cues_jhalmuri)
    assert winner == "Kolkata Jhalmuri"
    assert conf >= 0.85
    assert "mustard" in reason.lower()

    # Bhel Puri evidence
    cues_bhel = {"sauce": "wet_tamarind_mint_chutneys", "sev": "fine_nylon_sev", "oil": "none_visible"}
    winner_bhel, conf_bhel, _ = disambiguate_street_food_pair("Bhel Puri", "Jhalmuri", cues_bhel)
    assert winner_bhel == "Mumbai Bhel Puri"
    assert conf_bhel >= 0.80


def test_samosa_vs_kachori_discriminator():
    """Verifies Samosa vs Kachori disambiguation based on 3D tetrahedron vs blistered round khasta."""
    cues_samosa = {"shape": "pyramidal_tetrahedron", "crust": "smooth_pastry_with_cone_seam", "filling": "chunky_potato_peas"}
    winner_s, conf_s, _ = disambiguate_street_food_pair("Samosa", "Kachori", cues_samosa)
    assert winner_s == "Samosa"
    assert conf_s >= 0.85

    cues_kachori = {"shape": "round_flattened_sphere", "crust": "blistered_flaky_khasta", "filling": "ground_dal_or_onion_paste"}
    winner_k, conf_k, _ = disambiguate_street_food_pair("Samosa", "Kachori", cues_kachori)
    assert winner_k == "Kachori"
    assert conf_k >= 0.85


def test_street_roll_discriminator():
    """Verifies Kathi Roll vs Frankie vs Shawarma (Section 28, 29, 30)."""
    # Kathi roll
    cues_kathi = {"bread_type": "layered_paratha", "egg_lining": True, "filling": "chicken_tikka"}
    roll_name, conf_r, _ = StreetRollDiscriminator.classify_roll(cues_kathi)
    assert "Kathi Roll" in roll_name
    assert conf_r >= 0.85

    # Shawarma
    cues_shawarma = {"bread_type": "pita_kubbus", "sauce": "garlic_mayo_toum", "fries_inside": True}
    roll_name_s, conf_s, _ = StreetRollDiscriminator.classify_roll(cues_shawarma)
    assert "Shawarma" in roll_name_s
    assert conf_s >= 0.90

    # Frankie
    cues_frankie = {"bread_type": "thin_roti", "filling": "potato_cutlet", "seasoning": "frankie_masala"}
    roll_name_f, conf_f, _ = StreetRollDiscriminator.classify_roll(cues_frankie)
    assert "Frankie" in roll_name_f
    assert conf_f >= 0.85


def test_noodle_discriminator_maggi_vs_hakka_vs_thukpa():
    """Verifies noodle distinction: curly Maggi vs straight Hakka vs soupy Thukpa (Section 48 & 50)."""
    # Maggi
    cues_maggi = {"strand_shape": "wavy_curly", "is_instant_curry": True}
    name_m, conf_m, _ = NoodleDiscriminator.classify_noodles(cues_maggi)
    assert "Maggi" in name_m
    assert conf_m >= 0.90

    # Thukpa
    cues_thukpa = {"broth_present": True, "liquid_depth_cm": 2.5}
    name_t, conf_t, _ = NoodleDiscriminator.classify_noodles(cues_thukpa)
    assert "Thukpa" in name_t
    assert conf_t >= 0.90

    # Hakka Noodles
    cues_hakka = {"strand_shape": "straight_cylindrical", "wok_tossed": True, "sauce_color": "dark_soy"}
    name_h, conf_h, _ = NoodleDiscriminator.classify_noodles(cues_hakka)
    assert "Hakka Noodles" in name_h
    assert conf_h >= 0.90


def test_vada_pav_vs_dabeli():
    """Verifies Vada Pav vs Kutchi Dabeli disambiguation (Section 25 & 75)."""
    cues_dabeli = {"filling": "loose_dark_potato_mash", "toppings": ["masala_peanuts", "pomegranate_arils"]}
    winner, conf, _ = disambiguate_street_food_pair("Vada Pav", "Kutchi Dabeli", cues_dabeli)
    assert winner == "Kutchi Dabeli"
    assert conf >= 0.85


# =============================================================================
# 4. COMPOSITE MEAL DECOMPOSITIONS
# =============================================================================

def test_samosa_chaat_decomposer():
    """Verifies Samosa Chaat identifies underlying samosa separately from chole and dahi (Section 11)."""
    res = SamosaChaatCompositeDecomposer.decompose(samosa_count=1, broken=True, chole_portion_g=120.0, dahi_portion_g=60.0)
    assert len(res.components) >= 4
    comp_names = [c.name for c in res.components]
    assert any("Samosa" in n for n in comp_names)
    assert any("Chole" in n for n in comp_names)
    assert any("Dahi" in n for n in comp_names)
    assert res.total_mass_g > 300.0
    assert res.total_calories_range["low"] < res.total_calories_range["expected"] < res.total_calories_range["high"]


def test_vada_pav_platter_decomposer():
    """Verifies Vada Pav platter decomposition into pav, batata vada, and chutneys (Section 21)."""
    res = VadaPavCompositeDecomposer.decompose(vada_pav_count=2, butter_toasted=True, cheese_slice=False)
    assert len(res.components) >= 5
    comp_names = [c.name for c in res.components]
    assert any("Ladi Pav" in n for n in comp_names)
    assert any("Batata Vada" in n for n in comp_names)
    assert any("Garlic" in n for n in comp_names)
    assert any("Chilli" in n for n in comp_names)
    assert res.total_mass_g > 250.0


def test_pav_bhaji_platter_decomposer():
    """Verifies Pav Bhaji decomposition into Pavs, Bhaji, and melting butter slab (Section 22)."""
    res = PavBhajiCompositeDecomposer.decompose(pav_count=2, bhaji_portion_g=200.0, butter_slab_g=18.0)
    assert len(res.components) >= 4
    comp_names = [c.name for c in res.components]
    assert any("Ladi Pav" in n for n in comp_names)
    assert any("Bhaji" in n for n in comp_names)
    assert any("Butter" in n for n in comp_names)
    assert res.total_fat_g > 20.0  # butter adds substantial fat


def test_momos_platter_decomposer():
    """Verifies Momos platter counts momos individually and adds chutney & mayo (Section 46)."""
    res = MomosPlatterCompositeDecomposer.decompose(momo_count=8, filling="chicken", preparation="steamed", has_mayo=True)
    momo_comp = next(c for c in res.components if "Momos" in c.name)
    assert momo_comp.count == 8
    assert len(res.components) == 3  # momos, red chutney, mayo
    assert res.total_calories_range["expected"] > 400.0


def test_multi_food_street_combo_packaging_filter():
    """Verifies packaging items (paper plate, skewers, foil) are filtered out (Section 76, 79, 81)."""
    raw_items = [
        {"name": "Vada Pav", "count": 2, "estimated_weight_g": 260.0, "calories": 520.0, "confidence": 0.95},
        {"name": "French Fries", "count": 1, "estimated_weight_g": 100.0, "calories": 310.0, "confidence": 0.92},
        {"name": "paper_plate", "is_packaging": True, "estimated_weight_g": 15.0},
        {"name": "wooden_skewer", "is_packaging": True, "estimated_weight_g": 4.0},
        {"name": "aluminum_foil", "is_packaging": True, "estimated_weight_g": 5.0}
    ]
    res = MultiFoodStreetComboDecomposer.decompose_plate(plate_name="Vada Pav Combo Meal", items=raw_items)
    # Only Vada Pav and French Fries should remain
    assert len(res.components) == 2
    comp_names = [c.name for c in res.components]
    assert "Vada Pav" in comp_names
    assert "French Fries" in comp_names
    assert "paper_plate" not in comp_names


# =============================================================================
# 5. PORTION, OIL, CHEESE/MAYO, & BEVERAGE TESTS (Section 61, 65, 67, 68)
# =============================================================================

def test_oil_estimator_deep_fried_vs_steamed():
    """Verifies oil estimator never claims exact 15g and adjusts uncertainty (Section 65)."""
    oil_high = StreetOilEstimator.estimate_oil(preparation_style="Deep Fried", surface_sheen="greasy", is_deep_fried=True)
    assert oil_high.oil_level == "High"
    assert oil_high.fat_multiplier > 1.25
    assert oil_high.uncertainty_spread_pct >= 15.0

    oil_steamed = StreetOilEstimator.estimate_oil(preparation_style="Steamed")
    assert oil_steamed.oil_level == "Low"
    assert oil_steamed.fat_multiplier < 1.0


def test_cheese_and_mayonnaise_calculator():
    """Verifies cheese and mayo calorie and fat additions (Section 67 & 68)."""
    cheese = StreetCheeseMayonnaiseCalculator.calculate_cheese(cheese_type="grated", intensity="standard")
    assert cheese.calories >= 90.0
    assert cheese.fat_g >= 7.0

    mayo = StreetCheeseMayonnaiseCalculator.calculate_mayonnaise(mayo_type="garlic", intensity="loaded")
    assert mayo.calories > 200.0
    assert mayo.fat_g > 20.0


def test_beverage_sugar_handling():
    """Verifies that undetectable beverage sugar flags as 'Unknown' with user prompt (Section 61)."""
    # Unprompted cutting chai
    bev_unknown = BeverageSugarHandler.evaluate_beverage(beverage_type="cutting_chai", volume_ml=100.0)
    assert bev_unknown.sugar_status == "Unknown"
    assert bev_unknown.requires_user_confirmation is True
    assert bev_unknown.prompt_for_user is not None

    # User specified 2 spoons
    bev_known = BeverageSugarHandler.evaluate_beverage(beverage_type="cutting_chai", volume_ml=100.0, user_specified_sugar_spoons=2)
    assert bev_known.sugar_status == "Detected_Sugar"
    assert bev_known.requires_user_confirmation is False
    assert bev_known.sugar_added_cals == 40.0


# =============================================================================
# 6. SECTION 96 & 98 PRODUCTION ORCHESTRATOR TESTS
# =============================================================================

def test_orchestrator_analyze_street_dish_chicken_kathi_roll():
    """Verifies single item analysis matches Section 96 output specification."""
    res: Section96SingleItemOutput = production_orchestrator.analyze_street_food_dish(
        food_identifier="Chicken Kathi Roll",
        custom_weight_g=220.0,
        oil_override="Medium"
    )
    assert "Kathi Roll" in res.food_name
    assert res.estimated_weight_g == 220.0
    assert "–" in res.estimated_calories_range  # e.g., "450–580 kcal"
    assert "–" in res.protein_range_g
    assert res.calories_low < res.calories_expected < res.calories_high
    assert res.confidence in ("High", "Medium")


def test_orchestrator_unknown_food_fallback_rule_98():
    """Verifies Rule 98: fallback to 'Unknown Street Food' with Low confidence when evidence is insufficient."""
    res: Section96SingleItemOutput = production_orchestrator.analyze_street_food_dish(
        food_identifier="Alien UFO Snack",
        visual_cues={"low_visual_evidence": True}
    )
    assert res.food_name == "Unknown Street Food"
    assert res.canonical_id == "STREET_UNKNOWN"
    assert res.confidence == "Low"
    assert res.confidence_score <= 0.40
    assert res.requires_user_confirmation is True


def test_orchestrator_multi_food_plate_analysis():
    """Verifies multi-food plate analysis returns aggregated ranges per Section 96."""
    items = [
        {"name": "Vada Pav", "count": 2, "estimated_weight_g": 270.0},
        {"name": "Veg Hakka Noodles", "estimated_weight_g": 250.0}
    ]
    res: Section96MultiFoodOutput = production_orchestrator.analyze_street_multi_food_plate(
        plate_title="Street Evening Feast",
        items=items
    )
    assert len(res.detected_foods) == 2
    assert res.total_estimated_weight_g == 520.0
    assert "–" in res.total_estimated_calories_range
    assert res.total_calories_low < res.total_calories_expected < res.total_calories_high
    assert res.overall_confidence == "High"


# =============================================================================
# 11. SECTION 5, 20, 26, 72, 75, 80 QUALITY & OUTPUT TESTS
# =============================================================================

def test_section_5_pani_puri_component_separation():
    """Section 5: Output components separately when visible (puri, spiced filling, pani)."""
    pp = production_orchestrator.generate_street_section_5_pani_puri(count=6)
    assert isinstance(pp, Section5PaniPuriComponents)
    assert pp.food_name == "Pani Puri"
    assert pp.count == 6
    assert "puri" in pp.components
    assert "spiced filling" in pp.components
    assert "pani" in pp.components


def test_section_20_batata_vada_rule():
    """Section 20: If only potato vada is visible without pav bread, food_name = Batata Vada."""
    vada_pair = disambiguate_street_food_pair(
        candidate_a="Vada Pav",
        candidate_b="Batata Vada",
        observed_features={"bread": "absent", "structure": "standalone_fried_potato_sphere"}
    )
    assert vada_pair["resolved_food"] == "Batata Vada"
    assert "Batata Vada" in vada_pair["decision_rationale"]


def test_section_26_street_idli_vada_combo():
    """Section 26: Recognizes Idli, Medu Vada, Sambar, Coconut Chutney as separate items."""
    combo = production_orchestrator.generate_street_section_26_idli_vada_combo()
    assert isinstance(combo, Section26IdliVadaCombo)
    names = [it.food_name for it in combo.items]
    assert "Idli" in names
    assert "Medu Vada" in names
    assert "Sambar" in names
    assert "Coconut Chutney" in names


def test_section_72_unknown_street_food_output():
    """Section 72: Verifies Unknown Street Food output schema."""
    unk = production_orchestrator.generate_street_section_72_unknown_fallback(confidence=0.26)
    assert isinstance(unk, Section72UnknownStreetFood)
    assert unk.food_name == "Unknown Indian Street Food"
    assert unk.specific_dish == "Unknown"
    assert unk.confidence == 0.26
    assert unk.action == "Ask user for confirmation"


def test_section_75_multi_food_output():
    """Section 75: Multi-food output JSON example (Pani Puri, Samosa, Masala Chai)."""
    multi = production_orchestrator.generate_street_section_75_multi_food()
    assert isinstance(multi, Section75MultiFoodOutput)
    assert multi.meal_type == "Indian Street Food"
    assert len(multi.items) == 3

    item_names = [it.food_name for it in multi.items]
    assert "Pani Puri" in item_names
    assert "Samosa" in item_names
    assert "Masala Chai" in item_names

    pp = next(it for it in multi.items if it.food_name == "Pani Puri")
    assert pp.count == 6
    assert pp.estimated_weight_g == 180.0
    assert pp.confidence == 0.95


def test_section_80_final_street_quality_rules():
    """Section 80: Quality Rules (never classify dumpling as momo, pakora as bajji, etc.)."""
    # 1. Momo vs Dumpling
    momo_res = disambiguate_street_food_pair(
        candidate_a="Himalayan Momo",
        candidate_b="Chinese Dim Sum / Generic Dumpling",
        observed_features={"chutney": "fiery_red_chilli_garlic_sauce", "wrapper": "wheat_flour"}
    )
    assert momo_res["resolved_food"] == "Himalayan Momo"

    # 2. Kathi roll vs Frankie
    roll_res = disambiguate_street_food_pair(
        candidate_a="Kolkata Kathi Roll",
        candidate_b="Mumbai Frankie",
        observed_features={"bread": "flaky_layered_paratha", "egg": "bonded_egg_lining"}
    )
    assert roll_res["resolved_food"] == "Kolkata Kathi Roll"

