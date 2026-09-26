"""
Comprehensive Test Suite for Part 14 — Indian Sweets & Desserts Master Dataset & Recognition Specification
Verifies Sections 1 through 88, including:
- 13-level taxonomy and stable class IDs (IND-SWT-*)
- Multilingual synonym lookups
- Fallback classes (IND-SWT-UNKNOWN-*, IND-SWT-BOX-UNKNOWN-001)
- 25+ Hard Negative confusion pairs and disambiguation
- Diamond sweet verifier (Section 7: rejects 'Every diamond sweet = Kaju Katli')
- Spiral sweet verifier (Section 14 & 15: Jalebi != Jangri)
- White sweet verifier (Section 18: Rasgulla != Rasmalai != Sandesh)
- Section 87 Non-Negotiable Quality Rules verifier
- Qualitative sugar tiers (Section 51 & Rule 10)
- Fried sweet fat profiles (Section 52 & Rule 11)
- Dessert combination mass splitter (Section 67 & 68: Jalebi + Rabri, Rasmalai, Falooda)
- Multi-sweet platters and gift boxes (Diwali box, South Indian platter, Bengali platter, Ganesh Chaturthi prasad)
- Section 65 annotation, Section 85 uncertainty, Section 59 unknown, Section 81 app output, Section 61 user correction
- Production orchestrator wiring
"""

import pytest
from app.food_ai.taxonomy.sweets_master_taxonomy import (
    SWEETS_TAXONOMY_REGISTRY,
    SWEETS_SYNONYM_LOOKUP,
    get_sweet_food_class,
    resolve_sweet_food_by_name,
    SweetFoodClassRecord
)
from app.food_ai.datasets.sweets_hard_negatives import (
    SWEETS_CONFUSION_REGISTRY,
    disambiguate_sweet_pair,
    DiamondSweetVerifier,
    SpiralSweetVerifier,
    WhiteSweetVerifier,
    Section87NonNegotiableSweetVerifier
)
from app.food_ai.portion_engine.sweets_portions import (
    SWEET_PORTION_DATABASE,
    QualitativeSugarEstimator,
    FriedSweetFatEstimator,
    SweetComponentMassSplitter
)
from app.food_ai.datasets.sweets_composite_decomposer import (
    DiwaliMithaiBoxDecomposer,
    SouthIndianFestiveSweetPlatterDecomposer,
    BengaliMithaiThaliDecomposer,
    GaneshChaturthiPrasadDecomposer,
    JalebiRabriDessertPairingDecomposer,
    SweetCompositeDecompositionResult
)
from app.food_ai.nutrition_engine.sweets_recipes import (
    SweetRecipeNutritionCalculator,
    Section65SweetAnnotation,
    Section85CalorieUncertaintyOutput,
    Section59UnknownSweetOutput,
    Section61SweetUserCorrectionRecord,
    Section88SweetSingleOutput,
    Section81FinalAppSweetOutput
)
from app.food_ai.inference_orchestrator import production_orchestrator


class TestPart14SweetTaxonomy:
    """Tests taxonomy registration, IND-SWT-* stable IDs, 13-level hierarchy, and fallbacks."""

    def test_registered_classes_exist(self):
        assert len(SWEETS_TAXONOMY_REGISTRY) >= 20
        assert "IND-SWT-NI-KAJUKATLI-001" in SWEETS_TAXONOMY_REGISTRY
        assert "IND-SWT-NI-MOTICHOOR-001" in SWEETS_TAXONOMY_REGISTRY
        assert "IND-SWT-TN-MYSOREPAK-001" in SWEETS_TAXONOMY_REGISTRY
        assert "IND-SWT-TN-ADHIRASAM-001" in SWEETS_TAXONOMY_REGISTRY
        assert "IND-SWT-WB-RASGULLA-001" in SWEETS_TAXONOMY_REGISTRY
        assert "IND-SWT-NI-GULABJAMUN-001" in SWEETS_TAXONOMY_REGISTRY
        assert "IND-SWT-NI-JALEBI-001" in SWEETS_TAXONOMY_REGISTRY
        assert "IND-SWT-KL-PALPAYASAM-001" in SWEETS_TAXONOMY_REGISTRY
        assert "IND-SWT-MH-MODAK-001" in SWEETS_TAXONOMY_REGISTRY

    def test_stable_class_id_format_section_64(self):
        for cid, record in SWEETS_TAXONOMY_REGISTRY.items():
            assert record.canonical_food_id.startswith("IND-SWT-")

    def test_13_level_hierarchy_completeness(self):
        rec = get_sweet_food_class("IND-SWT-NI-KAJUKATLI-001")
        assert rec is not None
        h = rec.hierarchy
        assert h.level1_food == "Indian Food"
        assert h.level2_macro_category == "Sweets & Desserts"
        assert h.level3_region == "Pan-India"
        assert h.level5_sweet_family == "Kaju Katli"
        assert h.level6_specific_dish == "Kaju Katli"
        assert h.level8_base_ingredient == "Cashew"
        assert h.level9_cooking_method == "Pan-stirred"
        assert h.level10_syrup_state == "Dry"
        assert h.level11_filling_or_topping == "Silver Leaf"
        assert h.level12_portion_type == "piece_count"
        assert h.level13_nutrition_ref_id.startswith("REF-SWT-")

    def test_multilingual_synonym_resolution_section_63(self):
        # Tamil
        assert resolve_sweet_food_by_name("மைசூர் பாக்").canonical_food_id == "IND-SWT-TN-MYSOREPAK-001"
        assert resolve_sweet_food_by_name("அதிரசம்").canonical_food_id == "IND-SWT-TN-ADHIRASAM-001"
        # Bengali
        assert resolve_sweet_food_by_name("রসগোল্লা").canonical_food_id == "IND-SWT-WB-RASGULLA-001"
        assert resolve_sweet_food_by_name("সন্দেশ").canonical_food_id == "IND-SWT-WB-SANDESH-001"
        # Hindi
        assert resolve_sweet_food_by_name("गुलाब जामुन").canonical_food_id == "IND-SWT-NI-GULABJAMUN-001"
        assert resolve_sweet_food_by_name("काजू कतली").canonical_food_id == "IND-SWT-NI-KAJUKATLI-001"
        # Marathi
        assert resolve_sweet_food_by_name("उकडीचे मोदक").canonical_food_id == "IND-SWT-MH-MODAK-001"
        assert resolve_sweet_food_by_name("पुरणपोळी").canonical_food_id == "IND-SWT-MH-PURANPOLI-001"
        # Malayalam
        assert resolve_sweet_food_by_name("പാൽ പായസം").canonical_food_id == "IND-SWT-KL-PALPAYASAM-001"

    def test_fallback_classes_section_59_and_84(self):
        assert get_sweet_food_class("IND-SWT-UNKNOWN-001") is not None
        assert get_sweet_food_class("IND-SWT-MILK-UNKNOWN-001") is not None
        assert get_sweet_food_class("IND-SWT-SYRUP-UNKNOWN-001") is not None
        assert get_sweet_food_class("IND-SWT-BOX-UNKNOWN-001") is not None


class TestPart14SweetHardNegativesAndVerifiers:
    """Tests confusion registry, discriminators, and Section 87 rules."""

    def test_confusion_pairs_registered(self):
        assert len(SWEETS_CONFUSION_REGISTRY) >= 18
        assert "besan_laddu_vs_boondi_laddu" in SWEETS_CONFUSION_REGISTRY
        assert "boondi_laddu_vs_motichoor_laddu" in SWEETS_CONFUSION_REGISTRY
        assert "kaju_katli_vs_badam_barfi" in SWEETS_CONFUSION_REGISTRY
        assert "jalebi_vs_jangri" in SWEETS_CONFUSION_REGISTRY
        assert "gulab_jamun_vs_kala_jamun" in SWEETS_CONFUSION_REGISTRY
        assert "rasgulla_vs_rasmalai" in SWEETS_CONFUSION_REGISTRY
        assert "mysore_pak_vs_besan_barfi" in SWEETS_CONFUSION_REGISTRY
        assert "adhirasam_vs_medu_vadai" in SWEETS_CONFUSION_REGISTRY
        assert "modak_vs_kozhukattai" in SWEETS_CONFUSION_REGISTRY

    def test_besan_vs_boondi_laddu_disambiguation(self):
        d1, conf1, _ = disambiguate_sweet_pair("besan_laddu_vs_boondi_laddu", {
            "has_discrete_boondi_pearls": True
        })
        assert "Boondi Laddu" in d1
        assert conf1 >= 0.90

        d2, conf2, _ = disambiguate_sweet_pair("besan_laddu_vs_boondi_laddu", {
            "is_homogeneous_flour_paste": True
        })
        assert "Besan Laddu" in d2
        assert conf2 >= 0.90

    def test_boondi_vs_motichoor_pearl_diameter(self):
        d_moti, conf_m, _ = disambiguate_sweet_pair("boondi_laddu_vs_motichoor_laddu", {
            "has_micro_fine_pearls_1_to_2mm": True
        })
        assert "Motichoor" in d_moti
        assert conf_m >= 0.95

    def test_kaju_katli_vs_badam_barfi(self):
        d_kaju, conf_k, _ = disambiguate_sweet_pair("kaju_katli_vs_badam_barfi", {
            "is_smooth_matte_ivory_paste": True
        })
        assert "Kaju Katli" in d_kaju
        assert conf_k >= 0.95

    def test_jalebi_vs_jangri_rosette(self):
        d_jangri, conf_j, _ = disambiguate_sweet_pair("jalebi_vs_jangri", {
            "is_flower_rosette": True,
            "is_urad_dal_body": True
        })
        assert "Jangri" in d_jangri

        d_jal, _, _ = disambiguate_sweet_pair("jalebi_vs_jangri", {
            "is_thin_crisp_spiral": True
        })
        assert "Jalebi" in d_jal

    def test_rasgulla_vs_rasmalai(self):
        d_rm, _, _ = disambiguate_sweet_pair("rasgulla_vs_rasmalai", {
            "is_in_yellow_thickened_milk": True,
            "is_flattened_disc": True
        })
        assert "Rasmalai" in d_rm

        d_rg, _, _ = disambiguate_sweet_pair("rasgulla_vs_rasmalai", {
            "is_in_clear_syrup": True,
            "is_spherical_ball": True
        })
        assert "Rasgulla" in d_rg

    def test_diamond_sweet_verifier_section_7(self):
        # Gritty almond crumb rejects Kaju Katli claim
        valid, msg = DiamondSweetVerifier.verify_diamond_sweet(
            candidate="Kaju Katli",
            visual_features={"has_gritty_almond_crumb": True}
        )
        assert valid is False
        assert "Section 7" in msg

    def test_spiral_sweet_verifier_section_14_15(self):
        # Urad dal flower rosette rejects Jalebi claim
        valid, msg = SpiralSweetVerifier.verify_spiral_sweet(
            candidate="Jalebi",
            visual_features={"is_urad_dal_flower_rosette": True}
        )
        assert valid is False
        assert "Section 14" in msg

    def test_white_sweet_verifier_section_18(self):
        # White sweet lacking clear syrup rejects Rasgulla
        valid, msg = WhiteSweetVerifier.verify_white_sweet(
            candidate="Rasgulla",
            visual_features={"is_in_clear_sugar_syrup": False, "is_spongy_chhena_ball": False}
        )
        assert valid is False
        assert "Section 18" in msg

    def test_section_87_non_negotiable_rules(self):
        # Rule 1: Sweet by color alone
        v1, m1 = Section87NonNegotiableSweetVerifier.verify_prediction(
            candidate_dish="Yellow Sweet",
            visual_features={"color": "yellow"}
        )
        assert v1 is False
        assert "Rule 1" in m1

        # Rule 2: Sweet by shape alone
        v2, m2 = Section87NonNegotiableSweetVerifier.verify_prediction(
            candidate_dish="Some Sweet",
            visual_features={"shape_only": True}
        )
        assert v2 is False
        assert "Rule 2" in m2

        # Rule 3: Diamond sweet with almond != Kaju Katli
        v3, m3 = Section87NonNegotiableSweetVerifier.verify_prediction(
            candidate_dish="Kaju Katli",
            visual_features={"is_diamond_shape": True, "has_gritty_almond": True}
        )
        assert v3 is False
        assert "Rule 3" in m3

        # Rule 5: Spiral sweet with urad dal != Jalebi
        v5, m5 = Section87NonNegotiableSweetVerifier.verify_prediction(
            candidate_dish="Jalebi",
            visual_features={"is_urad_dal_flower_rosette": True}
        )
        assert v5 is False
        assert "Rule 5" in m5


class TestPart14SweetPortionsAndSugarFatEstimator:
    """Tests portion database, sugar estimator (Section 51), fat profile, and mass splitter."""

    def test_portion_configs_exist(self):
        assert "kaju_katli_piece" in SWEET_PORTION_DATABASE
        assert "laddu_piece" in SWEET_PORTION_DATABASE
        assert "gulab_jamun_piece" in SWEET_PORTION_DATABASE
        assert "mysore_pak_piece" in SWEET_PORTION_DATABASE

    def test_qualitative_sugar_estimator_section_51_rule_10(self):
        s_heavy = QualitativeSugarEstimator.estimate_sugar_tier("Heavy syrup")
        assert s_heavy["sugar_tier_name"] == "Syrup soaked / Heavy sugar infusion"
        assert isinstance(s_heavy["qualitative_sugar_range_g"], tuple)
        assert "Rule 10 compliant" in s_heavy["non_negotiable_compliance"]

        s_dry = QualitativeSugarEstimator.estimate_sugar_tier("Dry")
        assert s_dry["sugar_tier_name"] == "Moderate sugar contribution"

    def test_fried_sweet_fat_estimator_section_52(self):
        fat_mysore = FriedSweetFatEstimator.estimate_fat_profile("Mysore Pak", is_fried=False)
        assert fat_mysore["fat_profile_name"] == "Ghee-saturated / Ghee-fried"

        fat_jamun = FriedSweetFatEstimator.estimate_fat_profile("Gulab Jamun", is_fried=True)
        assert fat_jamun["fat_profile_name"] == "Deep-fried in oil/ghee"

        fat_modak = FriedSweetFatEstimator.estimate_fat_profile("Ukadiche Modak", is_fried=False, is_steamed=True)
        assert fat_modak["fat_profile_name"] == "Steamed / Unfried (Low fat)"

    def test_sweet_component_mass_splitter_jalebi_rabri(self):
        split = SweetComponentMassSplitter.split_dessert_combo("Jalebi with Rabri", total_weight_g=160.0)
        assert split.mass_conservation_verified is True
        assert "Crispy Jalebi" in split.components
        assert "Malai Rabri" in split.components
        assert round(sum(split.components.values()), 1) == 160.0

    def test_sweet_component_mass_splitter_rasmalai(self):
        split = SweetComponentMassSplitter.split_dessert_combo("Rasmalai", total_weight_g=120.0)
        assert split.mass_conservation_verified is True
        assert "Poached Chhena Discs" in split.components
        assert "Saffron Flavored Milk (Ras)" in split.components


class TestPart14SweetCompositeDecomposition:
    """Tests mixed sweet boxes and multi-dessert platters (Sections 48, 66, 82)."""

    def test_diwali_mithai_box_deconstruction_scenario_1(self):
        res = DiwaliMithaiBoxDecomposer.decompose()
        assert len(res.components) == 4
        names = [c.name for c in res.components]
        assert any("Kaju Katli" in n for n in names)
        assert any("Motichoor" in n for n in names)
        assert any("Mysore Pak" in n for n in names)
        assert any("Gulab Jamun" in n for n in names)
        assert res.anti_monolithic_verified is True
        assert res.no_double_counting_verified is True
        assert res.total_calories_range["expected"] > 1000

    def test_south_indian_festive_sweet_platter_scenario_2(self):
        res = SouthIndianFestiveSweetPlatterDecomposer.decompose()
        assert len(res.components) == 4
        names = [c.name for c in res.components]
        assert any("Pongal" in n for n in names)
        assert any("Payasam" in n for n in names)
        assert any("Adhirasam" in n for n in names)
        assert any("Kesari" in n for n in names)
        assert res.anti_monolithic_verified is True

    def test_bengali_mithai_thali_scenario_3(self):
        res = BengaliMithaiThaliDecomposer.decompose()
        assert len(res.components) == 3
        names = [c.name for c in res.components]
        assert any("Rasgulla" in n for n in names)
        assert any("Sandesh" in n for n in names)
        assert any("Mishti Doi" in n for n in names)

    def test_ganesh_chaturthi_prasad_scenario_4(self):
        res = GaneshChaturthiPrasadDecomposer.decompose()
        assert len(res.components) == 3
        names = [c.name for c in res.components]
        assert any("Modak" in n for n in names)
        assert any("Puran Poli" in n for n in names)
        assert any("Laddu" in n for n in names)

    def test_jalebi_rabri_pairing_scenario_5(self):
        res = JalebiRabriDessertPairingDecomposer.decompose()
        assert len(res.components) == 2
        names = [c.name for c in res.components]
        assert any("Jalebi" in n for n in names)
        assert any("Rabri" in n for n in names)
        assert res.no_double_counting_verified is True


class TestPart14SweetNutritionEngineAndSchemas:
    """Tests Section 65, 85, 59, 81, and 61 schemas."""

    def test_section_65_annotation(self):
        ann = SweetRecipeNutritionCalculator.generate_section_65_annotation(
            image_id="IMG_000123",
            dish_name="Adhirasam",
            region="Tamil Nadu",
            count=3,
            estimated_weight_g=105.0
        )
        assert isinstance(ann, Section65SweetAnnotation)
        assert ann.image_id == "IMG_000123"
        assert len(ann.food_items) == 1
        item = ann.food_items[0]
        assert item.class_id == "IND-SWT-TN-ADHIRASAM-001"
        assert item.count == 3
        assert item.estimated_weight_g == 105.0

    def test_section_85_uncertainty(self):
        unc = SweetRecipeNutritionCalculator.generate_section_85_uncertainty("Gulab Jamun", piece_count=2)
        assert isinstance(unc, Section85CalorieUncertaintyOutput)
        assert unc.calories_expected > 0
        assert unc.calorie_range["low"] < unc.calorie_range["high"]
        assert unc.piece_count == 2
        assert "Syrup soaked" in unc.sugar_contribution_tier

    def test_section_59_unknown_fallback(self):
        unk = SweetRecipeNutritionCalculator.generate_section_59_unknown("IMG_7777")
        assert isinstance(unk, Section59UnknownSweetOutput)
        assert unk.status == "unknown_confirmation_required"
        assert len(unk.confirmation_options) >= 5

    def test_section_81_app_output(self):
        comp = [
            {"food_name": "Kaju Katli", "piece_count": 4, "weight_g": 55.0, "calories": 250.0, "protein_g": 6.5, "fat_g": 14.5},
            {"food_name": "Gulab Jamun", "piece_count": 2, "weight_g": 70.0, "calories": 224.0, "protein_g": 3.2, "fat_g": 7.7}
        ]
        app_out = SweetRecipeNutritionCalculator.generate_section_81_app_output(comp)
        assert isinstance(app_out, Section81FinalAppSweetOutput)
        assert "Food Detected" in app_out.title
        assert app_out.total_calories_range["expected"] > 450

    def test_section_61_user_correction(self):
        rec = SweetRecipeNutritionCalculator.record_user_correction(
            image_id="IMG_00932",
            original_prediction="Kaju Katli",
            corrected_label="Badam Barfi",
            confidence=0.68
        )
        assert isinstance(rec, Section61SweetUserCorrectionRecord)
        assert rec.image_id == "IMG_00932"
        assert rec.corrected_label == "Badam Barfi"


class TestPart14SweetOrchestratorIntegration:
    """Tests production orchestrator wiring for Part 14."""

    def test_orchestrator_analyze_sweet_dish(self):
        out = production_orchestrator.analyze_sweet_dish("Kaju Katli", piece_count=4)
        assert isinstance(out, Section88SweetSingleOutput)
        assert "Kaju Katli" in out.food_name
        assert out.piece_count == 4
        assert out.total_portion_weight_g == 56.0

    def test_orchestrator_analyze_diwali_mithai_box(self):
        res = production_orchestrator.analyze_diwali_mithai_box()
        assert len(res.components) == 4

    def test_orchestrator_analyze_south_indian_sweet_platter(self):
        res = production_orchestrator.analyze_south_indian_sweet_platter()
        assert len(res.components) == 4

    def test_orchestrator_analyze_bengali_mithai_thali(self):
        res = production_orchestrator.analyze_bengali_mithai_thali()
        assert len(res.components) == 3

    def test_orchestrator_analyze_ganesh_chaturthi_prasad(self):
        res = production_orchestrator.analyze_ganesh_chaturthi_prasad()
        assert len(res.components) == 3

    def test_orchestrator_analyze_jalebi_rabri_pairing(self):
        res = production_orchestrator.analyze_jalebi_rabri_pairing()
        assert len(res.components) == 2

    def test_orchestrator_disambiguate_sweet_pair(self):
        dish, conf, _ = production_orchestrator.disambiguate_sweet_pair("kaju_katli_vs_badam_barfi", {
            "is_smooth_matte_ivory_paste": True
        })
        assert "Kaju Katli" in dish

    def test_orchestrator_verify_diamond_sweet(self):
        valid, msg = production_orchestrator.verify_diamond_sweet("Kaju Katli", {
            "has_gritty_almond_crumb": True
        })
        assert valid is False

    def test_orchestrator_verify_spiral_sweet(self):
        valid, msg = production_orchestrator.verify_spiral_sweet("Jalebi", {
            "is_urad_dal_flower_rosette": True
        })
        assert valid is False

    def test_orchestrator_verify_white_sweet(self):
        valid, msg = production_orchestrator.verify_white_sweet("Rasgulla", {
            "is_in_clear_sugar_syrup": False,
            "is_spongy_chhena_ball": False
        })
        assert valid is False

    def test_orchestrator_verify_section_87_sweet_rule(self):
        valid, msg = production_orchestrator.verify_section_87_sweet_rule("Kaju Katli", {
            "is_diamond_shape": True,
            "has_gritty_almond": True
        })
        assert valid is False
