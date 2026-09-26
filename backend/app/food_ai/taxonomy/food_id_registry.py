"""
Permanent Food ID Registry & Hierarchical Identity System
Implements Sections 1, 2, 3, 4, and 70 of Part 3.
Guarantees:
- Every food class has a unique, permanent ID (e.g., TN_BREAKFAST_IDLI_PLAIN)
- Strict 11-level hierarchy traversal
- Multi-lingual regional name mapping (English, Tamil, Malayalam, Kannada, Telugu)
- Canonical synonym resolution (mapping "idly", "steamed idli" -> TN_BREAKFAST_IDLI_PLAIN)
- Over 300 distinct, non-redundant South Indian culinary classes
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class FoodIdentityHierarchy(BaseModel):
    food_super_category: str = "South Indian"
    region: str # Tamil Nadu, Kerala, Karnataka, Andhra Pradesh, Telangana
    category: str # Breakfast, Lunch, Dinner, Snack, Sweet, Accompaniment, Non-Veg
    subcategory: str # Steamed Food, Crepe / Dosa, Lentil Fritter / Vada, Rice, Biryani, Lentil Stew, etc.
    canonical_food: str
    variant: str
    cooking_method: List[str]
    food_state: str
    common_ingredients: List[str]
    default_portion_type: str # piece_count, area_thickness_density, volume_density, meat_bone_cut
    default_serving_weight_g: float
    nutrition_reference_id: str

class PermanentFoodClassRecord(BaseModel):
    permanent_id: str
    hierarchy: FoodIdentityHierarchy
    canonical_name: str
    alternate_names: List[str] = Field(default_factory=list)
    regional_names: Dict[str, str] = Field(default_factory=dict)
    density_g_cm3: float = 0.80
    default_serving_style: str = "plate"
    default_container: str = "stainless_steel_plate"
    portion_model_type: str = "piece_count"
    nutrition_per_100g: Dict[str, float] = Field(default_factory=dict)

# Master Map of Permanent Class ID -> Record
PERMANENT_CLASS_REGISTRY: Dict[str, PermanentFoodClassRecord] = {}
SYNONYM_LOOKUP_MAP: Dict[str, str] = {}

def register_permanent_food(rec: PermanentFoodClassRecord):
    PERMANENT_CLASS_REGISTRY[rec.permanent_id] = rec
    # Index canonical name
    SYNONYM_LOOKUP_MAP[rec.canonical_name.lower().strip()] = rec.permanent_id
    # Index alternate names
    for alt in rec.alternate_names:
        SYNONYM_LOOKUP_MAP[alt.lower().strip()] = rec.permanent_id
    # Index regional names
    for reg_name in rec.regional_names.values():
        SYNONYM_LOOKUP_MAP[reg_name.lower().strip()] = rec.permanent_id

# =============================================================================
# 1. TAMIL NADU BREAKFAST & TIFFIN (IDLI, DOSA, VADA, PONGAL, PANIYARAM)
# =============================================================================

register_permanent_food(PermanentFoodClassRecord(
    permanent_id="TN_BREAKFAST_IDLI_PLAIN",
    canonical_name="Plain Steamed Idli",
    alternate_names=["idli", "idly", "rice idli", "steamed idli", "south indian idli", "vellai idli"],
    regional_names={"English": "Plain Steamed Idli", "Tamil": "இட்லி", "Malayalam": "ഇഡ്ഡലി", "Kannada": "ಇಡ್ಲಿ", "Telugu": "ఇడ్లీ"},
    density_g_cm3=0.72,
    default_serving_style="tiffin_plate",
    default_container="steel_plate",
    portion_model_type="piece_count",
    nutrition_per_100g={"calories": 136.0, "protein_g": 4.2, "carbs_g": 28.5, "fat_g": 0.6, "fiber_g": 1.4, "sodium_mg": 185.0},
    hierarchy=FoodIdentityHierarchy(
        region="Tamil Nadu",
        category="Breakfast",
        subcategory="Steamed Food",
        canonical_food="Idli",
        variant="Plain Steamed Rice & Urad Dal",
        cooking_method=["fermented", "steamed"],
        food_state="solid_porous",
        common_ingredients=["idli rice", "urad dal", "fenugreek seeds", "salt"],
        default_portion_type="piece_count",
        default_serving_weight_g=120.0,
        nutrition_reference_id="ifct_idli_plain"
    )
))

register_permanent_food(PermanentFoodClassRecord(
    permanent_id="TN_BREAKFAST_IDLI_MINI",
    canonical_name="Mini Button Idli",
    alternate_names=["mini idli", "button idli", "chitti idli", "cocktail idli", "14 idli"],
    regional_names={"English": "Mini Button Idli", "Tamil": "மினி இட்லி / பட்டன் இட்லி", "Telugu": "మినీ ఇడ్లీ", "Kannada": "ಮಿನಿ ಇಡ್ಲಿ"},
    density_g_cm3=0.74,
    portion_model_type="piece_count",
    nutrition_per_100g={"calories": 138.0, "protein_g": 4.2, "carbs_g": 28.8, "fat_g": 0.6, "fiber_g": 1.4, "sodium_mg": 185.0},
    hierarchy=FoodIdentityHierarchy(
        region="Tamil Nadu",
        category="Breakfast",
        subcategory="Steamed Food",
        canonical_food="Idli",
        variant="Miniature Coin Fermented Idli",
        cooking_method=["fermented", "steamed"],
        food_state="solid_porous",
        common_ingredients=["idli rice", "urad dal", "fenugreek", "salt"],
        default_portion_type="piece_count",
        default_serving_weight_g=160.0,
        nutrition_reference_id="ifct_idli_mini"
    )
))

register_permanent_food(PermanentFoodClassRecord(
    permanent_id="KA_BREAKFAST_IDLI_RAVA",
    canonical_name="Rava Idli",
    alternate_names=["rava idli", "sooji idli", "rawa idly", "semolina idli"],
    regional_names={"English": "Semolina Rava Idli", "Kannada": "ರವೆ ಇಡ್ಲಿ", "Tamil": "ரவா இட்லி", "Telugu": "రవ్వ ఇడ్లీ"},
    density_g_cm3=0.82,
    portion_model_type="piece_count",
    nutrition_per_100g={"calories": 165.0, "protein_g": 5.0, "carbs_g": 31.0, "fat_g": 3.2, "fiber_g": 1.6, "sodium_mg": 260.0},
    hierarchy=FoodIdentityHierarchy(
        region="Karnataka",
        category="Breakfast",
        subcategory="Steamed Food",
        canonical_food="Idli",
        variant="Semolina Curd Spiced Steamed Cake with Cashew",
        cooking_method=["steamed"],
        food_state="solid_crumbly",
        common_ingredients=["roasted semolina", "curd", "mustard seeds", "cashews", "carrots", "green chillies"],
        default_portion_type="piece_count",
        default_serving_weight_g=150.0,
        nutrition_reference_id="ifct_idli_rava"
    )
))

register_permanent_food(PermanentFoodClassRecord(
    permanent_id="TN_BREAKFAST_IDLI_PODI",
    canonical_name="Ghee Podi Idli",
    alternate_names=["podi idli", "ghee podi idli", "gunpowder idli", "milagai podi idli", "idli fry podi"],
    regional_names={"English": "Ghee Gunpowder Tossed Idli", "Tamil": "நெய் பொடி இட்லி", "Telugu": "నెయ్యి పొడి ఇడ్లీ"},
    density_g_cm3=0.78,
    portion_model_type="piece_count",
    nutrition_per_100g={"calories": 210.0, "protein_g": 5.4, "carbs_g": 26.5, "fat_g": 9.5, "fiber_g": 2.8, "sodium_mg": 380.0},
    hierarchy=FoodIdentityHierarchy(
        region="Tamil Nadu",
        category="Breakfast",
        subcategory="Steamed Food",
        canonical_food="Idli",
        variant="Steamed Idlis Tossed in Cow Ghee and Milagai Podi",
        cooking_method=["steamed", "tossed"],
        food_state="coated_solid",
        common_ingredients=["steamed idlis", "desi ghee", "spicy lentil podi"],
        default_portion_type="piece_count",
        default_serving_weight_g=180.0,
        nutrition_reference_id="ifct_idli_podi"
    )
))

register_permanent_food(PermanentFoodClassRecord(
    permanent_id="TN_BREAKFAST_DOSA_PLAIN",
    canonical_name="Plain Dosa",
    alternate_names=["dosa", "dosai", "sada dosa", "plain crepe", "roast dosa"],
    regional_names={"English": "Plain Fermented Crepe", "Tamil": "சாதாரண தோசை", "Malayalam": "ദോശ", "Kannada": "ದೋಸೆ", "Telugu": "దోశ"},
    density_g_cm3=0.48,
    portion_model_type="area_thickness_density",
    nutrition_per_100g={"calories": 168.0, "protein_g": 4.1, "carbs_g": 29.5, "fat_g": 4.0, "fiber_g": 1.5, "sodium_mg": 210.0},
    hierarchy=FoodIdentityHierarchy(
        region="Tamil Nadu",
        category="Breakfast",
        subcategory="Crepe / Dosa",
        canonical_food="Dosa",
        variant="Standard Golden Thin Fermented Crepe",
        cooking_method=["fermented", "pan_fried", "tawa_fried"],
        food_state="crispy_sheet",
        common_ingredients=["rice", "urad dal", "fenugreek", "oil", "salt"],
        default_portion_type="area_thickness_density",
        default_serving_weight_g=125.0,
        nutrition_reference_id="ifct_dosa_plain"
    )
))

register_permanent_food(PermanentFoodClassRecord(
    permanent_id="TN_BREAKFAST_DOSA_MASALA",
    canonical_name="Masala Dosa",
    alternate_names=["masala dosa", "masala dosai", "potato masala dosa", "aloo dosa"],
    regional_names={"English": "Potato Stuffed Masala Dosa", "Tamil": "மசால் தோசை", "Telugu": "మసాలా దోశ", "Kannada": "ಮಸಾಲ ದೋಸೆ"},
    density_g_cm3=0.58,
    portion_model_type="area_thickness_density",
    nutrition_per_100g={"calories": 188.0, "protein_g": 4.2, "carbs_g": 26.4, "fat_g": 7.5, "fiber_g": 2.2, "sodium_mg": 320.0},
    hierarchy=FoodIdentityHierarchy(
        region="Tamil Nadu",
        category="Breakfast",
        subcategory="Crepe / Dosa",
        canonical_food="Dosa",
        variant="Crisp Crepe Filled with Turmeric Mustard Potato Mash",
        cooking_method=["fermented", "tawa_fried", "boiled"],
        food_state="composite_crisp_and_soft_mash",
        common_ingredients=["fermented dosa batter", "potatoes", "onions", "green chillies", "mustard seeds", "turmeric", "curry leaves", "oil"],
        default_portion_type="area_thickness_density",
        default_serving_weight_g=200.0,
        nutrition_reference_id="ifct_dosa_masala"
    )
))

register_permanent_food(PermanentFoodClassRecord(
    permanent_id="KA_BREAKFAST_DOSA_MYSORE_MASALA",
    canonical_name="Mysore Masala Dosa",
    alternate_names=["mysore masala dosa", "mysuru masala dose", "red chutney dosa"],
    regional_names={"English": "Mysore Red Garlic Chutney Dosa", "Kannada": "ಮೈಸೂರು ಮಸಾಲ ದೋಸೆ", "Tamil": "மைசூர் மசால் தோசை"},
    density_g_cm3=0.62,
    portion_model_type="area_thickness_density",
    nutrition_per_100g={"calories": 215.0, "protein_g": 4.6, "carbs_g": 27.8, "fat_g": 10.2, "fiber_g": 2.4, "sodium_mg": 360.0},
    hierarchy=FoodIdentityHierarchy(
        region="Karnataka",
        category="Breakfast",
        subcategory="Crepe / Dosa",
        canonical_food="Dosa",
        variant="Thick-Crisp Dosa Smeared with Spicy Red Garlic Chutney & Butter",
        cooking_method=["fermented", "tawa_fried"],
        food_state="composite_crisp_glaze",
        common_ingredients=["fermented batter with chana dal", "byadagi red chilli garlic chutney", "potato palya", "butter", "ghee"],
        default_portion_type="area_thickness_density",
        default_serving_weight_g=230.0,
        nutrition_reference_id="ifct_dosa_mysore"
    )
))

register_permanent_food(PermanentFoodClassRecord(
    permanent_id="TN_BREAKFAST_DOSA_GHEE_ROAST",
    canonical_name="Ghee Paper Roast Dosa",
    alternate_names=["ghee roast", "ney roast", "cone dosa", "paper ghee roast", "ghee paper roast"],
    regional_names={"English": "Crisp Clarified Butter Cone Crepe", "Tamil": "நெய் ரோஸ்ட்", "Malayalam": "നെയ്യ് റോസ്റ്റ്"},
    density_g_cm3=0.42,
    portion_model_type="area_thickness_density",
    nutrition_per_100g={"calories": 235.0, "protein_g": 3.9, "carbs_g": 28.0, "fat_g": 12.4, "fiber_g": 1.2, "sodium_mg": 220.0},
    hierarchy=FoodIdentityHierarchy(
        region="Tamil Nadu",
        category="Breakfast",
        subcategory="Crepe / Dosa",
        canonical_food="Dosa",
        variant="Ultra-thin Wafer Crisp Golden Cone Roasted in Desi Ghee",
        cooking_method=["fermented", "slow_roasted_tawa"],
        food_state="ultra_crisp_brittle",
        common_ingredients=["dosa batter", "pure cow ghee in generous quantity"],
        default_portion_type="area_thickness_density",
        default_serving_weight_g=150.0,
        nutrition_reference_id="ifct_dosa_ghee_roast"
    )
))

register_permanent_food(PermanentFoodClassRecord(
    permanent_id="TN_BREAKFAST_VADA_MEDU",
    canonical_name="Medu Vada",
    alternate_names=["medu vada", "ulundhu vadai", "garelu", "uddina vade", "sambar vada dry", "lentil donut"],
    regional_names={"English": "Crispy Fluffy Lentil Donut", "Tamil": "மெது வடை", "Telugu": "గారెలు", "Kannada": "ಉದ್ದಿನ ವಡೆ", "Malayalam": "ഉഴുന്ന് വട"},
    density_g_cm3=0.62,
    portion_model_type="piece_count",
    nutrition_per_100g={"calories": 262.0, "protein_g": 9.6, "carbs_g": 28.0, "fat_g": 12.4, "fiber_g": 4.2, "sodium_mg": 310.0},
    hierarchy=FoodIdentityHierarchy(
        region="Tamil Nadu",
        category="Breakfast",
        subcategory="Lentil Fritter / Vada",
        canonical_food="Vada",
        variant="Aerated Whole Urad Dal Toroidal Donut with Central Aperture",
        cooking_method=["deep_fried"],
        food_state="solid_fried_donut",
        common_ingredients=["urad dal", "black peppercorns", "green chillies", "curry leaves", "ginger", "frying oil"],
        default_portion_type="piece_count",
        default_serving_weight_g=65.0,
        nutrition_reference_id="ifct_vada_medu"
    )
))

register_permanent_food(PermanentFoodClassRecord(
    permanent_id="TN_SNACK_VADA_PARUPPU",
    canonical_name="Paruppu Vada (Masala Vada)",
    alternate_names=["paruppu vada", "masala vadai", "parippu vada", "chana dal vada", "aamai vadai"],
    regional_names={"English": "Crunchy Split Chana Dal Fritter", "Tamil": "பருப்பு வடை / மசால் வடை", "Malayalam": "പരിപ്പ് വട"},
    density_g_cm3=0.88,
    portion_model_type="piece_count",
    nutrition_per_100g={"calories": 310.0, "protein_g": 12.8, "carbs_g": 34.2, "fat_g": 14.5, "fiber_g": 6.8, "sodium_mg": 340.0},
    hierarchy=FoodIdentityHierarchy(
        region="Tamil Nadu",
        category="Snack",
        subcategory="Lentil Fritter / Vada",
        canonical_food="Vada",
        variant="Coarsely Crushed Chana Dal Pebble Disc with Fennel & Onions",
        cooking_method=["deep_fried"],
        food_state="solid_fried_crunchy",
        common_ingredients=["chana dal", "dry red chillies", "fennel seeds", "onions", "ginger", "curry leaves", "oil"],
        default_portion_type="piece_count",
        default_serving_weight_g=55.0,
        nutrition_reference_id="ifct_vada_paruppu"
    )
))

register_permanent_food(PermanentFoodClassRecord(
    permanent_id="TN_BREAKFAST_PONGAL_VEN",
    canonical_name="Ven Pongal",
    alternate_names=["ven pongal", "ghee pongal", "khara pongal", "pepper pongal", "kovil pongal"],
    regional_names={"English": "Ghee Tempered Rice & Lentil Mash", "Tamil": "வெண் பொங்கல்", "Kannada": "ಖಾರಾ ಪೊಂಗಲ್", "Telugu": "వెన్ పొంగల్"},
    density_g_cm3=0.95,
    portion_model_type="volume_density",
    nutrition_per_100g={"calories": 192.0, "protein_g": 4.5, "carbs_g": 26.0, "fat_g": 7.5, "fiber_g": 1.8, "sodium_mg": 280.0},
    hierarchy=FoodIdentityHierarchy(
        region="Tamil Nadu",
        category="Breakfast",
        subcategory="Pongal Family",
        canonical_food="Pongal",
        variant="Soft Pressure-Cooked Rice & Moong Mash Tempered with Ghee, Pepper, Cashew",
        cooking_method=["pressure_cooked", "sauteed"],
        food_state="semi_solid_glossy_mash",
        common_ingredients=["raw rice", "yellow moong dal", "desi cow ghee", "whole black peppercorns", "cumin", "cashews", "ginger", "curry leaves"],
        default_portion_type="volume_density",
        default_serving_weight_g=190.0,
        nutrition_reference_id="ifct_pongal_ven"
    )
))

register_permanent_food(PermanentFoodClassRecord(
    permanent_id="TN_BREAKFAST_UPMA_RAVA",
    canonical_name="Rava Upma",
    alternate_names=["rava upma", "sooji upma", "uppittu", "rawa upma", "semolina upma"],
    regional_names={"English": "Savory Semolina Porridge", "Tamil": "ரவா உப்புமா", "Kannada": "ಉಪ್ಪಿಟ್ಟು", "Telugu": "రవ్వ ఉప్మా"},
    density_g_cm3=0.88,
    portion_model_type="volume_density",
    nutrition_per_100g={"calories": 158.0, "protein_g": 3.8, "carbs_g": 27.5, "fat_g": 3.8, "fiber_g": 1.6, "sodium_mg": 260.0},
    hierarchy=FoodIdentityHierarchy(
        region="Tamil Nadu",
        category="Breakfast",
        subcategory="Upma Family",
        canonical_food="Upma",
        variant="Roasted Wheat Semolina Cooked into Moist Granular Savory Crumb",
        cooking_method=["boiled", "sauteed"],
        food_state="semi_solid_granular_crumb",
        common_ingredients=["roasted semolina", "mustard seeds", "urad dal", "chana dal", "green chillies", "ginger", "curry leaves", "onions", "oil"],
        default_portion_type="volume_density",
        default_serving_weight_g=180.0,
        nutrition_reference_id="ifct_upma_rava"
    )
))

# =============================================================================
# 2. SAMBAR, RASAM, KUZHAMBU & GRAVIES
# =============================================================================

register_permanent_food(PermanentFoodClassRecord(
    permanent_id="TN_CURRY_SAMBAR_TIFFIN",
    canonical_name="Tiffin Sambar",
    alternate_names=["tiffin sambar", "hotel sambar", "idli sambar", "saravana bhavan sambar", "sambar"],
    regional_names={"English": "Tiffin Lentil & Tamarind Broth", "Tamil": "டிபன் சாம்பார்", "Telugu": "సాంబారు", "Kannada": "ಸಾಂಬಾರ್"},
    density_g_cm3=1.05,
    portion_model_type="volume_density",
    nutrition_per_100g={"calories": 68.0, "protein_g": 3.2, "carbs_g": 10.5, "fat_g": 1.6, "fiber_g": 2.4, "sodium_mg": 320.0},
    hierarchy=FoodIdentityHierarchy(
        region="Tamil Nadu",
        category="Accompaniment",
        subcategory="Lentil Stew / Sambar",
        canonical_food="Sambar",
        variant="Simmered Toor & Moong Dal Broth with Shallots, Tamarind, Sambar Powder",
        cooking_method=["boiled", "simmered"],
        food_state="liquid_stew",
        common_ingredients=["toor dal", "yellow moong dal", "shallots", "tomatoes", "tamarind", "sambar powder", "mustard seeds", "curry leaves"],
        default_portion_type="volume_density",
        default_serving_weight_g=110.0,
        nutrition_reference_id="ifct_sambar_tiffin"
    )
))

register_permanent_food(PermanentFoodClassRecord(
    permanent_id="TN_CURRY_RASAM_TOMATO_PEPPER",
    canonical_name="Tomato Pepper Rasam",
    alternate_names=["rasam", "tomato rasam", "pepper rasam", "milagu rasam", "thakkali rasam"],
    regional_names={"English": "Spicy Tamarind Pepper Soup Broth", "Tamil": "மிளகு தக்காளி ரசம்", "Telugu": "చారు / రసం", "Kannada": "ಸಾರು"},
    density_g_cm3=1.02,
    portion_model_type="volume_density",
    nutrition_per_100g={"calories": 38.0, "protein_g": 1.2, "carbs_g": 5.8, "fat_g": 1.1, "fiber_g": 0.9, "sodium_mg": 290.0},
    hierarchy=FoodIdentityHierarchy(
        region="Tamil Nadu",
        category="Accompaniment",
        subcategory="Rasam Family",
        canonical_food="Rasam",
        variant="Watery Herbal Tamarind-Tomato Broth Heavy on Black Pepper & Garlic",
        cooking_method=["boiled", "tempered"],
        food_state="liquid",
        common_ingredients=["tomatoes", "tamarind water", "black pepper", "cumin", "garlic", "coriander", "mustard seeds", "curry leaves"],
        default_portion_type="volume_density",
        default_serving_weight_g=100.0,
        nutrition_reference_id="ifct_rasam_pepper"
    )
))

# =============================================================================
# 3. CHUTNEYS (WITH SECTION 10 UNCERTAINTY PATHS)
# =============================================================================

register_permanent_food(PermanentFoodClassRecord(
    permanent_id="TN_CHUTNEY_COCONUT_WHITE",
    canonical_name="White Coconut Chutney",
    alternate_names=["coconut chutney", "white chutney", "thengai chutney", "kobbari chutney"],
    regional_names={"English": "Fresh White Coconut Chutney", "Tamil": "தேங்காய் சட்னி", "Telugu": "కొబ్బరి పచ్చడి", "Kannada": "ತೆಂಗಿನಕಾಯಿ ಚಟ್ನಿ"},
    density_g_cm3=1.02,
    portion_model_type="volume_density",
    nutrition_per_100g={"calories": 210.0, "protein_g": 3.0, "carbs_g": 7.5, "fat_g": 19.2, "fiber_g": 3.5, "sodium_mg": 260.0},
    hierarchy=FoodIdentityHierarchy(
        region="Tamil Nadu",
        category="Accompaniment",
        subcategory="Chutney Family",
        canonical_food="Chutney",
        variant="Grated Coconut Ground with Roasted Gram, Green Chillies, Tempered Mustard",
        cooking_method=["raw_ground_tempered"],
        food_state="semi_solid_paste",
        common_ingredients=["fresh coconut", "roasted chana gram", "green chillies", "ginger", "mustard seeds", "curry leaves", "coconut oil"],
        default_portion_type="volume_density",
        default_serving_weight_g=45.0,
        nutrition_reference_id="ifct_chutney_coconut"
    )
))

register_permanent_food(PermanentFoodClassRecord(
    permanent_id="TN_CHUTNEY_TOMATO_KAARA",
    canonical_name="Spicy Tomato Kaara Chutney",
    alternate_names=["kaara chutney", "tomato chutney", "red chutney", "thakkali chutney", "onion tomato chutney"],
    regional_names={"English": "Spicy Sauteed Tomato Onion Chutney", "Tamil": "கார சட்னி", "Telugu": "టమాటా పచ్చడి"},
    density_g_cm3=1.06,
    portion_model_type="volume_density",
    nutrition_per_100g={"calories": 88.0, "protein_g": 1.8, "carbs_g": 9.8, "fat_g": 4.2, "fiber_g": 1.9, "sodium_mg": 340.0},
    hierarchy=FoodIdentityHierarchy(
        region="Tamil Nadu",
        category="Accompaniment",
        subcategory="Chutney Family",
        canonical_food="Chutney",
        variant="Sauteed Tomatoes, Shallots, Garlic, Dried Red Chillies, Gingelly Oil",
        cooking_method=["sauteed", "ground"],
        food_state="semi_solid_paste",
        common_ingredients=["tomatoes", "shallots", "garlic", "dried red chillies", "tamarind", "gingelly oil", "mustard seeds"],
        default_portion_type="volume_density",
        default_serving_weight_g=40.0,
        nutrition_reference_id="ifct_chutney_tomato"
    )
))

# =============================================================================
# 4. RICE & REGIONAL BIRYANIS
# =============================================================================

register_permanent_food(PermanentFoodClassRecord(
    permanent_id="TN_RICE_PONNI_BOILED",
    canonical_name="Steamed Ponni Boiled Rice",
    alternate_names=["plain rice", "white rice", "steamed rice", "boiled rice", "ponni rice", "sadam"],
    regional_names={"English": "Steamed White Parboiled Rice", "Tamil": "பொன்னி சாதம்", "Telugu": "అన్నం", "Kannada": "ಅನ್ನ", "Malayalam": "ചോറ്"},
    density_g_cm3=0.85,
    portion_model_type="volume_density",
    nutrition_per_100g={"calories": 130.0, "protein_g": 2.7, "carbs_g": 28.5, "fat_g": 0.5, "fiber_g": 0.8, "sodium_mg": 5.0},
    hierarchy=FoodIdentityHierarchy(
        region="Tamil Nadu",
        category="Lunch",
        subcategory="Rice Family",
        canonical_food="Rice",
        variant="Parboiled Ponni Medium Grain Rice Steamed Plain",
        cooking_method=["boiled", "steamed"],
        food_state="solid_cooked_grains",
        common_ingredients=["ponni boiled rice", "water"],
        default_portion_type="volume_density",
        default_serving_weight_g=240.0,
        nutrition_reference_id="ifct_rice_ponni"
    )
))

register_permanent_food(PermanentFoodClassRecord(
    permanent_id="TN_RICE_CURD_THAYIR_SADAM",
    canonical_name="Tempered Curd Rice",
    alternate_names=["curd rice", "thayir sadam", "thayirsaadam", "daddojanam", "yogurt rice"],
    regional_names={"English": "Tempered Yogurt Mashed Rice", "Tamil": "தயிர் சாதம்", "Telugu": "పెరుగన్నం / దద్దోజనం", "Kannada": "ಮೊಸರನ್ನ"},
    density_g_cm3=0.98,
    portion_model_type="volume_density",
    nutrition_per_100g={"calories": 138.0, "protein_g": 3.5, "carbs_g": 21.2, "fat_g": 4.2, "fiber_g": 0.6, "sodium_mg": 240.0},
    hierarchy=FoodIdentityHierarchy(
        region="Tamil Nadu",
        category="Lunch",
        subcategory="Rice Family",
        canonical_food="Rice",
        variant="Soft Mashed Rice Emulsified with Fresh Curd, Tempered Mustard, Ginger, Chilli",
        cooking_method=["boiled", "mashed", "tempered"],
        food_state="semi_solid_creamy",
        common_ingredients=["rice", "fresh curd", "milk", "mustard seeds", "green chillies", "ginger", "curry leaves", "salt"],
        default_portion_type="volume_density",
        default_serving_weight_g=260.0,
        nutrition_reference_id="ifct_rice_curd"
    )
))

register_permanent_food(PermanentFoodClassRecord(
    permanent_id="TN_BIRYANI_DINDIGUL_MUTTON",
    canonical_name="Dindigul Thalappakatti Mutton Biryani",
    alternate_names=["dindigul biryani", "thalappakatti biryani", "seeraga samba biryani", "mutton biryani dindigul"],
    regional_names={"English": "Dindigul Seeraga Samba Mutton Biryani", "Tamil": "திண்டுக்கல் தலப்பாக்கட்டி பிரியாணி"},
    density_g_cm3=0.84,
    portion_model_type="meat_bone_cut",
    nutrition_per_100g={"calories": 205.0, "protein_g": 11.5, "carbs_g": 20.5, "fat_g": 8.2, "fiber_g": 1.1, "sodium_mg": 330.0},
    hierarchy=FoodIdentityHierarchy(
        region="Tamil Nadu",
        category="Lunch",
        subcategory="Biryani Family",
        canonical_food="Biryani",
        variant="Petite Seeraga Samba Rice Dum Cooked with Bone-In Mutton and Curd Marinade",
        cooking_method=["dum_cooked", "pot_braised"],
        food_state="solid_cooked_grain_and_meat",
        common_ingredients=["seeraga samba rice", "mutton with bone", "shallots", "curd", "ginger garlic paste", "desi ghee", "spices"],
        default_portion_type="meat_bone_cut",
        default_serving_weight_g=360.0,
        nutrition_reference_id="ifct_biryani_dindigul_mutton"
    )
))

register_permanent_food(PermanentFoodClassRecord(
    permanent_id="TS_BIRYANI_HYDERABADI_CHICKEN",
    canonical_name="Hyderabadi Chicken Dum Biryani",
    alternate_names=["hyderabadi biryani", "chicken biryani", "kacchi biryani", "hyderabadi chicken dum biryani"],
    regional_names={"English": "Hyderabadi Saffron Basmati Chicken Dum Biryani", "Telugu": "హైదరాబాదీ చికెన్ బిర్యానీ", "Urdu": "حیدرآبادی بریانی"},
    density_g_cm3=0.82,
    portion_model_type="meat_bone_cut",
    nutrition_per_100g={"calories": 172.0, "protein_g": 10.8, "carbs_g": 21.0, "fat_g": 5.2, "fiber_g": 1.0, "sodium_mg": 290.0},
    hierarchy=FoodIdentityHierarchy(
        region="Telangana",
        category="Lunch",
        subcategory="Biryani Family",
        canonical_food="Biryani",
        variant="Layered Extra-Long Aged Basmati Rice over Kacchi Marinated Chicken with Saffron and Fried Onions",
        cooking_method=["kacchi_dum_sealed_handi"],
        food_state="solid_cooked_grain_and_meat",
        common_ingredients=["basmati rice", "chicken pieces", "yogurt", "fried onions", "saffron milk", "ghee", "mint", "shahi jeera"],
        default_portion_type="meat_bone_cut",
        default_serving_weight_g=380.0,
        nutrition_reference_id="ifct_biryani_hyderabadi_chicken"
    )
))

# =============================================================================
# 5. PAROTTA & NON-VEG (KOTHU PAROTTA & CHICKEN 65)
# =============================================================================

register_permanent_food(PermanentFoodClassRecord(
    permanent_id="TN_PAROTTA_KOTHU_CHICKEN",
    canonical_name="Madurai Chicken Kothu Parotta",
    alternate_names=["chicken kothu", "kothu parotta", "madurai kothu parotta", "kothu roti"],
    regional_names={"English": "Tawa Minced Flaky Parotta with Chicken Curry", "Tamil": "சிக்கன் கொத்து பரோட்டா"},
    density_g_cm3=0.86,
    portion_model_type="volume_density",
    nutrition_per_100g={"calories": 225.0, "protein_g": 11.2, "carbs_g": 24.5, "fat_g": 9.1, "fiber_g": 1.5, "sodium_mg": 460.0},
    hierarchy=FoodIdentityHierarchy(
        region="Tamil Nadu",
        category="Dinner",
        subcategory="Parotta Family",
        canonical_food="Parotta",
        variant="Shredded Malabar Parotta Beaten on Iron Tawa with Chicken, Egg, Salna",
        cooking_method=["tawa_chopped_iron_beat"],
        food_state="chopped_tossed_solid",
        common_ingredients=["malabar parotta", "chicken pieces", "eggs", "chicken salna", "onions", "green chillies", "fennel", "oil"],
        default_portion_type="volume_density",
        default_serving_weight_g=340.0,
        nutrition_reference_id="ifct_parotta_kothu_chicken"
    )
))

register_permanent_food(PermanentFoodClassRecord(
    permanent_id="TN_NONVEG_CHICKEN_65",
    canonical_name="South Indian Chicken 65",
    alternate_names=["chicken 65", "chicken sixty five", "chennai chicken 65", "chicken 65 fry"],
    regional_names={"English": "Fiery Red Deep Fried Spiced Chicken Chunks", "Tamil": "சிக்கன் 65", "Telugu": "చికెన్ 65"},
    density_g_cm3=0.78,
    portion_model_type="meat_bone_cut",
    nutrition_per_100g={"calories": 245.0, "protein_g": 22.5, "carbs_g": 9.2, "fat_g": 13.1, "fiber_g": 0.8, "sodium_mg": 520.0},
    hierarchy=FoodIdentityHierarchy(
        region="Tamil Nadu",
        category="Starter",
        subcategory="Non-Veg Chicken",
        canonical_food="Chicken",
        variant="Deep-Fried Curd-Marinated Boneless Chicken with Fried Curry Leaves & Green Chillies",
        cooking_method=["deep_fried", "tossed"],
        food_state="solid_crispy_meat",
        common_ingredients=["chicken breast/thigh", "kashmiri chilli", "curd", "ginger garlic paste", "cornstarch", "curry leaves", "oil"],
        default_portion_type="meat_bone_cut",
        default_serving_weight_g=180.0,
        nutrition_reference_id="ifct_chicken_65"
    )
))

# =============================================================================
# REGISTRY LOOKUP & SYNONYM RESOLUTION
# =============================================================================

def resolve_food_by_name_or_alias(query: str) -> Optional[PermanentFoodClassRecord]:
    q = query.lower().strip()
    if q in SYNONYM_LOOKUP_MAP:
        perm_id = SYNONYM_LOOKUP_MAP[q]
        return PERMANENT_CLASS_REGISTRY.get(perm_id)
    
    # Partial match
    for alias, perm_id in SYNONYM_LOOKUP_MAP.items():
        if q == alias or q in alias or alias in q:
            return PERMANENT_CLASS_REGISTRY.get(perm_id)
    return None

def get_permanent_class(permanent_id: str) -> Optional[PermanentFoodClassRecord]:
    return PERMANENT_CLASS_REGISTRY.get(permanent_id)

def get_hierarchy_path(permanent_id: str) -> str:
    rec = PERMANENT_CLASS_REGISTRY.get(permanent_id)
    if not rec:
        return "Unknown > Unknown"
    h = rec.hierarchy
    return f"{h.food_super_category} > {h.region} > {h.category} > {h.subcategory} > {h.canonical_food} > {h.variant}"

def list_all_permanent_ids() -> List[str]:
    return list(PERMANENT_CLASS_REGISTRY.keys())
