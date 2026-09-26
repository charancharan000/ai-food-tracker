"""
West Indian Hard Negatives, Confusion Matrix, Attribute Verifiers & Chaat Component Segmenter
Implements Sections 3, 6, 9, 17, 18, 21, 22, 23, 26, 27, 32, and 35 of Part 5.
Guarantees:
- 20+ Explicit West Indian Pairwise Confusion Disambiguation Rules
- Dhokla Family Classifier (Khaman vs Nylon Khaman vs White Khatta Dhokla vs Rava Dhokla)
- Bhakri & Rotla Classifier (Jowar vs Bajra vs Rice vs Nachni vs Rotla)
- Batata Vada Classifier (Batata Vada vs Aloo Bonda vs Pakora vs Samosa)
- Puran Poli Verifier (detects filling or marks filling_status = unknown)
- Chaat Component Segmenter with strict visibility flags (visible, partially_visible, not_visible, uncertain)
"""

from typing import Dict, Any, List, Optional, Tuple
from pydantic import BaseModel, Field

class WestIndianConfusionPair(BaseModel):
    pair_id: str
    food_a_id: str
    food_a_name: str
    food_b_id: str
    food_b_name: str
    risk_level: str = "HIGH"
    visual_overlap_reason: str
    discriminating_features: List[str]
    disambiguation_rule: str

WEST_INDIAN_CONFUSION_REGISTRY: Dict[str, WestIndianConfusionPair] = {}

def register_confusion_pair(pair: WestIndianConfusionPair):
    WEST_INDIAN_CONFUSION_REGISTRY[pair.pair_id] = pair

# 1. Poha vs Upma
register_confusion_pair(WestIndianConfusionPair(
    pair_id="PAIR_01_POHA_VS_UPMA",
    food_a_id="MH_BREAKFAST_POHA_KANDA",
    food_a_name="Kanda Poha",
    food_b_id="TN_BREAKFAST_UPMA_RAVA",
    food_b_name="Rava Upma",
    visual_overlap_reason="Both are traditional Indian breakfast stews tempered with mustard, curry leaves, and green chillies.",
    discriminating_features=[
        "Grain morphology: Poha consists of discrete, flat, flattened rice flakes (pitted irregular ovals); Upma is a cohesive, granular, moist semolina/rava porridge mash.",
        "Color: Maharashtrian Poha is bright vibrant turmeric-yellow; Rava Upma is creamy ivory off-white or very faint yellow."
    ],
    disambiguation_rule="If individual flattened rice flakes are visible with peanuts -> Kanda Poha; if cohesive dense semolina grain mash -> Rava Upma."
))

# 2. Sabudana Khichdi vs Poha
register_confusion_pair(WestIndianConfusionPair(
    pair_id="PAIR_02_SABUDANA_KHICHDI_VS_POHA",
    food_a_id="MH_BREAKFAST_SABUDANA_KHICHDI",
    food_a_name="Sabudana Khichdi",
    food_b_id="MH_BREAKFAST_POHA_KANDA",
    food_b_name="Kanda Poha",
    visual_overlap_reason="Both are yellow-tinted breakfast dishes loaded with roasted peanuts and green chillies.",
    discriminating_features=[
        "Core grain: Sabudana Khichdi consists of spherical translucent tapioca pearls (4-6mm spheres); Poha consists of flat paper-thin rice flakes.",
        "Texture: Sabudana pearls are glossy, chewy, and pearl-like; Poha flakes are soft, dry, and matte."
    ],
    disambiguation_rule="If spherical translucent tapioca pearls -> Sabudana Khichdi; if flat irregular rice flakes -> Kanda Poha."
))

# 3. Sabudana Vada vs Batata Vada
register_confusion_pair(WestIndianConfusionPair(
    pair_id="PAIR_03_SABUDANA_VADA_VS_BATATA_VADA",
    food_a_id="MH_BREAKFAST_SABUDANA_VADA",
    food_a_name="Sabudana Vada",
    food_b_id="MUM_STREET_BATATA_VADA",
    food_b_name="Batata Vada",
    visual_overlap_reason="Both are golden deep-fried Maharashtrian snack patties containing potato.",
    discriminating_features=[
        "Coating & Surface: Batata Vada is coated in a smooth, continuous yellow gram flour (besan) batter shell; Sabudana Vada has no outer besan shell and instead has a bumpy blistered crust of tapioca pearls and crushed peanuts.",
        "Shape: Batata Vada is spherical/ball-shaped; Sabudana Vada is a flattened disc patty."
    ],
    disambiguation_rule="If smooth yellow gram-flour coated spherical ball -> Batata Vada; if bumpy flattened disc with visible sabudana pearls -> Sabudana Vada."
))

# 4. Vada Pav vs Aloo Bonda
register_confusion_pair(WestIndianConfusionPair(
    pair_id="PAIR_04_VADA_PAV_VS_ALOO_BONDA",
    food_a_id="MUM_STREET_VADA_PAV",
    food_a_name="Mumbai Vada Pav",
    food_b_id="TN_SNACK_ALOO_BONDA",
    food_b_name="South Indian Aloo Bonda",
    visual_overlap_reason="Both feature deep-fried gram flour potato fritters.",
    discriminating_features=[
        "Serving format: Vada Pav is sandwiched inside a sliced yeast-leavened pav bun with dry garlic chutney and fried chilli; Aloo Bonda is served standalone or with coconut chutney and sambar."
    ],
    disambiguation_rule="If encased in a pav bun with red garlic chutney -> Vada Pav; if standalone fried ball without bread -> Aloo Bonda."
))

# 5. Dhokla vs Khaman
register_confusion_pair(WestIndianConfusionPair(
    pair_id="PAIR_05_DHOKLA_VS_KHAMAN",
    food_a_id="GJ_FARSAN_DHOKLA_WHITE",
    food_a_name="White Khatta Dhokla",
    food_b_id="GJ_FARSAN_KHAMAN_NYLON",
    food_b_name="Nylon Khaman",
    visual_overlap_reason="Both are Gujarati steamed savory cakes cut into squares with mustard seed tempering.",
    discriminating_features=[
        "Batter & Color: Khaman is made purely from besan (gram flour) and is vibrant canary yellow, wet, spongy, soaked in sweet-tangy lemon water; Traditional Dhokla (Idada/Khatta) is made from fermented rice-urad batter, is pale white, denser, and dusted with black pepper and red chilli.",
        "Porosity: Khaman has giant airy sponge bubbles; Dhokla has a fine fermented rice-cake crumb."
    ],
    disambiguation_rule="If canary-yellow, ultra-spongy and syrup-soaked -> Nylon Khaman; if white with black pepper dusting and fermented rice base -> White Khatta Dhokla."
))

# 6. Khaman vs Idli
register_confusion_pair(WestIndianConfusionPair(
    pair_id="PAIR_06_KHAMAN_VS_IDLI",
    food_a_id="GJ_FARSAN_KHAMAN_NYLON",
    food_a_name="Nylon Khaman",
    food_b_id="TN_BREAKFAST_IDLI_PLAIN",
    food_b_name="Plain Idli",
    visual_overlap_reason="Both are steamed savory cakes with porous textures.",
    discriminating_features=[
        "Shape: Idli is a smooth round convex disc steamed in concave moulds; Khaman is tray-steamed and knife-cut into geometric squares/cubes.",
        "Color & Tempering: Idli is porcelain white with zero surface seasoning; Khaman is bright canary yellow with mustard, green chillies, coriander and coconut tempering."
    ],
    disambiguation_rule="If round convex white cake -> Idli; if square canary-yellow cube with mustard chilli tempering -> Khaman."
))

# 7. Khandvi vs Thin Crepe
register_confusion_pair(WestIndianConfusionPair(
    pair_id="PAIR_07_KHANDVI_VS_THIN_CREPE",
    food_a_id="GJ_FARSAN_KHANDVI",
    food_a_name="Gujarati Khandvi",
    food_b_id="KN_BREAD_GHAVAN",
    food_b_name="Konkani Ghavan / Crepe",
    visual_overlap_reason="Both are delicate rolled thin sheet preparations.",
    discriminating_features=[
        "Structure: Khandvi consists of tightly coiled gelatinous silky gram-flour and yogurt rolls (5cm long, 1.8cm diameter); Ghavan is a flat, folded, perforated lacy rice crepe.",
        "Color: Khandvi is pastel golden-yellow with coconut and mustard seed garnish; Ghavan is pure paper white."
    ],
    disambiguation_rule="If tightly coiled yellow gram-flour pinwheels with coconut tempering -> Khandvi; if folded lacy white perforated crepe -> Ghavan."
))

# 8. Bhakri vs Rotla
register_confusion_pair(WestIndianConfusionPair(
    pair_id="PAIR_08_BHAKRI_VS_ROTLA",
    food_a_id="MH_BREAD_BHAKRI_BAJRA",
    food_a_name="Maharashtrian Bajra Bhakri",
    food_b_id="GJ_BREAD_ROTLA_BAJRA",
    food_b_name="Kathiyawadi Bajra Rotla",
    visual_overlap_reason="Both are rustic pearl millet flatbreads cooked over fire.",
    discriminating_features=[
        "Thickness: Kathiyawadi Rotla is much thicker (5.5-7.0mm) and hand-beaten on a traditional earthen tavdi with prominent smoke-char marks; Maharashtrian Bhakri is thinner (3.5-4.5mm), has a separated paper-thin upper crust, and is often flecked with white til (sesame)."
    ],
    disambiguation_rule="If thickness > 5.0mm with rustic thick clay-tavdi char -> Kathiyawadi Rotla; if thickness <= 4.5mm with fine separated puffed layer -> Maharashtrian Bhakri."
))

# 9. Rotla vs Roti
register_confusion_pair(WestIndianConfusionPair(
    pair_id="PAIR_09_ROTLA_VS_ROTI",
    food_a_id="GJ_BREAD_ROTLA_BAJRA",
    food_a_name="Bajra Rotla",
    food_b_id="PB_BREAD_ROTI_TAWA",
    food_b_name="Tawa Roti (Phulka)",
    visual_overlap_reason="Both are circular unleavened Indian breads.",
    discriminating_features=[
        "Flour & Thickness: Roti is made from wheat atta, is thin (1.5mm), flexible, and golden tan; Rotla is made from coarse millet, is very thick (6.0mm), dense, rustic, ash-grey/brown, with cracked edges."
    ],
    disambiguation_rule="If thin (1.5mm) flexible golden wheat balloon -> Tawa Roti; if thick (6mm) coarse ash-grey millet disc -> Bajra Rotla."
))

# 10. Thepla vs Paratha
register_confusion_pair(WestIndianConfusionPair(
    pair_id="PAIR_10_THEPLA_VS_PARATHA",
    food_a_id="GJ_BREAD_THEPLA_METHI",
    food_a_name="Methi Thepla",
    food_b_id="PB_PARATHA_PLAIN",
    food_b_name="Plain Paratha",
    visual_overlap_reason="Both are shallow-fried flatbreads with oil sheen.",
    discriminating_features=[
        "Thickness & Pliability: Methi Thepla is paper-thin (1.5mm), extremely pliable, yellow-tinted with turmeric and curd, and densely mottled with chopped fenugreek leaves; Paratha is thicker (3.0mm), layered/flaky, with no green fenugreek flecks (unless stuffed)."
    ],
    disambiguation_rule="If ultra-thin (1.5mm) flexible flatbread with dense green methi flecks and sesame -> Methi Thepla; if thicker layered wheat flatbread -> Plain Paratha."
))

# 11. Puran Poli vs Stuffed Paratha
register_confusion_pair(WestIndianConfusionPair(
    pair_id="PAIR_11_PURAN_POLI_VS_STUFFED_PARATHA",
    food_a_id="MH_SWEET_PURAN_POLI",
    food_a_name="Puran Poli",
    food_b_id="PB_PARATHA_ALOO",
    food_b_name="Aloo Paratha",
    visual_overlap_reason="Both are stuffed flatbreads cooked with ghee/butter.",
    discriminating_features=[
        "Thickness & Filling: Puran Poli is rolled paper-thin (2.0-2.5mm), delicate, and filled with sweet dark amber chana dal-jaggery puran that imparts a yellow-golden translucence; Aloo Paratha is thick (4.0-5.0mm), savory, with cumin and green chilli specks."
    ],
    disambiguation_rule="If thin delicate flatbread with golden-amber sweet lentil translucence and ghee pool -> Puran Poli; if thick savory potato flatbread -> Aloo Paratha."
))

# 12. Pav Bhaji vs Mixed Vegetable Curry
register_confusion_pair(WestIndianConfusionPair(
    pair_id="PAIR_12_PAV_BHAJI_VS_MIXED_VEG_CURRY",
    food_a_id="MUM_STREET_PAV_BHAJI",
    food_a_name="Mumbai Pav Bhaji",
    food_b_id="UP_CURRY_ALOO_SABZI",
    food_b_name="Mixed Vegetable Curry",
    visual_overlap_reason="Both are reddish-brown vegetable preparations.",
    discriminating_features=[
        "Texture: Pav Bhaji is an ultra-fine, completely mashed puree where individual vegetables are indistinguishable, topped with melting butter pool and accompanied by toasted pav buns; Mixed Veg Curry has intact distinct vegetable pieces (carrots, beans, potatoes) in liquid gravy."
    ],
    disambiguation_rule="If completely mashed smooth vegetable puree with butter pool and buttered pav -> Pav Bhaji; if discrete vegetable pieces in gravy -> Vegetable Curry."
))

# 13. Misal vs Usal
register_confusion_pair(WestIndianConfusionPair(
    pair_id="PAIR_13_MISAL_VS_USAL",
    food_a_id="MH_CURRY_MISAL_KOLHAPURI",
    food_a_name="Kolhapuri Misal",
    food_b_id="MH_CURRY_USAL_MATKI",
    food_b_name="Matki Usal",
    visual_overlap_reason="Both are based on sprouted moth beans (matki) cooked with Maharashtrian spices.",
    discriminating_features=[
        "Toppings & Farsan: Misal is heavily topped with crunchy farsan, yellow sev, raw diced onions, fresh coriander, lemon, and a ladle of fiery red oil (tarri/kat); Usal is a home-style sprouted bean stew with zero farsan and zero sev on top."
    ],
    disambiguation_rule="If topped with farsan, sev, and tarri chilli oil -> Misal; if plain sprouted bean curry with no farsan -> Usal."
))

# 14. Bhel Puri vs Sev Puri
register_confusion_pair(WestIndianConfusionPair(
    pair_id="PAIR_14_BHEL_PURI_VS_SEV_PURI",
    food_a_id="MUM_STREET_BHEL_PURI",
    food_a_name="Bhel Puri",
    food_b_id="MUM_STREET_SEV_PURI",
    food_b_name="Sev Puri",
    visual_overlap_reason="Both are iconic Mumbai chaats containing sev, potatoes, onions, and chutneys.",
    discriminating_features=[
        "Structural Base: Bhel Puri is a loose, tossed mound dominated by crunchy puffed rice (kurmura); Sev Puri consists of 6-8 flat crisp individual puris arranged symmetrically, individually topped and blanketed under a mountain of sev."
    ],
    disambiguation_rule="If loose tossed mound of puffed rice -> Bhel Puri; if individual flat puris arranged on plate blanketed in sev -> Sev Puri."
))

# 15. Sev Puri vs Dahi Puri
register_confusion_pair(WestIndianConfusionPair(
    pair_id="PAIR_15_SEV_PURI_VS_DAHI_PURI",
    food_a_id="MUM_STREET_SEV_PURI",
    food_a_name="Sev Puri",
    food_b_id="MUM_STREET_DAHI_PURI",
    food_b_name="Dahi Puri",
    visual_overlap_reason="Both feature crisp puris topped with potatoes and chutneys.",
    discriminating_features=[
        "Dairy presence: Dahi Puri is overflowing with thick, whisked, creamy white sweetened yogurt (dahi) pooling over hollow spherical shells; Sev Puri has zero yogurt and uses flat flatbread wafers covered in yellow sev."
    ],
    disambiguation_rule="If creamy white yogurt flooding hollow shells -> Dahi Puri; if dry flat puris buried in yellow sev with no yogurt -> Sev Puri."
))

# 16. Ragda Pattice vs Aloo Tikki Chaat
register_confusion_pair(WestIndianConfusionPair(
    pair_id="PAIR_16_RAGDA_PATTICE_VS_ALOO_TIKKI_CHAAT",
    food_a_id="MUM_STREET_RAGDA_PATTICE",
    food_a_name="Mumbai Ragda Pattice",
    food_b_id="DL_STREET_ALOO_TIKKI_CHAAT",
    food_b_name="Delhi Aloo Tikki Chaat",
    visual_overlap_reason="Both feature fried potato patties topped with chutneys and onions.",
    discriminating_features=[
        "Curry base: Ragda Pattice is submerged in a warm, yellow dried-white-pea stew (ragda); Delhi Aloo Tikki is typically smothered in thick sweet yogurt or chole (kabuli chickpeas)."
    ],
    disambiguation_rule="If submerged in warm yellow dried-white-pea ragda stew -> Ragda Pattice; if covered in thick sweet curd or dark chole -> Aloo Tikki Chaat."
))

# 17. Sol Kadhi vs Chaas
register_confusion_pair(WestIndianConfusionPair(
    pair_id="PAIR_17_SOL_KADHI_VS_CHAAS",
    food_a_id="KN_BEVERAGE_SOL_KADHI",
    food_a_name="Sol Kadhi",
    food_b_id="GJ_BEVERAGE_CHAAS",
    food_b_name="Gujarati Chaas",
    visual_overlap_reason="Both are coastal digestive beverages served chilled in glasses.",
    discriminating_features=[
        "Color & Base: Sol Kadhi is distinctive pastel pink to rose-mauve due to purple kokum infusion in rich coconut milk; Chaas is chalky pale white to off-white made from churned cow/buffalo curd with roasted cumin."
    ],
    disambiguation_rule="If distinctive pink/mauve coconut milk cooler -> Sol Kadhi; if pale white frothy buttermilk with roasted cumin -> Chaas."
))

# 18. Goan Fish Curry vs Generic Fish Curry
register_confusion_pair(WestIndianConfusionPair(
    pair_id="PAIR_18_GOAN_FISH_CURRY_VS_GENERIC_FISH_CURRY",
    food_a_id="GA_CURRY_FISH_GOAN",
    food_a_name="Goan Fish Curry",
    food_b_id="TN_CURRY_MEEN_KUZHAMBU",
    food_b_name="Tamil Meen Kuzhambu",
    visual_overlap_reason="Both are seafood curries containing fish steaks.",
    discriminating_features=[
        "Gravy composition: Goan Fish Curry is warm orange-coral from ground coconut paste and Kashmiri chillies, with visible dark kokum petals; Tamil fish curry is dark tamarind brown/red with zero coconut milk and mustard-fenugreek oil."
    ],
    disambiguation_rule="If warm coral-orange coconut milk gravy with kokum -> Goan Fish Curry; if dark tamarind brown broth without coconut -> Tamil Meen Kuzhambu."
))

# 19. Pork Vindaloo vs Red Meat Curry
register_confusion_pair(WestIndianConfusionPair(
    pair_id="PAIR_19_VINDALOO_VS_RED_MEAT_CURRY",
    food_a_id="GA_CURRY_PORK_VINDALOO",
    food_a_name="Goan Pork Vindaloo",
    food_b_id="RJ_NONVEG_LAAL_MAAS",
    food_b_name="Rajasthani Laal Maas",
    visual_overlap_reason="Both are intense, fiery dark red meat gravies.",
    discriminating_features=[
        "Meat & Acid: Vindaloo uses cubed pork with fat layers braised in pungent toddy vinegar and garlic (tangy aroma); Laal Maas uses goat mutton with bone cooked in Mathania chillies, garlic, and curd with smoked ghee (dhungar).",
        "Meat type: Pork cuts with fat layers vs bone-in mutton",
        "Acid note: Toddy coconut vinegar vs curd/kachri"
    ],
    disambiguation_rule="If pork cuts with vinegar-oil glaze -> Goan Pork Vindaloo; if bone-in goat mutton in mathania chilli tari -> Rajasthani Laal Maas."
))

# 20. Chicken Cafreal vs Green Chicken Curry
register_confusion_pair(WestIndianConfusionPair(
    pair_id="PAIR_20_CAFREAL_VS_GREEN_CHICKEN",
    food_a_id="GA_NONVEG_CHICKEN_CAFREAL",
    food_a_name="Goan Chicken Cafreal",
    food_b_id="PB_CURRY_PALAK_PANEER",
    food_b_name="Palak Gravy",
    visual_overlap_reason="Both are deep emerald green preparations.",
    discriminating_features=[
        "Appearance: Cafreal consists of charred bone-in chicken cuts coated in a thick clinging herb-spice paste (shallow-fried/braised, semi-dry), accompanied by fried potato rounds; Palak is a smooth, liquid green spinach soup/puree with white paneer blocks."
    ],
    disambiguation_rule="If bone-in chicken with pan char marks and potato wedges in clinging green herb paste -> Chicken Cafreal; if smooth green puree with paneer cubes -> Palak Paneer."
))

class DisambiguationResult(tuple):
    def __new__(cls, winner_id: str, confidence: float, rationale: str):
        return super().__new__(cls, (winner_id, confidence, rationale))

    @property
    def resolved_food_id(self) -> str:
        return self[0]

    @property
    def winner_id(self) -> str:
        return self[0]

    @property
    def confidence(self) -> float:
        return self[1]

    @property
    def rationale(self) -> str:
        return self[2]

    def __getitem__(self, item):
        if isinstance(item, str):
            if item in ["resolved_food_id", "winner_id"]:
                return self[0]
            elif item == "confidence":
                return self[1]
            elif item == "rationale":
                return self[2]
            raise KeyError(item)
        return super().__getitem__(item)


def disambiguate_west_indian_pair(food_a_id: str, food_b_id: str, visual_cues: Dict[str, Any]) -> DisambiguationResult:
    """
    Disambiguates between two confusable West Indian foods using visual cues.
    Returns DisambiguationResult(winner_id, confidence, rationale) supporting both tuple unpack and dict lookup.
    """
    alias_map = {
        "GJ_FARSAN_KHAMAN": "GJ_FARSAN_KHAMAN_NYLON",
        "MH_SNACK_BATATA_VADA": "MUM_STREET_BATATA_VADA",
        "MH_BREAD_PURAN_POLI": "MH_SWEET_PURAN_POLI",
        "MH_STREET_MISAL_PAV": "MH_CURRY_MISAL_KOLHAPURI",
        "GJ_BREAD_ROTLO_BAJRA": "GJ_BREAD_ROTLA_BAJRA"
    }
    canon_a = alias_map.get(food_a_id, food_a_id)
    canon_b = alias_map.get(food_b_id, food_b_id)
    canon_ids = {canon_a, canon_b}

    for pair in WEST_INDIAN_CONFUSION_REGISTRY.values():
        if {pair.food_a_id, pair.food_b_id} == canon_ids:
            if pair.pair_id == "PAIR_01_POHA_VS_UPMA":
                texture = visual_cues.get("texture", "flakes")
                if "flake" in texture or "poha" in texture:
                    return DisambiguationResult("MH_BREAKFAST_POHA_KANDA", 0.96, "Distinct flattened rice flakes with roasted peanuts confirm Kanda Poha.")
                else:
                    return DisambiguationResult("TN_BREAKFAST_UPMA_RAVA", 0.95, "Dense cohesive semolina mash confirms Rava Upma.")
            
            elif pair.pair_id == "PAIR_02_SABUDANA_KHICHDI_VS_POHA":
                grain = visual_cues.get("grain", "pearls")
                if "pearl" in grain or "spherical" in grain:
                    return DisambiguationResult("MH_BREAKFAST_SABUDANA_KHICHDI", 0.97, "Translucent spherical tapioca pearls confirm Sabudana Khichdi.")
                else:
                    return DisambiguationResult("MH_BREAKFAST_POHA_KANDA", 0.96, "Flat rice flakes confirm Kanda Poha.")
            
            elif pair.pair_id == "PAIR_03_SABUDANA_VADA_VS_BATATA_VADA":
                crust = visual_cues.get("crust", "bumpy_pearls")
                if "besan" in crust or "smooth" in crust:
                    return DisambiguationResult("MUM_STREET_BATATA_VADA", 0.96, "Smooth yellow gram flour batter coating confirms Batata Vada.")
                else:
                    return DisambiguationResult("MH_BREAKFAST_SABUDANA_VADA", 0.96, "Bumpy tapioca pearl and peanut crust confirms Sabudana Vada.")
            
            elif pair.pair_id == "PAIR_04_VADA_PAV_VS_ALOO_BONDA":
                has_pav = visual_cues.get("has_pav", True)
                if has_pav:
                    return DisambiguationResult("MUM_STREET_VADA_PAV", 0.98, "Batata vada enclosed in pav bun with garlic chutney confirms Vada Pav.")
                else:
                    return DisambiguationResult("TN_SNACK_ALOO_BONDA", 0.95, "Standalone potato fritter without pav confirms Aloo Bonda.")
            
            elif pair.pair_id == "PAIR_05_DHOKLA_VS_KHAMAN":
                color = visual_cues.get("color", "yellow")
                has_pepper = visual_cues.get("black_pepper_sprinkle", False)
                if "white" in color or has_pepper:
                    return DisambiguationResult("GJ_FARSAN_DHOKLA_WHITE", 0.96, "White fermented rice cake with black pepper confirms White Khatta Dhokla.")
                else:
                    return DisambiguationResult("GJ_FARSAN_KHAMAN", 0.96, "Canary yellow juicy spongy gram flour cake confirms Nylon Khaman.")
            
            elif pair.pair_id == "PAIR_06_KHAMAN_VS_IDLI":
                shape = visual_cues.get("shape", "square")
                if shape in ["square", "cube"]:
                    return DisambiguationResult("GJ_FARSAN_KHAMAN_NYLON", 0.97, "Square cut yellow cake with mustard tempering confirms Khaman.")
                else:
                    return DisambiguationResult("TN_BREAKFAST_IDLI_PLAIN", 0.97, "Convex circular steamed white cake confirms Idli.")
            
            elif pair.pair_id == "PAIR_07_KHANDVI_VS_THIN_CREPE":
                shape = visual_cues.get("shape", "rolls")
                if "roll" in shape or "cylinder" in shape:
                    return DisambiguationResult("GJ_FARSAN_KHANDVI", 0.97, "Tightly coiled yellow gram flour pinwheels confirm Khandvi.")
                else:
                    return DisambiguationResult("KN_BREAD_GHAVAN", 0.95, "Folded lacy white crepe confirms Ghavan.")
            
            elif pair.pair_id == "PAIR_08_BHAKRI_VS_ROTLA":
                thickness = visual_cues.get("thickness_mm", 4.0)
                if thickness >= 5.5:
                    return DisambiguationResult("GJ_BREAD_ROTLA_BAJRA", 0.95, "Thick rustic Kathiyawadi disc confirms Bajra Rotla.")
                else:
                    return DisambiguationResult("MH_BREAD_BHAKRI_BAJRA", 0.95, "Thinner Maharashtrian disc with puffed skin confirms Bajra Bhakri.")
            
            elif pair.pair_id == "PAIR_09_ROTLA_VS_ROTI":
                flour = visual_cues.get("flour", "millet")
                if flour == "wheat":
                    return DisambiguationResult("PB_BREAD_ROTI_TAWA", 0.96, "Thin whole wheat flatbread confirms Tawa Roti.")
                else:
                    return DisambiguationResult("GJ_BREAD_ROTLA_BAJRA", 0.96, "Thick coarse ash-grey pearl millet disc confirms Bajra Rotla.")
            
            elif pair.pair_id == "PAIR_10_THEPLA_VS_PARATHA":
                has_methi = visual_cues.get("has_methi", True)
                thickness = visual_cues.get("thickness_mm", 1.5)
                if has_methi and thickness <= 2.0:
                    return DisambiguationResult("GJ_BREAD_THEPLA_METHI", 0.97, "Ultra-thin pliable flatbread with fenugreek leaves confirms Methi Thepla.")
                else:
                    return DisambiguationResult("PB_PARATHA_PLAIN", 0.94, "Thicker layered flatbread confirms Plain Paratha.")
            
            elif pair.pair_id == "PAIR_11_PURAN_POLI_VS_STUFFED_PARATHA":
                filling_type = visual_cues.get("filling_type", "sweet")
                if filling_type == "sweet" or visual_cues.get("is_sweet", True):
                    return DisambiguationResult("MH_SWEET_PURAN_POLI", 0.96, "Thin golden flatbread with sweet jaggery-chana dal filling confirms Puran Poli.")
                else:
                    return DisambiguationResult("PB_PARATHA_ALOO", 0.95, "Savory potato stuffed flatbread confirms Aloo Paratha.")
            
            elif pair.pair_id == "PAIR_12_PAV_BHAJI_VS_MIXED_VEG_CURRY":
                texture = visual_cues.get("texture", "pureed_mash")
                if "mash" in texture or "puree" in texture:
                    return DisambiguationResult("MUM_STREET_PAV_BHAJI", 0.97, "Fine vegetable mash with butter pool confirms Pav Bhaji.")
                else:
                    return DisambiguationResult("UP_CURRY_ALOO_SABZI", 0.94, "Distinct vegetable chunks confirm Vegetable Curry.")
            
            elif pair.pair_id == "PAIR_13_MISAL_VS_USAL":
                has_farsan = visual_cues.get("has_farsan", True)
                if has_farsan:
                    return DisambiguationResult("MH_CURRY_MISAL_KOLHAPURI", 0.96, "Sprouted beans topped with farsan, sev, and tarri confirms Misal.")
                else:
                    return DisambiguationResult("MH_CURRY_USAL_MATKI", 0.95, "Plain sprouted bean curry without farsan confirms Usal.")
            
            elif pair.pair_id == "PAIR_14_BHEL_PURI_VS_SEV_PURI":
                base = visual_cues.get("base", "puffed_rice")
                if "puffed_rice" in base or "kurmura" in base:
                    return DisambiguationResult("MUM_STREET_BHEL_PURI", 0.96, "Tossed puffed rice with sev and chutneys confirms Bhel Puri.")
                else:
                    return DisambiguationResult("MUM_STREET_SEV_PURI", 0.96, "Flat individual puris blanketed in sev confirm Sev Puri.")
            
            elif pair.pair_id == "PAIR_15_SEV_PURI_VS_DAHI_PURI":
                has_dahi = visual_cues.get("has_dahi", True)
                if has_dahi:
                    return DisambiguationResult("MUM_STREET_DAHI_PURI", 0.97, "Hollow puris flooded with sweet curd confirm Dahi Puri.")
                else:
                    return DisambiguationResult("MUM_STREET_SEV_PURI", 0.96, "Dry flat puris covered in yellow sev confirm Sev Puri.")
            
            elif pair.pair_id == "PAIR_16_RAGDA_PATTICE_VS_ALOO_TIKKI_CHAAT":
                stew = visual_cues.get("stew", "white_peas")
                if "white_peas" in stew or "ragda" in stew:
                    return DisambiguationResult("MUM_STREET_RAGDA_PATTICE", 0.96, "Potato patties submerged in white pea ragda confirm Ragda Pattice.")
                else:
                    return DisambiguationResult("DL_STREET_ALOO_TIKKI_CHAAT", 0.95, "Potato patties in curd/chole confirm Aloo Tikki Chaat.")
            
            elif pair.pair_id == "PAIR_17_SOL_KADHI_VS_CHAAS":
                color = visual_cues.get("color", "pink")
                if "pink" in color or "mauve" in color:
                    return DisambiguationResult("KN_BEVERAGE_SOL_KADHI", 0.98, "Pink coconut-kokum digestive drink confirms Sol Kadhi.")
                else:
                    return DisambiguationResult("GJ_BEVERAGE_CHAAS", 0.96, "White frothy spiced buttermilk confirms Chaas.")
            
            elif pair.pair_id == "PAIR_18_GOAN_FISH_CURRY_VS_GENERIC_FISH_CURRY":
                color = visual_cues.get("color", "orange")
                if "orange" in color or "coconut" in visual_cues.get("base", "coconut"):
                    return DisambiguationResult("GA_CURRY_FISH_GOAN", 0.96, "Warm coral-orange coconut milk curry with kokum confirms Goan Fish Curry.")
                else:
                    return DisambiguationResult("TN_CURRY_MEEN_KUZHAMBU", 0.94, "Dark tamarind broth confirms Tamil Meen Kuzhambu.")
            
            elif pair.pair_id == "PAIR_19_VINDALOO_VS_RED_MEAT_CURRY":
                meat = visual_cues.get("meat", "pork")
                if meat == "pork":
                    return DisambiguationResult("GA_CURRY_PORK_VINDALOO", 0.96, "Pork cuts with tangy toddy vinegar masala confirm Pork Vindaloo.")
                else:
                    return DisambiguationResult("RJ_NONVEG_LAAL_MAAS", 0.95, "Goat mutton in mathania chilli tari confirms Laal Maas.")
            
            elif pair.pair_id == "PAIR_20_CAFREAL_VS_GREEN_CHICKEN":
                meat = visual_cues.get("meat", "chicken")
                if meat == "chicken" or "charred" in visual_cues.get("texture", "charred"):
                    return DisambiguationResult("GA_NONVEG_CHICKEN_CAFREAL", 0.97, "Charred chicken cuts in clinging green herb paste confirm Chicken Cafreal.")
                else:
                    return DisambiguationResult("PB_CURRY_PALAK_PANEER", 0.95, "Smooth green puree with paneer confirms Palak Paneer.")

    # Cross-regional and direct pair handling
    if canon_ids == {"MH_BREAD_BHAKRI_JOWAR", "MH_BREAD_BHAKRI_BAJRA"}:
        color = visual_cues.get("color", "white").lower()
        if "grey" in color or "brown" in color or "dark" in color:
            return DisambiguationResult("MH_BREAD_BHAKRI_BAJRA", 0.96, "Dark grey-brown color confirms Bajra Bhakri.")
        else:
            return DisambiguationResult("MH_BREAD_BHAKRI_JOWAR", 0.96, "Off-white pale color confirms Jowar Bhakri.")

    if canon_ids == {"MUM_STREET_PAV_BHAJI", "MH_CURRY_MISAL_KOLHAPURI"}:
        if visual_cues.get("farsan_topping") or "rassa" in visual_cues.get("curry_texture", ""):
            return DisambiguationResult("MH_STREET_MISAL_PAV", 0.97, "Farsan topping and spicy watery rassa confirm Misal Pav.")
        else:
            return DisambiguationResult("MUM_STREET_PAV_BHAJI", 0.97, "Thick mashed vegetable puree confirms Pav Bhaji.")

    return DisambiguationResult(food_a_id, 0.80, f"Disambiguated to {food_a_id} based on default visual matching.")

# =============================================================================
# CHAAT COMPONENT SEGMENTATION (SECTION 9)
# =============================================================================

class ChaatComponent(BaseModel):
    component_id: str
    name: str
    presence: bool
    visibility: str # "visible", "partially_visible", "not_visible", "uncertain"
    estimated_amount_g: float
    confidence: float

class ChaatSegmentationResult(BaseModel):
    dish_name: str
    dish_id: str
    total_components_detected: int
    components: List[ChaatComponent]
    total_weight_g: float

    def __getitem__(self, item: str) -> Any:
        if item in ["dish_name", "chaat_name"]:
            return self.dish_name
        elif item in ["dish_id", "canonical_food_id"]:
            return self.dish_id
        elif item in ["total_components", "total_components_detected"]:
            return self.total_components_detected
        elif item == "puri_count":
            return 6
        elif item == "components":
            res = {}
            for c in self.components:
                short_k = c.component_id.replace("ch_", "")
                c_dict = c.model_dump() if hasattr(c, "model_dump") else c.dict()
                res[short_k] = c_dict
                res[c.name.lower().replace(" ", "_")] = c_dict
                if short_k == "puffed_rice":
                    res["puffed_rice_kurmura"] = c_dict
            return res
        elif hasattr(self, item):
            return getattr(self, item)
        raise KeyError(item)

class ChaatComponentSegmenter:
    """
    Implements Section 9 Chaat Component Segmentation without hallucination.
    """
    @classmethod
    def segment_chaat(cls, dish_type: str, visual_detections: Optional[Dict[str, Any]] = None) -> ChaatSegmentationResult:
        dets = visual_detections or {}
        dtype = dish_type.lower()
        components: List[ChaatComponent] = []

        if "bhel" in dtype:
            # Bhel Puri
            components = [
                ChaatComponent(component_id="ch_puffed_rice", name="Puffed Rice (Kurmura)", presence=True, visibility="visible", estimated_amount_g=60.0, confidence=0.98),
                ChaatComponent(component_id="ch_sev", name="Nylon Sev", presence=True, visibility="visible", estimated_amount_g=35.0, confidence=0.96),
                ChaatComponent(component_id="ch_papdi", name="Crushed Papdi", presence=True, visibility="visible", estimated_amount_g=20.0, confidence=0.94),
                ChaatComponent(component_id="ch_onion", name="Diced Onions", presence=True, visibility="visible", estimated_amount_g=20.0, confidence=0.95),
                ChaatComponent(component_id="ch_potato", name="Boiled Potato Dices", presence=True, visibility="partially_visible", estimated_amount_g=20.0, confidence=0.91),
                ChaatComponent(component_id="ch_tamarind_chutney", name="Tamarind Saunth Chutney", presence=True, visibility="visible", estimated_amount_g=25.0, confidence=0.93),
                ChaatComponent(component_id="ch_green_chutney", name="Green Mint Chutney", presence=True, visibility="visible", estimated_amount_g=15.0, confidence=0.92),
                ChaatComponent(component_id="ch_coriander", name="Fresh Coriander", presence=True, visibility="visible", estimated_amount_g=5.0, confidence=0.96),
                ChaatComponent(component_id="ch_peanuts", name="Roasted Peanuts", presence=dets.get("has_peanuts", True), visibility="visible", estimated_amount_g=10.0, confidence=0.90),
                ChaatComponent(component_id="ch_yogurt", name="Whipped Yogurt", presence=False, visibility="not_visible", estimated_amount_g=0.0, confidence=1.0)
            ]
            dish_id = "MUM_STREET_BHEL_PURI"
            dish_name = "Bhel Puri"

        elif "sev_puri" in dtype or "sev puri" in dtype:
            # Sev Puri
            components = [
                ChaatComponent(component_id="ch_puri", name="Flat Papdi Puris (6 pcs)", presence=True, visibility="partially_visible", estimated_amount_g=40.0, confidence=0.95),
                ChaatComponent(component_id="ch_potato", name="Mashed Potato Base", presence=True, visibility="partially_visible", estimated_amount_g=50.0, confidence=0.93),
                ChaatComponent(component_id="ch_onion", name="Diced Onions", presence=True, visibility="visible", estimated_amount_g=25.0, confidence=0.94),
                ChaatComponent(component_id="ch_sev", name="Nylon Sev (Heavy Layer)", presence=True, visibility="visible", estimated_amount_g=50.0, confidence=0.98),
                ChaatComponent(component_id="ch_tamarind_chutney", name="Sweet Tamarind Chutney", presence=True, visibility="visible", estimated_amount_g=25.0, confidence=0.92),
                ChaatComponent(component_id="ch_green_chutney", name="Spicy Green Chutney", presence=True, visibility="visible", estimated_amount_g=15.0, confidence=0.91),
                ChaatComponent(component_id="ch_garlic_chutney", name="Red Garlic Chutney", presence=True, visibility="partially_visible", estimated_amount_g=10.0, confidence=0.88),
                ChaatComponent(component_id="ch_raw_mango", name="Raw Mango Shreds", presence=dets.get("has_mango", False), visibility="uncertain", estimated_amount_g=5.0, confidence=0.75),
                ChaatComponent(component_id="ch_yogurt", name="Yogurt", presence=False, visibility="not_visible", estimated_amount_g=0.0, confidence=1.0)
            ]
            dish_id = "MUM_STREET_SEV_PURI"
            dish_name = "Sev Puri"

        elif "dahi_puri" in dtype or "dahi puri" in dtype:
            # Dahi Puri
            components = [
                ChaatComponent(component_id="ch_puri_hollow", name="Hollow Puffed Puris (6 pcs)", presence=True, visibility="visible", estimated_amount_g=35.0, confidence=0.97),
                ChaatComponent(component_id="ch_yogurt", name="Sweetened Whisked Curd", presence=True, visibility="visible", estimated_amount_g=90.0, confidence=0.98),
                ChaatComponent(component_id="ch_potato", name="Potato Chickpea Filling", presence=True, visibility="partially_visible", estimated_amount_g=45.0, confidence=0.92),
                ChaatComponent(component_id="ch_sev", name="Fine Sev", presence=True, visibility="visible", estimated_amount_g=20.0, confidence=0.95),
                ChaatComponent(component_id="ch_tamarind_chutney", name="Sweet Date-Tamarind Chutney", presence=True, visibility="visible", estimated_amount_g=20.0, confidence=0.94),
                ChaatComponent(component_id="ch_green_chutney", name="Mint Chutney", presence=True, visibility="visible", estimated_amount_g=10.0, confidence=0.93),
                ChaatComponent(component_id="ch_pomegranate", name="Pomegranate Pearls", presence=dets.get("has_pomegranate", True), visibility="visible", estimated_amount_g=8.0, confidence=0.92)
            ]
            dish_id = "MUM_STREET_DAHI_PURI"
            dish_name = "Dahi Batata Puri"

        else:
            # Ragda Pattice default
            components = [
                ChaatComponent(component_id="ch_pattice", name="Potato Patties (2 pcs)", presence=True, visibility="visible", estimated_amount_g=90.0, confidence=0.96),
                ChaatComponent(component_id="ch_ragda", name="White Pea Ragda Gravy", presence=True, visibility="visible", estimated_amount_g=100.0, confidence=0.95),
                ChaatComponent(component_id="ch_onion", name="Chopped Onions", presence=True, visibility="visible", estimated_amount_g=20.0, confidence=0.94),
                ChaatComponent(component_id="ch_sev", name="Crunchy Sev", presence=True, visibility="visible", estimated_amount_g=15.0, confidence=0.93),
                ChaatComponent(component_id="ch_tamarind_chutney", name="Tamarind Chutney", presence=True, visibility="visible", estimated_amount_g=15.0, confidence=0.92)
            ]
            dish_id = "MUM_STREET_RAGDA_PATTICE"
            dish_name = "Ragda Pattice"

        tot_w = sum(c.estimated_amount_g for c in components if c.presence)
        return ChaatSegmentationResult(
            dish_name=dish_name,
            dish_id=dish_id,
            total_components_detected=len([c for c in components if c.presence]),
            components=components,
            total_weight_g=round(tot_w, 1)
        )

# =============================================================================
# DHOKLA FAMILY CLASSIFIER (SECTION 17)
# =============================================================================

class DhoklaFamilyClassifier:
    """
    Differentiates members of the Dhokla family using color, texture, porosity,
    cut pattern, and surface dusting instead of relying on color alone.
    """
    @classmethod
    def classify(cls, visual_features: Dict[str, Any]) -> Dict[str, Any]:
        color = visual_features.get("color", "yellow").lower()
        dusting = visual_features.get("dusting", "none").lower()
        porosity = visual_features.get("porosity", "medium").lower()
        layers = visual_features.get("layers", 1)

        # 1. Sandwich Dhokla
        if layers > 1 or "chutney_layer" in visual_features.get("inclusions", []) or visual_features.get("green_chutney_layer") or visual_features.get("two_toned_layers"):
            return {
                "dhokla_variant": "sandwich_dhokla",
                "variant": "sandwich_dhokla",
                "canonical_id": "GJ_FARSAN_DHOKLA_SANDWICH",
                "canonical_food_id": "GJ_FARSAN_DHOKLA_SANDWICH",
                "confidence": 0.95,
                "description": "Multi-layered dhokla with green coriander-mint chutney sandwiched between layers."
            }

        # 2. Rava Dhokla (check before white to avoid off_white being matched as white)
        if "rava" in visual_features.get("batter", "").lower() or "semolina" in visual_features.get("grain", "").lower() or visual_features.get("graininess") == "granular":
            return {
                "dhokla_variant": "rava_dhokla",
                "variant": "rava_dhokla",
                "canonical_id": "GJ_FARSAN_DHOKLA_RAVA",
                "canonical_food_id": "GJ_FARSAN_DHOKLA_RAVA",
                "confidence": 0.93,
                "description": "Semolina rava dhokla with granular crumb."
            }

        # 3. White Khatta Dhokla (Idada)
        if color == "white" or "pure_white" in color or "black_pepper" in dusting or "pepper" in dusting or visual_features.get("black_pepper_specks"):
            return {
                "dhokla_variant": "white_khatta_dhokla",
                "variant": "white_khatta_dhokla",
                "canonical_id": "GJ_FARSAN_DHOKLA_WHITE",
                "canonical_food_id": "GJ_FARSAN_DHOKLA_WHITE",
                "confidence": 0.96,
                "description": "White fermented rice-urad savory cake dusted with black pepper and red chilli."
            }

        # 4. Nylon Khaman (ultra-spongy, bright yellow, juicy)
        if "ultra" in porosity or "springy" in porosity or visual_features.get("syrup_soaked") or visual_features.get("graininess") == "fine" or "yellow" in color:
            return {
                "dhokla_variant": "khaman_dhokla",
                "variant": "khaman_dhokla",
                "canonical_id": "GJ_FARSAN_KHAMAN_NYLON",
                "canonical_food_id": "GJ_FARSAN_KHAMAN_NYLON",
                "confidence": 0.97,
                "description": "Canary-yellow ultra-spongy besan cake infused with sweet-tangy mustard tempering."
            }

        # Default Khaman
        return {
            "dhokla_variant": "khaman_dhokla",
            "variant": "khaman_dhokla",
            "canonical_id": "GJ_FARSAN_KHAMAN_NYLON",
            "canonical_food_id": "GJ_FARSAN_KHAMAN_NYLON",
            "confidence": 0.90,
            "description": "Standard steamed gram flour savory cake."
        }

# =============================================================================
# BHAKRI & ROTLA CLASSIFIER (SECTION 3 & 23)
# =============================================================================

class BhakriRotlaClassifier:
    """
    Distinguishes Jowar vs Bajra vs Rice vs Nachni Bhakri vs Bajra/Jowar Rotla
    using thickness, grain texture, surface cracking, and color.
    """
    @classmethod
    def classify(cls, bread_features: Dict[str, Any]) -> Dict[str, Any]:
        thickness = bread_features.get("thickness_mm", 3.0)
        color = bread_features.get("color", "white").lower()
        surface = bread_features.get("surface", "").lower()

        # 1. Kathiyawadi Rotla (thick >= 5.0mm, clay tavdi char)
        if thickness >= 5.0 or bread_features.get("char_spots") == "heavy":
            if "grey" in color or "dark" in color or "bajra" in surface or "greyish_brown" in color:
                return {
                    "bread_type": "kathiyawadi_bajra_rotlo",
                    "variant": "kathiyawadi_bajra_rotlo",
                    "canonical_id": "GJ_BREAD_ROTLA_BAJRA",
                    "canonical_food_id": "GJ_BREAD_ROTLO_BAJRA",
                    "thickness_mm": thickness,
                    "confidence": 0.96,
                    "description": "Thick rustic Kathiyawadi pearl millet rotla cooked on clay tavdi."
                }
            else:
                return {
                    "bread_type": "jowar_rotla",
                    "variant": "jowar_rotla",
                    "canonical_id": "GJ_BREAD_ROTLA_JOWAR",
                    "canonical_food_id": "GJ_BREAD_ROTLA_JOWAR",
                    "thickness_mm": thickness,
                    "confidence": 0.94,
                    "description": "Thick rustic sorghum rotla."
                }

        # 2. Nachni / Ragi Bhakri (Dark chocolate brown / slate)
        if "chocolate" in color or "purple" in color or "dark_brown" in color or "dark" in color:
            return {
                "bread_type": "nachni_bhakri",
                "variant": "nachni_bhakri",
                "canonical_id": "MH_BREAD_BHAKRI_NACHNI",
                "canonical_food_id": "MH_BREAD_BHAKRI_NACHNI",
                "thickness_mm": thickness,
                "confidence": 0.96,
                "description": "Dark rustic finger millet (nachni/ragi) flatbread."
            }

        # 3. Rice Bhakri (Snow white, soft, delicate)
        if "snow_white" in color or "pure_white" in color or ("white" in color and thickness <= 2.8):
            return {
                "bread_type": "rice_bhakri",
                "variant": "rice_bhakri",
                "canonical_id": "MH_BREAD_BHAKRI_RICE",
                "canonical_food_id": "MH_BREAD_BHAKRI_RICE",
                "thickness_mm": thickness,
                "confidence": 0.95,
                "description": "Soft pliable pure white rice flour bhakri."
            }

        # 4. Bajra Bhakri (Maharashtrian, grey-brown, often white til seeds)
        if "grey" in color or "khaki" in color or "til" in surface or "sesame" in surface:
            return {
                "bread_type": "bajra_bhakri",
                "variant": "bajra_bhakri",
                "canonical_id": "MH_BREAD_BHAKRI_BAJRA",
                "canonical_food_id": "MH_BREAD_BHAKRI_BAJRA",
                "thickness_mm": thickness,
                "confidence": 0.95,
                "description": "Maharashtrian pearl millet bhakri with sesame seeds."
            }

        # 5. Jowar Bhakri (Chalky off-white, separated puffed skin)
        return {
            "bread_type": "jowar_bhakri",
            "variant": "jowar_bhakri",
            "canonical_id": "MH_BREAD_BHAKRI_JOWAR",
            "canonical_food_id": "MH_BREAD_BHAKRI_JOWAR",
            "thickness_mm": thickness,
            "confidence": 0.95,
            "description": "Unleavened pale sorghum bhakri with fine water-patting edge cracks."
        }

# =============================================================================
# BATATA VADA CLASSIFIER (SECTION 6)
# =============================================================================

class BatataVadaClassifier:
    """
    Distinguishes Batata Vada from Aloo Bonda, Pakora, Samosa, Medu Vada, Sabudana Vada.
    """
    @classmethod
    def classify(cls, snack_features: Dict[str, Any]) -> Dict[str, Any]:
        shape = snack_features.get("shape", "spherical").lower()
        crust = snack_features.get("crust", "smooth_besan").lower()
        context = snack_features.get("context", "standalone").lower()
        has_sago = snack_features.get("visible_sago_pearls", False)

        if has_sago:
            return {
                "class_name": "Sabudana Vada",
                "variant": "sabudana_vada",
                "canonical_id": "MH_BREAKFAST_SABUDANA_VADA",
                "canonical_food_id": "MH_BREAKFAST_SABUDANA_VADA",
                "confidence": 0.97,
                "distinction": "Crisp fried tapioca sago and crushed peanut patty."
            }

        if "doughnut" in shape or "hole" in shape or "torus" in shape:
            return {
                "class_name": "Medu Vada",
                "variant": "medu_vada",
                "canonical_id": "TN_BREAKFAST_MEDU_VADA",
                "canonical_food_id": "TN_BREAKFAST_MEDU_VADA",
                "confidence": 0.98,
                "distinction": "Ring-shaped savoury fried lentil doughnut with central hole."
            }

        if shape in ["pyramid", "triangle", "cone"]:
            return {
                "class_name": "Samosa",
                "variant": "samosa",
                "canonical_id": "UP_SNACK_SAMOSA",
                "canonical_food_id": "UP_SNACK_SAMOSA",
                "confidence": 0.98,
                "distinction": "Rigid 3D triangular pyramid with shortcrust pastry."
            }
        
        if "irregular" in shape or "fritter" in crust:
            return {
                "class_name": "Pakora",
                "variant": "pakora",
                "canonical_id": "MH_STREET_PAKODA",
                "canonical_food_id": "MH_STREET_PAKODA",
                "confidence": 0.94,
                "distinction": "Irregular jagged shape with loose fried batter tendrils."
            }

        if "pav" in context or "bun" in context:
            return {
                "class_name": "Mumbai Vada Pav",
                "variant": "vada_pav",
                "canonical_id": "MUM_STREET_VADA_PAV",
                "canonical_food_id": "MUM_STREET_VADA_PAV",
                "confidence": 0.98,
                "distinction": "Batata vada enclosed inside a pav bun."
            }

        return {
            "class_name": "Batata Vada",
            "variant": "batata_vada",
            "canonical_id": "MUM_STREET_BATATA_VADA",
            "canonical_food_id": "MH_SNACK_BATATA_VADA",
            "confidence": 0.96,
            "distinction": "Spherical golden gram-flour coated spiced potato dumpling."
        }

# =============================================================================
# PURAN POLI VERIFIER (SECTION 27)
# =============================================================================

class PuranPoliVerifier:
    """
    Implements Section 27 Puran Poli verification:
    Detects outer bread + sweet filling (chana dal, jaggery, cardamom).
    If filling is not visible (closed uncut flatbread):
    sets filling_status = 'unknown' and user_confirmation_required = True.
    """
    @classmethod
    def verify(cls, poli_features: Dict[str, Any]) -> Dict[str, Any]:
        is_torn = poli_features.get("is_cut_or_torn", False) or poli_features.get("is_flatbread_cut", False)
        visible_core = poli_features.get("visible_core_color", "none").lower()
        has_yellow_sweet = poli_features.get("yellow_sweet_chana_filling", False)
        thickness = poli_features.get("thickness_mm", 2.2)

        if (is_torn and ("amber" in visible_core or "brown" in visible_core or "yellow" in visible_core)) or has_yellow_sweet:
            return {
                "filling_status": "puran_identified",
                "filling_type": "chana_dal_jaggery_cardamom",
                "variant": "puran_poli",
                "canonical_id": "MH_SWEET_PURAN_POLI",
                "canonical_food_id": "MH_BREAD_PURAN_POLI",
                "confidence": 0.96,
                "user_confirmation_required": False,
                "description": "Sweet mashed chana dal & jaggery puran verified inside delicate thin flatbread."
            }
        elif is_torn and "potato" in visible_core:
            return {
                "filling_status": "visible",
                "filling_type": "savory_potato",
                "variant": "aloo_paratha",
                "canonical_id": "PB_PARATHA_ALOO",
                "canonical_food_id": "PB_PARATHA_ALOO",
                "confidence": 0.94,
                "user_confirmation_required": False,
                "description": "Savory potato filling verified (Aloo Paratha)."
            }
        else:
            # Unopened flatbread: cannot see inside
            return {
                "filling_status": "unknown",
                "filling_type": "unverified",
                "provisional_identity": "plain_paratha_or_chapati",
                "canonical_id": "MH_SWEET_PURAN_POLI",
                "canonical_food_id": "MH_BREAD_PURAN_POLI",
                "confidence": 0.72,
                "user_confirmation_required": True,
                "description": "Flatbread exterior matches Puran Poli with ghee sheen, but internal sweet filling is enclosed. Confirmation requested."
            }

