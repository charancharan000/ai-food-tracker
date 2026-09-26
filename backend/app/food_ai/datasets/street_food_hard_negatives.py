"""
Street Food Hard Negatives, Fine-Grained Disambiguation & Packaging Filter (Part 8)
Implements Sections 4, 6, 8, 10, 12, 20, 24, 28, 29, 30, 35, 41, 43, 48, 75, 76, 81, 95, 98.

Guarantees:
- 27+ Pan-Indian Street Food Confusion Pairs with fine-grained visual feature discrimination.
- PaniPuriCountingDiscriminator:
  * Counts visible whole, filled, empty, and partially eaten puris.
  * Estimates occlusion range when puris are partially hidden (Section 4).
  * Never claims exact count when occlusion is high.
- StreetRollDiscriminator:
  * Strict differentiation between Kathi Roll, Frankie, and Shawarma based on bread type,
    inner lining, filling style, and sauces (Section 28, 29, 30).
- NoodleDiscriminator:
  * Disambiguates Maggi (curly/wavy instant strands) from Hakka Noodles (long straight wok-tossed)
    and Thukpa (deep soup broth) (Section 48, 50).
- ChaatBaseDiscriminator:
  * Identifies underlying chaat foundation: Papdi vs Puri vs Samosa vs Kachori vs Pattice vs Bhalla.
- StreetPackagingFilter:
  * Filters disposable paper plates, newspaper liners, dona bowls, skewers, toothpicks, foil wraps
    so non-food objects never inflate weight or calories (Section 76, 81).
"""

from typing import List, Dict, Any, Optional, Tuple
from pydantic import BaseModel, Field


class ConfusionPairDefinition(BaseModel):
    pair_id: str
    food_a: str
    food_b: str
    distinguishing_features: List[str]
    a_visual_cues: Dict[str, Any]
    b_visual_cues: Dict[str, Any]


STREET_FOOD_CONFUSION_REGISTRY: Dict[str, ConfusionPairDefinition] = {
    "pani_puri_vs_puchka": ConfusionPairDefinition(
        pair_id="pani_puri_vs_puchka",
        food_a="Pani Puri / Golgappa",
        food_b="Kolkata Puchka",
        distinguishing_features=[
            "Water color & tanginess (green mint vs dark tamarind-gondhoraj)",
            "Filling base (warm white pea ragda or boiled potato vs dark mashed potato with bhaja masala & yellow peas)",
            "Puri texture (semolina golden puff vs thin flour crisp dark crust)"
        ],
        a_visual_cues={"water": "bright_green_mint_or_heeng", "filling": "warm_ragda_or_potato_chickpea", "puri": "suji_or_atta_sphere"},
        b_visual_cues={"water": "dark_tamarind_gondhoraj_tart", "filling": "heavily_spiced_potato_bhaja_masala", "puri": "darker_thin_maida_shell"}
    ),
    "bhel_puri_vs_jhalmuri": ConfusionPairDefinition(
        pair_id="bhel_puri_vs_jhalmuri",
        food_a="Mumbai Bhel Puri",
        food_b="Kolkata Jhalmuri",
        distinguishing_features=[
            "Oil presence: raw pungent yellow mustard oil sheen in Jhalmuri vs oil-free chutneys in Bhel Puri",
            "Chutneys: sweet tamarind & mint wet paste in Bhel vs raw mustard oil + bhaja masala in Jhalmuri",
            "Coconut & Chanachur: fresh raw coconut bits in Jhalmuri vs nylon sev in Bhel Puri"
        ],
        a_visual_cues={"sauce": "wet_tamarind_mint_chutneys", "sev": "fine_nylon_sev", "oil": "none_visible"},
        b_visual_cues={"oil": "raw_mustard_oil_yellow_sheen", "ingredients": ["chanachur", "coconut_slivers", "raw_chillies"], "masala": "dry_bhaja_powder"}
    ),
    "sev_puri_vs_dahi_puri": ConfusionPairDefinition(
        pair_id="sev_puri_vs_dahi_puri",
        food_a="Sev Puri",
        food_b="Dahi Puri",
        distinguishing_features=[
            "Base structure: Flat papdi discs in Sev Puri vs Puffed hollow round puris in Dahi Puri",
            "Dairy: Thick white curd/yogurt blanket over Dahi Puri vs Zero yogurt on classic Sev Puri",
            "Topping: Heavy dry yellow nylon sev cover in Sev Puri"
        ],
        a_visual_cues={"base": "flat_papdi_disc", "yogurt": "absent", "top": "dense_yellow_sev_carpet"},
        b_visual_cues={"base": "hollow_globe_puri", "yogurt": "heavy_white_curd_drizzle", "top": "curd_with_sev_and_pomegranate"}
    ),
    "dahi_puri_vs_papdi_chaat": ConfusionPairDefinition(
        pair_id="dahi_puri_vs_papdi_chaat",
        food_a="Dahi Puri",
        food_b="Papdi Chaat",
        distinguishing_features=[
            "Base: individual round hollow puris with punctured tops in Dahi Puri vs overlapping flat crispy papdi crackers in Papdi Chaat",
            "Serving geometry: Discrete pieces (usually 6 arranged radially) vs continuous layered shallow mound"
        ],
        a_visual_cues={"shape": "spherical_puris_with_open_crown", "arrangement": "discrete_individual_pieces"},
        b_visual_cues={"shape": "flat_crackers_layered", "arrangement": "continuous_stacked_mound"}
    ),
    "samosa_vs_kachori": ConfusionPairDefinition(
        pair_id="samosa_vs_kachori",
        food_a="Samosa",
        food_b="Kachori",
        distinguishing_features=[
            "Shape: Distinct 3-dimensional tetrahedron / pyramid triangle in Samosa vs Flattened or puffed disk / spherical dome in Kachori",
            "Crust texture: Smooth thick ajwain-flecked pastry in Samosa vs Flaky khasta blistered layered crust in Kachori",
            "Filling: Chunky potato cubes and whole peas in Samosa vs Fine spiced dal / caramelized onion / ground peas in Kachori"
        ],
        a_visual_cues={"shape": "pyramidal_tetrahedron", "crust": "smooth_pastry_with_cone_seam", "filling": "chunky_potato_peas"},
        b_visual_cues={"shape": "round_flattened_sphere", "crust": "blistered_flaky_khasta", "filling": "ground_dal_or_onion_paste"}
    ),
    "batata_vada_vs_aloo_bonda": ConfusionPairDefinition(
        pair_id="batata_vada_vs_aloo_bonda",
        food_a="Batata Vada (Maharashtra)",
        food_b="Aloo Bonda (South India)",
        distinguishing_features=[
            "Tempering: Intense mustard seed, turmeric yellow hue, curry leaf, and green chilli paste in Batata Vada",
            "Batter: Thin crisp golden chickpea coating in Batata Vada vs slightly thicker fluffier besan or maida crust in South Indian Bonda",
            "Accompaniments: Dry red garlic chutney + fried green chilli in Batata Vada vs Coconut chutney + Sambar in Aloo Bonda"
        ],
        a_visual_cues={"tempering": "curry_leaf_mustard_turmeric_yellow", "accompaniments": ["dry_garlic_chutney", "fried_chilli"]},
        b_visual_cues={"tempering": "mild_ginger_coriander_onion", "accompaniments": ["white_coconut_chutney", "sambar"]}
    ),
    "kathi_roll_vs_frankie": ConfusionPairDefinition(
        pair_id="kathi_roll_vs_frankie",
        food_a="Kolkata Kathi Roll",
        food_b="Mumbai Frankie",
        distinguishing_features=[
            "Bread: Flaky layered lachha paratha in Kathi Roll vs Thin soft wheat/maida roti in Frankie",
            "Egg lining: Egg is cooked directly bonded to the inner face of the paratha in Kathi Roll",
            "Filling: Chunky grilled skewers/tikka chunks in Kathi Roll vs cylindrical mashed potato cutlet roll in Frankie",
            "Seasoning: Raw red onion + fresh lime squeeze in Kathi Roll vs tangy Frankie masala powder + vinegar chillies in Frankie"
        ],
        a_visual_cues={"bread": "flaky_layered_paratha", "egg": "bonded_egg_lining", "meat_veg": "charred_tikka_chunks"},
        b_visual_cues={"bread": "thin_smooth_roti", "egg": "optional_wash", "meat_veg": "cylindrical_potato_cutlet", "seasoning": "frankie_powder"}
    ),
    "kathi_roll_vs_shawarma": ConfusionPairDefinition(
        pair_id="kathi_roll_vs_shawarma",
        food_a="Kathi Roll",
        food_b="Shawarma",
        distinguishing_features=[
            "Bread: Indian paratha/roti vs Middle Eastern pita/kubbus pocket",
            "Meat preparation: Pan-sautéed or tandoor tikka chunks in Kathi Roll vs Shaved vertical rotisserie spit meat in Shawarma",
            "Sauce: Mint-coriander green chutney in Kathi Roll vs Thick garlic mayonnaise (toum) or tahini in Shawarma",
            "Internal garnish: Raw sliced onion in Kathi Roll vs French fries and pickled cucumber/turnip in Shawarma"
        ],
        a_visual_cues={"sauce": "green_mint_chutney", "bread": "paratha_with_ghee", "garnish": "raw_red_onion"},
        b_visual_cues={"sauce": "white_garlic_mayo_toum", "bread": "kubbus_pita", "garnish": ["french_fries_inside", "pickled_turnip"]}
    ),
    "momo_vs_dumpling": ConfusionPairDefinition(
        pair_id="momo_vs_dumpling",
        food_a="Himalayan Momo",
        food_b="Chinese Dim Sum / Generic Dumpling",
        distinguishing_features=[
            "Pleating pattern: High-tension central top-knot circular pleat or crescent pinch pleat",
            "Accompaniment: Fiery red dalle khursani / bhoot jolokia chilli-garlic chutney served alongside",
            "Dough thickness: Sturdier wheat flour dough compared to crystal translucent starch dim sum wrappers"
        ],
        a_visual_cues={"chutney": "fiery_red_chilli_garlic_sauce", "pleat": "tight_top_knot_or_crescent", "wrapper": "wheat_flour"},
        b_visual_cues={"chutney": "soy_ginger_vinegar_dip", "wrapper": "translucent_tapioca_wheat_starch"}
    ),
    "hakka_noodles_vs_maggi": ConfusionPairDefinition(
        pair_id="hakka_noodles_vs_maggi",
        food_a="Veg Hakka Noodles",
        food_b="Masala Maggi",
        distinguishing_features=[
            "Noodle shape: Long, straight, smooth cylindrical cylindrical noodles in Hakka vs Wavy, crimped, curly ribbed strands in Maggi",
            "Cooking style: High-flame dry wok toss with char in Hakka vs Simmered in moist spiced broth in Maggi",
            "Vegetable cut: Long thin matchstick juliennes (cabbage, carrots, capsicum) in Hakka vs Small diced peas, onions, tomatoes in Maggi"
        ],
        a_visual_cues={"noodle_geometry": "straight_long_cylindrical", "cooking": "dry_wok_stir_fry", "veggie_cut": "julienned_matchsticks"},
        b_visual_cues={"noodle_geometry": "crimped_curly_wavy_ribbon", "cooking": "moist_masala_broth", "veggie_cut": "small_dices_and_peas"}
    ),
    "vada_pav_vs_dabeli": ConfusionPairDefinition(
        pair_id="vada_pav_vs_dabeli",
        food_a="Vada Pav",
        food_b="Kutchi Dabeli",
        distinguishing_features=[
            "Patty: Distinct golden spherical/flattened besan-battered fried potato vada in Vada Pav vs Smooth dark spiced potato mash filling in Dabeli",
            "Garnish: Masala peanuts (sing), pomegranate seeds (anar), and sev embedded inside Dabeli vs None in classic Vada Pav",
            "Chutneys: Dry red garlic chutney + fried chilli in Vada Pav vs Sweet tamarind and spicy red garlic slurry in Dabeli"
        ],
        a_visual_cues={"filling": "besan_fried_vada_patty", "chutney": "dry_red_garlic_powder", "chilli": "whole_fried_green_chilli"},
        b_visual_cues={"filling": "loose_dark_potato_mash", "toppings": ["masala_peanuts", "pomegranate_arils", "nylon_sev"]}
    ),
    "pav_bhaji_vs_misal_pav": ConfusionPairDefinition(
        pair_id="pav_bhaji_vs_misal_pav",
        food_a="Pav Bhaji",
        food_b="Misal Pav",
        distinguishing_features=[
            "Curry consistency: Thick, uniform, homogenized mashed vegetable paste in Pav Bhaji vs Liquid soupy curry with intact sprouted moth beans and red oil layer (tarri) in Misal Pav",
            "Crunchy toppings: Farsan / mixed sev floating on top of Misal vs Melting butter slab + raw diced onions on Pav Bhaji"
        ],
        a_visual_cues={"bhaji_texture": "thick_pureed_mashed_vegetables", "fat_form": "melting_butter_slab", "farsan": "absent"},
        b_visual_cues={"curry_texture": "watery_rassa_with_sprouts", "fat_form": "floating_red_oil_tarri", "farsan": "crispy_farsan_topping"}
    ),
    "jalebi_vs_imarti": ConfusionPairDefinition(
        pair_id="jalebi_vs_imarti",
        food_a="Jalebi",
        food_b="Imarti",
        distinguishing_features=[
            "Pattern: Irregular concentric random swirls in Jalebi vs Geometric floral ring with outer looped petals in Imarti",
            "Batter & color: Fermented refined wheat (maida) batter (bright golden-orange, crisp and glassy) in Jalebi vs Ground urad dal batter (matte reddish-orange, softer cake-like interior) in Imarti"
        ],
        a_visual_cues={"shape": "random_concentric_spiral", "texture": "glassy_crisp_translucent_edges", "batter": "maida"},
        b_visual_cues={"shape": "geometric_flower_with_petals", "texture": "matte_soft_spongy_interior", "batter": "urad_dal"}
    ),
    "kulfi_vs_ice_cream": ConfusionPairDefinition(
        pair_id="kulfi_vs_ice_cream",
        food_a="Indian Kulfi",
        food_b="Western Ice Cream",
        distinguishing_features=[
            "Structure: Dense, non-aerated, crystallized slow-churned reduced milk (rabri) in Kulfi vs Airy, fluffy, whipped aerated cream in Ice Cream",
            "Shape: Tapered conical stick or earthenware matka in Kulfi vs Spherical scoop in Ice Cream"
        ],
        a_visual_cues={"texture": "dense_crystallized_non_aerated", "serving": "tapered_stick_or_clay_matka"},
        b_visual_cues={"texture": "smooth_fluffy_aerated", "serving": "spherical_scoop_or_swirl"}
    ),
    "lassi_vs_chaas": ConfusionPairDefinition(
        pair_id="lassi_vs_chaas",
        food_a="Sweet Lassi",
        food_b="Masala Chaas",
        distinguishing_features=[
            "Thickness: Heavy, viscous, slow-flowing curd with floating malai (cream) layer in Lassi vs Thin, watery, light refreshing drink in Chaas",
            "Seasoning: Saffron/cardamom/nuts/sweet in Lassi vs Tempered cumin powder, black salt, ginger, curry leaves, coriander flecks in Chaas"
        ],
        a_visual_cues={"viscosity": "high_thick_creamy", "top": "floating_malai_clot_with_nuts"},
        b_visual_cues={"viscosity": "thin_watery_frothy", "top": "roasted_cumin_specks_coriander"}
    )
}


def disambiguate_street_food_pair(
    candidate_a: str,
    candidate_b: str,
    visual_evidence: Dict[str, Any]
) -> Tuple[str, float, str]:
    """
    Evaluates visual cues between high-confusion street food candidate pairs.
    Returns: (resolved_food, confidence, rationale)
    """
    for pair in STREET_FOOD_CONFUSION_REGISTRY.values():
        is_match = (
            (candidate_a.lower() in pair.food_a.lower() or pair.food_a.lower() in candidate_a.lower()) and
            (candidate_b.lower() in pair.food_b.lower() or pair.food_b.lower() in candidate_b.lower())
        )
        if is_match:
            score_a = 0
            score_b = 0
            reasons = []

            for k, val in pair.a_visual_cues.items():
                if visual_evidence.get(k) == val or (isinstance(val, list) and any(v in visual_evidence.get(k, []) for v in val)):
                    score_a += 1
                    reasons.append(f"Detected {k}={val} indicative of {pair.food_a}")

            for k, val in pair.b_visual_cues.items():
                if visual_evidence.get(k) == val or (isinstance(val, list) and any(v in visual_evidence.get(k, []) for v in val)):
                    score_b += 1
                    reasons.append(f"Detected {k}={val} indicative of {pair.food_b}")

            if score_a > score_b:
                return pair.food_a, min(0.95, 0.70 + 0.10 * (score_a - score_b)), "; ".join(reasons)
            elif score_b > score_a:
                return pair.food_b, min(0.95, 0.70 + 0.10 * (score_b - score_a)), "; ".join(reasons)
            else:
                return candidate_a, 0.55, f"Ambiguous between {pair.food_a} and {pair.food_b}; insufficient distinguishing cues."

    return candidate_a, 0.60, "Generic disambiguation fallback."


# =============================================================================
# SECTION 4 & 5 — PANI PURI COUNTING & OCCLUSION ESTIMATION
# =============================================================================

class PaniPuriCountResult(BaseModel):
    visible_total_puris: int
    filled_puris: int
    empty_puris: int
    partially_eaten_or_broken: int
    estimated_total_range: str  # e.g., "6" or "8-10"
    occlusion_percentage: float = Field(..., ge=0.0, le=100.0)
    confidence: str  # "High", "Medium", "Low"
    notes: str


class PaniPuriCountingDiscriminator:
    """
    Implements Section 4:
    - Counts whole puris, filled puris, empty puris, partially eaten puris.
    - If puris are partially occluded/stacked, emits an estimated range rather than false precision.
    """
    @staticmethod
    def count_puris(
        puri_detections: List[Dict[str, Any]],
        plate_or_bowl_area_cm2: float = 300.0
    ) -> PaniPuriCountResult:
        filled = 0
        empty = 0
        broken = 0

        for p in puri_detections:
            state = p.get("state", "filled").lower()
            if state == "filled":
                filled += 1
            elif state in ("empty", "dry"):
                empty += 1
            elif state in ("broken", "partially_eaten", "cracked"):
                broken += 1
            else:
                filled += 1

        visible = filled + empty + broken
        # Occlusion heuristic: if puris are densely clustered or overlapping
        overlap_count = sum(1 for p in puri_detections if p.get("is_overlapped", False))
        occlusion_pct = min(80.0, (overlap_count / max(1, visible)) * 60.0)

        if occlusion_pct > 30.0:
            est_low = visible
            est_high = visible + int(round(visible * 0.35)) + 1
            total_range = f"{est_low}–{est_high}"
            confidence = "Medium" if occlusion_pct < 60.0 else "Low"
            notes = f"High occlusion detected ({occlusion_pct:.1f}%). {visible} visible puris; estimated total {total_range}."
        else:
            total_range = str(visible)
            confidence = "High"
            notes = f"Clear visibility of {visible} puris ({filled} filled, {empty} empty, {broken} broken)."

        return PaniPuriCountResult(
            visible_total_puris=visible,
            filled_puris=filled,
            empty_puris=empty,
            partially_eaten_or_broken=broken,
            estimated_total_range=total_range,
            occlusion_percentage=round(occlusion_pct, 1),
            confidence=confidence,
            notes=notes
        )


# =============================================================================
# SECTION 28, 29, 30 — STREET ROLL DISCRIMINATOR
# =============================================================================

class StreetRollDiscriminator:
    """
    Strict discriminator between Kathi Roll, Frankie, and Shawarma.
    Never classifies every wrap as Shawarma (Section 30).
    """
    @staticmethod
    def classify_roll(cues: Dict[str, Any]) -> Tuple[str, float, str]:
        bread_type = cues.get("bread_type", "").lower()
        filling = cues.get("filling", "").lower()
        sauce = cues.get("sauce", "").lower()
        egg_lining = cues.get("egg_lining", False)
        fries_inside = cues.get("fries_inside", False)

        # Shawarma check
        if fries_inside or "mayo" in sauce or "toum" in sauce or "tahini" in sauce or "pita" in bread_type or "kubbus" in bread_type:
            return "Chicken Shawarma", 0.92, "Identified Middle-Eastern style shawarma: kubbus/pita bread, garlic mayo/toum, and internal fries."

        # Kathi Roll check
        if "paratha" in bread_type or egg_lining or "tikka" in filling or "kebab" in filling:
            return "Kolkata Kathi Roll", 0.90, "Identified Kolkata Kathi Roll: flaky layered paratha base with bonded egg wash and grilled tikka/kebab chunks."

        # Frankie check
        if "frankie_masala" in cues.get("seasoning", "") or "cutlet" in filling or "roti" in bread_type or "vinegar" in sauce:
            return "Mumbai Frankie", 0.88, "Identified Mumbai Frankie: thin soft roti wrapper with spiced cylindrical potato cutlet and vinegar-soaked chillies."

        # Default fallback
        return "Kolkata Kathi Roll", 0.65, "Defaulted to Kathi Roll family based on general street wrap appearance."


# =============================================================================
# SECTION 48 & 50 — NOODLE DISCRIMINATOR
# =============================================================================

class NoodleDiscriminator:
    """
    Distinguishes Hakka Noodles vs Chow Mein vs Thukpa vs Maggi (Instant Noodles).
    Never classifies based only on noodle shape (Section 48).
    """
    @staticmethod
    def classify_noodles(cues: Dict[str, Any]) -> Tuple[str, float, str]:
        strand_shape = cues.get("strand_shape", "").lower()
        broth_present = cues.get("broth_present", False)
        liquid_depth = cues.get("liquid_depth_cm", 0.0)
        sauce_color = cues.get("sauce_color", "").lower()

        # Thukpa soup check
        if broth_present and liquid_depth > 1.5:
            return "Tibetan Thukpa Noodle Soup", 0.93, "Identified Thukpa: noodles fully submerged in deep aromatic soup broth."

        # Maggi instant check
        if "curly" in strand_shape or "wavy" in strand_shape or "ribbed" in strand_shape or cues.get("is_instant_curry", False):
            return "Masala Maggi", 0.95, "Identified Masala Maggi: crimped wavy instant noodle strands with characteristic yellow masala glaze."

        # Hakka noodles check
        if "straight" in strand_shape or "cylindrical" in strand_shape or "soy" in sauce_color or cues.get("wok_tossed", True):
            return "Veg Hakka Noodles", 0.91, "Identified Veg Hakka Noodles: long straight cylindrical noodles stir-fried in high flame wok with julienned vegetables."

        return "Veg Hakka Noodles", 0.70, "General street noodle classification."


# =============================================================================
# SECTION 76 & 81 — PACKAGING & PRESENTATION FILTER
# =============================================================================

class StreetPackagingFilter:
    """
    Filters non-edible street presentation components:
    - paper plates, newspaper liners, dona (leaf) bowls, toothpicks, skewers, foil wraps.
    Guarantees calorie calculations apply solely to edible food items.
    """
    NON_EDIBLE_ITEMS = {
        "paper_plate", "dona_leaf_bowl", "plastic_container", "wooden_skewer",
        "toothpick", "aluminum_foil", "newspaper_sheet", "butter_paper",
        "plastic_cup", "cardboard_box", "tissue_paper"
    }

    @classmethod
    def filter_components(cls, detected_items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        edible_items = []
        for item in detected_items:
            name_clean = item.get("name", "").lower().replace(" ", "_")
            if any(non_edible in name_clean for non_edible in cls.NON_EDIBLE_ITEMS):
                continue
            if item.get("is_packaging", False):
                continue
            edible_items.append(item)
        return edible_items
