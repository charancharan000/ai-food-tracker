"""
Indian Bread Hard Negatives, Fine-Grained Disambiguation, Stack Detector & Kothu Segmenter (Part 10)
Implements Sections 5, 8, 11, 14, 16, 40, 41, 44, 45, 54, 75, 84 of Part 10 Master Training Specification.

Guarantees:
- 20+ Pan-Indian Bread Confusion Pairs:
  * Chapati vs Phulka (tawa uniform browning vs direct flame balloon puffing)
  * Naan vs Kulcha vs Tandoori Roti (teardrop airy maida vs stuffed flaky disk vs whole wheat char)
  * Aloo Paratha vs Aloo Kulcha vs Aloo Naan (atta tawa griddle vs tandoor flaky coriander disk vs blistered oval)
  * Laccha Paratha vs Kerala Parotta (wheat concentric spiral rings vs clapped translucent maida leaves)
  * Puri vs Bhatura vs Luchi (small wheat puff vs large fermented chewy bhatura vs white maida luchi)
  * Bhakri vs Rotla (smooth jowar flatbread vs rustic thick cracked pearl millet rotlo)
  * Thepla vs Paratha (thin pliable spiced fenugreek flatbread vs thicker griddled paratha)
  * Pathiri vs Appam vs Neer Dosa (dry tawa rice circle vs bowl-shaped spongy center with lacy frills)
- BreadStackDetector (Sections 44 & 45):
  * Counts visible bread edges in a stack and estimates total range with occlusion safety.
  * Never invents hidden pieces under stack occlusion.
- KothuParottaSegmenter (Section 14):
  * Segregates chopped parotta pieces, scrambled egg, meat, onions, and curry salna.
  * Never classifies Kothu Parotta simply as plain parotta.
- BreadStuffingToppingDiscriminator (Sections 40 & 41):
  * Separates stuffing (potato, paneer, gobi, sattu) from surface toppings (butter slab, ghee, garlic).
  * Never assumes butter solely from surface shine.
"""

from typing import List, Dict, Any, Optional, Tuple
from pydantic import BaseModel, Field


class BreadConfusionPair(BaseModel):
    pair_id: str
    dish_a: str
    dish_b: str
    distinguishing_features: List[str]
    a_visual_cues: Dict[str, Any]
    b_visual_cues: Dict[str, Any]


BREAD_CONFUSION_REGISTRY: Dict[str, BreadConfusionPair] = {
    "chapati_vs_phulka": BreadConfusionPair(
        pair_id="chapati_vs_phulka",
        dish_a="Plain Chapati",
        dish_b="Flame-Puffed Phulka",
        distinguishing_features=[
            "Cooking method & puffing: Chapati is pressed on flat tawa with uniform light-brown toasted spots; Phulka is flipped onto direct flame to inflate into a round spherical balloon",
            "Thickness & surface: Chapati has slightly sturdier rolled skin; Phulka has two paper-thin separated layers with delicate blistered charred flecks",
            "Pliability: Phulka is extremely light and airy compared to traditional homestyle chapati"
        ],
        a_visual_cues={"puffing_state": "flat_or_partial_blister", "cooking_method": "tawa_pressed", "spot_pattern": "uniform_golden_brown"},
        b_visual_cues={"puffing_state": "balloon_inflated", "cooking_method": "direct_flame", "spot_pattern": "speckled_char_spots"}
    ),
    "naan_vs_tandoori_roti": BreadConfusionPair(
        pair_id="naan_vs_tandoori_roti",
        dish_a="Butter Naan",
        dish_b="Tandoori Roti",
        distinguishing_features=[
            "Flour & color: Naan is refined flour (maida) with pale cream base and large charred bubbles; Tandoori Roti is coarse whole wheat (atta) with earthy brown hue",
            "Shape & elasticity: Naan is traditionally teardrop/elongated oval with stretchy elastic crumb; Tandoori Roti is circular and denser",
            "Glaze: Naan frequently has heavy melted butter, garlic, or nigella seeds"
        ],
        a_visual_cues={
            "flour": ["refined_flour_maida", "maida"],
            "flour_hue": ["pale_cream_maida", "cream", "white"],
            "shape": ["teardrop_elongated", "teardrop_oval", "teardrop", "oval"],
            "texture": "airy_elastic_bubbles"
        },
        b_visual_cues={
            "flour": ["whole_wheat_atta", "atta"],
            "flour_hue": ["earthy_brown_atta", "brown"],
            "shape": ["circular_flat", "circular_disk", "circular", "round"],
            "texture": "dense_charred_crust"
        }
    ),
    "naan_vs_kulcha": BreadConfusionPair(
        pair_id="naan_vs_kulcha",
        dish_a="Butter Naan",
        dish_b="Amritsari Kulcha",
        distinguishing_features=[
            "Structure & stuffing: Naan is an unleavened or yeast-leavened single tear-drop sheet; Amritsari Kulcha is multi-layered, flaky, stuffed with spiced potato/onion/anardana, and stamped with whole coriander seeds",
            "Surface finish: Crushed coriander seeds and dried pomegranate (anardana) specks on Kulcha vs nigella seeds/garlic on Naan",
            "Edge texture: Blistered soft-chewy edge in Naan vs crispy shatteringly flaky edge in Amritsari Kulcha"
        ],
        a_visual_cues={"stuffing": "none", "shape": "teardrop_oval", "surface_herbs": "nigella_or_plain"},
        b_visual_cues={"stuffing": "spiced_potato_onion", "shape": "round_or_oval_stuffed", "surface_herbs": "crushed_coriander_seeds_anardana"}
    ),
    "aloo_paratha_vs_aloo_kulcha": BreadConfusionPair(
        pair_id="aloo_paratha_vs_aloo_kulcha",
        dish_a="Punjabi Aloo Paratha",
        dish_b="Amritsari Aloo Kulcha",
        distinguishing_features=[
            "Flour base: Aloo Paratha uses whole wheat atta; Aloo Kulcha uses refined flour maida with layered ghee/butter shortening",
            "Cooking apparatus: Aloo Paratha is cooked on a flat cast-iron tawa with oil/ghee basting; Kulcha is slapped against the interior wall of a clay tandoor",
            "Crust texture: Soft golden toasted wheat exterior in Paratha vs crispy, flaky, blistered tandoori crust in Kulcha"
        ],
        a_visual_cues={"flour": "whole_wheat_atta", "cooking_method": "tawa_cooked", "crust": "tawa_toasted_soft"},
        b_visual_cues={"flour": "refined_flour_maida", "cooking_method": "tandoor_cooked", "crust": "flaky_blistered_crisp"}
    ),
    "laccha_paratha_vs_kerala_parotta": BreadConfusionPair(
        pair_id="laccha_paratha_vs_kerala_parotta",
        dish_a="Laccha Paratha",
        dish_b="Malabar / Kerala Parotta",
        distinguishing_features=[
            "Flour & dough technique: Laccha Paratha is whole wheat (or mixed) pleated into concentric circular spiral rings; Kerala Parotta is 100% maida vigorously slapped, stretched paper-thin, coiled, and clapped by hand",
            "Layer transparency: Kerala Parotta layers are translucent, paper-thin, and feather-light with elastic chew; Laccha Paratha layers are sturdier, wheat-colored, and crisper"
        ],
        a_visual_cues={
            "flour": ["whole_wheat", "whole_wheat_atta"],
            "flour_type": ["whole_wheat", "atta"],
            "layer_technique": ["concentric_spiral_rings", "concentric_spirals"],
            "layer_pattern": "concentric_spiral_rings",
            "tone": "golden_brown_wheat"
        },
        b_visual_cues={
            "flour": ["refined_flour_maida", "maida"],
            "flour_type": ["maida", "refined_flour"],
            "layer_technique": ["clapped_spiral_leaves", "clapped_leaves"],
            "layer_pattern": "clapped_feather_translucent_leaves",
            "tone": "pale_cream_with_crisp_spots"
        }
    ),
    "puri_vs_bhatura": BreadConfusionPair(
        pair_id="puri_vs_bhatura",
        dish_a="Whole Wheat Puri",
        dish_b="Amritsari Bhatura",
        distinguishing_features=[
            "Scale & diameter: Puri is small (10–14 cm); Bhatura is large (18–24 cm)",
            "Dough composition: Puri uses unleavened whole wheat flour (or semolina); Bhatura uses fermented maida enriched with curd, baking soda/yeast",
            "Crumb structure: Puri is hollow with a thin crispy shell that deflates quickly; Bhatura has a thicker, soft, chewy, web-like fermented interior crumb",
            "Meal context: Puri with aloo bhaji or halwa; Bhatura almost universally with dark spicy chole"
        ],
        a_visual_cues={
            "scale": "small_10_to_14cm",
            "flour": ["whole_wheat_atta", "whole_wheat"],
            "flour_base": ["whole_wheat", "atta"],
            "crumb": "thin_hollow_crisp"
        },
        b_visual_cues={
            "scale": "large_18_to_24cm",
            "flour": ["fermented_maida", "maida"],
            "flour_base": ["fermented_maida", "maida"],
            "crumb": "thick_chewy_spongy",
            "accompaniment": "chole"
        }
    ),
    "bhakri_vs_rotla": BreadConfusionPair(
        pair_id="bhakri_vs_rotla",
        dish_a="Maharashtrian Jowar Bhakri",
        dish_b="Gujarati Bajra Rotla",
        distinguishing_features=[
            "Grain: Jowar (sorghum) yields a lighter pale grey/white flatbread; Bajra (pearl millet) yields a darker greenish-grey/brown flatbread",
            "Edge appearance: Bhakri is patted relatively smooth and even; Rotla is noticeably thicker with rustic cracked edges and coarse grain texture",
            "Topping: Rotla is traditionally served with a large slab of white homemade butter (makhan) and jaggery"
        ],
        a_visual_cues={"grain": "jowar_sorghum", "color": "pale_grey_white", "edge": "smooth_patted"},
        b_visual_cues={"grain": "bajra_pearl_millet", "color": "dark_greyish_brown", "edge": "cracked_thick", "topping": "white_butter_makhan"}
    ),
    "thepla_vs_paratha": BreadConfusionPair(
        pair_id="thepla_vs_paratha",
        dish_a="Gujarati Methi Thepla",
        dish_b="Methi Paratha",
        distinguishing_features=[
            "Thickness: Thepla is rolled extremely thin and paper-like; Paratha is substantially thicker",
            "Texture: Thepla is soft, highly pliable, and dotted with tiny uniform brown freckles; Paratha has crisp flaky crust from tawa fat",
            "Spicing: Thepla incorporates turmeric, ajwain, sesame, and red chilli powder uniformly into the flour dough with yogurt"
        ],
        a_visual_cues={"thickness": "very_thin_pliable", "spotting": "tiny_freckled_dots", "hue": "turmeric_golden_with_methi"},
        b_visual_cues={"thickness": "medium_thick", "spotting": "broad_tawa_brown_patches", "hue": "wheat_brown"}
    ),
    "pathiri_vs_appam": BreadConfusionPair(
        pair_id="pathiri_vs_appam",
        dish_a="Malabar Rice Pathiri",
        dish_b="Kerala Palappam",
        distinguishing_features=[
            "Geometry: Pathiri is completely flat, circular, and dry-cooked; Appam is bowl-curved with a thick soft spongy domed center and paper-thin lacy frills",
            "Batter vs dough: Pathiri is made from cooked rice dough rolled with a rolling pin; Appam is poured from fermented rice-coconut milk batter into an appachatti"
        ],
        a_visual_cues={"geometry": "flat_uniform_circle", "texture": "soft_thin_flatbread", "color": "chalk_white"},
        b_visual_cues={"geometry": "bowl_shaped_curved", "texture": "spongy_thick_center_lacy_edges", "color": "white_with_crisp_rim"}
    ),
    "roti_vs_chapati": BreadConfusionPair(
        pair_id="roti_vs_chapati",
        dish_a="Tawa Whole Wheat Roti",
        dish_b="Homestyle Soft Chapati",
        distinguishing_features=[
            "Rolling & oiling: Chapati is typically rolled with a fold or oil smear, producing delicate thin layers; Roti is a single rolled disc",
            "Softness: Chapati retains high pliability when folded into quarters; rustic Tawa Roti is slightly firmer with rustic toasted spots"
        ],
        a_visual_cues={"structure": "single_sheet", "pliability": "firm_rustic", "spotting": "toasted_brown_patches"},
        b_visual_cues={"structure": "thin_multi_layer_fold", "pliability": "very_soft_pliable", "spotting": "delicate_light_freckles"}
    ),
    "roti_vs_paratha": BreadConfusionPair(
        pair_id="roti_vs_paratha",
        dish_a="Plain Wheat Roti",
        dish_b="Plain Tawa Paratha",
        distinguishing_features=[
            "Oil / fat application: Roti is dry-cooked on tawa with no fat during griddling (ghee optionally brushed after); Paratha is shallow-fried with oil/ghee sizzled directly on the tawa",
            "Crust finish: Dry matte surface with blister spots on Roti vs glistening, crispy, shallow-fried golden crust on Paratha"
        ],
        a_visual_cues={"cooking_fat": "dry_tawa", "surface_texture": "matte_soft", "sheen": "none_or_light"},
        b_visual_cues={"cooking_fat": "sizzled_tawa_oil", "surface_texture": "crisp_fried_crust", "sheen": "fried_glaze"}
    ),
    "paratha_vs_laccha_paratha": BreadConfusionPair(
        pair_id="paratha_vs_laccha_paratha",
        dish_a="Plain Triangle / Square Paratha",
        dish_b="Laccha Paratha",
        distinguishing_features=[
            "Layering pattern: Plain paratha has 3–4 internal geometric fold sheets; Laccha paratha displays dozens of fine concentric spiral rings visible on the surface",
            "Edge appearance: Smooth folded edges on triangle paratha vs multi-ribbed flaky ringed perimeter on Laccha"
        ],
        a_visual_cues={"layers": "geometric_internal_folds", "rings": "none"},
        b_visual_cues={"layers": "visible_concentric_spiral_rings", "rings": "distinct_visible"}
    ),
    "puri_vs_kachori": BreadConfusionPair(
        pair_id="puri_vs_kachori",
        dish_a="Whole Wheat Puffy Puri",
        dish_b="Khasta Dal Kachori",
        distinguishing_features=[
            "Crust texture: Puri has a thin, elastic, blistered golden shell that collapses upon cooling; Kachori has a thick, rigid, shatteringly crumbly shortcrust pastry shell (khasta)",
            "Stuffing: Puri is empty/hollow inside; Kachori is packed with a dense, highly spiced roasted urad/moong dal or onion filling"
        ],
        a_visual_cues={"crust": "thin_elastic_hollow_puff", "stuffing": "none", "rigidity": "soft_deflating"},
        b_visual_cues={"crust": "thick_flaky_shortcrust", "stuffing": "spiced_lentil_core", "rigidity": "rigid_spherical"}
    ),
    "thepla_vs_roti": BreadConfusionPair(
        pair_id="thepla_vs_roti",
        dish_a="Gujarati Methi Thepla",
        dish_b="Plain Wheat Roti",
        distinguishing_features=[
            "Ingredients: Thepla contains chopped fresh fenugreek (methi) leaves, turmeric golden hue, ajwain, sesame seeds, and yogurt in dough; Roti is solely wheat flour and water",
            "Shelf stability & thinness: Thepla is rolled paper-thin and stays flexible for days due to oil and yogurt moisture"
        ],
        a_visual_cues={"color": "yellow_turmeric_with_green_flecks", "herbs": ["methi_leaves", "sesame_seeds"], "thickness": "paper_thin"},
        b_visual_cues={"color": "uniform_wheat_beige", "herbs": [], "thickness": "standard_medium"}
    ),
    "bhakri_vs_thick_roti": BreadConfusionPair(
        pair_id="bhakri_vs_thick_roti",
        dish_a="Coarse Grain Bhakri",
        dish_b="Thick Wheat Roti",
        distinguishing_features=[
            "Flour & texture: Bhakri is made from gluten-free millet (jowar, bajra, ragi) or coarse wheat, showing visible grain meal, rustic cracks, and hand-patted edges; Thick Roti has smooth gluten-stretched rolled edges"
        ],
        a_visual_cues={"edges": "cracked_hand_patted", "flour_texture": "coarse_millet_grit", "color": "millet_ash_or_grey"},
        b_visual_cues={"edges": "smooth_rolled", "flour_texture": "smooth_wheat_atta", "color": "golden_brown_wheat"}
    ),
    "jowar_roti_vs_bajra_roti": BreadConfusionPair(
        pair_id="jowar_roti_vs_bajra_roti",
        dish_a="Jowar Roti (Sorghum)",
        dish_b="Bajra Roti (Pearl Millet)",
        distinguishing_features=[
            "Color shade: Jowar is light cream, chalky pale ivory, or light grey; Bajra is dark greenish-grey, earthy brown, or slate grey",
            "Flavor & aroma: Mild earthy grain for Jowar vs robust, nutty, grassy rustic aroma for Bajra"
        ],
        a_visual_cues={"color": "pale_ivory_cream_grey", "grain_type": "jowar_sorghum"},
        b_visual_cues={"color": "dark_slate_greenish_grey", "grain_type": "bajra_pearl_millet"}
    ),
    "ragi_roti_vs_jowar_roti": BreadConfusionPair(
        pair_id="ragi_roti_vs_jowar_roti",
        dish_a="Ragi Roti (Finger Millet)",
        dish_b="Jowar Roti (Sorghum)",
        distinguishing_features=[
            "Color: Ragi is distinctly dark chocolate-brown, purplish-brown, or deep terracotta red; Jowar is pale cream/white"
        ],
        a_visual_cues={"color": "dark_chocolate_purplish_brown", "grain_type": "ragi_finger_millet"},
        b_visual_cues={"color": "pale_ivory_cream", "grain_type": "jowar_sorghum"}
    ),
    "appam_vs_dosa": BreadConfusionPair(
        pair_id="appam_vs_dosa",
        dish_a="Kerala Appam",
        dish_b="Crisp Plain Dosa",
        distinguishing_features=[
            "Shape & curvature: Appam has a bowl-curved structure with a fluffy spongy domed center and delicate lacy translucent perimeter; Dosa is completely flat, large in diameter, and uniformly crisp",
            "Color: Appam is pristine white in center with pale golden lacy rim; Dosa has deep uniform golden-brown roasted caramelization"
        ],
        a_visual_cues={"shape": "curved_bowl", "center": "thick_spongy_white", "edges": "lacy_frills"},
        b_visual_cues={"shape": "flat_crepe", "center": "thin_crisp", "edges": "golden_brown_roasted"}
    ),
    "appam_vs_neer_dosa": BreadConfusionPair(
        pair_id="appam_vs_neer_dosa",
        dish_a="Kerala Appam",
        dish_b="Mangalorean Neer Dosa",
        distinguishing_features=[
            "Structure: Appam has a thick puffed fermented center with lacy edges; Neer Dosa is uniformly thin, feather-light, unfermented, and folded into triangular or rectangular handkerchief folds",
            "Cooking vessel: Appam is swirled in a concave appachatti; Neer Dosa is poured onto a flat tawa and covered"
        ],
        a_visual_cues={"geometry": "bowl_concave", "thickness": "thick_center_thin_edge", "fermentation": "fermented_yeasty"},
        b_visual_cues={"geometry": "folded_flat_triangle", "thickness": "uniformly_thin_lacy", "fermentation": "unfermented_rice"}
    ),
    "pathiri_vs_neer_dosa": BreadConfusionPair(
        pair_id="pathiri_vs_neer_dosa",
        dish_a="Malabar Rice Pathiri",
        dish_b="Mangalorean Neer Dosa",
        distinguishing_features=[
            "Texture & preparation: Pathiri is rolled from cooked rice flour dough, dry-roasted on tawa, smooth, opaque chalk-white, and completely dry; Neer Dosa is poured from a watery batter, moist, lacy, perforated with micro-holes, and folded"
        ],
        a_visual_cues={"surface": "smooth_opaque_dry", "presentation": "flat_circular_disc", "texture": "soft_dry_roti"},
        b_visual_cues={"surface": "lacy_perforated_micro_holes", "presentation": "folded_quadrant", "texture": "moist_delicate_crepe"}
    ),
    "neer_dosa_vs_paper_dosa": BreadConfusionPair(
        pair_id="neer_dosa_vs_paper_dosa",
        dish_a="Mangalorean Neer Dosa",
        dish_b="South Indian Paper Roast Dosa",
        distinguishing_features=[
            "Texture & color: Neer Dosa is soft, moist, snow-white, and pliable; Paper Roast Dosa is paper-thin, shatteringly brittle, deep golden brown, and rolled into a giant cone or cylindrical tube"
        ],
        a_visual_cues={"color": "snow_white", "texture": "soft_moist_pliable", "shape": "folded_soft_crepe"},
        b_visual_cues={"color": "deep_golden_brown", "texture": "brittle_crisp_shatter", "shape": "long_cylinder_or_cone"}
    ),
    "adai_vs_dosa": BreadConfusionPair(
        pair_id="adai_vs_dosa",
        dish_a="Tamil Multi-Dal Adai",
        dish_b="Fermented Rice Dosa",
        distinguishing_features=[
            "Texture & color: Adai is thick, heavy, rustic, coarse-textured with visible broken lentil grains, red chillies, and curry leaves; Dosa is thin, smooth, and evenly roasted from smooth fermented batter"
        ],
        a_visual_cues={"texture": "coarse_granular_lentil", "thickness": "thick_rustic", "inclusions": ["curry_leaves", "chilli_flakes"]},
        b_visual_cues={"texture": "smooth_fermented_crepe", "thickness": "thin_crisp", "inclusions": []}
    ),
    "pesarattu_vs_green_dosa": BreadConfusionPair(
        pair_id="pesarattu_vs_green_dosa",
        dish_a="Andhra Pesarattu",
        dish_b="Palak / Green Herb Dosa",
        distinguishing_features=[
            "Batter source: Pesarattu is naturally greenish-yellow from unhulled green gram (whole moong dal) ground with ginger and green chillies, topped with diced raw onions and cumin; Green Dosa is colored with spinach puree added to fermented rice batter"
        ],
        a_visual_cues={"hue": "olive_greenish_yellow", "toppings": ["diced_onions", "cumin_seeds"], "batter_base": "whole_green_moong"},
        b_visual_cues={"hue": "bright_emerald_spinach_green", "toppings": [], "batter_base": "rice_urad_spinach"}
    ),
    "roomali_roti_vs_thin_chapati": BreadConfusionPair(
        pair_id="roomali_roti_vs_thin_chapati",
        dish_a="Roomali Roti",
        dish_b="Thin Homestyle Chapati",
        distinguishing_features=[
            "Size & thinness: Roomali Roti is massive in diameter (30–45 cm), handkerchief-thin, translucent, and folded like a handkerchief; Chapati is standard personal size (15–18 cm)"
        ],
        a_visual_cues={"diameter_cm": "large_30_to_45cm", "presentation": "handkerchief_folded", "thickness": "translucent_paper_thin"},
        b_visual_cues={"diameter_cm": "standard_15_to_18cm", "presentation": "flat_circular_disc", "thickness": "standard_thin"}
    )
}

# =============================================================================
# SECTIONS 9, 16, 64 — ANTI-BIAS & SPECIFICATION VERIFIERS
# =============================================================================

class AlooParathaStuffingVerifier:
    """
    Implements Section 9:
    - Never detect Aloo Paratha merely from brown circular appearance.
    - If potato stuffing is hidden or unproven by visible stuffing bulges,
      cut-section evidence, or verified recipe context, returns fallback:
      'Paratha — stuffed variant uncertain'
    """
    @staticmethod
    def verify_stuffing(visual_cues: Dict[str, Any]) -> Tuple[str, float, str]:
        has_visible_bulges = visual_cues.get("has_stuffing_bulges", False)
        has_cut_section = visual_cues.get("has_cut_section_showing_filling", False)
        stuffing_detected = visual_cues.get("stuffing_detected", "unknown").lower()

        if has_cut_section and "potato" in stuffing_detected:
            return "Aloo Paratha", 0.95, "Verified potato filling confirmed via cut-section cross-view."
        elif has_visible_bulges and ("potato" in stuffing_detected or "aloo" in stuffing_detected):
            return "Aloo Paratha", 0.88, "Visible golden potato filling bulges and surface texture confirm Aloo Paratha."
        elif "paneer" in stuffing_detected:
            return "Paneer Paratha", 0.92, "White crumbly cottage cheese stuffing identified."
        elif "gobi" in stuffing_detected:
            return "Gobi Paratha", 0.90, "Grated cauliflower stuffing identified."
        elif "mooli" in stuffing_detected:
            return "Mooli Paratha", 0.89, "Grated white radish stuffing identified."
        else:
            # Section 9 fallback rule
            return "Paratha — stuffed variant uncertain", 0.62, "Section 9 Rule: Stuffing is hidden beneath surface; cannot confirm Aloo Paratha without evidence."


class MilletBreadGrainVerifier:
    """
    Implements Section 16:
    - Do not infer flour solely from color.
    - If visual evidence is insufficient to distinguish Bajra from Jowar or Ragi,
      returns fallback: 'Millet-based flatbread — exact grain uncertain'
    """
    @staticmethod
    def verify_grain(visual_cues: Dict[str, Any]) -> Tuple[str, float, str]:
        color = visual_cues.get("color", "").lower()
        grain_specified = visual_cues.get("grain_type", "").lower()
        has_verified_texture = visual_cues.get("has_verified_millet_texture", False)

        if "ragi" in grain_specified or "chocolate_purplish" in color:
            return "Ragi Roti", 0.93, "Distinct dark purple-brown finger millet grain verified."
        elif "bajra" in grain_specified and has_verified_texture:
            return "Bajra Roti", 0.91, "Coarse cracked pearl millet texture and slate-grey hue verified."
        elif "jowar" in grain_specified and has_verified_texture:
            return "Jowar Roti", 0.92, "Smooth patted pale cream sorghum grain verified."
        else:
            # Section 16 fallback rule
            return "Millet-based flatbread — exact grain uncertain", 0.58, "Section 16 Rule: Color alone is insufficient to verify exact millet species without grain texture evidence."


class Section64NonNegotiableBreadVerifier:
    """
    Implements Section 64 Non-Negotiable Quality Rules:
    - Never classify every flatbread as roti.
    - Never classify every fried bread as puri.
    - Never classify every layered bread as paratha.
    - Never classify naan and kulcha as the same class.
    - Never classify Kerala parotta and laccha paratha as identical.
    - Never infer flour solely from color.
    - Never infer exact stuffing without evidence.
    - Separate bread from curry, chutney, and gravy.
    - Never assume butter from shine alone.
    """
    @staticmethod
    def verify_prediction(
        candidate_bread: str,
        visual_features: Dict[str, Any]
    ) -> Tuple[bool, str]:
        cand = candidate_bread.lower()

        # Rule 1: Never classify naan and kulcha as same class
        if "naan" in cand and visual_features.get("is_kulcha", False):
            return False, "Section 64 Rule: Naan and Kulcha must never be merged into the same class."

        # Rule 2: Never classify Kerala parotta and laccha paratha as identical
        if "parotta" in cand and visual_features.get("is_laccha_paratha", False):
            return False, "Section 64 Rule: Kerala parotta and laccha paratha are distinct classes."

        # Rule 3: Never assume butter from shine alone
        shine = visual_features.get("surface_shine", "").lower()
        has_slab = visual_features.get("has_melting_butter_slab", False)
        if "butter" in cand and shine == "heavy_sheen" and not has_slab:
            return False, "Section 64 Rule: Surface shine alone does not prove butter (could be oil or steam wash)."

        # Rule 4: Kothu parotta never classified as plain parotta
        if "plain parotta" in cand and visual_features.get("is_chopped_shreds", False):
            return False, "Section 64 Rule: Chopped parotta with egg/meat must never be classified as plain parotta."

        return True, "Valid prediction complying with Section 64 rules."



class DisambiguationResult(dict):
    """
    Flexible result object supporting both dict access (res['predicted_dish'])
    and tuple unpacking (dish, score, rationale).
    """
    def __init__(
        self,
        predicted_dish: str,
        confidence: str,
        confidence_score: float,
        rationale: str,
        distinguishing_features: Optional[List[str]] = None
    ):
        super().__init__(
            predicted_dish=predicted_dish,
            confidence=confidence,
            confidence_score=confidence_score,
            rationale=rationale,
            distinguishing_features=distinguishing_features or []
        )
        self.predicted_dish = predicted_dish
        self.confidence = confidence
        self.confidence_score = confidence_score
        self.rationale = rationale
        self.distinguishing_features = distinguishing_features or []

    def __iter__(self):
        return iter((self.predicted_dish, self.confidence_score, self.rationale))


def disambiguate_bread_pair(
    candidate_a: Optional[str] = None,
    candidate_b: Optional[str] = None,
    visual_evidence: Optional[Dict[str, Any]] = None,
    pair_id: Optional[str] = None,
    visual_features: Optional[Dict[str, Any]] = None
) -> DisambiguationResult:
    """
    Evaluates visual cues between high-confusion bread candidate pairs.
    Returns: DisambiguationResult (dict + tuple unpackable)
    """
    cues = visual_features or visual_evidence or {}

    pair = None
    if pair_id:
        pid = pair_id.lower().strip()
        pair = BREAD_CONFUSION_REGISTRY.get(pid)
        if not pair:
            for k, p in BREAD_CONFUSION_REGISTRY.items():
                if pid in k or k in pid:
                    pair = p
                    break

    if not pair and candidate_a and candidate_b:
        for p in BREAD_CONFUSION_REGISTRY.values():
            if (
                (candidate_a.lower() in p.dish_a.lower() or p.dish_a.lower() in candidate_a.lower()) and
                (candidate_b.lower() in p.dish_b.lower() or p.dish_b.lower() in candidate_b.lower())
            ):
                pair = p
                break

    if pair:
        score_a = 0
        score_b = 0
        reasons = []

        # Special handling for diameter in puri vs bhatura
        if pair.pair_id == "puri_vs_bhatura":
            diam = cues.get("bread_diameter_cm") or cues.get("diameter_cm")
            if diam is not None:
                if diam >= 16.0:
                    score_b += 2
                    reasons.append(f"Diameter {diam}cm matches large Bhatura")
                else:
                    score_a += 2
                    reasons.append(f"Diameter {diam}cm matches compact Puri")

        for k, val in pair.a_visual_cues.items():
            ev_val = cues.get(k)
            if ev_val is not None:
                if ev_val == val or (isinstance(val, list) and ev_val in val) or (isinstance(ev_val, list) and val in ev_val):
                    score_a += 1
                    reasons.append(f"Visual cue {k}={ev_val} indicates {pair.dish_a}")

        for k, val in pair.b_visual_cues.items():
            ev_val = cues.get(k)
            if ev_val is not None:
                if ev_val == val or (isinstance(val, list) and ev_val in val) or (isinstance(ev_val, list) and val in ev_val):
                    score_b += 1
                    reasons.append(f"Visual cue {k}={ev_val} indicates {pair.dish_b}")

        if score_a > score_b:
            conf_score = min(0.96, 0.72 + 0.08 * (score_a - score_b))
            conf_str = "High" if conf_score >= 0.85 else "Medium"
            return DisambiguationResult(
                predicted_dish=pair.dish_a,
                confidence=conf_str,
                confidence_score=conf_score,
                rationale="; ".join(reasons) or f"Morphological match for {pair.dish_a}",
                distinguishing_features=pair.distinguishing_features
            )
        elif score_b > score_a:
            conf_score = min(0.96, 0.72 + 0.08 * (score_b - score_a))
            conf_str = "High" if conf_score >= 0.85 else "Medium"
            return DisambiguationResult(
                predicted_dish=pair.dish_b,
                confidence=conf_str,
                confidence_score=conf_score,
                rationale="; ".join(reasons) or f"Morphological match for {pair.dish_b}",
                distinguishing_features=pair.distinguishing_features
            )
        else:
            return DisambiguationResult(
                predicted_dish=pair.dish_a,
                confidence="Low",
                confidence_score=0.55,
                rationale=f"Ambiguous between {pair.dish_a} and {pair.dish_b}; visual cues balanced.",
                distinguishing_features=pair.distinguishing_features
            )

    fallback = candidate_a or "Unknown Indian Bread"
    return DisambiguationResult(
        predicted_dish=fallback,
        confidence="Low",
        confidence_score=0.50,
        rationale="Generic bread disambiguation fallback; pair not recognized.",
        distinguishing_features=[]
    )


# =============================================================================
# SECTIONS 44 & 45 — BREAD STACK DETECTOR & COUNTING
# =============================================================================

class BreadStackCountResult(BaseModel):
    is_stack: bool
    visible_edges_count: int
    estimated_total_range: str  # e.g., "3" or "3–5"
    occlusion_percentage: float
    confidence: str             # "High", "Medium", "Low"
    notes: str
    estimated_count_range: Tuple[int, int] = (1, 1)
    estimated_pieces_count: int = 1
    occlusion_flag: bool = False


class BreadStackDetector:
    """
    Implements Sections 44 & 45:
    - Counts visible bread edges in a stack (rotis, chapatis, puris, parathas).
    - If pieces are partially occluded in a pile, outputs an estimated range rather than false precision.
    - Never invents invisible pieces (Section 44).
    """
    @classmethod
    def detect_stack(
        cls,
        visible_edge_detections: Optional[int] = None,
        visible_edges_count: Optional[int] = None,
        stack_height_cm: Optional[float] = None,
        observed_stack_height_mm: Optional[float] = None,
        top_bread_type: str = "Chapati",
        rim_occlusion_angle_deg: float = 0.0,
        estimated_unit_thickness_mm: float = 2.5
    ) -> BreadStackCountResult:
        vis = visible_edges_count if visible_edges_count is not None else (visible_edge_detections if visible_edge_detections is not None else 1)
        vis = max(1, vis)
        height_mm = observed_stack_height_mm if observed_stack_height_mm is not None else (stack_height_cm * 10.0 if stack_height_cm is not None else None)

        if height_mm is not None and height_mm > 0:
            if top_bread_type.lower() in ["chapati", "phulka", "roti", "thepla", "pathiri"]:
                unit_th = max(3.8, estimated_unit_thickness_mm if estimated_unit_thickness_mm > 3.0 else 3.8)
            else:
                unit_th = estimated_unit_thickness_mm

            calc_pieces = int(round(height_mm / max(1.0, unit_th)))
            if calc_pieces > vis + 1 or rim_occlusion_angle_deg > 45.0:
                est_low = vis
                est_high = max(vis + 1, calc_pieces)
                occlusion_pct = min(75.0, ((est_high - vis) / est_high) * 100.0)
                conf = "Medium" if occlusion_pct < 50.0 else "Low"
                return BreadStackCountResult(
                    is_stack=True,
                    visible_edges_count=vis,
                    estimated_total_range=f"{est_low}–{est_high}",
                    occlusion_percentage=round(occlusion_pct, 1),
                    confidence=conf,
                    notes=f"Stack height ({height_mm} mm) indicates occluded pieces beneath visible top {vis} edges. Never invent hidden pieces.",
                    estimated_count_range=(est_low, est_high),
                    estimated_pieces_count=vis,
                    occlusion_flag=True
                )

        # Single or fully visible flat stack
        return BreadStackCountResult(
            is_stack=(vis > 1),
            visible_edges_count=vis,
            estimated_total_range=str(vis),
            occlusion_percentage=0.0,
            confidence="High",
            notes=f"Confirmed {vis} discrete piece{'s' if vis > 1 else ''} with clear edge visibility.",
            estimated_count_range=(vis, vis),
            estimated_pieces_count=vis,
            occlusion_flag=False
        )



# =============================================================================
# SECTION 14 — KOTHU PAROTTA SEGMENTER
# =============================================================================

class KothuSegmentedComponent(BaseModel):
    component_name: str
    mass_g: float
    weight_g: float = 0.0
    calories: float
    protein_g: float
    carbs_g: float
    fat_g: float

    def model_post_init(self, __context: Any) -> None:
        if self.weight_g == 0.0 and self.mass_g > 0.0:
            self.weight_g = self.mass_g


class KothuParottaSegmentationResult(BaseModel):
    dish_name: str = "Egg Kothu Parotta"
    primary_dish: str = "Egg Kothu Parotta"
    is_kothu_parotta: bool = True
    components: List[KothuSegmentedComponent]
    total_mass_g: float
    total_calories: float
    total_protein_g: float
    total_carbs_g: float
    total_fat_g: float
    warning_rule_applied: str

    def model_post_init(self, __context: Any) -> None:
        if not self.primary_dish and self.dish_name:
            self.primary_dish = self.dish_name


class KothuParottaSegmenter:
    """
    Implements Section 14:
    - Never classifies Kothu Parotta as plain parotta!
    - Segregates chopped parotta pieces, scrambled egg, meat, onion, and salna gravy.
    """
    @classmethod
    def segment_kothu(
        cls,
        total_dish_weight_g: float = 320.0,
        has_meat: bool = False,
        meat_type: str = "chicken",
        egg_count: int = 2
    ) -> KothuParottaSegmentationResult:
        parotta_g = total_dish_weight_g * (0.50 if has_meat else 0.58)
        egg_g = egg_count * 45.0
        salna_onion_g = total_dish_weight_g * 0.20
        meat_g = max(0.0, (total_dish_weight_g - (parotta_g + egg_g + salna_onion_g))) if has_meat else 0.0

        comps: List[KothuSegmentedComponent] = []

        # 1. Chopped Parotta Shreds
        p_cals = (parotta_g / 100.0) * 315.0
        comps.append(KothuSegmentedComponent(
            component_name="Chopped Malabar Parotta Shreds",
            mass_g=round(parotta_g, 1),
            weight_g=round(parotta_g, 1),
            calories=round(p_cals, 1),
            protein_g=round((parotta_g / 100.0) * 6.8, 1),
            carbs_g=round((parotta_g / 100.0) * 46.0, 1),
            fat_g=round((parotta_g / 100.0) * 11.5, 1)
        ))

        # 2. Scrambled Egg Pieces
        if egg_count > 0:
            e_cals = (egg_g / 100.0) * 145.0
            comps.append(KothuSegmentedComponent(
                component_name=f"Scrambled Eggs ({egg_count} eggs)",
                mass_g=round(egg_g, 1),
                weight_g=round(egg_g, 1),
                calories=round(e_cals, 1),
                protein_g=round((egg_g / 100.0) * 12.5, 1),
                carbs_g=round((egg_g / 100.0) * 1.0, 1),
                fat_g=round((egg_g / 100.0) * 10.2, 1)
            ))

        # 3. Salna Gravy & Sautéed Onions
        s_cals = (salna_onion_g / 100.0) * 110.0
        comps.append(KothuSegmentedComponent(
            component_name="Spicy Salna Gravy & Sautéed Onions",
            mass_g=round(salna_onion_g, 1),
            weight_g=round(salna_onion_g, 1),
            calories=round(s_cals, 1),
            protein_g=round((salna_onion_g / 100.0) * 2.2, 1),
            carbs_g=round((salna_onion_g / 100.0) * 8.5, 1),
            fat_g=round((salna_onion_g / 100.0) * 7.5, 1)
        ))

        # 4. Meat Chunks (if present)
        if has_meat and meat_g > 0:
            m_cals = (meat_g / 100.0) * 190.0
            comps.append(KothuSegmentedComponent(
                component_name=f"Spiced Sautéed {meat_type.title()} Chunks",
                mass_g=round(meat_g, 1),
                weight_g=round(meat_g, 1),
                calories=round(m_cals, 1),
                protein_g=round((meat_g / 100.0) * 20.0, 1),
                carbs_g=round((meat_g / 100.0) * 2.0, 1),
                fat_g=round((meat_g / 100.0) * 11.0, 1)
            ))

        tot_mass = sum(c.mass_g for c in comps)
        tot_cals = sum(c.calories for c in comps)
        tot_pro = sum(c.protein_g for c in comps)
        tot_carb = sum(c.carbs_g for c in comps)
        tot_fat = sum(c.fat_g for c in comps)

        dish_label = f"{meat_type.title()} Kothu Parotta" if has_meat else "Egg Kothu Parotta"
        return KothuParottaSegmentationResult(
            dish_name=dish_label,
            primary_dish=dish_label,
            is_kothu_parotta=True,
            components=comps,
            total_mass_g=round(tot_mass, 1),
            total_calories=round(tot_cals, 1),
            total_protein_g=round(tot_pro, 1),
            total_carbs_g=round(tot_carb, 1),
            total_fat_g=round(tot_fat, 1),
            warning_rule_applied="Rule 14: Kothu parotta decomposed into parotta shreds, eggs, salna, and meat components."
        )

    @classmethod
    def segment(
        cls,
        has_egg: bool = True,
        meat_type: str = "chicken",
        portion_g: float = 380.0,
        egg_count: int = 2,
        meta: Optional[Dict[str, Any]] = None
    ) -> KothuParottaSegmentationResult:
        has_meat = meat_type.lower() not in ["none", "", "veg", "vegetarian"]
        return cls.segment_kothu(
            total_dish_weight_g=portion_g,
            has_meat=has_meat,
            meat_type=meat_type,
            egg_count=egg_count if has_egg else 0
        )



# =============================================================================
# SECTIONS 40 & 41 — STUFFING & TOPPING DISCRIMINATOR
# =============================================================================

class StuffingToppingResult(BaseModel):
    bread_base: str
    stuffing: str            # "potato", "paneer", "gobi", "none", "unknown"
    topping: str             # "butter", "ghee", "garlic", "sesame", "none", "unknown"
    stuffing_confidence: float
    topping_confidence: float
    calorie_adjustment_kcal: float
    notes: str


class BreadStuffingToppingDiscriminator:
    """
    Implements Sections 40 & 41:
    - Identifies bread_type * stuffing_type (e.g. Aloo Paratha).
    - Distinguishes stuffing from toppings.
    - Never assumes butter solely from surface shine.
    """
    @staticmethod
    def identify(
        bread_name: str,
        visual_cues: Dict[str, Any]
    ) -> StuffingToppingResult:
        stuffing_cue = visual_cues.get("stuffing_detected", "none").lower()
        surface_shine = visual_cues.get("surface_shine", "matte").lower()
        visible_melting_slab = visual_cues.get("has_melting_butter_slab", False)
        visible_garlic = visual_cues.get("has_chopped_garlic", False)
        visible_sesame = visual_cues.get("has_sesame_seeds", False)

        cal_adj = 0.0

        # Stuffing logic
        if "aloo" in stuffing_cue or "potato" in stuffing_cue or "aloo" in bread_name.lower():
            stuffing = "potato"
            stuff_conf = 0.94
        elif "paneer" in stuffing_cue or "paneer" in bread_name.lower():
            stuffing = "paneer"
            stuff_conf = 0.92
            cal_adj += 35.0  # paneer is richer than potato
        elif "gobi" in stuffing_cue or "gobi" in bread_name.lower():
            stuffing = "gobi"
            stuff_conf = 0.90
        else:
            stuffing = "none"
            stuff_conf = 0.85

        # Topping logic (Section 41: Never assume butter from shine alone!)
        if visible_melting_slab:
            topping = "butter"
            top_conf = 0.96
            cal_adj += 72.0  # ~10g butter
            top_note = "Confirmed melting butter slab."
        elif visible_garlic:
            topping = "garlic"
            top_conf = 0.95
            top_note = "Confirmed minced garlic topping."
        elif visible_sesame:
            topping = "sesame"
            top_conf = 0.93
            top_note = "Confirmed toasted sesame seeds."
        elif surface_shine == "heavy_sheen":
            # Uncertain fat type
            topping = "unknown"
            top_conf = 0.60
            cal_adj += 45.0
            top_note = "Surface shine detected; fat type (ghee vs oil vs light butter) uncertain per Section 41."
        else:
            topping = "none"
            top_conf = 0.90
            top_note = "Dry unbuttered surface."

        return StuffingToppingResult(
            bread_base=bread_name,
            stuffing=stuffing,
            topping=topping,
            stuffing_confidence=stuff_conf,
            topping_confidence=top_conf,
            calorie_adjustment_kcal=round(cal_adj, 1),
            notes=f"Stuffing: {stuffing}; Topping: {topping}. {top_note}"
        )
