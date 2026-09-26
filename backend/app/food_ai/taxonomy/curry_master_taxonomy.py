"""
Indian Dal, Curry & Gravy Master Taxonomy & Identity Hierarchy (Part 11)
Implements Sections 0–3, 7, 10, 12–16, 18–22, 24–29, 31, 56, 72, 74 of Part 11.

Guarantees:
- Strict Hierarchical Identity Traversal:
  INDIAN FOOD -> CURRY / GRAVY / DAL / SEMI-DRY DISH -> REGION / STATE ->
  FOOD FAMILY (23 families) -> SPECIFIC DISH -> VARIANT -> MAIN INGREDIENT ->
  GRAVY BASE -> COOKING METHOD -> PORTION -> WEIGHT -> NUTRITION
- 23 Master Food Families:
  A. Dal (CURRY_DAL_*)
  B. Sambar (CURRY_SAMBAR_*)
  C. Rasam (CURRY_RASAM_*)
  D. Kuzhambu (CURRY_KUZHAMBU_*)
  E. Kootu (CURRY_KOOTU_*)
  F. Kadhi (CURRY_KADHI_*)
  G. Vegetable Curry (CURRY_VEG_*)
  H. Paneer Curry (CURRY_PANEER_*)
  I. Legume Curry (CURRY_LEGUME_*)
  J. Chicken Curry (CURRY_CHICKEN_*)
  K. Mutton Curry (CURRY_MUTTON_*)
  L. Fish Curry (CURRY_FISH_*)
  M. Egg Curry (CURRY_EGG_*)
  N. Seafood Curry (CURRY_SEAFOOD_*)
  O. Kurma (CURRY_KURMA_*)
  P. Salna (CURRY_SALNA_*)
  Q. Coconut-Based Curry (CURRY_COCONUT_*)
  R. Tomato-Based Gravy
  S. Onion-Based Gravy
  T. Yogurt-Based Gravy
  U. Cream-Based Gravy
  V. Dry / Semi-Dry Poriyal (CURRY_PORIYAL_*)
  W. Regional Specialty Curry
- Fallback: CURRY_UNKNOWN_001 ("Indian curry/gravy — exact dish uncertain")
- Multilingual synonym mapping across 11 languages.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class CurryHierarchy(BaseModel):
    level1_food: str = "Indian Food"
    level2_macro_category: str = "Curry / Gravy / Dal / Semi-Dry Dish"
    level3_region: str          # South India, North India, West India, East India, Pan-India
    level4_food_family: str     # Dal, Sambar, Rasam, Kuzhambu, Kootu, Kadhi, Paneer Curry, etc.
    level5_specific_dish: str   # Dal Tadka, Drumstick Sambar, Tomato Rasam, Butter Chicken, etc.
    level6_variant: str         # e.g., "Slow-Simmered Toor Dal with Ghee Garlic Tempering"
    level7_main_ingredient: str # toor_dal, chicken, paneer, fish, drumstick, chickpea, etc.
    level8_gravy_base: str      # dal_tamarind, tomato_onion_cream, coconut_milk, yogurt_besan, etc.
    level9_cooking_method: str  # Boiled, Slow simmered, Dum cooked, Sautéed, Fried
    level10_consistency: str    # Very thin, Thin, Medium, Thick, Very thick, Semi-dry, Dry
    level11_portion_type: str   # volume_ml, weight_grams
    level12_nutrition_ref_id: str


class CurryFoodClassRecord(BaseModel):
    canonical_food_id: str
    canonical_name: str
    hierarchy: CurryHierarchy
    food_family: str
    specific_dish: str
    region: str                 # South India, North India, West India, East India, Pan-India
    state_or_city: str
    regional_names: Dict[str, str] = Field(default_factory=dict)
    alternate_names: List[str] = Field(default_factory=list)
    vegetarian: bool = True
    main_ingredient: str = "toor_dal"
    gravy_base: str = "lentil"
    cooking_method: str = "Slow simmered"
    consistency: str = "Medium"
    has_meat: bool = False
    has_bone_in_pieces: bool = False
    piece_count_expected: Optional[int] = None
    default_portion_grams: float = 150.0
    density_g_ml: float = 1.08
    nutrition_per_100g: Dict[str, float] = Field(default_factory=dict)
    uncertainty_factors: List[str] = Field(default_factory=list)
    typical_oil_level: str = "Medium"  # Low, Medium, High, Very High, Unknown


CURRY_TAXONOMY_REGISTRY: Dict[str, CurryFoodClassRecord] = {}
CURRY_SYNONYM_LOOKUP: Dict[str, str] = {}


def register_curry_food_class(record: CurryFoodClassRecord, alias_ids: Optional[List[str]] = None) -> CurryFoodClassRecord:
    CURRY_TAXONOMY_REGISTRY[record.canonical_food_id] = record
    CURRY_TAXONOMY_REGISTRY[record.canonical_food_id.lower()] = record
    if alias_ids:
        for aid in alias_ids:
            CURRY_TAXONOMY_REGISTRY[aid] = record
            CURRY_TAXONOMY_REGISTRY[aid.lower()] = record
            CURRY_SYNONYM_LOOKUP[aid.lower().strip()] = record.canonical_food_id
    CURRY_SYNONYM_LOOKUP[record.canonical_name.lower().strip()] = record.canonical_food_id
    for alt in record.alternate_names:
        CURRY_SYNONYM_LOOKUP[alt.lower().strip()] = record.canonical_food_id
    for reg_name in record.regional_names.values():
        CURRY_SYNONYM_LOOKUP[reg_name.lower().strip()] = record.canonical_food_id
    return record


# =============================================================================
# 1. DAL FAMILY (Sections 3, 5, 6)
# =============================================================================

# 1.1 Dal Tadka
register_curry_food_class(CurryFoodClassRecord(
    canonical_food_id="CURRY_DAL_TADKA",
    canonical_name="Yellow Dal Tadka",
    hierarchy=CurryHierarchy(
        level3_region="Pan-India",
        level4_food_family="Dal",
        level5_specific_dish="Dal Tadka",
        level6_variant="Yellow Lentil Tempered with Ghee, Cumin, Garlic and Dried Red Chillies",
        level7_main_ingredient="toor_dal",
        level8_gravy_base="lentil_tempered",
        level9_cooking_method="Boiled and tempered",
        level10_consistency="Medium",
        level11_portion_type="volume_ml",
        level12_nutrition_ref_id="ifct_dal_tadka"
    ),
    food_family="Dal",
    specific_dish="Dal Tadka",
    region="North / Pan-India",
    state_or_city="Pan-India / Punjab",
    regional_names={"English": "Dal Tadka", "Hindi": "दाल तड़का", "Punjabi": "ਦਾਲ ਤੜਕਾ", "Tamil": "பருப்பு தட்கா", "Telugu": "పప్పు తాలింపు"},
    alternate_names=["dal tadka", "yellow dal tadka", "toor dal tadka", "dhal tadka", "tempered dal"],
    vegetarian=True,
    main_ingredient="toor_dal",
    gravy_base="lentil_tempered",
    cooking_method="Boiled and tempered",
    consistency="Medium",
    default_portion_grams=150.0,
    density_g_ml=1.06,
    nutrition_per_100g={"calories": 95.0, "protein_g": 5.2, "carbs_g": 12.5, "fat_g": 2.8, "fiber_g": 3.2, "sodium_mg": 280.0},
    uncertainty_factors=["ghee_tadka_floating_layer", "dal_dilution"],
    typical_oil_level="Medium"
), alias_ids=["yellow_dal_tadka", "dal_tadka"])

# 1.2 Dal Fry
register_curry_food_class(CurryFoodClassRecord(
    canonical_food_id="CURRY_DAL_FRY",
    canonical_name="Dhaba Dal Fry",
    hierarchy=CurryHierarchy(
        level3_region="North India",
        level4_food_family="Dal",
        level5_specific_dish="Dal Fry",
        level6_variant="Toor and Chana Dal Sautéed with Onion, Tomato, Ginger and Spices",
        level7_main_ingredient="toor_chana_dal",
        level8_gravy_base="tomato_onion_lentil",
        level9_cooking_method="Sautéed and simmered",
        level10_consistency="Medium-Thick",
        level11_portion_type="volume_ml",
        level12_nutrition_ref_id="ifct_dal_fry"
    ),
    food_family="Dal",
    specific_dish="Dal Fry",
    region="North India",
    state_or_city="Punjab / Dhaba",
    regional_names={"English": "Dal Fry", "Hindi": "दाल फ्राई", "Marathi": "डाळ फ्राय"},
    alternate_names=["dal fry", "dhaba dal fry", "spiced dal fry"],
    vegetarian=True,
    main_ingredient="toor_dal",
    gravy_base="tomato_onion_lentil",
    cooking_method="Sautéed and simmered",
    consistency="Medium",
    default_portion_grams=160.0,
    density_g_ml=1.08,
    nutrition_per_100g={"calories": 115.0, "protein_g": 5.8, "carbs_g": 14.0, "fat_g": 4.2, "fiber_g": 3.5, "sodium_mg": 310.0},
    uncertainty_factors=["butter_oil_sauté_mass", "onion_tomato_masala_density"],
    typical_oil_level="Medium"
))

# 1.3 Dal Makhani (Section 6)
register_curry_food_class(CurryFoodClassRecord(
    canonical_food_id="CURRY_DAL_MAKHANI",
    canonical_name="Punjabi Dal Makhani",
    hierarchy=CurryHierarchy(
        level3_region="North India",
        level4_food_family="Dal",
        level5_specific_dish="Dal Makhani",
        level6_variant="Slow Overnight Simmered Black Urad and Rajma with Butter and Cream",
        level7_main_ingredient="black_urad_rajma",
        level8_gravy_base="tomato_butter_cream",
        level9_cooking_method="Slow simmered",
        level10_consistency="Thick",
        level11_portion_type="volume_ml",
        level12_nutrition_ref_id="ifct_dal_makhani"
    ),
    food_family="Dal",
    specific_dish="Dal Makhani",
    region="North India",
    state_or_city="Punjab / Delhi",
    regional_names={"English": "Dal Makhani", "Hindi": "दाल मखनी", "Punjabi": "ਦਾਲ ਮੱਖਣੀ"},
    alternate_names=["dal makhani", "makhani dal", "black dal", "maa ki dal"],
    vegetarian=True,
    main_ingredient="black_urad",
    gravy_base="tomato_butter_cream",
    cooking_method="Slow simmered",
    consistency="Thick",
    default_portion_grams=180.0,
    density_g_ml=1.12,
    nutrition_per_100g={"calories": 165.0, "protein_g": 6.2, "carbs_g": 16.5, "fat_g": 8.5, "fiber_g": 4.8, "sodium_mg": 360.0},
    uncertainty_factors=["butter_quantity", "heavy_cream_dollop", "simmering_reduction"],
    typical_oil_level="High"
))

# 1.4 Moong Dal
register_curry_food_class(CurryFoodClassRecord(
    canonical_food_id="CURRY_DAL_MOONG",
    canonical_name="Light Yellow Moong Dal",
    hierarchy=CurryHierarchy(
        level3_region="Pan-India",
        level4_food_family="Dal",
        level5_specific_dish="Moong Dal",
        level6_variant="Light Easy Digestible Split Moong Dal with Cumin and Turmeric",
        level7_main_ingredient="yellow_moong_dal",
        level8_gravy_base="lentil",
        level9_cooking_method="Boiled",
        level10_consistency="Medium-Thin",
        level11_portion_type="volume_ml",
        level12_nutrition_ref_id="ifct_dal_moong"
    ),
    food_family="Dal",
    specific_dish="Moong Dal",
    region="Pan-India",
    state_or_city="Pan-India",
    regional_names={"English": "Moong Dal", "Hindi": "मूंग दाल", "Gujarati": "મગ ની દાળ", "Bengali": "মুগ ডাল"},
    alternate_names=["moong dal", "yellow moong dal", "pesara pappu", "paasi paruppu"],
    vegetarian=True,
    main_ingredient="moong_dal",
    gravy_base="lentil",
    cooking_method="Boiled",
    consistency="Medium",
    default_portion_grams=150.0,
    density_g_ml=1.04,
    nutrition_per_100g={"calories": 78.0, "protein_g": 4.8, "carbs_g": 11.5, "fat_g": 1.2, "fiber_g": 2.8, "sodium_mg": 210.0},
    uncertainty_factors=["water_dilution"],
    typical_oil_level="Low"
))


# =============================================================================
# 2. SAMBAR FAMILY (Sections 7, 8, 9)
# =============================================================================

# 2.1 Drumstick Vegetable Sambar (Section 8)
register_curry_food_class(CurryFoodClassRecord(
    canonical_food_id="CURRY_SAMBAR_DRUMSTICK",
    canonical_name="Drumstick Sambar (Murungakkai Sambar)",
    hierarchy=CurryHierarchy(
        level3_region="South India",
        level4_food_family="Sambar",
        level5_specific_dish="Drumstick Sambar",
        level6_variant="Toor Dal and Tamarind Stew with Drumstick, Shallots and Sambar Spices",
        level7_main_ingredient="drumstick",
        level8_gravy_base="dal_tamarind",
        level9_cooking_method="Boiled and simmered",
        level10_consistency="Medium",
        level11_portion_type="volume_ml",
        level12_nutrition_ref_id="ifct_sambar_drumstick"
    ),
    food_family="Sambar",
    specific_dish="Drumstick Sambar",
    region="South India",
    state_or_city="Tamil Nadu / Kerala / Karnataka",
    regional_names={"English": "Drumstick Sambar", "Tamil": "முருங்கைக்காய் சாம்பார்", "Telugu": "మునక్కాయ సాంబార్", "Malayalam": "മുരിങ്ങക്കായ സാമ്പാർ", "Kannada": "ನುಗ್ಗೆಕಾಯಿ ಸಾಂಬಾರು"},
    alternate_names=["drumstick sambar", "murungakkai sambar", "munakkaya sambar", "nuggekai sambar", "sambar"],
    vegetarian=True,
    main_ingredient="toor_dal",
    gravy_base="dal_tamarind",
    cooking_method="Boiled and simmered",
    consistency="Medium",
    default_portion_grams=150.0,
    density_g_ml=1.06,
    nutrition_per_100g={"calories": 62.0, "protein_g": 3.1, "carbs_g": 9.2, "fat_g": 1.4, "fiber_g": 2.5, "sodium_mg": 340.0},
    uncertainty_factors=["tamarind_concentration", "drumstick_pulp_volume"],
    typical_oil_level="Low"
), alias_ids=["CURRY_SAMBAR_VEG"])

# 2.2 Tiffin / Hotel Sambar
register_curry_food_class(CurryFoodClassRecord(
    canonical_food_id="CURRY_SAMBAR_TIFFIN",
    canonical_name="South Indian Tiffin Sambar (Hotel Sambar)",
    hierarchy=CurryHierarchy(
        level3_region="South India",
        level4_food_family="Sambar",
        level5_specific_dish="Tiffin Sambar",
        level6_variant="Aromatic Yellow Sambar with Pearl Onions, Toor Dal, Lentil Flour and Jaggery Hint",
        level7_main_ingredient="small_onion",
        level8_gravy_base="dal_tamarind_shallot",
        level9_cooking_method="Boiled",
        level10_consistency="Medium-Thin",
        level11_portion_type="volume_ml",
        level12_nutrition_ref_id="ifct_sambar_tiffin"
    ),
    food_family="Sambar",
    specific_dish="Tiffin Sambar",
    region="South India",
    state_or_city="Tamil Nadu / Chennai",
    regional_names={"English": "Hotel Sambar", "Tamil": "டிபன் சாம்பார்", "Kannada": "ಹೋಟೆಲ್ ಸಾಂಬಾರ್"},
    alternate_names=["tiffin sambar", "hotel sambar", "idli sambar", "chinna vengayam sambar"],
    vegetarian=True,
    main_ingredient="toor_dal",
    gravy_base="dal_tamarind",
    cooking_method="Boiled and simmered",
    consistency="Medium",
    default_portion_grams=140.0,
    density_g_ml=1.05,
    nutrition_per_100g={"calories": 68.0, "protein_g": 2.9, "carbs_g": 10.5, "fat_g": 1.6, "fiber_g": 2.2, "sodium_mg": 320.0},
    uncertainty_factors=["jaggery_sugar_hint", "dal_density"],
    typical_oil_level="Low"
))


# =============================================================================
# 3. RASAM FAMILY (Sections 10, 11)
# =============================================================================

# 3.1 Tomato Pepper Rasam
register_curry_food_class(CurryFoodClassRecord(
    canonical_food_id="CURRY_RASAM_TOMATO",
    canonical_name="Tomato Pepper Rasam (Thakkali Rasam)",
    hierarchy=CurryHierarchy(
        level3_region="South India",
        level4_food_family="Rasam",
        level5_specific_dish="Tomato Rasam",
        level6_variant="Clear Tamarind Tomato Broth with Crushed Black Pepper, Cumin, Garlic and Coriander",
        level7_main_ingredient="tomato",
        level8_gravy_base="tomato_tamarind_pepper",
        level9_cooking_method="Boiled and simmered",
        level10_consistency="Very thin",
        level11_portion_type="volume_ml",
        level12_nutrition_ref_id="ifct_rasam_tomato"
    ),
    food_family="Rasam",
    specific_dish="Tomato Rasam",
    region="South India",
    state_or_city="Tamil Nadu / Andhra Pradesh / Karnataka / Kerala",
    regional_names={"English": "Tomato Rasam", "Tamil": "தக்காளி ரசம்", "Telugu": "టమాటా రసం / చారు", "Kannada": "ಟೊಮೆಟೊ ಸಾರು", "Malayalam": "തക്കാളി രസം"},
    alternate_names=["tomato rasam", "thakkali rasam", "milagu rasam", "pepper rasam", "charu", "saaru", "rasam"],
    vegetarian=True,
    main_ingredient="tomato",
    gravy_base="tamarind_tomato_pepper",
    cooking_method="Boiled and simmered",
    consistency="Very thin",
    default_portion_grams=120.0,
    density_g_ml=1.01,
    nutrition_per_100g={"calories": 32.0, "protein_g": 0.9, "carbs_g": 5.2, "fat_g": 0.7, "fiber_g": 0.8, "sodium_mg": 290.0},
    uncertainty_factors=["tempering_ghee_oil", "dal_water_addition"],
    typical_oil_level="Very Low"
), alias_ids=["CURRY_RASAM_PLAIN", "CURRY_RASAM_PEPPER"])

# 3.2 Mysore Rasam
register_curry_food_class(CurryFoodClassRecord(
    canonical_food_id="CURRY_RASAM_MYSORE",
    canonical_name="Mysore Rasam (Coconut Spiced)",
    hierarchy=CurryHierarchy(
        level3_region="South India",
        level4_food_family="Rasam",
        level5_specific_dish="Mysore Rasam",
        level6_variant="Toor Dal Broth with Roasted Coconut, Coriander Seeds, Ghee and Red Chillies",
        level7_main_ingredient="coconut_toor_dal",
        level8_gravy_base="dal_coconut_spice",
        level9_cooking_method="Simmered",
        level10_consistency="Thin",
        level11_portion_type="volume_ml",
        level12_nutrition_ref_id="ifct_rasam_mysore"
    ),
    food_family="Rasam",
    specific_dish="Mysore Rasam",
    region="South India",
    state_or_city="Karnataka / Mysore",
    regional_names={"English": "Mysore Rasam", "Kannada": "ಮೈಸೂರು ಸಾರು", "Tamil": "மைசூர் ரசம்"},
    alternate_names=["mysore rasam", "mysore saaru", "coconut rasam"],
    vegetarian=True,
    main_ingredient="coconut",
    gravy_base="dal_coconut_spice",
    cooking_method="Simmered",
    consistency="Thin",
    default_portion_grams=130.0,
    density_g_ml=1.03,
    nutrition_per_100g={"calories": 48.0, "protein_g": 1.5, "carbs_g": 6.8, "fat_g": 1.8, "fiber_g": 1.2, "sodium_mg": 290.0},
    uncertainty_factors=["coconut_paste_richness"],
    typical_oil_level="Low"
))


# =============================================================================
# 4. KUZHAMBU FAMILY (Section 12)
# =============================================================================

# 4.1 Kara Kuzhambu
register_curry_food_class(CurryFoodClassRecord(
    canonical_food_id="CURRY_KUZHAMBU_KARA",
    canonical_name="Chettinad Kara Kuzhambu (Ennai Kathirikai)",
    hierarchy=CurryHierarchy(
        level3_region="South India",
        level4_food_family="Kuzhambu",
        level5_specific_dish="Kara Kuzhambu",
        level6_variant="Spicy Tangy Tamarind Gravy with Brinjal, Garlic and Gingelly Oil",
        level7_main_ingredient="brinjal",
        level8_gravy_base="tamarind_sesame_oil",
        level9_cooking_method="Slow simmered",
        level10_consistency="Medium-Thick",
        level11_portion_type="volume_ml",
        level12_nutrition_ref_id="ifct_kuzhambu_kara"
    ),
    food_family="Kuzhambu",
    specific_dish="Kara Kuzhambu",
    region="South India",
    state_or_city="Tamil Nadu / Chettinad",
    regional_names={"English": "Kara Kuzhambu", "Tamil": "காரக்குழம்பு", "Telugu": "పులుసు"},
    alternate_names=["kara kuzhambu", "kara kulambu", "puli kuzhambu", "ennai kathirikai kuzhambu", "vatha kuzhambu"],
    vegetarian=True,
    main_ingredient="brinjal",
    gravy_base="tamarind_sesame_oil",
    cooking_method="Slow simmered",
    consistency="Medium",
    default_portion_grams=140.0,
    density_g_ml=1.10,
    nutrition_per_100g={"calories": 110.0, "protein_g": 2.2, "carbs_g": 12.0, "fat_g": 6.2, "fiber_g": 2.8, "sodium_mg": 380.0},
    uncertainty_factors=["gingelly_oil_layer_thickness", "tamarind_density"],
    typical_oil_level="High"
), alias_ids=["CURRY_KUZHAMBU_PULI", "CURRY_KUZHAMBU_VATHA", "CURRY_KUZHAMBU_ENNAI_KATHIRIKAI"])

# 4.2 Mor Kuzhambu (Yogurt-Coconut based)
register_curry_food_class(CurryFoodClassRecord(
    canonical_food_id="CURRY_KUZHAMBU_MOR",
    canonical_name="Mor Kuzhambu (More Kuzhambu)",
    hierarchy=CurryHierarchy(
        level3_region="South India",
        level4_food_family="Kuzhambu",
        level5_specific_dish="Mor Kuzhambu",
        level6_variant="Sour Curd and Coconut Ground with Cumin, Green Chillies and White Pumpkin",
        level7_main_ingredient="curd",
        level8_gravy_base="yogurt_coconut",
        level9_cooking_method="Gentle simmer",
        level10_consistency="Medium",
        level11_portion_type="volume_ml",
        level12_nutrition_ref_id="ifct_kuzhambu_mor"
    ),
    food_family="Kuzhambu",
    specific_dish="Mor Kuzhambu",
    region="South India",
    state_or_city="Tamil Nadu / Kerala (Moru Curry)",
    regional_names={"English": "Mor Kuzhambu", "Tamil": "மோர் குழம்பு", "Malayalam": "മോര് കറി", "Telugu": "మజ్జిగ పులుసు"},
    alternate_names=["mor kuzhambu", "more kuzhambu", "mor kulambu", "moru curry", "majjiga pulusu"],
    vegetarian=True,
    main_ingredient="curd",
    gravy_base="yogurt_coconut",
    cooking_method="Gentle simmer",
    consistency="Medium",
    default_portion_grams=150.0,
    density_g_ml=1.06,
    nutrition_per_100g={"calories": 82.0, "protein_g": 3.4, "carbs_g": 6.8, "fat_g": 4.5, "fiber_g": 1.2, "sodium_mg": 280.0},
    uncertainty_factors=["coconut_paste_ratio", "yogurt_fat_content"],
    typical_oil_level="Medium"
))


# =============================================================================
# 5. KOOTU FAMILY (Section 13)
# =============================================================================

# 5.1 Keerai / Chow Chow Kootu
register_curry_food_class(CurryFoodClassRecord(
    canonical_food_id="CURRY_KOOTU_CHOW_CHOW",
    canonical_name="Chow Chow Kootu (Chayote & Moong Dal)",
    hierarchy=CurryHierarchy(
        level3_region="South India",
        level4_food_family="Kootu",
        level5_specific_dish="Kootu",
        level6_variant="Cooked Moong Dal and Chayote Squash Ground with Cumin Coconut Paste",
        level7_main_ingredient="chow_chow",
        level8_gravy_base="dal_coconut_vegetable",
        level9_cooking_method="Boiled and simmered",
        level10_consistency="Thick",
        level11_portion_type="volume_ml",
        level12_nutrition_ref_id="ifct_kootu_chow_chow"
    ),
    food_family="Kootu",
    specific_dish="Kootu",
    region="South India",
    state_or_city="Tamil Nadu",
    regional_names={"English": "Chow Chow Kootu", "Tamil": "சௌ சௌ கூட்டு"},
    alternate_names=["kootu", "chow chow kootu", "sorakkai kootu", "keerai kootu", "paruppu kootu"],
    vegetarian=True,
    main_ingredient="moong_dal",
    gravy_base="dal_coconut_vegetable",
    cooking_method="Boiled and simmered",
    consistency="Thick",
    default_portion_grams=140.0,
    density_g_ml=1.09,
    nutrition_per_100g={"calories": 75.0, "protein_g": 3.8, "carbs_g": 9.5, "fat_g": 2.5, "fiber_g": 2.6, "sodium_mg": 240.0},
    uncertainty_factors=["coconut_proportion", "dal_ratio"],
    typical_oil_level="Low"
), alias_ids=["CURRY_KOOTU_KEERAI", "CURRY_KOOTU_SORAKKAI", "CURRY_KOOTU_PARUPPU", "CURRY_KOOTU_MIXED_VEG"])


# =============================================================================
# 6. KADHI FAMILY (Section 20)
# =============================================================================

# 6.1 Punjabi Pakora Kadhi
register_curry_food_class(CurryFoodClassRecord(
    canonical_food_id="CURRY_KADHI_PUNJABI",
    canonical_name="Punjabi Pakora Kadhi",
    hierarchy=CurryHierarchy(
        level3_region="North India",
        level4_food_family="Kadhi",
        level5_specific_dish="Punjabi Kadhi",
        level6_variant="Sour Dahi and Besan Simmered with Onion Fritters (Pakoras) and Ghee Tadka",
        level7_main_ingredient="yogurt_besan",
        level8_gravy_base="yogurt_besan",
        level9_cooking_method="Slow simmered",
        level10_consistency="Medium-Thick",
        level11_portion_type="volume_ml",
        level12_nutrition_ref_id="ifct_kadhi_punjabi"
    ),
    food_family="Kadhi",
    specific_dish="Punjabi Kadhi",
    region="North India",
    state_or_city="Punjab / Delhi",
    regional_names={"English": "Punjabi Kadhi", "Hindi": "पंजाबी कढ़ी पकौड़ा", "Punjabi": "ਕੜ੍ਹੀ ਪਕੌੜਾ"},
    alternate_names=["punjabi kadhi", "pakora kadhi", "kadhi pakora", "kadhi"],
    vegetarian=True,
    main_ingredient="curd",
    gravy_base="yogurt_besan",
    cooking_method="Slow simmered",
    consistency="Medium",
    default_portion_grams=180.0,
    density_g_ml=1.08,
    nutrition_per_100g={"calories": 125.0, "protein_g": 4.5, "carbs_g": 11.2, "fat_g": 6.8, "fiber_g": 1.8, "sodium_mg": 380.0},
    uncertainty_factors=["pakora_fry_oil_absorption", "yogurt_sourness_fat"],
    typical_oil_level="Medium"
), alias_ids=["CURRY_KADHI_GUJARATI", "CURRY_KADHI_SINDHI"])


# =============================================================================
# 7. PANEER GRAVY FAMILY (Sections 16, 17)
# =============================================================================

# 7.1 Paneer Butter Masala
register_curry_food_class(CurryFoodClassRecord(
    canonical_food_id="CURRY_PANEER_BUTTER_MASALA",
    canonical_name="Paneer Butter Masala",
    hierarchy=CurryHierarchy(
        level3_region="North India",
        level4_food_family="Paneer Curry",
        level5_specific_dish="Paneer Butter Masala",
        level6_variant="Fresh Cottage Cheese Cubes in Creamy Butter Tomato Cashew Silk Gravy",
        level7_main_ingredient="paneer",
        level8_gravy_base="tomato_cashew_butter_cream",
        level9_cooking_method="Simmered",
        level10_consistency="Thick",
        level11_portion_type="weight_grams",
        level12_nutrition_ref_id="ifct_paneer_butter_masala"
    ),
    food_family="Paneer Curry",
    specific_dish="Paneer Butter Masala",
    region="North India",
    state_or_city="North India / Mughlai",
    regional_names={"English": "Paneer Butter Masala", "Hindi": "पनीर बटर मसाला"},
    alternate_names=["paneer butter masala", "paneer makhani", "butter paneer", "pbm"],
    vegetarian=True,
    main_ingredient="paneer",
    gravy_base="tomato_cashew_cream",
    cooking_method="Simmered",
    consistency="Thick",
    piece_count_expected=6,
    default_portion_grams=200.0,
    density_g_ml=1.14,
    nutrition_per_100g={"calories": 195.0, "protein_g": 7.5, "carbs_g": 8.5, "fat_g": 15.2, "fiber_g": 1.5, "sodium_mg": 390.0},
    uncertainty_factors=["butter_cream_excess", "cashew_paste_ratio", "paneer_weight"],
    typical_oil_level="Very High"
), alias_ids=["CURRY_PANEER_SHAHI", "CURRY_PANEER_TIKKA_MASALA"])

# 7.2 Palak Paneer
register_curry_food_class(CurryFoodClassRecord(
    canonical_food_id="CURRY_PANEER_PALAK",
    canonical_name="Palak Paneer",
    hierarchy=CurryHierarchy(
        level3_region="North India",
        level4_food_family="Paneer Curry",
        level5_specific_dish="Palak Paneer",
        level6_variant="Soft Paneer Cubes in Pureed Spiced Spinach Gravy",
        level7_main_ingredient="paneer",
        level8_gravy_base="spinach_onion_garlic",
        level9_cooking_method="Blanched and simmered",
        level10_consistency="Medium-Thick",
        level11_portion_type="weight_grams",
        level12_nutrition_ref_id="ifct_paneer_palak"
    ),
    food_family="Paneer Curry",
    specific_dish="Palak Paneer",
    region="North India",
    state_or_city="Punjab",
    regional_names={"English": "Palak Paneer", "Hindi": "पालक पनीर", "Punjabi": "ਪਾਲਕ ਪਨੀਰ"},
    alternate_names=["palak paneer", "saag paneer", "spinach paneer"],
    vegetarian=True,
    main_ingredient="paneer",
    gravy_base="spinach",
    cooking_method="Simmered",
    consistency="Medium",
    piece_count_expected=6,
    default_portion_grams=180.0,
    density_g_ml=1.10,
    nutrition_per_100g={"calories": 140.0, "protein_g": 7.8, "carbs_g": 5.5, "fat_g": 9.8, "fiber_g": 3.2, "sodium_mg": 310.0},
    uncertainty_factors=["paneer_mass", "cream_swirl"],
    typical_oil_level="Medium"
))


# =============================================================================
# 8. LEGUME CURRY FAMILY (Sections 18, 19)
# =============================================================================

# 8.1 Chole / Chana Masala (Section 18)
register_curry_food_class(CurryFoodClassRecord(
    canonical_food_id="CURRY_LEGUME_CHOLE",
    canonical_name="Punjabi Chole (Chana Masala)",
    hierarchy=CurryHierarchy(
        level3_region="North India",
        level4_food_family="Legume Curry",
        level5_specific_dish="Chole",
        level6_variant="Dark Tangy White Chickpea Curry with Anardana, Amchur and Spices",
        level7_main_ingredient="white_chickpeas",
        level8_gravy_base="onion_tomato_spice",
        level9_cooking_method="Slow simmered",
        level10_consistency="Thick",
        level11_portion_type="volume_ml",
        level12_nutrition_ref_id="ifct_chole_punjabi"
    ),
    food_family="Legume Curry",
    specific_dish="Chole",
    region="North India",
    state_or_city="Punjab / Delhi",
    regional_names={"English": "Chole", "Hindi": "छोले", "Punjabi": "ਛੋਲੇ", "Tamil": "சென்னா மசாலா"},
    alternate_names=["chole", "chana masala", "punjabi chole", "amritsari chole", "pindi chole"],
    vegetarian=True,
    main_ingredient="chickpeas",
    gravy_base="onion_tomato_spice",
    cooking_method="Slow simmered",
    consistency="Thick",
    default_portion_grams=180.0,
    density_g_ml=1.12,
    nutrition_per_100g={"calories": 138.0, "protein_g": 6.8, "carbs_g": 19.5, "fat_g": 4.0, "fiber_g": 5.5, "sodium_mg": 370.0},
    uncertainty_factors=["oil_tadka", "gravy_thickness"],
    typical_oil_level="Medium"
))

# 8.2 Rajma Masala (Section 19)
register_curry_food_class(CurryFoodClassRecord(
    canonical_food_id="CURRY_LEGUME_RAJMA",
    canonical_name="Punjabi Rajma Masala",
    hierarchy=CurryHierarchy(
        level3_region="North India",
        level4_food_family="Legume Curry",
        level5_specific_dish="Rajma",
        level6_variant="Red Kidney Beans Melt-in-Mouth Simmered in Aromatic Onion Tomato Gravy",
        level7_main_ingredient="red_kidney_beans",
        level8_gravy_base="onion_tomato_ginger",
        level9_cooking_method="Slow simmered",
        level10_consistency="Medium-Thick",
        level11_portion_type="volume_ml",
        level12_nutrition_ref_id="ifct_rajma_masala"
    ),
    food_family="Legume Curry",
    specific_dish="Rajma",
    region="North India",
    state_or_city="Punjab / Jammu",
    regional_names={"English": "Rajma Masala", "Hindi": "राजमा मसाला", "Punjabi": "ਰਾਜਮਾਹ"},
    alternate_names=["rajma", "rajma masala", "punjabi rajma", "rajma curry"],
    vegetarian=True,
    main_ingredient="rajma",
    gravy_base="onion_tomato",
    cooking_method="Slow simmered",
    consistency="Medium",
    default_portion_grams=180.0,
    density_g_ml=1.10,
    nutrition_per_100g={"calories": 128.0, "protein_g": 6.5, "carbs_g": 18.0, "fat_g": 3.4, "fiber_g": 5.8, "sodium_mg": 340.0},
    uncertainty_factors=["bean_starch_thickening", "ghee_topping"],
    typical_oil_level="Medium"
))


# =============================================================================
# 9. CHICKEN CURRY FAMILY (Sections 22, 23)
# =============================================================================

# 9.1 Homestyle Chicken Curry
register_curry_food_class(CurryFoodClassRecord(
    canonical_food_id="CURRY_CHICKEN_HOMESTYLE",
    canonical_name="Indian Homestyle Chicken Curry",
    hierarchy=CurryHierarchy(
        level3_region="Pan-India",
        level4_food_family="Chicken Curry",
        level5_specific_dish="Chicken Curry",
        level6_variant="Tender Bone-In Chicken Cooked in Onion, Tomato, Ginger and Coriander Gravy",
        level7_main_ingredient="chicken_bone_in",
        level8_gravy_base="onion_tomato_spice",
        level9_cooking_method="Simmered",
        level10_consistency="Medium",
        level11_portion_type="weight_grams",
        level12_nutrition_ref_id="ifct_chicken_curry_homestyle"
    ),
    food_family="Chicken Curry",
    specific_dish="Chicken Curry",
    region="Pan-India",
    state_or_city="Pan-India",
    regional_names={"English": "Chicken Curry", "Hindi": "चिकन करी", "Tamil": "சிக்கன் குழம்பு", "Telugu": "కోడి కూర", "Malayalam": "ചിക്കൻ കറി", "Bengali": "চিকেন কারি"},
    alternate_names=["chicken curry", "chicken gravy", "murgh curry", "kodi kura", "chicken kulambu", "chicken kuzhambu"],
    vegetarian=False,
    main_ingredient="chicken",
    gravy_base="onion_tomato_spice",
    cooking_method="Simmered",
    consistency="Medium",
    has_meat=True,
    has_bone_in_pieces=True,
    piece_count_expected=3,
    default_portion_grams=220.0,
    density_g_ml=1.09,
    nutrition_per_100g={"calories": 145.0, "protein_g": 14.5, "carbs_g": 4.5, "fat_g": 7.8, "fiber_g": 1.2, "sodium_mg": 380.0},
    uncertainty_factors=["chicken_to_gravy_ratio", "bone_mass_subtraction", "oil_layer"],
    typical_oil_level="Medium"
), alias_ids=["CURRY_CHICKEN_CHETTINAD", "CURRY_CHICKEN_ANDHRA", "CURRY_CHICKEN_KERALA"])

# 9.2 Butter Chicken (Murgh Makhani)
register_curry_food_class(CurryFoodClassRecord(
    canonical_food_id="CURRY_CHICKEN_BUTTER",
    canonical_name="Butter Chicken (Murgh Makhani)",
    hierarchy=CurryHierarchy(
        level3_region="North India",
        level4_food_family="Chicken Curry",
        level5_specific_dish="Butter Chicken",
        level6_variant="Tandoor Charred Chicken in Silky Rich Tomato, Butter, Cream and Cashew Gravy",
        level7_main_ingredient="chicken_tandoori",
        level8_gravy_base="tomato_cashew_butter_cream",
        level9_cooking_method="Tandoor roasted and simmered",
        level10_consistency="Thick",
        level11_portion_type="weight_grams",
        level12_nutrition_ref_id="ifct_chicken_butter"
    ),
    food_family="Chicken Curry",
    specific_dish="Butter Chicken",
    region="North India",
    state_or_city="Delhi / Punjab",
    regional_names={"English": "Butter Chicken", "Hindi": "बटर चिकन", "Urdu": "بٹر چکن"},
    alternate_names=["butter chicken", "murgh makhani", "chicken makhani"],
    vegetarian=False,
    main_ingredient="chicken",
    gravy_base="tomato_cashew_cream",
    cooking_method="Simmered",
    consistency="Thick",
    has_meat=True,
    has_bone_in_pieces=False,
    piece_count_expected=4,
    default_portion_grams=240.0,
    density_g_ml=1.14,
    nutrition_per_100g={"calories": 195.0, "protein_g": 13.5, "carbs_g": 6.8, "fat_g": 13.2, "fiber_g": 1.1, "sodium_mg": 420.0},
    uncertainty_factors=["butter_quantity", "heavy_cream_ratio", "sugar_honey_balance"],
    typical_oil_level="Very High"
), alias_ids=["CURRY_CHICKEN_TIKKA_MASALA"])


# =============================================================================
# 10. MUTTON CURRY FAMILY (Section 24)
# =============================================================================

# 10.1 Mutton Curry / Gravy
register_curry_food_class(CurryFoodClassRecord(
    canonical_food_id="CURRY_MUTTON_HOMESTYLE",
    canonical_name="Indian Mutton Curry (Gosht Gravy)",
    hierarchy=CurryHierarchy(
        level3_region="Pan-India",
        level4_food_family="Mutton Curry",
        level5_specific_dish="Mutton Curry",
        level6_variant="Bone-In Goat Meat Slow Cooked in Rich Spiced Onion Garlic Roghan Gravy",
        level7_main_ingredient="mutton_goat",
        level8_gravy_base="onion_garlic_roghan",
        level9_cooking_method="Slow pressure simmered",
        level10_consistency="Medium-Thick",
        level11_portion_type="weight_grams",
        level12_nutrition_ref_id="ifct_mutton_curry"
    ),
    food_family="Mutton Curry",
    specific_dish="Mutton Curry",
    region="Pan-India",
    state_or_city="Pan-India",
    regional_names={"English": "Mutton Curry", "Hindi": "मटन करी / गोश्त", "Tamil": "மட்டன் குழம்பு", "Telugu": "మటన్ కూర", "Malayalam": "മട്ടൻ കറി", "Urdu": "گوشت سالن"},
    alternate_names=["mutton curry", "mutton gravy", "gosht gravy", "mutton masala", "mutton kulambu", "goat curry"],
    vegetarian=False,
    main_ingredient="mutton",
    gravy_base="onion_tomato_spice",
    cooking_method="Slow simmered",
    consistency="Medium",
    has_meat=True,
    has_bone_in_pieces=True,
    piece_count_expected=3,
    default_portion_grams=220.0,
    density_g_ml=1.11,
    nutrition_per_100g={"calories": 185.0, "protein_g": 15.0, "carbs_g": 3.8, "fat_g": 12.2, "fiber_g": 1.0, "sodium_mg": 410.0},
    uncertainty_factors=["animal_fat_rendered", "bone_weight_fraction", "roghan_oil"],
    typical_oil_level="High"
), alias_ids=["CURRY_MUTTON_ROGAN_JOSH", "CURRY_MUTTON_CHETTINAD", "CURRY_MUTTON_LAAL_MAAS"])


# =============================================================================
# 11. FISH CURRY FAMILY (Section 25)
# =============================================================================

# 11.1 South Indian / Kerala Fish Curry (Meen Kuzhambu)
register_curry_food_class(CurryFoodClassRecord(
    canonical_food_id="CURRY_FISH_KERALA",
    canonical_name="Kerala / Tamil Fish Curry (Meen Kuzhambu)",
    hierarchy=CurryHierarchy(
        level3_region="South India",
        level4_food_family="Fish Curry",
        level5_specific_dish="Fish Curry",
        level6_variant="Fresh Fish Steaks Simmered in Kudampuli / Tamarind, Fenugreek and Red Chillies",
        level7_main_ingredient="fish_steak",
        level8_gravy_base="tamarind_kudampuli_chilli",
        level9_cooking_method="Earthen pot simmered",
        level10_consistency="Medium",
        level11_portion_type="weight_grams",
        level12_nutrition_ref_id="ifct_fish_curry_kerala"
    ),
    food_family="Fish Curry",
    specific_dish="Fish Curry",
    region="South India",
    state_or_city="Kerala / Tamil Nadu",
    regional_names={"English": "Fish Curry", "Tamil": "மீன் குழம்பு", "Malayalam": "മീൻ കറി", "Telugu": "చేపల పులుసు"},
    alternate_names=["fish curry", "meen curry", "meen kuzhambu", "meen kulambu", "chepala pulusu", "kerala fish curry", "macher jhol", "bengali fish curry"],
    vegetarian=False,
    main_ingredient="fish",
    gravy_base="tamarind_chilli",
    cooking_method="Simmered",
    consistency="Medium",
    has_meat=True,
    has_bone_in_pieces=True,
    piece_count_expected=2,
    default_portion_grams=200.0,
    density_g_ml=1.07,
    nutrition_per_100g={"calories": 115.0, "protein_g": 13.8, "carbs_g": 4.2, "fat_g": 4.8, "fiber_g": 1.1, "sodium_mg": 360.0},
    uncertainty_factors=["species_fat_content", "coconut_oil_glaze", "species_uncertain"],
    typical_oil_level="Medium"
), alias_ids=["CURRY_FISH_MEEN_KUZHAMBU", "CURRY_FISH_GOAN", "CURRY_FISH_BENGALI_JHOL", "CURRY_FISH_ANDHRA_PULUSU"])


# =============================================================================
# 12. EGG & SEAFOOD CURRY FAMILIES (Sections 26, 27)
# =============================================================================

# 12.1 Egg Curry
register_curry_food_class(CurryFoodClassRecord(
    canonical_food_id="CURRY_EGG_KERALA",
    canonical_name="South Indian Egg Curry (Mutta Roast / Curry)",
    hierarchy=CurryHierarchy(
        level3_region="South / Pan-India",
        level4_food_family="Egg Curry",
        level5_specific_dish="Egg Curry",
        level6_variant="Hard-Boiled Eggs Simmered in Onion, Tomato, Curry Leaves and Coconut Milk Gravy",
        level7_main_ingredient="boiled_egg",
        level8_gravy_base="onion_tomato_coconut",
        level9_cooking_method="Simmered",
        level10_consistency="Medium-Thick",
        level11_portion_type="weight_grams",
        level12_nutrition_ref_id="ifct_egg_curry"
    ),
    food_family="Egg Curry",
    specific_dish="Egg Curry",
    region="South / Pan-India",
    state_or_city="Kerala / Tamil Nadu",
    regional_names={"English": "Egg Curry", "Malayalam": "മുട്ട കറി", "Tamil": "முட்டை குழம்பு", "Hindi": "अंडा करी"},
    alternate_names=["egg curry", "mutta curry", "mutta roast", "egg gravy", "anda curry"],
    vegetarian=False,
    main_ingredient="egg",
    gravy_base="onion_tomato",
    cooking_method="Simmered",
    consistency="Medium",
    has_meat=False,
    piece_count_expected=2,
    default_portion_grams=180.0,
    density_g_ml=1.08,
    nutrition_per_100g={"calories": 132.0, "protein_g": 7.8, "carbs_g": 5.2, "fat_g": 9.0, "fiber_g": 1.2, "sodium_mg": 320.0},
    uncertainty_factors=["egg_count_independent", "gravy_oil"],
    typical_oil_level="Medium"
), alias_ids=["CURRY_EGG_NORTH_INDIAN", "CURRY_EGG_CHETTINAD"])

# 12.2 Prawn Curry
register_curry_food_class(CurryFoodClassRecord(
    canonical_food_id="CURRY_SEAFOOD_PRAWN_MASALA",
    canonical_name="Indian Prawn Curry / Masala",
    hierarchy=CurryHierarchy(
        level3_region="Coastal India",
        level4_food_family="Seafood Curry",
        level5_specific_dish="Prawn Curry",
        level6_variant="Juicy Prawns Cooked in Coconut, Tamarind, Kokum and Fiery Red Spices",
        level7_main_ingredient="prawns",
        level8_gravy_base="coconut_tomato_spice",
        level9_cooking_method="Quick simmered",
        level10_consistency="Medium",
        level11_portion_type="weight_grams",
        level12_nutrition_ref_id="ifct_prawn_curry"
    ),
    food_family="Seafood Curry",
    specific_dish="Prawn Curry",
    region="Coastal India",
    state_or_city="Kerala / Goa / Bengal / Tamil Nadu",
    regional_names={"English": "Prawn Curry", "Malayalam": "ചെമ്മീൻ കറി", "Tamil": "இறால் குழம்பு", "Bengali": "চিংড়ি মালাই কারি"},
    alternate_names=["prawn curry", "shrimp curry", "chemmeen curry", "eraal kuzhambu", "chingri malai curry"],
    vegetarian=False,
    main_ingredient="prawns",
    gravy_base="coconut_tomato_spice",
    cooking_method="Simmered",
    consistency="Medium",
    has_meat=True,
    piece_count_expected=6,
    default_portion_grams=180.0,
    density_g_ml=1.08,
    nutrition_per_100g={"calories": 120.0, "protein_g": 13.5, "carbs_g": 4.5, "fat_g": 5.5, "fiber_g": 1.0, "sodium_mg": 390.0},
    uncertainty_factors=["prawn_count", "coconut_milk_fat"],
    typical_oil_level="Medium"
))


# =============================================================================
# 13. KURMA & SALNA FAMILIES (Sections 28, 29)
# =============================================================================

# 13.1 Vegetable Kurma
register_curry_food_class(CurryFoodClassRecord(
    canonical_food_id="CURRY_KURMA_VEG",
    canonical_name="South Indian Vegetable Kurma",
    hierarchy=CurryHierarchy(
        level3_region="South India",
        level4_food_family="Kurma",
        level5_specific_dish="Vegetable Kurma",
        level6_variant="Diced Vegetables Simmered in White Coconut, Poppy Seeds, Fennel and Cashew Paste",
        level7_main_ingredient="mixed_vegetables",
        level8_gravy_base="coconut_cashew_fennel",
        level9_cooking_method="Simmered",
        level10_consistency="Medium-Thick",
        level11_portion_type="volume_ml",
        level12_nutrition_ref_id="ifct_kurma_veg"
    ),
    food_family="Kurma",
    specific_dish="Vegetable Kurma",
    region="South India",
    state_or_city="Tamil Nadu / Kerala / Karnataka",
    regional_names={"English": "Vegetable Kurma", "Tamil": "வெஜ் குருமா", "Kannada": "ತರಕಾರಿ ಕೂರ್ಮಾ", "Malayalam": "വെജിറ്റബിൾ കുറുമ"},
    alternate_names=["veg kurma", "vegetable kurma", "hotel kurma", "saravana bhavan kurma", "white kurma"],
    vegetarian=True,
    main_ingredient="vegetables",
    gravy_base="coconut_cashew",
    cooking_method="Simmered",
    consistency="Medium",
    default_portion_grams=160.0,
    density_g_ml=1.08,
    nutrition_per_100g={"calories": 95.0, "protein_g": 2.5, "carbs_g": 9.2, "fat_g": 5.5, "fiber_g": 2.8, "sodium_mg": 290.0},
    uncertainty_factors=["coconut_paste_mass", "cashew_poppy_seed_density"],
    typical_oil_level="Medium"
), alias_ids=["CURRY_KURMA_WHITE_COCONUT"])

# 13.2 Street Parotta Salna (Section 29)
register_curry_food_class(CurryFoodClassRecord(
    canonical_food_id="CURRY_SALNA_PLAIN_PAROTTA",
    canonical_name="Street-Style Parotta Salna (Empty Salna)",
    hierarchy=CurryHierarchy(
        level3_region="South India",
        level4_food_family="Salna",
        level5_specific_dish="Salna",
        level6_variant="Aromatic Thin Onion, Tomato, Fennel, Coconut and Chicken Broth Street Salna",
        level7_main_ingredient="onion_tomato_fennel",
        level8_gravy_base="thin_onion_coconut_spiced",
        level9_cooking_method="Boiled and reduced",
        level10_consistency="Thin",
        level11_portion_type="volume_ml",
        level12_nutrition_ref_id="ifct_salna_empty"
    ),
    food_family="Salna",
    specific_dish="Salna",
    region="South India",
    state_or_city="Tamil Nadu / Madurai",
    regional_names={"English": "Parotta Salna", "Tamil": "பரோட்டா சால்னா / எம்டி சால்னா"},
    alternate_names=["salna", "parotta salna", "empty salna", "plain salna", "madurai salna"],
    vegetarian=True,
    main_ingredient="onion_tomato",
    gravy_base="thin_spiced_gravy",
    cooking_method="Simmered",
    consistency="Thin",
    default_portion_grams=150.0,
    density_g_ml=1.04,
    nutrition_per_100g={"calories": 72.0, "protein_g": 1.8, "carbs_g": 6.5, "fat_g": 4.5, "fiber_g": 1.2, "sodium_mg": 340.0},
    uncertainty_factors=["chicken_broth_presence", "floating_oil_film"],
    typical_oil_level="Medium"
), alias_ids=["CURRY_SALNA_CHICKEN"])


# =============================================================================
# 14. PORIYAL / DRY CURRY FAMILY (Section 14)
# =============================================================================

# 14.1 Beans / Carrot Poriyal (Section 14)
register_curry_food_class(CurryFoodClassRecord(
    canonical_food_id="CURRY_PORIYAL_BEANS",
    canonical_name="South Indian Beans & Carrot Poriyal",
    hierarchy=CurryHierarchy(
        level3_region="South India",
        level4_food_family="Dry / Semi-Dry Poriyal",
        level5_specific_dish="Poriyal",
        level6_variant="Finely Diced French Beans Tempered with Mustard, Urad Dal, Curry Leaves and Fresh Coconut",
        level7_main_ingredient="french_beans",
        level8_gravy_base="dry_tempered",
        level9_cooking_method="Steamed and sautéed",
        level10_consistency="Dry",
        level11_portion_type="weight_grams",
        level12_nutrition_ref_id="ifct_poriyal_beans"
    ),
    food_family="Dry / Semi-Dry Poriyal",
    specific_dish="Poriyal",
    region="South India",
    state_or_city="Tamil Nadu / Kerala (Thoron) / Karnataka (Palya)",
    regional_names={"English": "Beans Poriyal", "Tamil": "பீன்ஸ் பொரியல்", "Malayalam": "ബീൻസ് തോരൻ", "Kannada": "ಬೀನ್ಸ್ ಪಲ್ಯ"},
    alternate_names=["poriyal", "beans poriyal", "beans thoran", "beans palya", "vegetable poriyal", "dry curry"],
    vegetarian=True,
    main_ingredient="french_beans",
    gravy_base="dry",
    cooking_method="Steamed and sautéed",
    consistency="Dry",
    default_portion_grams=80.0,
    density_g_ml=0.92,
    nutrition_per_100g={"calories": 85.0, "protein_g": 2.8, "carbs_g": 8.5, "fat_g": 4.5, "fiber_g": 3.8, "sodium_mg": 180.0},
    uncertainty_factors=["fresh_grated_coconut_volume", "oil_used_for_tempering"],
    typical_oil_level="Low"
), alias_ids=["CURRY_PORIYAL_CARROT", "CURRY_PORIYAL_CABBAGE", "CURRY_PORIYAL_POTATO", "CURRY_PORIYAL_BEETROOT"])


# =============================================================================
# 14B. VEGETABLE, COCONUT & GRAVY BASE FAMILIES
# =============================================================================

# Vegetable Curry
register_curry_food_class(CurryFoodClassRecord(
    canonical_food_id="CURRY_VEG_MIXED",
    canonical_name="Mixed Vegetable Curry / Sabzi",
    hierarchy=CurryHierarchy(
        level3_region="Pan-India",
        level4_food_family="Vegetable Curry",
        level5_specific_dish="Mixed Vegetable Curry",
        level6_variant="Carrot, Peas, Beans and Potato Simmered in Spiced Onion-Tomato Gravy",
        level7_main_ingredient="mixed_vegetables",
        level8_gravy_base="onion_tomato",
        level9_cooking_method="Simmered",
        level10_consistency="Medium",
        level11_portion_type="volume_ml",
        level12_nutrition_ref_id="ifct_veg_curry"
    ),
    food_family="Vegetable Curry",
    specific_dish="Mixed Vegetable Curry",
    region="Pan-India",
    state_or_city="Pan-India",
    regional_names={"English": "Veg Curry", "Hindi": "सब्जी करी"},
    alternate_names=["veg curry", "vegetable curry", "mixed veg curry", "mix veg"],
    vegetarian=True,
    main_ingredient="mixed_vegetables",
    gravy_base="onion_tomato",
    cooking_method="Simmered",
    consistency="Medium",
    default_portion_grams=150.0,
    density_g_ml=1.07,
    nutrition_per_100g={"calories": 90.0, "protein_g": 2.6, "carbs_g": 11.2, "fat_g": 4.0, "fiber_g": 3.0, "sodium_mg": 280.0},
    uncertainty_factors=["vegetable_potato_proportion", "oil_layer"],
    typical_oil_level="Medium"
), alias_ids=["CURRY_VEG_ALOO_GOBHI"])

# Coconut-Based Curry
register_curry_food_class(CurryFoodClassRecord(
    canonical_food_id="CURRY_COCONUT_STEW",
    canonical_name="Kerala Coconut Vegetable Stew",
    hierarchy=CurryHierarchy(
        level3_region="South India",
        level4_food_family="Coconut-Based Curry",
        level5_specific_dish="Coconut Stew",
        level6_variant="Mild Vegetables Simmered in Rich Coconut Milk Infused with Whole Spices",
        level7_main_ingredient="coconut_milk",
        level8_gravy_base="coconut_milk",
        level9_cooking_method="Gently simmered",
        level10_consistency="Medium",
        level11_portion_type="volume_ml",
        level12_nutrition_ref_id="ifct_coconut_stew"
    ),
    food_family="Coconut-Based Curry",
    specific_dish="Coconut Stew",
    region="South India",
    state_or_city="Kerala",
    regional_names={"English": "Coconut Stew", "Malayalam": "വെജിറ്റബിൾ സ്റ്റൂ"},
    alternate_names=["coconut stew", "kerala stew", "coconut curry", "coconut-based curry", "ishtu"],
    vegetarian=True,
    main_ingredient="coconut_milk",
    gravy_base="coconut_milk",
    cooking_method="Gently simmered",
    consistency="Medium",
    default_portion_grams=160.0,
    density_g_ml=1.06,
    nutrition_per_100g={"calories": 135.0, "protein_g": 2.0, "carbs_g": 8.0, "fat_g": 11.0, "fiber_g": 2.2, "sodium_mg": 260.0},
    uncertainty_factors=["coconut_milk_fat_thickness"],
    typical_oil_level="Medium"
))

# Tomato-Based Gravy
register_curry_food_class(CurryFoodClassRecord(
    canonical_food_id="CURRY_GRAVY_TOMATO",
    canonical_name="North Indian Spiced Tomato Gravy",
    hierarchy=CurryHierarchy(
        level3_region="North India",
        level4_food_family="Tomato-Based Gravy",
        level5_specific_dish="Tomato Gravy",
        level6_variant="Pureed Plum Tomatoes Cooked with Cumin, Ginger, Kasuri Methi and Spices",
        level7_main_ingredient="tomato",
        level8_gravy_base="pureed_tomato",
        level9_cooking_method="Simmered",
        level10_consistency="Medium",
        level11_portion_type="volume_ml",
        level12_nutrition_ref_id="ifct_tomato_gravy"
    ),
    food_family="Tomato-Based Gravy",
    specific_dish="Tomato Gravy",
    region="North India",
    state_or_city="North India",
    regional_names={"English": "Tomato Gravy", "Hindi": "टमाटर ग्रेवी"},
    alternate_names=["tomato gravy", "tamatar curry", "tomato-based gravy"],
    vegetarian=True,
    main_ingredient="tomato",
    gravy_base="tomato",
    cooking_method="Simmered",
    consistency="Medium",
    default_portion_grams=150.0,
    density_g_ml=1.05,
    nutrition_per_100g={"calories": 80.0, "protein_g": 1.8, "carbs_g": 7.5, "fat_g": 5.0, "fiber_g": 1.8, "sodium_mg": 310.0},
    uncertainty_factors=["oil_sheen", "tomato_acidity"],
    typical_oil_level="Medium"
))

# Onion-Based Gravy
register_curry_food_class(CurryFoodClassRecord(
    canonical_food_id="CURRY_GRAVY_ONION",
    canonical_name="Bhuna Onion Masala Gravy",
    hierarchy=CurryHierarchy(
        level3_region="North / Central India",
        level4_food_family="Onion-Based Gravy",
        level5_specific_dish="Onion Gravy",
        level6_variant="Slow Caramelized Onion Paste Cooked with Whole Garam Masala",
        level7_main_ingredient="onion",
        level8_gravy_base="caramelized_onion",
        level9_cooking_method="Slow sautéed and bhuna",
        level10_consistency="Thick",
        level11_portion_type="volume_ml",
        level12_nutrition_ref_id="ifct_onion_gravy"
    ),
    food_family="Onion-Based Gravy",
    specific_dish="Onion Gravy",
    region="North / Central India",
    state_or_city="Pan-India",
    regional_names={"English": "Onion Gravy", "Hindi": "प्याज मसाला ग्रेवी"},
    alternate_names=["onion gravy", "bhuna onion gravy", "onion-based gravy", "pyaza gravy"],
    vegetarian=True,
    main_ingredient="onion",
    gravy_base="onion",
    cooking_method="Bhuna",
    consistency="Thick",
    default_portion_grams=140.0,
    density_g_ml=1.10,
    nutrition_per_100g={"calories": 115.0, "protein_g": 2.2, "carbs_g": 10.5, "fat_g": 7.5, "fiber_g": 2.0, "sodium_mg": 340.0},
    uncertainty_factors=["bhuna_oil_content"],
    typical_oil_level="High"
))

# Yogurt-Based Gravy
register_curry_food_class(CurryFoodClassRecord(
    canonical_food_id="CURRY_GRAVY_YOGURT",
    canonical_name="Rajasthani Dahi Gravy / Gatta Curry",
    hierarchy=CurryHierarchy(
        level3_region="West / North India",
        level4_food_family="Yogurt-Based Gravy",
        level5_specific_dish="Yogurt Gravy",
        level6_variant="Whisked Spiced Curd Simmered with Gram Flour Dumplings and Hing",
        level7_main_ingredient="curd",
        level8_gravy_base="curd_besan",
        level9_cooking_method="Simmered",
        level10_consistency="Medium",
        level11_portion_type="volume_ml",
        level12_nutrition_ref_id="ifct_yogurt_gravy"
    ),
    food_family="Yogurt-Based Gravy",
    specific_dish="Yogurt Gravy",
    region="West / North India",
    state_or_city="Rajasthan / Gujarat",
    regional_names={"English": "Yogurt Gravy", "Hindi": "दही ग्रेवी / गट्टा"},
    alternate_names=["yogurt gravy", "dahi gravy", "dahi curry", "yogurt-based gravy"],
    vegetarian=True,
    main_ingredient="curd",
    gravy_base="yogurt",
    cooking_method="Simmered",
    consistency="Medium",
    default_portion_grams=160.0,
    density_g_ml=1.06,
    nutrition_per_100g={"calories": 105.0, "protein_g": 3.8, "carbs_g": 8.0, "fat_g": 6.5, "fiber_g": 1.2, "sodium_mg": 320.0},
    uncertainty_factors=["dahi_fat_pct"],
    typical_oil_level="Medium"
))

# Cream-Based Gravy
register_curry_food_class(CurryFoodClassRecord(
    canonical_food_id="CURRY_GRAVY_CREAM",
    canonical_name="Mughlai Shahi Malai Gravy",
    hierarchy=CurryHierarchy(
        level3_region="North India",
        level4_food_family="Cream-Based Gravy",
        level5_specific_dish="Cream Gravy",
        level6_variant="Heavy Cream and Cashew Nut Paste Infused with Saffron and Cardamom",
        level7_main_ingredient="cream_cashew",
        level8_gravy_base="heavy_cream_cashew",
        level9_cooking_method="Gently simmered",
        level10_consistency="Thick",
        level11_portion_type="volume_ml",
        level12_nutrition_ref_id="ifct_cream_gravy"
    ),
    food_family="Cream-Based Gravy",
    specific_dish="Cream Gravy",
    region="North India",
    state_or_city="Mughlai / Delhi / Lucknow",
    regional_names={"English": "Cream Gravy", "Hindi": "शाही मलाई ग्रेवी"},
    alternate_names=["cream gravy", "malai gravy", "shahi gravy", "cream-based gravy", "white korma gravy"],
    vegetarian=True,
    main_ingredient="cream_cashew",
    gravy_base="cream_cashew",
    cooking_method="Simmered",
    consistency="Thick",
    default_portion_grams=150.0,
    density_g_ml=1.14,
    nutrition_per_100g={"calories": 210.0, "protein_g": 4.5, "carbs_g": 9.5, "fat_g": 18.0, "fiber_g": 1.0, "sodium_mg": 330.0},
    uncertainty_factors=["dairy_cream_percentage", "cashew_paste_ratio"],
    typical_oil_level="Very High"
))


# =============================================================================
# 15. UNKNOWN CURRY FALLBACK (Sections 52, 73, 74)
# =============================================================================

register_curry_food_class(CurryFoodClassRecord(
    canonical_food_id="CURRY_UNKNOWN_001",
    canonical_name="Indian curry/gravy — exact dish uncertain",
    hierarchy=CurryHierarchy(
        level3_region="Pan-India",
        level4_food_family="Regional Specialty Curry",
        level5_specific_dish="Unknown",
        level6_variant="Unverified Indian Gravy (Insufficient Visual Evidence)",
        level7_main_ingredient="unknown",
        level8_gravy_base="unknown",
        level9_cooking_method="Simmered",
        level10_consistency="Medium",
        level11_portion_type="weight_grams",
        level12_nutrition_ref_id="ifct_curry_unknown"
    ),
    food_family="Regional Specialty Curry",
    specific_dish="Unknown",
    region="Pan-India",
    state_or_city="Unknown",
    regional_names={"English": "Unknown Indian Curry", "Hindi": "अज्ञात भारतीय करी / सालन"},
    alternate_names=["unknown curry", "unidentified gravy", "curry/gravy uncertain", "unknown dal"],
    vegetarian=True,
    main_ingredient="unknown",
    gravy_base="unknown",
    cooking_method="Simmered",
    consistency="Medium",
    default_portion_grams=150.0,
    density_g_ml=1.06,
    nutrition_per_100g={"calories": 110.0, "protein_g": 3.5, "carbs_g": 9.5, "fat_g": 6.5, "fiber_g": 2.0, "sodium_mg": 320.0},
    uncertainty_factors=["insufficient_visual_evidence", "unknown_recipe_composition"],
    typical_oil_level="Unknown"
), alias_ids=["CURRY_UNKNOWN"])


# =============================================================================
# LOOKUP & HELPER UTILITIES
# =============================================================================

def get_curry_food_class(canonical_id: str) -> Optional[CurryFoodClassRecord]:
    """Retrieve record by canonical ID."""
    return CURRY_TAXONOMY_REGISTRY.get(canonical_id)


def resolve_curry_food_by_name(query: str) -> Optional[CurryFoodClassRecord]:
    """
    Resolves any query string (canonical name, English alias, regional script)
    into the canonical CurryFoodClassRecord. Returns None if unmapped.
    """
    if not query:
        return None
    q = query.lower().strip()
    if q in CURRY_SYNONYM_LOOKUP:
        return CURRY_TAXONOMY_REGISTRY.get(CURRY_SYNONYM_LOOKUP[q])
    for alt, cid in CURRY_SYNONYM_LOOKUP.items():
        if alt in q or q in alt:
            return CURRY_TAXONOMY_REGISTRY.get(cid)
    return None


def filter_curries_by_family(food_family: str) -> List[CurryFoodClassRecord]:
    """Returns all registered curry classes in a given family."""
    fam = food_family.lower().strip()
    return [
        rec for rec in CURRY_TAXONOMY_REGISTRY.values()
        if rec.food_family.lower() == fam or fam in rec.hierarchy.level4_food_family.lower()
    ]
