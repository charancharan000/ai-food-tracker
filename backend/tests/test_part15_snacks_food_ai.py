"""
Test Suite for Part 15 — Indian Snacks & Tiffin Master Specification
Tests:
- 14-Level Taxonomy Hierarchy & Stable Class IDs (IND-SNK-*, IND-TIF-*)
- Multilingual Synonym Lookups (Tamil, Telugu, Kannada, Hindi, Bengali, Marathi, Gujarati)
- Hard Negatives & Specialized Verifiers (Dhokla vs Khaman, Samosa vs Kachori, Vada vs Bonda, etc.)
- Portion Engine, Countable Piece Estimation, Two-Photo Mode & Qualitative Oil Tiers
- Composite Decomposers:
  * South Indian Tiffin Combo (Section 64 benchmark: Idli + Vada + Sambar + Chutney)
  * Samosa Plate with Chutneys
  * Pani Puri 6-Piece Assembly (Shells + Filling + Spicy/Sweet Pani + Boondi)
  * Aloo Tikki Chole Chaat
  * Vada Pav Assembly
  * Misal Pav Platter
  * Momo Platter (Steamed Veg, Chicken, Fried)
- Anti-Monolithic line item guarantees & accompaniment separation (Section 39)
- Section 74 Non-Negotiable Operational Rules validation
- Production Inference Orchestrator integration
- Active Learning User Correction audit store (Section 53)
"""

import pytest
from app.food_ai.taxonomy.snacks_tiffin_master_taxonomy import (
    SNACKS_TAXONOMY_REGISTRY,
    SNACKS_SYNONYM_LOOKUP,
    get_snack_record_by_id,
    resolve_snack_alias,
    SnackFoodClassRecord,
)
from app.food_ai.datasets.snacks_hard_negatives import (
    SNACKS_CONFUSION_REGISTRY,
    DhoklaVsKhamanVerifier,
    SamosaVsKachoriVerifier,
    VadaVsBondaVerifier,
    Section74NonNegotiableSnackVerifier,
    disambiguate_snack_pair,
)
from app.food_ai.portion_engine.snacks_portions import (
    SNACK_PORTION_DATABASE,
    CountablePieceEstimator,
    QualitativeOilEstimator,
    TwoPhotoPortionMode,
)
from app.food_ai.datasets.snacks_composite_decomposer import (
    TiffinComboDecomposer,
    SamosaPlateDecomposer,
    PaniPuriAssemblyDecomposer,
    AlooTikkiChaatDecomposer,
    VadaPavDecomposer,
    MisalPavDecomposer,
    MomoPlatterDecomposer,
)
from app.food_ai.nutrition_engine.snacks_recipes import (
    SnackRecipeNutritionCalculator,
    Section63SnackAnnotation,
    Section64MultiFoodOutput,
    Section64MultiFoodItem,
    Section51UnknownSnackFallback,
    Section53SnackUserCorrectionRecord,
)
from app.food_ai.inference_orchestrator import production_orchestrator


class TestSnacksTaxonomy:
    """Verifies Sections 1–13, 17–29, 40, 41, 51."""

    def test_stable_class_id_and_hierarchy_depth(self):
        record = get_snack_record_by_id("IND-SNK-TN-MEDHUVADAI-001")
        assert record is not None
        assert record.canonical_name == "Medhu Vadai"
        assert record.hierarchy.level1_food == "Indian Food"
        assert record.hierarchy.level2_macro_category == "Snacks & Tiffin"
        assert record.hierarchy.level3_region == "South India"
        assert record.hierarchy.level4_state == "Tamil Nadu"
        assert record.hierarchy.level5_snack_family == "Fried Snacks"
        assert record.hierarchy.level6_specific_food == "Medhu Vadai"
        assert record.hierarchy.level8_main_ingredient == "Urad Dal"
        assert record.hierarchy.level10_cooking_method == "Deep Fried"

    def test_multilingual_synonym_lookup(self):
        # Tamil
        rec_ta = resolve_snack_alias("மெது வடை / உளுந்து வடை")
        assert rec_ta is not None
        assert rec_ta.canonical_food_id == "IND-SNK-TN-MEDHUVADAI-001"

        # Telugu
        rec_te = resolve_snack_alias("పునుగులు")
        assert rec_te is not None
        assert rec_te.canonical_food_id == "IND-SNK-AP-PUNUGULU-001"

        # Kannada
        rec_kn = resolve_snack_alias("ಮದ್ದೂರು ವಡೆ")
        assert rec_kn is not None
        assert rec_kn.canonical_food_id == "IND-SNK-KA-MADDURVADA-001"

        # Marathi
        rec_mr = resolve_snack_alias("वडा पाव")
        assert rec_mr is not None
        assert rec_mr.canonical_food_id == "IND-SNK-MH-VADAPAV-001"

        # Gujarati
        rec_gu = resolve_snack_alias("ફાફડા")
        assert rec_gu is not None
        assert rec_gu.canonical_food_id == "IND-SNK-GJ-FAFDA-001"

        # Bengali
        rec_bn = resolve_snack_alias("সিঙাড়া")
        assert rec_bn is not None
        assert rec_bn.canonical_food_id == "IND-SNK-NI-SAMOSA-001"

    def test_canonical_id_standardization(self):
        expected_ids = [
            "IND-SNK-TN-MEDHUVADAI-001",
            "IND-SNK-TN-MASALAVADAI-001",
            "IND-SNK-TN-ONIONBAJJI-001",
            "IND-SNK-TN-POTATOBONDA-001",
            "IND-SNK-TN-MURUKKU-001",
            "IND-SNK-TN-THATTAI-001",
            "IND-SNK-TN-PANIYARAM-001",
            "IND-TIF-TN-IDLI-001",
            "IND-TIF-TN-MASALADOSA-001",
            "IND-TIF-TN-VENPONGAL-001",
            "IND-SNK-KL-PAZHAMPORI-001",
            "IND-SNK-KL-UNNIYAPPAM-001",
            "IND-SNK-KL-EGGBPUFF-001",
            "IND-SNK-KA-MADDURVADA-001",
            "IND-SNK-KA-MYSOREBONDA-001",
            "IND-SNK-AP-PUNUGULU-001",
            "IND-SNK-TS-SARVAPINDI-001",
            "IND-SNK-NI-SAMOSA-001",
            "IND-SNK-NI-PYAZKACHORI-001",
            "IND-SNK-NI-DALKACHORI-001",
            "IND-SNK-NI-ALOOTIKKI-001",
            "IND-SNK-NI-PANIPURI-001",
            "IND-SNK-MH-SEVPURI-001",
            "IND-SNK-MH-VADAPAV-001",
            "IND-SNK-MH-MISALPAV-001",
            "IND-SNK-MH-SABUDANAVADA-001",
            "IND-SNK-GJ-DHOKLA-001",
            "IND-SNK-GJ-KHAMAN-001",
            "IND-SNK-GJ-KHANDVI-001",
            "IND-SNK-GJ-FAFDA-001",
            "IND-SNK-WB-SINGARA-001",
            "IND-SNK-WB-JHALMURI-001",
            "IND-SNK-OD-DAHIBARA-001",
            "IND-SNK-BR-LITTICHOKHA-001",
            "IND-SNK-JH-DHUSKA-001",
            "IND-SNK-NE-VEGMOMO-001",
            "IND-SNK-NE-CHICKENMOMO-001",
            "IND-SNK-NE-FRIEDCHICKENMOMO-001",
            "IND-SNK-TN-MIXTURE-001",
            "IND-SNK-RJ-BHUJIA-001",
        ]
        for cid in expected_ids:
            rec = get_snack_record_by_id(cid)
            assert rec is not None, f"Missing expected snack canonical ID: {cid}"

    def test_standard_fallback_unknown_classes(self):
        fallback_ids = [
            "IND-SNK-UNKNOWN-001",
            "IND-SNK-FRIED-UNKNOWN-001",
            "IND-SNK-STEAMED-UNKNOWN-001",
            "IND-TIF-UNKNOWN-001",
            "IND-SNK-CHAAT-UNKNOWN-001",
        ]
        for fid in fallback_ids:
            rec = get_snack_record_by_id(fid)
            assert rec is not None, f"Missing fallback class: {fid}"
            assert "Unclassified" in rec.specific_food or "uncertain" in rec.alternate_names[0]


class TestSnacksHardNegatives:
    """Verifies Section 30 & Section 49 confusion pairs and specialized verifiers."""

    def test_dhokla_vs_khaman_verifier(self):
        # Case 1: Bright sunshine yellow, spongy aerated bounce, glistening syrup
        res_khaman = DhoklaVsKhamanVerifier.verify({
            "color": "bright yellow",
            "texture": "spongy hyper-aerated",
            "surface_moisture": "glistening with syrup soak",
            "fermented_appearance": False,
        })
        assert res_khaman["is_khaman"] is True
        assert res_khaman["predicted_food_id"] == "IND-SNK-GJ-KHAMAN-001"
        assert res_khaman["confidence"] >= 0.90

        # Case 2: Pale ivory, fermented micro-pores, firm texture
        res_dhokla = DhoklaVsKhamanVerifier.verify({
            "color": "pale ivory off-white",
            "texture": "firm steamed cake",
            "surface_moisture": "dry tempered",
            "fermented_appearance": True,
        })
        assert res_dhokla["is_khaman"] is False
        assert res_dhokla["predicted_food_id"] == "IND-SNK-GJ-DHOKLA-001"

    def test_samosa_vs_kachori_verifier(self):
        # Case 1: Pyramidal geometry with potato chunks
        res_samosa = SamosaVsKachoriVerifier.verify({
            "shape": "pyramidal triangle",
            "crust_texture": "smooth with ajwain",
            "filling": "potato green peas",
        })
        assert res_samosa["is_samosa"] is True
        assert res_samosa["predicted_food_id"] == "IND-SNK-NI-SAMOSA-001"

        # Case 2: Puffed circular disc with flaky blistered crust and dal paste
        res_kachori = SamosaVsKachoriVerifier.verify({
            "shape": "puffed circular disc",
            "crust_texture": "flaky blistered khasta",
            "filling": "spiced moong dal",
        })
        assert res_kachori["is_samosa"] is False
        assert res_kachori["predicted_food_id"] == "IND-SNK-NI-DALKACHORI-001"

    def test_vada_vs_bonda_verifier(self):
        # Case 1: Central hole perforation
        res_vada = VadaVsBondaVerifier.verify({
            "has_central_hole": True,
            "geometry": "toroid doughnut",
            "core_type": "aerated urad lentil crumb",
        })
        assert res_vada["is_vada"] is True
        assert res_vada["predicted_food_id"] == "IND-SNK-TN-MEDHUVADAI-001"

        # Case 2: Solid sphere with mashed potato core
        res_bonda = VadaVsBondaVerifier.verify({
            "has_central_hole": False,
            "geometry": "solid sphere",
            "core_type": "spiced potato mash",
        })
        assert res_bonda["is_vada"] is False
        assert res_bonda["predicted_food_id"] == "IND-SNK-TN-POTATOBONDA-001"

    def test_registered_confusion_pairs(self):
        expected_pairs = [
            "samosa_vs_kachori",
            "samosa_vs_curry_puff",
            "dhokla_vs_khaman",
            "dhokla_vs_idli",
            "vada_vs_bonda",
            "maddur_vada_vs_medhu_vada",
            "bajji_vs_pakoda",
            "vada_pav_vs_batata_vada",
            "pav_bhaji_vs_misal_pav",
            "momo_vs_kozhukattai",
            "murukku_vs_chakli",
        ]
        for pid in expected_pairs:
            assert pid in SNACKS_CONFUSION_REGISTRY
            pair = SNACKS_CONFUSION_REGISTRY[pid]
            assert len(pair.discriminative_visual_features) >= 2
            assert len(pair.discriminative_ingredient_features) >= 1


class TestPortionAndOilEstimators:
    """Verifies Sections 32, 33, 35, 36, 37."""

    def test_countable_piece_estimator_overlapping(self):
        # Clean separate pieces
        res_clean = CountablePieceEstimator.estimate_pieces(detected_instances_count=3, is_overlapping=False)
        assert res_clean["piece_count"] == 3
        assert res_clean["count_range"] == (3, 3)
        assert res_clean["count_uncertain"] is False

        # Overlapping stacked pile
        res_overlap = CountablePieceEstimator.estimate_pieces(detected_instances_count=4, is_overlapping=True)
        assert res_overlap["piece_count"] == 4
        assert res_overlap["count_uncertain"] is True
        assert res_overlap["user_confirmation_recommended"] is True

    def test_qualitative_oil_estimator_non_negotiable(self):
        # Steamed (Idli / Dhokla)
        oil_steamed = QualitativeOilEstimator.estimate_oil_level("steamed", sheen_score=0.1)
        assert oil_steamed["oil_tier"] == "Low visible oil"
        assert "exact" not in oil_steamed["oil_tier"].lower()

        # Deep-fried (Samosa / Vada)
        oil_fried = QualitativeOilEstimator.estimate_oil_level("deep fried", sheen_score=0.8, fried_blistering=True)
        assert oil_fried["oil_tier"] == "Deep-fried"
        assert oil_fried["oil_factor_multiplier"] > 1.20
        assert "Section 37" in oil_fried["disclaimer"]

        # Shallow fried (Aloo Tikki / Dosa)
        oil_shallow = QualitativeOilEstimator.estimate_oil_level("shallow fried", sheen_score=0.5)
        assert oil_shallow["oil_tier"] == "Moderate visible oil"

    def test_two_photo_portion_refinement(self):
        # Regular size samosas
        reg_samosa = TwoPhotoPortionMode.refine_portion(
            food_id="IND-SNK-NI-SAMOSA-001",
            top_view_piece_count=2,
            side_view_height_cm=3.5,
            reference_plate_diameter_cm=24.0,
        )
        assert reg_samosa["size_tier"] == "Regular"
        assert reg_samosa["piece_count"] == 2
        assert reg_samosa["total_estimated_weight_g"] == 170.0

        # Jumbo / Halwai tall samosas
        jumbo_samosa = TwoPhotoPortionMode.refine_portion(
            food_id="IND-SNK-NI-SAMOSA-001",
            top_view_piece_count=2,
            side_view_height_cm=5.5,
            reference_plate_diameter_cm=24.0,
        )
        assert jumbo_samosa["size_tier"] == "Jumbo / Extra Large"
        assert jumbo_samosa["total_estimated_weight_g"] > 170.0


class TestCompositeDecomposers:
    """Verifies Sections 14, 16, 25, 31, 39, 64."""

    def test_south_indian_tiffin_combo_section_64_benchmark(self):
        """Validates exact specification benchmark: Idli (4), Medhu Vada (2), Sambar, Coconut Chutney."""
        platter = TiffinComboDecomposer.decompose(idli_count=4, vada_count=2, sambar_volume_ml=120.0, chutney_volume_ml=40.0)
        assert platter.total_components_count == 4
        assert platter.zero_monolithic_guarantee is True

        comp_dict = {c.component_name: c for c in platter.components}
        assert "Idli" in comp_dict
        assert comp_dict["Idli"].count == 4
        assert comp_dict["Idli"].estimated_weight_g == 180.0

        assert "Medhu Vadai" in comp_dict
        assert comp_dict["Medhu Vadai"].count == 2
        assert comp_dict["Medhu Vadai"].estimated_weight_g == 100.0

        assert "Sambar" in comp_dict
        assert comp_dict["Sambar"].role == "accompaniment"

        assert "Coconut Chutney" in comp_dict
        assert comp_dict["Coconut Chutney"].role == "accompaniment"

        assert platter.total_plate_weight_g > 400.0
        assert platter.total_calories > 500.0

    def test_samosa_plate_decomposer_accompaniment_isolation(self):
        platter = SamosaPlateDecomposer.decompose(samosa_count=2, include_chutneys=True)
        assert platter.total_components_count >= 3
        comp_dict = {c.component_name: c for c in platter.components}
        assert "Punjabi Samosa" in comp_dict
        assert comp_dict["Punjabi Samosa"].count == 2
        assert comp_dict["Punjabi Samosa"].estimated_weight_g == 170.0
        assert "Saunth (Sweet Tamarind Chutney)" in comp_dict
        assert "Mint Coriander Chutney" in comp_dict

    def test_pani_puri_assembly_decomposer_section_16(self):
        """Verifies Section 16 rule: Never calculate entire plate as only pani puri."""
        platter = PaniPuriAssemblyDecomposer.decompose(puri_count=6)
        assert platter.total_components_count == 5
        comp_dict = {c.component_name: c for c in platter.components}
        assert "Crisp Hollow Puri Shells" in comp_dict
        assert comp_dict["Crisp Hollow Puri Shells"].count == 6
        assert "Potato & Black Chana Stuffing" in comp_dict
        assert "Teekha Mint-Coriander Spicy Water" in comp_dict
        assert "Meetha Tamarind Sweet Chutney Drop" in comp_dict
        assert "Crisp Boondi Floating Garnish" in comp_dict

    def test_delhi_aloo_tikki_chaat_decomposer(self):
        platter = AlooTikkiChaatDecomposer.decompose(tikki_count=2)
        assert platter.total_components_count == 6
        comp_dict = {c.component_name: c for c in platter.components}
        assert "Crispy Aloo Tikki Patties" in comp_dict
        assert comp_dict["Crispy Aloo Tikki Patties"].count == 2
        assert "Spiced Chole Curry Gravy" in comp_dict
        assert "Sweetened Whisked Dahi (Curd)" in comp_dict
        assert "Nylon Sev & Chopped Onions Garnish" in comp_dict

    def test_mumbai_vada_pav_decomposer(self):
        platter = VadaPavDecomposer.decompose(vada_pav_count=1)
        assert platter.total_components_count == 4
        comp_dict = {c.component_name: c for c in platter.components}
        assert "Batata Vada Fried Patty" in comp_dict
        assert "Ladi Pav Bread Bun" in comp_dict
        assert "Dry Red Garlic-Peanut Chutney" in comp_dict
        assert "Fried Salted Green Chilli" in comp_dict

    def test_maharashtra_misal_pav_decomposer(self):
        platter = MisalPavDecomposer.decompose(pav_count=2)
        assert platter.total_components_count == 5
        comp_dict = {c.component_name: c for c in platter.components}
        assert "Sprouted Moth Bean (Matki) Kat/Rassa Gravy" in comp_dict
        assert "Crunchy Farsan & Sev Topping" in comp_dict
        assert "Ladi Pav Buns" in comp_dict
        assert comp_dict["Ladi Pav Buns"].count == 2
        assert "Fresh Lemon Wedge" in comp_dict

    def test_momo_platter_decomposer(self):
        # Steamed Veg
        platter_veg = MomoPlatterDecomposer.decompose(momo_type="steamed_veg", momo_count=6)
        assert platter_veg.total_components_count == 3
        comp_veg = {c.component_name: c for c in platter_veg.components}
        assert "Steamed Veg Momo" in comp_veg
        assert comp_veg["Steamed Veg Momo"].count == 6

        # Fried Chicken
        platter_fried = MomoPlatterDecomposer.decompose(momo_type="fried_chicken", momo_count=6)
        comp_fried = {c.component_name: c for c in platter_fried.components}
        assert "Fried Chicken Momo" in comp_fried
        assert comp_fried["Fried Chicken Momo"].count == 6
        assert comp_fried["Fried Chicken Momo"].fat_g > comp_veg["Steamed Veg Momo"].fat_g


class TestNutritionEngineAndActiveLearning:
    """Verifies Sections 42, 43, 44, 53, 63, 64."""

    def test_snack_recipe_nutrition_calculator_piece_scaling(self):
        res_samosa = SnackRecipeNutritionCalculator.calculate_nutrition(
            food_id_or_name="Samosa",
            piece_count=3,
            preparation_style="commercial",
            include_accompaniments=True,
        )
        assert res_samosa["canonical_food_id"] == "IND-SNK-NI-SAMOSA-001"
        assert res_samosa["piece_count"] == 3
        assert res_samosa["snack_weight_g"] == 255.0 # 3 x 85g
        assert res_samosa["snack_nutrition"]["calories"] > 600.0
        assert len(res_samosa["accompaniments_breakdown"]) > 0
        assert res_samosa["total_plate_calories"] > res_samosa["snack_nutrition"]["calories"]

    def test_user_correction_audit_store(self):
        corr = SnackRecipeNutritionCalculator.record_user_correction(
            image_uri="https://storage.test/snack_photo_01.jpg",
            predicted_id="IND-SNK-NI-SAMOSA-001",
            predicted_name="Samosa",
            confidence=0.72,
            corrected_id="IND-SNK-NI-DALKACHORI-001",
            corrected_name="Dal Kachori",
            portion_weight_g=130.0,
            region="Uttar Pradesh",
        )
        assert corr.correction_id.startswith("corr-snk-")
        assert corr.user_corrected_name == "Dal Kachori"
        assert corr.original_prediction_name == "Samosa"


class TestSection74NonNegotiableRules:
    """Verifies Section 74 strict compliance."""

    def test_rejection_of_color_and_shape_only_predictions(self):
        payload_invalid = {
            "canonical_name": "Samosa",
            "decision_basis": "shape_only classification from triangle contour",
            "estimated_weight_g": 85.0,
        }
        val = Section74NonNegotiableSnackVerifier.validate_snack_output(payload_invalid)
        assert val["is_valid"] is False
        assert any("color or shape" in v for v in val["violations"])

    def test_rejection_of_exact_oil_milliliters(self):
        payload_invalid_oil = {
            "canonical_name": "Medhu Vadai",
            "decision_basis": "visual deep learning",
            "oil_estimation": "Exactly 12 ml oil absorbed",
            "estimated_weight_g": 90.0,
        }
        val = Section74NonNegotiableSnackVerifier.validate_snack_output(payload_invalid_oil)
        assert val["is_valid"] is False
        assert any("exact oil volume" in v for v in val["violations"])

    def test_rejection_of_accompaniment_mixed_in_snack_weight(self):
        payload_mixed = {
            "canonical_name": "Medhu Vadai",
            "decision_basis": "visual deep learning",
            "accompaniments": ["Sambar", "Coconut Chutney"],
            "estimated_weight_g": 250.0,
            "accompaniment_weight_g": 160.0,
            "is_accompaniment_mixed_in_snack_weight": True,
        }
        val = Section74NonNegotiableSnackVerifier.validate_snack_output(payload_mixed)
        assert val["is_valid"] is False
        assert any("Chutneys/Sambar/Sauces must not be combined" in v for v in val["violations"])

    def test_clean_compliant_payload(self):
        payload_valid = {
            "canonical_name": "Medhu Vadai",
            "decision_basis": "multimodal texture and geometry fusion",
            "oil_estimation": "Deep-fried (High visible oil)",
            "accompaniments": ["Coconut Chutney", "Sambar"],
            "estimated_weight_g": 90.0,
            "accompaniment_weight_g": 140.0,
            "is_accompaniment_mixed_in_snack_weight": False,
            "food_confidence": 0.96,
        }
        val = Section74NonNegotiableSnackVerifier.validate_snack_output(payload_valid)
        assert val["is_valid"] is True
        assert len(val["violations"]) == 0


class TestProductionInferenceOrchestratorSnacks:
    """Verifies orchestrator methods exposed in ProductionInferenceOrchestrator."""

    def test_orchestrator_analyze_snack_dish(self):
        res = production_orchestrator.analyze_snack_dish(dish_name_or_id="Medhu Vadai", piece_count=2)
        assert res["canonical_food_id"] == "IND-SNK-TN-MEDHUVADAI-001"
        assert res["piece_count"] == 2
        assert res["snack_weight_g"] == 90.0
        assert res["zero_monolithic_guarantee"] is True

    def test_orchestrator_tiffin_combo(self):
        res = production_orchestrator.analyze_tiffin_combo(idli_count=4, vada_count=2)
        assert res.total_components_count == 4
        assert res.total_plate_weight_g > 400.0

    def test_orchestrator_pani_puri(self):
        res = production_orchestrator.analyze_pani_puri_plate(puri_count=6)
        assert res.total_components_count == 5

    def test_orchestrator_vada_pav(self):
        res = production_orchestrator.analyze_snack_vada_pav(count=1)
        assert res.total_components_count == 4

    def test_orchestrator_misal_pav(self):
        res = production_orchestrator.analyze_snack_misal_pav(pav_count=2)
        assert res.total_components_count == 5

    def test_orchestrator_momo_platter(self):
        res = production_orchestrator.analyze_momo_platter(momo_type="steamed_chicken", momo_count=6)
        assert res.total_components_count == 3

    def test_orchestrator_dhokla_vs_khaman_verifier(self):
        res = production_orchestrator.verify_dhokla_vs_khaman({
            "color": "bright yellow",
            "texture": "spongy",
            "surface_moisture": "syrup soaked",
        })
        assert res["is_khaman"] is True
        assert res["predicted_food_id"] == "IND-SNK-GJ-KHAMAN-001"
