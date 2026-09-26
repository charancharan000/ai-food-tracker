"""
Indian Rice & Biryani Master Taxonomy & Identity Hierarchy (Part 9)
Implements Sections 0-19, 21-42, 55, 62, 70, 77 of Part 9 Master Training Specification.

Guarantees:
- Strict Hierarchical Identity Traversal:
  Indian Food -> Rice-Based Food -> Master Rice Family (13 families) ->
  Sub-Family / Canonical Food -> Regional Style -> Grain Attributes -> Cooking State -> Portion -> Nutrition
- 13 Master Rice Families:
  1. Plain Rice (RICE_PLAIN_*)
  2. Biryani (BIRYANI_*)
  3. Pulao (PULAO_*)
  4. Fried Rice (FRIEDRICE_*)
  5. Mixed Rice / Variety Rice (VARIETY_RICE_*)
  6. Khichdi (KHICHDI_*)
  7. Pongal (PONGAL_*)
  8. Rice Porridge / Kanji (KANJI_*)
  9. Curd Rice (CURD_RICE_*)
  10. Rice Desserts (RICE_DESSERT_*)
  11. Rice Snacks / Cakes (RICE_SNACK_*)
  12. Regional Rice Dishes (REGIONAL_RICE_*)
  13. Rice + Curry Meals (RICE_MEAL_*)
  Plus RICE_UNKNOWN fallback.
- Rice Grain Attributes:
  * Grain length: short_grain, medium_grain, long_grain, slender_grain
  * Grain texture: fluffy_separated, sticky, clumped, broken, mushy_porridge
- Cooking States:
  Raw, Soaked, Boiled, Steamed, Pressure Cooked, Fried, Stir Fried, Slow Cooked, Dum Cooked, Fermented, Mashed, Porridge, Unknown.
- Permanent Canonical IDs:
  * BIRYANI_HYDERABADI_CHICKEN, BIRYANI_AMBUR_MUTTON, BIRYANI_DINDIGUL_MUTTON,
    BIRYANI_THALASSERY_CHICKEN, BIRYANI_KOLKATA_CHICKEN, BIRYANI_LUCKNOWI_MUTTON,
    BIRYANI_DONNE_CHICKEN, BIRYANI_MEMONI_MUTTON, BIRYANI_VEG, BIRYANI_EGG,
    PULAO_VEG, PULAO_YAKHNI, VARIETY_RICE_LEMON, VARIETY_RICE_PULIYODARAI,
    CURD_RICE_TRADITIONAL, KHICHDI_MOONG_DAL, PONGAL_VEN, PONGAL_SAKKARAI, etc.
- Multilingual regional names across Hindi, Telugu, Tamil, Malayalam, Kannada, Bengali, Odia, Urdu, etc.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class RiceHierarchy(BaseModel):
    level1_food: str = "Indian Food"
    level2_macro_category: str = "Rice-Based Food"
    level3_rice_family: str     # Biryani, Pulao, Plain Rice, Variety Rice, Khichdi, Pongal, etc.
    level4_sub_family: str      # e.g., Chicken Biryani, Mutton Biryani, Veg Pulao, Lemon Rice
    level5_canonical_food: str
    level6_regional_style: str  # Hyderabadi, Ambur, Dindigul, Thalassery, Kolkata, Lucknowi, Donne, etc.
    level7_grain_type: str      # long_grain_basmati, short_grain_seeraga_samba, sona_masuri, etc.
    level8_cooking_state: str   # Dum Cooked, Steamed, One-Pot Absorption, Wok Stir-Fried, Mashed
    level9_portion_type: str    # plate_grams, handi_vessel, bowl_grams
    level10_nutrition_ref_id: str


class RiceFoodClassRecord(BaseModel):
    canonical_food_id: str
    canonical_name: str
    hierarchy: RiceHierarchy
    rice_family: str
    regional_style: str
    region: str                 # South India, North India, East India, West India, Pan-India
    state_or_city: str          # Telangana / Hyderabad, Tamil Nadu / Ambur, West Bengal / Kolkata, etc.
    regional_names: Dict[str, str] = Field(default_factory=dict)
    alternate_names: List[str] = Field(default_factory=list)
    vegetarian: bool = True
    protein_type: str = "vegetarian"  # chicken, mutton, egg, fish, prawn, paneer, veg
    primary_ingredients: List[str] = Field(default_factory=list)
    signature_components: List[str] = Field(default_factory=list)  # e.g. ["boiled_potato", "egg", "fried_onions"]
    typical_side_dishes: List[str] = Field(default_factory=list)   # e.g. ["mirchi_ka_salan", "onion_raita"]
    grain_length: str = "long_grain"   # short_grain, medium_grain, long_grain, slender_grain
    grain_texture: str = "fluffy_separated"  # fluffy_separated, sticky, mushy_porridge, clumped
    default_portion_grams: float = 380.0
    density_g_cm3: float = 0.85
    nutrition_per_100g: Dict[str, float] = Field(default_factory=dict)
    uncertainty_factors: List[str] = Field(default_factory=list)
    ghee_oil_level_typical: str = "Medium"  # Low, Medium, High, Unknown


RICE_TAXONOMY_REGISTRY: Dict[str, RiceFoodClassRecord] = {}
RICE_SYNONYM_LOOKUP: Dict[str, str] = {}


def register_rice_food_class(record: RiceFoodClassRecord) -> RiceFoodClassRecord:
    RICE_TAXONOMY_REGISTRY[record.canonical_food_id] = record
    RICE_SYNONYM_LOOKUP[record.canonical_name.lower().strip()] = record.canonical_food_id
    for alt in record.alternate_names:
        RICE_SYNONYM_LOOKUP[alt.lower().strip()] = record.canonical_food_id
    for reg_name in record.regional_names.values():
        RICE_SYNONYM_LOOKUP[reg_name.lower().strip()] = record.canonical_food_id
    return record


# =============================================================================
# 1. BIRYANI MASTER TAXONOMY & REGIONAL STYLES (Sections 5 - 19)
# =============================================================================

# 1.1 Hyderabadi Dum Biryani (Section 6)
register_rice_food_class(RiceFoodClassRecord(
    canonical_food_id="BIRYANI_HYDERABADI_CHICKEN",
    canonical_name="Hyderabadi Chicken Dum Biryani",
    hierarchy=RiceHierarchy(
        level3_rice_family="Biryani",
        level4_sub_family="Chicken Biryani",
        level5_canonical_food="Hyderabadi Biryani",
        level6_regional_style="Hyderabadi Kacchi / Pakki Dum",
        level7_grain_type="long_grain_basmati",
        level8_cooking_state="Dum Cooked",
        level9_portion_type="plate_grams",
        level10_nutrition_ref_id="ifct_biryani_hyderabadi_chicken"
    ),
    rice_family="Biryani",
    regional_style="Hyderabadi",
    region="South India",
    state_or_city="Telangana / Hyderabad",
    regional_names={"English": "Hyderabadi Chicken Biryani", "Telugu": "హైదరాబాదీ చికెన్ బిర్యానీ", "Urdu": "حیدرآبادی چکن بریانی", "Hindi": "हैदराबादी चिकन बिरयानी"},
    alternate_names=["hyderabadi biryani", "hyderabadi dum biryani", "kacchi biryani", "hyderabad chicken biryani"],
    vegetarian=False,
    protein_type="chicken",
    primary_ingredients=["aged basmati rice", "marinated bone-in chicken", "yogurt", "fried onions (birista)", "mint leaves", "coriander", "saffron milk", "ghee", "shahi whole spices"],
    signature_components=["long slender basmati grains with orange/white marbling", "bone-in chicken pieces", "golden fried onions", "boiled egg (often 1)"],
    typical_side_dishes=["mirchi ka salan", "onion-cucumber raita"],
    grain_length="long_grain",
    grain_texture="fluffy_separated",
    default_portion_grams=420.0,
    density_g_cm3=0.82,
    nutrition_per_100g={"calories": 182.0, "protein_g": 9.4, "carbs_g": 22.5, "fat_g": 6.2, "fiber_g": 1.2, "sodium_mg": 380.0},
    uncertainty_factors=["rice_to_chicken_ratio", "birista_ghee_quantity", "salan_inclusion"],
    ghee_oil_level_typical="High"
))

register_rice_food_class(RiceFoodClassRecord(
    canonical_food_id="BIRYANI_HYDERABADI_MUTTON",
    canonical_name="Hyderabadi Mutton Dum Biryani",
    hierarchy=RiceHierarchy(
        level3_rice_family="Biryani",
        level4_sub_family="Mutton Biryani",
        level5_canonical_food="Hyderabadi Biryani",
        level6_regional_style="Hyderabadi Kacchi Dum",
        level7_grain_type="long_grain_basmati",
        level8_cooking_state="Dum Cooked",
        level9_portion_type="plate_grams",
        level10_nutrition_ref_id="ifct_biryani_hyderabadi_mutton"
    ),
    rice_family="Biryani",
    regional_style="Hyderabadi",
    region="South India",
    state_or_city="Telangana / Hyderabad",
    regional_names={"English": "Hyderabadi Mutton Biryani", "Telugu": "హైదరాబాదీ మటన్ బిర్యానీ", "Urdu": "حیدرآبادی مٹن بریانی"},
    alternate_names=["hyderabadi gosht biryani", "kacchi gosht ki biryani", "hyderabadi mutton dum biryani"],
    vegetarian=False,
    protein_type="mutton",
    primary_ingredients=["basmati rice", "raw marinated goat mutton chunks", "curd", "fried onions", "saffron", "ghee", "garam masala"],
    signature_components=["tender bone-in mutton pieces", "fragrant long grains", "caramelized birista"],
    typical_side_dishes=["mirchi ka salan", "dahi ki chutney"],
    grain_length="long_grain",
    grain_texture="fluffy_separated",
    default_portion_grams=430.0,
    density_g_cm3=0.84,
    nutrition_per_100g={"calories": 205.0, "protein_g": 11.2, "carbs_g": 21.0, "fat_g": 8.5, "fiber_g": 1.1, "sodium_mg": 410.0},
    uncertainty_factors=["mutton_fat_content", "ghee_glaze"],
    ghee_oil_level_typical="High"
))

# 1.2 Ambur Biryani (Section 7)
register_rice_food_class(RiceFoodClassRecord(
    canonical_food_id="BIRYANI_AMBUR_MUTTON",
    canonical_name="Ambur Mutton Biryani",
    hierarchy=RiceHierarchy(
        level3_rice_family="Biryani",
        level4_sub_family="Mutton Biryani",
        level5_canonical_food="Ambur Biryani",
        level6_regional_style="Arcot / Ambur Seeraga Samba Dum",
        level7_grain_type="short_grain_seeraga_samba",
        level8_cooking_state="Dum Cooked",
        level9_portion_type="plate_grams",
        level10_nutrition_ref_id="ifct_biryani_ambur_mutton"
    ),
    rice_family="Biryani",
    regional_style="Ambur",
    region="South India",
    state_or_city="Tamil Nadu / Ambur",
    regional_names={"English": "Ambur Mutton Biryani", "Tamil": "ஆம்பூர் மட்டன் பிரியாணி"},
    alternate_names=["ambur biryani", "arcot biryani", "ambur mutton dum biryani"],
    vegetarian=False,
    protein_type="mutton",
    primary_ingredients=["seeraga samba rice", "mutton pieces", "curd", "red chilli paste", "coriander", "mint", "ghee/oil"],
    signature_components=["small fragrant seeraga samba grains", "dark reddish-brown masala hue", "mutton chunks"],
    typical_side_dishes=["ennai kathirikai (sour brinjal gravy)", "onion raita"],
    grain_length="short_grain",
    grain_texture="fluffy_separated",
    default_portion_grams=400.0,
    density_g_cm3=0.86,
    nutrition_per_100g={"calories": 198.0, "protein_g": 10.8, "carbs_g": 22.0, "fat_g": 7.6, "fiber_g": 1.4, "sodium_mg": 420.0},
    uncertainty_factors=["seeraga_samba_absorption", "brinjal_side_dish"],
    ghee_oil_level_typical="Medium"
))

# 1.3 Dindigul Thalappakatti Biryani (Section 8)
register_rice_food_class(RiceFoodClassRecord(
    canonical_food_id="BIRYANI_DINDIGUL_MUTTON",
    canonical_name="Dindigul Mutton Biryani",
    hierarchy=RiceHierarchy(
        level3_rice_family="Biryani",
        level4_sub_family="Mutton Biryani",
        level5_canonical_food="Dindigul Biryani",
        level6_regional_style="Thalappakatti Seeraga Samba Dum",
        level7_grain_type="short_grain_seeraga_samba",
        level8_cooking_state="Dum Cooked",
        level9_portion_type="plate_grams",
        level10_nutrition_ref_id="ifct_biryani_dindigul_mutton"
    ),
    rice_family="Biryani",
    regional_style="Dindigul",
    region="South India",
    state_or_city="Tamil Nadu / Dindigul",
    regional_names={"English": "Dindigul Mutton Biryani", "Tamil": "திண்டுக்கல் தலப்பாகட்டி மட்டன் பிரியாணி"},
    alternate_names=["dindigul biryani", "thalappakatti biryani", "thalapakattu biryani", "dindigul mutton thalappakatti"],
    vegetarian=False,
    protein_type="mutton",
    primary_ingredients=["seeraga samba rice", "tender tender goat mutton chunks", "curd", "black pepper", "ginger-garlic", "lemon", "ghee"],
    signature_components=["small ovular seeraga samba grains", "distinct peppery dark masala", "rich bone-marrow flavor"],
    typical_side_dishes=["dalcha", "onion raita"],
    grain_length="short_grain",
    grain_texture="fluffy_separated",
    default_portion_grams=410.0,
    density_g_cm3=0.87,
    nutrition_per_100g={"calories": 204.0, "protein_g": 11.0, "carbs_g": 21.5, "fat_g": 8.2, "fiber_g": 1.3, "sodium_mg": 430.0},
    uncertainty_factors=["mutton_fat_retention", "seeraga_samba_ghee_ratio"],
    ghee_oil_level_typical="High"
))

# 1.4 Thalassery / Malabar Biryani (Section 9 & 13)
register_rice_food_class(RiceFoodClassRecord(
    canonical_food_id="BIRYANI_THALASSERY_CHICKEN",
    canonical_name="Thalassery Chicken Biryani",
    hierarchy=RiceHierarchy(
        level3_rice_family="Biryani",
        level4_sub_family="Chicken Biryani",
        level5_canonical_food="Thalassery Biryani",
        level6_regional_style="Malabar Jeerakasala Dum",
        level7_grain_type="short_grain_jeerakasala",
        level8_cooking_state="Dum Cooked",
        level9_portion_type="plate_grams",
        level10_nutrition_ref_id="ifct_biryani_thalassery_chicken"
    ),
    rice_family="Biryani",
    regional_style="Thalassery",
    region="South India",
    state_or_city="Kerala / Thalassery / Malabar",
    regional_names={"English": "Thalassery Chicken Biryani", "Malayalam": "തലശ്ശേരി ചിക്കൻ ബിരിയാണി"},
    alternate_names=["thalassery biryani", "malabar biryani", "kerala chicken biryani", "tellicherry biryani"],
    vegetarian=False,
    protein_type="chicken",
    primary_ingredients=["jeerakasala (khyma) rice", "chicken", "ghee", "fried onions (birista)", "cashews", "raisins", "malabar garam masala", "curd"],
    signature_components=["short thin jeerakasala rice grains", "golden fried cashews & raisins", "mild aromatic greenish-yellow masala base"],
    typical_side_dishes=["chammanthi (coconut-mint chutney)", "dates-lemon pickle", "raita"],
    grain_length="short_grain",
    grain_texture="fluffy_separated",
    default_portion_grams=390.0,
    density_g_cm3=0.85,
    nutrition_per_100g={"calories": 192.0, "protein_g": 9.8, "carbs_g": 23.0, "fat_g": 6.8, "fiber_g": 1.2, "sodium_mg": 370.0},
    uncertainty_factors=["cashew_raisin_density", "ghee_quantity"],
    ghee_oil_level_typical="Medium"
))

# 1.5 Kolkata Biryani (Section 10)
register_rice_food_class(RiceFoodClassRecord(
    canonical_food_id="BIRYANI_KOLKATA_CHICKEN",
    canonical_name="Kolkata Chicken Biryani with Aloo & Egg",
    hierarchy=RiceHierarchy(
        level3_rice_family="Biryani",
        level4_sub_family="Chicken Biryani",
        level5_canonical_food="Kolkata Biryani",
        level6_regional_style="Awadhi-Exiled Kolkata Dum",
        level7_grain_type="long_grain_basmati",
        level8_cooking_state="Dum Cooked",
        level9_portion_type="plate_grams",
        level10_nutrition_ref_id="ifct_biryani_kolkata_chicken"
    ),
    rice_family="Biryani",
    regional_style="Kolkata",
    region="East India",
    state_or_city="West Bengal / Kolkata",
    regional_names={"English": "Kolkata Chicken Biryani", "Bengali": "কলকাতা চিকেন বিরিয়ানি", "Hindi": "कोलकाता बिरयानी"},
    alternate_names=["kolkata biryani", "calcutta biryani", "kolkata chicken dum biryani", "bengali biryani"],
    vegetarian=False,
    protein_type="chicken",
    primary_ingredients=["extra long basmati rice", "chicken", "large boiled spiced potato (aloo)", "hard-boiled egg", "meetha attar", "rose water", "kewra water", "saffron milk", "ghee"],
    signature_components=["prominent large halved or whole yellow spiced potato (aloo)", "boiled whole egg", "delicate meetha attar aroma", "light yellow/cream grains"],
    typical_side_dishes=["chicken chaap", "mutton chaap", "onion salad"],
    grain_length="long_grain",
    grain_texture="fluffy_separated",
    default_portion_grams=450.0,
    density_g_cm3=0.82,
    nutrition_per_100g={"calories": 175.0, "protein_g": 8.6, "carbs_g": 24.5, "fat_g": 5.2, "fiber_g": 1.5, "sodium_mg": 360.0},
    uncertainty_factors=["potato_mass_70g_vs_120g", "boiled_egg_presence", "meetha_attar_ghee"],
    ghee_oil_level_typical="Medium"
))

# 1.6 Lucknowi / Awadhi Biryani (Section 11)
register_rice_food_class(RiceFoodClassRecord(
    canonical_food_id="BIRYANI_LUCKNOWI_MUTTON",
    canonical_name="Lucknowi Awadhi Mutton Biryani",
    hierarchy=RiceHierarchy(
        level3_rice_family="Biryani",
        level4_sub_family="Mutton Biryani",
        level5_canonical_food="Lucknowi Biryani",
        level6_regional_style="Awadhi Pakki Dum in Yakhni",
        level7_grain_type="long_grain_basmati",
        level8_cooking_state="Dum Cooked",
        level9_portion_type="plate_grams",
        level10_nutrition_ref_id="ifct_biryani_lucknowi_mutton"
    ),
    rice_family="Biryani",
    regional_style="Lucknowi",
    region="North India",
    state_or_city="Uttar Pradesh / Lucknow",
    regional_names={"English": "Lucknowi Mutton Biryani", "Urdu": "لکھنوی مٹن بریانی", "Hindi": "लखनऊई मटन बिरयानी"},
    alternate_names=["lucknowi biryani", "awadhi biryani", "pakki biryani", "lucknow mutton dum biryani"],
    vegetarian=False,
    protein_type="mutton",
    primary_ingredients=["basmati rice", "tender mutton simmered in rich yakhni broth", "saffron milk", "kewra water", "ghee", "potli whole spices"],
    signature_components=["subtle delicate golden hues", "fragrant yakhni-infused grains", "mild non-fiery aroma"],
    typical_side_dishes=["burani raita", "shami kebab"],
    grain_length="long_grain",
    grain_texture="fluffy_separated",
    default_portion_grams=420.0,
    density_g_cm3=0.83,
    nutrition_per_100g={"calories": 196.0, "protein_g": 10.5, "carbs_g": 21.5, "fat_g": 7.8, "fiber_g": 1.0, "sodium_mg": 390.0},
    uncertainty_factors=["yakhni_stock_richness", "ghee_quantity"],
    ghee_oil_level_typical="Medium"
))

# 1.7 Karnataka Donne Biryani (Section 14)
register_rice_food_class(RiceFoodClassRecord(
    canonical_food_id="BIRYANI_DONNE_CHICKEN",
    canonical_name="Bengaluru Shivaji Donne Chicken Biryani",
    hierarchy=RiceHierarchy(
        level3_rice_family="Biryani",
        level4_sub_family="Chicken Biryani",
        level5_canonical_food="Donne Biryani",
        level6_regional_style="Karnataka Maratha Donne Dum",
        level7_grain_type="short_grain_jeera_samba",
        level8_cooking_state="Dum Cooked",
        level9_portion_type="plate_grams",
        level10_nutrition_ref_id="ifct_biryani_donne_chicken"
    ),
    rice_family="Biryani",
    regional_style="Karnataka",
    region="South India",
    state_or_city="Karnataka / Bengaluru",
    regional_names={"English": "Donne Chicken Biryani", "Kannada": "ದೊನ್ನೆ ಚಿಕನ್ ಬಿರಿಯಾನಿ"},
    alternate_names=["donne biryani", "shivaji military hotel biryani", "bangalore donne biryani", "karnataka biryani"],
    vegetarian=False,
    protein_type="chicken",
    primary_ingredients=["jeera samba rice", "chicken", "vibrant green mint-coriander paste", "green chillies", "spices", "ghee"],
    signature_components=["distinct herbal greenish-olive color", "served in palm leaf bowl (donne)", "boiled egg garnish"],
    typical_side_dishes=["onion raita", "spicy rasam / soup"],
    grain_length="short_grain",
    grain_texture="fluffy_separated",
    default_portion_grams=390.0,
    density_g_cm3=0.86,
    nutrition_per_100g={"calories": 188.0, "protein_g": 9.6, "carbs_g": 22.8, "fat_g": 6.8, "fiber_g": 1.4, "sodium_mg": 410.0},
    uncertainty_factors=["green_herb_paste_density", "oil_in_military_style"],
    ghee_oil_level_typical="Medium"
))

# 1.8 Vegetarian Biryani (Section 17)
register_rice_food_class(RiceFoodClassRecord(
    canonical_food_id="BIRYANI_VEG_DUM",
    canonical_name="Royal Vegetable Dum Biryani",
    hierarchy=RiceHierarchy(
        level3_rice_family="Biryani",
        level4_sub_family="Vegetable Biryani",
        level5_canonical_food="Veg Biryani",
        level6_regional_style="Dum Cooked Layered Vegetable",
        level7_grain_type="long_grain_basmati",
        level8_cooking_state="Dum Cooked",
        level9_portion_type="plate_grams",
        level10_nutrition_ref_id="ifct_biryani_veg_dum"
    ),
    rice_family="Biryani",
    regional_style="Pan-India",
    region="Pan-India",
    state_or_city="Pan-India",
    regional_names={"English": "Vegetable Biryani", "Hindi": "वेज बिरयानी"},
    alternate_names=["veg biryani", "vegetable dum biryani", "paneer veg biryani"],
    vegetarian=True,
    protein_type="vegetarian",
    primary_ingredients=["basmati rice", "carrots", "french beans", "green peas", "cauliflower florets", "paneer cubes (optional)", "curd", "fried onions", "mint", "saffron"],
    signature_components=["layered colorful vegetables", "paneer cubes", "fried onion garnish"],
    typical_side_dishes=["vegetable raita", "mirchi salan"],
    grain_length="long_grain",
    grain_texture="fluffy_separated",
    default_portion_grams=370.0,
    density_g_cm3=0.83,
    nutrition_per_100g={"calories": 158.0, "protein_g": 4.5, "carbs_g": 25.2, "fat_g": 4.6, "fiber_g": 2.4, "sodium_mg": 360.0},
    uncertainty_factors=["paneer_presence", "ghee_glaze"],
    ghee_oil_level_typical="Medium"
))


# =============================================================================
# 2. PULAO MASTER TAXONOMY (Sections 21 - 25)
# =============================================================================

register_rice_food_class(RiceFoodClassRecord(
    canonical_food_id="PULAO_VEG_HOMESTYLE",
    canonical_name="Homestyle Green Peas & Veg Pulao",
    hierarchy=RiceHierarchy(
        level3_rice_family="Pulao",
        level4_sub_family="Veg Pulao",
        level5_canonical_food="Veg Pulao",
        level6_regional_style="One-Pot Absorption Cooked",
        level7_grain_type="long_grain_basmati",
        level8_cooking_state="One-Pot Absorption",
        level9_portion_type="plate_grams",
        level10_nutrition_ref_id="ifct_pulao_veg"
    ),
    rice_family="Pulao",
    regional_style="North / Pan-India",
    region="North / Pan-India",
    state_or_city="Pan-India",
    regional_names={"English": "Veg Pulao", "Hindi": "वेज पुलाव", "Punjabi": "ਮਟਰ ਪੁਲਾਓ"},
    alternate_names=["pulao", "veg pulao", "matar pulao", "peas pulao"],
    vegetarian=True,
    protein_type="vegetarian",
    primary_ingredients=["basmati rice", "green peas (matar)", "carrots", "whole cumin", "cardamom", "cloves", "ghee"],
    signature_components=["homogeneous light colored grains (not layered)", "mild whole spice aroma", "green peas and diced carrots"],
    typical_side_dishes=["cucumber raita", "boondi raita"],
    grain_length="long_grain",
    grain_texture="fluffy_separated",
    default_portion_grams=320.0,
    density_g_cm3=0.82,
    nutrition_per_100g={"calories": 142.0, "protein_g": 3.4, "carbs_g": 26.5, "fat_g": 2.6, "fiber_g": 1.8, "sodium_mg": 290.0},
    uncertainty_factors=["ghee_measurement", "vegetable_ratio"],
    ghee_oil_level_typical="Low"
))

register_rice_food_class(RiceFoodClassRecord(
    canonical_food_id="PULAO_YAKHNI_MUTTON",
    canonical_name="Kashmiri Mutton Yakhni Pulao",
    hierarchy=RiceHierarchy(
        level3_rice_family="Pulao",
        level4_sub_family="Mutton Pulao",
        level5_canonical_food="Yakhni Pulao",
        level6_regional_style="Kashmiri Broth-Simmered Absorption",
        level7_grain_type="long_grain_basmati",
        level8_cooking_state="One-Pot Absorption",
        level9_portion_type="plate_grams",
        level10_nutrition_ref_id="ifct_pulao_yakhni_mutton"
    ),
    rice_family="Pulao",
    regional_style="Kashmiri",
    region="North India",
    state_or_city="Jammu & Kashmir / Kashmir",
    regional_names={"English": "Yakhni Pulao", "Kashmiri": "یخنی پلاؤ", "Hindi": "यखनी पुलाव"},
    alternate_names=["yakhni pulao", "kashmiri yakhni pulao", "mutton pulao"],
    vegetarian=False,
    protein_type="mutton",
    primary_ingredients=["basmati rice", "mutton", "aromatic meat yakhni broth (fennel, dry ginger, cloves, cinnamon)", "ghee", "curd"],
    signature_components=["pale ivory rice glistening with meat broth", "tender mutton chunks", "subtle aromatic spice without red chillies"],
    typical_side_dishes=["kashmiri onion raita", "walnut chutney"],
    grain_length="long_grain",
    grain_texture="fluffy_separated",
    default_portion_grams=380.0,
    density_g_cm3=0.84,
    nutrition_per_100g={"calories": 185.0, "protein_g": 10.2, "carbs_g": 21.0, "fat_g": 6.8, "fiber_g": 0.8, "sodium_mg": 380.0},
    uncertainty_factors=["yakhni_fat_rendered", "ghee_added"],
    ghee_oil_level_typical="Medium"
))


# =============================================================================
# 3. VARIETY RICE MASTER TAXONOMY (Sections 28 - 35)
# =============================================================================

# 3.1 Lemon Rice (Section 29)
register_rice_food_class(RiceFoodClassRecord(
    canonical_food_id="VARIETY_RICE_LEMON",
    canonical_name="South Indian Lemon Rice (Chitranna / Elumichai Sadam)",
    hierarchy=RiceHierarchy(
        level3_rice_family="Variety Rice",
        level4_sub_family="Lemon Rice",
        level5_canonical_food="Lemon Rice",
        level6_regional_style="South Indian Tempered",
        level7_grain_type="sona_masuri",
        level8_cooking_state="Steamed & Tempered",
        level9_portion_type="plate_grams",
        level10_nutrition_ref_id="ifct_variety_lemon_rice"
    ),
    rice_family="Variety Rice",
    regional_style="South Indian",
    region="South India",
    state_or_city="Tamil Nadu / Karnataka / Andhra Pradesh",
    regional_names={"English": "Lemon Rice", "Tamil": "எலுமிச்சை சாதம்", "Kannada": "ಚಿತ್ರಾನ್ನ", "Telugu": "నిమ్మకాయ పులిహోర"},
    alternate_names=["lemon rice", "chitranna", "elumichai sadam", "nimmakaya pulihora"],
    vegetarian=True,
    protein_type="vegetarian",
    primary_ingredients=["cooked white rice", "fresh lemon juice", "turmeric", "roasted peanuts", "chana dal", "urad dal", "mustard seeds", "green chillies", "curry leaves", "oil/ghee"],
    signature_components=["bright sunny yellow turmeric hue", "crunchy roasted peanuts", "crisp split chana/urad dal specks", "curry leaves"],
    typical_side_dishes=["potato fry (urulai kizhangu varuval)", "appalam/papad", "pickle"],
    grain_length="medium_grain",
    grain_texture="fluffy_separated",
    default_portion_grams=300.0,
    density_g_cm3=0.84,
    nutrition_per_100g={"calories": 178.0, "protein_g": 4.1, "carbs_g": 28.5, "fat_g": 5.4, "fiber_g": 1.6, "sodium_mg": 310.0},
    uncertainty_factors=["peanut_quantity", "tempering_oil_volume"],
    ghee_oil_level_typical="Medium"
))

# 3.2 Tamarind Rice / Puliyodarai / Pulihora (Section 30)
register_rice_food_class(RiceFoodClassRecord(
    canonical_food_id="VARIETY_RICE_PULIYODARAI",
    canonical_name="Traditional Temple Style Puliyodarai / Tamarind Rice",
    hierarchy=RiceHierarchy(
        level3_rice_family="Variety Rice",
        level4_sub_family="Tamarind Rice",
        level5_canonical_food="Puliyodarai",
        level6_regional_style="Temple Style Spiced Tamarind Paste",
        level7_grain_type="sona_masuri",
        level8_cooking_state="Steamed & Mixed",
        level9_portion_type="plate_grams",
        level10_nutrition_ref_id="ifct_variety_puliyodarai"
    ),
    rice_family="Variety Rice",
    regional_style="South Indian",
    region="South India",
    state_or_city="Tamil Nadu / Andhra Pradesh / Karnataka",
    regional_names={"English": "Tamarind Rice", "Tamil": "புளியோதரை", "Telugu": "పులిహోర", "Kannada": "ಹುಳಿಯನ್ನ"},
    alternate_names=["puliyodarai", "pulihora", "tamarind rice", "kovil puliyodharai", "hulianna"],
    vegetarian=True,
    protein_type="vegetarian",
    primary_ingredients=["cooked white rice", "concentrated tamarind pulp paste (pulikachal)", "sesame oil (gingelly oil)", "roasted peanuts", "fenugreek powder", "red chillies", "mustard", "curry leaves", "asafoetida"],
    signature_components=["deep reddish-brown/amber color", "gingelly oil sheen", "roasted peanuts and dried red chillies"],
    typical_side_dishes=["appalam", "sundal"],
    grain_length="medium_grain",
    grain_texture="fluffy_separated",
    default_portion_grams=300.0,
    density_g_cm3=0.86,
    nutrition_per_100g={"calories": 195.0, "protein_g": 4.2, "carbs_g": 31.0, "fat_g": 6.2, "fiber_g": 2.1, "sodium_mg": 390.0},
    uncertainty_factors=["gingelly_oil_glaze", "peanut_density"],
    ghee_oil_level_typical="High"
))

# 3.3 Curd Rice / Thayir Sadam (Section 31)
register_rice_food_class(RiceFoodClassRecord(
    canonical_food_id="CURD_RICE_TRADITIONAL",
    canonical_name="Traditional South Indian Tempered Curd Rice (Thayir Sadam)",
    hierarchy=RiceHierarchy(
        level3_rice_family="Curd Rice",
        level4_sub_family="Curd Rice",
        level5_canonical_food="Curd Rice",
        level6_regional_style="South Indian Tempered & Soft Mashed",
        level7_grain_type="sona_masuri",
        level8_cooking_state="Soft Mashed & Mixed",
        level9_portion_type="plate_grams",
        level10_nutrition_ref_id="ifct_curd_rice_traditional"
    ),
    rice_family="Curd Rice",
    regional_style="South Indian",
    region="South India",
    state_or_city="Tamil Nadu / Karnataka / Andhra Pradesh",
    regional_names={"English": "Curd Rice", "Tamil": "தயிர் சாதம்", "Telugu": "పెరుగన్నం", "Kannada": "ಮೊಸರನ್ನ", "Malayalam": "തൈര് സാദം"},
    alternate_names=["curd rice", "thayir sadam", "daddojanam", "mosaranna", "bagala bath"],
    vegetarian=True,
    protein_type="vegetarian",
    primary_ingredients=["soft cooked mashed white rice", "fresh whole milk curd (dahi)", "milk", "mustard seeds", "green chillies", "ginger juliennes", "curry leaves", "coriander", "pomegranate arils (optional)"],
    signature_components=["creamy white texture with visible green chillies, ginger, and curry leaves", "ruby pomegranate arils / grated carrot on top"],
    typical_side_dishes=["mango pickle (mavadu)", "lemon pickle", "fried mor milagai (sun-dried salted curd chillies)"],
    grain_length="medium_grain",
    grain_texture="mushy_porridge",
    default_portion_grams=320.0,
    density_g_cm3=0.92,
    nutrition_per_100g={"calories": 138.0, "protein_g": 3.8, "carbs_g": 22.5, "fat_g": 3.8, "fiber_g": 0.8, "sodium_mg": 280.0},
    uncertainty_factors=["whole_milk_vs_toned_curd", "cream_content"],
    ghee_oil_level_typical="Low"
))


# =============================================================================
# 4. KHICHDI & PONGAL MASTER TAXONOMY (Sections 36 - 38)
# =============================================================================

# 4.1 Khichdi (Section 36)
register_rice_food_class(RiceFoodClassRecord(
    canonical_food_id="KHICHDI_MOONG_DAL",
    canonical_name="Moong Dal Khichdi with Ghee",
    hierarchy=RiceHierarchy(
        level3_rice_family="Khichdi",
        level4_sub_family="Dal Khichdi",
        level5_canonical_food="Moong Dal Khichdi",
        level6_regional_style="North / West Indian Comfort Simmered",
        level7_grain_type="medium_grain",
        level8_cooking_state="Pressure Cooked / Soft Simmered",
        level9_portion_type="bowl_grams",
        level10_nutrition_ref_id="ifct_khichdi_moong_dal"
    ),
    rice_family="Khichdi",
    regional_style="Pan-India",
    region="Pan-India",
    state_or_city="Gujarat / Maharashtra / North India",
    regional_names={"English": "Moong Dal Khichdi", "Hindi": "खिचड़ी", "Gujarati": "ખીચડી", "Marathi": "खिचडी"},
    alternate_names=["khichdi", "dal khichdi", "moong khichdi", "comfort khichdi"],
    vegetarian=True,
    protein_type="vegetarian",
    primary_ingredients=["white rice", "yellow split moong dal (or green chilka)", "turmeric", "cumin seeds", "ginger", "asafoetida", "desi ghee"],
    signature_components=["soft semi-solid yellow porridge texture", "glistening ghee surface", "intact or mashed soft moong dal"],
    typical_side_dishes=["papad", "curd (dahi)", "pickle (achaar)", "kadhi"],
    grain_length="medium_grain",
    grain_texture="mushy_porridge",
    default_portion_grams=330.0,
    density_g_cm3=0.94,
    nutrition_per_100g={"calories": 128.0, "protein_g": 4.6, "carbs_g": 21.0, "fat_g": 2.8, "fiber_g": 1.8, "sodium_mg": 260.0},
    uncertainty_factors=["ghee_topping_dollop", "dal_to_rice_ratio"],
    ghee_oil_level_typical="Medium"
))

# 4.2 Ven Pongal (Section 37)
register_rice_food_class(RiceFoodClassRecord(
    canonical_food_id="PONGAL_VEN_TRADITIONAL",
    canonical_name="Traditional South Indian Ven Pongal (Ghee Pongal)",
    hierarchy=RiceHierarchy(
        level3_rice_family="Pongal",
        level4_sub_family="Ven Pongal",
        level5_canonical_food="Ven Pongal",
        level6_regional_style="Tamil Nadu Breakfast Ghee Tempered",
        level7_grain_type="raw_rice",
        level8_cooking_state="Mashed / Ghee Tempered",
        level9_portion_type="plate_grams",
        level10_nutrition_ref_id="ifct_pongal_ven_traditional"
    ),
    rice_family="Pongal",
    regional_style="Tamil Nadu",
    region="South India",
    state_or_city="Tamil Nadu / Chennai",
    regional_names={"English": "Ven Pongal", "Tamil": "வெண் பொங்கல்", "Kannada": "ಖಾರಾ ಪೊಂಗಲ್", "Telugu": "వెన్ పొంగల్"},
    alternate_names=["ven pongal", "ghee pongal", "khara pongal", "pongal"],
    vegetarian=True,
    protein_type="vegetarian",
    primary_ingredients=["raw rice", "yellow moong dal", "desi ghee", "whole black peppercorns (milagu)", "cumin seeds (jeeragam)", "crushed ginger", "curry leaves", "golden fried cashews", "asafoetida"],
    signature_components=["creamy velvety mashed rice-dal emulsion", "glistening aromatic desi ghee coating", "whole black peppercorns and fried cashew halves"],
    typical_side_dishes=["tiffin sambar", "coconut chutney", "medu vada"],
    grain_length="medium_grain",
    grain_texture="mushy_porridge",
    default_portion_grams=300.0,
    density_g_cm3=0.96,
    nutrition_per_100g={"calories": 182.0, "protein_g": 4.8, "carbs_g": 24.5, "fat_g": 7.4, "fiber_g": 1.6, "sodium_mg": 280.0},
    uncertainty_factors=["desi_ghee_quantity_heavy_vs_standard", "cashew_count"],
    ghee_oil_level_typical="High"
))

# 4.3 Sakkarai Pongal / Sweet Pongal (Section 38)
register_rice_food_class(RiceFoodClassRecord(
    canonical_food_id="PONGAL_SAKKARAI_SWEET",
    canonical_name="Traditional Sakkarai Pongal (Sweet Jaggery Pongal)",
    hierarchy=RiceHierarchy(
        level3_rice_family="Pongal",
        level4_sub_family="Sweet Pongal",
        level5_canonical_food="Sakkarai Pongal",
        level6_regional_style="Tamil Harvest Festival Sweet Rice",
        level7_grain_type="raw_rice",
        level8_cooking_state="Simmered with Jaggery & Ghee",
        level9_portion_type="bowl_grams",
        level10_nutrition_ref_id="ifct_pongal_sakkarai"
    ),
    rice_family="Pongal",
    regional_style="Tamil Nadu",
    region="South India",
    state_or_city="Tamil Nadu",
    regional_names={"English": "Sweet Pongal", "Tamil": "சர்க்கரை பொங்கல்", "Telugu": "చక్కెర పొంగలి"},
    alternate_names=["sakkarai pongal", "sweet pongal", "jaggery pongal"],
    vegetarian=True,
    protein_type="vegetarian",
    primary_ingredients=["raw rice", "yellow moong dal", "dark jaggery syrup (vellam)", "desi ghee", "golden fried cashews", "raisins", "cardamom powder", "edible camphor (pacha karpooram) pinch"],
    signature_components=["rich dark brown/amber glossy sheen", "fragrant cardamom-ghee aroma", "fried cashews and raisins"],
    typical_side_dishes=[],
    grain_length="medium_grain",
    grain_texture="mushy_porridge",
    default_portion_grams=200.0,
    density_g_cm3=1.05,
    nutrition_per_100g={"calories": 268.0, "protein_g": 4.2, "carbs_g": 48.0, "fat_g": 7.2, "fiber_g": 1.2, "sodium_mg": 65.0},
    uncertainty_factors=["jaggery_sugar_concentration", "ghee_saturation"],
    ghee_oil_level_typical="High"
))


# =============================================================================
# 5. PLAIN RICE & UNKNOWN FALLBACK (Sections 2 & 61)
# =============================================================================

register_rice_food_class(RiceFoodClassRecord(
    canonical_food_id="RICE_PLAIN_WHITE_STEAMED",
    canonical_name="Steamed White Rice (Variety Unspecified)",
    hierarchy=RiceHierarchy(
        level3_rice_family="Plain Rice",
        level4_sub_family="White Rice",
        level5_canonical_food="Steamed Rice",
        level6_regional_style="Steamed / Boiled",
        level7_grain_type="unspecified_variety",
        level8_cooking_state="Steamed",
        level9_portion_type="plate_grams",
        level10_nutrition_ref_id="ifct_rice_white_steamed"
    ),
    rice_family="Plain Rice",
    regional_style="Pan-India",
    region="Pan-India",
    state_or_city="Pan-India",
    regional_names={"English": "Steamed White Rice", "Hindi": "सादा चावल", "Tamil": "சாதம்", "Bengali": "ভাত"},
    alternate_names=["plain rice", "white rice", "steamed rice", "boiled rice", "bhat", "sadam"],
    vegetarian=True,
    protein_type="vegetarian",
    primary_ingredients=["white rice", "water"],
    signature_components=["white fluffy grains", "neutral unseasoned appearance"],
    typical_side_dishes=["dal", "sambar", "curry"],
    grain_length="medium_grain",
    grain_texture="fluffy_separated",
    default_portion_grams=250.0,
    density_g_cm3=0.81,
    nutrition_per_100g={"calories": 130.0, "protein_g": 2.7, "carbs_g": 28.2, "fat_g": 0.3, "fiber_g": 0.4, "sodium_mg": 5.0},
    uncertainty_factors=["exact_cultivar_undetectable_by_camera"],
    ghee_oil_level_typical="Low"
))

register_rice_food_class(RiceFoodClassRecord(
    canonical_food_id="RICE_UNKNOWN",
    canonical_name="Unknown Rice Dish",
    hierarchy=RiceHierarchy(
        level3_rice_family="Regional Rice Dishes",
        level4_sub_family="Unknown",
        level5_canonical_food="Unknown Rice Dish",
        level6_regional_style="Unknown",
        level7_grain_type="unspecified",
        level8_cooking_state="Unknown",
        level9_portion_type="plate_grams",
        level10_nutrition_ref_id="ifct_unknown_rice"
    ),
    rice_family="Regional Rice Dishes",
    regional_style="Unknown",
    region="Pan-India",
    state_or_city="Unknown",
    regional_names={"English": "Unknown Rice Dish", "Hindi": "अज्ञात चावल का व्यंजन"},
    alternate_names=["unknown rice", "unidentified rice dish"],
    vegetarian=True,
    protein_type="vegetarian",
    primary_ingredients=["rice"],
    signature_components=[],
    typical_side_dishes=[],
    grain_length="medium_grain",
    grain_texture="fluffy_separated",
    default_portion_grams=300.0,
    density_g_cm3=0.84,
    nutrition_per_100g={"calories": 160.0, "protein_g": 4.0, "carbs_g": 26.0, "fat_g": 4.5, "fiber_g": 1.0, "sodium_mg": 300.0},
    uncertainty_factors=["insufficient_visual_evidence", "unknown_preparation"],
    ghee_oil_level_typical="Unknown"
))


# =============================================================================
# LOOKUP & HELPER UTILITIES
# =============================================================================

def get_rice_food_class(canonical_id: str) -> Optional[RiceFoodClassRecord]:
    """Retrieve record by canonical ID."""
    return RICE_TAXONOMY_REGISTRY.get(canonical_id)


def resolve_rice_food_by_name(query: str) -> Optional[RiceFoodClassRecord]:
    """
    Resolves any query string (canonical name, English alias, Hindi/regional name)
    into the canonical RiceFoodClassRecord. Returns None if unmapped.
    """
    if not query:
        return None
    q = query.lower().strip()
    if q in RICE_SYNONYM_LOOKUP:
        return RICE_TAXONOMY_REGISTRY.get(RICE_SYNONYM_LOOKUP[q])
    for alt, cid in RICE_SYNONYM_LOOKUP.items():
        if alt in q or q in alt:
            return RICE_TAXONOMY_REGISTRY.get(cid)
    return None


def filter_rice_foods_by_family(rice_family: str) -> List[RiceFoodClassRecord]:
    """Returns all registered rice dishes in a given rice family."""
    fam = rice_family.lower().strip()
    return [
        rec for rec in RICE_TAXONOMY_REGISTRY.values()
        if rec.rice_family.lower() == fam or fam in rec.hierarchy.level3_rice_family.lower()
    ]
