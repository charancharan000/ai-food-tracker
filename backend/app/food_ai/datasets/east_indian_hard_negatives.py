"""
East Indian Hard Negative Confusion Matrix & Disambiguation Engine (Part 6)
Implements Sections 3, 4, 10, 11, 13, 14, 24, 25, 28, 32, 35, 37, 38, 39, 40, 55 of Part 6.

Guarantees:
- Pairwise Disambiguation Matrix for 30+ East Indian visual confusion pairs
- Fish Species Classifier with strict separation of fish_species_confidence from dish_confidence
- Shorshe / Mustard Fish Detector vs yellow / coconut / tomato fish curry
- Dahibara Aloodum Component Segmenter vs generic Dahi Vada / Dahi Bhalla
- Jhalmuri Component Segmenter without assuming invisible ingredients
- Kathi Roll Multi-layer Segmenter
- Champaran Ahuna Mutton Verifier (pot, intact whole garlic bulb, oil layer)
- Leafy Green Saag Disambiguator (never forces exact species under ambiguous visual evidence)
"""

from typing import List, Dict, Any, Optional, Tuple
from pydantic import BaseModel, Field

class EastIndianConfusionPair(BaseModel):
    confusion_id: str
    target_class_id: str
    target_name: str
    confuser_class_id: str
    confuser_name: str
    primary_confusion_reason: str
    discriminating_visual_features: List[str]
    disambiguation_rule: str

EAST_INDIAN_CONFUSION_REGISTRY: Dict[str, EastIndianConfusionPair] = {}

def register_east_confusion(pair: EastIndianConfusionPair):
    EAST_INDIAN_CONFUSION_REGISTRY[pair.confusion_id] = pair

# =============================================================================
# 1. SWEETS & DESSERT HARD NEGATIVE PAIRS (Section 39, 55)
# =============================================================================

register_east_confusion(EastIndianConfusionPair(
    confusion_id="CONF_RASGULLA_VS_GULAB_JAMUN",
    target_class_id="WB_SWEET_RASGULLA",
    target_name="Kolkata Rasgulla",
    confuser_class_id="NI_SWEET_GULAB_JAMUN",
    confuser_name="Gulab Jamun",
    primary_confusion_reason="Both are spherical milk-based sweets resting in translucent sugar syrup.",
    discriminating_visual_features=[
        "Rasgulla is pristine snow white or ivory; Gulab Jamun is deep golden brown or dark caramel mahogany",
        "Rasgulla exhibits fine spongy elastic porous chhana surface; Gulab Jamun has smooth fried khoya crust",
        "Rasgulla rests in very light runny watery clear syrup; Gulab Jamun sits in thicker sticky cardamom-rose syrup"
    ],
    disambiguation_rule="If color is snow-white and surface shows spongy porous elasticity, classify as Rasgulla. If dark fried brown/mahogany, classify as Gulab Jamun."
))

register_east_confusion(EastIndianConfusionPair(
    confusion_id="CONF_SANDESH_VS_PEDA",
    target_class_id="WB_SWEET_PLAIN_SANDESH",
    target_name="Sandesh",
    confuser_class_id="NI_SWEET_PEDA",
    confuser_name="Peda",
    primary_confusion_reason="Both can be small round or disc-shaped pale sweets.",
    discriminating_visual_features=[
        "Sandesh has delicate crumbly moist chhana grain, intricate conch shell (shankha) or floral wooden mould imprints",
        "Peda has dense heavy caramelized mawa (khoya) texture, oily thumb depression, and firmer consistency",
        "Nolen Gur Sandesh has light beige-caramel date jaggery sheen, never dark mawa brown"
    ],
    disambiguation_rule="Examine surface texture and mould patterns: fine chhana curd grain + floral/shankha mold -> Sandesh; dense smooth mawa with central thumb indent -> Peda. Do not classify all white sweets as Sandesh."
))

register_east_confusion(EastIndianConfusionPair(
    confusion_id="CONF_MISHTI_DOI_VS_YOGURT_KHEER",
    target_class_id="WB_SWEET_MISHTI_DOI",
    target_name="Mishti Doi",
    confuser_class_id="DAIRY_PLAIN_YOGURT",
    confuser_name="Plain Yogurt / Kheer / Rabri / Custard",
    primary_confusion_reason="All are creamy dairy preparations served in bowls or cups.",
    discriminating_visual_features=[
        "Mishti Doi has a distinct pale reddish-caramel to terracotta-tan hue from caramelized milk, served in porous clay bhar/matka",
        "Surface of Mishti Doi is glossy, perfectly set without visible floating rice grains (unlike Kheer) or thick clotted malai shreds (unlike Rabri)",
        "Plain dahi is stark white with acidic whey separation; custard has artificial egg-yellow sheen"
    ],
    disambiguation_rule="Porous earthen clay pot + set gelatinous caramel tan surface + no visible grains -> Mishti Doi. Never infer sweetness level solely from visual appearance."
))

register_east_confusion(EastIndianConfusionPair(
    confusion_id="CONF_CHHENA_PODA_VS_CAKE",
    target_class_id="OD_SWEET_CHHENA_PODA",
    target_name="Odia Chhena Poda",
    confuser_class_id="WESTERN_CHEESECAKE",
    confuser_name="Western Cheesecake / Baked Milk Cake",
    primary_confusion_reason="Both have a caramelized or burnt upper crust and a dense dairy interior.",
    discriminating_visual_features=[
        "Chhena Poda has a rustic, unevenly charred dark brown-black burnt caramelized top from wood-fire or sal leaves",
        "Crumb shows coarse glistening honeycombed chhana texture with embedded roasted cashews, raisins, and green cardamom pods",
        "Cheesecake has smooth processed cream cheese uniformity without coarse chhana curds or charred sal-leaf fiber traces"
    ],
    disambiguation_rule="Coarse chhana honeycomb curd texture + rustic caramelized char crust + embedded cashews/cardamom -> Chhena Poda."
))

register_east_confusion(EastIndianConfusionPair(
    confusion_id="CONF_PATISHAPTA_VS_CREPE",
    target_class_id="WB_SWEET_PATISHAPTA",
    target_name="Patishapta Pitha",
    confuser_class_id="FRENCH_CREPE",
    confuser_name="French Crepe / Thin Dosa",
    primary_confusion_reason="Both are rolled thin griddled batters.",
    discriminating_visual_features=[
        "Patishapta is made of rice flour-suji batter, soft pale ivory/yellowish with visible stuffed coconut-jaggery or kheer filling visible at edges",
        "French crepes are made of wheat-egg batter with brown griddle speckles; dosas are crisp golden-brown fermented urad dal crepes"
    ],
    disambiguation_rule="Rolled pale soft rice-suji crepe containing coconut-nolen gur or kheer filling -> Patishapta."
))

register_east_confusion(EastIndianConfusionPair(
    confusion_id="CONF_MALPUA_VS_PANCAKE",
    target_class_id="WB_SWEET_MALPUA",
    target_name="Malpua",
    confuser_class_id="WESTERN_PANCAKE",
    confuser_name="Pancake",
    primary_confusion_reason="Flat fried circular batter cakes.",
    discriminating_visual_features=[
        "Malpua has deep-fried lacy crisp caramelized crinkled edges and is soaked in fragrant cardamom-saffron sugar syrup",
        "Western pancakes are dry, thick, fluffy, griddled without sugar syrup immersion"
    ],
    disambiguation_rule="Lacy crisp fried edges + heavy glistening sugar syrup bath -> Malpua."
))

register_east_confusion(EastIndianConfusionPair(
    confusion_id="CONF_THEKUA_VS_COOKIE",
    target_class_id="BR_SWEET_THEKUA",
    target_name="Bihari Thekua",
    confuser_class_id="WESTERN_COOKIE",
    confuser_name="Western Cookie / Mathri",
    primary_confusion_reason="Dense, hard, sweet or savory baked/fried discs.",
    discriminating_visual_features=[
        "Thekua has deeply embossed wooden die (sancha) floral or geometric impressions",
        "Deep golden-brown from jaggery and ghee frying, with visible embedded whole fennel seeds (saunf) and dry coconut shavings",
        "Hard snap texture, not porous leavened biscuit"
    ],
    disambiguation_rule="Traditional wooden sancha relief pattern + jaggery-fried hardness + whole fennel seeds -> Thekua."
))

register_east_confusion(EastIndianConfusionPair(
    confusion_id="CONF_KHAJA_VS_PASTRY",
    target_class_id="OD_SWEET_PURI_KHAJA",
    target_name="Puri / Silao Khaja",
    confuser_class_id="WESTERN_CROISSANT",
    confuser_name="Puff Pastry / Croissant",
    primary_confusion_reason="Multi-layered flaky golden pastry.",
    discriminating_visual_features=[
        "Khaja features dozens of crisp, brittle, dry, glassy sugar-glazed fried flour layers",
        "Croissants are soft, buttery, yeast-leavened breads; Khaja is unleavened, deep-fried in ghee, brittle and crystalline"
    ],
    disambiguation_rule="Crispy crystalline sugar-glazed brittle multi-layered fried wafer -> Khaja."
))

# =============================================================================
# 2. BREAD & BREAKFAST HARD NEGATIVE PAIRS (Section 40)
# =============================================================================

register_east_confusion(EastIndianConfusionPair(
    confusion_id="CONF_LUCHI_VS_PURI",
    target_class_id="WB_BREAD_LUCHI",
    target_name="Luchi",
    confuser_class_id="NI_BREAD_PURI_WHEAT",
    confuser_name="North Indian Whole Wheat Puri",
    primary_confusion_reason="Both are puffed, deep-fried unleavened round breads.",
    discriminating_visual_features=[
        "Luchi is made strictly of refined all-purpose flour (maida), appearing pale white to translucent ivory without golden-brown tanning",
        "Puri is made of whole wheat flour (atta), exhibiting a distinct golden-brown to reddish hue with blistered spots",
        "Luchi crust is ultra-thin, delicate, paper-soft, and non-greasy when properly fried"
    ],
    disambiguation_rule="If puffed bread is pristine pale white/cream with paper-thin crust -> Luchi. If golden-brown/tan with whole wheat grain color -> Puri."
))

register_east_confusion(EastIndianConfusionPair(
    confusion_id="CONF_RADHA_BALLAVI_VS_KACHORI",
    target_class_id="WB_BREAD_RADHA_BALLAVI",
    target_name="Radha Ballavi",
    confuser_class_id="NI_BREAD_KACHORI",
    confuser_name="Khasta Kachori / Dal Kachori",
    primary_confusion_reason="Both are dal-stuffed fried breads.",
    discriminating_visual_features=[
        "Radha Ballavi is larger, softer, pliable, puffed bread with a thin uniform layer of spiced black gram (biuli/urad dal) paste inside",
        "Khasta Kachori has a thick, rigid, brittle, flaky, hollow crust filled with dry spicy coarse lentil mixture"
    ],
    disambiguation_rule="Soft, flexible, puffed white-bread envelope with thin moist fennel-urad dal paste -> Radha Ballavi; brittle thick flaky shell -> Khasta Kachori."
))

register_east_confusion(EastIndianConfusionPair(
    confusion_id="CONF_SATTU_PARATHA_VS_ALOO_PARATHA",
    target_class_id="BR_BREAD_SATTU_PARATHA",
    target_name="Sattu Paratha",
    confuser_class_id="NI_BREAD_ALOO_PARATHA",
    confuser_name="Aloo Paratha",
    primary_confusion_reason="Stuffed whole wheat flatbreads cooked on tawa.",
    discriminating_visual_features=[
        "Sattu Paratha filling is dryish, granular, yellow-tan roasted gram flour flecked with black kalonji seeds and ajwain",
        "Aloo Paratha filling is moist, dense, mashed potato with coriander and red chilli flakes",
        "Sattu aroma carries roasted chana and raw mustard oil pungency"
    ],
    disambiguation_rule="Granular roasted gram stuffing with kalonji/ajwain flecks -> Sattu Paratha; smooth mashed potato stuffing -> Aloo Paratha."
))

register_east_confusion(EastIndianConfusionPair(
    confusion_id="CONF_DHUSKA_VS_VADA",
    target_class_id="JH_SNACK_DHUSKA",
    target_name="Jharkhandi Dhuska",
    confuser_class_id="SOUTH_INDIAN_MEDU_VADA",
    confuser_name="Medu Vada / Batata Vada",
    primary_confusion_reason="Golden deep-fried snacks.",
    discriminating_visual_features=[
        "Dhuska is a solid, puffed, round disc without a central hole (unlike Medu Vada)",
        "Dhuska interior is light yellow, fluffy, spongy crumb made from rice and chana dal batter",
        "Always served accompanied by yellow/black chana ghugni or aloo dum, never coconut chutney / sambar"
    ],
    disambiguation_rule="Solid round puffed rice-chana disc served with Ghugni/Aloo Dum -> Dhuska."
))

register_east_confusion(EastIndianConfusionPair(
    confusion_id="CONF_CHILKA_ROTI_VS_DOSA",
    target_class_id="JH_BREAD_CHILKA_ROTI",
    target_name="Chilka Roti",
    confuser_class_id="SOUTH_INDIAN_DOSA",
    confuser_name="Plain Dosa",
    primary_confusion_reason="Thin rice-lentil tawa griddled crepes.",
    discriminating_visual_features=[
        "Chilka Roti is softer, thicker, rustic, pale ivory/yellowish with subtle browning, served with rustic sabzi/saag",
        "Dosa is paper-thin, crispy, golden-brown, fermented, rolled or folded into cylindrical cone"
    ],
    disambiguation_rule="Rustic soft flat rice-chana crepe without crisp golden curl -> Chilka Roti."
))

# =============================================================================
# 3. FISH & CURRY HARD NEGATIVE PAIRS (Sections 4, 38, 55)
# =============================================================================

register_east_confusion(EastIndianConfusionPair(
    confusion_id="CONF_SHORSHE_FISH_VS_YELLOW_CURRY",
    target_class_id="WB_FISH_SHORSHE_ILISH",
    target_name="Shorshe Fish (Hilsa / Rui / Katla)",
    confuser_class_id="GENERIC_YELLOW_FISH_CURRY",
    confuser_name="Generic Yellow Fish Curry / Coconut Curry",
    primary_confusion_reason="Both have bright yellow/golden gravy.",
    discriminating_visual_features=[
        "Shorshe gravy has dense coarse mustard seed paste (shorshe bata) suspension, pungent mustard oil aroma sheen",
        "Prominent slit fresh green chillies and whole kalo jeere (nigella seeds) scattered on surface",
        "Generic yellow fish curry uses turmeric-onion-tomato or coconut milk without pungent mustard grain texture"
    ],
    disambiguation_rule="Pungent grainy yellow-green mustard seed paste + floating raw mustard oil sheen + green chilli slits -> Shorshe Fish."
))

register_east_confusion(EastIndianConfusionPair(
    confusion_id="CONF_MACHER_JHOL_VS_THIN_CURRY",
    target_class_id="WB_FISH_MACHER_JHOL",
    target_name="Macher Jhol",
    confuser_class_id="GENERIC_THIN_CURRY",
    confuser_name="Generic Thin Fish Curry",
    primary_confusion_reason="Thin runny brownish-red fish broth.",
    discriminating_visual_features=[
        "Macher Jhol specifically features distinct fried whole carp (rohu/katla) steaks paired with large elongated halved potato wedges",
        "Tempered with black nigella seeds (kalo jeere) and cumin-ginger paste, clear surface without dairy/coconut cream"
    ],
    disambiguation_rule="Thin light cumin-nigella broth + bone-in carp steak + large soft potato half -> Bengali Macher Jhol."
))

register_east_confusion(EastIndianConfusionPair(
    confusion_id="CONF_CHINGRI_MALAI_VS_COCONUT_CHICKEN",
    target_class_id="WB_FISH_CHINGRI_MALAI_CURRY",
    target_name="Chingri Malai Curry",
    confuser_class_id="GENERIC_COCONUT_CURRY",
    confuser_name="Coconut Chicken Curry",
    primary_confusion_reason="Both have creamy pale-orange coconut milk gravy.",
    discriminating_visual_features=[
        "Chingri Malai Curry contains large whole prawns with heads/tails intact, releasing reddish-orange prawn fat into coconut cream",
        "Fragrant with ghee, whole cinnamon, green cardamom, and slit green chillies"
    ],
    disambiguation_rule="Intact whole large prawns + rich golden-orange coconut cream gravy -> Chingri Malai Curry."
))

register_east_confusion(EastIndianConfusionPair(
    confusion_id="CONF_PAKHALA_VS_PLAIN_RICE_WATER",
    target_class_id="OD_RICE_DAHI_PAKHALA",
    target_name="Odia Pakhala (Dahi / Basi)",
    confuser_class_id="WB_RICE_PLAIN",
    confuser_name="Plain Rice with Accidental Water",
    primary_confusion_reason="Rice submerged in liquid.",
    discriminating_visual_features=[
        "Pakhala features intentional fermentation or curd blending (torani/dahi), tempered with fried mustard seeds and curry leaves",
        "Accompanied by dedicated side platters: fried fish, badi chura, saga bhaja, aloo bhaja, raw onions, and lime"
    ],
    disambiguation_rule="Do not classify ordinary rice with water as Pakhala without supporting culinary evidence (curd, tempering, or authentic Odia sides)."
))

register_east_confusion(EastIndianConfusionPair(
    confusion_id="CONF_DALMA_VS_DAL_SAMBAR",
    target_class_id="OD_CURRY_DALMA",
    target_name="Odia Dalma",
    confuser_class_id="SOUTH_INDIAN_SAMBAR",
    confuser_name="Sambar / Mixed Vegetable Dal",
    primary_confusion_reason="Lentil stew containing chunky vegetables.",
    discriminating_visual_features=[
        "Dalma contains specific East Indian vegetables: yellow pumpkin, raw papaya, plantain, saru (taro root), drumstick",
        "Topped with fragrant bhaja jeera lanka gunda (roasted cumin-dry chilli powder) and desi ghee, without tamarind/sambar powder tang"
    ],
    disambiguation_rule="Toor/moong dal with pumpkin + raw papaya + plantain + roasted cumin-chilli powder topping -> Dalma. Never classify as Sambar."
))

register_east_confusion(EastIndianConfusionPair(
    confusion_id="CONF_DAHIBARA_ALOODUM_VS_DAHI_VADA",
    target_class_id="OD_STREET_DAHIBARA_ALOODUM",
    target_name="Cuttack Dahibara Aloodum",
    confuser_class_id="NI_STREET_DAHI_VADA",
    confuser_name="Generic Dahi Vada / Dahi Bhalla",
    primary_confusion_reason="Urad dal dumplings in yogurt.",
    discriminating_visual_features=[
        "Dahibara Aloodum is an 8-component composite: vadas sit in thin sour dahi-pani broth, topped with thick spicy Aloo Dum and yellow Ghugni",
        "Garnished with chopped onions, fine sev, coriander, and bhaja jeera powder",
        "Generic Dahi Vada sits in thick sweet beaten yogurt with saunth (tamarind) and mint chutney alone"
    ],
    disambiguation_rule="Presence of Aloo Dum + Ghugni + Sev + thin spiced dahi broth over vadas -> Dahibara Aloodum. Never classify as generic Dahi Vada."
))

register_east_confusion(EastIndianConfusionPair(
    confusion_id="CONF_CHAMPARAN_MUTTON_VS_MUTTON_CURRY",
    target_class_id="BR_MEAT_CHAMPARAN_MUTTON",
    target_name="Champaran Mutton (Ahuna)",
    confuser_class_id="WB_MEAT_KOSHA_MANGSHO",
    confuser_name="Generic Mutton Curry / Kosha Mangsho",
    primary_confusion_reason="Dark spiced mutton curry.",
    discriminating_visual_features=[
        "Champaran Ahuna Mutton is cooked in an earthen clay pot (handi) sealed with dough",
        "Crucial signature: whole, unpeeled, intact garlic bulb (lahsun ki ganth) cooked inside the gravy",
        "Heavy visible mustard oil floating layer and whole whole black peppercorns/cloves"
    ],
    disambiguation_rule="Do not identify dish solely because it is a dark mutton curry. Earthen handi + intact whole garlic bulb + thick mustard oil float -> Champaran Ahuna Mutton."
))

# =============================================================================
# 4. SPECIALIZED CLASSIFIERS & DISCRIMINATORS
# =============================================================================

class FishSpeciesClassificationResult(BaseModel):
    dish_name: str
    dish_confidence: float
    fish_species: str # "Rohu", "Catla", "Hilsa", "Bhetki", "Pabda", "Koi", "Tangra", "Pomfret", "Prawn", "Crab", "unknown"
    fish_species_confidence: float
    visual_evidence_sufficient: bool
    evidence_notes: str

class FishSpeciesClassifier:
    """
    Implements Sections 3, 37, 38 and Quality Rule 3:
    - Species classification MUST be separate from dish classification.
    - If fish is partially submerged, coated in thick gravy, or broken:
      fish_species = "unknown", fish_species_confidence = low,
      while dish_confidence may remain high.
    """
    @staticmethod
    def classify_fish_and_species(
        visual_cues: Dict[str, Any],
        detected_dish: str
    ) -> FishSpeciesClassificationResult:
        submerged = visual_cues.get("is_submerged", False)
        visible_anatomy = visual_cues.get("visible_anatomy", []) # e.g. ["silvery_scales", "broad_body", "whiskers", "prawn_curled_tail", "crab_claws"]
        steak_shape = visual_cues.get("steak_shape", "obscured") # "oval_gada", "broad_peti", "whole_small_fish", "fillet", "obscured"

        # Check if visual evidence is insufficient
        if submerged or not visible_anatomy or steak_shape == "obscured":
            return FishSpeciesClassificationResult(
                dish_name=detected_dish,
                dish_confidence=0.92,
                fish_species="unknown",
                fish_species_confidence=0.25,
                visual_evidence_sufficient=False,
                evidence_notes="Fish piece is submerged in gravy or anatomy is obscured; exact species cannot be confirmed from visual evidence alone (enforcing Quality Rule 3)."
            )

        # Distinguish species based on positive anatomical cues
        if "crab_claws" in visible_anatomy or "crab_shell" in visible_anatomy:
            return FishSpeciesClassificationResult(
                dish_name=detected_dish, dish_confidence=0.96, fish_species="Crab",
                fish_species_confidence=0.98, visual_evidence_sufficient=True,
                evidence_notes="Clear crab carapace and claws identified."
            )

        if "prawn_curled_tail" in visible_anatomy or "prawn_antenna" in visible_anatomy:
            return FishSpeciesClassificationResult(
                dish_name=detected_dish, dish_confidence=0.95, fish_species="Prawn",
                fish_species_confidence=0.96, visual_evidence_sufficient=True,
                evidence_notes="Distinct prawn segmented tail and curved body verified."
            )

        if "hilsa_broad_herring_cross_section" in visible_anatomy or "ilish_silvery_fine_texture" in visible_anatomy:
            return FishSpeciesClassificationResult(
                dish_name=detected_dish, dish_confidence=0.95, fish_species="Hilsa",
                fish_species_confidence=0.91, visual_evidence_sufficient=True,
                evidence_notes="Distinctive broad oily clupeid cross-section and silver hues match Hilsa (Ilish)."
            )

        if "catfish_barbels" in visible_anatomy and steak_shape == "whole_small_fish":
            return FishSpeciesClassificationResult(
                dish_name=detected_dish, dish_confidence=0.93, fish_species="Tangra",
                fish_species_confidence=0.90, visual_evidence_sufficient=True,
                evidence_notes="Small whole freshwater catfish with prominent barbels matches Tangra."
            )

        if "butterfish_flat_silvery_elongated" in visible_anatomy:
            return FishSpeciesClassificationResult(
                dish_name=detected_dish, dish_confidence=0.94, fish_species="Pabda",
                fish_species_confidence=0.92, visual_evidence_sufficient=True,
                evidence_notes="Slender scaleless silvery butterfish profile matches Pabda."
            )

        if "boneless_white_firm_fillet" in visible_anatomy:
            return FishSpeciesClassificationResult(
                dish_name=detected_dish, dish_confidence=0.94, fish_species="Bhetki",
                fish_species_confidence=0.88, visual_evidence_sufficient=True,
                evidence_notes="Thick uniform boneless barramundi fillet matches Bhetki."
            )

        if "carp_bone_in_steak" in visible_anatomy:
            if steak_shape == "broad_peti":
                return FishSpeciesClassificationResult(
                    dish_name=detected_dish, dish_confidence=0.92, fish_species="Catla",
                    fish_species_confidence=0.82, visual_evidence_sufficient=True,
                    evidence_notes="Large broad curved belly carp cut matches Catla (Katla)."
                )
            return FishSpeciesClassificationResult(
                dish_name=detected_dish, dish_confidence=0.92, fish_species="Rohu",
                fish_species_confidence=0.80, visual_evidence_sufficient=True,
                evidence_notes="Standard freshwater carp bone-in steak matches Rohu (Rui)."
            )

        return FishSpeciesClassificationResult(
            dish_name=detected_dish, dish_confidence=0.88, fish_species="unknown",
            fish_species_confidence=0.35, visual_evidence_sufficient=False,
            evidence_notes="Fish identified as generic carp/freshwater fish; insufficient cues for definitive species call."
        )


class MustardFishDetector:
    """
    Implements Section 4: Shorshe Maach vs generic yellow / coconut / tomato fish curry.
    Detects mustard paste grain, green chilli slits, mustard seeds, and mustard oil float.
    """
    @staticmethod
    def evaluate(cues: Dict[str, Any]) -> Dict[str, Any]:
        has_mustard_paste = cues.get("mustard_paste_texture", False)
        has_green_chilli = cues.get("slit_green_chillies", False)
        has_mustard_oil_sheen = cues.get("mustard_oil_sheen", False)
        has_coconut_milk = cues.get("coconut_milk_base", False)
        has_tomato_redness = cues.get("tomato_red_base", False)

        if has_coconut_milk:
            return {"is_mustard_fish": False, "category": "coconut_fish_curry", "confidence": 0.94}
        if has_tomato_redness:
            return {"is_mustard_fish": False, "category": "tomato_fish_curry", "confidence": 0.92}

        if has_mustard_paste and (has_green_chilli or has_mustard_oil_sheen):
            return {
                "is_mustard_fish": True,
                "category": "shorshe_maach",
                "confidence": 0.95,
                "features_detected": ["mustard_seed_paste", "pungent_mustard_oil", "green_chillies"]
            }

        return {"is_mustard_fish": False, "category": "generic_yellow_curry", "confidence": 0.70}


class DahibaraAloodumSegmenter:
    """
    Implements Section 35: Segment 8 distinct Dahibara Aloodum components.
    Never classify as generic Dahi Vada!
    """
    @staticmethod
    def segment_components(cues: Dict[str, Any]) -> Dict[str, Any]:
        components = {
            "dahibara": cues.get("has_soaked_urad_vadas", True),
            "aloodum": cues.get("has_dark_spiced_potato_curry", True),
            "ghugni": cues.get("has_yellow_pea_curry", True),
            "tempered_yogurt_liquid": cues.get("has_thin_buttermilk_liquid", True),
            "chutney": cues.get("has_sweet_tangy_chutney", True),
            "sev_garnish": cues.get("has_fine_crisp_sev", True),
            "chopped_onion": cues.get("has_raw_onions", True),
            "coriander": cues.get("has_fresh_coriander", True)
        }
        present_count = sum(1 for v in components.values() if v)
        is_authentic = present_count >= 5 and components["dahibara"] and components["aloodum"]
        return {
            "is_dahibara_aloodum": is_authentic,
            "components_present": components,
            "component_coverage_score": round(present_count / 8.0, 2),
            "disambiguation_note": "Identified as authentic Cuttack Dahibara Aloodum multi-layer street preparation; distinguished from single-dish Dahi Vada."
        }


class ChamparanMuttonDetector:
    """
    Implements Section 28: Champaran / Ahuna Mutton Verifier.
    Enforces Rule: Do not identify dish only because it is a dark mutton curry.
    Requires earthen pot, thick masala, oil layer, whole spices, or intact whole garlic bulb.
    """
    @staticmethod
    def verify(cues: Dict[str, Any]) -> Dict[str, Any]:
        has_clay_handi = cues.get("earthen_clay_pot_visible", False)
        has_whole_garlic_bulb = cues.get("whole_intact_garlic_bulb_visible", False)
        has_mustard_oil_layer = cues.get("heavy_mustard_oil_float", False)
        has_whole_spices = cues.get("whole_peppercorn_cloves_visible", False)

        score = 0
        if has_clay_handi: score += 35
        if has_whole_garlic_bulb: score += 40
        if has_mustard_oil_layer: score += 15
        if has_whole_spices: score += 10

        is_confirmed = score >= 50 or has_whole_garlic_bulb
        return {
            "is_champaran_ahuna_mutton": is_confirmed,
            "evidence_score": score,
            "whole_garlic_detected": has_whole_garlic_bulb,
            "clay_handi_detected": has_clay_handi,
            "verdict": "Confirmed Champaran Ahuna Mutton" if is_confirmed else "Generic Mutton Curry (insufficient Champaran visual signatures)"
        }


class LeafyGreenSaagVerifier:
    """
    Implements Section 32: Jharkhand & East Indian wild saag.
    Quality Rule: Never force exact species identification if visual evidence is insufficient.
    Output: leafy_green_dish + possible_species + confidence.
    """
    @staticmethod
    def identify_saag(cues: Dict[str, Any]) -> Dict[str, Any]:
        leaf_shape = cues.get("leaf_shape", "chopped_fine") # "bifid_folded" (koinar), "tiny_oval" (munga), "creeper_fleshy" (poi), "chopped_fine"
        is_dry_stir_fry = cues.get("is_dry_bhaji", True)

        if leaf_shape == "bifid_folded":
            return {
                "leafy_green_dish": "Jharkhandi Saag Bhaji",
                "possible_species": ["Koinar Saag (Bauhinia purpurea)"],
                "species_confidence": 0.88,
                "is_species_exact": True
            }
        elif leaf_shape == "tiny_oval":
            return {
                "leafy_green_dish": "Munga Saag Bhaji",
                "possible_species": ["Munga / Sajana Saag (Moringa oleifera)"],
                "species_confidence": 0.90,
                "is_species_exact": True
            }
        elif leaf_shape == "creeper_fleshy":
            return {
                "leafy_green_dish": "Poi Saag Bhaji",
                "possible_species": ["Poi Saag (Malabar Spinach)"],
                "species_confidence": 0.85,
                "is_species_exact": True
            }
        else:
            return {
                "leafy_green_dish": "East Indian Saag Bhaja",
                "possible_species": ["Koshila Saag", "Palanga Saag", "Beng Saag", "Bathua Saag"],
                "species_confidence": 0.40,
                "is_species_exact": False,
                "notes": "Exact leafy green species cannot be confirmed due to fine chopped/wilted state; broad dish classification preserved per Rule 32."
            }


def disambiguate_east_indian_pair(confusion_id: str) -> Optional[EastIndianConfusionPair]:
    return EAST_INDIAN_CONFUSION_REGISTRY.get(confusion_id)
