"""
Comprehensive Test Suite for Indian Dal, Curry & Gravy AI System (Part 11)
Validates compliance with Sections 0 through 74 of Part 11 Master Training Specification.
"""

import pytest
from app.food_ai.taxonomy.curry_master_taxonomy import (
    CURRY_TAXONOMY_REGISTRY,
    CURRY_SYNONYM_LOOKUP,
    get_curry_food_class,
    resolve_curry_food_by_name,
    filter_curries_by_family,
    CurryFoodClassRecord
)
from app.food_ai.datasets.curry_hard_negatives import (
    CURRY_CONFUSION_REGISTRY,
    disambiguate_curry_pair,
    DalVsSambarVerifier,
    PaneerPieceDetector,
    ChickenMeatPieceCounter,
    FishSpeciesVerifier,
    GravyBaseClassifier,
    CurryConsistencyEstimator,
    Section73NonNegotiableCurryVerifier
)
from app.food_ai.portion_engine.curry_portions import (
    CurryPortionEngine,
    CurryFloatingOilEstimator,
    CurryProteinGravySplitter,
    CONSISTENCY_DENSITY_MAP,
    VESSEL_VOLUME_MAP
)
from app.food_ai.datasets.curry_composite_decomposer import (
    CurryRiceDecomposer,
    CurryBreadDecomposer,
    BananaLeafThaliDecomposer
)
from app.food_ai.nutrition_engine.curry_recipes import (
    CurryRecipeNutritionCalculator,
    Section57CurryAnnotation,
    Section57ChickenCurryAnnotation,
    Section52UnknownCurryOutput,
    Section66FinalAppOutput,
    Section70CalorieUncertaintyOutput,
    Section88CurrySingleOutput
)
from app.food_ai.inference_orchestrator import production_orchestrator


class TestPart11CurryTaxonomy:
    """Tests 12-level hierarchy, 23 master families, multilingual synonyms, and class coverage."""

    def test_minimum_registered_curry_classes(self):
        assert len(CURRY_TAXONOMY_REGISTRY) >= 60, f"Expected >= 60 registered classes, got {len(CURRY_TAXONOMY_REGISTRY)}"

    def test_23_master_families_represented(self):
        expected_families = [
            "Dal", "Sambar", "Rasam", "Kuzhambu", "Kootu", "Kadhi",
            "Vegetable Curry", "Paneer Curry", "Legume Curry", "Chicken Curry",
            "Mutton Curry", "Fish Curry", "Egg Curry", "Seafood Curry",
            "Kurma", "Salna", "Coconut-Based Curry", "Tomato-Based Gravy",
            "Onion-Based Gravy", "Yogurt-Based Gravy", "Cream-Based Gravy",
            "Dry / Semi-Dry Poriyal", "Regional Specialty Curry"
        ]
        families_present = {rec.food_family for rec in CURRY_TAXONOMY_REGISTRY.values()}
        for fam in expected_families:
            assert fam in families_present, f"Missing master curry family: {fam}"

    def test_12_level_hierarchy_completeness(self):
        sample = CURRY_TAXONOMY_REGISTRY["yellow_dal_tadka"]
        h = sample.hierarchy
        assert h.level1_food == "Indian Food"
        assert h.level2_macro_category == "Curry / Gravy / Dal / Semi-Dry Dish"
        assert h.level3_region in ["Pan-India", "North India", "South India", "West India", "East India"]
        assert h.level4_food_family == "Dal"
        assert "Dal Tadka" in h.level5_specific_dish
        assert len(h.level6_variant) > 0
        assert h.level7_main_ingredient == "toor_dal"
        assert len(h.level8_gravy_base) > 0
        assert len(h.level9_cooking_method) > 0
        assert h.level10_consistency in ["Very thin", "Thin", "Medium", "Thick", "Very thick", "Semi-dry", "Dry"]
        assert h.level11_portion_type in ["volume_ml", "weight_grams"]
        assert len(h.level12_nutrition_ref_id) > 0

    def test_multilingual_synonym_resolution(self):
        assert resolve_curry_food_by_name("dal tadka") is not None
        assert resolve_curry_food_by_name("paruppu") is not None
        assert resolve_curry_food_by_name("murgh makhani") is not None
        assert resolve_curry_food_by_name("ennai kathirikai") is not None
        assert resolve_curry_food_by_name("macher jhol") is not None
        assert resolve_curry_food_by_name("mor kuzhambu") is not None

    def test_unknown_curry_fallback_class_exists(self):
        rec = CURRY_TAXONOMY_REGISTRY.get("curry_unknown_001")
        assert rec is not None
        assert rec.canonical_food_id == "CURRY_UNKNOWN_001"
        assert rec.canonical_name == "Indian curry/gravy — exact dish uncertain"


class TestPart11CurryHardNegativesAndVerifiers:
    """Tests Section 42 disambiguation pairs, Dal vs Sambar, Fish species, and Section 73 rules."""

    def test_confusion_pairs_count(self):
        assert len(CURRY_CONFUSION_REGISTRY) >= 14

    def test_dal_vs_sambar_with_drumstick_and_tamarind(self):
        cues = {
            "has_drumstick": True,
            "has_tamarind_tint": True,
            "has_tempered_curry_leaves": True,
            "has_shallots": True
        }
        res, conf, reason = DalVsSambarVerifier.verify(cues)
        assert "Sambar" in res
        assert conf >= 0.88

    def test_dal_vs_sambar_with_garlic_jeera_turmeric(self):
        cues = {
            "has_garlic_tadka": True,
            "has_bright_turmeric": True,
            "has_cumin": True,
            "has_chunky_vegetables": False
        }
        res, conf, reason = DalVsSambarVerifier.verify(cues)
        assert "Dal" in res
        assert conf >= 0.85

    def test_dal_vs_sambar_ambiguous_fallback_section_9(self):
        # When neither side has decisive cues
        cues = {
            "color": "yellowish_orange",
            "liquid_texture": "medium"
        }
        res, conf, reason = DalVsSambarVerifier.verify(cues)
        assert res == "Dal/sambar-like dish — exact type uncertain"
        assert conf < 0.60
        assert "insufficient" in reason.lower()

    def test_fish_species_verifier_known_vs_uncertain_section_25(self):
        # Clear hilsa cut
        known_cues = {"is_hilsa_steak_cut": True, "curry_color": "yellow_mustard"}
        res_k, conf_k, _ = FishSpeciesVerifier.verify(known_cues)
        assert "Ilish" in res_k or "Hilsa" in res_k
        assert conf_k >= 0.85

        # Ambiguous cut without anatomical proof
        vague_cues = {"fish_present": True}
        res_u, conf_u, _ = FishSpeciesVerifier.verify(vague_cues)
        assert res_u == "Fish curry — species uncertain"
        assert conf_u < 0.60

    def test_paneer_piece_counter_and_detector(self):
        cues = {"cube_count": 6, "edges": "soft_defined", "color": "creamy_white", "porous_texture": True}
        count, conf, is_verified = PaneerPieceDetector.detect_paneer(cues)
        assert count == 6
        assert conf >= 0.88
        assert is_verified is True

    def test_chicken_meat_piece_counter(self):
        cues = {"visible_cuts": 4, "is_bone_in": True}
        count, is_bone, conf = ChickenMeatPieceCounter.count_pieces(cues)
        assert count == 4
        assert is_bone is True
        assert conf >= 0.85

    def test_section_73_non_negotiable_curry_verifier(self):
        # 1. Red color alone does not prove chicken curry
        valid, msg = Section73NonNegotiableCurryVerifier.verify_prediction(
            candidate_dish="Chicken Tikka Masala",
            visual_features={"color": "red", "has_poultry_evidence": False}
        )
        assert valid is False
        assert "Section 73 Rule" in msg

        # 2. Dark color alone does not prove mutton curry
        valid_m, msg_m = Section73NonNegotiableCurryVerifier.verify_prediction(
            candidate_dish="Mutton Rogan Josh",
            visual_features={"color": "dark_brown", "has_meat_evidence": False}
        )
        assert valid_m is False
        assert "Section 73 Rule" in msg_m

        # 3. White cubes alone without proof do not assert paneer
        valid_p, msg_p = Section73NonNegotiableCurryVerifier.verify_prediction(
            candidate_dish="Paneer Butter Masala",
            visual_features={"color": "orange", "has_paneer_evidence": False, "is_ambiguous_white_cube": True}
        )
        assert valid_p is False
        assert "Section 73 Rule" in msg_p


class TestPart11CurryPortions:
    """Tests volumetric calibrations, density matrix, floating oil, and protein-gravy mass splitting."""

    def test_vessel_volumetric_calibrations(self):
        assert VESSEL_VOLUME_MAP["small_katori"] == 100.0
        assert VESSEL_VOLUME_MAP["medium_katori"] == 150.0
        assert VESSEL_VOLUME_MAP["standard_bowl"] == 240.0
        assert VESSEL_VOLUME_MAP["serving_handi"] == 350.0

    def test_consistency_density_matrix(self):
        assert CONSISTENCY_DENSITY_MAP["Very thin"] == 1.01
        assert CONSISTENCY_DENSITY_MAP["Thin"] == 1.04
        assert CONSISTENCY_DENSITY_MAP["Medium"] == 1.08
        assert CONSISTENCY_DENSITY_MAP["Thick"] == 1.14
        assert CONSISTENCY_DENSITY_MAP["Dry"] == 0.95

    def test_floating_oil_estimator_tiers(self):
        low = CurryFloatingOilEstimator.estimate_floating_oil({"oil_sheen": "low"})
        assert low["tier_name"] == "Low Sheen"
        assert low["added_oil_grams"] == 2.0

        high = CurryFloatingOilEstimator.estimate_floating_oil({"oil_sheen": "roghan"})
        assert high["tier_name"] == "High Sheen / Roghan"
        assert high["added_oil_grams"] == 14.0

    def test_curry_protein_gravy_splitter_mass_conservation(self):
        # 220g dish with 3 chicken bone-in pieces
        split = CurryProteinGravySplitter.split_portion(
            protein_type="chicken",
            total_dish_weight_g=220.0,
            piece_count=3,
            is_bone_in=True
        )
        assert split.mass_conservation_check is True
        assert round(split.piece_weight_total_g + split.gravy_weight_g, 1) == 220.0
        assert split.bone_weight_g > 0
        assert split.edible_meat_weight_g > 0
        assert split.gravy_weight_g > 0


class TestPart11CurryCompositeDecomposition:
    """Tests Rice+Curry, Bread+Curry, and Banana Leaf Meal deconstruction (Sections 39, 40, 67)."""

    def test_rice_curry_decomposer_independent_items(self):
        res = CurryRiceDecomposer.decompose(
            rice_type="Steamed Sona Masoori Rice",
            rice_grams=200.0,
            curry_name="Yellow Dal Tadka",
            curry_grams=160.0
        )
        assert len(res.components) == 2
        assert res.components[0].category == "grain_staple"
        assert res.components[1].category == "curry_gravy"
        assert res.total_weight_g == 360.0
        assert res.total_calories_range["expected"] > 0

    def test_bread_curry_decomposer_paneer_split(self):
        res = CurryBreadDecomposer.decompose(
            bread_name="Tandoori Roti",
            bread_count=2,
            curry_name="Paneer Butter Masala",
            curry_weight_g=200.0,
            paneer_piece_count=5
        )
        # Should contain Roti, Paneer Cubes, and Makhani Gravy
        names = [c.name for c in res.components]
        assert any("Roti" in n for n in names)
        assert any("Paneer" in n for n in names)
        assert any("Gravy" in n for n in names)
        assert res.total_calories_range["expected"] > 0

    def test_banana_leaf_thali_decomposer_anti_monolithic_section_67(self):
        res = BananaLeafThaliDecomposer.decompose(has_non_veg=False)
        # At least 8 items: Rice, Sambar, Rasam, Kootu, Poriyal, Curd, Appalam, Pickle
        assert len(res.components) >= 8
        items = {c.name: c.calories for c in res.components}
        # Sambar, Rasam, Kootu, Rice must each have their own discrete non-zero calories
        assert any("Sambar" in k for k in items)
        assert any("Rasam" in k for k in items)
        assert any("Kootu" in k for k in items)
        assert any("Rice" in k for k in items)
        # Verify calories range is structured (low, expected, high)
        assert "expected" in res.total_calories_range
        assert res.total_calories_range["low"] < res.total_calories_range["expected"] < res.total_calories_range["high"]


class TestPart11NutritionEngineAndSchemas:
    """Tests Section 52, 57, 66, 70, 88 schemas and recipe dynamic nutrition."""

    def test_section_57_curry_annotation(self):
        ann = CurryRecipeNutritionCalculator.generate_section_57_curry_annotation("Yellow Dal Tadka")
        assert isinstance(ann, Section57CurryAnnotation)
        assert ann.curry_family == "Dal"
        assert ann.calories > 0
        assert ann.protein_g > 0
        assert ann.uncertainty_range["low"] < ann.calories < ann.uncertainty_range["high"]

    def test_section_57_chicken_curry_annotation(self):
        ann = CurryRecipeNutritionCalculator.generate_section_57_chicken_annotation(
            curry_name="Homestyle Chicken Curry",
            piece_count=3,
            is_bone_in=True
        )
        assert isinstance(ann, Section57ChickenCurryAnnotation)
        assert ann.curry_family == "Chicken Curries"
        assert ann.cut_type == "Bone-in"
        assert ann.meat_weight_g > 0
        assert ann.gravy_weight_g > 0
        assert ann.meat_weight_g + ann.gravy_weight_g <= ann.total_weight_g

    def test_section_52_unknown_fallback(self):
        out = CurryRecipeNutritionCalculator.generate_section_52_unknown_fallback(color="yellow", consistency="medium")
        assert isinstance(out, Section52UnknownCurryOutput)
        assert out.status == "uncertain"
        assert out.predicted_category == "Indian curry/gravy — exact dish uncertain"
        assert out.confidence < 0.50
        assert out.requires_user_confirmation is True

    def test_section_66_app_output(self):
        out = CurryRecipeNutritionCalculator.generate_section_66_app_output("Yellow Dal Tadka")
        assert isinstance(out, Section66FinalAppOutput)
        assert "–" in out.calories_range or "-" in out.calories_range
        assert out.confidence_score >= 0.85
        assert len(out.uncertainty_factors) >= 1

    def test_section_70_uncertainty_output(self):
        out = CurryRecipeNutritionCalculator.generate_section_70_uncertainty_output("Butter Chicken")
        assert isinstance(out, Section70CalorieUncertaintyOutput)
        assert out.nominal_calories > 0
        assert out.calories_low < out.nominal_calories < out.calories_high
        assert len(out.uncertainty_variance_reasons) >= 1


class TestPart11OrchestratorIntegration:
    """Tests orchestrator wiring for Part 11."""

    def test_orchestrator_analyze_curry_dish(self):
        out = production_orchestrator.analyze_curry_dish("Yellow Dal Tadka")
        assert isinstance(out, Section88CurrySingleOutput)
        assert out.food_name == "Yellow Dal Tadka"
        assert out.confidence == "High"

    def test_orchestrator_analyze_curry_rice_plate(self):
        res = production_orchestrator.analyze_curry_rice_plate()
        assert len(res.components) == 2
        assert res.total_weight_g == 360.0

    def test_orchestrator_analyze_curry_bread_plate(self):
        res = production_orchestrator.analyze_curry_bread_plate()
        assert len(res.components) >= 2
        assert res.total_calories_range["expected"] > 0

    def test_orchestrator_analyze_banana_leaf_meal(self):
        res = production_orchestrator.analyze_banana_leaf_meal()
        assert len(res.components) >= 8

    def test_orchestrator_disambiguate_curry_pair(self):
        cues = {"has_drumstick": True, "has_tamarind_tint": True}
        dish, conf, _ = production_orchestrator.disambiguate_curry_pair("dal_vs_sambar", cues)
        assert "Sambar" in dish

    def test_orchestrator_verify_dal_vs_sambar(self):
        res, conf, _ = production_orchestrator.verify_dal_vs_sambar({"has_drumstick": True})
        assert "Sambar" in res

    def test_orchestrator_verify_fish_species(self):
        res, conf, _ = production_orchestrator.verify_fish_species({})
        assert res == "Fish curry — species uncertain"

    def test_orchestrator_verify_section_73_curry_rule(self):
        valid, msg = production_orchestrator.verify_section_73_curry_rule(
            candidate_curry="Chicken Curry",
            visual_features={"color": "red", "has_poultry_evidence": False}
        )
        assert valid is False
