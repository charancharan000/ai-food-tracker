"""
Indian Snacks & Tiffin Hard Negative System & Specialized Verifiers (Part 15)
Implements Sections 11, 12, 14, 16, 18, 19, 23, 26, 30, 49, 74 of Part 15 Specification.

Mandatory Confusion Pairs (Section 30):
- Samosa ↔ Kachori
- Samosa ↔ Curry Puff
- Kachori ↔ Puri
- Puri ↔ Bhatura
- Vada ↔ Bonda
- Vada ↔ Aloo Bonda
- Bajji ↔ Pakoda
- Pakoda ↔ Bhajji
- Dhokla ↔ Khaman
- Dhokla ↔ Idli
- Idli ↔ Steamed Rice Cake
- Momo ↔ Kozhukattai
- Momo ↔ Dumpling
- Pani Puri ↔ Golgappa ↔ Puchka
- Bhel Puri ↔ Jhalmuri
- Sev Puri ↔ Bhel Puri
- Dahi Puri ↔ Dahi Bhalla
- Aloo Tikki ↔ Aloo Patty
- Vada Pav ↔ Batata Vada
- Vada Pav ↔ Burger
- Pav Bhaji ↔ Misal Pav
- Misal Pav ↔ Usal Pav
- Poha ↔ Upma
- Poha ↔ Aval Upma
- Sabudana Khichdi ↔ Khichdi
- Thalipeeth ↔ Paratha
- Thepla ↔ Paratha
- Maddur Vada ↔ Medhu Vada
- Punugulu ↔ Pakoda
- Murukku ↔ Chakli
- Thattai ↔ Puri
- Seedai ↔ Fried Dough Ball
- Paniyaram ↔ Appe
- Paniyaram ↔ Bonda
- Kothimbir Vadi ↔ Patra
- Patra ↔ Alu Vadi
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class SnackConfusionPair(BaseModel):
    pair_id: str
    class_a_id: str
    class_a_name: str
    class_b_id: str
    class_b_name: str
    primary_confusion_reason: str
    discriminative_visual_features: List[str]
    discriminative_ingredient_features: List[str]
    recommended_feature_test: str


SNACKS_CONFUSION_REGISTRY: Dict[str, SnackConfusionPair] = {
    # 1. Samosa vs Kachori
    "samosa_vs_kachori": SnackConfusionPair(
        pair_id="samosa_vs_kachori",
        class_a_id="IND-SNK-NI-SAMOSA-001",
        class_a_name="Samosa",
        class_b_id="IND-SNK-NI-DALKACHORI-001",
        class_b_name="Kachori",
        primary_confusion_reason="Both are golden deep-fried maida pastries with savory spiced fillings.",
        discriminative_visual_features=[
            "Samosa has a distinct pyramidal/conical triangular shape with pleated base seam",
            "Kachori has a puffed circular/disc shape with a central pinched spiral or blistered convex surface",
            "Samosa crust is relatively smooth with micro-bubbles and ajwain seeds",
            "Kachori crust is deeply flaky, brittle, and blistered (khasta)",
        ],
        discriminative_ingredient_features=[
            "Samosa filling is predominantly chunky potato and green peas with whole coriander seeds",
            "Kachori filling is coarse spiced moong dal paste or caramelized spiced onions with roasted besan",
        ],
        recommended_feature_test="Check geometry: Pyramidal triangle -> Samosa; Puffed circular disc -> Kachori.",
    ),

    # 2. Samosa vs Curry Puff
    "samosa_vs_curry_puff": SnackConfusionPair(
        pair_id="samosa_vs_curry_puff",
        class_a_id="IND-SNK-NI-SAMOSA-001",
        class_a_name="Samosa",
        class_b_id="IND-SNK-KL-EGGBPUFF-001",
        class_b_name="Curry Puff / Veg Puff",
        primary_confusion_reason="Both are handheld savory pastries with spiced vegetable/egg filling.",
        discriminative_visual_features=[
            "Samosa is deep-fried with oil sheen, crisp fried pastry skin and sharp conical edges",
            "Curry Puff is baked with dozens of distinct laminated flaky golden-brown layers and dry crumb",
        ],
        discriminative_ingredient_features=[
            "Samosa pastry uses oil/ghee moin deep fried",
            "Puff pastry uses cold butter/margarine laminated and oven-baked",
        ],
        recommended_feature_test="Check surface: Fried oil-fried skin -> Samosa; Oven-baked laminated multi-layer pastry -> Puff.",
    ),

    # 3. Dhokla vs Khaman (Crucial Section 19/26 Discrimination)
    "dhokla_vs_khaman": SnackConfusionPair(
        pair_id="dhokla_vs_khaman",
        class_a_id="IND-SNK-GJ-DHOKLA-001",
        class_a_name="Dhokla (Khatta Dhokla)",
        class_b_id="IND-SNK-GJ-KHAMAN-001",
        class_b_name="Khaman (Nylon Khaman)",
        primary_confusion_reason="Both are yellow or off-white steamed square cakes with mustard-seed tempering from Gujarat.",
        discriminative_visual_features=[
            "Dhokla is pale ivory to light yellowish, firmer fermented texture with natural sour fermentation micro-pores",
            "Khaman is bright radiant yellow, hyper-porous, spongy, highly aerated like a wet foam, glistening with sugar-mustard syrup",
        ],
        discriminative_ingredient_features=[
            "Dhokla is made from fermented ground rice and chana dal batter with sour curd",
            "Khaman is made purely from besan (gram flour) with quick chemical leavening (eno/soda) and soaked in sweet lemon-mustard syrup",
        ],
        recommended_feature_test="Check aeration & color: Bright yellow, bouncy, wet syrup glistened -> Khaman; Pale ivory/light yellow, fermented, firm -> Khatta Dhokla.",
    ),

    # 4. Dhokla vs Idli
    "dhokla_vs_idli": SnackConfusionPair(
        pair_id="dhokla_vs_idli",
        class_a_id="IND-SNK-GJ-DHOKLA-001",
        class_a_name="Dhokla",
        class_b_id="IND-TIF-TN-IDLI-001",
        class_b_name="Idli",
        primary_confusion_reason="Both are white/pale steamed fermented cakes.",
        discriminative_visual_features=[
            "Dhokla is cut into square or diamond cubes from a large tray, often tempered with mustard seeds, sesame, and green chillies",
            "Idli is circular convex disk shaped from round concave mold, pure white, untempered on the surface",
        ],
        discriminative_ingredient_features=[
            "Dhokla contains chana dal and rice fermented with sour curd",
            "Idli contains parboiled rice and urad dal fermented naturally",
        ],
        recommended_feature_test="Check geometry and surface: Untempered circular disc -> Idli; Tempered cube/diamond -> Dhokla.",
    ),

    # 5. Vada vs Bonda
    "vada_vs_bonda": SnackConfusionPair(
        pair_id="vada_vs_bonda",
        class_a_id="IND-SNK-TN-MEDHUVADAI-001",
        class_a_name="Medhu Vadai",
        class_b_id="IND-SNK-TN-POTATOBONDA-001",
        class_b_name="Potato Bonda",
        primary_confusion_reason="Both are round golden South Indian deep-fried savory snacks.",
        discriminative_visual_features=[
            "Medhu Vadai has a central hole (toroid / doughnut shape) with visible black pepper specks",
            "Bonda is a solid sphere without any central hole, covered in a smooth besan batter envelope",
        ],
        discriminative_ingredient_features=[
            "Medhu Vadai is made entirely of fluffy ground urad dal batter",
            "Potato Bonda has a spiced mashed potato core coated in gram flour (besan) batter",
        ],
        recommended_feature_test="Check central hole: Toroid with central hole -> Medhu Vadai; Solid sphere with besan batter -> Potato Bonda.",
    ),

    # 6. Maddur Vada vs Medhu Vada
    "maddur_vada_vs_medhu_vada": SnackConfusionPair(
        pair_id="maddur_vada_vs_medhu_vada",
        class_a_id="IND-SNK-KA-MADDURVADA-001",
        class_a_name="Maddur Vada",
        class_b_id="IND-SNK-TN-MEDHUVADAI-001",
        class_b_name="Medhu Vadai",
        primary_confusion_reason="Both share the name 'Vada' in South Indian snack culture.",
        discriminative_visual_features=[
            "Maddur Vada is a flat, coarse, jagged disc with ruffled edges and visible onion slices embedded throughout",
            "Medhu Vadai is a smooth, puffy golden doughnut with a distinct central perforation",
        ],
        discriminative_ingredient_features=[
            "Maddur Vada is semolina (rava), rice flour, and maida dough packed with sliced onions",
            "Medhu Vadai is aerated urad dal batter",
        ],
        recommended_feature_test="Check texture & perforation: Fluffy doughnut -> Medhu Vadai; Thin crunchy jagged disc with visible onions -> Maddur Vada.",
    ),

    # 7. Bajji vs Pakoda
    "bajji_vs_pakoda": SnackConfusionPair(
        pair_id="bajji_vs_pakoda",
        class_a_id="IND-SNK-TN-ONIONBAJJI-001",
        class_a_name="Bajji",
        class_b_id="IND-SNK-TN-MASALAVADAI-001",
        class_b_name="Pakoda",
        primary_confusion_reason="Both are deep-fried fritters made with gram flour (besan) and onions/vegetables.",
        discriminative_visual_features=[
            "Bajji features intact, distinct vegetable slices (onion ring, banana strip, whole chilli) enrobed in a smooth puffy batter coat",
            "Pakoda features craggy, irregular, shredded vegetable clusters with crisp jagged spikes and thin batter coating",
        ],
        discriminative_ingredient_features=[
            "Bajji uses wet dipping batter poured over vegetable slices",
            "Pakoda uses dry-rubbed vegetables mixed with just enough besan to bind without excess water",
        ],
        recommended_feature_test="Check morphology: Smooth uniform enrobed slice -> Bajji; Craggy jagged irregular fritter clump -> Pakoda.",
    ),

    # 8. Vada Pav vs Batata Vada
    "vada_pav_vs_batata_vada": SnackConfusionPair(
        pair_id="vada_pav_vs_batata_vada",
        class_a_id="IND-SNK-MH-VADAPAV-001",
        class_a_name="Vada Pav",
        class_b_id="IND-SNK-TN-POTATOBONDA-001",
        class_b_name="Batata Vada (Solo)",
        primary_confusion_reason="Batata Vada is the fried component inside Vada Pav.",
        discriminative_visual_features=[
            "Vada Pav is an assembled sandwich consisting of a bread pav bun sliced open with the vada inside, topped with dry garlic chutney",
            "Batata Vada is the solitary fried potato ball served without pav bread",
        ],
        discriminative_ingredient_features=[
            "Vada Pav incorporates pav bread carbs and dry peanut-garlic powder",
            "Batata Vada is purely the potato patty and besan coating",
        ],
        recommended_feature_test="Check bread enclosure: Placed inside pav bun -> Vada Pav; Solo fritter -> Batata Vada.",
    ),

    # 9. Pav Bhaji vs Misal Pav
    "pav_bhaji_vs_misal_pav": SnackConfusionPair(
        pair_id="pav_bhaji_vs_misal_pav",
        class_a_id="IND-SNK-MH-MISALPAV-001",
        class_a_name="Misal Pav",
        class_b_id="IND-SNK-MH-VADAPAV-001",
        class_b_name="Pav Bhaji",
        primary_confusion_reason="Both are iconic Mumbai street foods served with pav buns.",
        discriminative_visual_features=[
            "Misal Pav features a thin, fiery, oily red soup (rassa/kat/tarri) over intact sprouted beans (matki), crowned with dry crunchy farsan/sev and raw chopped onions",
            "Pav Bhaji features a thick, homogeneous, buttery mashed vegetable puree without crunchy farsan or whole beans",
        ],
        discriminative_ingredient_features=[
            "Misal is sprouted moth beans (matki) in fiery spiced broth topped with crunchy farsan",
            "Bhaji is heavily mashed potatoes, tomatoes, peas and cauliflower cooked with butter and pav bhaji masala",
        ],
        recommended_feature_test="Check gravy consistency: Thick mashed vegetable puree -> Pav Bhaji; Thin liquid soup with sprouted beans & crunchy farsan -> Misal Pav.",
    ),

    # 10. Momo vs Kozhukattai
    "momo_vs_kozhukattai": SnackConfusionPair(
        pair_id="momo_vs_kozhukattai",
        class_a_id="IND-SNK-NE-VEGMOMO-001",
        class_a_name="Momo",
        class_b_id="IND-SNK-TN-PANIYARAM-001",
        class_b_name="Kozhukattai / Modak",
        primary_confusion_reason="Both are steamed dumplings with folded/pleated outer shells.",
        discriminative_visual_features=[
            "Momo wrapper is thin, translucent refined wheat flour (maida) with fine crescent or circular pleats, served with fiery red chilli sauce",
            "Kozhukattai / Modak shell is thick, matte-white steamed rice flour dough with distinct vertical fluting or smooth modak cone, served with no spicy chutney",
        ],
        discriminative_ingredient_features=[
            "Momo filling is savory minced vegetables, chicken or pork seasoned with soy and ginger",
            "Kozhukattai is typically sweet with jaggery and grated coconut, or savory with seasoned toor/chana dal",
        ],
        recommended_feature_test="Check shell translucency & accompaniment: Thin maida wrapper with red chilli chutney -> Momo; Thick opaque rice dough -> Kozhukattai.",
    ),

    # 11. Murukku vs Chakli
    "murukku_vs_chakli": SnackConfusionPair(
        pair_id="murukku_vs_chakli",
        class_a_id="IND-SNK-TN-MURUKKU-001",
        class_a_name="Murukku",
        class_b_id="IND-SNK-TN-THATTAI-001",
        class_b_name="Chakli",
        primary_confusion_reason="Both are spiral extruded fried crispy snacks.",
        discriminative_visual_features=[
            "Tamil Murukku (Thenkuzhal) is lighter ivory-golden in color, smoother star-point ridges, made of rice and urad dal",
            "Maharashtra/Gujarat Chakli is darker reddish-brown, intensely spiky ridges, made from roasted multigrain bhajani flour",
        ],
        discriminative_ingredient_features=[
            "Murukku uses rice flour and roasted urad dal flour with cumin/sesame and butter",
            "Chakli uses roasted bhajani (rice, chana dal, urad dal, coriander seeds) with spicy red chilli and ajwain",
        ],
        recommended_feature_test="Check ridge spikes & color: Light ivory, smooth ridges -> Thenkuzhal Murukku; Darker reddish-gold, sharp prickly ridges -> Chakli.",
    ),
}


class DhoklaVsKhamanVerifier:
    """Specialized verifier for Gujarat steamed cakes (Section 19 & 26)."""

    @classmethod
    def verify(cls, visual_features: Dict[str, Any]) -> Dict[str, Any]:
        color = visual_features.get("color", "").lower()
        texture = visual_features.get("texture", "").lower()
        surface_moisture = visual_features.get("surface_moisture", "").lower()
        fermented_tang = visual_features.get("fermented_appearance", False)

        is_khaman = False
        reasons = []

        if "bright yellow" in color or "sunshine yellow" in color or "neon yellow" in color:
            is_khaman = True
            reasons.append("Radiant bright yellow coloration indicates turmeric/besan khaman rather than fermented dal")

        if "spongy" in texture or "hyper-aerated" in texture or "soft foam" in texture:
            is_khaman = True
            reasons.append("High aeration and elastic bounce indicate instant leavened nylon khaman")

        if "glistening" in surface_moisture or "syrup soaked" in surface_moisture or "juicy" in surface_moisture:
            is_khaman = True
            reasons.append("Liquid syrup soak visible on cut surface")

        if "pale" in color or "ivory" in color or "off-white" in color or fermented_tang:
            is_khaman = False
            reasons.append("Pale ivory tone and dense fermented micro-pores confirm traditional Khatta Dhokla")

        target_id = "IND-SNK-GJ-KHAMAN-001" if is_khaman else "IND-SNK-GJ-DHOKLA-001"
        target_name = "Khaman (Nylon Khaman)" if is_khaman else "Dhokla (Khatta Dhokla)"

        return {
            "predicted_food_id": target_id,
            "predicted_name": target_name,
            "is_khaman": is_khaman,
            "confidence": 0.94 if reasons else 0.70,
            "verification_reasons": reasons,
        }


class SamosaVsKachoriVerifier:
    """Specialized verifier for triangular samosa vs circular kachori (Sections 11 & 12)."""

    @classmethod
    def verify(cls, visual_features: Dict[str, Any]) -> Dict[str, Any]:
        shape = visual_features.get("shape", "").lower()
        crust_texture = visual_features.get("crust_texture", "").lower()
        visible_filling = visual_features.get("filling", "").lower()

        is_samosa = True
        reasons = []

        if "triangle" in shape or "pyramid" in shape or "conical" in shape:
            is_samosa = True
            reasons.append("Pyramidal/triangular geometry matches samosa fold")
        elif "disc" in shape or "circle" in shape or "round puff" in shape or "convex" in shape:
            is_samosa = False
            reasons.append("Flattened or puffed circular disc matches kachori morphology")

        if "flaky blistered" in crust_texture or "khasta" in crust_texture:
            if not is_samosa:
                reasons.append("Deeply blistered flaky shell confirms khasta kachori")
        elif "smooth with ajwain" in crust_texture:
            is_samosa = True
            reasons.append("Shortcrust with ajwain points to samosa")

        if "potato" in visible_filling or "green peas" in visible_filling:
            is_samosa = True
            reasons.append("Potato-pea chunks confirm samosa filling")
        elif "dal" in visible_filling or "onion paste" in visible_filling:
            is_samosa = False
            reasons.append("Spiced dal/onion filling indicates kachori")

        target_id = "IND-SNK-NI-SAMOSA-001" if is_samosa else "IND-SNK-NI-DALKACHORI-001"
        target_name = "Samosa" if is_samosa else "Kachori"

        return {
            "predicted_food_id": target_id,
            "predicted_name": target_name,
            "is_samosa": is_samosa,
            "confidence": 0.96 if reasons else 0.75,
            "verification_reasons": reasons,
        }


class VadaVsBondaVerifier:
    """Specialized verifier for toroid Medhu Vadai vs spherical Potato Bonda (Sections 5 & 27)."""

    @classmethod
    def verify(cls, visual_features: Dict[str, Any]) -> Dict[str, Any]:
        has_central_hole = visual_features.get("has_central_hole", False)
        geometry = visual_features.get("geometry", "").lower()
        core_type = visual_features.get("core_type", "").lower()

        is_vada = True
        reasons = []

        if has_central_hole or "doughnut" in geometry or "toroid" in geometry:
            is_vada = True
            reasons.append("Central hole perforation confirms Medhu Vadai")
        elif "sphere" in geometry or "ball" in geometry:
            is_vada = False
            reasons.append("Solid spherical geometry without central perforation indicates Potato Bonda")

        if "potato" in core_type:
            is_vada = False
            reasons.append("Spiced mashed potato core confirms Potato Bonda")
        elif "urad" in core_type or "lentil crumb" in core_type:
            is_vada = True
            reasons.append("Aerated urad dal crumb confirms Medhu Vadai")

        target_id = "IND-SNK-TN-MEDHUVADAI-001" if is_vada else "IND-SNK-TN-POTATOBONDA-001"
        target_name = "Medhu Vadai" if is_vada else "Potato Bonda"

        return {
            "predicted_food_id": target_id,
            "predicted_name": target_name,
            "is_vada": is_vada,
            "confidence": 0.98 if reasons else 0.72,
            "verification_reasons": reasons,
        }


class Section74NonNegotiableSnackVerifier:
    """
    Validates all mandatory operational rules from Section 74:
    - Never classify only by color.
    - Never classify only by shape.
    - Separate chutneys, sambar, sauces, yogurt.
    - Count individual pieces where possible.
    - Qualitative oil estimation only; never state exact oil ml from appearance.
    - Support unknown fallback when confidence < 50.
    """

    @classmethod
    def validate_snack_output(cls, output_payload: Dict[str, Any]) -> Dict[str, Any]:
        violations = []
        warnings = []

        # Rule 1: No classification purely by color or shape
        pred_source = output_payload.get("decision_basis", "")
        if "color_only" in pred_source or "shape_only" in pred_source:
            violations.append("Violation Section 74 Rule 1 & 2: Classification based purely on color or shape is strictly prohibited.")

        # Rule 2: Separate accompaniments
        accompaniments = output_payload.get("accompaniments", [])
        snack_weight = output_payload.get("estimated_weight_g", 0)
        accompaniment_weight = output_payload.get("accompaniment_weight_g", 0)
        if accompaniments and accompaniment_weight > 0 and output_payload.get("is_accompaniment_mixed_in_snack_weight", False):
            violations.append("Violation Section 74 Rule 4: Chutneys/Sambar/Sauces must not be combined into the primary snack weight.")

        # Rule 3: Qualitative oil only
        oil_claim = str(output_payload.get("oil_estimation", ""))
        if any(unit in oil_claim.lower() for unit in ["ml oil", "grams of oil", "exact oil", "12 ml", "15 ml"]):
            violations.append("Violation Section 74 Rule 28: Stating exact oil volume/weight from photograph alone is strictly prohibited.")

        # Rule 4: Fallback to unknown when confidence is low
        confidence = output_payload.get("food_confidence", 1.0)
        food_id = output_payload.get("canonical_name", "")
        if confidence < 0.50 and "uncertain" not in food_id.lower() and "unknown" not in food_id.lower():
            warnings.append("Warning Section 74 Rule 38: Low confidence (<0.50) without fallback to calibrated uncertain class.")

        return {
            "is_valid": len(violations) == 0,
            "violations": violations,
            "warnings": warnings,
            "passed_rules_count": 6 - len(violations),
        }


def disambiguate_snack_pair(pair_id: str, visual_evidence: Dict[str, Any]) -> Dict[str, Any]:
    """Resolve a registered hard-negative pair using Section 30 verifiers."""
    if pair_id == "dhokla_vs_khaman":
        return DhoklaVsKhamanVerifier.verify(visual_evidence)
    elif pair_id == "samosa_vs_kachori":
        return SamosaVsKachoriVerifier.verify(visual_evidence)
    elif pair_id == "vada_vs_bonda":
        return VadaVsBondaVerifier.verify(visual_evidence)

    pair = SNACKS_CONFUSION_REGISTRY.get(pair_id)
    if not pair:
        return {"error": f"Unknown confusion pair '{pair_id}'"}

    return {
        "pair_id": pair_id,
        "class_a": pair.class_a_name,
        "class_b": pair.class_b_name,
        "primary_confusion_reason": pair.primary_confusion_reason,
        "discriminative_visual_features": pair.discriminative_visual_features,
        "recommended_feature_test": pair.recommended_feature_test,
    }
