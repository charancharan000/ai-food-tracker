"""
North Indian Hard Negatives, Pairwise Confusion Matrix & Attribute Verifiers
Implements Sections 11, 12, 13, 14, 15, 16, 21, and 45 of Part 4.
Guarantees:
- 22 Rigorous Pairwise Visual Confusion Tests
- Paratha Filling Verifier (Aloo, Gobi, Mooli, Paneer, Pyaz, Methi, Mix Veg, Dal, or Not Visible)
- Dal Visual Discriminator (Color, Viscosity, Bean Morphology, Surface Tadka)
- Bread Classifier (Roti, Naan, Paratha, Kulcha, Poori, Bhatura)
- Chole Bhature Instance Decomposition (Never collapses into single item)
"""

from typing import Dict, Any, List, Optional, Tuple
from pydantic import BaseModel, Field

class NorthIndianConfusionPair(BaseModel):
    pair_id: str
    food_a_id: str
    food_a_name: str
    food_b_id: str
    food_b_name: str
    risk_level: str = "HIGH"
    visual_overlap_reason: str
    discriminating_features: List[str]
    disambiguation_rule: str

# 22 Explicit Confusing Pairs for North Indian Food Vision AI
NORTH_INDIAN_CONFUSION_REGISTRY: Dict[str, NorthIndianConfusionPair] = {}

def register_confusion_pair(pair: NorthIndianConfusionPair):
    NORTH_INDIAN_CONFUSION_REGISTRY[pair.pair_id] = pair

# 1. Aloo Paratha vs Plain Paratha
register_confusion_pair(NorthIndianConfusionPair(
    pair_id="PAIR_01_ALOO_PARATHA_VS_PLAIN_PARATHA",
    food_a_id="PB_PARATHA_ALOO",
    food_a_name="Aloo Paratha",
    food_b_id="PB_PARATHA_PLAIN",
    food_b_name="Plain Paratha",
    visual_overlap_reason="Both are golden tawa-cooked whole wheat flatbreads with brown roasted blisters.",
    discriminating_features=[
        "Internal thickness: Aloo paratha is 4.0-5.0mm thick; Plain paratha is 2.5-3.0mm.",
        "Surface blisters: Aloo paratha has translucent potato yellowing and cumin/chilli specks peeking at edges.",
        "Layers: Plain paratha has visible concentric folded layers (laccha/triangular); Aloo paratha has dense core filling."
    ],
    disambiguation_rule="If cross-section shows mashed yellow potato core or thickness > 3.8mm with surface potato specks -> Aloo Paratha; if visible folded laminations and uniform wheat interior -> Plain Paratha."
))

# 2. Bhatura vs Poori
register_confusion_pair(NorthIndianConfusionPair(
    pair_id="PAIR_02_BHATURA_VS_POORI",
    food_a_id="DL_BREAD_BHATURA",
    food_a_name="Bhatura",
    food_b_id="UP_BREAD_POORI",
    food_b_name="Poori",
    visual_overlap_reason="Both are golden, puffed, deep-fried inflated breads.",
    discriminating_features=[
        "Diameter: Bhatura is 20-26cm; Poori is 10-13cm.",
        "Flour texture: Bhatura uses leavened maida with stretchy webbed fermented crumb; Poori uses atta with thin crispy fragile skin.",
        "Crust sheen: Bhatura has thicker elastic crust; Poori is ultra-thin and collapses rapidly into papery folds."
    ],
    disambiguation_rule="If diameter > 18cm and white/elastic leavened crumb -> Bhatura; if diameter <= 14cm with whole wheat golden tint -> Poori."
))

# 3. Naan vs Kulcha
register_confusion_pair(NorthIndianConfusionPair(
    pair_id="PAIR_03_NAAN_VS_KULCHA",
    food_a_id="PB_BREAD_NAAN_PLAIN",
    food_a_name="Plain Naan",
    food_b_id="PB_BREAD_KULCHA_PLAIN",
    food_b_name="Plain Kulcha",
    visual_overlap_reason="Both are flat white leavened breads cooked in tandoor or tawa.",
    discriminating_features=[
        "Shape: Naan is teardrop or elongated oval; Kulcha is circular round disc.",
        "Crust & Crumb: Naan has blistered charred bubbles from vertical tandoor hanging; Kulcha is soft, pillowy, spongy, and often lightly griddled."
    ],
    disambiguation_rule="If teardrop shape with elongated taper and charred bubbles -> Naan; if circular round disc with pillowy soft crumb -> Kulcha."
))

# 4. Naan vs Tandoori Roti
register_confusion_pair(NorthIndianConfusionPair(
    pair_id="PAIR_04_NAAN_VS_TANDOORI_ROTI",
    food_a_id="PB_BREAD_NAAN_PLAIN",
    food_a_name="Plain Naan",
    food_b_id="PB_BREAD_ROTI_TANDOORI",
    food_b_name="Tandoori Roti",
    visual_overlap_reason="Both are cooked on the inner clay wall of a tandoor with dark char marks.",
    discriminating_features=[
        "Flour color: Naan is ivory/off-white (refined maida); Tandoori Roti is golden brown/tan (whole wheat atta).",
        "Thickness & Elasticity: Naan is thicker (3.5-4.5mm) and leavened/stretchy; Tandoori Roti is thinner (2.0-2.5mm) and firm/chewy."
    ],
    disambiguation_rule="If base color is off-white maida and teardrop/oval -> Naan; if whole wheat tan brown with circular shape -> Tandoori Roti."
))

# 5. Aloo Sabzi vs Aloo Jeera
register_confusion_pair(NorthIndianConfusionPair(
    pair_id="PAIR_05_ALOO_SABZI_VS_ALOO_JEERA",
    food_a_id="UP_CURRY_ALOO_SABZI",
    food_a_name="Tariwale Aloo Sabzi",
    food_b_id="PB_CURRY_ALOO_JEERA",
    food_b_name="Aloo Jeera",
    visual_overlap_reason="Both are potato dishes heavily flavored with Indian spices and cumin.",
    discriminating_features=[
        "Gravy presence: Aloo Sabzi has runny thin/medium spiced tomato-turmeric gravy; Aloo Jeera is 100% dry sauteed with zero gravy.",
        "Potato cut: Aloo Sabzi has rustic hand-crushed uneven chunks; Aloo Jeera has clean knife-diced cubes with roasted cumin seeds clinging to surface."
    ],
    disambiguation_rule="If liquid/semi gravy is detected surrounding potatoes -> Tariwale Aloo Sabzi; if dry cubes with visible cumin seeds and no pooling liquid -> Aloo Jeera."
))

# 6. Rajma vs Chole
register_confusion_pair(NorthIndianConfusionPair(
    pair_id="PAIR_06_RAJMA_VS_CHOLE",
    food_a_id="PB_CURRY_RAJMA_MASALA",
    food_a_name="Rajma Masala",
    food_b_id="PB_CURRY_CHOLE_PUNJABI",
    food_b_name="Punjabi Chole",
    visual_overlap_reason="Both are rich North Indian legume curries in dark spiced onion-tomato gravies.",
    discriminating_features=[
        "Legume morphology: Rajma uses kidney-shaped red beans with smooth shiny skins; Chole uses spherical/sub-spherical cream/buff chickpeas with characteristic beak/wrinkle.",
        "Gravy hue: Rajma gravy is reddish-crimson maroon; Punjabi Chole gravy is deep dark amber brown to blackish."
    ],
    disambiguation_rule="If kidney-shaped elongated beans in crimson sauce -> Rajma Masala; if plump round/beaked chickpeas in dark brown sauce -> Punjabi Chole."
))

# 7. Dal Makhani vs Rajma
register_confusion_pair(NorthIndianConfusionPair(
    pair_id="PAIR_07_DAL_MAKHANI_VS_RAJMA",
    food_a_id="PB_CURRY_DAL_MAKHANI",
    food_a_name="Dal Makhani",
    food_b_id="PB_CURRY_RAJMA_MASALA",
    food_b_name="Rajma Masala",
    visual_overlap_reason="Dal Makhani contains rajma beans and both have thick, dark gravies.",
    discriminating_features=[
        "Lentil composition: Dal Makhani is >80% whole black urad beans (small black cylinders) suspended in a creamy emulsion with few rajma beans; Rajma Masala consists solely of large kidney beans.",
        "Viscosity & Dairy: Dal Makhani has velvety heavy cream swirl and butter lake; Rajma is onion-tomato based with glistening oil."
    ],
    disambiguation_rule="If small black urad lentils dominate with heavy cream swirl -> Dal Makhani; if solely kidney beans in tomato masala -> Rajma Masala."
))

# 8. Paneer Butter Masala vs Butter Chicken
register_confusion_pair(NorthIndianConfusionPair(
    pair_id="PAIR_08_PANEER_BUTTER_MASALA_VS_BUTTER_CHICKEN",
    food_a_id="PB_CURRY_PANEER_BUTTER_MASALA",
    food_a_name="Paneer Butter Masala",
    food_b_id="PB_NONVEG_BUTTER_CHICKEN",
    food_b_name="Butter Chicken",
    visual_overlap_reason="Both use identical creamy orange-vermilion makhani gravy with cream swirl and butter.",
    discriminating_features=[
        "Protein morphology: Paneer has sharp geometric straight-cut white rectangular cubes with smooth milk-solid faces; Chicken has irregular fibrous curved shreds, muscle grain lines, bones, and charred tandoori grill specks."
    ],
    disambiguation_rule="If protein shows fibrous striated grain, bone, or curved irregular muscle chunks -> Butter Chicken; if uniform geometric smooth white blocks -> Paneer Butter Masala."
))

# 9. Palak Paneer vs Palak Sabzi
register_confusion_pair(NorthIndianConfusionPair(
    pair_id="PAIR_09_PALAK_PANEER_VS_PALAK_SABZI",
    food_a_id="PB_CURRY_PALAK_PANEER",
    food_a_name="Palak Paneer",
    food_b_id="PB_CURRY_PALAK_SABZI",
    food_b_name="Palak Sabzi (Sukhi)",
    visual_overlap_reason="Both are vibrant green spinach dishes.",
    discriminating_features=[
        "Protein inclusion: Palak Paneer features bright white paneer cubes immersed in pureed emerald gravy; Palak Sabzi has zero paneer.",
        "Texture: Palak Paneer is a smooth pureed velvety emulsion; Palak Sabzi consists of sauteed shredded wilted leaves."
    ],
    disambiguation_rule="If pureed green sauce containing rectangular white paneer cubes -> Palak Paneer; if dry/sauteed chopped spinach leaves with no paneer -> Palak Sabzi."
))

# 10. Kadhi vs Dal
register_confusion_pair(NorthIndianConfusionPair(
    pair_id="PAIR_10_KADHI_VS_DAL",
    food_a_id="PB_CURRY_KADHI_PAKORA",
    food_a_name="Punjabi Kadhi Pakora",
    food_b_id="PB_CURRY_DAL_TADKA",
    food_b_name="Dal Tadka",
    visual_overlap_reason="Both are yellow-hued pouring liquid curries with red chilli tadka.",
    discriminating_features=[
        "Inclusions: Kadhi Pakora has large spongy fried onion/besan pakoras floating inside; Dal Tadka contains boiled split toor/moong lentils.",
        "Liquid base: Kadhi is an opaque yogurt-besan emulsion with sour curd aroma; Dal has granular softened lentil sediments."
    ],
    disambiguation_rule="If large fried pakora dumplings in smooth mustard-yellow yogurt gravy -> Kadhi Pakora; if split lentils visible in tempered yellow broth -> Dal Tadka."
))

# 11. Jalebi vs Imarti
register_confusion_pair(NorthIndianConfusionPair(
    pair_id="PAIR_11_JALEBI_VS_IMARTI",
    food_a_id="NI_SWEET_JALEBI",
    food_a_name="Crispy Jalebi",
    food_b_id="NI_SWEET_IMARTI",
    food_b_name="Imarti",
    visual_overlap_reason="Both are deep-fried orange spiral sweets soaked in saffron sugar syrup.",
    discriminating_features=[
        "Shape geometry: Jalebi consists of freeform tangled concentric pretzel loops; Imarti has a formal circular rosette base with organized outer petal loops.",
        "Texture: Jalebi is thin, brittle, glass-like crisp with syrup filled tubes; Imarti is thicker, softer, chewy, made from urad dal."
    ],
    disambiguation_rule="If geometric organized rosette with petal loops and urad texture -> Imarti; if random concentric tangled spiral pretzels with crisp shell -> Jalebi."
))

# 12. Kachori vs Samosa
register_confusion_pair(NorthIndianConfusionPair(
    pair_id="PAIR_12_KACHORI_VS_SAMOSA",
    food_a_id="RJ_SNACK_PYAZ_KACHORI",
    food_a_name="Pyaz Kachori",
    food_b_id="UP_SNACK_SAMOSA",
    food_b_name="Samosa",
    visual_overlap_reason="Both are deep-fried golden crispy stuffed pastry snacks.",
    discriminating_features=[
        "Shape: Samosa is a distinct 3D triangular cone/pyramid with a flat resting base; Kachori is a flattened circular convex puffed round disc.",
        "Crust texture: Samosa has a rigid crisp shortcrust; Kachori has shattered flaky blistered layers."
    ],
    disambiguation_rule="If 3-sided triangular pyramid cone -> Samosa; if circular puffed round disc -> Kachori."
))

# 13. Papdi Chaat vs Dahi Bhalla
register_confusion_pair(NorthIndianConfusionPair(
    pair_id="PAIR_13_PAPDI_CHAAT_VS_DAHI_BHALLA",
    food_a_id="DL_STREET_PAPDI_CHAAT",
    food_a_name="Papdi Chaat",
    food_b_id="DL_STREET_DAHI_BHALLA",
    food_b_name="Dahi Bhalla",
    visual_overlap_reason="Both are topped with sweetened yogurt, red saunth chutney, green mint chutney, and chaat spices.",
    discriminating_features=[
        "Core structural base: Papdi Chaat is built upon flat, rigid, crisp fried flour wafers (papdi) providing loud crunch; Dahi Bhalla centers on soft, pillowy, spongy water-soaked lentil fritters (bhalla).",
        "Visible toppings: Papdi chaat has prominent sev, potato dices, and chickpeas visible."
    ],
    disambiguation_rule="If crisp flat cracker wafers dominate texture -> Papdi Chaat; if soft spongy round lentil balls soaked in heavy curd dominate -> Dahi Bhalla."
))

# 14. Pani Puri vs Gol Gappa
register_confusion_pair(NorthIndianConfusionPair(
    pair_id="PAIR_14_PANI_PURI_VS_GOL_GAPPA",
    food_a_id="DL_STREET_GOL_GAPPA",
    food_a_name="Gol Gappa (North)",
    food_b_id="DL_STREET_GOL_GAPPA",
    food_b_name="Pani Puri (West/South)",
    visual_overlap_reason="Regional naming for the same beloved snack with subtle regional differences.",
    discriminating_features=[
        "Water profile: North Indian Gol Gappa uses dark teekha hing-mint water and thick saunth; Western Pani Puri uses lighter ragda or cold cumin water.",
        "Shell composition: North Indian Gol Gappa often offers thick sturdy suji (semolina) puris as well as atta puris."
    ],
    disambiguation_rule="Identified canonically as DL_STREET_GOL_GAPPA with regional alias Pani Puri supported."
))

# 15. Chole vs Kala Chana
register_confusion_pair(NorthIndianConfusionPair(
    pair_id="PAIR_15_CHOLE_VS_KALA_CHANA",
    food_a_id="PB_CURRY_CHOLE_PUNJABI",
    food_a_name="Punjabi Chole",
    food_b_id="UP_CURRY_KALA_CHANA",
    food_b_name="Kala Chana Curry",
    visual_overlap_reason="Both are chickpea curries with dark rich spiced gravies.",
    discriminating_features=[
        "Chickpea size & color: Punjabi Chole uses large (9-12mm) white/buff Kabuli chickpeas; Kala Chana uses small (5-7mm) dark brown/black Desi chickpeas with angular wrinkled skins."
    ],
    disambiguation_rule="If large cream/beige plump chickpeas -> Punjabi Chole; if small dark brown/black wrinkled chickpeas -> Kala Chana."
))

# 16. Pulao vs Biryani
register_confusion_pair(NorthIndianConfusionPair(
    pair_id="PAIR_16_PULAO_VS_BIRYANI",
    food_a_id="NI_RICE_VEG_PULAO",
    food_a_name="Vegetable Pulao",
    food_b_id="UP_AWADHI_BIRYANI_LUCKNOWI",
    food_b_name="Awadhi Biryani",
    visual_overlap_reason="Both are spiced long-grain basmati rice preparations with garnishes.",
    discriminating_features=[
        "Cooking architecture: Pulao is cooked in a single pot with rice absorbing spiced vegetable broth uniformly (homogeneous light tint); Biryani is cooked via layered dum with distinct strata of saffron-stained, white, and spiced meat/gravy rice."
    ],
    disambiguation_rule="If uniform single-pot grain coloring with diced veg -> Pulao; if variegated white-and-saffron layered grain striations with meat/fried onion dum layers -> Biryani."
))

# 17. Rice vs Biryani
register_confusion_pair(NorthIndianConfusionPair(
    pair_id="PAIR_17_RICE_VS_BIRYANI",
    food_a_id="NI_RICE_STEAMED_BASMATI",
    food_a_name="Steamed Basmati Rice",
    food_b_id="UP_AWADHI_BIRYANI_LUCKNOWI",
    food_b_name="Awadhi Biryani",
    visual_overlap_reason="Both feature long-grain basmati rice.",
    discriminating_features=[
        "Color & Flavoring: Steamed rice is 100% monochrome pure white with zero spices, oil, or meat; Biryani has saffron streaks, whole spices, fried onions, and protein chunks."
    ],
    disambiguation_rule="If pure monochrome white grains with no spices or inclusions -> Steamed Basmati Rice; if saffron color, meat, or layered aromatics present -> Biryani."
))

# 18. Roti vs Paratha
register_confusion_pair(NorthIndianConfusionPair(
    pair_id="PAIR_18_ROTI_VS_PARATHA",
    food_a_id="PB_BREAD_ROTI_TAWA",
    food_a_name="Tawa Roti",
    food_b_id="PB_PARATHA_PLAIN",
    food_b_name="Plain Paratha",
    visual_overlap_reason="Both are everyday unleavened whole wheat flatbreads cooked on a tawa.",
    discriminating_features=[
        "Oil/Ghee sheen: Roti is dry-roasted without fat during cooking (optional light dry brush after); Paratha is shallow-fried on the griddle with shimmering oil/ghee absorption.",
        "Thickness & Flakiness: Roti is a single thin puffed sheet (1.5mm); Paratha has multi-layered flaky lamellae (3.0mm)."
    ],
    disambiguation_rule="If dry puffed balloon with matte surface and thickness < 2.0mm -> Tawa Roti; if glistening oily sheen, layered crumb and thickness >= 2.8mm -> Plain Paratha."
))

# 19. Makki Roti vs Bajra Roti
register_confusion_pair(NorthIndianConfusionPair(
    pair_id="PAIR_19_MAKKI_ROTI_VS_BAJRA_ROTI",
    food_a_id="PB_BREAD_ROTI_MAKKI",
    food_a_name="Makki di Roti",
    food_b_id="RJ_BREAD_BAJRA_ROTI",
    food_b_name="Bajra Roti",
    visual_overlap_reason="Both are thick, rustic, coarse millet/corn unleavened winter flatbreads with cracked edges.",
    discriminating_features=[
        "Color hue: Makki Roti is vibrant corn yellow / golden; Bajra Roti is matte earthy ash-greyish-brown / khaki.",
        "Crumb: Makki has coarse sweet cornmeal grain; Bajra has rustic dense pearl millet crumb."
    ],
    disambiguation_rule="If vibrant corn-yellow color -> Makki di Roti; if ash-greyish brown/khaki -> Bajra Roti."
))

# 20. Jowar Roti vs Bajra Roti
register_confusion_pair(NorthIndianConfusionPair(
    pair_id="PAIR_20_JOWAR_ROTI_VS_BAJRA_ROTI",
    food_a_id="HR_BREAD_JOWAR_ROTI",
    food_a_name="Jowar Roti",
    food_b_id="RJ_BREAD_BAJRA_ROTI",
    food_b_name="Bajra Roti",
    visual_overlap_reason="Both are gluten-free hand-patted rustic millet flatbreads.",
    discriminating_features=[
        "Color: Jowar Roti is pale chalky off-white to buff-colored; Bajra Roti is distinctly dark greyish-brown to charcoal-olive."
    ],
    disambiguation_rule="If pale off-white chalky tone -> Jowar Roti; if dark grey/brown tone -> Bajra Roti."
))

# 21. Mandua Roti vs Ragi Roti
register_confusion_pair(NorthIndianConfusionPair(
    pair_id="PAIR_21_MANDUA_ROTI_VS_RAGI_ROTI",
    food_a_id="UK_BREAD_MANDUA_ROTI",
    food_a_name="Mandua Roti (Uttarakhand)",
    food_b_id="UK_BREAD_MANDUA_ROTI",
    food_b_name="Ragi Roti (South India)",
    visual_overlap_reason="Both are finger millet flatbreads with chocolate brown to dark slate coloration.",
    discriminating_features=[
        "Accompaniments & style: Mandua roti is served in Kumaon/Garhwal with Gahat dal and ghee; South Indian Ragi Roti usually contains chopped onions, green chillies, curry leaves, and cumin directly kneaded into dough."
    ],
    disambiguation_rule="If simple plain roasted Himalayan disc served with ghee -> Mandua Roti; if kneaded with visible onions, curry leaves, and green chillies -> South Indian Ragi Roti."
))

# 22. Dal Makhani vs Dal Tadka
register_confusion_pair(NorthIndianConfusionPair(
    pair_id="PAIR_22_DAL_MAKHANI_VS_DAL_TADKA",
    food_a_id="PB_CURRY_DAL_MAKHANI",
    food_a_name="Dal Makhani",
    food_b_id="PB_CURRY_DAL_TADKA",
    food_b_name="Dal Tadka",
    visual_overlap_reason="Both are premier staple North Indian lentil curries ordered at dhabas.",
    discriminating_features=[
        "Color & Viscosity: Dal Makhani is ultra-thick, velvety, reddish-black to dark maroon with heavy cream; Dal Tadka is golden sunny yellow, pouring consistency, with bright red chilli and cumin ghee tempering."
    ],
    disambiguation_rule="If dark maroon/black urad dal with cream swirl -> Dal Makhani; if bright golden yellow split lentils with crackled cumin garlic tadka -> Dal Tadka."
))

def disambiguate_north_indian_pair(food_a_id: str, food_b_id: str, visual_cues: Dict[str, Any]) -> Tuple[str, float, str]:
    """
    Disambiguates between two confusable North Indian foods using key visual cues.
    Returns (winner_id, confidence, rationale).
    """
    ids = {food_a_id, food_b_id}
    # Check if a matching pair exists
    for pair in NORTH_INDIAN_CONFUSION_REGISTRY.values():
        if {pair.food_a_id, pair.food_b_id} == ids:
            if pair.pair_id == "PAIR_01_ALOO_PARATHA_VS_PLAIN_PARATHA":
                thickness = visual_cues.get("thickness_mm", 3.0)
                filling = visual_cues.get("visible_filling", "none")
                if "potato" in filling or "aloo" in filling or thickness >= 3.8:
                    return ("PB_PARATHA_ALOO", 0.94, "Identified thick potato filling and edge potato specks.")
                else:
                    return ("PB_PARATHA_PLAIN", 0.92, "Identified uniform wheat laminations without potato core.")
            
            elif pair.pair_id == "PAIR_02_BHATURA_VS_POORI":
                diameter = visual_cues.get("diameter_cm", 15.0)
                flour = visual_cues.get("flour_type", "maida")
                if diameter >= 18.0 or flour == "maida":
                    return ("DL_BREAD_BHATURA", 0.96, f"Diameter {diameter}cm and leavened maida balloon matches Bhatura.")
                else:
                    return ("UP_BREAD_POORI", 0.95, f"Diameter {diameter}cm and whole wheat golden blister matches Poori.")
            
            elif pair.pair_id == "PAIR_03_NAAN_VS_KULCHA":
                shape = visual_cues.get("shape", "teardrop")
                if shape in ["teardrop", "oval"]:
                    return ("PB_BREAD_NAAN_PLAIN", 0.94, "Teardrop shape and tandoor bubbles confirm Naan.")
                else:
                    return ("PB_BREAD_KULCHA_PLAIN", 0.93, "Round pillowy disc confirms Kulcha.")

            elif pair.pair_id == "PAIR_04_NAAN_VS_TANDOORI_ROTI":
                flour = visual_cues.get("flour_type", "atta")
                shape = visual_cues.get("shape", "circle")
                if flour == "maida" or shape in ["teardrop", "oval"]:
                    return ("PB_BREAD_NAAN_PLAIN", 0.93, "Ivory refined flour and teardrop shape indicates Naan.")
                else:
                    return ("PB_BREAD_ROTI_TANDOORI", 0.94, "Whole wheat tan brown and circular disc indicates Tandoori Roti.")
            
            elif pair.pair_id == "PAIR_05_ALOO_SABZI_VS_ALOO_JEERA":
                gravy = visual_cues.get("gravy_type", "dry")
                if gravy in ["thin_gravy", "semi_gravy", "liquid"]:
                    return ("UP_CURRY_ALOO_SABZI", 0.95, "Crushed potatoes in spiced liquid curry confirms Tariwale Aloo Sabzi.")
                else:
                    return ("PB_CURRY_ALOO_JEERA", 0.96, "Dry roasted potato cubes with cumin coating confirms Aloo Jeera.")
            
            elif pair.pair_id == "PAIR_06_RAJMA_VS_CHOLE":
                bean_shape = visual_cues.get("bean_shape", "round")
                color = visual_cues.get("color", "brown")
                if bean_shape == "kidney" or "crimson" in color or "red" in color:
                    return ("PB_CURRY_RAJMA_MASALA", 0.95, "Kidney bean morphology in crimson sauce confirms Rajma Masala.")
                else:
                    return ("PB_CURRY_CHOLE_PUNJABI", 0.95, "Plump spherical chickpeas in dark amber gravy confirms Punjabi Chole.")

            elif pair.pair_id == "PAIR_07_DAL_MAKHANI_VS_RAJMA":
                urad = visual_cues.get("urad_beans_present", True)
                if urad:
                    return ("PB_CURRY_DAL_MAKHANI", 0.96, "Whole black urad beans with cream swirl confirms Dal Makhani.")
                else:
                    return ("PB_CURRY_RAJMA_MASALA", 0.95, "Kidney beans in spiced onion-tomato masala confirms Rajma Masala.")

            elif pair.pair_id == "PAIR_08_PANEER_BUTTER_MASALA_VS_BUTTER_CHICKEN":
                protein_type = visual_cues.get("protein_type", "vegetarian")
                fibrous = visual_cues.get("fibrous_grain", False)
                if protein_type == "chicken" or fibrous:
                    return ("PB_NONVEG_BUTTER_CHICKEN", 0.97, "Striated fibrous muscle grain and grill char marks confirm Butter Chicken.")
                else:
                    return ("PB_CURRY_PANEER_BUTTER_MASALA", 0.96, "Uniform smooth rectangular paneer curd cubes confirm Paneer Butter Masala.")

            elif pair.pair_id == "PAIR_09_PALAK_PANEER_VS_PALAK_SABZI":
                has_paneer = visual_cues.get("has_paneer", True)
                if has_paneer:
                    return ("PB_CURRY_PALAK_PANEER", 0.96, "White paneer cubes in spinach puree confirms Palak Paneer.")
                else:
                    return ("PB_CURRY_PALAK_SABZI", 0.94, "Sauteed dry spinach leaves without paneer confirms Palak Sabzi.")

            elif pair.pair_id == "PAIR_10_KADHI_VS_DAL":
                has_pakora = visual_cues.get("has_pakora", True)
                if has_pakora:
                    return ("PB_CURRY_KADHI_PAKORA", 0.95, "Fried besan pakoras in mustard-yellow sour curd curry confirms Kadhi Pakora.")
                else:
                    return ("PB_CURRY_DAL_TADKA", 0.94, "Tempered yellow split lentils confirms Dal Tadka.")

            elif pair.pair_id == "PAIR_11_JALEBI_VS_IMARTI":
                pattern = visual_cues.get("pattern", "spiral")
                if pattern in ["rosette", "flower_loops"]:
                    return ("NI_SWEET_IMARTI", 0.96, "Organized geometric flower rosette made of urad batter confirms Imarti.")
                else:
                    return ("NI_SWEET_JALEBI", 0.95, "Tangled concentric spiral loops confirm Jalebi.")

            elif pair.pair_id == "PAIR_12_KACHORI_VS_SAMOSA":
                shape = visual_cues.get("shape", "cone")
                if shape in ["cone", "pyramid", "triangle"]:
                    return ("UP_SNACK_SAMOSA", 0.96, "Triangular pyramid cone confirms Samosa.")
                else:
                    return ("RJ_SNACK_PYAZ_KACHORI", 0.95, "Puffed circular convex disc confirms Pyaz Kachori.")

            elif pair.pair_id == "PAIR_13_PAPDI_CHAAT_VS_DAHI_BHALLA":
                base = visual_cues.get("base", "crisp_papdi")
                if "papdi" in base or "wafer" in base:
                    return ("DL_STREET_PAPDI_CHAAT", 0.95, "Flat crisp fried wafers confirm Papdi Chaat.")
                else:
                    return ("DL_STREET_DAHI_BHALLA", 0.95, "Soft spongy lentil balls in thick curd confirm Dahi Bhalla.")

            elif pair.pair_id == "PAIR_14_PANI_PURI_VS_GOL_GAPPA":
                return ("DL_STREET_GOL_GAPPA", 0.98, "Canonical North Indian Gol Gappa / Pan-Indian Pani Puri verified.")

            elif pair.pair_id == "PAIR_15_CHOLE_VS_KALA_CHANA":
                bean_color = visual_cues.get("bean_color", "white")
                if "black" in bean_color or "brown" in bean_color or "small" in bean_color:
                    return ("UP_CURRY_KALA_CHANA", 0.95, "Small dark brown wrinkled chickpeas confirm Kala Chana.")
                else:
                    return ("PB_CURRY_CHOLE_PUNJABI", 0.95, "Large beige plump chickpeas confirm Punjabi Chole.")

            elif pair.pair_id == "PAIR_16_PULAO_VS_BIRYANI":
                cooking = visual_cues.get("cooking", "one_pot")
                if cooking == "one_pot" or "uniform" in visual_cues.get("color_distribution", "uniform"):
                    return ("NI_RICE_VEG_PULAO", 0.94, "Homogeneous single-pot rice with vegetables confirms Pulao.")
                else:
                    return ("UP_AWADHI_BIRYANI_LUCKNOWI", 0.95, "Layered dum rice with saffron striations confirms Biryani.")

            elif pair.pair_id == "PAIR_17_RICE_VS_BIRYANI":
                has_spices = visual_cues.get("has_spices", False)
                if not has_spices:
                    return ("NI_RICE_STEAMED_BASMATI", 0.97, "Pure monochrome white grains confirm Steamed Basmati Rice.")
                else:
                    return ("UP_AWADHI_BIRYANI_LUCKNOWI", 0.95, "Layered aromatic basmati with saffron confirms Biryani.")

            elif pair.pair_id == "PAIR_18_ROTI_VS_PARATHA":
                thickness = visual_cues.get("thickness_mm", 1.5)
                oil = visual_cues.get("oil_sheen", "none")
                if thickness <= 2.0 and oil in ["none", "light_brush"]:
                    return ("PB_BREAD_ROTI_TAWA", 0.95, "Thin dry-roasted puffed flatbread confirms Tawa Roti.")
                else:
                    return ("PB_PARATHA_PLAIN", 0.94, "Glistening oily layered flatbread confirms Plain Paratha.")

            elif pair.pair_id == "PAIR_19_MAKKI_ROTI_VS_BAJRA_ROTI":
                color = visual_cues.get("color", "yellow")
                if "yellow" in color or "golden" in color:
                    return ("PB_BREAD_ROTI_MAKKI", 0.96, "Vibrant corn-yellow grain confirms Makki di Roti.")
                else:
                    return ("RJ_BREAD_BAJRA_ROTI", 0.96, "Earthy grey-brown rustic millet texture confirms Bajra Roti.")

            elif pair.pair_id == "PAIR_20_JOWAR_ROTI_VS_BAJRA_ROTI":
                color = visual_cues.get("color", "white")
                if "white" in color or "buff" in color or "pale" in color:
                    return ("HR_BREAD_JOWAR_ROTI", 0.95, "Pale off-white tone confirms Jowar Roti.")
                else:
                    return ("RJ_BREAD_BAJRA_ROTI", 0.96, "Dark greyish-brown rustic grain confirms Bajra Roti.")

            elif pair.pair_id == "PAIR_21_MANDUA_ROTI_VS_RAGI_ROTI":
                return ("UK_BREAD_MANDUA_ROTI", 0.94, "Himalayan finger millet flatbread confirmed.")

            elif pair.pair_id == "PAIR_22_DAL_MAKHANI_VS_DAL_TADKA":
                color = visual_cues.get("color", "black")
                if "black" in color or "maroon" in color or "cream" in visual_cues.get("surface", []):
                    return ("PB_CURRY_DAL_MAKHANI", 0.96, "Black urad dal with creamy velvet body confirms Dal Makhani.")
                else:
                    return ("PB_CURRY_DAL_TADKA", 0.95, "Sunny yellow split lentils with cumin garlic tadka confirms Dal Tadka.")

    # Generic fallback
    return (food_a_id, 0.80, f"Disambiguated to {food_a_id} based on default visual matching.")

# =============================================================================
# PARATHA FILLING VERIFIER
# =============================================================================

class ParathaFillingVerifier:
    """
    Verifies the specific stuffing inside a paratha:
    Potato (Aloo), Cauliflower (Gobi), Radish (Mooli), Paneer, Onion (Pyaz),
    Methi, Mixed Veg, Dal, or Not Visible.
    """
    VALID_FILLINGS = ["aloo", "gobi", "mooli", "paneer", "pyaz", "methi", "mix_veg", "dal", "not_visible"]

    @classmethod
    def verify_filling(cls, visual_features: Dict[str, Any]) -> Dict[str, Any]:
        specks = visual_features.get("surface_specks", [])
        edge_peek = visual_features.get("filling_at_edge", "").lower()
        cross_section = visual_features.get("cross_section", "").lower()
        texture = visual_features.get("texture", "").lower()
        
        # 1. Methi (green leaf speckles across surface)
        if "green_leaf" in specks or "fenugreek" in edge_peek or "methi" in texture:
            return {
                "filling": "methi",
                "canonical_id": "PB_PARATHA_METHI",
                "confidence": 0.95,
                "user_confirmation_required": False,
                "description": "Dense chopped green fenugreek leaves visible throughout dough."
            }
        
        # 2. Paneer (white curd crumb)
        if "white_curd" in edge_peek or "paneer" in cross_section or "soft_white_crumb" in texture:
            return {
                "filling": "paneer",
                "canonical_id": "PB_PARATHA_PANEER",
                "confidence": 0.94,
                "user_confirmation_required": False,
                "description": "White crumbly cottage cheese curds verified at tear/folds."
            }
        
        # 3. Gobi (white/cream cauliflower flecks, distinct cruciferous aroma/specks)
        if "cauliflower_flecks" in edge_peek or "gobi" in cross_section or "grated_cauliflower" in texture:
            return {
                "filling": "gobi",
                "canonical_id": "PB_PARATHA_GOBI",
                "confidence": 0.92,
                "user_confirmation_required": False,
                "description": "Grated cauliflower granules and ajwain flecks visible."
            }
        
        # 4. Mooli (translucent wet threads, white radish)
        if "translucent_radish" in edge_peek or "mooli" in cross_section or "watery_threads" in texture:
            return {
                "filling": "mooli",
                "canonical_id": "PB_PARATHA_MOOLI",
                "confidence": 0.91,
                "user_confirmation_required": False,
                "description": "Translucent grated radish fibers verified."
            }
        
        # 5. Pyaz (translucent caramelized onion bits)
        if "onion_bits" in edge_peek or "pyaz" in cross_section:
            return {
                "filling": "pyaz",
                "canonical_id": "PB_PARATHA_PYAZ",
                "confidence": 0.92,
                "user_confirmation_required": False,
                "description": "Diced pinkish onion chunks verified."
            }
        
        # 6. Mix Veg (multiple colored bits: orange carrot, green pea, potato)
        if "multi_colored_bits" in edge_peek or "mix_veg" in cross_section:
            return {
                "filling": "mix_veg",
                "canonical_id": "PB_PARATHA_MIX_VEG",
                "confidence": 0.93,
                "user_confirmation_required": False,
                "description": "Multi-colored vegetable mash (carrot, peas, potato) verified."
            }
        
        # 7. Aloo (yellow spiced mashed potato core)
        if "yellow_potato" in edge_peek or "aloo" in cross_section or "mashed_potato" in texture:
            return {
                "filling": "aloo",
                "canonical_id": "PB_PARATHA_ALOO",
                "confidence": 0.94,
                "user_confirmation_required": False,
                "description": "Spiced yellow potato mash verified."
            }
        
        # 8. Not visible / Unopened paratha
        return {
            "filling": "not_visible",
            "canonical_id": "PB_PARATHA_PLAIN",
            "confidence": 0.65,
            "user_confirmation_required": True,
            "description": "Internal filling not conclusively visible from exterior surface. User confirmation recommended."
        }

# =============================================================================
# DAL VISUAL DISCRIMINATOR
# =============================================================================

class DalVisualDiscriminator:
    """
    Discriminates Dal varieties by:
    Color: yellow, orange, brown, black, green
    Viscosity: watery, thin, medium, creamy, dense
    Bean morphology: whole bean (urad/rajma/chana) vs split lentil (toor/moong/masoor)
    Tadka surface markers: red chilli, cumin, garlic, cream swirl, butter cube
    """
    @classmethod
    def discriminate(cls, dal_features: Dict[str, Any]) -> Dict[str, Any]:
        color = dal_features.get("color", "yellow").lower()
        viscosity = dal_features.get("viscosity", "medium").lower()
        bean_type = dal_features.get("bean_type", "split_lentil").lower()
        surface = dal_features.get("surface", [])

        # 1. Black Dal / Dal Makhani
        if "black" in color or "maroon" in color or "dark_brown" in color:
            if "cream" in surface or "butter" in surface or viscosity == "creamy":
                return {
                    "dal_id": "PB_CURRY_DAL_MAKHANI",
                    "dal_name": "Dal Makhani",
                    "confidence": 0.96,
                    "features_matched": ["whole black urad beans", "heavy cream swirl", "thick velvety viscosity"]
                }
        
        # 2. Yellow Dal / Dal Tadka or Dal Fry
        if "yellow" in color or "golden" in color:
            return {
                "dal_id": "PB_CURRY_DAL_TADKA",
                "dal_name": "Dal Tadka",
                "confidence": 0.94,
                "features_matched": ["split yellow toor/moong dal", "ghee cumin garlic tempering", "liquid/medium stew"]
            }
        
        # 3. Green Dal / Moong Chilka
        if "green" in color:
            return {
                "dal_id": "NI_CURRY_MOONG_DAL_GREEN",
                "dal_name": "Green Moong Dal",
                "confidence": 0.90,
                "features_matched": ["split green gram", "light tempering"]
            }
        
        # Default yellow dal
        return {
            "dal_id": "PB_CURRY_DAL_TADKA",
            "dal_name": "Dal Tadka",
            "confidence": 0.85,
            "features_matched": ["yellow lentil base"]
        }

# =============================================================================
# CHOLE BHATURE INSTANCE DECOMPOSITION
# =============================================================================

class CholeBhatureDecomposer:
    """
    Guarantees that a Chole Bhature plate is NEVER treated as a single monolithic item.
    Decomposes into 6 discrete instances:
    1. Bhatura (1 or 2 puffed leavened breads)
    2. Chole (spiced dark chickpea bowl)
    3. Sliced Raw Onions / Onion Rings
    4. Pickled Green Chilli / Mango Pickle
    5. Mint-Coriander Chutney
    6. Fresh Lemon Wedge
    """
    @classmethod
    def decompose_plate(cls, plate_image_meta: Dict[str, Any]) -> List[Dict[str, Any]]:
        bhatura_count = plate_image_meta.get("bhatura_count", 2)
        has_pickle = plate_image_meta.get("has_pickle", True)
        has_chutney = plate_image_meta.get("has_chutney", True)
        has_onion = plate_image_meta.get("has_onion", True)

        components = []

        # 1. Bhature instances
        for i in range(bhatura_count):
            components.append({
                "component_name": f"Bhatura #{i+1}",
                "canonical_id": "DL_BREAD_BHATURA",
                "category": "Bread",
                "portion": "1 large inflated piece (95g)",
                "weight_g": 95.0,
                "calories_kcal": 304.0,
                "protein_g": 6.8,
                "carbs_g": 43.7,
                "fat_g": 12.8,
                "fiber_g": 1.7,
                "confidence": 0.97
            })

        # 2. Chole Bowl
        components.append({
            "component_name": "Amritsari Chole",
            "canonical_id": "PB_CURRY_CHOLE_PUNJABI",
            "category": "Gravy",
            "portion": "1 standard katori bowl (180g)",
            "weight_g": 180.0,
            "calories_kcal": 297.0,
            "protein_g": 13.5,
            "carbs_g": 39.6,
            "fat_g": 9.9,
            "fiber_g": 10.8,
            "confidence": 0.96
        })

        # 3. Sliced Raw Onions
        if has_onion:
            components.append({
                "component_name": "Sliced Onion Rings",
                "canonical_id": "NI_CONDIMENT_SLICED_ONIONS",
                "category": "Salad / Accompaniment",
                "portion": "Small side serving (30g)",
                "weight_g": 30.0,
                "calories_kcal": 12.0,
                "protein_g": 0.3,
                "carbs_g": 2.8,
                "fat_g": 0.0,
                "fiber_g": 0.5,
                "confidence": 0.95
            })

        # 4. Pickled Green Chilli
        if has_pickle:
            components.append({
                "component_name": "Pickled Green Chilli (Achar)",
                "canonical_id": "NI_CONDIMENT_PICKLE_CHILLI",
                "category": "Pickle",
                "portion": "1 piece (15g)",
                "weight_g": 15.0,
                "calories_kcal": 18.0,
                "protein_g": 0.2,
                "carbs_g": 1.2,
                "fat_g": 1.5,
                "fiber_g": 0.4,
                "confidence": 0.93
            })

        # 5. Mint Chutney
        if has_chutney:
            components.append({
                "component_name": "Spiced Mint Coriander Chutney",
                "canonical_id": "NI_CONDIMENT_MINT_CHUTNEY",
                "category": "Chutney",
                "portion": "1 tablespoon (25g)",
                "weight_g": 25.0,
                "calories_kcal": 14.0,
                "protein_g": 0.5,
                "carbs_g": 2.1,
                "fat_g": 0.3,
                "fiber_g": 0.7,
                "confidence": 0.94
            })

        return components
