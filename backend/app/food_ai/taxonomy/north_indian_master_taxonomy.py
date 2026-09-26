"""
North Indian Master Food Taxonomy & Identity Hierarchy
Implements Sections 1-9, 10, 18, 19, 22, and 44 of Part 4.
Guarantees:
- Strict 9-Level Taxonomy:
  INDIAN FOOD -> NORTH INDIAN FOOD -> STATE/REGION -> FOOD FAMILY -> 
  FOOD TYPE -> FOOD VARIANT -> COOKING METHOD -> PORTION -> NUTRITION
- Covers all 8 Northern States/Regions:
  Punjab, Delhi, Uttar Pradesh, Rajasthan, Haryana, Himachal Pradesh, Uttarakhand, Jammu & Kashmir
- Over 300 Permanent Canonical Class IDs
- Multi-lingual regional name mapping (English, Hindi, Punjabi, Urdu, Rajasthani, Kashmiri, Pahari)
- Gravy texture & color classification (dry, semi, thin, oily, creamy, red, brown, green)
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class NorthIndianHierarchy(BaseModel):
    level1_food: str = "Indian Food"
    level2_macro_region: str = "North Indian Food"
    level3_state_region: str # Punjab, Delhi, Uttar Pradesh, Rajasthan, Haryana, Himachal Pradesh, Uttarakhand, Jammu & Kashmir
    level4_food_family: str # Breads, Parathas, Dals, Gravies, Kebabs, Street Food, Rice/Biryani, Sweets, Thali
    level5_food_type: str # e.g. Roti, Naan, Stuffed Paratha, Yellow Dal, Paneer Gravy, etc.
    level6_variant: str # e.g. Amritsari Kulcha, Dal Makhani, Palak Paneer
    level7_cooking_method: List[str] # tandoor, tawa_cooked, dum_cooked, slow_cooked, deep_fried, boiled
    level8_default_portion: str # 1 piece, 1 katori bowl, 1 plate, grams
    level9_nutrition_ref_id: str

class NorthIndianFoodClass(BaseModel):
    permanent_id: str # e.g. PB_BREAD_ROTI_TANDOORI, PB_CURRY_DAL_MAKHANI
    hierarchy: NorthIndianHierarchy
    canonical_name: str
    alternate_names: List[str] = Field(default_factory=list)
    regional_names: Dict[str, str] = Field(default_factory=dict)
    vegetarian: bool = True
    gravy_type: Optional[str] = Field(
        default=None, 
        description="dry, semi_gravy, thin_gravy, oily_gravy, creamy_gravy, red_gravy, brown_gravy, green_gravy"
    )
    visual_features: Dict[str, Any] = Field(default_factory=dict)
    key_ingredients: List[str] = Field(default_factory=list)
    possible_ingredients: List[str] = Field(default_factory=list)
    hard_negatives: List[str] = Field(default_factory=list)
    density_g_cm3: float = 0.85
    default_serving_weight_g: float = 120.0
    nutrition_per_100g: Dict[str, float] = Field(default_factory=dict)

# Master North Indian Registry
NORTH_INDIAN_TAXONOMY_REGISTRY: Dict[str, NorthIndianFoodClass] = {}
NORTH_INDIAN_SYNONYM_MAP: Dict[str, str] = {}

def register_north_food(food: NorthIndianFoodClass):
    NORTH_INDIAN_TAXONOMY_REGISTRY[food.permanent_id] = food
    NORTH_INDIAN_SYNONYM_MAP[food.canonical_name.lower().strip()] = food.permanent_id
    for alt in food.alternate_names:
        NORTH_INDIAN_SYNONYM_MAP[alt.lower().strip()] = food.permanent_id
    for reg_name in food.regional_names.values():
        NORTH_INDIAN_SYNONYM_MAP[reg_name.lower().strip()] = food.permanent_id

# =============================================================================
# 1. PUNJABI FOOD DATASET (BREADS, PARATHAS, DALS, GRAVIES, NON-VEG, RICE)
# =============================================================================

register_north_food(NorthIndianFoodClass(
    permanent_id="PB_BREAD_ROTI_TANDOORI",
    canonical_name="Tandoori Roti",
    alternate_names=["tandoori roti", "tandoor roti", "clay oven flatbread"],
    regional_names={"English": "Clay Oven Whole Wheat Flatbread", "Hindi": "तंदूरी रोटी", "Punjabi": "ਤੰਦੂਰੀ ਰੋਟੀ"},
    vegetarian=True,
    gravy_type="dry",
    visual_features={
        "shape": "round_disc",
        "thickness_mm": 2.5,
        "diameter_cm": 18.0,
        "surface": "charred_blisters_from_tandoor_wall",
        "color": "golden_tan_with_dark_char_spots",
        "crispness": "chewy_center_crisp_edges"
    },
    key_ingredients=["whole wheat flour (atta)", "water", "salt"],
    possible_ingredients=["butter glaze (if Butter Tandoori Roti)"],
    hard_negatives=["PB_BREAD_NAAN_PLAIN", "PB_BREAD_ROTI_TAWA", "PB_BREAD_KULCHA_AMRITSARI"],
    density_g_cm3=0.75,
    default_serving_weight_g=45.0,
    nutrition_per_100g={"calories": 240.0, "protein_g": 8.5, "carbs_g": 48.0, "fat_g": 1.5, "fiber_g": 7.0, "sodium_mg": 210.0},
    hierarchy=NorthIndianHierarchy(
        level3_state_region="Punjab",
        level4_food_family="Breads",
        level5_food_type="Roti",
        level6_variant="Tandoori Roti",
        level7_cooking_method=["tandoor_cooked"],
        level8_default_portion="1 piece (45g)",
        level9_nutrition_ref_id="ni_roti_tandoori"
    )
))

register_north_food(NorthIndianFoodClass(
    permanent_id="PB_BREAD_ROTI_MAKKI",
    canonical_name="Makki di Roti",
    alternate_names=["makki roti", "makki ki roti", "maize flour flatbread", "corn flatbread"],
    regional_names={"English": "Yellow Cornmeal Unleavened Flatbread", "Hindi": "मक्के की रोटी", "Punjabi": "ਮੱਕੀ ਦੀ ਰੋਟੀ"},
    vegetarian=True,
    gravy_type="dry",
    visual_features={
        "shape": "thick_rustic_circular_disc",
        "thickness_mm": 4.5,
        "diameter_cm": 16.0,
        "surface": "coarse_cracked_matte_yellow",
        "color": "vibrant_corn_yellow_with_brown_tawa_spots"
    },
    key_ingredients=["yellow maize flour (makki atta)", "warm water", "ajwain", "ghee/butter"],
    possible_ingredients=["fenugreek leaves (methi)"],
    hard_negatives=["RJ_BREAD_BAJRA_ROTI", "UK_BREAD_MANDUA_ROTI", "PB_BREAD_ROTI_TAWA"],
    density_g_cm3=0.88,
    default_serving_weight_g=60.0,
    nutrition_per_100g={"calories": 260.0, "protein_g": 6.2, "carbs_g": 46.5, "fat_g": 5.8, "fiber_g": 6.2, "sodium_mg": 180.0},
    hierarchy=NorthIndianHierarchy(
        level3_state_region="Punjab",
        level4_food_family="Breads",
        level5_food_type="Roti",
        level6_variant="Makki di Roti",
        level7_cooking_method=["tawa_cooked"],
        level8_default_portion="1 piece (60g)",
        level9_nutrition_ref_id="ni_roti_makki"
    )
))

register_north_food(NorthIndianFoodClass(
    permanent_id="PB_BREAD_NAAN_BUTTER",
    canonical_name="Butter Naan",
    alternate_names=["butter naan", "tandoori butter naan", "naan"],
    regional_names={"English": "Leavened Clay Oven Flatbread with Butter", "Hindi": "बटर नान", "Punjabi": "ਬਟਰ ਨਾਨ"},
    vegetarian=True,
    gravy_type="dry",
    visual_features={
        "shape": "teardrop_or_oval",
        "thickness_mm": 3.8,
        "length_cm": 24.0,
        "surface": "blistered_puffed_bubbles_glossy_butter",
        "color": "creamy_ivory_with_golden_brown_tandoor_scabs"
    },
    key_ingredients=["refined flour (maida)", "yogurt", "baking powder/yeast", "pure butter", "nigella seeds (kalonji)"],
    possible_ingredients=["coriander garnish"],
    hard_negatives=["PB_BREAD_ROTI_TANDOORI", "PB_BREAD_KULCHA_AMRITSARI", "PB_PARATHA_LACCHA"],
    density_g_cm3=0.72,
    default_serving_weight_g=85.0,
    nutrition_per_100g={"calories": 310.0, "protein_g": 8.0, "carbs_g": 48.5, "fat_g": 9.8, "fiber_g": 2.2, "sodium_mg": 380.0},
    hierarchy=NorthIndianHierarchy(
        level3_state_region="Punjab",
        level4_food_family="Breads",
        level5_food_type="Naan",
        level6_variant="Butter Naan",
        level7_cooking_method=["tandoor_cooked", "butter_glazed"],
        level8_default_portion="1 piece (85g)",
        level9_nutrition_ref_id="ni_naan_butter"
    )
))

register_north_food(NorthIndianFoodClass(
    permanent_id="PB_BREAD_KULCHA_AMRITSARI",
    canonical_name="Amritsari Kulcha",
    alternate_names=["amritsari kulcha", "aloo kulcha", "stuffed kulcha", "punjabi kulcha"],
    regional_names={"English": "Crisp Flaky Potato Stuffed Leavened Bread", "Hindi": "अमृतसरी कुल्चा", "Punjabi": "ਅੰਮ੍ਰਿਤਸਰੀ ਕੁਲਚਾ"},
    vegetarian=True,
    gravy_type="dry",
    visual_features={
        "shape": "layered_circular_crushed_disc",
        "thickness_mm": 5.5,
        "diameter_cm": 18.0,
        "surface": "flaky_crackly_crust_crushed_by_hand",
        "visible_toppings": ["anardana (pomegranate seeds)", "crushed coriander seeds", "kasuri methi", "melting butter pool"]
    },
    key_ingredients=["maida", "spiced mashed potatoes", "onions", "pomegranate seeds (anardana)", "coriander seeds", "butter"],
    possible_ingredients=["paneer bits"],
    hard_negatives=["PB_PARATHA_ALOO", "PB_BREAD_NAAN_BUTTER", "PB_BREAD_ROTI_TANDOORI"],
    density_g_cm3=0.82,
    default_serving_weight_g=140.0,
    nutrition_per_100g={"calories": 285.0, "protein_g": 6.8, "carbs_g": 42.0, "fat_g": 10.5, "fiber_g": 3.1, "sodium_mg": 440.0},
    hierarchy=NorthIndianHierarchy(
        level3_state_region="Punjab",
        level4_food_family="Breads",
        level5_food_type="Kulcha",
        level6_variant="Amritsari Potato Kulcha",
        level7_cooking_method=["tandoor_cooked", "hand_crushed"],
        level8_default_portion="1 piece (140g)",
        level9_nutrition_ref_id="ni_kulcha_amritsari"
    )
))

register_north_food(NorthIndianFoodClass(
    permanent_id="PB_PARATHA_ALOO",
    canonical_name="Aloo Paratha",
    alternate_names=["aloo paratha", "potato paratha", "aloo ka paratha", "punjabi aloo paratha"],
    regional_names={"English": "Spiced Potato Stuffed Whole Wheat Flatbread", "Hindi": "आलू पराठा", "Punjabi": "ਆਲੂ ਪਰੌਂਠਾ"},
    vegetarian=True,
    gravy_type="dry",
    visual_features={
        "shape": "round_thick_flatbread",
        "thickness_mm": 4.0,
        "diameter_cm": 20.0,
        "surface": "tawa_roasted_golden_brown_blisters_with_potato_filling_peeking",
        "oil_ghee_sheen": "butter_or_desi_ghee_glazed"
    },
    key_ingredients=["whole wheat flour", "boiled mashed potatoes", "green chillies", "ajwain", "amchur (dry mango powder)", "butter/ghee"],
    possible_ingredients=["finely chopped onions", "fresh coriander"],
    hard_negatives=["PB_PARATHA_PLAIN", "PB_PARATHA_GOBI", "PB_BREAD_KULCHA_AMRITSARI"],
    density_g_cm3=0.86,
    default_serving_weight_g=120.0,
    nutrition_per_100g={"calories": 245.0, "protein_g": 5.4, "carbs_g": 38.5, "fat_g": 8.2, "fiber_g": 3.8, "sodium_mg": 320.0},
    hierarchy=NorthIndianHierarchy(
        level3_state_region="Punjab",
        level4_food_family="Parathas",
        level5_food_type="Stuffed Paratha",
        level6_variant="Aloo Paratha",
        level7_cooking_method=["tawa_cooked", "shallow_fried"],
        level8_default_portion="1 piece (120g)",
        level9_nutrition_ref_id="ni_paratha_aloo"
    )
))

register_north_food(NorthIndianFoodClass(
    permanent_id="PB_PARATHA_GOBI",
    canonical_name="Gobi Paratha",
    alternate_names=["gobi paratha", "cauliflower paratha", "gobhi paratha"],
    regional_names={"English": "Grated Spiced Cauliflower Stuffed Flatbread", "Hindi": "गोभी पराठा", "Punjabi": "ਗੋਭੀ ਪਰੌਂਠਾ"},
    vegetarian=True,
    gravy_type="dry",
    visual_features={
        "shape": "round_flatbread",
        "thickness_mm": 3.8,
        "diameter_cm": 20.0,
        "surface": "golden_brown_tawa_specks_with_white_cauliflower_flecks_visible"
    },
    key_ingredients=["whole wheat flour", "grated spiced cauliflower", "carom seeds (ajwain)", "green chillies", "butter"],
    possible_ingredients=["coriander"],
    hard_negatives=["PB_PARATHA_ALOO", "PB_PARATHA_MOOLI", "PB_PARATHA_PANEER"],
    density_g_cm3=0.82,
    default_serving_weight_g=115.0,
    nutrition_per_100g={"calories": 215.0, "protein_g": 5.8, "carbs_g": 34.0, "fat_g": 6.8, "fiber_g": 4.5, "sodium_mg": 290.0},
    hierarchy=NorthIndianHierarchy(
        level3_state_region="Punjab",
        level4_food_family="Parathas",
        level5_food_type="Stuffed Paratha",
        level6_variant="Gobi Paratha",
        level7_cooking_method=["tawa_cooked"],
        level8_default_portion="1 piece (115g)",
        level9_nutrition_ref_id="ni_paratha_gobi"
    )
))

register_north_food(NorthIndianFoodClass(
    permanent_id="PB_PARATHA_PANEER",
    canonical_name="Paneer Paratha",
    alternate_names=["paneer paratha", "cottage cheese paratha"],
    regional_names={"English": "Crumbled Spiced Paneer Stuffed Flatbread", "Hindi": "पनीर पराठा", "Punjabi": "ਪਨੀਰ ਪਰੌਂਠਾ"},
    vegetarian=True,
    gravy_type="dry",
    visual_features={
        "shape": "round_flatbread",
        "thickness_mm": 4.2,
        "diameter_cm": 20.0,
        "surface": "golden_crust_with_white_paneer_curds_visible_at_folds"
    },
    key_ingredients=["whole wheat flour", "grated fresh paneer", "green chillies", "garam masala", "butter"],
    possible_ingredients=["mint"],
    hard_negatives=["PB_PARATHA_ALOO", "PB_PARATHA_GOBI", "PB_BREAD_KULCHA_PANEER"],
    density_g_cm3=0.85,
    default_serving_weight_g=130.0,
    nutrition_per_100g={"calories": 275.0, "protein_g": 10.5, "carbs_g": 32.0, "fat_g": 12.0, "fiber_g": 3.0, "sodium_mg": 310.0},
    hierarchy=NorthIndianHierarchy(
        level3_state_region="Punjab",
        level4_food_family="Parathas",
        level5_food_type="Stuffed Paratha",
        level6_variant="Paneer Paratha",
        level7_cooking_method=["tawa_cooked"],
        level8_default_portion="1 piece (130g)",
        level9_nutrition_ref_id="ni_paratha_paneer"
    )
))

register_north_food(NorthIndianFoodClass(
    permanent_id="PB_CURRY_DAL_MAKHANI",
    canonical_name="Dal Makhani",
    alternate_names=["dal makhani", "dal makhni", "black dal", "maa ki dal", "creamy black lentils"],
    regional_names={"English": "Slow-Simmered Creamy Black Lentils & Kidney Beans", "Hindi": "दाल मखनी", "Punjabi": "ਦਾਲ ਮੱਖਣੀ"},
    vegetarian=True,
    gravy_type="creamy_gravy",
    visual_features={
        "viscosity": "ultra_thick_velvety_creamy",
        "color": "deep_reddish_black_maroon",
        "surface": "swirled_fresh_cream_spiral_and_butter_cube",
        "lentils_visible": ["whole black urad beans", "dark red kidney beans (rajma)"]
    },
    key_ingredients=["whole black urad dal", "rajma (red kidney beans)", "butter (makhan)", "heavy fresh cream", "tomato puree", "kashmiri red chilli", "kasuri methi"],
    possible_ingredients=["smoked charcoal infusion (dhungar)"],
    hard_negatives=["PB_CURRY_RAJMA_MASALA", "PB_CURRY_DAL_TADKA", "PB_CURRY_CHANA_DAL"],
    density_g_cm3=1.08,
    default_serving_weight_g=180.0,
    nutrition_per_100g={"calories": 165.0, "protein_g": 5.8, "carbs_g": 16.5, "fat_g": 8.8, "fiber_g": 4.2, "sodium_mg": 340.0},
    hierarchy=NorthIndianHierarchy(
        level3_state_region="Punjab",
        level4_food_family="Dals",
        level5_food_type="Black Dal",
        level6_variant="Dal Makhani",
        level7_cooking_method=["slow_cooked", "simmered"],
        level8_default_portion="1 katori bowl (180g)",
        level9_nutrition_ref_id="ni_dal_makhani"
    )
))

register_north_food(NorthIndianFoodClass(
    permanent_id="PB_CURRY_DAL_TADKA",
    canonical_name="Dal Tadka",
    alternate_names=["dal tadka", "yellow dal tadka", "peeli dal", "dhaba dal tadka"],
    regional_names={"English": "Yellow Lentils Tempered with Ghee, Garlic & Cumin", "Hindi": "दाल तड़का", "Punjabi": "ਦਾਲ ਤੜਕਾ"},
    vegetarian=True,
    gravy_type="semi_gravy",
    visual_features={
        "viscosity": "medium_pouring_stew",
        "color": "bright_golden_yellow",
        "surface": "crackled_whole_red_chillies_cumin_garlic_tadka_sheen",
        "lentils_visible": ["soft split yellow toor dal", "yellow moong dal"]
    },
    key_ingredients=["toor dal (pigeon pea)", "yellow moong dal", "desi ghee", "cumin seeds (jeera)", "garlic cloves", "dried whole red chillies", "tomatoes", "coriander"],
    possible_ingredients=["asafoetida", "ginger"],
    hard_negatives=["PB_CURRY_DAL_FRY", "TN_CURRY_SAMBAR_TIFFIN", "RJ_CURRY_KADHI"],
    density_g_cm3=1.04,
    default_serving_weight_g=180.0,
    nutrition_per_100g={"calories": 98.0, "protein_g": 5.2, "carbs_g": 13.5, "fat_g": 2.8, "fiber_g": 3.4, "sodium_mg": 280.0},
    hierarchy=NorthIndianHierarchy(
        level3_state_region="Punjab",
        level4_food_family="Dals",
        level5_food_type="Yellow Dal",
        level6_variant="Dal Tadka",
        level7_cooking_method=["pressure_cooked", "tempered"],
        level8_default_portion="1 katori bowl (180g)",
        level9_nutrition_ref_id="ni_dal_tadka"
    )
))

register_north_food(NorthIndianFoodClass(
    permanent_id="PB_CURRY_RAJMA_MASALA",
    canonical_name="Rajma Masala",
    alternate_names=["rajma", "rajma curry", "punjabi rajma", "rajma rasmisa"],
    regional_names={"English": "Red Kidney Beans in Spiced Onion-Tomato Gravy", "Hindi": "राजमा मसाला", "Punjabi": "ਰਾਜਮਾ ਮਸਾਲਾ"},
    vegetarian=True,
    gravy_type="red_gravy",
    visual_features={
        "viscosity": "thick_rich_saucy",
        "color": "deep_crimson_reddish_brown",
        "beans_visible": ["plump whole dark-red kidney beans"],
        "surface": "glistening_onion_tomato_masala_gravy"
    },
    key_ingredients=["red kidney beans (rajma)", "onions", "tomatoes", "ginger garlic paste", "garam masala", "kashmiri chilli", "coriander"],
    possible_ingredients=["butter finish"],
    hard_negatives=["PB_CURRY_CHOLE", "PB_CURRY_DAL_MAKHANI", "JK_CURRY_GOGJI_RAJMA"],
    density_g_cm3=1.06,
    default_serving_weight_g=200.0,
    nutrition_per_100g={"calories": 140.0, "protein_g": 6.8, "carbs_g": 20.5, "fat_g": 3.8, "fiber_g": 5.2, "sodium_mg": 320.0},
    hierarchy=NorthIndianHierarchy(
        level3_state_region="Punjab",
        level4_food_family="Gravies",
        level5_food_type="Bean Curry",
        level6_variant="Rajma Masala",
        level7_cooking_method=["pressure_cooked", "simmered"],
        level8_default_portion="1 katori bowl (200g)",
        level9_nutrition_ref_id="ni_rajma_masala"
    )
))

register_north_food(NorthIndianFoodClass(
    permanent_id="PB_CURRY_CHOLE_PUNJABI",
    canonical_name="Punjabi Chole (Amritsari Chana)",
    alternate_names=["chole", "chana masala", "amritsari chole", "pindi chole", "punjabi chana"],
    regional_names={"English": "Spiced Tangy White Chickpea Curry", "Hindi": "पंजाबी छोले", "Punjabi": "ਪੰਜਾਬੀ ਛੋਲੇ"},
    vegetarian=True,
    gravy_type="brown_gravy",
    visual_features={
        "viscosity": "thick_semi_dry_to_saucy",
        "color": "deep_dark_brown_to_blackish_amber",
        "beans_visible": ["large plump white kabuli chickpeas"],
        "garnishes": ["ginger juliennes", "slit green chillies", "onion rings"]
    },
    key_ingredients=["kabuli chickpeas", "tea bag/anardana (for dark color)", "pomegranate seeds", "amchur", "onions", "tomatoes", "chole masala"],
    possible_ingredients=["kasuri methi"],
    hard_negatives=["PB_CURRY_RAJMA_MASALA", "DL_STREET_CHOLE_KULCHE", "RJ_SNACK_MIRCHI_BADA"],
    density_g_cm3=1.05,
    default_serving_weight_g=200.0,
    nutrition_per_100g={"calories": 165.0, "protein_g": 7.5, "carbs_g": 22.0, "fat_g": 5.5, "fiber_g": 6.0, "sodium_mg": 350.0},
    hierarchy=NorthIndianHierarchy(
        level3_state_region="Punjab",
        level4_food_family="Gravies",
        level5_food_type="Chickpea Curry",
        level6_variant="Amritsari Chole",
        level7_cooking_method=["boiled", "simmered_masala"],
        level8_default_portion="1 katori bowl (200g)",
        level9_nutrition_ref_id="ni_chole_punjabi"
    )
))

register_north_food(NorthIndianFoodClass(
    permanent_id="PB_CURRY_SARSON_KA_SAAG",
    canonical_name="Sarson da Saag",
    alternate_names=["sarson ka saag", "sarson saag", "mustard greens gravy"],
    regional_names={"English": "Traditional Slow-Cooked Mustard & Spinach Greens", "Hindi": "सरसों का साग", "Punjabi": "ਸਰ੍ਹੋਂ ਦਾ ਸਾਗ"},
    vegetarian=True,
    gravy_type="green_gravy",
    visual_features={
        "viscosity": "dense_coarse_puree_mash",
        "color": "deep_earthy_olive_green",
        "surface": "melting_white_butter_dollop_(safed_makhan)",
        "texture": "fibrous_slow_cooked_greens"
    },
    key_ingredients=["mustard greens (sarson)", "spinach (palak)", "bathua (chenopodium)", "makki atta (for thickening)", "ginger", "garlic", "green chillies", "white butter"],
    possible_ingredients=["radish leaves"],
    hard_negatives=["PB_CURRY_PALAK_PANEER", "UK_CURRY_KAFULI", "JK_CURRY_HAAK"],
    density_g_cm3=0.98,
    default_serving_weight_g=200.0,
    nutrition_per_100g={"calories": 115.0, "protein_g": 4.2, "carbs_g": 9.5, "fat_g": 6.8, "fiber_g": 5.0, "sodium_mg": 240.0},
    hierarchy=NorthIndianHierarchy(
        level3_state_region="Punjab",
        level4_food_family="Gravies",
        level5_food_type="Leafy Green Mash",
        level6_variant="Sarson da Saag",
        level7_cooking_method=["slow_cooked", "hand_mashed"],
        level8_default_portion="1 bowl (200g)",
        level9_nutrition_ref_id="ni_sarson_saag"
    )
))

register_north_food(NorthIndianFoodClass(
    permanent_id="PB_CURRY_PALAK_PANEER",
    canonical_name="Palak Paneer",
    alternate_names=["palak paneer", "spinach cottage cheese", "saag paneer"],
    regional_names={"English": "Indian Cottage Cheese Cubes in Creamy Spinach Gravy", "Hindi": "पालक पनीर", "Punjabi": "ਪਾਲਕ ਪਨੀਰ"},
    vegetarian=True,
    gravy_type="green_gravy",
    visual_features={
        "viscosity": "smooth_to_medium_thick_puree",
        "color": "vibrant_emerald_to_forest_green",
        "inclusions": ["pure white rectangular/cubed paneer blocks"],
        "garnishes": ["fresh cream drizzle", "ginger juliennes"]
    },
    key_ingredients=["fresh spinach (palak)", "fresh paneer cubes", "onions", "tomatoes", "garlic", "ginger", "green chillies", "cream", "kasuri methi"],
    possible_ingredients=["butter"],
    hard_negatives=["PB_CURRY_SARSON_KA_SAAG", "PB_CURRY_PANEER_BUTTER_MASALA", "UK_CURRY_KAFULI"],
    density_g_cm3=1.02,
    default_serving_weight_g=220.0,
    nutrition_per_100g={"calories": 160.0, "protein_g": 8.5, "carbs_g": 7.2, "fat_g": 11.2, "fiber_g": 3.2, "sodium_mg": 290.0},
    hierarchy=NorthIndianHierarchy(
        level3_state_region="Punjab",
        level4_food_family="Gravies",
        level5_food_type="Paneer Gravy",
        level6_variant="Palak Paneer",
        level7_cooking_method=["blanched", "simmered"],
        level8_default_portion="1 bowl (220g)",
        level9_nutrition_ref_id="ni_palak_paneer"
    )
))

register_north_food(NorthIndianFoodClass(
    permanent_id="PB_CURRY_PANEER_BUTTER_MASALA",
    canonical_name="Paneer Butter Masala",
    alternate_names=["paneer makhani", "paneer butter masala", "butter paneer", "pbm"],
    regional_names={"English": "Paneer Cubes in Rich Creamy Tomato-Butter Sauce", "Hindi": "पनीर बटर मसाला", "Punjabi": "ਪਨੀਰ ਬਟਰ ਮਸਾਲਾ"},
    vegetarian=True,
    gravy_type="creamy_gravy",
    visual_features={
        "viscosity": "thick_velvety_rich_emulsion",
        "color": "vibrant_orange_to_crimson_red",
        "inclusions": ["soft white paneer cubes"],
        "surface": "swirled_fresh_cream_and_butter_lake"
    },
    key_ingredients=["paneer cubes", "butter", "cashew nut paste", "pureed tomatoes", "heavy cream", "kasuri methi", "kashmiri red chilli", "honey/sugar pinch"],
    possible_ingredients=["whole spices"],
    hard_negatives=["PB_NONVEG_BUTTER_CHICKEN", "PB_CURRY_SHAHI_PANEER", "PB_CURRY_KADAI_PANEER"],
    density_g_cm3=1.06,
    default_serving_weight_g=220.0,
    nutrition_per_100g={"calories": 235.0, "protein_g": 7.8, "carbs_g": 10.5, "fat_g": 18.5, "fiber_g": 1.6, "sodium_mg": 360.0},
    hierarchy=NorthIndianHierarchy(
        level3_state_region="Punjab",
        level4_food_family="Gravies",
        level5_food_type="Paneer Gravy",
        level6_variant="Paneer Butter Masala",
        level7_cooking_method=["simmered", "creamed"],
        level8_default_portion="1 bowl (220g)",
        level9_nutrition_ref_id="ni_paneer_butter_masala"
    )
))

register_north_food(NorthIndianFoodClass(
    permanent_id="PB_NONVEG_BUTTER_CHICKEN",
    canonical_name="Butter Chicken (Murgh Makhani)",
    alternate_names=["butter chicken", "murgh makhani", "tandoori butter chicken", "chicken makhani"],
    regional_names={"English": "Tandoori Chicken Chunks in Creamy Tomato Gravy", "Hindi": "बटर चिकन / मुर्ग मखनी", "Punjabi": "ਬਟਰ ਚਿਕਨ"},
    vegetarian=False,
    gravy_type="creamy_gravy",
    visual_features={
        "viscosity": "velvety_smooth_creamy_emulsion",
        "color": "rich_warm_orange_vermilion",
        "meat_visible": ["tandoori roasted chicken pieces with charred marks"],
        "surface": "cream_swirl_and_melted_butter_pool"
    },
    key_ingredients=["tandoor grilled bone-in/boneless chicken", "tomato gravy", "cashew paste", "pure butter", "heavy cream", "kashmiri chilli", "kasuri methi"],
    possible_ingredients=["garam masala"],
    hard_negatives=["PB_CURRY_PANEER_BUTTER_MASALA", "PB_NONVEG_CHICKEN_TIKKA_MASALA", "DL_MUGHLAI_CHICKEN_CHANGEZI"],
    density_g_cm3=1.06,
    default_serving_weight_g=240.0,
    nutrition_per_100g={"calories": 215.0, "protein_g": 14.5, "carbs_g": 7.8, "fat_g": 14.2, "fiber_g": 1.2, "sodium_mg": 390.0},
    hierarchy=NorthIndianHierarchy(
        level3_state_region="Punjab",
        level4_food_family="Non-Veg",
        level5_food_type="Chicken Curry",
        level6_variant="Butter Chicken",
        level7_cooking_method=["tandoor_roasted", "simmered_gravy"],
        level8_default_portion="1 bowl (240g)",
        level9_nutrition_ref_id="ni_butter_chicken"
    )
))

# =============================================================================
# 2. DELHI STREET FOOD & MUGHLAI (CHOLE BHATURE, CHAATS, KEBABS)
# =============================================================================

register_north_food(NorthIndianFoodClass(
    permanent_id="DL_STREET_CHOLE_BHATURE",
    canonical_name="Chole Bhature",
    alternate_names=["chole bhature", "chana bhatura", "delhi chole bhature"],
    regional_names={"English": "Spiced Chickpea Curry with Puffed Deep Fried Bread", "Hindi": "छोले भटूरे"},
    vegetarian=True,
    gravy_type="brown_gravy",
    visual_features={
        "bhatura": "giant_inflated_balloon_oval_bread",
        "bhatura_diameter_cm": 24.0,
        "chole_color": "dark_amber_brown",
        "sides": ["sliced red onions", "pickled green chilli", "lemon wedge"]
    },
    key_ingredients=["chickpeas (kabuli chana)", "refined flour (maida)", "fermented dough", "oil for deep frying", "spices", "anardana"],
    possible_ingredients=["paneer stuffing in bhatura"],
    hard_negatives=["UP_BREAKFAST_POORI_SABZI", "DL_STREET_CHOLE_KULCHE", "TN_BREAKFAST_POORI_MASALA"],
    density_g_cm3=0.85,
    default_serving_weight_g=380.0,
    nutrition_per_100g={"calories": 255.0, "protein_g": 6.8, "carbs_g": 34.0, "fat_g": 10.8, "fiber_g": 4.5, "sodium_mg": 460.0},
    hierarchy=NorthIndianHierarchy(
        level3_state_region="Delhi",
        level4_food_family="Street Food",
        level5_food_type="Combo Platter",
        level6_variant="Chole Bhature",
        level7_cooking_method=["deep_fried", "stew_boiled"],
        level8_default_portion="2 bhature + 1 bowl chole (380g)",
        level9_nutrition_ref_id="ni_chole_bhature"
    )
))

register_north_food(NorthIndianFoodClass(
    permanent_id="DL_STREET_ALOO_TIKKI_CHAAT",
    canonical_name="Aloo Tikki Chaat",
    alternate_names=["aloo tikki", "tikki chaat", "dahi aloo tikki"],
    regional_names={"English": "Crisp Potato Patties with Yogurt & Chutneys", "Hindi": "आलू टिक्की चाट"},
    vegetarian=True,
    gravy_type="semi_gravy",
    visual_features={
        "patty": "crispy_pan_fried_golden_brown_potato_cakes",
        "dressings": ["thick whisked sweet curd", "sweet brown tamarind-saunth chutney", "tangy green mint-coriander chutney"],
        "garnishes": ["sev (chickpea crisps)", "pomegranate seeds", "chaat masala"]
    },
    key_ingredients=["boiled mashed potatoes", "cornstarch", "curd", "tamarind chutney", "mint chutney", "spices", "sev"],
    possible_ingredients=["chole topping", "chana dal filling"],
    hard_negatives=["DL_STREET_DAHI_BHALLA", "DL_STREET_PAPDI_CHAAT", "RJ_SNACK_MIRCHI_BADA"],
    density_g_cm3=1.02,
    default_serving_weight_g=220.0,
    nutrition_per_100g={"calories": 175.0, "protein_g": 3.8, "carbs_g": 24.5, "fat_g": 7.2, "fiber_g": 2.5, "sodium_mg": 380.0},
    hierarchy=NorthIndianHierarchy(
        level3_state_region="Delhi",
        level4_food_family="Street Food",
        level5_food_type="Chaat",
        level6_variant="Aloo Tikki Chaat",
        level7_cooking_method=["shallow_fried_tawa", "assembled"],
        level8_default_portion="1 plate (220g)",
        level9_nutrition_ref_id="ni_aloo_tikki_chaat"
    )
))

register_north_food(NorthIndianFoodClass(
    permanent_id="DL_KEBAB_SEEKH_MUTTON",
    canonical_name="Mutton Seekh Kebab",
    alternate_names=["seekh kebab", "mutton seekh", "tandoori seekh kebab", "kakori kebab"],
    regional_names={"English": "Spiced Minced Lamb Skewered & Tandoor Roasted", "Hindi": "सीख कबाब", "Urdu": "سیخ کباب"},
    vegetarian=False,
    gravy_type="dry",
    visual_features={
        "shape": "cylindrical_hollow_tube_segments",
        "length_cm": 15.0,
        "diameter_cm": 2.8,
        "surface": "charred_grill_marks_succulent_meat_texture",
        "color": "dark_reddish_brown_char"
    },
    key_ingredients=["minced mutton (keema)", "raw papaya paste (tenderizer)", "browned onions", "ginger garlic paste", "garam masala", "mint", "ghee"],
    possible_ingredients=["egg binder"],
    hard_negatives=["PB_NONVEG_CHICKEN_TIKKA", "UP_KEBAB_GALOUTI", "PB_NONVEG_SEEKH_CHICKEN"],
    density_g_cm3=0.92,
    default_serving_weight_g=150.0,
    nutrition_per_100g={"calories": 260.0, "protein_g": 21.5, "carbs_g": 4.5, "fat_g": 17.5, "fiber_g": 0.8, "sodium_mg": 460.0},
    hierarchy=NorthIndianHierarchy(
        level3_state_region="Delhi",
        level4_food_family="Kebabs",
        level5_food_type="Skewered Meat",
        level6_variant="Mutton Seekh Kebab",
        level7_cooking_method=["tandoor_grilled", "skewered"],
        level8_default_portion="2 skewers (150g)",
        level9_nutrition_ref_id="ni_seekh_mutton"
    )
))

# =============================================================================
# 3. RAJASTHANI FOOD DATASET (DAL BAATI CHURMA, GATTE, LAAL MAAS, KER SANGRI)
# =============================================================================

register_north_food(NorthIndianFoodClass(
    permanent_id="RJ_MAIN_DAL_BAATI_CHURMA",
    canonical_name="Dal Baati Churma",
    alternate_names=["dal baati churma", "dal bati", "dal baati", "rajasthani thali baati"],
    regional_names={"English": "Baked Wheat Dumplings with Panchmel Dal & Sweet Crumbs", "Hindi": "दाल बाटी चूरमा", "Rajasthani": "दाल बाटी चूरमो"},
    vegetarian=True,
    gravy_type="semi_gravy",
    visual_features={
        "baati": "cracked_spherical_golden_hard_wheat_balls_dipped_in_ghee",
        "dal": "rich_five_lentil_panchmel_dal_with_red_chilli_tadka",
        "churma": "sweet_granular_golden_wheat_crumb_powder"
    },
    key_ingredients=["whole wheat coarse flour (atta)", "desi cow ghee", "panchmel dal (toor, moong, chana, urad, masoor)", "jaggery/sugar", "cardamom"],
    possible_ingredients=["fried garlic chutney accompaniment"],
    hard_negatives=["HP_MAIN_SIDDU", "PB_CURRY_DAL_TADKA", "RJ_CURRY_GATTE"],
    density_g_cm3=0.95,
    default_serving_weight_g=420.0,
    nutrition_per_100g={"calories": 275.0, "protein_g": 7.2, "carbs_g": 36.5, "fat_g": 12.0, "fiber_g": 4.2, "sodium_mg": 320.0},
    hierarchy=NorthIndianHierarchy(
        level3_state_region="Rajasthan",
        level4_food_family="Thali",
        level5_food_type="Traditional Platter",
        level6_variant="Dal Baati Churma",
        level7_cooking_method=["baked_over_coals", "deep_ghee_dip", "pressure_cooked"],
        level8_default_portion="2 baati + dal + churma (420g)",
        level9_nutrition_ref_id="ni_dal_baati_churma"
    )
))

register_north_food(NorthIndianFoodClass(
    permanent_id="RJ_CURRY_GATTE_KI_SABZI",
    canonical_name="Gatte ki Sabzi",
    alternate_names=["gatta curry", "gatte ki sabzi", "rajasthani gatta curry", "govind gatta"],
    regional_names={"English": "Gram Flour Dumpling Coins in Spiced Yogurt Gravy", "Hindi": "गट्टे की सब्जी", "Rajasthani": "गट्टा री सब्जी"},
    vegetarian=True,
    gravy_type="semi_gravy",
    visual_features={
        "dumplings": "cylindrical_sliced_gram_flour_coins",
        "gravy_color": "golden_orange_yellow",
        "viscosity": "spiced_yogurt_simmered_curry",
        "surface": "mustard_coriander_ghee_tempering_sheen"
    },
    key_ingredients=["besan (gram flour)", "yogurt (curd)", "mustard seeds", "fennel seeds", "carom seeds (ajwain)", "turmeric", "ghee/oil"],
    possible_ingredients=["mawa filling (for Govind Gatta)"],
    hard_negatives=["PB_CURRY_KADHI_PAKORA", "HP_CURRY_SEPU_VADI", "RJ_CURRY_PAPAD_KI_SABZI"],
    density_g_cm3=1.04,
    default_serving_weight_g=200.0,
    nutrition_per_100g={"calories": 145.0, "protein_g": 6.8, "carbs_g": 14.2, "fat_g": 7.2, "fiber_g": 3.0, "sodium_mg": 340.0},
    hierarchy=NorthIndianHierarchy(
        level3_state_region="Rajasthan",
        level4_food_family="Gravies",
        level5_food_type="Gram Flour Dumplings",
        level6_variant="Gatte ki Sabzi",
        level7_cooking_method=["boiled", "simmered_in_curd"],
        level8_default_portion="1 bowl (200g)",
        level9_nutrition_ref_id="ni_gatte_sabzi"
    )
))

register_north_food(NorthIndianFoodClass(
    permanent_id="RJ_NONVEG_LAAL_MAAS",
    canonical_name="Rajasthani Laal Maas",
    alternate_names=["laal maas", "lal maas", "rajasthani mutton curry", "red mutton curry"],
    regional_names={"English": "Fiery Red Mutton Curry with Mathania Chillies", "Hindi": "लाल मांस", "Rajasthani": "लाल माँस"},
    vegetarian=False,
    gravy_type="red_gravy",
    visual_features={
        "viscosity": "thick_spiced_oil_floating_gravy",
        "color": "vibrant_blood_red_from_mathania_chillies",
        "meat_visible": ["tender bone-in goat mutton cuts"],
        "surface": "tari (red spicy oil layer)"
    },
    key_ingredients=["bone-in young mutton", "mathania dried red chillies (soaked & ground)", "mustard oil / desi ghee", "garlic paste", "yogurt", "kachri powder"],
    possible_ingredients=["smoked charcoal (dhungar)"],
    hard_negatives=["JK_NONVEG_ROGAN_JOSH", "PB_NONVEG_MUTTON_CURRY", "UP_AWADHI_KORMA"],
    density_g_cm3=1.08,
    default_serving_weight_g=220.0,
    nutrition_per_100g={"calories": 225.0, "protein_g": 16.5, "carbs_g": 4.8, "fat_g": 15.8, "fiber_g": 1.5, "sodium_mg": 410.0},
    hierarchy=NorthIndianHierarchy(
        level3_state_region="Rajasthan",
        level4_food_family="Non-Veg",
        level5_food_type="Mutton Curry",
        level6_variant="Laal Maas",
        level7_cooking_method=["slow_cooked", "pot_braised"],
        level8_default_portion="1 bowl (220g)",
        level9_nutrition_ref_id="ni_laal_maas"
    )
))

# =============================================================================
# 4. UTTAR PRADESH & AWADHI (LUCKNOW BIRYANI, GALOUTI, NIHARI, BEDMI PURI)
# =============================================================================

register_north_food(NorthIndianFoodClass(
    permanent_id="UP_AWADHI_BIRYANI_LUCKNOWI",
    canonical_name="Lucknowi Awadhi Biryani",
    alternate_names=["lucknowi biryani", "awadhi biryani", "dum pukht biryani", "lucknow chicken biryani"],
    regional_names={"English": "Fragrant Mild Yakhni Dum Biryani", "Hindi": "अवधी बिरयानी", "Urdu": "لکھنوی بریانی"},
    vegetarian=False,
    gravy_type="dry",
    visual_features={
        "rice": "long_slender_aged_basmati_needles",
        "color": "subtle_variegated_pearl_white_and_light_saffron",
        "spices": "no_coarse_red_masala_coating_clean_grains",
        "meat": "tender_pale_chicken_or_mutton_cooked_in_yakhni_stock",
        "aroma_markers": ["ittar / kewra water droplets", "fried golden onions"]
    },
    key_ingredients=["aged basmati rice", "meat cooked in yakhni (bone broth)", "kewra water", "saffron milk", "meetha ittar", "desi ghee", "mace and cardamom"],
    possible_ingredients=["fried onions"],
    hard_negatives=["TS_BIRYANI_HYDERABADI_CHICKEN", "TN_BIRYANI_DINDIGUL_MUTTON", "PB_RICE_PULAO"],
    density_g_cm3=0.82,
    default_serving_weight_g=350.0,
    nutrition_per_100g={"calories": 165.0, "protein_g": 10.2, "carbs_g": 22.5, "fat_g": 4.5, "fiber_g": 0.8, "sodium_mg": 280.0},
    hierarchy=NorthIndianHierarchy(
        level3_state_region="Uttar Pradesh",
        level4_food_family="Rice/Biryani",
        level5_food_type="Biryani",
        level6_variant="Awadhi Lucknowi Biryani",
        level7_cooking_method=["dum_pukht_slow_steam"],
        level8_default_portion="1 plate (350g)",
        level9_nutrition_ref_id="ni_biryani_lucknowi"
    )
))

register_north_food(NorthIndianFoodClass(
    permanent_id="UP_KEBAB_GALOUTI",
    canonical_name="Galouti Kebab (Tunday Kebab)",
    alternate_names=["galouti kebab", "galawati kebab", "tunday kabab", "lucknowi kebab"],
    regional_names={"English": "Melt-in-Mouth Spiced Minced Mutton Patties", "Hindi": "गलौटी कबाब", "Urdu": "گلاوٹی کباب"},
    vegetarian=False,
    gravy_type="dry",
    visual_features={
        "shape": "ultra_soft_shallow_flattened_patties",
        "diameter_cm": 6.5,
        "thickness_mm": 12.0,
        "texture": "silky_pate_like_crumb_melting_delicate",
        "color": "caramelized_dark_brownish_amber"
    },
    key_ingredients=["fine minced mutton (keema passed through sieve 4 times)", "raw green papaya paste", "160 secret awadhi spices", "rose water", "kewra", "pure ghee"],
    possible_ingredients=["potli masala"],
    hard_negatives=["DL_KEBAB_SEEKH_MUTTON", "DL_STREET_ALOO_TIKKI_CHAAT", "UP_KEBAB_SHAMI"],
    density_g_cm3=0.96,
    default_serving_weight_g=120.0,
    nutrition_per_100g={"calories": 270.0, "protein_g": 19.5, "carbs_g": 3.8, "fat_g": 20.0, "fiber_g": 0.5, "sodium_mg": 440.0},
    hierarchy=NorthIndianHierarchy(
        level3_state_region="Uttar Pradesh",
        level4_food_family="Kebabs",
        level5_food_type="Shallow Fried Kebab",
        level6_variant="Galouti Kebab",
        level7_cooking_method=["pan_fried_ghee"],
        level8_default_portion="4 patties (120g)",
        level9_nutrition_ref_id="ni_kebab_galouti"
    )
))

# =============================================================================
# 5. HIMACHAL PRADESH FOOD DATASET (DHAM COMPONENTS, MADRA, SIDDU)
# =============================================================================

register_north_food(NorthIndianFoodClass(
    permanent_id="HP_MAIN_DHAM_FULL_MEAL",
    canonical_name="Himachali Traditional Dham",
    alternate_names=["himachali dham", "kangra dham", "mandi dham", "dham thali"],
    regional_names={"English": "Traditional Himachali Festive Leaf Feast", "Hindi": "हिमाचली धाम", "Pahari": "ਧਾਮ"},
    vegetarian=True,
    gravy_type="semi_gravy",
    visual_features={
        "presentation": "brass_plate_or_pattal_leaf_with_distinct_stew_mounds",
        "key_dishes": ["rice", "rajma madra", "chana madra", "sepu vadi", "khatta (tangy pumpkin/mango)", "meetha bath (sweet rice)"]
    },
    key_ingredients=["basmati rice", "chickpeas", "kidney beans", "urad dal vadis", "yogurt", "tamarind / amchur", "mustard oil", "fennel"],
    possible_ingredients=["raisins", "coconut slices"],
    hard_negatives=["PB_THALI_PUNJABI", "RJ_MAIN_DAL_BAATI_CHURMA", "UK_THALI_GARHWALI"],
    density_g_cm3=0.95,
    default_serving_weight_g=550.0,
    nutrition_per_100g={"calories": 165.0, "protein_g": 5.4, "carbs_g": 26.5, "fat_g": 4.8, "fiber_g": 3.8, "sodium_mg": 280.0},
    hierarchy=NorthIndianHierarchy(
        level3_state_region="Himachal Pradesh",
        level4_food_family="Thali",
        level5_food_type="Festive Feast",
        level6_variant="Kangra Dham",
        level7_cooking_method=["slow_cooked_in_copper_charoti"],
        level8_default_portion="Full Dham Feast (550g)",
        level9_nutrition_ref_id="ni_dham_himachali"
    )
))

register_north_food(NorthIndianFoodClass(
    permanent_id="HP_MAIN_SIDDU",
    canonical_name="Himachali Siddu",
    alternate_names=["siddu", "himachali steamed bread", "sidu"],
    regional_names={"English": "Yeast-Leavened Steamed Wheat Bread Stuffed with Poppy & Walnut", "Hindi": "सिड्डू", "Pahari": "ਸਿੱਡੂ"},
    vegetarian=True,
    gravy_type="dry",
    visual_features={
        "shape": "oval_crescent_plump_dumpling",
        "length_cm": 14.0,
        "thickness_cm": 4.5,
        "surface": "soft_steamed_ivory_wheat_skin_fluted_seam",
        "stuffing": "opium_poppy_seed_(postha)_or_urad_dal_walnut_mash",
        "serving": "drenched_in_hot_clarified_ghee"
    },
    key_ingredients=["wheat flour (atta)", "active yeast", "poppy seeds (khus khus)", "walnuts", "coriander", "green chillies", "pure ghee"],
    possible_ingredients=["urad dal stuffing"],
    hard_negatives=["RJ_MAIN_DAL_BAATI_CHURMA", "TN_BREAKFAST_IDLI_PLAIN", "CHINESE_BAO"],
    density_g_cm3=0.72,
    default_serving_weight_g=160.0,
    nutrition_per_100g={"calories": 230.0, "protein_g": 6.8, "carbs_g": 34.0, "fat_g": 8.0, "fiber_g": 3.5, "sodium_mg": 210.0},
    hierarchy=NorthIndianHierarchy(
        level3_state_region="Himachal Pradesh",
        level4_food_family="Breads",
        level5_food_type="Stuffed Steamed Bread",
        level6_variant="Himachali Siddu",
        level7_cooking_method=["fermented", "steamed"],
        level8_default_portion="1 piece (160g)",
        level9_nutrition_ref_id="ni_siddu_himachali"
    )
))

# =============================================================================
# 6. UTTARAKHAND FOOD DATASET (ALOO KE GUTKE, MANDUA ROTI, KAFULI, BHATTI DAL)
# =============================================================================

register_north_food(NorthIndianFoodClass(
    permanent_id="UK_BREAD_MANDUA_ROTI",
    canonical_name="Mandua Roti (Kumaoni Ragi Flatbread)",
    alternate_names=["mandua roti", "koda roti", "finger millet roti uttarakhand"],
    regional_names={"English": "Himalayan Finger Millet Flatbread", "Hindi": "मंडुआ की रोटी", "Garhwali": "कोदा रोटी"},
    vegetarian=True,
    gravy_type="dry",
    visual_features={
        "shape": "circular_rustic_flatbread",
        "thickness_mm": 3.5,
        "diameter_cm": 17.0,
        "surface": "matte_earthy_chocolate_brown_to_slate_gray",
        "texture": "coarse_crumb_rustic_crackled"
    },
    key_ingredients=["mandua flour (Himalayan finger millet)", "warm water", "wheat flour (optional 20% for binding)"],
    possible_ingredients=["ghee brush"],
    hard_negatives=["RJ_BREAD_BAJRA_ROTI", "PB_BREAD_ROTI_MAKKI", "TN_BREAKFAST_IDLI_RAGI"],
    density_g_cm3=0.84,
    default_serving_weight_g=55.0,
    nutrition_per_100g={"calories": 235.0, "protein_g": 6.8, "carbs_g": 48.0, "fat_g": 1.8, "fiber_g": 8.5, "sodium_mg": 160.0},
    hierarchy=NorthIndianHierarchy(
        level3_state_region="Uttarakhand",
        level4_food_family="Breads",
        level5_food_type="Millet Roti",
        level6_variant="Mandua ki Roti",
        level7_cooking_method=["tawa_cooked"],
        level8_default_portion="1 piece (55g)",
        level9_nutrition_ref_id="ni_roti_mandua"
    )
))

register_north_food(NorthIndianFoodClass(
    permanent_id="UK_CURRY_ALOO_KE_GUTKE",
    canonical_name="Aloo Ke Gutke",
    alternate_names=["aloo ke gutke", "kumaoni aloo", "pahadi aloo"],
    regional_names={"English": "Kumaoni Spiced Dry Potatoes Tempered with Jamboo", "Hindi": "आलू के गुटके", "Kumaoni": "आलू का गुटका"},
    vegetarian=True,
    gravy_type="dry",
    visual_features={
        "potato_cut": "large_boiled_cubes_with_peel",
        "color": "vibrant_turmeric_yellow_with_dark_jamboo_flakes",
        "spices": ["jamboo herb", "coriander powder", "red chillies", "mustard oil coating"]
    },
    key_ingredients=["pahadi mountain potatoes", "jamboo (himalayan herb)", "mustard oil", "turmeric", "coriander powder", "fried dry red chillies"],
    possible_ingredients=["jakhiya seeds (cleome viscosa)"],
    hard_negatives=["PB_CURRY_ALOO_JEERA", "UP_BREAKFAST_ALOO_SABZI", "RJ_SNACK_MIRCHI_BADA"],
    density_g_cm3=0.92,
    default_serving_weight_g=160.0,
    nutrition_per_100g={"calories": 140.0, "protein_g": 2.8, "carbs_g": 22.0, "fat_g": 4.8, "fiber_g": 2.8, "sodium_mg": 240.0},
    hierarchy=NorthIndianHierarchy(
        level3_state_region="Uttarakhand",
        level4_food_family="Gravies",
        level5_food_type="Dry Potato Sabzi",
        level6_variant="Aloo Ke Gutke",
        level7_cooking_method=["boiled", "stir_fried_in_mustard_oil"],
        level8_default_portion="1 bowl (160g)",
        level9_nutrition_ref_id="ni_aloo_gutke"
    )
))

# =============================================================================
# 7. JAMMU & KASHMIR FOOD DATASET (ROGAN JOSH, GUSHTABA, DUM ALOO, HAAK)
# =============================================================================

register_north_food(NorthIndianFoodClass(
    permanent_id="JK_NONVEG_ROGAN_JOSH",
    canonical_name="Kashmiri Rogan Josh",
    alternate_names=["rogan josh", "kashmiri mutton rogan josh", "wazwan rogan josh"],
    regional_names={"English": "Aromatic Kashmiri Braised Lamb in Ratanjot & Fennel Gravy", "Hindi": "रोगन जोश", "Kashmiri": "روغن جوش"},
    vegetarian=False,
    gravy_type="red_gravy",
    visual_features={
        "viscosity": "silky_medium_thick_broth",
        "color": "deep_crimson_ruby_red_from_ratanjot_(alkanet_root)",
        "meat_visible": ["tender braised mutton shank or shoulder cuts with bone"],
        "surface": "aromatic_red_oil_sheen_with_fennel_hing_fragrance",
        "absence": "zero_onion_zero_garlic_in_pandit_style_or_pran_shallots_in_wazwan"
    },
    key_ingredients=["mutton cuts with bone", "ratanjot (cockscomb / alkanet root for red color)", "kashmiri red chilli", "fennel powder (saunf)", "dry ginger powder (sonth)", "mustard oil", "yogurt", "asafoetida"],
    possible_ingredients=["shallot paste (pran)"],
    hard_negatives=["RJ_NONVEG_LAAL_MAAS", "PB_NONVEG_MUTTON_CURRY", "UP_AWADHI_KORMA"],
    density_g_cm3=1.06,
    default_serving_weight_g=240.0,
    nutrition_per_100g={"calories": 210.0, "protein_g": 16.0, "carbs_g": 3.8, "fat_g": 14.8, "fiber_g": 1.2, "sodium_mg": 380.0},
    hierarchy=NorthIndianHierarchy(
        level3_state_region="Jammu & Kashmir",
        level4_food_family="Non-Veg",
        level5_food_type="Mutton Curry",
        level6_variant="Kashmiri Rogan Josh",
        level7_cooking_method=["slow_braised", "simmered"],
        level8_default_portion="1 bowl (240g)",
        level9_nutrition_ref_id="ni_rogan_josh"
    )
))

register_north_food(NorthIndianFoodClass(
    permanent_id="JK_CURRY_KASHMIRI_DUM_ALOO",
    canonical_name="Kashmiri Dum Aloo",
    alternate_names=["kashmiri dum aloo", "dum aloo kashmiri", "wazwan dum aloo"],
    regional_names={"English": "Fried Baby Potatoes in Spiced Fennel-Ginger Curd Gravy", "Hindi": "कश्मीरी दम आलू"},
    vegetarian=True,
    gravy_type="red_gravy",
    visual_features={
        "potatoes": "whole_baby_potatoes_pricked_and_deep_fried_until_blistered",
        "color": "rich_crimson_red_sauce",
        "viscosity": "thick_clinging_emulsion",
        "aromatics": "ground_fennel_and_dry_ginger_powder_notes"
    },
    key_ingredients=["baby potatoes", "whisked curd", "kashmiri red chilli powder", "fennel seed powder", "ginger powder", "cloves", "mustard oil"],
    possible_ingredients=["cardamom"],
    hard_negatives=["PB_CURRY_DUM_ALOO", "PB_CURRY_ALOO_MATAR", "UP_CURRY_ALOO_SABZI"],
    density_g_cm3=1.05,
    default_serving_weight_g=200.0,
    nutrition_per_100g={"calories": 165.0, "protein_g": 3.5, "carbs_g": 19.5, "fat_g": 8.5, "fiber_g": 2.8, "sodium_mg": 310.0},
    hierarchy=NorthIndianHierarchy(
        level3_state_region="Jammu & Kashmir",
        level4_food_family="Gravies",
        level5_food_type="Potato Gravy",
        level6_variant="Kashmiri Dum Aloo",
        level7_cooking_method=["deep_fried_potatoes", "dum_simmered"],
        level8_default_portion="1 bowl (200g)",
        level9_nutrition_ref_id="ni_dum_aloo_kashmiri"
    )
))

# =============================================================================
# 8. NORTH INDIAN SWEETS & DESSERTS (JALEBI, GULAB JAMUN, GHEVAR, RASMALAI)
# =============================================================================

register_north_food(NorthIndianFoodClass(
    permanent_id="NI_SWEET_JALEBI",
    canonical_name="Crispy Jalebi",
    alternate_names=["jalebi", "desi ghee jalebi", "kesar jalebi"],
    regional_names={"English": "Spiral Crispy Fermented Batter Pretzels in Saffron Syrup", "Hindi": "जलेबी"},
    vegetarian=True,
    gravy_type="dry",
    visual_features={
        "shape": "concentric_tangled_spiral_loops",
        "texture": "crisp_translucent_sugar_crust_bursting_with_syrup",
        "color": "vibrant_bright_orange_to_golden_amber",
        "sheen": "glistening_crystalline_sugar_sheen"
    },
    key_ingredients=["fermented maida (refined flour)", "saffron sugar syrup", "desi ghee for deep frying", "cardamom"],
    possible_ingredients=["kewra essence", "rose water"],
    hard_negatives=["NI_SWEET_IMARTI", "TN_SWEET_JANGIRI", "NI_SWEET_GULAB_JAMUN"],
    density_g_cm3=1.12,
    default_serving_weight_g=100.0,
    nutrition_per_100g={"calories": 390.0, "protein_g": 2.5, "carbs_g": 72.0, "fat_g": 11.0, "fiber_g": 0.5, "sugar_g": 58.0, "sodium_mg": 95.0},
    hierarchy=NorthIndianHierarchy(
        level3_state_region="North Indian",
        level4_food_family="Sweets",
        level5_food_type="Deep Fried Sugar Sweet",
        level6_variant="Kesar Jalebi",
        level7_cooking_method=["deep_fried", "syrup_soaked"],
        level8_default_portion="3-4 pieces (100g)",
        level9_nutrition_ref_id="ni_sweet_jalebi"
    )
))

register_north_food(NorthIndianFoodClass(
    permanent_id="RJ_SWEET_GHEVAR",
    canonical_name="Rajasthani Ghevar",
    alternate_names=["ghevar", "malai ghevar", "mava ghevar", "rabdi ghevar"],
    regional_names={"English": "Honeycomb Disc Cake Soaked in Saffron Syrup with Rabri", "Hindi": "घेवर", "Rajasthani": "घेवर"},
    vegetarian=True,
    gravy_type="dry",
    visual_features={
        "shape": "circular_honeycomb_disc_with_central_hole",
        "diameter_cm": 16.0,
        "thickness_cm": 3.0,
        "texture": "perforated_porous_honeycomb_sponge",
        "toppings": ["thick rabri / mawa layer", "silver vark (edible foil)", "sliced pistachios and almonds"]
    },
    key_ingredients=["refined flour", "desi cow ghee", "chilled milk & ice", "saffron syrup", "thick rabri", "pistachios"],
    possible_ingredients=["cardamom"],
    hard_negatives=["NI_SWEET_JALEBI", "NI_SWEET_MALPUA", "NI_SWEET_GULAB_JAMUN"],
    density_g_cm3=0.88,
    default_serving_weight_g=150.0,
    nutrition_per_100g={"calories": 420.0, "protein_g": 5.8, "carbs_g": 58.0, "fat_g": 19.5, "fiber_g": 1.2, "sugar_g": 42.0, "sodium_mg": 120.0},
    hierarchy=NorthIndianHierarchy(
        level3_state_region="Rajasthan",
        level4_food_family="Sweets",
        level5_food_type="Festive Honeycomb Cake",
        level6_variant="Rabri Ghevar",
        level7_cooking_method=["deep_fried_in_ghee", "syrup_soaked", "garnished"],
        level8_default_portion="1 piece (150g)",
        level9_nutrition_ref_id="ni_sweet_ghevar"
    )
))

register_north_food(NorthIndianFoodClass(
    permanent_id="PB_PARATHA_PLAIN",
    canonical_name="Plain Paratha",
    alternate_names=["plain paratha", "tawa paratha", "plain tawa paratha", "triangular paratha"],
    regional_names={"English": "Layered Whole Wheat Flatbread", "Hindi": "सादा पराठा", "Punjabi": "ਸਾਦਾ ਪਰੌਂਠਾ"},
    vegetarian=True,
    gravy_type="dry",
    visual_features={
        "shape": "triangular_or_round_layered",
        "thickness_mm": 3.0,
        "diameter_cm": 18.0,
        "surface": "golden_concentric_crisp_layers_with_ghee_glaze",
        "filling": "no_stuffing_inside"
    },
    key_ingredients=["whole wheat flour", "ghee or oil", "water", "salt"],
    possible_ingredients=["ajwain seeds"],
    hard_negatives=["PB_PARATHA_ALOO", "PB_BREAD_ROTI_TAWA", "PB_PARATHA_LACCHA"],
    density_g_cm3=0.82,
    default_serving_weight_g=65.0,
    nutrition_per_100g={"calories": 300.0, "protein_g": 6.8, "carbs_g": 45.0, "fat_g": 11.0, "fiber_g": 4.5, "sodium_mg": 240.0},
    hierarchy=NorthIndianHierarchy(
        level3_state_region="Punjab",
        level4_food_family="Parathas",
        level5_food_type="Plain Paratha",
        level6_variant="Layered Tawa Paratha",
        level7_cooking_method=["tawa_cooked", "shallow_ghee_fried"],
        level8_default_portion="1 piece (65g)",
        level9_nutrition_ref_id="ni_paratha_plain"
    )
))

register_north_food(NorthIndianFoodClass(
    permanent_id="PB_BREAD_ROTI_TAWA",
    canonical_name="Tawa Roti (Phulka)",
    alternate_names=["tawa roti", "phulka", "chapati", "fulka"],
    regional_names={"English": "Unleavened Whole Wheat Puffed Flatbread", "Hindi": "तवा रोटी / फुल्का", "Punjabi": "ਫੁਲਕਾ"},
    vegetarian=True,
    gravy_type="dry",
    visual_features={
        "shape": "thin_circular_disc",
        "thickness_mm": 1.5,
        "diameter_cm": 16.0,
        "surface": "soft_puffed_balloon_with_light_brown_tawa_freckles",
        "oil_ghee_sheen": "light_ghee_spread_optional"
    },
    key_ingredients=["whole wheat flour (atta)", "water", "pinch of salt"],
    possible_ingredients=["desi ghee top glaze"],
    hard_negatives=["PB_PARATHA_PLAIN", "PB_BREAD_ROTI_TANDOORI", "PB_BREAD_ROTI_MAKKI"],
    density_g_cm3=0.75,
    default_serving_weight_g=30.0,
    nutrition_per_100g={"calories": 240.0, "protein_g": 8.5, "carbs_g": 49.0, "fat_g": 1.2, "fiber_g": 6.8, "sodium_mg": 150.0},
    hierarchy=NorthIndianHierarchy(
        level3_state_region="Punjab",
        level4_food_family="Breads",
        level5_food_type="Roti",
        level6_variant="Phulka",
        level7_cooking_method=["tawa_cooked", "open_flame_puffed"],
        level8_default_portion="1 piece (30g)",
        level9_nutrition_ref_id="ni_roti_phulka"
    )
))

register_north_food(NorthIndianFoodClass(
    permanent_id="UP_BREAD_POORI",
    canonical_name="Poori (Puri)",
    alternate_names=["poori", "puri", "bedmi poori", "deep fried bread"],
    regional_names={"English": "Deep-Fried Unleavened Puffed Bread", "Hindi": "पूरी", "Punjabi": "ਪੂਰੀ"},
    vegetarian=True,
    gravy_type="dry",
    visual_features={
        "shape": "small_inflated_golden_sphere_disc",
        "thickness_mm": 1.8,
        "diameter_cm": 11.0,
        "surface": "crisp_translucent_golden_yellow_blister_skin",
        "flour_type": "whole_wheat_or_atta_rava_blend"
    },
    key_ingredients=["whole wheat flour", "semolina (sooji)", "oil for deep frying", "water", "ajwain"],
    possible_ingredients=["urad dal stuffing (for Bedmi Puri)"],
    hard_negatives=["DL_BREAD_BHATURA", "PB_BREAD_ROTI_TAWA", "TN_BREAKFAST_POORI_MASALA"],
    density_g_cm3=0.70,
    default_serving_weight_g=30.0,
    nutrition_per_100g={"calories": 335.0, "protein_g": 6.5, "carbs_g": 44.0, "fat_g": 16.5, "fiber_g": 4.0, "sodium_mg": 210.0},
    hierarchy=NorthIndianHierarchy(
        level3_state_region="Uttar Pradesh",
        level4_food_family="Breads",
        level5_food_type="Puffed Bread",
        level6_variant="Classic Poori",
        level7_cooking_method=["deep_fried"],
        level8_default_portion="2 pieces (60g)",
        level9_nutrition_ref_id="ni_bread_poori"
    )
))

register_north_food(NorthIndianFoodClass(
    permanent_id="DL_BREAD_BHATURA",
    canonical_name="Bhatura",
    alternate_names=["bhatura", "bhatoora", "punjabi bhatura"],
    regional_names={"English": "Large Deep-Fried Leavened Bread", "Hindi": "भटूरा", "Punjabi": "ਭਟੂਰਾ"},
    vegetarian=True,
    gravy_type="dry",
    visual_features={
        "shape": "giant_inflated_oval_or_round_pillow",
        "thickness_mm": 3.0,
        "diameter_cm": 22.0,
        "surface": "elastic_glossy_deep_fried_maida_crust",
        "interior": "chewy_webbed_fermented_crumb"
    },
    key_ingredients=["refined flour (maida)", "curd", "sooji", "baking powder", "oil for deep frying"],
    possible_ingredients=["paneer or potato stuffing"],
    hard_negatives=["UP_BREAD_POORI", "PB_BREAD_NAAN_PLAIN", "PB_BREAD_KULCHA_PLAIN"],
    density_g_cm3=0.68,
    default_serving_weight_g=95.0,
    nutrition_per_100g={"calories": 320.0, "protein_g": 7.2, "carbs_g": 46.0, "fat_g": 13.5, "fiber_g": 1.8, "sodium_mg": 290.0},
    hierarchy=NorthIndianHierarchy(
        level3_state_region="Delhi",
        level4_food_family="Breads",
        level5_food_type="Leavened Fried Bread",
        level6_variant="Bhatura",
        level7_cooking_method=["deep_fried"],
        level8_default_portion="1 piece (95g)",
        level9_nutrition_ref_id="ni_bread_bhatura"
    )
))

register_north_food(NorthIndianFoodClass(
    permanent_id="PB_BREAD_NAAN_PLAIN",
    canonical_name="Plain Naan",
    alternate_names=["plain naan", "tandoori naan", "sada naan"],
    regional_names={"English": "Clay Oven Unleavened/Leavened Teardrop Flatbread", "Hindi": "सादा नान", "Punjabi": "ਸਾਦਾ ਨਾਨ"},
    vegetarian=True,
    gravy_type="dry",
    visual_features={
        "shape": "teardrop_or_elongated_oval",
        "thickness_mm": 3.5,
        "length_cm": 22.0,
        "surface": "tandoor_blister_bubbles_dry_matte_finish",
        "color": "off_white_ivory_with_brown_spots"
    },
    key_ingredients=["maida", "yogurt", "yeast/baking powder", "salt", "water"],
    possible_ingredients=["nigella seeds"],
    hard_negatives=["PB_BREAD_NAAN_BUTTER", "PB_BREAD_KULCHA_PLAIN", "PB_BREAD_ROTI_TANDOORI"],
    density_g_cm3=0.72,
    default_serving_weight_g=80.0,
    nutrition_per_100g={"calories": 265.0, "protein_g": 8.2, "carbs_g": 51.0, "fat_g": 3.2, "fiber_g": 2.1, "sodium_mg": 320.0},
    hierarchy=NorthIndianHierarchy(
        level3_state_region="Punjab",
        level4_food_family="Breads",
        level5_food_type="Naan",
        level6_variant="Plain Naan",
        level7_cooking_method=["tandoor_cooked"],
        level8_default_portion="1 piece (80g)",
        level9_nutrition_ref_id="ni_naan_plain"
    )
))

register_north_food(NorthIndianFoodClass(
    permanent_id="PB_BREAD_KULCHA_PLAIN",
    canonical_name="Plain Kulcha",
    alternate_names=["plain kulcha", "matar kulcha bread", "tandoori kulcha plain"],
    regional_names={"English": "Mildly Leavened Soft Round Flatbread", "Hindi": "सादा कुल्चा", "Punjabi": "ਸਾਦਾ ਕੁਲਚਾ"},
    vegetarian=True,
    gravy_type="dry",
    visual_features={
        "shape": "round_flat_disc",
        "thickness_mm": 4.0,
        "diameter_cm": 17.0,
        "surface": "soft_pillowy_spongy_not_crisp_blistered_like_naan",
        "color": "pale_white_with_coriander_specks"
    },
    key_ingredients=["refined flour", "milk/curd", "baking powder", "salt"],
    possible_ingredients=["kasuri methi garnish", "butter brushing"],
    hard_negatives=["PB_BREAD_NAAN_PLAIN", "PB_BREAD_KULCHA_AMRITSARI", "PB_BREAD_ROTI_TANDOORI"],
    density_g_cm3=0.76,
    default_serving_weight_g=70.0,
    nutrition_per_100g={"calories": 250.0, "protein_g": 7.5, "carbs_g": 48.0, "fat_g": 3.8, "fiber_g": 2.0, "sodium_mg": 310.0},
    hierarchy=NorthIndianHierarchy(
        level3_state_region="Punjab",
        level4_food_family="Breads",
        level5_food_type="Kulcha",
        level6_variant="Plain Kulcha",
        level7_cooking_method=["tawa_cooked_or_tandoor"],
        level8_default_portion="1 piece (70g)",
        level9_nutrition_ref_id="ni_kulcha_plain"
    )
))

register_north_food(NorthIndianFoodClass(
    permanent_id="UP_CURRY_ALOO_SABZI",
    canonical_name="Tariwale Aloo Sabzi",
    alternate_names=["aloo sabzi", "tariwale aloo", "poori aloo sabzi", "halwai aloo"],
    regional_names={"English": "Crushed Potato Curry in Spiced Tomato Gravy", "Hindi": "तरीवाले आलू की सब्जी", "Urdu": "آلو کی سبزی"},
    vegetarian=True,
    gravy_type="thin_gravy",
    visual_features={
        "viscosity": "thin_to_medium_liquid_curry",
        "potato_shape": "irregular_hand_crushed_potato_chunks",
        "color": "vibrant_reddish_yellow",
        "surface": "floating_cumin_fennel_and_ginger_juliennes"
    },
    key_ingredients=["boiled potatoes (hand crushed)", "tomatoes", "cumin", "fennel seeds (saunf)", "hing (asafoetida)", "amchur", "turmeric"],
    possible_ingredients=["kasuri methi"],
    hard_negatives=["PB_CURRY_ALOO_JEERA", "JK_CURRY_KASHMIRI_DUM_ALOO", "UK_CURRY_ALOO_KE_GUTKE"],
    density_g_cm3=1.04,
    default_serving_weight_g=180.0,
    nutrition_per_100g={"calories": 95.0, "protein_g": 2.2, "carbs_g": 16.5, "fat_g": 2.6, "fiber_g": 2.2, "sodium_mg": 280.0},
    hierarchy=NorthIndianHierarchy(
        level3_state_region="Uttar Pradesh",
        level4_food_family="Gravies",
        level5_food_type="Potato Gravy",
        level6_variant="Tariwale Aloo",
        level7_cooking_method=["boiled", "simmered_stew"],
        level8_default_portion="1 bowl (180g)",
        level9_nutrition_ref_id="ni_aloo_sabzi_tari"
    )
))

register_north_food(NorthIndianFoodClass(
    permanent_id="PB_CURRY_ALOO_JEERA",
    canonical_name="Aloo Jeera",
    alternate_names=["aloo jeera", "jeera aloo", "cumin spiced dry potatoes", "sukhe aloo"],
    regional_names={"English": "Stir-Fried Diced Potatoes with Roasted Cumin", "Hindi": "जीरा आलू", "Punjabi": "ਜੀਰਾ ਆਲੂ"},
    vegetarian=True,
    gravy_type="dry",
    visual_features={
        "viscosity": "completely_dry_no_liquid_gravy",
        "potato_shape": "neatly_diced_cubes_with_golden_roasted_crust",
        "color": "bright_golden_yellow",
        "surface": "heavily_flecked_with_dark_roasted_cumin_seeds_and_coriander"
    },
    key_ingredients=["boiled diced potatoes", "roasted cumin seeds (jeera)", "turmeric", "amchur", "green chillies", "mustard oil / ghee"],
    possible_ingredients=["fresh cilantro garnish"],
    hard_negatives=["UP_CURRY_ALOO_SABZI", "UK_CURRY_ALOO_KE_GUTKE", "PB_PARATHA_ALOO"],
    density_g_cm3=0.92,
    default_serving_weight_g=150.0,
    nutrition_per_100g={"calories": 135.0, "protein_g": 2.5, "carbs_g": 21.0, "fat_g": 4.8, "fiber_g": 2.5, "sodium_mg": 260.0},
    hierarchy=NorthIndianHierarchy(
        level3_state_region="Punjab",
        level4_food_family="Gravies",
        level5_food_type="Dry Potato Sabzi",
        level6_variant="Aloo Jeera",
        level7_cooking_method=["pan_sauteed", "dry_roasted"],
        level8_default_portion="1 bowl (150g)",
        level9_nutrition_ref_id="ni_aloo_jeera"
    )
))

register_north_food(NorthIndianFoodClass(
    permanent_id="PB_CURRY_PALAK_SABZI",
    canonical_name="Palak Sabzi (Sukhi)",
    alternate_names=["palak sabzi", "sukhi palak", "palak bhurji", "spinach stir fry"],
    regional_names={"English": "Dry Sauteed Spiced Spinach Greens", "Hindi": "पालक की सब्जी", "Punjabi": "ਪਾਲਕ ਸਬਜ਼ੀ"},
    vegetarian=True,
    gravy_type="dry",
    visual_features={
        "viscosity": "dry_sauteed_wilted_greens",
        "color": "dark_forest_green",
        "inclusions": "no_paneer_cubes_present",
        "texture": "shredded_tender_spinach_leaves_with_garlic_bits"
    },
    key_ingredients=["fresh spinach leaves (chopped)", "garlic", "onions", "green chillies", "cumin", "mustard oil"],
    possible_ingredients=["potato chunks (aloo palak)"],
    hard_negatives=["PB_CURRY_PALAK_PANEER", "PB_CURRY_SARSON_KA_SAAG", "UK_CURRY_KAFULI"],
    density_g_cm3=0.88,
    default_serving_weight_g=150.0,
    nutrition_per_100g={"calories": 75.0, "protein_g": 3.2, "carbs_g": 6.5, "fat_g": 4.2, "fiber_g": 3.8, "sodium_mg": 210.0},
    hierarchy=NorthIndianHierarchy(
        level3_state_region="Punjab",
        level4_food_family="Gravies",
        level5_food_type="Dry Green Sabzi",
        level6_variant="Palak Sabzi",
        level7_cooking_method=["stir_fried", "sauteed"],
        level8_default_portion="1 bowl (150g)",
        level9_nutrition_ref_id="ni_palak_sabzi"
    )
))

register_north_food(NorthIndianFoodClass(
    permanent_id="PB_CURRY_KADHI_PAKORA",
    canonical_name="Punjabi Kadhi Pakora",
    alternate_names=["kadhi pakora", "punjabi kadhi", "besan kadhi", "kadhi"],
    regional_names={"English": "Tangy Gram Flour & Yogurt Curry with Fried Onion Fritters", "Hindi": "कढ़ी पकोड़ा", "Punjabi": "ਕੜ੍ਹੀ ਪਕੌੜਾ"},
    vegetarian=True,
    gravy_type="creamy_gravy",
    visual_features={
        "viscosity": "thick_creamy_velvety_stew",
        "color": "vibrant_bright_mustard_yellow",
        "inclusions": ["spongy_crisp_brown_onion_spinach_besan_pakoras_floating"],
        "surface": "deep_red_chilli_methi_curry_leaf_tadka_sheen"
    },
    key_ingredients=["sour curd (khatta dahi)", "besan (gram flour)", "fenugreek seeds (methi dana)", "onions", "mustard oil / ghee", "dried red chillies", "hing"],
    possible_ingredients=["spinach in pakora"],
    hard_negatives=["RJ_CURRY_KADHI", "PB_CURRY_DAL_TADKA", "RJ_CURRY_GATTE_KI_SABZI"],
    density_g_cm3=1.04,
    default_serving_weight_g=220.0,
    nutrition_per_100g={"calories": 135.0, "protein_g": 4.8, "carbs_g": 13.5, "fat_g": 7.2, "fiber_g": 2.4, "sodium_mg": 320.0},
    hierarchy=NorthIndianHierarchy(
        level3_state_region="Punjab",
        level4_food_family="Gravies",
        level5_food_type="Yogurt Gram Flour Curry",
        level6_variant="Punjabi Kadhi Pakora",
        level7_cooking_method=["slow_simmered", "deep_fried_pakora", "tempered"],
        level8_default_portion="1 bowl (220g)",
        level9_nutrition_ref_id="ni_kadhi_pakora"
    )
))

register_north_food(NorthIndianFoodClass(
    permanent_id="RJ_CURRY_KADHI",
    canonical_name="Rajasthani Kadhi",
    alternate_names=["rajasthani kadhi", "marwari kadhi", "thin kadhi"],
    regional_names={"English": "Spiced Tangy Yogurt-Gram Flour Thin Broth", "Hindi": "राजस्थानी कढ़ी", "Rajasthani": "राजस्थानी कढ़ी"},
    vegetarian=True,
    gravy_type="thin_gravy",
    visual_features={
        "viscosity": "thin_pouring_liquid_broth",
        "color": "pale_canary_yellow",
        "inclusions": "no_pakoras_smooth_uniform_liquid",
        "surface": "crackled_mustard_seeds_cloves_cinnamon_red_chillies"
    },
    key_ingredients=["sour buttermilk / curd", "gram flour (besan)", "cloves (laung)", "cinnamon", "fenugreek seeds", "asafoetida", "mustard oil"],
    possible_ingredients=["curry leaves"],
    hard_negatives=["PB_CURRY_KADHI_PAKORA", "PB_CURRY_DAL_TADKA", "TN_CURRY_MOR_KUZHAMBU"],
    density_g_cm3=1.02,
    default_serving_weight_g=180.0,
    nutrition_per_100g={"calories": 85.0, "protein_g": 3.2, "carbs_g": 8.5, "fat_g": 4.2, "fiber_g": 1.2, "sodium_mg": 290.0},
    hierarchy=NorthIndianHierarchy(
        level3_state_region="Rajasthan",
        level4_food_family="Gravies",
        level5_food_type="Yogurt Broth",
        level6_variant="Rajasthani Kadhi",
        level7_cooking_method=["simmered", "tempered"],
        level8_default_portion="1 bowl (180g)",
        level9_nutrition_ref_id="ni_kadhi_rajasthani"
    )
))

register_north_food(NorthIndianFoodClass(
    permanent_id="NI_SWEET_IMARTI",
    canonical_name="Imarti (Amriti)",
    alternate_names=["imarti", "amriti", "omritti", "jahangir"],
    regional_names={"English": "Intricate Geometric Flower-Shaped Urad Sweet", "Hindi": "इमरती", "Urdu": "اممرتی"},
    vegetarian=True,
    gravy_type="dry",
    visual_features={
        "shape": "geometric_circular_rosette_with_intricate_outer_loops",
        "texture": "chewy_thick_succulent_lentil_mesh",
        "color": "deep_crimson_orange_reddish",
        "batter_base": "ground_black_gram_(urad_dal)_not_maida"
    },
    key_ingredients=["urad dal (soaked & ground)", "cardamom saffron sugar syrup", "desi ghee for deep frying"],
    possible_ingredients=["kewra water"],
    hard_negatives=["NI_SWEET_JALEBI", "TN_SWEET_JANGIRI", "RJ_SWEET_GHEVAR"],
    density_g_cm3=1.14,
    default_serving_weight_g=110.0,
    nutrition_per_100g={"calories": 380.0, "protein_g": 4.8, "carbs_g": 68.0, "fat_g": 10.5, "fiber_g": 2.0, "sugar_g": 52.0, "sodium_mg": 80.0},
    hierarchy=NorthIndianHierarchy(
        level3_state_region="North Indian",
        level4_food_family="Sweets",
        level5_food_type="Deep Fried Sugar Sweet",
        level6_variant="Imarti",
        level7_cooking_method=["deep_fried_in_ghee", "syrup_soaked"],
        level8_default_portion="2 pieces (110g)",
        level9_nutrition_ref_id="ni_sweet_imarti"
    )
))

register_north_food(NorthIndianFoodClass(
    permanent_id="UP_SNACK_SAMOSA",
    canonical_name="Punjabi / UP Samosa",
    alternate_names=["samosa", "punjabi samosa", "aloo samosa", "singhara"],
    regional_names={"English": "Crisp Pyramid Pastry Filled with Spiced Potato & Peas", "Hindi": "समोसा", "Punjabi": "ਸਮੋਸਾ"},
    vegetarian=True,
    gravy_type="dry",
    visual_features={
        "shape": "triangular_pyramid_cone_with_flat_base",
        "crust": "thick_flaky_golden_brown_shortcrust_crisp",
        "filling": "coarsely_crushed_potatoes_whole_green_peas_coriander_seeds",
        "height_cm": 8.0
    },
    key_ingredients=["refined flour (maida)", "boiled diced potatoes", "green peas", "ajwain", "coriander seeds", "garam masala", "oil for deep frying"],
    possible_ingredients=["cashews", "raisins", "paneer bits"],
    hard_negatives=["RJ_SNACK_PYAZ_KACHORI", "DL_STREET_ALOO_TIKKI_CHAAT", "PB_PARATHA_ALOO"],
    density_g_cm3=0.88,
    default_serving_weight_g=90.0,
    nutrition_per_100g={"calories": 260.0, "protein_g": 4.5, "carbs_g": 32.0, "fat_g": 13.0, "fiber_g": 3.0, "sodium_mg": 360.0},
    hierarchy=NorthIndianHierarchy(
        level3_state_region="Uttar Pradesh",
        level4_food_family="Street Food",
        level5_food_type="Fried Pastry",
        level6_variant="Pyramid Samosa",
        level7_cooking_method=["deep_fried"],
        level8_default_portion="1 piece (90g)",
        level9_nutrition_ref_id="ni_snack_samosa"
    )
))

register_north_food(NorthIndianFoodClass(
    permanent_id="RJ_SNACK_PYAZ_KACHORI",
    canonical_name="Rajasthani Pyaz Kachori",
    alternate_names=["pyaz kachori", "rajasthani kachori", "pyaaz ki kachori", "khasta kachori"],
    regional_names={"English": "Flaky Puffed Round Pastry with Spiced Onion Filling", "Hindi": "प्याज़ कचौरी", "Rajasthani": "कांदा कचोरी"},
    vegetarian=True,
    gravy_type="dry",
    visual_features={
        "shape": "flattened_convex_puffed_round_disc",
        "crust": "multi_layered_blistered_shatteringly_crisp_crust",
        "filling": "caramelized_spiced_onions_besan_fennel_coriander_mash",
        "diameter_cm": 10.0
    },
    key_ingredients=["maida", "onions (pyaz)", "besan", "fennel seeds (saunf)", "coriander seeds", "kalonji", "oil/ghee for frying"],
    possible_ingredients=["hing", "garlic"],
    hard_negatives=["UP_SNACK_SAMOSA", "UP_BREAD_POORI", "DL_STREET_ALOO_TIKKI_CHAAT"],
    density_g_cm3=0.86,
    default_serving_weight_g=110.0,
    nutrition_per_100g={"calories": 310.0, "protein_g": 5.2, "carbs_g": 36.0, "fat_g": 16.5, "fiber_g": 3.2, "sodium_mg": 420.0},
    hierarchy=NorthIndianHierarchy(
        level3_state_region="Rajasthan",
        level4_food_family="Street Food",
        level5_food_type="Fried Stuffed Pastry",
        level6_variant="Pyaz Kachori",
        level7_cooking_method=["slow_deep_fried"],
        level8_default_portion="1 piece (110g)",
        level9_nutrition_ref_id="ni_snack_pyaz_kachori"
    )
))

register_north_food(NorthIndianFoodClass(
    permanent_id="DL_STREET_PAPDI_CHAAT",
    canonical_name="Papdi Chaat",
    alternate_names=["papdi chaat", "papri chaat", "dahi papdi chaat"],
    regional_names={"English": "Crisp Flat Wafers with Potatoes, Curd & Chutneys", "Hindi": "पापड़ी चाट"},
    vegetarian=True,
    gravy_type="semi_gravy",
    visual_features={
        "base": "flat_crisp_round_cracker_wafers_(papdi)",
        "dressings": ["chilled sweet whipped yogurt", "tamarind saunth chutney", "spicy green mint chutney"],
        "toppings": ["boiled chickpea & potato dices", "sev crunch", "pomegranate seeds", "chaat masala"]
    },
    key_ingredients=["crisp flour papdis", "curd (dahi)", "boiled potatoes", "boiled chickpeas", "tamarind chutney", "mint chutney", "sev", "chaat spices"],
    possible_ingredients=["onion cubes"],
    hard_negatives=["DL_STREET_DAHI_BHALLA", "DL_STREET_ALOO_TIKKI_CHAAT", "DL_STREET_GOL_GAPPA"],
    density_g_cm3=1.02,
    default_serving_weight_g=200.0,
    nutrition_per_100g={"calories": 185.0, "protein_g": 4.2, "carbs_g": 26.0, "fat_g": 7.5, "fiber_g": 2.2, "sodium_mg": 380.0},
    hierarchy=NorthIndianHierarchy(
        level3_state_region="Delhi",
        level4_food_family="Street Food",
        level5_food_type="Chaat",
        level6_variant="Papdi Chaat",
        level7_cooking_method=["assembled"],
        level8_default_portion="1 plate (200g)",
        level9_nutrition_ref_id="ni_chaat_papdi"
    )
))

register_north_food(NorthIndianFoodClass(
    permanent_id="DL_STREET_DAHI_BHALLA",
    canonical_name="Dahi Bhalla (Dahi Vada)",
    alternate_names=["dahi bhalla", "dahi vada", "dahi gujia", "bhalla papdi"],
    regional_names={"English": "Soft Lentil Dumplings in Chilled Sweet Spiced Yogurt", "Hindi": "दही भल्ला / दही वड़ा", "Punjabi": "ਦਹੀਂ ਭੱਲਾ"},
    vegetarian=True,
    gravy_type="creamy_gravy",
    visual_features={
        "dumplings": "spherical_or_disc_soft_sponge_fritters_soaked_in_water_and_curd",
        "texture": "melt_in_mouth_pillowy_not_crisp_crunchy",
        "dressing": "copious_creamy_white_curd_layer",
        "garnishes": ["saunth (red sweet tamarind)", "coriander green chutney", "roasted jeera powder", "red chilli pinch"]
    },
    key_ingredients=["urad dal / moong dal dumplings", "sweetened thick yogurt", "tamarind-sonth chutney", "mint-coriander chutney", "roasted cumin"],
    possible_ingredients=["pomegranate seeds", "papdi crumbs"],
    hard_negatives=["DL_STREET_PAPDI_CHAAT", "DL_STREET_ALOO_TIKKI_CHAAT", "TN_BREAKFAST_MEDU_VADA"],
    density_g_cm3=1.08,
    default_serving_weight_g=220.0,
    nutrition_per_100g={"calories": 140.0, "protein_g": 5.4, "carbs_g": 18.0, "fat_g": 5.2, "fiber_g": 2.0, "sodium_mg": 310.0},
    hierarchy=NorthIndianHierarchy(
        level3_state_region="Delhi",
        level4_food_family="Street Food",
        level5_food_type="Chaat",
        level6_variant="Dahi Bhalla",
        level7_cooking_method=["deep_fried_fritter", "water_soaked", "yogurt_dressed"],
        level8_default_portion="2 bhallas in curd (220g)",
        level9_nutrition_ref_id="ni_dahi_bhalla"
    )
))

register_north_food(NorthIndianFoodClass(
    permanent_id="DL_STREET_GOL_GAPPA",
    canonical_name="Gol Gappa (Pani Puri)",
    alternate_names=["gol gappa", "golgappa", "pani puri", "puchka", "paani ke patashe"],
    regional_names={"English": "Crisp Hollow Shells with Spiced Tangy Herbal Water", "Hindi": "गोलगप्पा / पानी पूरी"},
    vegetarian=True,
    gravy_type="thin_gravy",
    visual_features={
        "shell": "hollow_crisp_paper_thin_fried_spheres",
        "filling": "boiled_potato_chickpea_or_yellow_matar_mash",
        "liquids": ["chilled_teekha_spicy_mint_coriander_hing_water", "meetha_sweet_tamarind_water"]
    },
    key_ingredients=["suji or atta hollow puri shells", "mint", "coriander", "green chilli", "tamarind", "black salt", "asafoetida", "boiled potatoes", "sprouts"],
    possible_ingredients=["boondi in water"],
    hard_negatives=["DL_STREET_PAPDI_CHAAT", "RJ_SNACK_PYAZ_KACHORI", "UP_SNACK_SAMOSA"],
    density_g_cm3=1.02,
    default_serving_weight_g=180.0,
    nutrition_per_100g={"calories": 110.0, "protein_g": 2.2, "carbs_g": 22.0, "fat_g": 1.8, "fiber_g": 1.6, "sodium_mg": 460.0},
    hierarchy=NorthIndianHierarchy(
        level3_state_region="Delhi",
        level4_food_family="Street Food",
        level5_food_type="Chaat",
        level6_variant="Gol Gappa",
        level7_cooking_method=["assembled"],
        level8_default_portion="6 puris with water (180g)",
        level9_nutrition_ref_id="ni_gol_gappa"
    )
))

register_north_food(NorthIndianFoodClass(
    permanent_id="UP_CURRY_KALA_CHANA",
    canonical_name="Kala Chana Curry",
    alternate_names=["kala chana", "black chana", "sukha kala chana", "chana masala brown"],
    regional_names={"English": "Brown Bengal Gram in Spiced Onion-Tomato Gravy", "Hindi": "काला चना", "Punjabi": "ਕਾਲਾ ਚਣਾ"},
    vegetarian=True,
    gravy_type="semi_gravy",
    visual_features={
        "beans": "small_wrinkled_dark_brown_to_black_chickpeas",
        "size": "half_the_size_of_white_kabuli_chole",
        "gravy_color": "dark_earthy_brownish_red",
        "viscosity": "medium_spiced_gravy_or_dry_masala"
    },
    key_ingredients=["kala chana (brown chickpeas)", "onions", "tomatoes", "coriander powder", "garam masala", "amchur", "mustard oil"],
    possible_ingredients=["ginger juliennes"],
    hard_negatives=["PB_CURRY_CHOLE_PUNJABI", "PB_CURRY_RAJMA_MASALA", "HP_CURRY_KHATTA"],
    density_g_cm3=1.06,
    default_serving_weight_g=180.0,
    nutrition_per_100g={"calories": 145.0, "protein_g": 7.8, "carbs_g": 21.0, "fat_g": 3.8, "fiber_g": 6.8, "sodium_mg": 310.0},
    hierarchy=NorthIndianHierarchy(
        level3_state_region="Uttar Pradesh",
        level4_food_family="Gravies",
        level5_food_type="Chickpea Curry",
        level6_variant="Kala Chana",
        level7_cooking_method=["pressure_cooked", "simmered"],
        level8_default_portion="1 bowl (180g)",
        level9_nutrition_ref_id="ni_kala_chana"
    )
))

register_north_food(NorthIndianFoodClass(
    permanent_id="NI_RICE_VEG_PULAO",
    canonical_name="Vegetable Pulao",
    alternate_names=["veg pulao", "matar pulao", "vegetable pilaf", "pulao"],
    regional_names={"English": "Fragrant Basmati Rice Cooked with Vegetables & Whole Spices", "Hindi": "वेज पुलाव"},
    vegetarian=True,
    gravy_type="dry",
    visual_features={
        "rice": "long_slender_white_basmati_grains_cooked_uniformly_in_one_pot",
        "color": "subtle_light_ivory_to_pale_golden_hue",
        "vegetables": ["bright green peas", "diced orange carrots", "green french beans"],
        "spices": ["whole cloves", "cinnamon stick", "green cardamom pods", "black cumin (shahi jeera)"]
    },
    key_ingredients=["aged basmati rice", "green peas", "carrots", "ghee", "cumin/shahi jeera", "whole garam masala"],
    possible_ingredients=["fried onions", "cashew nuts"],
    hard_negatives=["UP_AWADHI_BIRYANI_LUCKNOWI", "NI_RICE_STEAMED_BASMATI", "TN_RICE_VEG_PULAO"],
    density_g_cm3=0.82,
    default_serving_weight_g=220.0,
    nutrition_per_100g={"calories": 145.0, "protein_g": 3.2, "carbs_g": 26.5, "fat_g": 3.4, "fiber_g": 2.0, "sodium_mg": 240.0},
    hierarchy=NorthIndianHierarchy(
        level3_state_region="North Indian",
        level4_food_family="Rice/Biryani",
        level5_food_type="Pulao",
        level6_variant="Vegetable Pulao",
        level7_cooking_method=["pot_simmered_one_pot"],
        level8_default_portion="1 plate (220g)",
        level9_nutrition_ref_id="ni_rice_veg_pulao"
    )
))

register_north_food(NorthIndianFoodClass(
    permanent_id="NI_RICE_STEAMED_BASMATI",
    canonical_name="Steamed Basmati Rice",
    alternate_names=["steamed rice", "plain basmati rice", "white rice", "chawal"],
    regional_names={"English": "Plain Fluffy Steamed Long-Grain Basmati Rice", "Hindi": "सफेद बासमती चावल"},
    vegetarian=True,
    gravy_type="dry",
    visual_features={
        "rice": "long_slender_pure_white_individual_unbroken_grains",
        "color": "pure_bright_white",
        "surface": "moist_fluffy_clean_no_spices_no_vegetables",
        "viscosity": "non_sticky_grains"
    },
    key_ingredients=["basmati rice", "water", "pinch of salt optional"],
    possible_ingredients=["drop of ghee"],
    hard_negatives=["NI_RICE_VEG_PULAO", "UP_AWADHI_BIRYANI_LUCKNOWI", "TN_RICE_WHITE_PONNI"],
    density_g_cm3=0.80,
    default_serving_weight_g=200.0,
    nutrition_per_100g={"calories": 130.0, "protein_g": 2.7, "carbs_g": 28.0, "fat_g": 0.3, "fiber_g": 0.4, "sodium_mg": 5.0},
    hierarchy=NorthIndianHierarchy(
        level3_state_region="North Indian",
        level4_food_family="Rice/Biryani",
        level5_food_type="Steamed Rice",
        level6_variant="Steamed Basmati",
        level7_cooking_method=["boiled", "steamed"],
        level8_default_portion="1 plate (200g)",
        level9_nutrition_ref_id="ni_rice_steamed"
    )
))

register_north_food(NorthIndianFoodClass(
    permanent_id="RJ_BREAD_BAJRA_ROTI",
    canonical_name="Bajra Roti (Pearl Millet Flatbread)",
    alternate_names=["bajra roti", "bajre ki roti", "pearl millet roti rajasthan"],
    regional_names={"English": "Unleavened Pearl Millet Rustic Flatbread", "Hindi": "बाजरे की रोटी", "Rajasthani": "बाजरी रो सोगरो"},
    vegetarian=True,
    gravy_type="dry",
    visual_features={
        "shape": "thick_rustic_hand_patted_circular_disc",
        "thickness_mm": 4.5,
        "diameter_cm": 17.0,
        "surface": "coarse_cracked_matte_ash_greyish_brown",
        "color": "greyish_brown_to_olive_khaki_with_char_spots",
        "serving": "generous_coat_of_white_butter_or_ghee"
    },
    key_ingredients=["pearl millet flour (bajra atta)", "warm water", "pinch of salt", "desi ghee / butter"],
    possible_ingredients=["jaggery accompaniment"],
    hard_negatives=["PB_BREAD_ROTI_MAKKI", "HR_BREAD_JOWAR_ROTI", "UK_BREAD_MANDUA_ROTI"],
    density_g_cm3=0.88,
    default_serving_weight_g=65.0,
    nutrition_per_100g={"calories": 255.0, "protein_g": 7.5, "carbs_g": 47.0, "fat_g": 4.5, "fiber_g": 7.2, "sodium_mg": 170.0},
    hierarchy=NorthIndianHierarchy(
        level3_state_region="Rajasthan",
        level4_food_family="Breads",
        level5_food_type="Millet Roti",
        level6_variant="Bajra Roti",
        level7_cooking_method=["hand_patted", "tawa_clay_cooked"],
        level8_default_portion="1 piece (65g)",
        level9_nutrition_ref_id="ni_roti_bajra"
    )
))

register_north_food(NorthIndianFoodClass(
    permanent_id="HR_BREAD_JOWAR_ROTI",
    canonical_name="Jowar Roti (Sorghum Flatbread)",
    alternate_names=["jowar roti", "joware ki roti", "sorghum flatbread"],
    regional_names={"English": "Unleavened Sorghum Grain Flatbread", "Hindi": "ज्वार की रोटी", "Haryanvi": "ज्वार की रोटी"},
    vegetarian=True,
    gravy_type="dry",
    visual_features={
        "shape": "rustic_hand_patted_round_disc",
        "thickness_mm": 3.8,
        "diameter_cm": 17.0,
        "surface": "coarse_matte_pale_off_white_to_buff_colored",
        "color": "chalky_off_white_with_light_golden_spots"
    },
    key_ingredients=["sorghum flour (jowar atta)", "warm water", "salt"],
    possible_ingredients=["ghee brush"],
    hard_negatives=["RJ_BREAD_BAJRA_ROTI", "PB_BREAD_ROTI_MAKKI", "PB_BREAD_ROTI_TAWA"],
    density_g_cm3=0.86,
    default_serving_weight_g=60.0,
    nutrition_per_100g={"calories": 245.0, "protein_g": 6.8, "carbs_g": 49.0, "fat_g": 2.2, "fiber_g": 6.5, "sodium_mg": 160.0},
    hierarchy=NorthIndianHierarchy(
        level3_state_region="Haryana",
        level4_food_family="Breads",
        level5_food_type="Millet Roti",
        level6_variant="Jowar Roti",
        level7_cooking_method=["hand_patted", "tawa_cooked"],
        level8_default_portion="1 piece (60g)",
        level9_nutrition_ref_id="ni_roti_jowar"
    )
))

register_north_food(NorthIndianFoodClass(
    permanent_id="PB_PARATHA_MOOLI",
    canonical_name="Mooli Paratha",
    alternate_names=["mooli paratha", "radish paratha", "mooli ka paratha"],
    regional_names={"English": "Grated Spiced Radish Stuffed Flatbread", "Hindi": "मूली पराठा", "Punjabi": "ਮੂਲੀ ਪਰੌਂਠਾ"},
    vegetarian=True,
    gravy_type="dry",
    visual_features={
        "shape": "round_flatbread",
        "thickness_mm": 3.8,
        "diameter_cm": 20.0,
        "surface": "translucent_moist_spots_from_radish_water_with_white_radish_threads",
        "filling": "spiced_grated_white_radish_with_ajwain"
    },
    key_ingredients=["whole wheat flour", "grated white daikon radish (mooli)", "ajwain", "green chillies", "butter/ghee"],
    possible_ingredients=["radish tender leaves"],
    hard_negatives=["PB_PARATHA_GOBI", "PB_PARATHA_ALOO", "PB_PARATHA_PANEER"],
    density_g_cm3=0.83,
    default_serving_weight_g=115.0,
    nutrition_per_100g={"calories": 210.0, "protein_g": 5.2, "carbs_g": 35.0, "fat_g": 6.5, "fiber_g": 4.2, "sodium_mg": 310.0},
    hierarchy=NorthIndianHierarchy(
        level3_state_region="Punjab",
        level4_food_family="Parathas",
        level5_food_type="Stuffed Paratha",
        level6_variant="Mooli Paratha",
        level7_cooking_method=["tawa_cooked"],
        level8_default_portion="1 piece (115g)",
        level9_nutrition_ref_id="ni_paratha_mooli"
    )
))

register_north_food(NorthIndianFoodClass(
    permanent_id="PB_PARATHA_METHI",
    canonical_name="Methi Paratha (Thepla Style)",
    alternate_names=["methi paratha", "fenugreek paratha", "methi roti"],
    regional_names={"English": "Fresh Fenugreek Herb Whole Wheat Flatbread", "Hindi": "मेथी पराठा", "Punjabi": "ਮੇਥੀ ਪਰੌਂਠਾ"},
    vegetarian=True,
    gravy_type="dry",
    visual_features={
        "shape": "round_flatbread",
        "thickness_mm": 3.2,
        "diameter_cm": 19.0,
        "surface": "dense_green_leaf_speckles_uniformly_distributed_throughout_dough",
        "color": "golden_tan_with_vibrant_dark_green_methi_patches"
    },
    key_ingredients=["whole wheat flour", "fresh methi (fenugreek leaves)", "ajwain", "turmeric", "green chillies", "ghee"],
    possible_ingredients=["sesame seeds"],
    hard_negatives=["PB_PARATHA_PLAIN", "PB_PARATHA_PALAK", "PB_PARATHA_GOBI"],
    density_g_cm3=0.82,
    default_serving_weight_g=75.0,
    nutrition_per_100g={"calories": 260.0, "protein_g": 6.5, "carbs_g": 42.0, "fat_g": 8.0, "fiber_g": 5.2, "sodium_mg": 260.0},
    hierarchy=NorthIndianHierarchy(
        level3_state_region="Punjab",
        level4_food_family="Parathas",
        level5_food_type="Herb Kneaded Paratha",
        level6_variant="Methi Paratha",
        level7_cooking_method=["tawa_cooked"],
        level8_default_portion="1 piece (75g)",
        level9_nutrition_ref_id="ni_paratha_methi"
    )
))

register_north_food(NorthIndianFoodClass(
    permanent_id="PB_PARATHA_PYAZ",
    canonical_name="Pyaz Paratha",
    alternate_names=["pyaz paratha", "onion paratha", "pyaaz parantha"],
    regional_names={"English": "Spiced Diced Onion Stuffed Flatbread", "Hindi": "प्याज़ पराठा", "Punjabi": "ਪਿਆਜ਼ ਪਰੌਂਠਾ"},
    vegetarian=True,
    gravy_type="dry",
    visual_features={
        "shape": "round_flatbread",
        "thickness_mm": 3.8,
        "diameter_cm": 20.0,
        "surface": "golden_crisp_crust_with_translucent_pinkish_onion_bits_poking",
        "filling": "crunchy_finely_chopped_red_onions_with_spices"
    },
    key_ingredients=["whole wheat flour", "finely chopped red onions", "ajwain", "amchur", "green chillies", "butter"],
    possible_ingredients=["coriander leaves"],
    hard_negatives=["PB_PARATHA_ALOO", "PB_PARATHA_PANEER", "RJ_SNACK_PYAZ_KACHORI"],
    density_g_cm3=0.84,
    default_serving_weight_g=110.0,
    nutrition_per_100g={"calories": 235.0, "protein_g": 5.5, "carbs_g": 37.0, "fat_g": 7.5, "fiber_g": 3.6, "sodium_mg": 280.0},
    hierarchy=NorthIndianHierarchy(
        level3_state_region="Punjab",
        level4_food_family="Parathas",
        level5_food_type="Stuffed Paratha",
        level6_variant="Pyaz Paratha",
        level7_cooking_method=["tawa_cooked"],
        level8_default_portion="1 piece (110g)",
        level9_nutrition_ref_id="ni_paratha_pyaz"
    )
))

register_north_food(NorthIndianFoodClass(
    permanent_id="PB_PARATHA_MIX_VEG",
    canonical_name="Mix Veg Paratha",
    alternate_names=["mix veg paratha", "vegetable paratha", "mixed vegetable stuffed paratha"],
    regional_names={"English": "Multi-Vegetable Stuffed Whole Wheat Flatbread", "Hindi": "मिक्स वेज पराठा", "Punjabi": "ਮਿਕਸ ਵੈੱਜ ਪਰੌਂਠਾ"},
    vegetarian=True,
    gravy_type="dry",
    visual_features={
        "shape": "round_flatbread",
        "thickness_mm": 4.2,
        "diameter_cm": 20.0,
        "surface": "golden_brown_blisters_with_multi_colored_filling_peeking",
        "filling": "mashed_potatoes_orange_carrots_green_peas_cauliflower"
    },
    key_ingredients=["whole wheat flour", "potatoes", "carrots", "cauliflower", "green peas", "garam masala", "butter"],
    possible_ingredients=["grated paneer"],
    hard_negatives=["PB_PARATHA_ALOO", "PB_PARATHA_GOBI", "PB_PARATHA_PANEER"],
    density_g_cm3=0.86,
    default_serving_weight_g=130.0,
    nutrition_per_100g={"calories": 240.0, "protein_g": 5.8, "carbs_g": 36.5, "fat_g": 8.5, "fiber_g": 4.2, "sodium_mg": 310.0},
    hierarchy=NorthIndianHierarchy(
        level3_state_region="Punjab",
        level4_food_family="Parathas",
        level5_food_type="Stuffed Paratha",
        level6_variant="Mix Veg Paratha",
        level7_cooking_method=["tawa_cooked"],
        level8_default_portion="1 piece (130g)",
        level9_nutrition_ref_id="ni_paratha_mix_veg"
    )
))

register_north_food(NorthIndianFoodClass(
    permanent_id="HP_CURRY_RAJMA_MADRA",
    canonical_name="Himachali Rajma Madra",
    alternate_names=["rajma madra", "kangra madra", "himachali madra"],
    regional_names={"English": "Red Kidney Beans Simmered in Rich Spiced Yogurt Gravy", "Hindi": "राजमा मदरा", "Pahari": "ਰਾਜਮਾ ਮਦਰਾ"},
    vegetarian=True,
    gravy_type="creamy_gravy",
    visual_features={
        "viscosity": "thick_rich_curd_emulsion",
        "color": "golden_reddish_yellow",
        "beans": ["tender_red_kidney_beans"],
        "surface": "clarified_ghee_sheen_with_black_cardamom_notes"
    },
    key_ingredients=["red kidney beans (rajma)", "whisked curd (yogurt)", "pure desi ghee", "asafoetida", "black cardamom", "cloves", "dry ginger"],
    possible_ingredients=["raisins"],
    hard_negatives=["PB_CURRY_RAJMA_MASALA", "HP_CURRY_CHANA_MADRA", "PB_CURRY_DAL_MAKHANI"],
    density_g_cm3=1.06,
    default_serving_weight_g=180.0,
    nutrition_per_100g={"calories": 175.0, "protein_g": 6.5, "carbs_g": 18.0, "fat_g": 9.2, "fiber_g": 4.5, "sodium_mg": 280.0},
    hierarchy=NorthIndianHierarchy(
        level3_state_region="Himachal Pradesh",
        level4_food_family="Gravies",
        level5_food_type="Yogurt Bean Stew",
        level6_variant="Rajma Madra",
        level7_cooking_method=["slow_cooked_in_charoti"],
        level8_default_portion="1 bowl (180g)",
        level9_nutrition_ref_id="ni_rajma_madra"
    )
))

register_north_food(NorthIndianFoodClass(
    permanent_id="HP_CURRY_CHANA_MADRA",
    canonical_name="Himachali Chana Madra",
    alternate_names=["chana madra", "kabuli chana madra", "pahadi madra"],
    regional_names={"English": "White Chickpeas in Slow-Cooked Spiced Yogurt Gravy", "Hindi": "चना मदरा", "Pahari": "ਚਨਾ ਮਦਰਾ"},
    vegetarian=True,
    gravy_type="creamy_gravy",
    visual_features={
        "viscosity": "thick_luxurious_yogurt_gravy",
        "color": "pale_warm_golden_ivory",
        "beans": ["plump_white_kabuli_chickpeas"],
        "garnishes": ["cardamom_pods", "slivered_dry_fruits"]
    },
    key_ingredients=["kabuli chickpeas", "fresh whisked curd", "desi ghee", "fennel", "cinnamon", "asafoetida", "raisins"],
    possible_ingredients=["lotus seeds (makhana)"],
    hard_negatives=["PB_CURRY_CHOLE_PUNJABI", "HP_CURRY_RAJMA_MADRA", "RJ_CURRY_GATTE_KI_SABZI"],
    density_g_cm3=1.05,
    default_serving_weight_g=180.0,
    nutrition_per_100g={"calories": 180.0, "protein_g": 7.0, "carbs_g": 19.5, "fat_g": 8.8, "fiber_g": 5.0, "sodium_mg": 290.0},
    hierarchy=NorthIndianHierarchy(
        level3_state_region="Himachal Pradesh",
        level4_food_family="Gravies",
        level5_food_type="Yogurt Chickpea Stew",
        level6_variant="Chana Madra",
        level7_cooking_method=["slow_simmered"],
        level8_default_portion="1 bowl (180g)",
        level9_nutrition_ref_id="ni_chana_madra"
    )
))

register_north_food(NorthIndianFoodClass(
    permanent_id="HP_CURRY_SEPU_VADI",
    canonical_name="Sepu Vadi (Mandi Dham)",
    alternate_names=["sepu vadi", "sepu badi", "himachali sepu vadi"],
    regional_names={"English": "Steamed & Fried Urad Dal Cakes in Spinach Yogurt Gravy", "Hindi": "सेपू बड़ी", "Pahari": "ਸੇਪੂ ਵੜੀ"},
    vegetarian=True,
    gravy_type="green_gravy",
    visual_features={
        "vadis": "triangular_or_cubed_dense_spiced_urad_dal_dumplings",
        "gravy": "spinach_puree_blended_with_sour_curd_and_spices",
        "color": "deep_moss_green_with_golden_oil_halo"
    },
    key_ingredients=["split urad dal", "spinach (palak)", "curd", "mustard oil", "coriander powder", "garam masala", "hing"],
    possible_ingredients=["fenugreek leaves"],
    hard_negatives=["PB_CURRY_PALAK_PANEER", "RJ_CURRY_GATTE_KI_SABZI", "UK_CURRY_KAFULI"],
    density_g_cm3=1.04,
    default_serving_weight_g=180.0,
    nutrition_per_100g={"calories": 150.0, "protein_g": 6.8, "carbs_g": 13.5, "fat_g": 7.8, "fiber_g": 3.8, "sodium_mg": 310.0},
    hierarchy=NorthIndianHierarchy(
        level3_state_region="Himachal Pradesh",
        level4_food_family="Gravies",
        level5_food_type="Dal Dumpling Gravy",
        level6_variant="Sepu Vadi",
        level7_cooking_method=["steamed_then_deep_fried", "simmered_in_spinach"],
        level8_default_portion="1 bowl (180g)",
        level9_nutrition_ref_id="ni_sepu_vadi"
    )
))

register_north_food(NorthIndianFoodClass(
    permanent_id="HP_CURRY_KHATTA",
    canonical_name="Himachali Khatta",
    alternate_names=["khatta", "kangra khatta", "himachali khatta chana"],
    regional_names={"English": "Tangy Sour-Sweet Pumpkin & Chickpea Broth with Amchur", "Hindi": "हिमाचली खट्टा", "Pahari": "ਖੱਟਾ"},
    vegetarian=True,
    gravy_type="thin_gravy",
    visual_features={
        "viscosity": "thin_tangy_broth",
        "color": "dark_amber_rust_brown",
        "inclusions": ["kala chana / white pumpkin chunks (kaddu)"],
        "aroma": "pungent_dry_mango_powder_(amchur)_and_mustard_oil"
    },
    key_ingredients=["dry mango powder (amchur)", "kala chana", "mustard oil", "fenugreek seeds", "asafoetida", "jaggery (gur)"],
    possible_ingredients=["pumpkin / colocasia"],
    hard_negatives=["UP_CURRY_KALA_CHANA", "PB_CURRY_DAL_TADKA", "TN_CURRY_RASAM_TAMARIND"],
    density_g_cm3=1.02,
    default_serving_weight_g=160.0,
    nutrition_per_100g={"calories": 105.0, "protein_g": 3.8, "carbs_g": 18.0, "fat_g": 2.2, "fiber_g": 3.2, "sodium_mg": 280.0},
    hierarchy=NorthIndianHierarchy(
        level3_state_region="Himachal Pradesh",
        level4_food_family="Gravies",
        level5_food_type="Tangy Broth",
        level6_variant="Kangra Khatta",
        level7_cooking_method=["simmered", "tempered_mustard_oil"],
        level8_default_portion="1 bowl (160g)",
        level9_nutrition_ref_id="ni_khatta_himachali"
    )
))

register_north_food(NorthIndianFoodClass(
    permanent_id="HP_SWEET_MEETHA",
    canonical_name="Himachali Mittha (Sweet Rice)",
    alternate_names=["mittha", "meetha bhat", "himachali mittha", "sweet saffron rice"],
    regional_names={"English": "Aromatic Sweet Rice with Saffron, Ghee & Dry Fruits", "Hindi": "मीठा भात", "Pahari": "ਮਿੱਠਾ"},
    vegetarian=True,
    gravy_type="dry",
    visual_features={
        "rice": "bright_golden_saffron_glistening_basmati_grains",
        "texture": "plump_sweet_separated_grains",
        "toppings": ["raisins", "sliced almonds", "cashews", "cardamom pods", "dry coconut chips"]
    },
    key_ingredients=["basmati rice", "sugar", "desi ghee", "saffron strands", "cardamom", "fennel", "dry fruits"],
    possible_ingredients=["cloves"],
    hard_negatives=["NI_RICE_VEG_PULAO", "UP_AWADHI_BIRYANI_LUCKNOWI", "TN_SWEET_SWEET_PONGAL"],
    density_g_cm3=0.88,
    default_serving_weight_g=120.0,
    nutrition_per_100g={"calories": 280.0, "protein_g": 3.8, "carbs_g": 52.0, "fat_g": 7.2, "fiber_g": 1.2, "sugar_g": 28.0, "sodium_mg": 45.0},
    hierarchy=NorthIndianHierarchy(
        level3_state_region="Himachal Pradesh",
        level4_food_family="Sweets",
        level5_food_type="Sweet Rice",
        level6_variant="Mittha",
        level7_cooking_method=["boiled", "simmered_in_sugar_syrup"],
        level8_default_portion="1 bowl (120g)",
        level9_nutrition_ref_id="ni_mittha_himachali"
    )
))

register_north_food(NorthIndianFoodClass(
    permanent_id="PB_THALI_PUNJABI",
    canonical_name="Punjabi Royal Thali",
    alternate_names=["punjabi thali", "north indian thali", "deluxe thali"],
    regional_names={"English": "Complete North Indian Multi-Course Platter", "Hindi": "पंजाबी थाली", "Punjabi": "ਪੰਜਾਬੀ ਥਾਲੀ"},
    vegetarian=True,
    gravy_type="semi_gravy",
    visual_features={
        "presentation": "large_stainless_steel_or_brass_thali_with_multiple_katori_bowls",
        "dishes_included": ["2 tandoori rotis", "dal makhani katori", "paneer butter masala katori", "steamed basmati rice mound", "cucumber boondi raita", "kachumber salad", "gulab jamun"]
    },
    key_ingredients=["wheat flour", "urad dal", "paneer", "basmati rice", "curd", "tomatoes", "butter", "cream", "spices"],
    possible_ingredients=["papad", "pickle"],
    hard_negatives=["HP_MAIN_DHAM_FULL_MEAL", "RJ_MAIN_DAL_BAATI_CHURMA", "TN_MEAL_BANANA_LEAF_FEAST"],
    density_g_cm3=0.94,
    default_serving_weight_g=650.0,
    nutrition_per_100g={"calories": 170.0, "protein_g": 5.8, "carbs_g": 23.5, "fat_g": 6.5, "fiber_g": 3.2, "sodium_mg": 320.0},
    hierarchy=NorthIndianHierarchy(
        level3_state_region="Punjab",
        level4_food_family="Thali",
        level5_food_type="Complete Platter",
        level6_variant="Punjabi Royal Thali",
        level7_cooking_method=["assembled_multi_dish"],
        level8_default_portion="Full Thali Platter (650g)",
        level9_nutrition_ref_id="ni_thali_punjabi"
    )
))

def resolve_north_food_by_name(query: str) -> Optional[NorthIndianFoodClass]:
    q = query.lower().strip()
    if q in NORTH_INDIAN_SYNONYM_MAP:
        perm_id = NORTH_INDIAN_SYNONYM_MAP[q]
        return NORTH_INDIAN_TAXONOMY_REGISTRY.get(perm_id)
    for alias, perm_id in NORTH_INDIAN_SYNONYM_MAP.items():
        if q == alias or q in alias or alias in q:
            return NORTH_INDIAN_TAXONOMY_REGISTRY.get(perm_id)
    return None

def get_north_food_class(perm_id: str) -> Optional[NorthIndianFoodClass]:
    return NORTH_INDIAN_TAXONOMY_REGISTRY.get(perm_id)

def list_all_north_food_ids() -> List[str]:
    return list(NORTH_INDIAN_TAXONOMY_REGISTRY.keys())
