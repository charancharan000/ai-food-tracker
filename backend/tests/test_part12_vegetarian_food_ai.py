"""
Comprehensive Test Suite for Indian Vegetarian Food AI System (Part 12)
Validates compliance with Sections 1 through 76 of Part 12 Master Training Specification.
"""

import pytest
from app.food_ai.taxonomy.vegetarian_master_taxonomy import (
    VEGETARIAN_TAXONOMY_REGISTRY,
    VEGETARIAN_SYNONYM_LOOKUP,
    get_veg_food_class,
    resolve_veg_food_by_name,
    filter_veg_by_family,
    VegetarianFoodClassRecord
)
from app.food_ai.datasets.vegetarian_hard_negatives import (
    VEGETARIAN_CONFUSION_REGISTRY,
    disambiguate_vegetarian_pair,
    KeralaSadyaItemDiscriminator,
    PaneerTofuPotatoDiscriminator,
    CountableVegetarianItemCounter,
    Section75NonNegotiableVegetarianVerifier
)
from app.food_ai.portion_engine.vegetarian_portions import (
    VegetarianPortionEngine,
    QualitativeVegetarianOilEstimator,
    VegetarianComponentMassSplitter,
    VEGETARIAN_PORTION_DATABASE
)
from app.food_ai.datasets.vegetarian_composite_decomposer import (
    SouthIndianVegetarianThaliDecomposer,
    NorthIndianVegetarianThaliDecomposer,
    KeralaSadyaDecomposer,
    GujaratiThaliDecomposer
)
from app.food_ai.nutrition_engine.vegetarian_recipes import (
    VegetarianRecipeNutritionCalculator,
    Section55VegetarianAnnotation,
    Section42VegetarianNutritionOutput,
    Section49UnknownVegetarianOutput,
    Section68FinalAppVegetarianOutput,
    Section67CalorieUncertaintyOutput,
    Section88VegetarianSingleOutput,
    Section51UserCorrectionRecord
)
from app.food_ai.inference_orchestrator import production_orchestrator


class TestPart12VegetarianTaxonomy:
    """Tests 14-level hierarchy, stable class IDs, regional datasets, and multilingual aliases."""

    def test_registered_class_count(self):
        assert len(VEGETARIAN_TAXONOMY_REGISTRY) >= 50

    def test_stable_class_id_format_section_54(self):
        sample = VEGETARIAN_TAXONOMY_REGISTRY["IND-VEG-TN-POR-BEAN-001"]
        assert sample.canonical_food_id.startswith("IND-VEG-")
        assert "TN" in sample.canonical_food_id
        assert "BEAN" in sample.canonical_food_id

    def test_14_level_hierarchy_completeness(self):
        sample = VEGETARIAN_TAXONOMY_REGISTRY["IND-VEG-TN-POR-BEAN-001"]
        h = sample.hierarchy
        assert h.level1_food == "Indian Food"
        assert h.level2_macro_category == "Vegetarian Food"
        assert h.level3_region == "South India"
        assert h.level4_state == "Tamil Nadu"
        assert h.level5_food_family == "Poriyal"
        assert h.level6_specific_dish == "Beans Poriyal"
        assert len(h.level7_variant) > 0
        assert h.level8_main_ingredient == "beans"
        assert "coconut" in h.level9_secondary_ingredients
        assert h.level10_cooking_method == "Stir-fried"
        assert h.level11_texture_consistency == "Dry"
        assert h.level12_portion_type == "weight_grams"
        assert h.level13_weight_g_default > 0
        assert len(h.level14_nutrition_ref_id) > 0

    def test_multilingual_synonym_resolution_section_53(self):
        # Tamil
        assert resolve_veg_food_by_name("பீன்ஸ் பொரியல்") is not None
        # Hindi
        assert resolve_veg_food_by_name("आलू गोभी") is not None
        # Malayalam
        assert resolve_veg_food_by_name("അവിയൽ") is not None
        # Gujarati
        assert resolve_veg_food_by_name("ઉંધિયું") is not None
        # English aliases
        assert resolve_veg_food_by_name("palak paneer") is not None
        assert resolve_veg_food_by_name("baingan bharta") is not None
        assert resolve_veg_food_by_name("chana masala") is not None
        assert resolve_veg_food_by_name("chokha") is not None

    def test_section_49_fallback_classes_exist(self):
        assert get_veg_food_class("IND-VEG-UNKNOWN-001") is not None
        assert get_veg_food_class("IND-VEG-CURRY-UNKNOWN-001") is not None
        assert get_veg_food_class("IND-VEG-PANEER-UNKNOWN-001") is not None


class TestPart12VegetarianHardNegativesAndVerifiers:
    """Tests 20+ confusion pairs, Sadya discriminator, White cube verification, and Section 75 rules."""

    def test_confusion_pairs_count(self):
        assert len(VEGETARIAN_CONFUSION_REGISTRY) >= 20

    def test_paneer_vs_potato_disambiguation(self):
        cues_paneer = {"texture": "porous_soft_curd", "has_porous_curd": True, "color": "opaque_milky_white"}
        res, conf, reason = disambiguate_vegetarian_pair("paneer_vs_potato", cues_paneer)
        assert "Paneer" in res
        assert conf >= 0.85

        cues_potato = {"texture": "waxy_starchy_translucent", "has_waxy_starch": True}
        res_p, conf_p, _ = disambiguate_vegetarian_pair("paneer_vs_potato", cues_potato)
        assert "Potato" in res_p
        assert conf_p >= 0.85

    def test_avial_vs_mixed_veg_curry_disambiguation(self):
        cues = {"cut": "long_batons", "has_baton_cuts": True, "has_coconut_curd_base": True}
        res, conf, _ = disambiguate_vegetarian_pair("avial_vs_mixed_veg_curry", cues)
        assert "Avial" in res
        assert conf >= 0.88

    def test_kerala_sadya_item_discriminator_section_6(self):
        # 1. Avial
        res_a, conf_a, _ = KeralaSadyaItemDiscriminator.discriminate({
            "has_baton_cuts": True,
            "has_coconut_curd_base": True
        })
        assert "Avial" in res_a

        # 2. Thoran
        res_t, conf_t, _ = KeralaSadyaItemDiscriminator.discriminate({
            "is_dry_stir_fry": True,
            "has_heavy_grated_coconut": True
        })
        assert "Thoran" in res_t

        # 3. Olan
        res_o, conf_o, _ = KeralaSadyaItemDiscriminator.discriminate({
            "has_white_coconut_milk": True,
            "has_ash_gourd": True
        })
        assert "Olan" in res_o

        # 4. Erissery
        res_e, conf_e, _ = KeralaSadyaItemDiscriminator.discriminate({
            "has_toasted_brown_coconut": True,
            "has_pumpkin": True
        })
        assert "Erissery" in res_e

        # 5. Kalan
        res_k, conf_k, _ = KeralaSadyaItemDiscriminator.discriminate({
            "is_thick_reduced_yogurt": True,
            "has_pepper_heat": True
        })
        assert "Kalan" in res_k

        # 6. Ambiguous fallback
        res_u, conf_u, _ = KeralaSadyaItemDiscriminator.discriminate({"color": "yellowish"})
        assert "uncertain" in res_u.lower()
        assert conf_u < 0.60

    def test_paneer_tofu_potato_white_cube_classifier_section_13_32(self):
        # Tofu crosshatch
        res_tofu, conf_t, _ = PaneerTofuPotatoDiscriminator.classify_white_cube({"has_crosshatch_press_marks": True})
        assert "Tofu" in res_tofu

        # Potato rounded starch
        res_pot, conf_p, _ = PaneerTofuPotatoDiscriminator.classify_white_cube({"has_translucent_starch": True})
        assert "Potato" in res_pot

        # True Paneer
        res_pan, conf_pn, _ = PaneerTofuPotatoDiscriminator.classify_white_cube({
            "has_porous_curd_matrix": True,
            "is_dairy_chalky_white": True
        })
        assert "Paneer" in res_pan

        # Vague white cube fallback
        res_v, conf_v, _ = PaneerTofuPotatoDiscriminator.classify_white_cube({})
        assert "uncertain" in res_v.lower()
        assert conf_v <= 0.50

    def test_countable_vegetarian_item_counter_section_38(self):
        res = CountableVegetarianItemCounter.count_and_estimate_mass("paneer_cube", 6)
        assert res["piece_count"] == 6
        assert res["total_estimated_mass_g"] == 108.0

        res_k = CountableVegetarianItemCounter.count_and_estimate_mass("kofta_ball", 2)
        assert res_k["piece_count"] == 2
        assert res_k["total_estimated_mass_g"] == 80.0

    def test_section_75_non_negotiable_rules(self):
        # White cube alone cannot assert paneer
        valid, msg = Section75NonNegotiableVegetarianVerifier.verify_prediction(
            candidate_dish="Paneer Butter Masala",
            visual_features={"is_unverified_white_cube": True}
        )
        assert valid is False
        assert "Section 75 Rule" in msg

        # Yellow color alone does not prove Dal
        valid_d, msg_d = Section75NonNegotiableVegetarianVerifier.verify_prediction(
            candidate_dish="Dal Tadka",
            visual_features={"color": "yellow", "has_lentil_evidence": False}
        )
        assert valid_d is False


class TestPart12VegetarianPortionsAndFatEstimator:
    """Tests portion configurations, qualitative fat tiers (Section 31), and mass splitter (Section 69)."""

    def test_portion_configs_exist(self):
        assert "poriyal_thoran" in VEGETARIAN_PORTION_DATABASE
        assert "kootu_avial" in VEGETARIAN_PORTION_DATABASE
        assert "paneer_gravy" in VEGETARIAN_PORTION_DATABASE

    def test_qualitative_oil_estimator_section_31(self):
        # Never exact 17g
        fat_info = QualitativeVegetarianOilEstimator.estimate_qualitative_oil({"oil_sheen": "high"})
        assert fat_info["fat_tier_name"] == "High visible oil"
        assert isinstance(fat_info["qualitative_fat_range_g"], tuple)
        assert "Section 31 compliant" in fat_info["non_negotiable_compliance"]

    def test_component_mass_splitter_mass_conservation_section_69(self):
        split = VegetarianComponentMassSplitter.split_dish(
            dish_name="Paneer Butter Masala",
            total_dish_weight_g=200.0,
            piece_count=5,
            piece_type="paneer_cube"
        )
        assert split.mass_conservation_verified is True
        assert round(split.inclusions_weight_g + split.gravy_weight_g, 1) == 200.0


class TestPart12VegetarianCompositeDecomposition:
    """Tests multi-item Thali decomposers adhering to anti-monolithic rule (Sections 34, 35, 58)."""

    def test_south_indian_veg_thali_deconstruction(self):
        res = SouthIndianVegetarianThaliDecomposer.decompose()
        assert len(res.components) == 9
        names = [c.name for c in res.components]
        assert any("Rice" in n for n in names)
        assert any("Sambar" in n for n in names)
        assert any("Rasam" in n for n in names)
        assert any("Kootu" in n for n in names)
        assert any("Poriyal" in n for n in names)
        assert res.anti_monolithic_verified is True
        assert res.total_calories_range["expected"] > 500

    def test_north_indian_veg_thali_deconstruction(self):
        res = NorthIndianVegetarianThaliDecomposer.decompose()
        assert len(res.components) == 8
        names = [c.name for c in res.components]
        assert any("Roti" in n for n in names)
        assert any("Dal" in n for n in names)
        assert any("Paneer" in n for n in names)
        assert any("Aloo Gobi" in n for n in names)
        assert res.total_calories_range["expected"] > 600

    def test_kerala_sadya_deconstruction_12_items(self):
        res = KeralaSadyaDecomposer.decompose()
        assert len(res.components) == 12
        names = [c.name for c in res.components]
        assert any("Avial" in n for n in names)
        assert any("Thoran" in n for n in names)
        assert any("Olan" in n for n in names)
        assert any("Erissery" in n for n in names)
        assert any("Kalan" in n for n in names)

    def test_gujarati_thali_deconstruction(self):
        res = GujaratiThaliDecomposer.decompose()
        assert len(res.components) == 8
        names = [c.name for c in res.components]
        assert any("Rotli" in n for n in names)
        assert any("Undhiyu" in n for n in names)
        assert any("Dhokla" in n for n in names)


class TestPart12VegetarianNutritionEngineAndSchemas:
    """Tests Section 55, 42, 49, 68, 67, 51 schemas."""

    def test_section_55_annotation(self):
        ann = VegetarianRecipeNutritionCalculator.generate_section_55_annotation(
            image_id="IMG_000123",
            dish_name="Beans Poriyal",
            region="Tamil Nadu"
        )
        assert isinstance(ann, Section55VegetarianAnnotation)
        assert ann.image_id == "IMG_000123"
        assert len(ann.food_items) == 1
        assert ann.food_items[0].name == "Beans Poriyal"

    def test_section_42_output(self):
        out = VegetarianRecipeNutritionCalculator.generate_section_42_output("North Indian Aloo Gobi")
        assert isinstance(out, Section42VegetarianNutritionOutput)
        assert out.weight_g > 0
        assert out.calories_kcal > 0
        assert out.protein_g > 0

    def test_section_49_unknown_fallbacks(self):
        gen = VegetarianRecipeNutritionCalculator.generate_section_49_unknown_fallback("general")
        assert gen.predicted_category == "Indian vegetarian dish — exact identity uncertain"
        assert gen.confidence < 0.50

        curry = VegetarianRecipeNutritionCalculator.generate_section_49_unknown_fallback("curry")
        assert curry.predicted_category == "Vegetable curry — exact type uncertain"

        paneer = VegetarianRecipeNutritionCalculator.generate_section_49_unknown_fallback("paneer")
        assert paneer.predicted_category == "Paneer-based dish — exact recipe uncertain"

    def test_section_68_app_output(self):
        out = VegetarianRecipeNutritionCalculator.generate_section_68_app_output([
            ("Kadai Paneer", "Medium", 91),
            ("Beans Poriyal", "Medium", 94)
        ])
        assert isinstance(out, Section68FinalAppVegetarianOutput)
        assert len(out.detected_dishes) == 2
        assert "–" in out.total_estimated_calories_range

    def test_section_51_user_correction_record(self):
        rec = VegetarianRecipeNutritionCalculator.record_user_correction(
            original_prediction="Paneer Butter Masala",
            user_correction="Kadai Paneer",
            image_reference="IMG_PANEER_001.jpg"
        )
        assert isinstance(rec, Section51UserCorrectionRecord)
        assert rec.final_confirmed_label == "Kadai Paneer"
        assert rec.active_learning_priority == "High"


class TestPart12VegetarianOrchestratorIntegration:
    """Tests orchestrator wiring for Part 12."""

    def test_orchestrator_analyze_vegetarian_dish(self):
        out = production_orchestrator.analyze_vegetarian_dish("Beans Poriyal")
        assert isinstance(out, Section88VegetarianSingleOutput)
        assert out.food_name == "Beans Poriyal"

    def test_orchestrator_analyze_south_indian_veg_thali(self):
        res = production_orchestrator.analyze_south_indian_veg_thali()
        assert len(res.components) == 9

    def test_orchestrator_analyze_north_indian_veg_thali(self):
        res = production_orchestrator.analyze_north_indian_veg_thali()
        assert len(res.components) == 8

    def test_orchestrator_analyze_kerala_sadya(self):
        res = production_orchestrator.analyze_kerala_sadya()
        assert len(res.components) == 12

    def test_orchestrator_analyze_gujarati_vegetarian_thali(self):
        res = production_orchestrator.analyze_gujarati_vegetarian_thali()
        assert len(res.components) == 8

    def test_orchestrator_disambiguate_vegetarian_pair(self):
        cues = {"texture": "porous_soft_curd", "has_porous_curd": True}
        dish, conf, _ = production_orchestrator.disambiguate_vegetarian_pair("paneer_vs_potato", cues)
        assert "Paneer" in dish

    def test_orchestrator_discriminate_kerala_sadya_items(self):
        res, conf, _ = production_orchestrator.discriminate_kerala_sadya_items({
            "has_baton_cuts": True,
            "has_coconut_curd_base": True
        })
        assert "Avial" in res

    def test_orchestrator_verify_paneer_vs_tofu_vs_potato(self):
        res, conf, _ = production_orchestrator.verify_paneer_vs_tofu_vs_potato({
            "has_crosshatch_press_marks": True
        })
        assert "Tofu" in res

    def test_orchestrator_verify_section_75_vegetarian_rule(self):
        valid, msg = production_orchestrator.verify_section_75_vegetarian_rule(
            candidate_dish="Paneer Butter Masala",
            visual_features={"is_unverified_white_cube": True}
        )
        assert valid is False
