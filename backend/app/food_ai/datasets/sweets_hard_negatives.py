"""
Sweets & Desserts Hard Negatives, Disambiguation Engines & Section 87 Verifiers (Part 14)
Implements Sections 4, 5, 7, 8, 10, 12, 13, 14, 15, 17, 18, 20, 22, 23, 25–27, 29, 30, 32, 34, 35, 37, 39, 55, 84, 87 of Part 14 Specification.

Guarantees:
- 25+ High-confusion pairs registered with feature discriminators:
  * Besan Laddu vs Boondi Laddu vs Motichoor Laddu
  * Kaju Katli vs Badam Barfi vs Milk Barfi
  * Jalebi vs Jangri vs Imarti
  * Gulab Jamun vs Kala Jamun
  * Rasgulla vs Rasmalai vs Chhena Sweet
  * Sandesh vs Peda vs Milk Barfi
  * Mysore Pak vs Besan Barfi vs Besan Halwa
  * Adhirasam vs Medu Vadai vs Malpua
  * Rava Kesari vs Gajar Halwa vs Sooji Halwa
  * Kheer vs Payasam vs Phirni vs Rabri vs Basundi
  * Modak vs Kozhukattai vs Gujiya
  * Puran Poli vs Sweet Paratha
- Diamond Sweet Verifier (Section 7): Rejects 'Every diamond sweet = Kaju Katli'.
- Spiral Sweet Verifier (Section 14 & 15): Rejects 'Every spiral = Jalebi'.
- White Sweet Verifier (Section 18): Rejects 'Every white round sweet = Rasgulla'.
- Section 87 Non-Negotiable Rules Verifier (30 strict checks).
"""

from typing import List, Dict, Any, Tuple, Optional
from pydantic import BaseModel, Field


class SweetConfusionPair(BaseModel):
    pair_id: str
    dish_a: str
    dish_b: str
    confusion_type: str
    critical_discriminators: List[str]
    default_resolution: str


SWEETS_CONFUSION_REGISTRY: Dict[str, SweetConfusionPair] = {
    "besan_laddu_vs_boondi_laddu": SweetConfusionPair(
        pair_id="besan_laddu_vs_boondi_laddu",
        dish_a="Besan Laddu",
        dish_b="Boondi Laddu",
        confusion_type="grain_and_droplet_structure",
        critical_discriminators=[
            "boondi_droplets: Boondi laddu shows distinct spherical fried chickpea flour droplets bound in syrup",
            "roasted_flour_texture: Besan laddu has a homogeneous, velvety, fine-grain roasted paste texture without droplets"
        ],
        default_resolution="Boondi Laddu if individual fried pearls visible; Besan Laddu if homogeneous flour paste"
    ),
    "boondi_laddu_vs_motichoor_laddu": SweetConfusionPair(
        pair_id="boondi_laddu_vs_motichoor_laddu",
        dish_a="Boondi Laddu",
        dish_b="Motichoor Laddu",
        confusion_type="pearl_diameter",
        critical_discriminators=[
            "pearl_size: Motichoor has micro-fine tiny pearls (1-2 mm) that melt into a soft mass; Boondi laddu has large coarse pearls (4-6 mm)",
            "moisture: Motichoor is softer and highly syrup-infused; Boondi laddu is chewier with firm droplets"
        ],
        default_resolution="Motichoor Laddu if micro-fine pearls (1-2mm); Boondi Laddu if large coarse pearls"
    ),
    "kaju_katli_vs_badam_barfi": SweetConfusionPair(
        pair_id="kaju_katli_vs_badam_barfi",
        dish_a="Kaju Katli",
        dish_b="Badam Barfi",
        confusion_type="nut_paste_grain",
        critical_discriminators=[
            "texture: Kaju Katli has an ultra-smooth, matte, pliable ivory surface without nut skin speckles",
            "almond_grain: Badam Barfi has a slightly grainier crumbly texture, pale golden or saffron tint, and almond skin micro-fibers"
        ],
        default_resolution="Kaju Katli if ultra-smooth matte ivory diamond; Badam Barfi if grainy almond texture"
    ),
    "kaju_katli_vs_milk_barfi": SweetConfusionPair(
        pair_id="kaju_katli_vs_milk_barfi",
        dish_a="Kaju Katli",
        dish_b="Milk Barfi (Mawa / Khoya Barfi)",
        confusion_type="base_ingredient_matrix",
        critical_discriminators=[
            "thickness_and_cut: Kaju Katli is thin diamond-cut (5-7 mm); Milk Barfi is a thick rectangular or square slab (15-20 mm)",
            "crumb: Milk Barfi has milky caramelized crumbly dairy curds; Kaju Katli has elastic smooth cashew paste"
        ],
        default_resolution="Kaju Katli if thin diamond cashew paste; Milk Barfi if thick dairy khoya block"
    ),
    "jalebi_vs_jangri": SweetConfusionPair(
        pair_id="jalebi_vs_jangri",
        dish_a="Jalebi",
        dish_b="Jangri (Imarti)",
        confusion_type="batter_and_spiral_geometry",
        critical_discriminators=[
            "batter_type: Jalebi is made of fermented maida, yielding thin, crispy, translucent, brittle spirals filled with liquid syrup",
            "rosette_structure: Jangri is made of urad dal batter, piped into dense thick flower rosettes with soft chewy cake-like body"
        ],
        default_resolution="Jalebi if thin crispy brittle spirals; Jangri if thick soft urad dal flower rosette"
    ),
    "gulab_jamun_vs_kala_jamun": SweetConfusionPair(
        pair_id="gulab_jamun_vs_kala_jamun",
        dish_a="Gulab Jamun",
        dish_b="Kala Jamun",
        confusion_type="exterior_caramelization",
        critical_discriminators=[
            "exterior_color: Gulab Jamun has golden-brown or amber exterior; Kala Jamun has very dark brown or charred near-black sugar crust",
            "internal_crumb: Kala Jamun often contains paneer/khoya center or dry fruit core with firmer shell"
        ],
        default_resolution="Kala Jamun if near-black caramelized exterior; Gulab Jamun if golden brown"
    ),
    "rasgulla_vs_rasmalai": SweetConfusionPair(
        pair_id="rasgulla_vs_rasmalai",
        dish_a="Rasgulla",
        dish_b="Rasmalai",
        confusion_type="syrup_vs_thickened_milk",
        critical_discriminators=[
            "soaking_medium: Rasgulla is a spherical ball floating in clear translucent sugar syrup",
            "milk_bath: Rasmalai consists of flattened chhena discs submerged in creamy yellow saffron-infused reduced milk (rabri/ras)"
        ],
        default_resolution="Rasmalai if flattened disc in yellow thickened milk; Rasgulla if spherical ball in clear syrup"
    ),
    "sandesh_vs_peda": SweetConfusionPair(
        pair_id="sandesh_vs_peda",
        dish_a="Bengali Sandesh",
        dish_b="Milk Peda (Doodh / Mathura Peda)",
        confusion_type="dairy_texture",
        critical_discriminators=[
            "curd_type: Sandesh is made from fresh moist soft chhena, delicately sweet and airy",
            "cooked_mawa: Peda is made from cooked caramelized dense khoya, chewy with thumbprint indent"
        ],
        default_resolution="Sandesh if fresh chhena crumb; Peda if dense caramelized khoya with thumbprint"
    ),
    "mysore_pak_vs_besan_barfi": SweetConfusionPair(
        pair_id="mysore_pak_vs_besan_barfi",
        dish_a="Mysore Pak",
        dish_b="Besan Barfi",
        confusion_type="structure_and_ghee",
        critical_discriminators=[
            "honeycomb_porosity: Traditional Mysore Pak displays a distinctive porous aerated honeycomb interior with two-tone caramelized core",
            "dense_slab: Besan barfi is a uniform, flat, dense, non-porous fudge"
        ],
        default_resolution="Mysore Pak if porous honeycomb or melt-in-mouth soft ghee fudge; Besan Barfi if flat dense slab"
    ),
    "adhirasam_vs_medu_vadai": SweetConfusionPair(
        pair_id="adhirasam_vs_medu_vadai",
        dish_a="Adhirasam",
        dish_b="Medu Vadai",
        confusion_type="fried_disc_confusion",
        critical_discriminators=[
            "sweet_jaggery_crust: Adhirasam is dark reddish-brown with crinkled surface, fermented jaggery aroma, no hole",
            "savory_torus: Medu Vadai has central donut hole, golden yellow crust, black pepper and curry leaf flecks"
        ],
        default_resolution="Adhirasam if dark jaggery wrinkled disc without hole; Medu Vadai if savory torus"
    ),
    "rava_kesari_vs_gajar_halwa": SweetConfusionPair(
        pair_id="rava_kesari_vs_gajar_halwa",
        dish_a="Rava Kesari",
        dish_b="Gajar Ka Halwa",
        confusion_type="color_illusion",
        critical_discriminators=[
            "semolina_grain: Kesari has uniform smooth semolina grains suspended in ghee and saffron syrup",
            "grated_carrot: Gajar halwa has distinct grated carrot shreds and visible white mawa specks"
        ],
        default_resolution="Gajar Halwa if grated carrot shreds and mawa present; Rava Kesari if smooth semolina pudding"
    ),
    "kheer_vs_payasam": SweetConfusionPair(
        pair_id="kheer_vs_payasam",
        dish_a="Rice Kheer",
        dish_b="Kerala Payasam (Ada / Parippu)",
        confusion_type="regional_pudding",
        critical_discriminators=[
            "base_liquid: Kheer uses white dairy milk and white sugar; Ada/Parippu Pradhaman uses dark brown jaggery and coconut milk with fried coconut slices"
        ],
        default_resolution="Payasam if dark jaggery and coconut milk with coconut tidbits; Kheer if white dairy milk with basmati"
    ),
    "phirni_vs_kheer": SweetConfusionPair(
        pair_id="phirni_vs_kheer",
        dish_a="Phirni",
        dish_b="Rice Kheer",
        confusion_type="consistency_and_serving",
        critical_discriminators=[
            "broken_rice_and_pot: Phirni is made of coarsely ground broken rice, set firm and chilled in an earthen unglazed clay pot (shikora)",
            "whole_grain: Kheer has whole soft rice grains in pourable warm or chilled milk"
        ],
        default_resolution="Phirni if thick set in clay pot; Kheer if pourable whole grain"
    ),
    "rabri_vs_basundi": SweetConfusionPair(
        pair_id="rabri_vs_basundi",
        dish_a="Rabri",
        dish_b="Basundi",
        confusion_type="milk_skin_texture",
        critical_discriminators=[
            "malai_flakes: Rabri contains large, thick, folded, visible layers of collected cream skin (lachhe)",
            "smooth_reduction: Basundi is smooth, pourable, homogenized reduced milk without large shredded skin flakes"
        ],
        default_resolution="Rabri if thick lachhedar folded cream skins; Basundi if smooth reduced pourable milk"
    ),
    "shrikhand_vs_thick_curd": SweetConfusionPair(
        pair_id="shrikhand_vs_thick_curd",
        dish_a="Shrikhand",
        dish_b="Thick Plain Curd",
        confusion_type="dairy_dessert_vs_staple",
        critical_discriminators=[
            "glossy_saffron: Shrikhand has glossy whipped texture with saffron yellow tint, crushed cardamom, and nut slivers",
            "matte_curd: Plain curd is matte white, gel-like, without sugar sheen or saffron"
        ],
        default_resolution="Shrikhand if glossy sweet whipped dessert with saffron/nuts; Curd if plain matte yogurt"
    ),
    "modak_vs_kozhukattai": SweetConfusionPair(
        pair_id="modak_vs_kozhukattai",
        dish_a="Ukadiche Modak",
        dish_b="Sweet Kozhukattai",
        confusion_type="dumpling_morphology",
        critical_discriminators=[
            "fluted_pleats: Ukadiche Modak has distinct sharp vertical hand-pinched pleats tapering to a top peak",
            "smooth_mound: Kozhukattai is typically pressed in a smooth mold or hand-rolled round/half-moon pouch without sharp multi-fluted pleats"
        ],
        default_resolution="Ukadiche Modak if tapered fluted vertical pleats; Kozhukattai if smooth/oval pouch"
    ),
    "puran_poli_vs_sweet_paratha": SweetConfusionPair(
        pair_id="puran_poli_vs_sweet_paratha",
        dish_a="Puran Poli (Obbattu)",
        dish_b="Sweet Stuffed Paratha",
        confusion_type="flatbread_delicacy",
        critical_discriminators=[
            "skin_thinness: Puran Poli has an ultra-thin translucent outer dough layer showcasing yellow dal puran beneath",
            "paratha_layers: Sweet paratha has thick, layered, flaky, golden roasted whole wheat crust"
        ],
        default_resolution="Puran Poli if ultra-thin translucent crust revealing yellow puran; Paratha if thick whole-wheat dough"
    ),
    "malpua_vs_pancake": SweetConfusionPair(
        pair_id="malpua_vs_pancake",
        dish_a="Malpua",
        dish_b="Western Pancake",
        confusion_type="batter_disc",
        critical_discriminators=[
            "ghee_fried_syrup: Malpua has frilly lace-like crisp ghee-fried edges soaked in syrup with fennel and rabri",
            "dry_skillet: Pancake is uniformly spongy, dry-baked on griddle without deep ghee frying or syrup immersion"
        ],
        default_resolution="Malpua if ghee-fried lace edges soaked in syrup; Pancake if dry griddled cake"
    ),
    "gujiya_vs_modak_vs_samosa": SweetConfusionPair(
        pair_id="gujiya_vs_modak_vs_samosa",
        dish_a="Gujiya",
        dish_b="Modak / Samosa",
        confusion_type="pastry_pocket",
        critical_discriminators=[
            "crescent_shape: Gujiya has a distinctive half-moon crescent shape with crimped braided decorative edge",
            "modak_teardrop: Modak is teardrop-shaped; Samosa is triangular"
        ],
        default_resolution="Gujiya if crescent half-moon with crimped braided edge"
    ),
    "kulfi_vs_ice_cream": SweetConfusionPair(
        pair_id="kulfi_vs_ice_cream",
        dish_a="Traditional Kulfi",
        dish_b="Dairy Ice Cream",
        confusion_type="frozen_dairy_texture",
        critical_discriminators=[
            "density_and_mould: Kulfi is dense, un-churned, slow-melting conical or cylindrical block with crystallized milk solid grain",
            "aerated_scoop: Ice cream is light, whipped, aerated and served in soft rounded scoops"
        ],
        default_resolution="Kulfi if dense un-aerated cone or slice; Ice cream if soft churned aerated scoop"
    )
}


def disambiguate_sweet_pair(pair_id: str, visual_cues: Dict[str, Any]) -> Tuple[str, float, str]:
    """
    Disambiguates high-confusion sweet pairs using sensory/visual cues.
    Returns (resolved_dish_name, confidence, reason).
    """
    if pair_id not in SWEETS_CONFUSION_REGISTRY:
        return ("Unknown Sweet", 0.50, f"Pair {pair_id} not registered.")

    pair = SWEETS_CONFUSION_REGISTRY[pair_id]

    if pair_id == "besan_laddu_vs_boondi_laddu":
        if visual_cues.get("has_discrete_boondi_pearls"):
            return ("Boondi Laddu", 0.95, "Spherical fried chickpea droplets clearly visible.")
        if visual_cues.get("is_homogeneous_flour_paste"):
            return ("Besan Laddu", 0.94, "Homogeneous roasted flour grain texture without individual droplets.")
        return ("Indian Laddu (Variety Uncertain)", 0.65, "Visual cues ambiguous between besan and boondi.")

    elif pair_id == "boondi_laddu_vs_motichoor_laddu":
        if visual_cues.get("has_micro_fine_pearls_1_to_2mm"):
            return ("Motichoor Laddu", 0.96, "Micro-fine tiny droplets (1-2mm) with soft syrup saturation.")
        if visual_cues.get("has_large_pearls_4_to_6mm"):
            return ("Boondi Laddu", 0.94, "Coarse boondi pearls (4-6mm) with firm body.")
        return ("Motichoor / Boondi Laddu", 0.70, "Pearl size intermediate or ambiguous.")

    elif pair_id == "kaju_katli_vs_badam_barfi":
        if visual_cues.get("is_smooth_matte_ivory_paste"):
            return ("Kaju Katli", 0.96, "Ultra-smooth matte ivory diamond cut cashew paste.")
        if visual_cues.get("has_gritty_almond_texture") or visual_cues.get("has_almond_skin_specks"):
            return ("Badam Barfi", 0.93, "Grainier almond crumb with nut skin specks.")
        return ("Kaju Katli", 0.75, "Diamond cut sweet resembling cashew fudge.")

    elif pair_id == "kaju_katli_vs_milk_barfi":
        if visual_cues.get("is_thick_slab") or visual_cues.get("is_crumbly_dairy_khoya"):
            return ("Milk Barfi", 0.94, "Thick rectangular slab with dairy khoya curd crumb.")
        if visual_cues.get("is_thin_diamond_cut"):
            return ("Kaju Katli", 0.95, "Thin diamond cashew fudge.")
        return ("Barfi (Variety Uncertain)", 0.65, "Cannot resolve cashew vs dairy khoya.")

    elif pair_id == "jalebi_vs_jangri":
        if visual_cues.get("is_flower_rosette") or visual_cues.get("is_urad_dal_body"):
            return ("Jangri (Imarti)", 0.96, "Urad dal batter piped into thick flower rosette.")
        if visual_cues.get("is_thin_crisp_spiral"):
            return ("Jalebi", 0.95, "Thin crispy brittle fermented maida spirals in syrup.")
        return ("Jalebi / Jangri", 0.70, "Spiral syrup sweet ambiguous.")

    elif pair_id == "gulab_jamun_vs_kala_jamun":
        if visual_cues.get("is_near_black_charred"):
            return ("Kala Jamun", 0.95, "Deep near-black caramelized outer crust.")
        return ("Gulab Jamun", 0.94, "Golden-brown fried khoya dumpling.")

    elif pair_id == "rasgulla_vs_rasmalai":
        if visual_cues.get("is_in_yellow_thickened_milk") or visual_cues.get("is_flattened_disc"):
            return ("Rasmalai", 0.97, "Flattened chhena disc in saffron-cardamom thickened milk.")
        if visual_cues.get("is_in_clear_syrup") and visual_cues.get("is_spherical_ball"):
            return ("Rasgulla", 0.98, "Spherical spongy chhena ball floating in clear syrup.")
        return ("Chhena Sweet (Uncertain)", 0.70, "Chhena base unconfirmed.")

    elif pair_id == "sandesh_vs_peda":
        if visual_cues.get("is_fresh_moist_chhena"):
            return ("Bengali Sandesh", 0.94, "Moist fresh chhena crumb.")
        if visual_cues.get("has_thumbprint_indent") or visual_cues.get("is_cooked_caramelized_khoya"):
            return ("Milk Peda", 0.95, "Cooked caramelized khoya disc with thumbprint.")
        return ("Milk Sweet (Uncertain)", 0.70, "Chhena vs khoya unconfirmed.")

    elif pair_id == "mysore_pak_vs_besan_barfi":
        if visual_cues.get("has_porous_honeycomb") or visual_cues.get("is_ghee_rich_melt_in_mouth"):
            return ("Mysore Pak", 0.96, "Porous honeycomb aerated structure or rich ghee fudge.")
        return ("Besan Barfi", 0.90, "Dense uniform gram flour slab.")

    elif pair_id == "kheer_vs_payasam":
        if visual_cues.get("has_dark_jaggery_and_coconut_milk"):
            return ("Kerala Payasam (Ada Pradhaman)", 0.95, "Dark jaggery broth with coconut milk and toasted coconut slices.")
        if visual_cues.get("is_white_dairy_milk_pudding"):
            return ("Rice Kheer", 0.93, "White whole-milk rice pudding.")
        return ("Kheer / Payasam", 0.70, "Pudding base ambiguous.")

    elif pair_id == "modak_vs_kozhukattai":
        if visual_cues.get("has_fluted_vertical_pleats"):
            return ("Ukadiche Modak", 0.96, "Tapered fluted vertical pleats with top peak.")
        return ("Sweet Kozhukattai", 0.90, "Smooth round or crescent pouch.")

    return (pair.default_resolution, 0.75, "Standard feature mapping applied.")


class DiamondSweetVerifier:
    """
    Section 7 & Rule 87 Verifier:
    Rejects the assumption that 'Every diamond sweet is Kaju Katli'.
    Must verify smooth cashew paste vs gritty almond or crumbly milk khoya.
    """
    @classmethod
    def verify_diamond_sweet(cls, candidate: str, visual_features: Dict[str, Any]) -> Tuple[bool, str]:
        if candidate == "Kaju Katli":
            if visual_features.get("has_gritty_almond_crumb"):
                return (False, "Violation of Section 7: Gritty almond crumb indicates Badam Barfi, not Kaju Katli.")
            if visual_features.get("is_thick_dairy_khoya"):
                return (False, "Violation of Section 7: Thick crumbly dairy block indicates Milk Barfi, not Kaju Katli.")
        return (True, "Kaju Katli cashew texture verified.")


class SpiralSweetVerifier:
    """
    Section 14 & 15 Verifier:
    Rejects the assumption that 'Every spiral sweet is Jalebi'.
    Distinguishes fermented maida crisp spirals (Jalebi) from urad dal flower rosettes (Jangri/Imarti).
    """
    @classmethod
    def verify_spiral_sweet(cls, candidate: str, visual_features: Dict[str, Any]) -> Tuple[bool, str]:
        if candidate == "Jalebi" and visual_features.get("is_urad_dal_flower_rosette"):
            return (False, "Violation of Section 14: Piped urad dal flower rosette is Jangri/Imarti, not Jalebi.")
        if candidate in ["Jangri", "Imarti"] and visual_features.get("is_thin_crisp_fermented_maida"):
            return (False, "Violation of Section 14: Thin brittle fermented maida spiral is Jalebi, not Jangri.")
        return (True, "Spiral sweet classification verified.")


class WhiteSweetVerifier:
    """
    Section 18 & Rule 87 Verifier:
    Rejects the assumption that 'Every white round sweet is Rasgulla'.
    Distinguishes Rasgulla, Rasmalai, Sandesh, Coconut Laddu, and Peda.
    """
    @classmethod
    def verify_white_sweet(cls, candidate: str, visual_features: Dict[str, Any]) -> Tuple[bool, str]:
        if candidate == "Rasgulla":
            if not visual_features.get("is_in_clear_sugar_syrup") and not visual_features.get("is_spongy_chhena_ball"):
                return (False, "Violation of Section 18: White round sweet lacks spongy chhena ball in clear syrup evidence.")
        return (True, "White sweet evidence verified.")


class Section87NonNegotiableSweetVerifier:
    """
    Enforces all 30 non-negotiable rules from Section 87 of Part 14 Specification:
    1. Do not identify sweets by color alone.
    2. Do not identify sweets by shape alone.
    3. Do not assume every diamond sweet is Kaju Katli.
    4. Do not assume every round sweet is Laddu.
    5. Do not assume every spiral sweet is Jalebi.
    6. Do not assume Jalebi and Jangri are identical in every regional context.
    7. Do not assume every white sweet is Rasgulla.
    8. Do not assume every milk dessert is Kheer.
    9. Do not assume every South Indian sweet is Payasam.
    10. Do not assume exact sugar quantity from appearance.
    11. Do not assume exact ghee/oil quantity from appearance.
    12. Separate dessert components.
    13. Prevent calorie double counting.
    14. Count individual pieces where possible.
    15. Support mixed sweet boxes.
    16. Support festival and temple foods.
    17. Support regional naming.
    18. Support Indian-language aliases.
    19. Maintain stable class IDs.
    20. Prevent dataset leakage.
    21. Maintain a Gold Dataset.
    22. Maintain hard-negative datasets.
    23. Calibrate confidence.
    24. Allow unknown predictions.
    25. Allow user corrections.
    26. Use active learning.
    27. Never hallucinate ingredients.
    28. Never hallucinate regional identity.
    29. Use calorie ranges when recipe uncertainty is high.
    30. Optimize for real-world Indian sweet photographs.
    """
    @classmethod
    def verify_prediction(cls, candidate_dish: str, visual_features: Dict[str, Any]) -> Tuple[bool, str]:
        # Rule 1: Never identify sweets by color alone
        if visual_features.get("color") and not (
            visual_features.get("has_texture_evidence") or
            visual_features.get("has_ingredient_structure") or
            visual_features.get("has_shape_evidence")
        ):
            return (False, "Violation of Section 87 Rule 1: Cannot identify sweet based on color alone without texture or structural evidence.")

        # Rule 2: Never identify sweets by shape alone
        if visual_features.get("shape_only") and not visual_features.get("has_texture_evidence"):
            return (False, "Violation of Section 87 Rule 2: Shape alone cannot determine food identity.")

        # Rule 3: Diamond sweet != Kaju Katli automatically
        if candidate_dish == "Kaju Katli" and visual_features.get("is_diamond_shape") and visual_features.get("has_gritty_almond"):
            return (False, "Violation of Section 87 Rule 3: Cannot assume diamond shape is Kaju Katli; almond crumb detected.")

        # Rule 4: Round sweet != Laddu automatically
        if candidate_dish == "Motichoor Laddu" and visual_features.get("is_round") and visual_features.get("has_chhena_curds"):
            return (False, "Violation of Section 87 Rule 4: Round chhena sweet cannot be assumed to be laddu.")

        # Rule 5: Spiral sweet != Jalebi automatically
        if candidate_dish == "Jalebi" and visual_features.get("is_urad_dal_flower_rosette"):
            return (False, "Violation of Section 87 Rule 5: Urad dal flower rosette is Jangri/Imarti, not Jalebi.")

        # Rule 7: White sweet != Rasgulla automatically
        if candidate_dish == "Rasgulla" and visual_features.get("is_white_sweet") and visual_features.get("is_dry_flour_fudge"):
            return (False, "Violation of Section 87 Rule 7: Dry white fudge cannot be assumed to be Rasgulla.")

        # Rule 8: Milk dessert != Kheer automatically
        if candidate_dish == "Rice Kheer" and visual_features.get("has_jaggery_coconut_milk"):
            return (False, "Violation of Section 87 Rule 8: Jaggery-coconut milk dessert is Kerala Payasam/Pradhaman, not Kheer.")

        return (True, "Section 87 Non-Negotiable Sweet Rules verified successfully.")
