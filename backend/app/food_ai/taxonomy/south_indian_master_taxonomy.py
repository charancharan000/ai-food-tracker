"""
South Indian Food Master Taxonomy
Comprehensive hierarchical knowledge base covering Tamil Nadu, Kerala, Karnataka,
Andhra Pradesh, Telangana, and Puducherry.
Provides deep visual signatures, vessel classifications, portion distributions,
and honest uncertainty handling to prevent incorrect confident predictions.
"""

from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field

class SouthIndianDishProfile(BaseModel):
    dish_name: str
    region: str # Tamil Nadu, Kerala, Karnataka, Andhra Pradesh, Telangana, Puducherry
    meal_type: str # Breakfast, Lunch, Tiffin, Dinner, Snack, Sweet
    category: str # Idli, Dosa, Vada, Pongal, Upma, Rice, Biryani, Bread, Curry, Side Dish, Condiment, Sweet, Snack
    variants: List[str] = Field(default_factory=list)
    cooking_methods: List[str] = Field(default_factory=list)
    food_states: List[str] = Field(default_factory=list)
    primary_ingredients: List[str] = Field(default_factory=list)
    visual_signature: Dict[str, Any] = Field(default_factory=dict)
    distinguishing_features: List[str] = Field(default_factory=list)
    confusing_counterparts: List[str] = Field(default_factory=list)
    typical_serving_vessel: List[str] = Field(default_factory=list)
    typical_portion_weights_g: Dict[str, float] = Field(default_factory=dict) # small, medium, large
    calories_per_100g: float
    protein_per_100g: float
    carbs_per_100g: float
    fat_per_100g: float
    fiber_per_100g: float = 0.0
    sodium_per_100g: float = 0.0
    uncertain_fallback_label: str

SOUTH_INDIAN_REGIONAL_BRANCHES: List[str] = [
    "Tamil Nadu",
    "Kerala",
    "Karnataka",
    "Andhra Pradesh",
    "Telangana",
    "Puducherry"
]

# =====================================================================
# 1. IDLI MASTER DATASET (25+ classes)
# =====================================================================
IDLI_MASTER_CLASSES: List[str] = [
    "plain idli",
    "soft idli",
    "mini idli",
    "button idli",
    "kanchipuram idli",
    "rava idli",
    "thatte idli",
    "mallige idli",
    "millet idli",
    "ragi idli",
    "oats idli",
    "vegetable idli",
    "carrot idli",
    "beetroot idli",
    "podi idli",
    "ghee podi idli",
    "fried idli",
    "chilli idli",
    "masala idli",
    "stuffed idli",
    "instant idli",
    "brown rice idli",
    "red rice idli",
    "black rice idli",
    "multigrain idli",
]

IDLI_VISUAL_DISCRIMINATION: Dict[str, Dict[str, Any]] = {
    "plain idli": {
        "color": "Brilliant white to ivory",
        "diameter_cm": (7.0, 8.5),
        "thickness_cm": (2.0, 2.8),
        "texture": "Spongy, micro-porous surface from yeast/bacterial fermentation",
        "confusing_pairs": ["rava idli", "dhokla", "appam", "paniyaram", "steamed rice cake", "modak", "white bun"],
        "fallback_label": "Idli detected; exact variant uncertain"
    },
    "rava idli": {
        "color": "Creamy beige / pale golden with visible mustard seeds, green chilli bits, cashew nut half on top",
        "diameter_cm": (7.5, 9.0),
        "thickness_cm": (2.2, 3.0),
        "texture": "Granular semolina crumb, slightly denser than rice idli",
        "confusing_pairs": ["plain idli", "dhokla"],
        "fallback_label": "Idli detected; exact variant uncertain"
    },
    "thatte idli": {
        "color": "Soft white",
        "diameter_cm": (12.0, 15.0),
        "thickness_cm": (1.2, 1.8),
        "texture": "Plate-sized flat disk steamed in shallow traditional plates",
        "serving_style": "Served topped with a dollop of butter or spiced podi",
        "fallback_label": "Idli detected; exact variant uncertain"
    },
    "mini idli": {
        "color": "White or podi-coated",
        "diameter_cm": (2.5, 3.5),
        "thickness_cm": (1.0, 1.5),
        "texture": "Bite-sized rounded disks, typically served 14-20 pieces immersed in a bowl of sambar",
        "fallback_label": "Mini Idli detected"
    },
    "podi idli": {
        "color": "Dark brick-red / orange-brown coated",
        "texture": "Glistening spicy dry chutney powder (gunpowder) adhered with warm ghee or sesame oil",
        "fallback_label": "Podi Idli detected"
    }
}

# =====================================================================
# 2. SAMBAR MASTER DATASET (17+ classes)
# =====================================================================
SAMBAR_MASTER_CLASSES: List[str] = [
    "sambar",
    "tiffin sambar",
    "hotel sambar",
    "home-style sambar",
    "mini idli sambar",
    "sambar with vegetables",
    "drumstick sambar",
    "onion sambar",
    "shallot sambar",
    "brinjal sambar",
    "pumpkin sambar",
    "radish sambar",
    "carrot sambar",
    "mixed vegetable sambar",
    "arachuvitta sambar",
    "keerai sambar",
    "instant sambar",
]

SAMBAR_SITUATIONAL_CONTEXTS: List[str] = [
    "inside separate steel katori bowl",
    "inside ceramic bowl",
    "poured over idlis in a shallow bowl (sambar idli)",
    "poured in section of compartmentalized thali plate",
    "poured on fresh banana leaf",
    "mixed with hot white rice",
    "dipped with crispy medu vada (sambar vada)",
    "served beside dosa on plate"
]

# =====================================================================
# 3. CHUTNEY MASTER DATASET (32+ classes)
# =====================================================================
CHUTNEY_MASTER_CLASSES: List[str] = [
    "coconut chutney",
    "white coconut chutney",
    "red coconut chutney",
    "green coconut chutney",
    "mint chutney",
    "pudina chutney",
    "coriander chutney",
    "green chutney",
    "tomato chutney",
    "red tomato chutney",
    "onion tomato chutney",
    "onion chutney",
    "shallot chutney",
    "garlic chutney",
    "ginger chutney",
    "peanut chutney",
    "groundnut chutney",
    "sesame chutney",
    "ellu chutney",
    "curry leaf chutney",
    "karuvepillai chutney",
    "pudina coconut chutney",
    "peanut coconut chutney",
    "spicy chutney",
    "kaara chutney",
    "milagai chutney",
    "podi",
    "idli podi",
    "gunpowder",
    "curry leaf podi",
    "sesame podi",
    "peanut podi",
]

CHUTNEY_AMBIGUITY_RULES: Dict[str, str] = {
    "white_chutney_insufficient_evidence": "White chutney detected; exact type uncertain (Coconut vs Peanut/Sesame)",
    "green_chutney_insufficient_evidence": "Green chutney detected; exact type uncertain (Mint vs Coriander vs Coconut Green)",
    "red_chutney_insufficient_evidence": "Red chutney detected; exact type uncertain (Tomato vs Onion Chilli vs Kaara)",
    "podi_insufficient_evidence": "Spiced Podi detected (Gunpowder); oil/ghee status observed"
}

# =====================================================================
# 4. DOSA MASTER DATASET (32+ classes)
# =====================================================================
DOSA_MASTER_CLASSES: List[str] = [
    "plain dosa",
    "crispy dosa",
    "soft dosa",
    "paper dosa",
    "set dosa",
    "kal dosa",
    "rava dosa",
    "onion rava dosa",
    "masala dosa",
    "ghee roast",
    "ghee dosa",
    "ghee masala dosa",
    "onion dosa",
    "tomato dosa",
    "podi dosa",
    "ghee podi dosa",
    "Mysore masala dosa",
    "cheese dosa",
    "paneer dosa",
    "chicken dosa",
    "egg dosa",
    "butter dosa",
    "neer dosa",
    "adai dosa",
    "millet dosa",
    "ragi dosa",
    "oats dosa",
    "wheat dosa",
    "brown rice dosa",
    "pesarattu",
    "moong dal dosa",
    "appam-style dosa",
]

DOSA_VISUAL_RULES: Dict[str, Dict[str, Any]] = {
    "plain dosa": {
        "shape": "Rolled cylinder or half-fold",
        "thickness": "Thin (1-2mm)",
        "surface": "Golden-brown circular roasting swirls, no filling inside",
        "distinctions": ["plain dosa != paper dosa", "plain dosa != ghee roast", "plain dosa != neer dosa", "dosa != crepe"]
    },
    "masala dosa": {
        "shape": "Folded envelope or rolled cylinder",
        "filling": "Yellow turmeric potato masala visibly nested or bulging inside",
        "distinctions": ["masala dosa != plain dosa with chutney", "masala dosa != Mysore masala dosa (red paste lining)"]
    },
    "rava dosa": {
        "shape": "Very wide, brittle net-like lacy structure",
        "surface": "Prominent holes/pores across entire surface, studded with black peppercorns, cumin, green chillies",
        "distinctions": ["rava dosa != normal dosa", "onion rava has caramelized translucent onions embedded in mesh"]
    },
    "neer dosa": {
        "shape": "Folded into delicate soft triangles",
        "color": "Snow white, paper-thin, unroasted (no golden browning)",
        "distinctions": ["neer dosa != plain dosa", "neer dosa != appam"]
    },
    "pesarattu": {
        "shape": "Flat crepe",
        "color": "Earthy olive-green to greenish-brown from whole green gram moong dal",
        "filling": "Often stuffed with cooked rava upma (MLA Pesarattu)",
        "distinctions": ["pesarattu != normal dosa"]
    }
}

# =====================================================================
# 5. VADA MASTER DATASET (14 classes)
# =====================================================================
VADA_MASTER_CLASSES: List[str] = [
    "medu vada",
    "ulundhu vada",
    "paruppu vada",
    "masala vada",
    "dal vada",
    "keerai vada",
    "thayir vada",
    "sambar vada",
    "curd vada",
    "rasa vada",
    "milagai vada",
    "banana vada",
    "chicken vada",
    "sweet vada",
]

VADA_DISCRIMINATION_RULES: Dict[str, Dict[str, Any]] = {
    "medu vada": {
        "geometry": "Toroidal donut shape with central hole",
        "exterior": "Crisp golden-brown skin with fine bubbling",
        "interior": "Fluffy white urad dal crumb with embedded peppercorns and curry leaves",
        "distinctions": ["medu vada != bonda (bonda has no hole)", "medu vada != pakoda", "vada != sweet doughnut"]
    },
    "masala vada / paruppu vada": {
        "geometry": "Flat circular rough patty without central hole",
        "exterior": "Crunchy coarse texture with visible halved chana dal pieces, fennel seeds, chopped red chillies",
        "color": "Dark golden-brown to deep rustic brown",
        "distinctions": ["paruppu vada != medu vada"]
    }
}

# =====================================================================
# 6. PONGAL & UPMA MASTER DATASETS
# =====================================================================
PONGAL_MASTER_CLASSES: List[str] = [
    "ven pongal",
    "ghee pongal",
    "millet pongal",
    "rava pongal",
    "sweet pongal",
    "sakkarai pongal",
    "chakkarai pongal",
    "kovil pongal",
    "pepper pongal",
]

UPMA_MASTER_CLASSES: List[str] = [
    "rava upma",
    "vegetable upma",
    "semiya upma",
    "vermicelli upma",
    "rice upma",
    "aval upma",
    "millet upma",
    "oats upma",
    "bread upma",
    "tomato upma",
]

# =====================================================================
# 7. POORI / PAROTTA / KOTHU PAROTTA & ROTI
# =====================================================================
POORI_MASTER_CLASSES: List[str] = [
    "plain poori",
    "masala poori",
    "puri",
    "chola poori",
    "bhatura",
]

PAROTTA_MASTER_CLASSES: List[str] = [
    "plain parotta",
    "coin parotta",
    "mini parotta",
    "wheat parotta",
    "malabar parotta",
    "kerala parotta",
    "kothu parotta",
    "egg kothu parotta",
    "chicken kothu parotta",
    "mutton kothu parotta",
    "chilli parotta",
    "cheese parotta",
]

KOTHU_PAROTTA_SPECIAL_CLASSES: List[str] = [
    "plain kothu parotta",
    "egg kothu parotta",
    "chicken kothu parotta",
    "mutton kothu parotta",
    "vegetable kothu parotta",
    "chilli kothu parotta",
]

ROTI_MASTER_CLASSES: List[str] = [
    "chapati",
    "phulka",
    "roti",
    "tandoori roti",
    "rumali roti",
]

# =====================================================================
# 8. RICE & BIRYANI MASTER DATASETS (33+ Rice, 18+ Biryani)
# =====================================================================
RICE_MASTER_CLASSES: List[str] = [
    "plain white rice",
    "steamed rice",
    "boiled rice",
    "brown rice",
    "red rice",
    "hand-pounded rice",
    "matta rice",
    "seeraga samba rice",
    "ponni rice",
    "sona masuri rice",
    "ghee rice",
    "nei sadam",
    "kuska",
    "jeera rice",
    "vegetable rice",
    "mixed rice",
    "sambar rice",
    "rasam rice",
    "curd rice",
    "thayir sadam",
    "lemon rice",
    "elumichai sadam",
    "tamarind rice",
    "puliyodarai",
    "puliyogare",
    "tomato rice",
    "coconut rice",
    "mango rice",
    "mint rice",
    "pudina rice",
    "coriander rice",
    "sesame rice",
    "millet rice",
]

BIRYANI_MASTER_CLASSES: List[str] = [
    "chicken biryani",
    "mutton biryani",
    "egg biryani",
    "fish biryani",
    "prawn biryani",
    "veg biryani",
    "mushroom biryani",
    "paneer biryani",
    "beef biryani",
    "Ambur biryani",
    "Vaniyambadi biryani",
    "Dindigul biryani",
    "Thalappakatti-style biryani",
    "Chettinad biryani",
    "Hyderabadi biryani",
    "Malabar biryani",
    "Kalyani biryani",
    "Kuska",
]

BIRYANI_HARD_NEGATIVE_PAIRS: List[Dict[str, str]] = [
    {"pair": "Biryani vs Chicken Fried Rice", "rule": "Fried rice has wok-tossed separated grains with shredded carrots and spring onions; biryani has spice-coated grains with dum marinade."},
    {"pair": "Biryani vs Pulao", "rule": "Pulao is mildly spiced with whole vegetables cooked by water absorption; biryani is heavily layered with meat masala."},
    {"pair": "Biryani vs Kuska", "rule": "Kuska contains no meat pieces; Biryani must feature meat or egg chunks."},
    {"pair": "Biryani vs Ghee Rice", "rule": "Ghee rice is pale white/yellow with fried cashews and raisins, not dark spice-marinated."},
    {"pair": "Biryani vs Tomato Rice", "rule": "Tomato rice is red-hued with cooked tomato pulp, lacking whole biryani meat and dum aroma."}
]

# =====================================================================
# 9. KERALA, KARNATAKA, ANDHRA & TELANGANA MASTER FOODS
# =====================================================================
KERALA_MASTER_CLASSES: List[str] = [
    "appam", "palappam", "idiyappam", "puttu", "kadala curry", "kerala parotta",
    "avial", "thoran", "olan", "erissery", "kalan", "pachadi", "kichadi",
    "sambar", "rasam", "parippu curry", "fish curry", "meen curry", "meen fry",
    "beef curry", "chicken curry", "mutton curry", "puttu kadala", "appam stew",
    "vegetable stew", "payasam", "ada pradhaman", "palada payasam", "unniyappam",
    "banana fry", "pazham pori", "kozhukatta"
]

KARNATAKA_MASTER_CLASSES: List[str] = [
    "rava idli", "thatte idli", "mallige idli", "set dosa", "neer dosa",
    "mysore masala dosa", "bisi bele bath", "puliyogare", "vangi bath", "chitranna",
    "curd rice", "uppittu", "ragi mudde", "sambar", "rasam", "kosambari", "palya",
    "obattu", "holige", "mysore pak", "kesari bath", "maddur vada", "mangalore buns"
]

ANDHRA_TELANGANA_MASTER_CLASSES: List[str] = [
    "Andhra meals", "pulihora", "gongura rice", "gongura pachadi", "pappu",
    "tomato pappu", "dal", "pesarattu", "upma pesarattu", "gutti vankaya",
    "bendakaya fry", "potato fry", "chicken curry", "Andhra chicken", "chicken fry",
    "Andhra mutton", "mutton fry", "fish fry", "royyala iguru", "prawn curry",
    "mirchi bajji", "garelu", "boondi", "Hyderabadi biryani", "double ka meetha", "haleem"
]

# =====================================================================
# 10. SNACKS & SWEETS MASTER DATASETS
# =====================================================================
SNACKS_MASTER_CLASSES: List[str] = [
    "bajji", "onion bajji", "chilli bajji", "potato bajji", "banana bajji", "bread bajji",
    "bonda", "aloo bonda", "mysore bonda", "mangalore bonda",
    "pakoda", "onion pakoda", "banana chips", "murukku", "thenkuzhal", "thattai",
    "seedai", "nippattu", "mixture", "samosa", "kachori", "pani puri", "masala puri", "vada pav"
]

SWEETS_MASTER_CLASSES: List[str] = [
    "kesari", "rava kesari", "pineapple kesari", "carrot halwa", "beetroot halwa",
    "tirunelveli halwa", "wheat halwa", "sakkarai pongal", "payasam", "semiya payasam",
    "rice payasam", "paal payasam", "adai pradhaman", "gulab jamun", "jalebi",
    "mysore pak", "laddu", "boondi laddu", "motichoor laddu", "adhirasam",
    "kozhukattai", "paal kozhukattai", "modak", "unniyappam"
]

# =====================================================================
# 11. VEGETABLE SIDE DISHES & NON-VEG MASTER DATASETS
# =====================================================================
VEGETABLE_SIDE_DISHES: List[str] = [
    "beans poriyal", "carrot poriyal", "beetroot poriyal", "cabbage poriyal",
    "potato poriyal", "okra poriyal", "brinjal poriyal", "cauliflower poriyal",
    "kovakkai poriyal", "snake gourd poriyal", "bottle gourd poriyal", "drumstick poriyal",
    "keerai", "spinach", "moringa leaves", "kootu", "keerai kootu", "chow chow kootu",
    "bottle gourd kootu", "avial", "thoran"
]

NON_VEG_MASTER_CLASSES: List[str] = [
    "chicken 65", "chicken fry", "chicken pepper fry", "chicken sukka", "chicken chukka",
    "chicken chettinad", "chicken curry", "chicken gravy", "chicken roast", "chicken tikka",
    "chicken kebab", "chicken lollipop", "chicken leg", "chicken breast", "chicken wings",
    "chicken biryani", "chicken kothu parotta",
    "mutton curry", "mutton gravy", "mutton sukka", "mutton chukka", "mutton fry",
    "mutton pepper fry", "mutton kola", "mutton biryani", "mutton keema", "mutton soup",
    "fish fry", "fish curry", "meen kuzhambu", "meen varuval", "tawa fish", "fish roast", "fish biryani",
    "prawn fry", "prawn thokku", "prawn masala", "prawn curry", "crab masala", "crab curry", "nandu masala", "squid fry", "squid curry",
    "boiled egg", "half boiled egg", "full boiled egg", "omelette", "egg dosa", "egg kalakki", "egg bhurji", "egg curry", "egg masala", "egg podimas", "egg rice", "egg biryani"
]

# =====================================================================
# 12. SERVING VESSELS
# =====================================================================
SERVING_VESSEL_CLASSES: List[str] = [
    "banana leaf (traditional feast)",
    "stainless steel thali (compartmentalized)",
    "round steel plate",
    "ceramic / porcelain plate",
    "steel katori bowl",
    "ceramic side bowl",
    "paper plate / leaf plate",
    "plastic takeaway meal tray",
    "traditional tiffin dabba carrier"
]
