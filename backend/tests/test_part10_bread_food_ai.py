"""
Test Suite for Part 10: Indian Bread Recognition Master Training Specification
Tests Sections 1-87:
- Master Bread Taxonomy across 18 families (Sections 1-38, 61, 63, 64)
- 20+ Hard Negative Pair Disambiguations (Sections 5, 8, 11, 14, 16, 75, 84)
- Stack Detection with Occlusion Safety (Sections 44, 45)
- Kothu Parotta Component Segmentation (Section 14)
- Bread Stuffing & Dough Ratio Estimation (Sections 40, 41)
- Bread Fat & Ghee Modeling with Rule 84 Shine Guard (Sections 46, 47, 84)
- Composite Meal Decompositions (Roti-Dal-Sabzi, Paratha Thali, Chole Bhature) (Sections 50-60)
- Section 82 Single & Multi-Item Nutrition Output Engine
- Section 84/85 Unknown Bread Fallback
- Unified Orchestrator Integration
"""

import pytest
from app.food_ai.taxonomy.bread_master_taxonomy import (
    BREAD_TAXONOMY_REGISTRY,
    get_bread_food_class,
    resolve_bread_food_by_name,
    filter_breads_by_family,
    BreadFoodClassRecord
)
from app.food_ai.datasets.bread_hard_negatives import (
    BREAD_CONFUSION_REGISTRY,
    disambiguate_bread_pair,
    BreadStackDetector,
    KothuParottaSegmenter,
    BreadStuffingToppingDiscriminator,
    AlooParathaStuffingVerifier,
    MilletBreadGrainVerifier,
    Section64NonNegotiableBreadVerifier
)
from app.food_ai.datasets.bread_composite_decomposer import (
    BreadMealDecomposer,
    ParathaThaliDecomposer,
    CholeBhatureBreadDecomposer
)
from app.food_ai.portion_engine.bread_portions import (
    BREAD_PORTION_DATABASE,
    resolve_bread_portion,
    BreadFatEstimator,
    BreadStuffingDoughRatioEstimator
)
from app.food_ai.nutrition_engine.bread_recipes import (
    BreadRecipeNutritionCalculator,
    Section82BreadSingleOutput,
    Section82BreadMultiOutput,
    Section50BreadSingleAnnotation,
    Section50MultiFoodAnnotation,
    Section51UnknownBreadOutput,
    Section62FinalAppOutput
)
from app.food_ai.inference_orchestrator import production_orchestrator


class TestPart10BreadTaxonomy:
    """Tests bread taxonomy coverage and hierarchical attributes."""

    def test_taxonomy_coverage(self):
        assert len(BREAD_TAXONOMY_REGISTRY) >= 60
        # Verify Section 23: Dosa family separation as fermented rice/lentil pancake
        dosa_rec = get_bread_food_class("BREAD_PANCAKE_DOSA_PLAIN")
        assert dosa_rec is not None
        assert dosa_rec.bread_family == "Fermented rice/lentil pancake family"
        assert dosa_rec.hierarchy.level4_bread_family == "Fermented rice/lentil pancake family"
        # Verify unknown fallback exists
        assert "BREAD_UNKNOWN_001" in BREAD_TAXONOMY_REGISTRY

    def test_bread_hierarchy_levels(self):
        rec = get_bread_food_class("BREAD_ROTI_001")
        assert rec is not None
        assert rec.hierarchy.level1_food == "Indian Food"
        assert rec.hierarchy.level2_macro_category == "Bread"
        assert rec.hierarchy.level7_flour_grain == "whole_wheat"
        assert rec.cooking_method == "Tawa cooked"

    def test_multilingual_and_synonym_resolution(self):
        # Resolve by Hindi script
        rec_hi = resolve_bread_food_by_name("रोटी")
        assert rec_hi is not None
        assert rec_hi.canonical_food_id == "BREAD_ROTI_001"

        # Resolve by Tamil
        rec_ta = resolve_bread_food_by_name("பரோட்டா")
        assert rec_ta is not None
        assert rec_ta.canonical_food_id == "BREAD_PARATHA_005"

        # Resolve by alias
        rec_naan = resolve_bread_food_by_name("butter garlic naan")
        assert rec_naan is not None
        assert "naan" in rec_naan.canonical_name.lower()

    def test_filter_by_family(self):
        parathas = filter_breads_by_family("Paratha family")
        assert len(parathas) >= 3


class TestPart10HardNegativesAndDisambiguation:
    """Tests fine-grained bread confusion pairs per Section 5, 8, 11, etc."""

    def test_chapati_vs_phulka(self):
        # Balloon inflated -> Phulka
        res_phulka = disambiguate_bread_pair(
            pair_id="chapati_vs_phulka",
            visual_features={"puffing_state": "balloon_inflated", "cooking_method": "direct_flame"}
        )
        assert res_phulka["predicted_dish"] == "Flame-Puffed Phulka"
        assert res_phulka["confidence"] == "High"

        # Flat / tawa pressed -> Chapati
        res_chapati = disambiguate_bread_pair(
            pair_id="chapati_vs_phulka",
            visual_features={"puffing_state": "flat_or_partial_blister", "cooking_method": "tawa_pressed"}
        )
        assert res_chapati["predicted_dish"] == "Plain Chapati"

    def test_naan_vs_tandoori_roti(self):
        # Maida pale teardrop -> Naan
        res_naan = disambiguate_bread_pair(
            pair_id="naan_vs_tandoori_roti",
            visual_features={"flour_hue": "pale_cream_maida", "shape": "teardrop_oval"}
        )
        assert res_naan["predicted_dish"] == "Butter Naan"

        # Atta earthy brown circular -> Tandoori Roti
        res_roti = disambiguate_bread_pair(
            pair_id="naan_vs_tandoori_roti",
            visual_features={"flour_hue": "earthy_brown_atta", "shape": "circular_disk"}
        )
        assert res_roti["predicted_dish"] == "Tandoori Roti"

    def test_laccha_paratha_vs_kerala_parotta(self):
        # Translucent clapped maida leaves -> Kerala Parotta
        res_parotta = disambiguate_bread_pair(
            pair_id="laccha_paratha_vs_kerala_parotta",
            visual_features={"layer_technique": "clapped_spiral_leaves", "flour_type": "maida"}
        )
        assert res_parotta["predicted_dish"] == "Malabar / Kerala Parotta"

        # Atta concentric spiral rings -> Laccha Paratha
        res_laccha = disambiguate_bread_pair(
            pair_id="laccha_paratha_vs_kerala_parotta",
            visual_features={"layer_technique": "concentric_spiral_rings", "flour_type": "whole_wheat"}
        )
        assert res_laccha["predicted_dish"] == "Laccha Paratha"

    def test_puri_vs_bhatura(self):
        # Large fermented chewy oval -> Bhatura
        res_bhatura = disambiguate_bread_pair(
            pair_id="puri_vs_bhatura",
            visual_features={"bread_diameter_cm": 22.0, "flour_base": "fermented_maida"}
        )
        assert res_bhatura["predicted_dish"] == "Amritsari Bhatura"

        # Small whole wheat puff -> Puri
        res_puri = disambiguate_bread_pair(
            pair_id="puri_vs_bhatura",
            visual_features={"bread_diameter_cm": 11.0, "flour_base": "whole_wheat"}
        )
        assert res_puri["predicted_dish"] == "Whole Wheat Puri"


class TestPart10StackDetection:
    """Tests BreadStackDetector and occlusion handling per Sections 44 & 45."""

    def test_stack_without_occlusion(self):
        res = BreadStackDetector.detect_stack(
            visible_edges_count=3,
            top_bread_type="Chapati",
            observed_stack_height_mm=12.0
        )
        assert res.estimated_count_range == (3, 3)
        assert res.estimated_pieces_count == 3
        assert res.occlusion_flag is False
        assert res.confidence == "High"

    def test_stack_with_severe_occlusion(self):
        # 3 visible edges but 35mm height implies hidden bread layers
        res = BreadStackDetector.detect_stack(
            visible_edges_count=3,
            top_bread_type="Chapati",
            observed_stack_height_mm=35.0,
            rim_occlusion_angle_deg=55.0
        )
        assert res.occlusion_flag is True
        assert res.confidence in ["Medium", "Low"]
        assert res.estimated_count_range[1] > 3
        assert "Never invent hidden pieces" in res.notes


class TestPart10KothuParottaSegmentation:
    """Tests KothuParottaSegmenter per Section 14."""

    def test_kothu_segmentation(self):
        res = KothuParottaSegmenter.segment(
            has_egg=True,
            meat_type="chicken",
            portion_g=380.0
        )
        assert res.is_kothu_parotta is True
        assert res.primary_dish == "Chicken Kothu Parotta"
        assert len(res.components) >= 4

        # Verify parotta shreds are segregated from salna and meat
        comp_names = [c.component_name for c in res.components]
        assert any("Parotta Shreds" in n for n in comp_names)
        assert any("Chicken" in n for n in comp_names)
        assert any("Egg" in n for n in comp_names)
        assert any("Salna" in n for n in comp_names)

        # Mass balance check
        sum_mass = sum(c.weight_g for c in res.components)
        assert abs(sum_mass - 380.0) < 1.0


class TestPart10StuffingAndFatModeling:
    """Tests stuffing-dough ratio & fat estimator per Sections 40, 46, 47, 84."""

    def test_stuffing_dough_ratio(self):
        split = BreadStuffingDoughRatioEstimator.split_stuffed_bread("Aloo Paratha", total_mass_g=200.0)
        assert split.dough_mass_g == 110.0  # 55%
        assert split.stuffing_mass_g == 90.0   # 45%
        assert split.stuffing_type == "potato"

    def test_rule_84_shine_guard_never_assumes_butter(self):
        # Glossy shine without physical butter slab -> Medium fat, uncertain fat type, shine warning
        fat_res = BreadFatEstimator.estimate_fat(
            bread_canonical_name="Plain Chapati",
            surface_cues={"surface_sheen": "glossy", "butter_slab_present": False}
        )
        assert fat_res.fat_type_guess == "uncertain"
        assert "Never assume butter" in fat_res.rationale

    def test_butter_slab_detected(self):
        fat_res = BreadFatEstimator.estimate_fat(
            bread_canonical_name="Aloo Paratha",
            surface_cues={"butter_slab_present": True}
        )
        assert fat_res.fat_level == "Very High"
        assert fat_res.fat_type_guess == "butter"
        assert fat_res.butter_slab_detected is True

    def test_dry_phulka_zero_added_fat(self):
        fat_res = BreadFatEstimator.estimate_fat(
            bread_canonical_name="Flame-Puffed Phulka",
            surface_cues={"surface_sheen": "dry"}
        )
        assert fat_res.fat_level == "Very Low"
        assert fat_res.added_fat_typical_g < 1.0


class TestPart10CompositeDecomposition:
    """Tests meal decomposition for Roti-Dal-Sabzi, Paratha Thali, and Chole Bhature."""

    def test_bread_meal_decomposer(self):
        meal = BreadMealDecomposer.decompose(
            bread_type="Chapati",
            bread_count=2,
            has_dal=True,
            dal_type="Dal Tadka",
            has_sabzi=True,
            sabzi_type="Bhindi Masala"
        )
        assert meal.plate_type == "Roti + Dal + Sabzi Composite Meal"
        assert len(meal.components) >= 3
        # Chapati weight is 2 * 40g = 80g
        bread_comp = [c for c in meal.components if "Chapati" in c.item_name][0]
        assert bread_comp.weight_g == 80.0

    def test_paratha_thali_decomposer(self):
        thali = ParathaThaliDecomposer.decompose(
            paratha_type="Aloo Paratha",
            paratha_count=2,
            has_white_butter_slab=True
        )
        assert thali.plate_type == "Stuffed Paratha Thali Platter"
        names = [c.item_name for c in thali.components]
        assert any("Makhan" in n or "White Butter" in n for n in names)
        assert any("Dahi" in n or "Curd" in n for n in names)
        assert any("Achar" in n or "Pickle" in n for n in names)

    def test_chole_bhature_decomposer(self):
        cb = CholeBhatureBreadDecomposer.decompose(bhatura_count=2)
        assert cb.plate_type == "Chole Bhature Classic Platter"
        names = [c.item_name for c in cb.components]
        assert any("Bhatura" in n for n in names)
        assert any("Chole" in n for n in names)


class TestPart10NutritionAndOrchestrator:
    """Tests Section 82 single & composite output schemas and orchestrator integration."""

    def test_single_bread_nutrition_output(self):
        res = production_orchestrator.analyze_bread_dish(
            food_identifier="butter naan",
            piece_count=1,
            portion_category="Medium"
        )
        assert isinstance(res, Section82BreadSingleOutput)
        assert "Naan" in res.food_name
        assert "kcal" in res.estimated_calories_range
        assert res.calories_low < res.calories_expected < res.calories_high
        assert res.fat_level_estimate == "High"

    def test_section_84_unknown_bread_fallback(self):
        # Ambiguous or unknown bread -> Low confidence fallback per Rule 85
        res = production_orchestrator.analyze_bread_dish(
            food_identifier="unidentified flatbread",
            visual_cues={"low_visual_evidence": True}
        )
        assert res.confidence == "Low"
        assert res.canonical_id == "BREAD_UNKNOWN_001"
        assert res.requires_user_confirmation is True
        assert res.confirmation_prompt is not None

    def test_multi_item_bread_plate_output(self):
        items = [
            {"name": "Whole Wheat Chapati", "weight_g": 80.0, "calories": 208.0, "type": "bread"},
            {"name": "Dal Tadka", "weight_g": 180.0, "calories": 195.0, "type": "curry"},
            {"name": "Aloo Gobi Dry Sabzi", "weight_g": 150.0, "calories": 160.0, "type": "sabzi"}
        ]
        multi = production_orchestrator.analyze_bread_composite_plate(
            plate_title="Home Roti Meal",
            items=items
        )
        assert isinstance(multi, Section82BreadMultiOutput)
        assert len(multi.detected_items) == 3
        assert multi.total_estimated_weight_g == 410.0
        assert "kcal" in multi.total_estimated_calories_range
        assert multi.overall_confidence == "High"


class TestPart10ExtendedHardNegatives:
    """Tests Section 42 comprehensive confusion pairs."""

    def test_appam_vs_dosa_disambiguation(self):
        # Appam: bowl concave, spongy center, lacy edges
        res = disambiguate_bread_pair(
            pair_id="appam_vs_dosa",
            visual_features={"shape": "curved_bowl", "center": "thick_spongy_white", "edges": "lacy_frills"}
        )
        assert "Appam" in res["predicted_dish"]
        assert res["confidence"] == "High"

        # Dosa: flat crepe, golden brown roasted
        res_dosa = disambiguate_bread_pair(
            pair_id="appam_vs_dosa",
            visual_features={"shape": "flat_crepe", "center": "thin_crisp", "edges": "golden_brown_roasted"}
        )
        assert "Dosa" in res_dosa["predicted_dish"]

    def test_pathiri_vs_neer_dosa_disambiguation(self):
        # Pathiri: smooth opaque dry circular disc
        res_pathiri = disambiguate_bread_pair(
            pair_id="pathiri_vs_neer_dosa",
            visual_features={"surface": "smooth_opaque_dry", "presentation": "flat_circular_disc", "texture": "soft_dry_roti"}
        )
        assert "Pathiri" in res_pathiri["predicted_dish"]

        # Neer Dosa: folded quadrant, moist delicate crepe, lacy perforated
        res_neer = disambiguate_bread_pair(
            pair_id="pathiri_vs_neer_dosa",
            visual_features={"surface": "lacy_perforated_micro_holes", "presentation": "folded_quadrant", "texture": "moist_delicate_crepe"}
        )
        assert "Neer Dosa" in res_neer["predicted_dish"]

    def test_jowar_vs_bajra_roti_disambiguation(self):
        # Jowar: pale ivory cream
        res_jowar = disambiguate_bread_pair(
            pair_id="jowar_roti_vs_bajra_roti",
            visual_features={"color": "pale_ivory_cream_grey", "grain_type": "jowar_sorghum"}
        )
        assert "Jowar" in res_jowar["predicted_dish"]

        # Bajra: dark slate greenish grey
        res_bajra = disambiguate_bread_pair(
            pair_id="jowar_roti_vs_bajra_roti",
            visual_features={"color": "dark_slate_greenish_grey", "grain_type": "bajra_pearl_millet"}
        )
        assert "Bajra" in res_bajra["predicted_dish"]

    def test_roomali_roti_vs_thin_chapati_disambiguation(self):
        # Roomali: large 30-45 cm, handkerchief folded
        res_roomali = disambiguate_bread_pair(
            pair_id="roomali_roti_vs_thin_chapati",
            visual_features={"diameter_cm": "large_30_to_45cm", "presentation": "handkerchief_folded"}
        )
        assert "Roomali" in res_roomali["predicted_dish"]

    def test_puri_vs_kachori_disambiguation(self):
        # Puri: thin elastic hollow puff
        res_puri = disambiguate_bread_pair(
            pair_id="puri_vs_kachori",
            visual_features={"crust": "thin_elastic_hollow_puff", "stuffing": "none"}
        )
        assert "Puri" in res_puri["predicted_dish"]

        # Kachori: thick flaky shortcrust, spiced lentil core
        res_kachori = disambiguate_bread_pair(
            pair_id="puri_vs_kachori",
            visual_features={"crust": "thick_flaky_shortcrust", "stuffing": "spiced_lentil_core"}
        )
        assert "Kachori" in res_kachori["predicted_dish"]


class TestPart10SpecificationVerifiers:
    """Tests Section 9, 16, 34, 64 quality rules & verifiers."""

    def test_aloo_paratha_stuffing_verifier_hidden_fallback(self):
        # Section 9 Rule: If stuffing is hidden without visible bulges or cut section,
        # return 'Paratha — stuffed variant uncertain'
        dish, conf, reason = production_orchestrator.verify_aloo_paratha_stuffing(
            visual_cues={"has_stuffing_bulges": False, "has_cut_section_showing_filling": False, "stuffing_detected": "unknown"}
        )
        assert dish == "Paratha — stuffed variant uncertain"
        assert conf < 0.70
        assert "Section 9 Rule" in reason

    def test_aloo_paratha_stuffing_verifier_cut_section_success(self):
        dish, conf, reason = production_orchestrator.verify_aloo_paratha_stuffing(
            visual_cues={"has_cut_section_showing_filling": True, "stuffing_detected": "potato"}
        )
        assert dish == "Aloo Paratha"
        assert conf >= 0.90

    def test_millet_bread_grain_verifier_color_alone_fallback(self):
        # Section 16 Rule: Do not infer flour solely from color
        dish, conf, reason = production_orchestrator.verify_millet_bread_grain(
            visual_cues={"color": "grey", "grain_type": "unknown", "has_verified_millet_texture": False}
        )
        assert dish == "Millet-based flatbread — exact grain uncertain"
        assert conf < 0.70
        assert "Section 16 Rule" in reason

    def test_millet_bread_grain_verifier_texture_verified(self):
        dish, conf, reason = production_orchestrator.verify_millet_bread_grain(
            visual_cues={"color": "slate_grey", "grain_type": "bajra", "has_verified_millet_texture": True}
        )
        assert dish == "Bajra Roti"
        assert conf >= 0.90

    def test_section_64_rules_enforcement(self):
        # Rule: Naan and Kulcha must never be merged
        ok1, reason1 = production_orchestrator.verify_section_64_bread_rule(
            candidate_bread="Butter Naan",
            visual_features={"is_kulcha": True}
        )
        assert ok1 is False
        assert "Kulcha" in reason1

        # Rule: Surface shine alone does not prove butter
        ok2, reason2 = production_orchestrator.verify_section_64_bread_rule(
            candidate_bread="Butter Naan",
            visual_features={"surface_shine": "heavy_sheen", "has_melting_butter_slab": False}
        )
        assert ok2 is False
        assert "shine alone" in reason2

        # Rule: Chopped parotta with egg/meat must never be classified as plain parotta
        ok3, reason3 = production_orchestrator.verify_section_64_bread_rule(
            candidate_bread="Plain Parotta",
            visual_features={"is_chopped_shreds": True}
        )
        assert ok3 is False
        assert "plain parotta" in reason3


class TestPart10SchemasAndOutputs:
    """Tests Section 50, 51, 62 output schemas."""

    def test_section_50_single_bread_annotation_schema(self):
        ann: Section50BreadSingleAnnotation = production_orchestrator.generate_bread_section_50_single_annotation(
            food_category="bread",
            region="north_indian",
            food_name="aloo_paratha",
            variant="stuffed",
            flour="wheat",
            cooking_method="tawa",
            stuffing=["potato"],
            toppings=["butter"],
            count=2,
            estimated_weight_g=180.0,
            confidence=0.91
        )
        assert ann.food_category == "bread"
        assert ann.food_name == "aloo_paratha"
        assert ann.count == 2
        assert ann.estimated_weight_g == 180.0
        assert ann.confidence == 0.91
        assert "potato" in ann.stuffing
        assert "butter" in ann.toppings

    def test_section_50_multi_food_annotation_schema(self):
        multi: Section50MultiFoodAnnotation = production_orchestrator.generate_bread_section_50_multi_annotation(
            foods_spec=[
                {"name": "chapati", "count": 3, "estimated_weight_g": 120.0},
                {"name": "dal", "estimated_weight_g": 150.0},
                {"name": "vegetable_curry", "estimated_weight_g": 100.0}
            ]
        )
        assert len(multi.foods) == 3
        assert multi.foods[0].name == "chapati"
        assert multi.foods[0].count == 3
        assert multi.foods[1].name == "dal"
        assert multi.foods[2].name == "vegetable_curry"

    def test_section_51_unknown_bread_fallback_schema(self):
        res: Section51UnknownBreadOutput = production_orchestrator.generate_bread_section_51_unknown_fallback(
            prediction="Indian flatbread — exact type uncertain",
            fallback_alternative="Bread-like food — insufficient visual evidence",
            confidence=0.38
        )
        assert res.status == "uncertain"
        assert res.prediction == "Indian flatbread — exact type uncertain"
        assert res.confidence == 0.38
        assert res.user_confirmation_required is True

    def test_section_62_final_app_output_schema(self):
        out: Section62FinalAppOutput = production_orchestrator.generate_bread_section_62_final_app_output(
            meal_title="Paratha Breakfast Platter",
            paratha_count=2,
            paratha_weight_g=180.0,
            has_curd=True,
            curd_weight_g=100.0,
            has_pickle=True,
            pickle_weight_g=15.0
        )
        assert out.meal_title == "Paratha Breakfast Platter"
        assert len(out.detected_foods) == 3
        assert out.detected_foods[0].food_name == "Aloo Paratha"
        assert out.detected_foods[0].quantity == 2
        assert out.detected_foods[0].estimated_weight_g == 180.0
        assert out.detected_foods[1].food_name == "Curd"
        assert out.detected_foods[1].estimated_weight_g == 100.0
        assert out.detected_foods[2].food_name == "Pickle"
        assert out.detected_foods[2].estimated_weight_g == 15.0
        assert out.user_can_edit is True
        assert "food" in out.detected_foods[0].editable_fields
        assert "quantity" in out.detected_foods[0].editable_fields
        assert "weight" in out.detected_foods[0].editable_fields
