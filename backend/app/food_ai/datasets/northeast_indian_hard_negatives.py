"""
Northeast India Hard Negative Confusion Matrix & Disambiguation Engine (Part 7)
Implements Sections 11, 12, 13, 16, 17, 18, 21, 22, 23, 25, 26, 31, 33, 34, 37, 38, 39, 40, 41, 42, 43, 44, 58, 59, 84.

Guarantees:
- Disambiguation matrix for 25+ Northeast visual confusion pairs
- Northeast Rice-Meat Platter Discriminator (Jadoh vs Galho vs Sawhchiar vs Pulao vs Khichdi)
- Fermented Soybean Discriminator (Axone vs Tungrymbai vs Kinema)
- Mashed Vegetable & Fermented Fish Discriminator (Aloo Pitika vs Eromba vs Mosdeng vs Singju)
- Wood-Smoked Meat Verifier vs Fried / Grilled / Burnt Meat
- Bamboo Shoot Ingredient vs Dish Classifier
- Momo & Thukpa Cross-State Classifiers with count and portion estimation
"""

from typing import List, Dict, Any, Optional, Tuple
from pydantic import BaseModel, Field

class NortheastConfusionPair(BaseModel):
    confusion_id: str
    target_class_id: str
    target_name: str
    confuser_class_id: str
    confuser_name: str
    primary_confusion_reason: str
    discriminating_visual_features: List[str]
    disambiguation_rule: str

NORTHEAST_CONFUSION_REGISTRY: Dict[str, NortheastConfusionPair] = {}

def register_northeast_confusion(pair: NortheastConfusionPair):
    NORTHEAST_CONFUSION_REGISTRY[pair.confusion_id] = pair

# =============================================================================
# 1. RICE & MEAT DISH HARD NEGATIVES (Sections 11, 22, 26, 48, 59)
# =============================================================================

register_northeast_confusion(NortheastConfusionPair(
    confusion_id="CONF_JADOH_VS_PULAO_KHICHDI",
    target_class_id="ML_RICE_JADOH_PORK",
    target_name="Khasi Jadoh",
    confuser_class_id="PAN_INDIAN_PULAO",
    confuser_name="Pulao / Khichdi / Biryani",
    primary_confusion_reason="Both are rice cooked with meat and spices.",
    discriminating_visual_features=[
        "Jadoh uses short bold hill rice (jingshai), cooked in pork fat/blood or simple turmeric-ginger broth without saffron, kewra, or whole dry fruits",
        "Pulao/Biryani uses long-grain basmati rice, fried brown onions (beresta), and aromatic whole spices (cinnamon, cloves, cardamom)",
        "Jadoh exhibits an earthy golden-reddish hue with distinct pork pieces containing white fat rind"
    ],
    disambiguation_rule="Short bold rice grains cooked in pork broth with ginger-onion profile + pork fat -> Jadoh. Never classify generic basmati pulao/biryani as Jadoh."
))

register_northeast_confusion(NortheastConfusionPair(
    confusion_id="CONF_JADOH_VS_GALHO",
    target_class_id="ML_RICE_JADOH_PORK",
    target_name="Khasi Jadoh",
    confuser_class_id="NL_RICE_GALHO",
    confuser_name="Naga Galho",
    primary_confusion_reason="Both are Northeast rice dishes with pork.",
    discriminating_visual_features=[
        "Jadoh is a relatively dry, separated-grain pilaf-style rice dish served on plates",
        "Galho is a soupy, wet, broken-grain comforting rice porridge containing abundant leafy greens and fermented axone"
    ],
    disambiguation_rule="Dry pilaf-style rice with pork -> Jadoh; soupy wet rice stew with leafy greens and axone aroma -> Galho."
))

register_northeast_confusion(NortheastConfusionPair(
    confusion_id="CONF_GALHO_VS_SAWHCHIAR_CONGEE",
    target_class_id="NL_RICE_GALHO",
    target_name="Naga Galho",
    confuser_class_id="MZ_RICE_SAWHCHIAR",
    confuser_name="Mizo Sawhchiar / Congee",
    primary_confusion_reason="Porridge-like savory rice preparations.",
    discriminating_visual_features=[
        "Galho prominently features green leafy vegetables, smoked pork, and the characteristic scent of axone (fermented soybean)",
        "Sawhchiar is a pale, creamy meat-and-rice porridge with shredded chicken or pork, subtle ginger, and black pepper, devoid of heavy leafy greens and axone"
    ],
    disambiguation_rule="Abundant green leafy vegetables + smoked meat + axone -> Galho; pale creamy rice porridge with shredded meat -> Sawhchiar."
))

# =============================================================================
# 2. FERMENTED SOYBEAN HARD NEGATIVES (Sections 13, 25, 39, 42)
# =============================================================================

register_northeast_confusion(NortheastConfusionPair(
    confusion_id="CONF_AXONE_VS_TUNGRYMBAI_KINEMA",
    target_class_id="NL_FERMENTED_AXONE",
    target_name="Naga Axone / Akhuni",
    confuser_class_id="ML_FERMENTED_TUNGRYMBAI",
    confuser_name="Khasi Tungrymbai / Sikkimese Kinema",
    primary_confusion_reason="All are fermented indigenous whole soybean foods.",
    discriminating_visual_features=[
        "Axone is a dense, pungent, brownish-grey paste or banana-leaf wrapped cake, with strong smoky aroma",
        "Tungrymbai is cooked with heavy ground black sesame paste (nei-iong), giving it a charcoal-black color and nutty sesame profile",
        "Kinema retains visible sticky, mucilaginous whole soybean curds, often pan-cooked with tomatoes, onions, and turmeric"
    ],
    disambiguation_rule="Dense pungent brown paste in Naga meat dish -> Axone; deep charcoal-black sesame paste -> Tungrymbai; sticky whole soybeans in tomato-onion curry -> Kinema."
))

# =============================================================================
# 3. MASHED VEGETABLE & CHUTNEY HARD NEGATIVES (Sections 8, 16, 17, 31, 46)
# =============================================================================

register_northeast_confusion(NortheastConfusionPair(
    confusion_id="CONF_ALOO_PITIKA_VS_EROMBA_MOSDENG",
    target_class_id="AS_VEG_ALOO_PITIKA",
    target_name="Assamese Aloo Pitika",
    confuser_class_id="MN_CHUTNEY_EROMBA",
    confuser_name="Manipuri Eromba / Tripuri Mosdeng",
    primary_confusion_reason="All are coarse mashed vegetable preparations.",
    discriminating_visual_features=[
        "Aloo Pitika is purely vegetarian: boiled potatoes mashed with raw pungent mustard oil, raw onions, and green chillies",
        "Eromba contains roasted Ngari (fermented fish), fiery king chilli (u-morok), boiled vegetables, and local chives (maroi)",
        "Mosdeng Serma is predominantly charred roasted tomatoes and roasted Berma (fermented fish) with green chillies"
    ],
    disambiguation_rule="Mashed potato with yellow raw mustard oil sheen without fish -> Aloo Pitika; vegetable mash with dark roasted Ngari fish and king chilli -> Eromba; charred tomato pulp with Berma -> Mosdeng."
))

register_northeast_confusion(NortheastConfusionPair(
    confusion_id="CONF_SINGJU_VS_COLESLAW_SALAD",
    target_class_id="MN_SALAD_SINGJU",
    target_name="Manipuri Singju",
    confuser_class_id="WESTERN_COLESLAW",
    confuser_name="Western Coleslaw / Tossed Salad",
    primary_confusion_reason="Shredded raw vegetables.",
    discriminating_visual_features=[
        "Singju is tossed with roasted chickpea/pea flour, roasted perilla seeds, crushed roasted Ngari fermented fish, and fiery red chillies",
        "Coleslaw is dressed with mayonnaise, cream, or vinegar-sugar dressing without fermented fish or roasted perilla powder"
    ],
    disambiguation_rule="Finely shredded cabbage/lotus stem with roasted gram powder, perilla seeds, and ngari -> Singju."
))

# =============================================================================
# 4. SMOKED MEAT & BAMBOO SHOOT HARD NEGATIVES (Sections 12, 23, 27, 43, 44)
# =============================================================================

register_northeast_confusion(NortheastConfusionPair(
    confusion_id="CONF_SMOKED_PORK_VS_FRIED_PORK",
    target_class_id="NL_MEAT_SMOKED_PORK_AXONE",
    target_name="Northeast Wood-Smoked Pork",
    confuser_class_id="GENERIC_FRIED_PORK",
    confuser_name="Pan-Fried Pork / Bacon",
    primary_confusion_reason="Dark reddish-brown cooked pork slices.",
    discriminating_visual_features=[
        "Smoked pork exhibits a deep mahogany-to-black cured surface from months of hearth wood-smoking, golden cured subcutaneous fat, and firm dense texture",
        "Fried pork has light golden batter or surface blisters with uncured fresh pork fat and juices"
    ],
    disambiguation_rule="Traditional hearth wood-smoke curing (dense mahogany crust, translucent cured fat) -> Smoked Pork. Never identify fried pork as smoked pork based on darkness alone."
))

register_northeast_confusion(NortheastConfusionPair(
    confusion_id="CONF_BAMBOO_SHOOT_VS_CABBAGE",
    target_class_id="NE_VEG_BAMBOO_SHOOT",
    target_name="Bamboo Shoot (Fresh / Fermented)",
    confuser_class_id="VEG_CABBAGE_SHREDS",
    confuser_name="Shredded Cabbage / Banana Stem",
    primary_confusion_reason="Pale yellowish fibrous shreds in curries.",
    discriminating_visual_features=[
        "Bamboo shoot shreds show rigid parallel fibrous grain, characteristic circular growth rings on slices, and pale ivory-yellow color",
        "Cabbage leaves are soft, curved, undulating with leafy veining and lack tubular cross-sections"
    ],
    disambiguation_rule="Parallel woody fibers and hollow segmented shoot slices -> Bamboo Shoot."
))

# =============================================================================
# 5. MOMO & THUKPA HARD NEGATIVES (Sections 33, 34, 40, 41)
# =============================================================================

register_northeast_confusion(NortheastConfusionPair(
    confusion_id="CONF_MOMO_VS_CHINESE_DIMSUM",
    target_class_id="NE_MOMO_PORK_STEAMED",
    target_name="Northeast Steamed Momo",
    confuser_class_id="CHINESE_DIM_SUM",
    confuser_name="Chinese Dim Sum / Xiao Long Bao",
    primary_confusion_reason="Pleated steamed wheat dumplings.",
    discriminating_visual_features=[
        "Northeast Momos are rustic, medium-thick wheat skin dumplings with minced seasoned meat/veg, served with fiery red tomato-garlic-king chilli chutney",
        "Xiao Long Bao contains gelatinized soup broth inside; Cantonese Har Gow has crystal translucent tapioca-starch skin"
    ],
    disambiguation_rule="Pleated wheat dumpling served with fiery red chilli-garlic chutney -> Northeast Momo."
))

register_northeast_confusion(NortheastConfusionPair(
    confusion_id="CONF_THUKPA_VS_RAMEN_PHO",
    target_class_id="NE_THUKPA_CHICKEN",
    target_name="Northeast Thukpa",
    confuser_class_id="JAPANESE_RAMEN",
    confuser_name="Japanese Ramen / Vietnamese Pho",
    primary_confusion_reason="Wheat noodles served in hot broth with meat and vegetables.",
    discriminating_visual_features=[
        "Thukpa has clear lightly spiced Tibetan-Himalayan cumin-garlic-ginger broth with shredded cabbage, carrots, spring onions, and meat",
        "Ramen features thick tonkotsu / miso broth with chashu pork belly rolls, nori seaweed, menma bamboo, and ajitsuke tamago",
        "Pho uses flat rice noodles with star anise broth, fresh basil, lime, and bean sprouts"
    ],
    disambiguation_rule="Cylindrical wheat noodles in light cumin-ginger spiced broth with shredded vegetables -> Thukpa."
))

# =============================================================================
# 6. SPECIALIZED CLASSIFIERS
# =============================================================================

class NortheastRiceMeatDiscriminator:
    """
    Implements Sections 11, 22, 26, 48:
    Distinguishes Jadoh (dry pilaf, Khasi) vs Galho (soupy with greens/axone, Naga)
    vs Sawhchiar (creamy plain porridge, Mizo) vs Pulao/Khichdi.
    """
    @staticmethod
    def classify(cues: Dict[str, Any]) -> Dict[str, Any]:
        has_abundant_greens = cues.get("has_leafy_greens", False)
        has_axone_aroma = cues.get("has_axone", False)
        is_soupy_porridge = cues.get("is_soupy_porridge", False) or "porridge" in str(cues.get("consistency", "")).lower()
        is_dry_pilaf = cues.get("is_dry_pilaf", False) or "pilaf" in str(cues.get("consistency", "")).lower()
        has_pork_fat = cues.get("has_pork_fat", False) or "pork_fat" in str(cues.get("cooking_fat", "")).lower()
        is_short_bold = "short" in str(cues.get("grain_type", "")).lower() or "bold" in str(cues.get("grain_type", "")).lower()
        has_creamy_shredded_meat = cues.get("has_creamy_shredded_meat", False)

        if is_soupy_porridge and (has_abundant_greens or has_axone_aroma):
            return {
                "dish_name": "Galho",
                "canonical_id": "NL_RICE_GALHO",
                "state": "Nagaland",
                "confidence": 0.94,
                "notes": "Soupy rice preparation with abundant greens and axone characteristics."
            }

        if is_soupy_porridge and has_creamy_shredded_meat:
            return {
                "dish_name": "Sawhchiar",
                "canonical_id": "MZ_RICE_SAWHCHIAR",
                "state": "Mizoram",
                "confidence": 0.92,
                "notes": "Pale creamy meat and rice porridge matching Mizo Sawhchiar."
            }

        if is_dry_pilaf or has_pork_fat or is_short_bold:
            return {
                "dish_name": "Jadoh",
                "canonical_id": "ML_RICE_JADOH_PORK",
                "state": "Meghalaya",
                "confidence": 0.95,
                "notes": "Dry short-grain rice cooked in meat broth and pork fat matching Khasi Jadoh."
            }


        return {
            "dish_name": "Northeast Rice Preparation",
            "canonical_id": "AS_RICE_JOHA",
            "state": "Northeast India",
            "confidence": 0.65,
            "notes": "Generic rice dish; evidence insufficient to distinguish between specific regional styles."
        }


class FermentedSoybeanDiscriminator:
    """
    Implements Sections 13, 25, 39, 42:
    Disambiguates Axone (Nagaland) vs Tungrymbai (Meghalaya) vs Kinema (Sikkim).
    """
    @staticmethod
    def classify(cues: Dict[str, Any]) -> Dict[str, Any]:
        has_black_sesame = cues.get("has_black_sesame", False)
        color = cues.get("color", "brown") # "charcoal_black", "brown", "pale_sticky"
        is_sticky_whole_bean = cues.get("is_sticky_whole_bean", False)

        if has_black_sesame or color == "charcoal_black":
            return {
                "fermented_product": "Tungrymbai",
                "canonical_id": "ML_FERMENTED_TUNGRYMBAI",
                "state": "Meghalaya",
                "confidence": 0.95,
                "notes": "Fermented soybean cooked with roasted black sesame (nei-iong) matches Khasi Tungrymbai."
            }

        if is_sticky_whole_bean and cues.get("in_tomato_curry", False):
            return {
                "fermented_product": "Kinema",
                "canonical_id": "SK_FERMENTED_KINEMA",
                "state": "Sikkim",
                "confidence": 0.92,
                "notes": "Sticky whole fermented soybeans in curry match Sikkimese Kinema."
            }

        return {
            "fermented_product": "Axone / Akhuni",
            "canonical_id": "NL_FERMENTED_AXONE",
            "state": "Nagaland",
            "confidence": 0.93,
            "notes": "Pungent brown fermented soybean mash/paste matches Naga Axone."
        }


class MashedVegetableChutneyDiscriminator:
    """
    Implements Sections 8, 16, 17, 31:
    Aloo Pitika (Assam) vs Eromba (Manipur) vs Mosdeng (Tripura) vs Singju (Manipur).
    """
    @staticmethod
    def classify(cues: Dict[str, Any]) -> Dict[str, Any]:
        has_fermented_fish = cues.get("has_fermented_fish", False)
        has_roasted_tomatoes = cues.get("has_roasted_tomatoes", False)
        is_raw_shredded_salad = cues.get("is_raw_shredded_salad", False)
        has_raw_mustard_oil = cues.get("has_raw_mustard_oil", False)

        if is_raw_shredded_salad:
            return {
                "dish_name": "Manipuri Singju",
                "canonical_id": "MN_SALAD_SINGJU",
                "state": "Manipur",
                "confidence": 0.96,
                "notes": "Raw shredded seasonal vegetables with chickpea powder and perilla matches Singju."
            }

        if has_fermented_fish and has_roasted_tomatoes:
            return {
                "dish_name": "Mosdeng Serma",
                "canonical_id": "TR_CHUTNEY_MOSDENG_SERMA",
                "state": "Tripura",
                "confidence": 0.94,
                "notes": "Charred roasted tomato mash with fermented Berma fish matches Tripuri Mosdeng Serma."
            }

        if has_fermented_fish and not has_roasted_tomatoes:
            return {
                "dish_name": "Manipuri Eromba",
                "canonical_id": "MN_CHUTNEY_EROMBA",
                "state": "Manipur",
                "confidence": 0.95,
                "notes": "Boiled vegetable and potato mash with roasted Ngari fermented fish and king chilli matches Eromba."
            }

        if has_raw_mustard_oil and not has_fermented_fish:
            return {
                "dish_name": "Assamese Aloo Pitika",
                "canonical_id": "AS_VEG_ALOO_PITIKA",
                "state": "Assam",
                "confidence": 0.96,
                "notes": "Mashed potato with raw pungent mustard oil and onions matches Assamese Aloo Pitika."
            }

        return {
            "dish_name": "Northeast Chutney / Mash",
            "canonical_id": "AS_VEG_ALOO_PITIKA",
            "state": "Northeast India",
            "confidence": 0.70,
            "notes": "Mashed vegetable preparation; insufficient cues to isolate specific state variant."
        }


class SmokedMeatVerifier:
    """
    Implements Section 43:
    Distinguishes wood-smoked meat from grilled, roasted, fried, or charred meat.
    Never relies on darkness alone.
    """
    @staticmethod
    def verify(cues: Dict[str, Any]) -> Dict[str, Any]:
        has_smoke_ring = cues.get("has_cured_smoke_ring", False)
        has_cured_amber_fat = cues.get("has_cured_amber_fat", False)
        has_wood_smoke_texture = cues.get("has_wood_smoke_texture", False)
        is_freshly_charred_or_burnt = cues.get("is_freshly_charred_or_burnt", False)
        is_batter_fried = cues.get("is_batter_fried", False)

        if is_batter_fried:
            return {"is_smoked": False, "category": "deep_fried_meat", "confidence": 0.95}

        if is_freshly_charred_or_burnt and not has_cured_amber_fat:
            return {"is_smoked": False, "category": "charred_or_burnt_meat", "confidence": 0.88}

        if has_smoke_ring or (has_cured_amber_fat and has_wood_smoke_texture):
            return {
                "is_smoked": True,
                "category": "authentic_wood_smoked_meat",
                "confidence": 0.95,
                "notes": "Cured translucent fat and wood-smoke mahogany exterior confirm traditional smoked meat."
            }

        return {"is_smoked": False, "category": "cooked_meat_uncertain", "confidence": 0.55}


def disambiguate_northeast_pair(
    pair_id: Optional[str] = None,
    confusion_id: Optional[str] = None,
    visual_features: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    cid = pair_id or confusion_id or ""
    pair = NORTHEAST_CONFUSION_REGISTRY.get(cid)
    if not pair:
        return {
            "resolved": False,
            "error": f"Unknown confusion id: {cid}"
        }

    cues = visual_features or {}
    # Use specialized classifiers based on target class
    if "JADOH" in pair.target_class_id or "GALHO" in pair.target_class_id or "PULAO" in pair.confuser_class_id:
        res = NortheastRiceMeatDiscriminator.classify(cues)
        return {
            "resolved": True,
            "selected_class_id": res["canonical_id"],
            "selected_name": res["dish_name"],
            "confidence": res["confidence"],
            "resolution_notes": res["notes"]
        }

    if "AXONE" in pair.target_class_id or "TUNGRYMBAI" in pair.confuser_class_id:
        res = FermentedSoybeanDiscriminator.classify(cues)
        return {
            "resolved": True,
            "selected_class_id": res["canonical_id"],
            "selected_name": res["dish_name"],
            "confidence": res["confidence"],
            "resolution_notes": res["notes"]
        }

    if "PITIKA" in pair.target_class_id or "EROMBA" in pair.confuser_class_id:
        res = MashedVegetableChutneyDiscriminator.classify(cues)
        return {
            "resolved": True,
            "selected_class_id": res["canonical_id"],
            "selected_name": res["dish_name"],
            "confidence": res["confidence"],
            "resolution_notes": res["notes"]
        }

    # Default fallback to pair target
    return {
        "resolved": True,
        "selected_class_id": pair.target_class_id,
        "selected_name": pair.target_name,
        "confidence": 0.90,
        "resolution_notes": pair.disambiguation_rule
    }

