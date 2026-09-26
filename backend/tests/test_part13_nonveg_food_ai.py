"""
Comprehensive Test Suite for Part 13 — Indian Non-Veg Master Dataset & Recognition Training Specification
Verifies Sections 1 through 90, including:
- 12-level taxonomy and stable class IDs (IND-NV-*)
- Multilingual synonym lookups
- Fallback classes (IND-NV-UNKNOWN-*, IND-NV-RM-UNKNOWN-001)
- 20+ Hard Negative confusion pairs and disambiguation
- Fish species classifier (Section 14 & Rule 2 fallback to 'Species uncertain')
- Meat anatomy cut classifier (Section 5 & 11 fallback to 'Cut uncertain')
- Bone state detection (Section 6)
- Piece counting with bounded ranges (Section 33)
- Bone-in vs edible meat deduction (Section 34 & Rule 9)
- Section 39 & Rule 11 Qualitative oil tiers
- Anti-monolithic composite meal deconstruction (Biryani platter, South Indian, North Indian, Kerala)
- Rule 14 Biryani decoupling (raita/salan not in biryani) and zero double counting
- Section 67 annotation, Section 70 uncertainty, Section 61 unknown, Section 79 app output, Section 64 correction
- Section 89 Non-negotiable quality rules verifier
- Production orchestrator wiring
"""

import pytest
from app.food_ai.taxonomy.nonveg_master_taxonomy import (
    NONVEG_TAXONOMY_REGISTRY,
    NONVEG_SYNONYM_LOOKUP,
    get_nonveg_food_class,
    resolve_nonveg_food_by_name,
    NonVegFoodClassRecord
)
from app.food_ai.datasets.nonveg_hard_negatives import (
    NONVEG_CONFUSION_REGISTRY,
    disambiguate_nonveg_pair,
    FishSpeciesClassifier,
    MeatAnatomyCutClassifier,
    BoneStateDetector,
    NonVegPieceCounter,
    Section89NonNegotiableNonVegVerifier
)
from app.food_ai.portion_engine.nonveg_portions import (
    NONVEG_PORTION_DATABASE,
    BoneToEdibleWeightCalculator,
    QualitativeNonVegOilEstimator,
    NonVegComponentMassSplitter,
    TwoPhotoPortionEngine
)
from app.food_ai.datasets.nonveg_composite_decomposer import (
    NonVegBiryaniPlatterDecomposer,
    SouthIndianNonVegMealDecomposer,
    NorthIndianNonVegMealDecomposer,
    KeralaNonVegMealDecomposer,
    NonVegCompositeDecompositionResult
)
from app.food_ai.nutrition_engine.nonveg_recipes import (
    NonVegRecipeNutritionCalculator,
    Section67NonVegAnnotation,
    Section70CalorieUncertaintyOutput,
    Section61UnknownNonVegOutput,
    Section64UserCorrectionRecord,
    Section88NonVegSingleOutput,
    Section79FinalAppNonVegOutput
)
from app.food_ai.inference_orchestrator import production_orchestrator


class TestPart13NonVegTaxonomy:
    """Tests taxonomy registration, IND-NV-* stable IDs, 12-level hierarchy, and fallbacks."""

    def test_registered_classes_exist(self):
        assert len(NONVEG_TAXONOMY_REGISTRY) >= 20
        assert "IND-NV-CH-TN-CHE-001" in NONVEG_TAXONOMY_REGISTRY
        assert "IND-NV-CH-PB-BUTTER-001" in NONVEG_TAXONOMY_REGISTRY
        assert "IND-NV-MT-TN-CHUKKA-001" in NONVEG_TAXONOMY_REGISTRY
        assert "IND-NV-FS-KL-MEEN-001" in NONVEG_TAXONOMY_REGISTRY
        assert "IND-NV-PR-KL-ROAST-001" in NONVEG_TAXONOMY_REGISTRY
        assert "IND-NV-EG-PAN-BOILED-001" in NONVEG_TAXONOMY_REGISTRY

    def test_stable_class_id_format_section_66(self):
        for cid, record in NONVEG_TAXONOMY_REGISTRY.items():
            assert record.canonical_food_id.startswith("IND-NV-")

    def test_12_level_hierarchy_completeness(self):
        rec = get_nonveg_food_class("IND-NV-CH-TN-CHE-001")
        assert rec is not None
        h = rec.hierarchy
        assert h.level1_food == "Indian Food"
        assert h.level2_macro_category == "Non-Vegetarian Food"
        assert h.level3_protein == "Chicken"
        assert h.level4_region == "South India"
        assert h.level5_state == "Tamil Nadu"
        assert h.level6_food_family == "Chicken Chettinad"
        assert h.level7_specific_dish == "Chicken Chettinad"
        assert "bone-in" in h.level8_variant.lower()
        assert h.level9_cooking_method == "Simmered"
        assert h.level10_bone_state == "bone_in"
        assert h.level11_portion_type == "weight_grams"
        assert h.level12_nutrition_ref_id.startswith("REF-NV-")

    def test_multilingual_synonym_resolution_section_65(self):
        # Tamil
        assert resolve_nonveg_food_by_name("செட்டிநாடு சிக்கன்").canonical_food_id == "IND-NV-CH-TN-CHE-001"
        # Hindi
        assert resolve_nonveg_food_by_name("बटर चिकन").canonical_food_id == "IND-NV-CH-PB-BUTTER-001"
        # Malayalam
        assert resolve_nonveg_food_by_name("കരിമീൻ പൊള്ളിച്ചത്").canonical_food_id == "IND-NV-FS-KL-POLLICHATHU-001"
        # Bengali
        assert resolve_nonveg_food_by_name("কষা মাংস").canonical_food_id == "IND-NV-MT-WB-KOSHA-001"
        # English colloquial
        assert resolve_nonveg_food_by_name("chicken 65").canonical_food_id == "IND-NV-CH-PAN-65-001"

    def test_fallback_classes_section_61_and_83(self):
        assert get_nonveg_food_class("IND-NV-UNKNOWN-001") is not None
        assert get_nonveg_food_class("IND-NV-CH-UNKNOWN-001") is not None
        assert get_nonveg_food_class("IND-NV-MT-UNKNOWN-001") is not None
        assert get_nonveg_food_class("IND-NV-FS-UNKNOWN-001") is not None
        assert get_nonveg_food_class("IND-NV-SF-UNKNOWN-001") is not None
        assert get_nonveg_food_class("IND-NV-EG-UNKNOWN-001") is not None
        assert get_nonveg_food_class("IND-NV-RM-UNKNOWN-001") is not None


class TestPart13NonVegHardNegativesAndVerifiers:
    """Tests confusion registry, discriminators, cut classifier, and Section 89 rules."""

    def test_confusion_pairs_registered(self):
        assert len(NONVEG_CONFUSION_REGISTRY) >= 15
        assert "chicken_vs_mutton" in NONVEG_CONFUSION_REGISTRY
        assert "chicken_65_vs_chicken_fry" in NONVEG_CONFUSION_REGISTRY
        assert "tandoori_vs_chicken_tikka" in NONVEG_CONFUSION_REGISTRY
        assert "fish_fry_vs_chicken_fry" in NONVEG_CONFUSION_REGISTRY
        assert "squid_vs_onion_rings" in NONVEG_CONFUSION_REGISTRY
        assert "boiled_egg_vs_paneer" in NONVEG_CONFUSION_REGISTRY
        assert "mutton_vs_beef" in NONVEG_CONFUSION_REGISTRY
        assert "biryani_vs_meat_pulao" in NONVEG_CONFUSION_REGISTRY

    def test_chicken_vs_mutton_disambiguation(self):
        dish_m, conf_m, _ = disambiguate_nonveg_pair("chicken_vs_mutton", {
            "has_marrow_bone": True,
            "is_dark_meat_fiber": True
        })
        assert "Mutton" in dish_m
        assert conf_m >= 0.90

        dish_c, conf_c, _ = disambiguate_nonveg_pair("chicken_vs_mutton", {
            "has_pale_fiber": True,
            "has_hollow_bone": True
        })
        assert "Chicken" in dish_c
        assert conf_c >= 0.90

    def test_chicken_65_vs_chicken_fry_disambiguation(self):
        dish, conf, _ = disambiguate_nonveg_pair("chicken_65_vs_chicken_fry", {
            "has_fried_curry_leaves": True,
            "is_crispy_red_bites": True
        })
        assert dish == "Chicken 65"

    def test_fish_species_classifier_section_14_and_rule_2(self):
        # Clear evidence: Seer fish center cut steak
        sp, conf, _ = FishSpeciesClassifier.classify_species({
            "thick_round_steak": True,
            "single_central_round_bone": True
        })
        assert "Seer Fish" in sp
        assert conf >= 0.90

        # Weak evidence: small curry photo -> MUST fallback to species uncertain
        sp_weak, conf_weak, msg = FishSpeciesClassifier.classify_species({
            "in_red_gravy": True
        })
        assert "Species Uncertain" in sp_weak
        assert "Section 14 compliant" in msg

    def test_meat_anatomy_cut_classifier_section_5_11(self):
        # Clear cut: drumstick
        cut, conf, _ = MeatAnatomyCutClassifier.classify_cut({"has_drumstick_shank_and_head": True})
        assert "Drumstick" in cut
        assert conf >= 0.90

        # Lollipop
        cut_l, _, _ = MeatAnatomyCutClassifier.classify_cut({"is_frenched_lollipop": True})
        assert "Lollipop" in cut_l

        # Ambiguous cut -> fallback
        cut_amb, _, msg = MeatAnatomyCutClassifier.classify_cut({"irregular_chunk": True})
        assert "Cut uncertain" in cut_amb
        assert "Section 5 compliant" in msg

    def test_bone_state_detector_section_6(self):
        state, conf, _ = BoneStateDetector.detect_bone_state({"has_exposed_bone": True})
        assert state == "bone_in"

        state_bl, _, _ = BoneStateDetector.detect_bone_state({"is_pure_boneless_cubes_or_tikka": True})
        assert state_bl == "boneless"

    def test_piece_counter_section_33(self):
        boxes = [{"bbox": [10, 10, 50, 50]}, {"bbox": [60, 60, 100, 100]}, {"bbox": [110, 110, 150, 150]}]
        res = NonVegPieceCounter.count_pieces("chicken_curry_piece", boxes)
        assert res["detected_piece_count"] == 3
        min_wt, max_wt = res["estimated_weight_range_g"]
        assert min_wt < max_wt
        assert "Section 33 compliant" in res["rule_compliance"]

    def test_section_89_non_negotiable_rules(self):
        # Rule 1: Meat by color alone without structure
        valid1, msg1 = Section89NonNegotiableNonVegVerifier.verify_prediction(
            candidate_dish="Generic Meat Curry",
            visual_features={"color": "red"}
        )
        assert valid1 is False
        assert "Rule 1" in msg1

        # Rule 3: Red curry alone != chicken
        valid3, msg3 = Section89NonNegotiableNonVegVerifier.verify_prediction(
            candidate_dish="Chicken Curry",
            visual_features={"color": "red", "has_poultry_evidence": False}
        )
        assert valid3 is False
        assert "Rule 3" in msg3

        # Rule 6: Rice + poured curry != biryani
        valid6, msg6 = Section89NonNegotiableNonVegVerifier.verify_prediction(
            candidate_dish="Chicken Biryani",
            visual_features={"is_poured_curry_over_white_rice": True}
        )
        assert valid6 is False
        assert "Rule 6" in msg6

        # Rule 28: Unverified red meat species
        valid28, msg28 = Section89NonNegotiableNonVegVerifier.verify_prediction(
            candidate_dish="Beef Curry",
            visual_features={"is_unverified_red_meat": True}
        )
        assert valid28 is False
        assert "Rule 28" in msg28


class TestPart13NonVegPortionsAndBoneDeduction:
    """Tests bone deduction (Section 34), qualitative oil (Section 39), and mass splitter."""

    def test_portion_configs_exist(self):
        assert "chicken_curry" in NONVEG_PORTION_DATABASE
        assert "mutton_curry" in NONVEG_PORTION_DATABASE
        assert "fish_curry" in NONVEG_PORTION_DATABASE
        assert "biryani_plate" in NONVEG_PORTION_DATABASE

    def test_bone_to_edible_weight_deduction_section_34_rule_9(self):
        # 200g bone-in chicken curry cut
        calc = BoneToEdibleWeightCalculator.calculate_edible_weight(
            total_portion_weight_g=200.0,
            protein_type="chicken",
            bone_state="bone_in",
            anatomical_cut="curry_cut"
        )
        # Never calculate 200g bone-in chicken = 200g edible!
        assert calc["edible_meat_weight_g"] < 200.0
        assert calc["bone_shell_weight_deducted_g"] > 0
        assert 140.0 <= calc["edible_meat_weight_g"] <= 155.0
        assert "Rule 9 compliant" in calc["non_negotiable_rule_compliance"]

    def test_crab_shell_deduction_section_34(self):
        # 300g whole crab
        calc_crab = BoneToEdibleWeightCalculator.calculate_edible_weight(
            total_portion_weight_g=300.0,
            protein_type="crab",
            bone_state="bone_in",
            anatomical_cut="whole"
        )
        # Crab shell is 50-60% of weight
        assert calc_crab["edible_meat_weight_g"] <= 160.0
        assert calc_crab["bone_shell_weight_deducted_g"] >= 140.0

    def test_qualitative_oil_estimator_section_39_rule_11(self):
        fat_info = QualitativeNonVegOilEstimator.estimate_qualitative_oil({"oil_sheen": "high"})
        assert fat_info["fat_tier_name"] == "High visible oil"
        assert isinstance(fat_info["qualitative_fat_range_g"], tuple)
        assert "Rule 11 compliant" in fat_info["non_negotiable_compliance"]

    def test_component_mass_splitter_mass_conservation(self):
        split = NonVegComponentMassSplitter.split_dish(
            dish_name="Chicken Curry",
            total_dish_weight_g=200.0,
            piece_count=4,
            piece_type="chicken_curry_piece"
        )
        assert split.mass_conservation_verified is True
        assert round(split.pieces_weight_g + split.gravy_weight_g, 1) == 200.0


class TestPart13NonVegCompositeDecomposition:
    """Tests multi-food non-veg meal deconstruction and Rule 14 Biryani decoupling."""

    def test_biryani_platter_deconstruction_and_rule_14(self):
        res = NonVegBiryaniPlatterDecomposer.decompose()
        assert len(res.components) == 5
        names = [c.name for c in res.components]
        assert any("Biryani" in n for n in names)
        assert any("65" in n for n in names)
        assert any("Egg" in n for n in names)
        assert any("Raita" in n for n in names)
        assert any("Salan" in n for n in names)

        # Rule 14 verification: Raita and Salan have is_biryani_side=True and separate weights
        raita = next(c for c in res.components if "Raita" in c.name)
        salan = next(c for c in res.components if "Salan" in c.name)
        biryani = next(c for c in res.components if "Biryani" in c.name)

        assert raita.is_biryani_side is True
        assert salan.is_biryani_side is True
        assert biryani.weight_g == 350.0  # Biryani weight alone
        assert res.anti_monolithic_verified is True
        assert res.no_double_counting_verified is True

    def test_south_indian_nonveg_meal_deconstruction(self):
        res = SouthIndianNonVegMealDecomposer.decompose()
        assert len(res.components) == 8
        names = [c.name for c in res.components]
        assert any("Rice" in n for n in names)
        assert any("Chettinad" in n for n in names)
        assert any("Fish Fry" in n for n in names)
        assert any("Egg" in n for n in names)
        assert any("Poriyal" in n for n in names)
        assert any("Rasam" in n for n in names)
        assert res.anti_monolithic_verified is True

    def test_north_indian_nonveg_meal_deconstruction(self):
        res = NorthIndianNonVegMealDecomposer.decompose()
        assert len(res.components) == 6
        names = [c.name for c in res.components]
        assert any("Butter Chicken" in n for n in names)
        assert any("Tikka" in n for n in names)
        assert any("Naan" in n for n in names)
        assert any("Rice" in n for n in names)

    def test_kerala_nonveg_meal_deconstruction(self):
        res = KeralaNonVegMealDecomposer.decompose()
        assert len(res.components) == 6
        names = [c.name for c in res.components]
        assert any("Matta" in n for n in names)
        assert any("Fish Curry" in n for n in names)
        assert any("Pollichathu" in n for n in names)
        assert any("Chicken Roast" in n for n in names)


class TestPart13NonVegNutritionEngineAndSchemas:
    """Tests Section 67, 70, 61, 79, and 64 schemas."""

    def test_section_67_annotation(self):
        ann = NonVegRecipeNutritionCalculator.generate_section_67_annotation(
            image_id="IMG_00001",
            dish_name="Chicken Chettinad",
            region="Tamil Nadu",
            portion_g=150.0,
            piece_count=6,
            bone_state="bone_in"
        )
        assert isinstance(ann, Section67NonVegAnnotation)
        assert ann.image_id == "IMG_00001"
        assert len(ann.food_items) == 1
        item = ann.food_items[0]
        assert item.class_id == "IND-NV-CH-TN-CHE-001"
        assert item.portion_g == 150.0
        assert item.bone_state == "bone_in"

    def test_section_70_uncertainty(self):
        unc = NonVegRecipeNutritionCalculator.generate_section_70_uncertainty("Mutton Rogan Josh")
        assert isinstance(unc, Section70CalorieUncertaintyOutput)
        assert unc.calories_expected > 0
        assert unc.calorie_range["low"] < unc.calorie_range["high"]
        assert unc.bone_weight_deducted_g > 0

    def test_section_61_unknown_fallback(self):
        unk = NonVegRecipeNutritionCalculator.generate_section_61_unknown("IMG_9999")
        assert isinstance(unk, Section61UnknownNonVegOutput)
        assert unk.status == "unknown_confirmation_required"
        assert len(unk.confirmation_options) >= 5

    def test_section_79_app_output(self):
        comp = [
            {"food_name": "Chicken Chettinad", "weight_g": 150.0, "piece_count": 6, "calories": 273.0, "protein_g": 26.2, "fat_g": 16.2},
            {"food_name": "Steamed Rice", "weight_g": 180.0, "calories": 234.0, "protein_g": 4.7, "fat_g": 0.7}
        ]
        app_out = NonVegRecipeNutritionCalculator.generate_section_79_app_output(comp)
        assert isinstance(app_out, Section79FinalAppNonVegOutput)
        assert "Food Detected" in app_out.title
        assert app_out.total_calories_range["expected"] > 500

    def test_section_64_user_correction(self):
        rec = NonVegRecipeNutritionCalculator.record_user_correction(
            image_id="IMG_00992",
            original_prediction="Chicken Curry",
            user_correction="Mutton Curry",
            confidence=0.62
        )
        assert isinstance(rec, Section64UserCorrectionRecord)
        assert rec.image_id == "IMG_00992"
        assert rec.user_correction == "Mutton Curry"


class TestPart13NonVegOrchestratorIntegration:
    """Tests orchestrator wiring for Part 13."""

    def test_orchestrator_analyze_nonveg_dish(self):
        out = production_orchestrator.analyze_nonveg_dish("Chicken Chettinad", portion_category="Medium")
        assert isinstance(out, Section88NonVegSingleOutput)
        assert "Chettinad" in out.food_name
        assert out.bone_state == "bone_in"
        assert out.bone_weight_deducted_g > 0

    def test_orchestrator_analyze_biryani_platter(self):
        res = production_orchestrator.analyze_biryani_platter()
        assert len(res.components) == 5

    def test_orchestrator_analyze_south_indian_nonveg_meal(self):
        res = production_orchestrator.analyze_south_indian_nonveg_meal()
        assert len(res.components) == 8

    def test_orchestrator_analyze_north_indian_nonveg_meal(self):
        res = production_orchestrator.analyze_north_indian_nonveg_meal()
        assert len(res.components) == 6

    def test_orchestrator_analyze_kerala_nonveg_meal(self):
        res = production_orchestrator.analyze_kerala_nonveg_meal()
        assert len(res.components) == 6

    def test_orchestrator_disambiguate_nonveg_pair(self):
        dish, conf, _ = production_orchestrator.disambiguate_nonveg_pair("fish_fry_vs_chicken_fry", {
            "has_myotome_flaking": True,
            "has_central_vertebrae": True
        })
        assert "Fish Fry" in dish

    def test_orchestrator_classify_fish_species(self):
        sp, conf, _ = production_orchestrator.classify_fish_species({
            "flat_diamond_body": True,
            "silver_white_shiny_skin": True
        })
        assert "Pomfret" in sp

    def test_orchestrator_classify_meat_anatomy_cut(self):
        cut, conf, _ = production_orchestrator.classify_meat_anatomy_cut({
            "has_drumstick_shank_and_head": True
        })
        assert "Drumstick" in cut

    def test_orchestrator_detect_bone_state(self):
        bstate, conf, _ = production_orchestrator.detect_bone_state({
            "has_exposed_bone": True
        })
        assert bstate == "bone_in"

    def test_orchestrator_verify_section_89_nonveg_rule(self):
        valid, msg = production_orchestrator.verify_section_89_nonveg_rule(
            candidate_dish="Chicken Curry",
            visual_features={"color": "red"}
        )
        assert valid is False
