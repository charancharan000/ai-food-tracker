"""
Indian Vegetarian Master Taxonomy & Identity Hierarchy (Part 12)
Implements Sections 1–12, 13–26, 49, 53, 54, 74, 75, 76 of Part 12 Master Training Specification.

Guarantees:
- Strict 14-Level Identity Traversal:
  Indian Food -> Vegetarian Food -> Region -> State -> Food Family -> Specific Dish ->
  Variant -> Main Ingredient -> Secondary Ingredients -> Cooking Method ->
  Texture/Consistency -> Portion -> Weight -> Nutrition
- Stable Class ID System (Section 54): IND-VEG-* format.
- 50+ Vegetarian Food Families (Section 3).
- Comprehensive Regional Datasets:
  * South India: Tamil Nadu (Poriyal, Kootu, Keerai), Kerala (Avial, Thoran, Sadya),
    Karnataka (Palya, Saagu, Huli), Andhra/Telangana (Vankaya, Pappu, Fry)
  * North India: Punjab, UP, Delhi, Rajasthan, Kashmir, Himachal (Paneer, Aloo, Sabzi, Kofta)
  * West India: Maharashtra (Usal, Zunka, Bharli Vangi), Gujarat (Undhiyu, Shaak), Goa (Xacuti, Foogath)
  * East India: Bengal (Aloo Posto, Shukto), Odisha (Dalma, Santula), Bihar (Chokha, Sattu)
  * Northeast India: Bamboo shoot, leafy greens, squash, fermented veg
- Specialized Category Inclusions:
  Paneer, Tofu/Soy, Mushroom, Legumes, Potatoes, Brinjal, Leafy Greens, Gourds,
  Jackfruit, Raw Banana, Cauliflower, Okra, Mixed Veg, Stuffed Veg.
- Robust Fallback System (Section 49 & 76):
  * "Indian vegetarian dish — exact identity uncertain" (IND_VEG_UNKNOWN_001)
  * "Vegetable curry — exact type uncertain" (IND_VEG_CURRY_UNKNOWN)
  * "Paneer-based dish — exact recipe uncertain" (IND_VEG_PANEER_UNKNOWN)
- Multilingual synonym mappings across 12 Indian languages (Section 53).
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class VegetarianHierarchy(BaseModel):
    level1_food: str = "Indian Food"
    level2_macro_category: str = "Vegetarian Food"
    level3_region: str          # South India, North India, West India, East India, Northeast India, Pan-India
    level4_state: str           # Tamil Nadu, Kerala, Punjab, Gujarat, West Bengal, etc.
    level5_food_family: str     # Poriyal, Kootu, Avial, Thoran, Sabzi, Paneer Dishes, Legume Dishes, etc.
    level6_specific_dish: str   # Beans Poriyal, Palak Paneer, Aloo Gobi, Undhiyu, Dalma, etc.
    level7_variant: str         # e.g., "Stir-fried french beans with grated coconut and mustard tempering"
    level8_main_ingredient: str # beans, paneer, potato, cauliflower, brinjal, etc.
    level9_secondary_ingredients: List[str] = Field(default_factory=list) # coconut, mustard, tomato, onion, cumin, etc.
    level10_cooking_method: str # Stir-fried, Boiled, Simmered, Deep-fried, Roasted, Steamed, Mashed, Raw
    level11_texture_consistency: str # Dry, Semi-dry, Thick gravy, Thin gravy, Creamy, Mashed, Crispy, Soft
    level12_portion_type: str   # weight_grams, volume_ml, piece_count
    level13_weight_g_default: float = 150.0
    level14_nutrition_ref_id: str


class VegetarianFoodClassRecord(BaseModel):
    canonical_food_id: str      # Stable ID (Section 54): IND-VEG-TN-POR-BEAN-001, etc.
    canonical_name: str         # Canonical English name
    hierarchy: VegetarianHierarchy
    food_family: str            # High-level class from Section 3
    specific_dish: str
    region: str                 # South India, North India, West India, East India, Northeast India, Pan-India
    state_or_city: str
    regional_names: Dict[str, str] = Field(default_factory=dict)
    alternate_names: List[str] = Field(default_factory=list)
    vegetarian: bool = True
    main_ingredient: str
    secondary_ingredients: List[str] = Field(default_factory=list)
    cooking_method: str = "Stir-fried"
    consistency: str = "Dry"    # Dry, Semi-dry, Thick gravy, Thin gravy, Creamy, Mashed, Crispy
    is_countable: bool = False
    piece_count_expected: Optional[int] = None
    default_portion_grams: float = 150.0
    density_g_ml: float = 1.05
    nutrition_per_100g: Dict[str, float] = Field(default_factory=dict)
    uncertainty_factors: List[str] = Field(default_factory=list)
    typical_oil_level: str = "Moderate visible oil"  # Low, Moderate, High, Oil pooling, Tempering visible, Ghee/butter


VEGETARIAN_TAXONOMY_REGISTRY: Dict[str, VegetarianFoodClassRecord] = {}
VEGETARIAN_SYNONYM_LOOKUP: Dict[str, str] = {}


def register_veg_food_class(record: VegetarianFoodClassRecord, alias_ids: Optional[List[str]] = None) -> VegetarianFoodClassRecord:
    VEGETARIAN_TAXONOMY_REGISTRY[record.canonical_food_id] = record
    VEGETARIAN_TAXONOMY_REGISTRY[record.canonical_food_id.lower()] = record
    if alias_ids:
        for aid in alias_ids:
            VEGETARIAN_TAXONOMY_REGISTRY[aid] = record
            VEGETARIAN_TAXONOMY_REGISTRY[aid.lower()] = record
            VEGETARIAN_SYNONYM_LOOKUP[aid.lower().strip()] = record.canonical_food_id
    VEGETARIAN_SYNONYM_LOOKUP[record.canonical_name.lower().strip()] = record.canonical_food_id
    for alt in record.alternate_names:
        VEGETARIAN_SYNONYM_LOOKUP[alt.lower().strip()] = record.canonical_food_id
    for reg_name in record.regional_names.values():
        VEGETARIAN_SYNONYM_LOOKUP[reg_name.lower().strip()] = record.canonical_food_id
    return record


# =============================================================================
# 1. SOUTH INDIA — TAMIL NADU (Section 5)
# =============================================================================

# 1.1 Beans Poriyal
register_veg_food_class(VegetarianFoodClassRecord(
    canonical_food_id="IND-VEG-TN-POR-BEAN-001",
    canonical_name="Beans Poriyal",
    hierarchy=VegetarianHierarchy(
        level3_region="South India",
        level4_state="Tamil Nadu",
        level5_food_family="Poriyal",
        level6_specific_dish="Beans Poriyal",
        level7_variant="Finely Diced French Beans Stir-Fried with Mustard, Urad Dal, Curry Leaves and Fresh Coconut",
        level8_main_ingredient="beans",
        level9_secondary_ingredients=["coconut", "mustard", "curry_leaves", "urad_dal"],
        level10_cooking_method="Stir-fried",
        level11_texture_consistency="Dry",
        level12_portion_type="weight_grams",
        level13_weight_g_default=80.0,
        level14_nutrition_ref_id="ifct_beans_poriyal"
    ),
    food_family="Poriyal",
    specific_dish="Beans Poriyal",
    region="South India",
    state_or_city="Tamil Nadu",
    regional_names={"English": "Beans Poriyal", "Tamil": "பீன்ஸ் பொரியல்", "Malayalam": "ബീൻസ് തോരൻ", "Telugu": "బీన్స్ తాలింపు"},
    alternate_names=["beans poriyal", "french beans poriyal", "beans dry curry", "beans stir fry"],
    vegetarian=True,
    main_ingredient="beans",
    secondary_ingredients=["coconut", "mustard", "curry_leaves"],
    cooking_method="Stir-fried",
    consistency="Dry",
    default_portion_grams=80.0,
    density_g_ml=0.92,
    nutrition_per_100g={"calories": 75.0, "protein_g": 2.6, "carbs_g": 8.0, "fat_g": 3.8, "fiber_g": 3.5, "sodium_mg": 180.0},
    uncertainty_factors=["grated_coconut_amount", "tempering_oil"],
    typical_oil_level="Tempering visible"
), alias_ids=["IND_VEG_TN_BEANS_PORIYAL", "beans_poriyal"])

# 1.2 Carrot & Cabbage Poriyal
register_veg_food_class(VegetarianFoodClassRecord(
    canonical_food_id="IND-VEG-TN-POR-CARROT-001",
    canonical_name="Carrot Cabbage Poriyal",
    hierarchy=VegetarianHierarchy(
        level3_region="South India",
        level4_state="Tamil Nadu",
        level5_food_family="Poriyal",
        level6_specific_dish="Carrot Cabbage Poriyal",
        level7_variant="Shredded Carrots and Cabbage Steamed and Tempered with Coconut",
        level8_main_ingredient="carrot",
        level9_secondary_ingredients=["cabbage", "coconut", "mustard", "green_chilli"],
        level10_cooking_method="Stir-fried",
        level11_texture_consistency="Dry",
        level12_portion_type="weight_grams",
        level13_weight_g_default=85.0,
        level14_nutrition_ref_id="ifct_carrot_cabbage_poriyal"
    ),
    food_family="Poriyal",
    specific_dish="Carrot Cabbage Poriyal",
    region="South India",
    state_or_city="Tamil Nadu",
    regional_names={"English": "Carrot Poriyal", "Tamil": "கேரட் முட்டைக்கோஸ் பொரியல்"},
    alternate_names=["carrot poriyal", "cabbage poriyal", "carrot cabbage poriyal", "cabbage carrot stir fry"],
    vegetarian=True,
    main_ingredient="carrot",
    secondary_ingredients=["cabbage", "coconut", "mustard"],
    cooking_method="Stir-fried",
    consistency="Dry",
    default_portion_grams=85.0,
    density_g_ml=0.94,
    nutrition_per_100g={"calories": 68.0, "protein_g": 1.8, "carbs_g": 9.2, "fat_g": 2.8, "fiber_g": 3.2, "sodium_mg": 160.0},
    uncertainty_factors=["coconut_volume"],
    typical_oil_level="Low visible oil"
), alias_ids=["IND_VEG_TN_CARROT_PORIYAL", "IND_VEG_TN_CABBAGE_PORIYAL"])

# 1.3 Beetroot Poriyal
register_veg_food_class(VegetarianFoodClassRecord(
    canonical_food_id="IND-VEG-TN-POR-BEET-001",
    canonical_name="Beetroot Poriyal",
    hierarchy=VegetarianHierarchy(
        level3_region="South India",
        level4_state="Tamil Nadu",
        level5_food_family="Poriyal",
        level6_specific_dish="Beetroot Poriyal",
        level7_variant="Grated or Diced Deep Purple Beetroot Sautéed with Mustard, Chillies and Coconut",
        level8_main_ingredient="beetroot",
        level9_secondary_ingredients=["coconut", "mustard", "curry_leaves"],
        level10_cooking_method="Stir-fried",
        level11_texture_consistency="Dry",
        level12_portion_type="weight_grams",
        level13_weight_g_default=80.0,
        level14_nutrition_ref_id="ifct_beetroot_poriyal"
    ),
    food_family="Poriyal",
    specific_dish="Beetroot Poriyal",
    region="South India",
    state_or_city="Tamil Nadu",
    regional_names={"English": "Beetroot Poriyal", "Tamil": "பீட்ரூட் பொரியல்"},
    alternate_names=["beetroot poriyal", "beet poriyal", "beetroot stir fry", "beetroot thoran"],
    vegetarian=True,
    main_ingredient="beetroot",
    secondary_ingredients=["coconut", "mustard"],
    cooking_method="Stir-fried",
    consistency="Dry",
    default_portion_grams=80.0,
    density_g_ml=0.95,
    nutrition_per_100g={"calories": 72.0, "protein_g": 1.9, "carbs_g": 10.5, "fat_g": 2.6, "fiber_g": 2.9, "sodium_mg": 170.0},
    uncertainty_factors=["natural_sugars", "coconut_ratio"],
    typical_oil_level="Low visible oil"
), alias_ids=["IND_VEG_TN_BEETROOT_PORIYAL"])

# 1.4 Vendakkai (Okra) Poriyal / Roast
register_veg_food_class(VegetarianFoodClassRecord(
    canonical_food_id="IND-VEG-TN-POR-VENDAKKAI-001",
    canonical_name="Vendakkai Poriyal (Okra Stir-Fry)",
    hierarchy=VegetarianHierarchy(
        level3_region="South India",
        level4_state="Tamil Nadu",
        level5_food_family="Okra/Ladies Finger Dishes",
        level6_specific_dish="Vendakkai Poriyal",
        level7_variant="Crisp-Sautéed Sliced Okra without Sliminess, Seasoned with Sambar Powder and Mustard",
        level8_main_ingredient="okra",
        level9_secondary_ingredients=["mustard", "sambar_powder", "curry_leaves"],
        level10_cooking_method="Pan-fried",
        level11_texture_consistency="Dry",
        level12_portion_type="weight_grams",
        level13_weight_g_default=90.0,
        level14_nutrition_ref_id="ifct_vendakkai_poriyal"
    ),
    food_family="Okra/Ladies Finger Dishes",
    specific_dish="Vendakkai Poriyal",
    region="South India",
    state_or_city="Tamil Nadu",
    regional_names={"English": "Okra Fry", "Tamil": "வெண்டைக்காய் பொரியல் / வறுவல்", "Hindi": "भिंडी फ्राई"},
    alternate_names=["vendakkai poriyal", "vendakkai varuval", "okra fry", "bhindi poriyal", "ladies finger fry"],
    vegetarian=True,
    main_ingredient="okra",
    secondary_ingredients=["sambar_powder", "mustard"],
    cooking_method="Pan-fried",
    consistency="Dry",
    default_portion_grams=90.0,
    density_g_ml=0.96,
    nutrition_per_100g={"calories": 95.0, "protein_g": 2.2, "carbs_g": 8.5, "fat_g": 5.8, "fiber_g": 3.6, "sodium_mg": 210.0},
    uncertainty_factors=["roasting_oil_absorption"],
    typical_oil_level="Moderate visible oil"
), alias_ids=["IND_VEG_TN_VENDAKKAI_PORIYAL", "vendakkai_poriyal"])

# 1.5 Vazhaikkai (Raw Banana) Poriyal / Varuval
register_veg_food_class(VegetarianFoodClassRecord(
    canonical_food_id="IND-VEG-TN-POR-VAZHAI-001",
    canonical_name="Vazhaikkai Varuval (Raw Banana Roast)",
    hierarchy=VegetarianHierarchy(
        level3_region="South India",
        level4_state="Tamil Nadu",
        level5_food_family="Raw Banana Dishes",
        level6_specific_dish="Vazhaikkai Varuval",
        level7_variant="Thick Sliced Plantain Cubes Pan-Roasted with Chilli, Coriander and Fennel",
        level8_main_ingredient="raw_banana",
        level9_secondary_ingredients=["chilli_powder", "fennel", "garlic", "curry_leaves"],
        level10_cooking_method="Pan-roasted",
        level11_texture_consistency="Crispy",
        level12_portion_type="weight_grams",
        level13_weight_g_default=100.0,
        level14_nutrition_ref_id="ifct_vazhaikkai_varuval"
    ),
    food_family="Raw Banana Dishes",
    specific_dish="Vazhaikkai Varuval",
    region="South India",
    state_or_city="Tamil Nadu",
    regional_names={"English": "Raw Banana Roast", "Tamil": "வாழைக்காய் வறுவல்", "Malayalam": "വാഴക്ക വറുത്തത്"},
    alternate_names=["vazhaikkai varuval", "vazhaikkai poriyal", "raw banana fry", "plantain roast", "kaccha kela fry"],
    vegetarian=True,
    main_ingredient="raw_banana",
    secondary_ingredients=["chilli", "fennel"],
    cooking_method="Pan-roasted",
    consistency="Crispy",
    default_portion_grams=100.0,
    density_g_ml=1.02,
    nutrition_per_100g={"calories": 140.0, "protein_g": 1.8, "carbs_g": 24.5, "fat_g": 4.5, "fiber_g": 3.0, "sodium_mg": 240.0},
    uncertainty_factors=["starch_density", "surface_roast_oil"],
    typical_oil_level="Moderate visible oil"
), alias_ids=["IND_VEG_TN_VAZHAIKKAI_VARUVAL", "raw_banana_roast"])

# 1.6 Chow Chow Kootu
register_veg_food_class(VegetarianFoodClassRecord(
    canonical_food_id="IND-VEG-TN-KOO-CHOWCHOW-001",
    canonical_name="Chow Chow Kootu",
    hierarchy=VegetarianHierarchy(
        level3_region="South India",
        level4_state="Tamil Nadu",
        level5_food_family="Kootu",
        level6_specific_dish="Chow Chow Kootu",
        level7_variant="Diced Chayote Squash Cooked with Moong Dal, Coconut-Cumin Paste and Mustard Tempering",
        level8_main_ingredient="chow_chow",
        level9_secondary_ingredients=["moong_dal", "coconut", "cumin", "green_chilli"],
        level10_cooking_method="Simmered",
        level11_texture_consistency="Thick gravy",
        level12_portion_type="volume_ml",
        level13_weight_g_default=140.0,
        level14_nutrition_ref_id="ifct_chow_chow_kootu"
    ),
    food_family="Kootu",
    specific_dish="Chow Chow Kootu",
    region="South India",
    state_or_city="Tamil Nadu",
    regional_names={"English": "Chow Chow Kootu", "Tamil": "சௌ சௌ கூட்டு"},
    alternate_names=["chow chow kootu", "chayote kootu", "chow chow dal", "chayote squash kootu"],
    vegetarian=True,
    main_ingredient="chow_chow",
    secondary_ingredients=["moong_dal", "coconut", "cumin"],
    cooking_method="Simmered",
    consistency="Thick gravy",
    default_portion_grams=140.0,
    density_g_ml=1.10,
    nutrition_per_100g={"calories": 85.0, "protein_g": 3.2, "carbs_g": 10.5, "fat_g": 3.5, "fiber_g": 2.8, "sodium_mg": 230.0},
    uncertainty_factors=["coconut_paste_ratio", "dal_thickness"],
    typical_oil_level="Tempering visible"
), alias_ids=["IND_VEG_TN_CHOW_CHOW_KOOTU", "chow_chow_kootu"])

# 1.7 Sorakkai (Bottle Gourd) / Poosanikai (Ash Gourd) Kootu
register_veg_food_class(VegetarianFoodClassRecord(
    canonical_food_id="IND-VEG-TN-KOO-SORAKKAI-001",
    canonical_name="Sorakkai / Poosanikai Kootu",
    hierarchy=VegetarianHierarchy(
        level3_region="South India",
        level4_state="Tamil Nadu",
        level5_food_family="Bottle Gourd Dishes",
        level6_specific_dish="Sorakkai Kootu",
        level7_variant="Tender Bottle Gourd or Ash Gourd Cubes Stewed with Chana Dal and Ground Coconut",
        level8_main_ingredient="bottle_gourd",
        level9_secondary_ingredients=["chana_dal", "coconut", "cumin", "peppercorns"],
        level10_cooking_method="Simmered",
        level11_texture_consistency="Thick gravy",
        level12_portion_type="volume_ml",
        level13_weight_g_default=140.0,
        level14_nutrition_ref_id="ifct_sorakkai_kootu"
    ),
    food_family="Bottle Gourd Dishes",
    specific_dish="Sorakkai Kootu",
    region="South India",
    state_or_city="Tamil Nadu",
    regional_names={"English": "Bottle Gourd Kootu", "Tamil": "சுரைக்காய் கூட்டு / பூசணிக்காய் கூட்டு"},
    alternate_names=["sorakkai kootu", "poosanikai kootu", "lauki kootu", "ash gourd kootu", "bottle gourd stew"],
    vegetarian=True,
    main_ingredient="bottle_gourd",
    secondary_ingredients=["chana_dal", "coconut"],
    cooking_method="Simmered",
    consistency="Thick gravy",
    default_portion_grams=140.0,
    density_g_ml=1.09,
    nutrition_per_100g={"calories": 78.0, "protein_g": 2.9, "carbs_g": 9.5, "fat_g": 3.0, "fiber_g": 2.5, "sodium_mg": 210.0},
    uncertainty_factors=["gourd_water_content", "coconut_paste"],
    typical_oil_level="Tempering visible"
), alias_ids=["IND_VEG_TN_POOSANIKAI_KOOTU", "sorakkai_kootu"])

# 1.8 Keerai Masiyal / Keerai Kootu (Greens Mash)
register_veg_food_class(VegetarianFoodClassRecord(
    canonical_food_id="IND-VEG-TN-KEE-MASIYAL-001",
    canonical_name="Keerai Masiyal",
    hierarchy=VegetarianHierarchy(
        level3_region="South India",
        level4_state="Tamil Nadu",
        level5_food_family="Leafy Green Dishes",
        level6_specific_dish="Keerai Masiyal",
        level7_variant="Slow-Cooked Mashed Amaranth or Spinach Greens Seasoned with Garlic, Cumin and Ghee",
        level8_main_ingredient="amaranth_greens",
        level9_secondary_ingredients=["garlic", "cumin", "shallots", "ghee"],
        level10_cooking_method="Mashed",
        level11_texture_consistency="Mashed",
        level12_portion_type="volume_ml",
        level13_weight_g_default=120.0,
        level14_nutrition_ref_id="ifct_keerai_masiyal"
    ),
    food_family="Leafy Green Dishes",
    specific_dish="Keerai Masiyal",
    region="South India",
    state_or_city="Tamil Nadu",
    regional_names={"English": "Greens Mash", "Tamil": "கீரை மசியல் / கடைசல்"},
    alternate_names=["keerai masiyal", "keerai kadaisal", "spinach masiyal", "paruppu keerai", "greens mash"],
    vegetarian=True,
    main_ingredient="amaranth_greens",
    secondary_ingredients=["garlic", "cumin", "ghee"],
    cooking_method="Mashed",
    consistency="Mashed",
    default_portion_grams=120.0,
    density_g_ml=1.06,
    nutrition_per_100g={"calories": 62.0, "protein_g": 3.5, "carbs_g": 5.5, "fat_g": 2.8, "fiber_g": 3.8, "sodium_mg": 190.0},
    uncertainty_factors=["added_ghee_tempering"],
    typical_oil_level="Tempering visible"
), alias_ids=["IND_VEG_TN_KEERAI_MASIYAL", "keerai_masiyal"])

# 1.9 Ennai Kathirikai Kuzhambu (Stuffed Brinjal Gravy)
register_veg_food_class(VegetarianFoodClassRecord(
    canonical_food_id="IND-VEG-TN-KUZ-KATHIRIKAI-001",
    canonical_name="Ennai Kathirikai Kuzhambu",
    hierarchy=VegetarianHierarchy(
        level3_region="South India",
        level4_state="Tamil Nadu",
        level5_food_family="Brinjal/Eggplant Dishes",
        level6_specific_dish="Ennai Kathirikai",
        level7_variant="Small Baby Brinjals Slit and Shallow Fried in Sesame Oil, Cooked in Tangy Spicy Tamarind Gravy",
        level8_main_ingredient="brinjal",
        level9_secondary_ingredients=["tamarind", "sesame_oil", "shallots", "fenugreek", "peanuts"],
        level10_cooking_method="Simmered",
        level11_texture_consistency="Thick gravy",
        level12_portion_type="volume_ml",
        level13_weight_g_default=150.0,
        level14_nutrition_ref_id="ifct_ennai_kathirikai"
    ),
    food_family="Brinjal/Eggplant Dishes",
    specific_dish="Ennai Kathirikai Kuzhambu",
    region="South India",
    state_or_city="Tamil Nadu / Chettinad",
    regional_names={"English": "Stuffed Brinjal Curry", "Tamil": "எண்ணெய் கத்திரிக்காய் குழம்பு"},
    alternate_names=["ennai kathirikai kuzhambu", "ennai kathirikai", "chettinad brinjal gravy", "bagara baingan south"],
    vegetarian=True,
    main_ingredient="brinjal",
    secondary_ingredients=["tamarind", "sesame_oil", "shallots"],
    cooking_method="Simmered",
    consistency="Thick gravy",
    default_portion_grams=150.0,
    density_g_ml=1.10,
    nutrition_per_100g={"calories": 135.0, "protein_g": 2.2, "carbs_g": 9.0, "fat_g": 10.5, "fiber_g": 3.2, "sodium_mg": 380.0},
    uncertainty_factors=["sesame_gingelly_oil_glaze"],
    typical_oil_level="High visible oil"
), alias_ids=["IND_VEG_TN_ENNAI_KATHIRIKAI", "ennai_kathirikai"])


# =============================================================================
# 2. SOUTH INDIA — KERALA (Section 6)
# =============================================================================

# 2.1 Kerala Avial
register_veg_food_class(VegetarianFoodClassRecord(
    canonical_food_id="IND-VEG-KL-AVI-001",
    canonical_name="Kerala Avial",
    hierarchy=VegetarianHierarchy(
        level3_region="South India",
        level4_state="Kerala",
        level5_food_family="Avial",
        level6_specific_dish="Avial",
        level7_variant="Baton-Cut Mixed Vegetables Cooked with Coarsely Ground Coconut, Green Chillies, Curd and Finished with Coconut Oil & Curry Leaves",
        level8_main_ingredient="mixed_vegetables",
        level9_secondary_ingredients=["coconut", "curd", "coconut_oil", "curry_leaves", "raw_banana", "drumstick", "yam"],
        level10_cooking_method="Steamed and simmered",
        level11_texture_consistency="Semi-dry",
        level12_portion_type="weight_grams",
        level13_weight_g_default=120.0,
        level14_nutrition_ref_id="ifct_kerala_avial"
    ),
    food_family="Avial",
    specific_dish="Avial",
    region="South India",
    state_or_city="Kerala / Tamil Nadu",
    regional_names={"English": "Avial", "Malayalam": "അവിയൽ", "Tamil": "அவியல்"},
    alternate_names=["avial", "aviyal", "kerala avial", "sadya avial"],
    vegetarian=True,
    main_ingredient="mixed_vegetables",
    secondary_ingredients=["coconut", "curd", "coconut_oil"],
    cooking_method="Steamed and simmered",
    consistency="Semi-dry",
    default_portion_grams=120.0,
    density_g_ml=1.04,
    nutrition_per_100g={"calories": 115.0, "protein_g": 2.5, "carbs_g": 9.5, "fat_g": 7.5, "fiber_g": 3.6, "sodium_mg": 220.0},
    uncertainty_factors=["coconut_paste_mass", "raw_coconut_oil_finish"],
    typical_oil_level="Coconut-based fat appearance"
), alias_ids=["IND_VEG_KL_AVIAL", "kerala_avial"])

# 2.2 Kerala Cabbage / Beans Thoran
register_veg_food_class(VegetarianFoodClassRecord(
    canonical_food_id="IND-VEG-KL-THO-CABBAGE-001",
    canonical_name="Kerala Cabbage Thoran",
    hierarchy=VegetarianHierarchy(
        level3_region="South India",
        level4_state="Kerala",
        level5_food_family="Thoran",
        level6_specific_dish="Cabbage Thoran",
        level7_variant="Finely Shredded Cabbage Sautéed with Mustard, Shallots, Green Chillies and Generous Grated Coconut",
        level8_main_ingredient="cabbage",
        level9_secondary_ingredients=["coconut", "shallots", "mustard", "green_chilli"],
        level10_cooking_method="Stir-fried",
        level11_texture_consistency="Dry",
        level12_portion_type="weight_grams",
        level13_weight_g_default=85.0,
        level14_nutrition_ref_id="ifct_cabbage_thoran"
    ),
    food_family="Thoran",
    specific_dish="Cabbage Thoran",
    region="South India",
    state_or_city="Kerala",
    regional_names={"English": "Cabbage Thoran", "Malayalam": "കാബേജ് തോരൻ"},
    alternate_names=["cabbage thoran", "thoran", "kerala thoran", "beans thoran", "upperi"],
    vegetarian=True,
    main_ingredient="cabbage",
    secondary_ingredients=["coconut", "shallots", "mustard"],
    cooking_method="Stir-fried",
    consistency="Dry",
    default_portion_grams=85.0,
    density_g_ml=0.92,
    nutrition_per_100g={"calories": 82.0, "protein_g": 2.2, "carbs_g": 7.2, "fat_g": 5.2, "fiber_g": 3.0, "sodium_mg": 170.0},
    uncertainty_factors=["coconut_amount", "shallots_volume"],
    typical_oil_level="Tempering visible"
), alias_ids=["IND_VEG_KL_THORAN", "cabbage_thoran"])

# 2.3 Kerala Olan
register_veg_food_class(VegetarianFoodClassRecord(
    canonical_food_id="IND-VEG-KL-OLA-001",
    canonical_name="Kerala Olan",
    hierarchy=VegetarianHierarchy(
        level3_region="South India",
        level4_state="Kerala",
        level5_food_family="Ash Gourd Dishes",
        level6_specific_dish="Olan",
        level7_variant="Ash Gourd and Cowpeas (Vanpayar) Simmered in Light Coconut Milk, Finished with Coconut Oil & Fresh Curry Leaves",
        level8_main_ingredient="ash_gourd",
        level9_secondary_ingredients=["cowpea", "coconut_milk", "green_chilli", "coconut_oil"],
        level10_cooking_method="Simmered",
        level11_texture_consistency="Semi-dry",
        level12_portion_type="volume_ml",
        level13_weight_g_default=110.0,
        level14_nutrition_ref_id="ifct_kerala_olan"
    ),
    food_family="Ash Gourd Dishes",
    specific_dish="Olan",
    region="South India",
    state_or_city="Kerala",
    regional_names={"English": "Olan", "Malayalam": "ഓലൻ"},
    alternate_names=["olan", "kerala olan", "sadya olan", "ash gourd cowpea olan"],
    vegetarian=True,
    main_ingredient="ash_gourd",
    secondary_ingredients=["cowpea", "coconut_milk"],
    cooking_method="Simmered",
    consistency="Semi-dry",
    default_portion_grams=110.0,
    density_g_ml=1.03,
    nutrition_per_100g={"calories": 95.0, "protein_g": 2.8, "carbs_g": 8.5, "fat_g": 5.8, "fiber_g": 2.4, "sodium_mg": 180.0},
    uncertainty_factors=["coconut_milk_fat_thickness"],
    typical_oil_level="Coconut-based fat appearance"
), alias_ids=["IND_VEG_KL_OLAN", "kerala_olan"])

# 2.4 Kerala Erissery (Pumpkin & Toasted Coconut)
register_veg_food_class(VegetarianFoodClassRecord(
    canonical_food_id="IND-VEG-KL-ERI-001",
    canonical_name="Kerala Mathanga Erissery",
    hierarchy=VegetarianHierarchy(
        level3_region="South India",
        level4_state="Kerala",
        level5_food_family="Pumpkin Dishes",
        level6_specific_dish="Mathanga Erissery",
        level7_variant="Yellow Pumpkin and Vanpayar Stewed with Ground Coconut, Topped with Golden Roasted Coconut and Mustard",
        level8_main_ingredient="pumpkin",
        level9_secondary_ingredients=["cowpea", "roasted_coconut", "cumin", "pepper"],
        level10_cooking_method="Simmered and tempered",
        level11_texture_consistency="Thick gravy",
        level12_portion_type="volume_ml",
        level13_weight_g_default=130.0,
        level14_nutrition_ref_id="ifct_mathanga_erissery"
    ),
    food_family="Pumpkin Dishes",
    specific_dish="Mathanga Erissery",
    region="South India",
    state_or_city="Kerala",
    regional_names={"English": "Pumpkin Erissery", "Malayalam": "മത്തങ്ങ എരിശ്ശേരി"},
    alternate_names=["erissery", "mathanga erissery", "pumpkin erissery", "kerala erissery", "kaya erissery"],
    vegetarian=True,
    main_ingredient="pumpkin",
    secondary_ingredients=["cowpea", "roasted_coconut"],
    cooking_method="Simmered and tempered",
    consistency="Thick gravy",
    default_portion_grams=130.0,
    density_g_ml=1.08,
    nutrition_per_100g={"calories": 110.0, "protein_g": 3.0, "carbs_g": 12.0, "fat_g": 5.5, "fiber_g": 3.2, "sodium_mg": 210.0},
    uncertainty_factors=["toasted_coconut_garnish_volume"],
    typical_oil_level="Tempering visible"
), alias_ids=["IND_VEG_KL_ERISSERY", "mathanga_erissery"])

# 2.5 Kerala Kalan / Pulissery (Yam & Plantain Yogurt Gravy)
register_veg_food_class(VegetarianFoodClassRecord(
    canonical_food_id="IND-VEG-KL-KAL-001",
    canonical_name="Kerala Kalan / Mor Pulissery",
    hierarchy=VegetarianHierarchy(
        level3_region="South India",
        level4_state="Kerala",
        level5_food_family="Yogurt-Based Vegetarian Dishes",
        level6_specific_dish="Kalan",
        level7_variant="Elephant Foot Yam and Raw Plantain Cooked in Sour Buttermilk with Coconut-Black Pepper Paste, Reduced Thick",
        level8_main_ingredient="curd",
        level9_secondary_ingredients=["yam", "raw_banana", "coconut", "black_pepper", "fenugreek"],
        level10_cooking_method="Slow simmered",
        level11_texture_consistency="Thick gravy",
        level12_portion_type="volume_ml",
        level13_weight_g_default=120.0,
        level14_nutrition_ref_id="ifct_kerala_kalan"
    ),
    food_family="Yogurt-Based Vegetarian Dishes",
    specific_dish="Kalan",
    region="South India",
    state_or_city="Kerala",
    regional_names={"English": "Kalan", "Malayalam": "കാളൻ / പുളിശ്ശേരി"},
    alternate_names=["kalan", "pulissery", "kerala kalan", "mor pulissery", "sadya kalan"],
    vegetarian=True,
    main_ingredient="curd",
    secondary_ingredients=["yam", "coconut", "black_pepper"],
    cooking_method="Slow simmered",
    consistency="Thick gravy",
    default_portion_grams=120.0,
    density_g_ml=1.09,
    nutrition_per_100g={"calories": 125.0, "protein_g": 3.5, "carbs_g": 11.5, "fat_g": 7.0, "fiber_g": 2.5, "sodium_mg": 240.0},
    uncertainty_factors=["sour_dahi_fat", "pepper_heat"],
    typical_oil_level="Moderate visible oil"
), alias_ids=["IND_VEG_KL_KALAN", "IND_VEG_KL_PULISSERY"])

# 2.6 Kerala Kadala Curry
register_veg_food_class(VegetarianFoodClassRecord(
    canonical_food_id="IND-VEG-KL-KADALA-001",
    canonical_name="Kerala Kadala Curry",
    hierarchy=VegetarianHierarchy(
        level3_region="South India",
        level4_state="Kerala",
        level5_food_family="Black-Eyed Pea / Chickpea Dishes",
        level6_specific_dish="Kadala Curry",
        level7_variant="Black Chickpeas Simmered in Roasted Coconut, Coriander and Garam Masala Gravy",
        level8_main_ingredient="black_chickpeas",
        level9_secondary_ingredients=["roasted_coconut", "shallots", "curry_leaves", "coconut_oil"],
        level10_cooking_method="Simmered",
        level11_texture_consistency="Thick gravy",
        level12_portion_type="volume_ml",
        level13_weight_g_default=160.0,
        level14_nutrition_ref_id="ifct_kadala_curry"
    ),
    food_family="Black-Eyed Pea / Chickpea Dishes",
    specific_dish="Kadala Curry",
    region="South India",
    state_or_city="Kerala",
    regional_names={"English": "Black Chickpea Curry", "Malayalam": "കടലക്കറി"},
    alternate_names=["kadala curry", "kerala kadala curry", "puttu kadala curry", "black chana curry kerala"],
    vegetarian=True,
    main_ingredient="black_chickpeas",
    secondary_ingredients=["roasted_coconut", "shallots"],
    cooking_method="Simmered",
    consistency="Thick gravy",
    default_portion_grams=160.0,
    density_g_ml=1.12,
    nutrition_per_100g={"calories": 155.0, "protein_g": 7.2, "carbs_g": 18.5, "fat_g": 6.2, "fiber_g": 5.8, "sodium_mg": 310.0},
    uncertainty_factors=["roasted_coconut_paste_ratio"],
    typical_oil_level="Moderate visible oil"
), alias_ids=["IND_VEG_KL_KADALA_CURRY", "kadala_curry"])


# =============================================================================
# 3. SOUTH INDIA — KARNATAKA & ANDHRA (Sections 7, 8)
# =============================================================================

# 3.1 Karnataka Vegetable Saagu
register_veg_food_class(VegetarianFoodClassRecord(
    canonical_food_id="IND-VEG-KA-SAAGU-001",
    canonical_name="Karnataka Mixed Vegetable Saagu",
    hierarchy=VegetarianHierarchy(
        level3_region="South India",
        level4_state="Karnataka",
        level5_food_family="Vegetable Curry",
        level6_specific_dish="Vegetable Saagu",
        level7_variant="Potato, Carrot, Peas and Beans Stewed in Coriander-Spiced Coconut and Roasted Gram Gravy",
        level8_main_ingredient="mixed_vegetables",
        level9_secondary_ingredients=["coconut", "roasted_gram", "coriander", "cinnamon"],
        level10_cooking_method="Simmered",
        level11_texture_consistency="Thick gravy",
        level12_portion_type="volume_ml",
        level13_weight_g_default=150.0,
        level14_nutrition_ref_id="ifct_veg_saagu"
    ),
    food_family="Vegetable Curry",
    specific_dish="Vegetable Saagu",
    region="South India",
    state_or_city="Karnataka / Bangalore",
    regional_names={"English": "Veg Saagu", "Kannada": "ತರಕಾರಿ ಸಾಗು"},
    alternate_names=["vegetable saagu", "veg saagu", "karnataka saagu", "poori saagu", "set dosa saagu"],
    vegetarian=True,
    main_ingredient="mixed_vegetables",
    secondary_ingredients=["coconut", "roasted_gram"],
    cooking_method="Simmered",
    consistency="Thick gravy",
    default_portion_grams=150.0,
    density_g_ml=1.10,
    nutrition_per_100g={"calories": 105.0, "protein_g": 3.0, "carbs_g": 12.5, "fat_g": 4.8, "fiber_g": 3.0, "sodium_mg": 260.0},
    uncertainty_factors=["roasted_gram_thickener"],
    typical_oil_level="Moderate visible oil"
), alias_ids=["IND_VEG_KA_VEG_SAAGU", "veg_saagu"])

# 3.2 Andhra Gutti Vankaya Kura (Stuffed Brinjal Curry)
register_veg_food_class(VegetarianFoodClassRecord(
    canonical_food_id="IND-VEG-AP-GUTTI-VANKAYA-001",
    canonical_name="Andhra Gutti Vankaya Kura",
    hierarchy=VegetarianHierarchy(
        level3_region="South India",
        level4_state="Andhra Pradesh / Telangana",
        level5_food_family="Brinjal/Eggplant Dishes",
        level6_specific_dish="Gutti Vankaya",
        level7_variant="Whole Small Brinjals Stuffed with Roasted Peanuts, Sesame, Coconut and Spices, Simmered in Thick Gravy",
        level8_main_ingredient="brinjal",
        level9_secondary_ingredients=["peanuts", "sesame_seeds", "coconut", "tamarind", "shallots"],
        level10_cooking_method="Simmered",
        level11_texture_consistency="Thick gravy",
        level12_portion_type="weight_grams",
        level13_weight_g_default=160.0,
        level14_nutrition_ref_id="ifct_gutti_vankaya"
    ),
    food_family="Brinjal/Eggplant Dishes",
    specific_dish="Gutti Vankaya Kura",
    region="South India",
    state_or_city="Andhra Pradesh / Telangana",
    regional_names={"English": "Stuffed Brinjal", "Telugu": "గుత్తి వంకాయ కూర"},
    alternate_names=["gutti vankaya", "gutti vankaya kura", "andhra stuffed brinjal", "ennegayi andhra"],
    vegetarian=True,
    main_ingredient="brinjal",
    secondary_ingredients=["peanuts", "sesame", "coconut"],
    cooking_method="Simmered",
    consistency="Thick gravy",
    default_portion_grams=160.0,
    density_g_ml=1.12,
    nutrition_per_100g={"calories": 145.0, "protein_g": 3.8, "carbs_g": 9.5, "fat_g": 10.5, "fiber_g": 3.8, "sodium_mg": 340.0},
    uncertainty_factors=["peanut_sesame_paste_density", "oil_layer"],
    typical_oil_level="High visible oil"
), alias_ids=["IND_VEG_AP_GUTTI_VANKAYA", "gutti_vankaya"])

# 3.3 Andhra Bendakaya / Dondakaya Fry
register_veg_food_class(VegetarianFoodClassRecord(
    canonical_food_id="IND-VEG-AP-BENDAKAYA-FRY-001",
    canonical_name="Andhra Bendakaya Fry (Crispy Okra Fry)",
    hierarchy=VegetarianHierarchy(
        level3_region="South India",
        level4_state="Andhra Pradesh / Telangana",
        level5_food_family="Okra/Ladies Finger Dishes",
        level6_specific_dish="Bendakaya Fry",
        level7_variant="Crispy Fried Sliced Okra Mixed with Roasted Peanuts, Curry Leaves and Garlic Chilli Powder (Karam)",
        level8_main_ingredient="okra",
        level9_secondary_ingredients=["peanuts", "garlic", "chilli_powder", "curry_leaves"],
        level10_cooking_method="Deep-fried",
        level11_texture_consistency="Crispy",
        level12_portion_type="weight_grams",
        level13_weight_g_default=90.0,
        level14_nutrition_ref_id="ifct_bendakaya_fry"
    ),
    food_family="Okra/Ladies Finger Dishes",
    specific_dish="Bendakaya Fry",
    region="South India",
    state_or_city="Andhra Pradesh / Telangana",
    regional_names={"English": "Crispy Okra Fry", "Telugu": "బెండకాయ వేపుడు"},
    alternate_names=["bendakaya fry", "bendakaya vepudu", "andhra okra fry", "dondakaya fry", "crispy bhindi andhra"],
    vegetarian=True,
    main_ingredient="okra",
    secondary_ingredients=["peanuts", "garlic", "chilli"],
    cooking_method="Deep-fried",
    consistency="Crispy",
    default_portion_grams=90.0,
    density_g_ml=0.95,
    nutrition_per_100g={"calories": 165.0, "protein_g": 3.5, "carbs_g": 11.0, "fat_g": 12.0, "fiber_g": 4.0, "sodium_mg": 280.0},
    uncertainty_factors=["deep_fry_oil_retention", "peanut_weight"],
    typical_oil_level="High visible oil"
), alias_ids=["IND_VEG_AP_BENDAKAYA_FRY", "bendakaya_fry"])


# =============================================================================
# 4. NORTH INDIA (Section 9)
# =============================================================================

# 4.1 Aloo Gobi
register_veg_food_class(VegetarianFoodClassRecord(
    canonical_food_id="IND-VEG-NI-ALOO-GOBI-001",
    canonical_name="North Indian Aloo Gobi",
    hierarchy=VegetarianHierarchy(
        level3_region="North India",
        level4_state="Punjab / Delhi",
        level5_food_family="Cauliflower Dishes",
        level6_specific_dish="Aloo Gobi",
        level7_variant="Cauliflower Florets and Potato Wedges Sautéed with Cumin, Ginger, Turmeric and Garam Masala",
        level8_main_ingredient="cauliflower",
        level9_secondary_ingredients=["potato", "ginger", "cumin", "coriander"],
        level10_cooking_method="Pan-fried",
        level11_texture_consistency="Semi-dry",
        level12_portion_type="weight_grams",
        level13_weight_g_default=150.0,
        level14_nutrition_ref_id="ifct_aloo_gobi"
    ),
    food_family="Cauliflower Dishes",
    specific_dish="Aloo Gobi",
    region="North India",
    state_or_city="Punjab / Delhi / UP",
    regional_names={"English": "Aloo Gobi", "Hindi": "आलू गोभी", "Punjabi": "ਆਲੂ ਗੋਭੀ"},
    alternate_names=["aloo gobi", "alu gobi", "aloo gobhi", "spiced potato cauliflower"],
    vegetarian=True,
    main_ingredient="cauliflower",
    secondary_ingredients=["potato", "ginger", "cumin"],
    cooking_method="Pan-fried",
    consistency="Semi-dry",
    default_portion_grams=150.0,
    density_g_ml=1.04,
    nutrition_per_100g={"calories": 115.0, "protein_g": 2.8, "carbs_g": 15.5, "fat_g": 4.8, "fiber_g": 3.4, "sodium_mg": 240.0},
    uncertainty_factors=["potato_to_floret_ratio", "cooking_fat"],
    typical_oil_level="Moderate visible oil"
), alias_ids=["IND_VEG_NI_ALOO_GOBI", "aloo_gobi"])

# 4.2 Baingan Bharta
register_veg_food_class(VegetarianFoodClassRecord(
    canonical_food_id="IND-VEG-NI-BAINGAN-BHARTA-001",
    canonical_name="Punjabi Baingan Bharta",
    hierarchy=VegetarianHierarchy(
        level3_region="North India",
        level4_state="Punjab",
        level5_food_family="Brinjal/Eggplant Dishes",
        level6_specific_dish="Baingan Bharta",
        level7_variant="Charcoal-Roasted Eggplant Mashed and Sautéed with Onions, Tomatoes, Ginger and Green Chillies",
        level8_main_ingredient="brinjal",
        level9_secondary_ingredients=["onion", "tomato", "green_chilli", "mustard_oil"],
        level10_cooking_method="Roasted and mashed",
        level11_texture_consistency="Mashed",
        level12_portion_type="weight_grams",
        level13_weight_g_default=140.0,
        level14_nutrition_ref_id="ifct_baingan_bharta"
    ),
    food_family="Brinjal/Eggplant Dishes",
    specific_dish="Baingan Bharta",
    region="North India",
    state_or_city="Punjab",
    regional_names={"English": "Roasted Eggplant Mash", "Hindi": "बैंगन भर्ता", "Punjabi": "ਬੈਂਗਣ ਦਾ ਭੜਥਾ"},
    alternate_names=["baingan bharta", "baingan ka bharta", "eggplant mash", "roasted brinjal curry"],
    vegetarian=True,
    main_ingredient="brinjal",
    secondary_ingredients=["onion", "tomato", "ginger"],
    cooking_method="Roasted and mashed",
    consistency="Mashed",
    default_portion_grams=140.0,
    density_g_ml=1.06,
    nutrition_per_100g={"calories": 95.0, "protein_g": 2.1, "carbs_g": 8.0, "fat_g": 6.2, "fiber_g": 3.5, "sodium_mg": 250.0},
    uncertainty_factors=["mustard_oil_absorbed", "smoky_char_loss"],
    typical_oil_level="Moderate visible oil"
), alias_ids=["IND_VEG_NI_BAINGAN_BHARTA", "baingan_bharta"])

# 4.3 Bhindi Masala
register_veg_food_class(VegetarianFoodClassRecord(
    canonical_food_id="IND-VEG-NI-BHINDI-MASALA-001",
    canonical_name="North Indian Bhindi Masala",
    hierarchy=VegetarianHierarchy(
        level3_region="North India",
        level4_state="Delhi / UP",
        level5_food_family="Okra/Ladies Finger Dishes",
        level6_specific_dish="Bhindi Masala",
        level7_variant="Tender Cut Okra Sautéed with Sliced Onions, Cumin, Amchur and Garam Masala",
        level8_main_ingredient="okra",
        level9_secondary_ingredients=["onion", "amchur", "cumin", "coriander"],
        level10_cooking_method="Pan-fried",
        level11_texture_consistency="Semi-dry",
        level12_portion_type="weight_grams",
        level13_weight_g_default=130.0,
        level14_nutrition_ref_id="ifct_bhindi_masala"
    ),
    food_family="Okra/Ladies Finger Dishes",
    specific_dish="Bhindi Masala",
    region="North India",
    state_or_city="Delhi / UP / Punjab",
    regional_names={"English": "Bhindi Masala", "Hindi": "भिंडी मसाला"},
    alternate_names=["bhindi masala", "spiced okra", "bhindi do pyaza", "dahi bhindi"],
    vegetarian=True,
    main_ingredient="okra",
    secondary_ingredients=["onion", "amchur"],
    cooking_method="Pan-fried",
    consistency="Semi-dry",
    default_portion_grams=130.0,
    density_g_ml=1.02,
    nutrition_per_100g={"calories": 98.0, "protein_g": 2.4, "carbs_g": 9.2, "fat_g": 5.8, "fiber_g": 3.8, "sodium_mg": 230.0},
    uncertainty_factors=["oil_absorption_during_sauté"],
    typical_oil_level="Moderate visible oil"
), alias_ids=["IND_VEG_NI_BHINDI_MASALA", "bhindi_masala"])

# 4.4 Chana Masala / Punjabi Chole
register_veg_food_class(VegetarianFoodClassRecord(
    canonical_food_id="IND-VEG-NI-CHOLE-001",
    canonical_name="Punjabi Chana Masala (Chole)",
    hierarchy=VegetarianHierarchy(
        level3_region="North India",
        level4_state="Punjab / Delhi",
        level5_food_family="Chole",
        level6_specific_dish="Chana Masala",
        level7_variant="White Chickpeas Simmered in Onion, Tomato, Pomegranate Seeds (Anardana) and Chole Masala",
        level8_main_ingredient="chickpeas",
        level9_secondary_ingredients=["onion", "tomato", "anardana", "ginger"],
        level10_cooking_method="Simmered",
        level11_texture_consistency="Thick gravy",
        level12_portion_type="volume_ml",
        level13_weight_g_default=180.0,
        level14_nutrition_ref_id="ifct_chana_masala"
    ),
    food_family="Chole",
    specific_dish="Chana Masala",
    region="North India",
    state_or_city="Punjab / Delhi",
    regional_names={"English": "Chickpea Curry", "Hindi": "चना मसाला / छोले", "Punjabi": "ਛੋਲੇ"},
    alternate_names=["chole", "chana masala", "punjabi chole", "amritsari chole", "pindi chole"],
    vegetarian=True,
    main_ingredient="chickpeas",
    secondary_ingredients=["onion", "tomato", "anardana"],
    cooking_method="Simmered",
    consistency="Thick gravy",
    default_portion_grams=180.0,
    density_g_ml=1.12,
    nutrition_per_100g={"calories": 145.0, "protein_g": 7.5, "carbs_g": 19.5, "fat_g": 4.8, "fiber_g": 5.8, "sodium_mg": 380.0},
    uncertainty_factors=["gravy_thickness", "ghee_float"],
    typical_oil_level="Moderate visible oil"
), alias_ids=["IND_VEG_NI_CHOLE", "chana_masala"])

# 4.5 Rajma Masala
register_veg_food_class(VegetarianFoodClassRecord(
    canonical_food_id="IND-VEG-NI-RAJMA-001",
    canonical_name="Punjabi Rajma Masala",
    hierarchy=VegetarianHierarchy(
        level3_region="North India",
        level4_state="Punjab / Jammu",
        level5_food_family="Rajma",
        level6_specific_dish="Rajma Masala",
        level7_variant="Red Kidney Beans Slow-Simmered in Rich Spiced Onion-Tomato-Ginger Gravy",
        level8_main_ingredient="kidney_beans",
        level9_secondary_ingredients=["onion", "tomato", "ginger", "garam_masala"],
        level10_cooking_method="Slow simmered",
        level11_texture_consistency="Thick gravy",
        level12_portion_type="volume_ml",
        level13_weight_g_default=180.0,
        level14_nutrition_ref_id="ifct_rajma_masala"
    ),
    food_family="Rajma",
    specific_dish="Rajma Masala",
    region="North India",
    state_or_city="Punjab / Jammu & Kashmir",
    regional_names={"English": "Kidney Bean Curry", "Hindi": "राजमा मसाला", "Punjabi": "ਰਾਜਮਾਂਹ"},
    alternate_names=["rajma", "rajma masala", "punjabi rajma", "kashmiri rajma"],
    vegetarian=True,
    main_ingredient="kidney_beans",
    secondary_ingredients=["onion", "tomato", "ginger"],
    cooking_method="Slow simmered",
    consistency="Thick gravy",
    default_portion_grams=180.0,
    density_g_ml=1.12,
    nutrition_per_100g={"calories": 138.0, "protein_g": 7.2, "carbs_g": 18.2, "fat_g": 4.2, "fiber_g": 5.2, "sodium_mg": 360.0},
    uncertainty_factors=["slow_cook_reduction", "butter_addition"],
    typical_oil_level="Moderate visible oil"
), alias_ids=["IND_VEG_NI_RAJMA", "rajma_masala"])

# 4.6 Dum Aloo (Kashmiri / Punjabi)
register_veg_food_class(VegetarianFoodClassRecord(
    canonical_food_id="IND-VEG-NI-DUM-ALOO-001",
    canonical_name="Dum Aloo",
    hierarchy=VegetarianHierarchy(
        level3_region="North India",
        level4_state="Kashmir / Punjab",
        level5_food_family="Potato Dishes",
        level6_specific_dish="Dum Aloo",
        level7_variant="Fried Baby Potatoes Dum-Cooked in Spiced Fennel-Ginger Yogurt or Tomato Gravy",
        level8_main_ingredient="potato",
        level9_secondary_ingredients=["curd", "fennel", "dry_ginger", "kashmiri_chilli"],
        level10_cooking_method="Dum cooked",
        level11_texture_consistency="Thick gravy",
        level12_portion_type="weight_grams",
        level13_weight_g_default=160.0,
        level14_nutrition_ref_id="ifct_dum_aloo"
    ),
    food_family="Potato Dishes",
    specific_dish="Dum Aloo",
    region="North India",
    state_or_city="Kashmir / Punjab / Banaras",
    regional_names={"English": "Dum Aloo", "Hindi": "दम आलू", "Kashmiri": "دم اوول"},
    alternate_names=["dum aloo", "kashmiri dum aloo", "banarasi dum aloo", "baby potato curry"],
    vegetarian=True,
    main_ingredient="potato",
    secondary_ingredients=["curd", "fennel", "ginger"],
    cooking_method="Dum cooked",
    consistency="Thick gravy",
    default_portion_grams=160.0,
    density_g_ml=1.12,
    nutrition_per_100g={"calories": 155.0, "protein_g": 2.8, "carbs_g": 19.5, "fat_g": 7.2, "fiber_g": 2.8, "sodium_mg": 320.0},
    uncertainty_factors=["baby_potatoes_fried_oil_content", "curd_fat"],
    typical_oil_level="High visible oil"
), alias_ids=["IND_VEG_NI_DUM_ALOO", "dum_aloo"])

# 4.7 Malai Kofta
register_veg_food_class(VegetarianFoodClassRecord(
    canonical_food_id="IND-VEG-NI-MALAI-KOFTA-001",
    canonical_name="Shahi Malai Kofta",
    hierarchy=VegetarianHierarchy(
        level3_region="North India",
        level4_state="Delhi / Mughlai",
        level5_food_family="Vegetable Sabzi",
        level6_specific_dish="Malai Kofta",
        level7_variant="Fried Paneer and Potato Dumplings in Rich Creamy Cashew-Tomato Makhani Gravy",
        level8_main_ingredient="paneer",
        level9_secondary_ingredients=["potato", "cashew", "cream", "tomato", "raisins"],
        level10_cooking_method="Deep-fried and simmered",
        level11_texture_consistency="Creamy",
        level12_portion_type="weight_grams",
        level13_weight_g_default=180.0,
        level14_nutrition_ref_id="ifct_malai_kofta"
    ),
    food_family="Vegetable Sabzi",
    specific_dish="Malai Kofta",
    region="North India",
    state_or_city="Delhi / Punjab / Lucknow",
    regional_names={"English": "Malai Kofta", "Hindi": "मलाई कोफ्ता"},
    alternate_names=["malai kofta", "shahi malai kofta", "paneer kofta", "kofta curry"],
    vegetarian=True,
    main_ingredient="paneer",
    secondary_ingredients=["potato", "cashew", "cream"],
    cooking_method="Deep-fried and simmered",
    consistency="Creamy",
    is_countable=True,
    piece_count_expected=2,
    default_portion_grams=180.0,
    density_g_ml=1.15,
    nutrition_per_100g={"calories": 215.0, "protein_g": 6.5, "carbs_g": 15.0, "fat_g": 14.5, "fiber_g": 1.8, "sodium_mg": 390.0},
    uncertainty_factors=["fried_kofta_oil", "cream_cashew_density"],
    typical_oil_level="Ghee/butter visibly present"
), alias_ids=["IND_VEG_NI_MALAI_KOFTA", "malai_kofta"])


# =============================================================================
# 5. PANEER MASTER CLASSES (Section 13)
# =============================================================================

# 5.1 Paneer Butter Masala
register_veg_food_class(VegetarianFoodClassRecord(
    canonical_food_id="IND-VEG-PB-PAN-MASALA-001",
    canonical_name="Paneer Butter Masala",
    hierarchy=VegetarianHierarchy(
        level3_region="North India",
        level4_state="Punjab / Delhi",
        level5_food_family="Paneer Dishes",
        level6_specific_dish="Paneer Butter Masala",
        level7_variant="Fresh Cottage Cheese Cubes Simmered in Rich Silk Tomato-Cashew-Butter Sauce",
        level8_main_ingredient="paneer",
        level9_secondary_ingredients=["tomato", "butter", "cream", "cashew", "kasuri_methi"],
        level10_cooking_method="Simmered",
        level11_texture_consistency="Creamy",
        level12_portion_type="weight_grams",
        level13_weight_g_default=200.0,
        level14_nutrition_ref_id="ifct_paneer_butter_masala"
    ),
    food_family="Paneer Dishes",
    specific_dish="Paneer Butter Masala",
    region="North India",
    state_or_city="North India",
    regional_names={"English": "Paneer Butter Masala", "Hindi": "पनीर बटर मसाला", "Tamil": "பன்னீர் பட்டர் மசாலா"},
    alternate_names=["paneer butter masala", "paneer makhani", "butter paneer", "pbm"],
    vegetarian=True,
    main_ingredient="paneer",
    secondary_ingredients=["tomato", "butter", "cream"],
    cooking_method="Simmered",
    consistency="Creamy",
    is_countable=True,
    piece_count_expected=6,
    default_portion_grams=200.0,
    density_g_ml=1.14,
    nutrition_per_100g={"calories": 195.0, "protein_g": 7.5, "carbs_g": 8.5, "fat_g": 15.2, "fiber_g": 1.5, "sodium_mg": 390.0},
    uncertainty_factors=["butter_cream_excess", "cashew_paste_ratio"],
    typical_oil_level="Ghee/butter visibly present"
), alias_ids=["IND_VEG_PANEER_BUTTER_MASALA", "paneer_butter_masala"])

# 5.2 Kadai Paneer
register_veg_food_class(VegetarianFoodClassRecord(
    canonical_food_id="IND-VEG-NI-KADAI-PANEER-001",
    canonical_name="Kadai Paneer",
    hierarchy=VegetarianHierarchy(
        level3_region="North India",
        level4_state="Delhi / Punjab",
        level5_food_family="Paneer Dishes",
        level6_specific_dish="Kadai Paneer",
        level7_variant="Paneer Cubes and Bell Peppers Tossed with Freshly Roasted and Crushed Kadai Masala",
        level8_main_ingredient="paneer",
        level9_secondary_ingredients=["capsicum", "onion", "coriander_seeds", "dry_red_chillies"],
        level10_cooking_method="Wok-tossed",
        level11_texture_consistency="Semi-dry",
        level12_portion_type="weight_grams",
        level13_weight_g_default=180.0,
        level14_nutrition_ref_id="ifct_kadai_paneer"
    ),
    food_family="Paneer Dishes",
    specific_dish="Kadai Paneer",
    region="North India",
    state_or_city="North India",
    regional_names={"English": "Kadai Paneer", "Hindi": "कड़ाही पनीर"},
    alternate_names=["kadai paneer", "karahi paneer", "kadhai paneer"],
    vegetarian=True,
    main_ingredient="paneer",
    secondary_ingredients=["capsicum", "onion", "kadai_spices"],
    cooking_method="Wok-tossed",
    consistency="Semi-dry",
    is_countable=True,
    piece_count_expected=6,
    default_portion_grams=180.0,
    density_g_ml=1.12,
    nutrition_per_100g={"calories": 175.0, "protein_g": 8.2, "carbs_g": 7.5, "fat_g": 12.8, "fiber_g": 2.2, "sodium_mg": 360.0},
    uncertainty_factors=["tossing_oil_amount", "bell_pepper_ratio"],
    typical_oil_level="Moderate visible oil"
), alias_ids=["IND_VEG_KADAI_PANEER", "kadai_paneer"])

# 5.3 Palak Paneer
register_veg_food_class(VegetarianFoodClassRecord(
    canonical_food_id="IND-VEG-NI-PALAK-PANEER-001",
    canonical_name="Palak Paneer",
    hierarchy=VegetarianHierarchy(
        level3_region="North India",
        level4_state="Punjab",
        level5_food_family="Paneer Dishes",
        level6_specific_dish="Palak Paneer",
        level7_variant="Fresh Soft Paneer Cubes in Pureed Blanched Spinach Infused with Garlic and Cumin",
        level8_main_ingredient="paneer",
        level9_secondary_ingredients=["spinach", "garlic", "ginger", "cream"],
        level10_cooking_method="Blanched and simmered",
        level11_texture_consistency="Thick gravy",
        level12_portion_type="weight_grams",
        level13_weight_g_default=180.0,
        level14_nutrition_ref_id="ifct_palak_paneer"
    ),
    food_family="Paneer Dishes",
    specific_dish="Palak Paneer",
    region="North India",
    state_or_city="Punjab",
    regional_names={"English": "Spinach Paneer", "Hindi": "पालक पनीर", "Punjabi": "ਪਾਲਕ ਪਨੀਰ"},
    alternate_names=["palak paneer", "saag paneer", "spinach cottage cheese"],
    vegetarian=True,
    main_ingredient="paneer",
    secondary_ingredients=["spinach", "garlic"],
    cooking_method="Blanched and simmered",
    consistency="Thick gravy",
    is_countable=True,
    piece_count_expected=5,
    default_portion_grams=180.0,
    density_g_ml=1.10,
    nutrition_per_100g={"calories": 140.0, "protein_g": 7.8, "carbs_g": 5.2, "fat_g": 9.8, "fiber_g": 2.8, "sodium_mg": 320.0},
    uncertainty_factors=["added_butter_cream"],
    typical_oil_level="Moderate visible oil"
), alias_ids=["IND_VEG_PALAK_PANEER", "palak_paneer"])

# 5.4 Paneer Bhurji
register_veg_food_class(VegetarianFoodClassRecord(
    canonical_food_id="IND-VEG-NI-PANEER-BHURJI-001",
    canonical_name="Amritsari Paneer Bhurji",
    hierarchy=VegetarianHierarchy(
        level3_region="North India",
        level4_state="Punjab",
        level5_food_family="Paneer Dishes",
        level6_specific_dish="Paneer Bhurji",
        level7_variant="Crumbled Fresh Cottage Cheese Sautéed with Chopped Onions, Tomatoes, Green Chillies and Butter",
        level8_main_ingredient="paneer",
        level9_secondary_ingredients=["onion", "tomato", "green_chilli", "butter"],
        level10_cooking_method="Scrambled / Sautéed",
        level11_texture_consistency="Semi-dry",
        level12_portion_type="weight_grams",
        level13_weight_g_default=140.0,
        level14_nutrition_ref_id="ifct_paneer_bhurji"
    ),
    food_family="Paneer Dishes",
    specific_dish="Paneer Bhurji",
    region="North India",
    state_or_city="Punjab / Delhi",
    regional_names={"English": "Scrambled Paneer", "Hindi": "पनीर भुर्जी"},
    alternate_names=["paneer bhurji", "scrambled paneer", "bhurji paneer"],
    vegetarian=True,
    main_ingredient="paneer",
    secondary_ingredients=["onion", "tomato", "butter"],
    cooking_method="Scrambled / Sautéed",
    consistency="Semi-dry",
    default_portion_grams=140.0,
    density_g_ml=1.05,
    nutrition_per_100g={"calories": 185.0, "protein_g": 11.2, "carbs_g": 4.5, "fat_g": 13.8, "fiber_g": 1.2, "sodium_mg": 310.0},
    uncertainty_factors=["butter_quantity"],
    typical_oil_level="Moderate visible oil"
), alias_ids=["IND_VEG_PANEER_BHURJI", "paneer_bhurji"])


# =============================================================================
# 6. TOFU, SOY & MUSHROOM DATASETS (Sections 14, 15)
# =============================================================================

# 6.1 Tofu Stir-Fry / Curry
register_veg_food_class(VegetarianFoodClassRecord(
    canonical_food_id="IND-VEG-TOFU-CURRY-001",
    canonical_name="Spiced Tofu Masala",
    hierarchy=VegetarianHierarchy(
        level3_region="Pan-India",
        level4_state="Modern Indian",
        level5_food_family="Tofu Dishes",
        level6_specific_dish="Tofu Masala",
        level7_variant="Pan-Seared Soy Tofu Cubes Simmered in Onion-Tomato-Ginger Gravy",
        level8_main_ingredient="tofu",
        level9_secondary_ingredients=["onion", "tomato", "cumin", "garam_masala"],
        level10_cooking_method="Pan-seared and simmered",
        level11_texture_consistency="Semi-dry",
        level12_portion_type="weight_grams",
        level13_weight_g_default=150.0,
        level14_nutrition_ref_id="ifct_tofu_masala"
    ),
    food_family="Tofu Dishes",
    specific_dish="Tofu Masala",
    region="Pan-India",
    state_or_city="Pan-India",
    regional_names={"English": "Tofu Curry", "Hindi": "टोफू मसाला"},
    alternate_names=["tofu masala", "tofu curry", "tofu stir fry", "chilli tofu"],
    vegetarian=True,
    main_ingredient="tofu",
    secondary_ingredients=["onion", "tomato"],
    cooking_method="Pan-seared and simmered",
    consistency="Semi-dry",
    is_countable=True,
    piece_count_expected=6,
    default_portion_grams=150.0,
    density_g_ml=1.06,
    nutrition_per_100g={"calories": 110.0, "protein_g": 9.5, "carbs_g": 4.8, "fat_g": 6.2, "fiber_g": 2.0, "sodium_mg": 280.0},
    uncertainty_factors=["searing_oil"],
    typical_oil_level="Moderate visible oil"
), alias_ids=["IND_VEG_TOFU_MASALA", "tofu_curry"])

# 6.2 Soya Chunks Curry (Nutrela)
register_veg_food_class(VegetarianFoodClassRecord(
    canonical_food_id="IND-VEG-SOY-CURRY-001",
    canonical_name="Soya Chunks Masala Curry",
    hierarchy=VegetarianHierarchy(
        level3_region="Pan-India",
        level4_state="North / Pan-India",
        level5_food_family="Soy-Based Dishes",
        level6_specific_dish="Soya Chunks Curry",
        level7_variant="Rehydrated Textured Vegetable Protein (TVP) Chunks Simmered in Spiced Onion-Tomato Gravy",
        level8_main_ingredient="soya_chunks",
        level9_secondary_ingredients=["potato", "onion", "tomato", "ginger"],
        level10_cooking_method="Pressure cooked and simmered",
        level11_texture_consistency="Thick gravy",
        level12_portion_type="weight_grams",
        level13_weight_g_default=170.0,
        level14_nutrition_ref_id="ifct_soya_curry"
    ),
    food_family="Soy-Based Dishes",
    specific_dish="Soya Chunks Curry",
    region="Pan-India",
    state_or_city="Pan-India",
    regional_names={"English": "Soya Chunks Curry", "Hindi": "सोया चंक्स करी / न्यूट्रेला"},
    alternate_names=["soya chunks curry", "soya bean curry", "nutrela curry", "mealmaker curry", "soya sabzi"],
    vegetarian=True,
    main_ingredient="soya_chunks",
    secondary_ingredients=["potato", "onion", "tomato"],
    cooking_method="Simmered",
    consistency="Thick gravy",
    default_portion_grams=170.0,
    density_g_ml=1.08,
    nutrition_per_100g={"calories": 125.0, "protein_g": 12.5, "carbs_g": 10.0, "fat_g": 3.8, "fiber_g": 4.5, "sodium_mg": 310.0},
    uncertainty_factors=["hydration_level_of_chunks"],
    typical_oil_level="Moderate visible oil"
), alias_ids=["IND_VEG_SOYA_CURRY", "soya_chunks_curry"])

# 6.3 Mushroom Masala / Pepper Fry
register_veg_food_class(VegetarianFoodClassRecord(
    canonical_food_id="IND-VEG-MUSHROOM-MASALA-001",
    canonical_name="Button Mushroom Pepper Fry",
    hierarchy=VegetarianHierarchy(
        level3_region="Pan-India",
        level4_state="South / Pan-India",
        level5_food_family="Mushroom Dishes",
        level6_specific_dish="Mushroom Pepper Fry",
        level7_variant="Sliced White Button Mushrooms Sautéed with Crushed Black Pepper, Shallots and Curry Leaves",
        level8_main_ingredient="mushroom",
        level9_secondary_ingredients=["black_pepper", "shallots", "curry_leaves", "fennel"],
        level10_cooking_method="Stir-fried",
        level11_texture_consistency="Semi-dry",
        level12_portion_type="weight_grams",
        level13_weight_g_default=130.0,
        level14_nutrition_ref_id="ifct_mushroom_pepper_fry"
    ),
    food_family="Mushroom Dishes",
    specific_dish="Mushroom Pepper Fry",
    region="Pan-India",
    state_or_city="Tamil Nadu / Kerala / Pan-India",
    regional_names={"English": "Mushroom Pepper Fry", "Tamil": "காளான் மிளகு வறுவல்", "Hindi": "मशरूम मसाला"},
    alternate_names=["mushroom pepper fry", "mushroom masala", "kalan varuval", "mushroom curry", "mushroom roast"],
    vegetarian=True,
    main_ingredient="mushroom",
    secondary_ingredients=["black_pepper", "shallots"],
    cooking_method="Stir-fried",
    consistency="Semi-dry",
    default_portion_grams=130.0,
    density_g_ml=0.98,
    nutrition_per_100g={"calories": 78.0, "protein_g": 3.8, "carbs_g": 5.2, "fat_g": 4.8, "fiber_g": 2.2, "sodium_mg": 240.0},
    uncertainty_factors=["mushroom_water_shrinkage"],
    typical_oil_level="Moderate visible oil"
), alias_ids=["IND_VEG_MUSHROOM_MASALA", "mushroom_pepper_fry"])


# =============================================================================
# 7. WEST & EAST INDIA SPECIALTIES (Sections 10, 11)
# =============================================================================

# 7.1 Gujarati Undhiyu
register_veg_food_class(VegetarianFoodClassRecord(
    canonical_food_id="IND-VEG-GJ-UNDHIYU-001",
    canonical_name="Surti Undhiyu",
    hierarchy=VegetarianHierarchy(
        level3_region="West India",
        level4_state="Gujarat",
        level5_food_family="Regional Vegetarian Specialties",
        level6_specific_dish="Undhiyu",
        level7_variant="Winter Mixed Vegetables (Surti Papdi, Sweet Potato, Yam, Baby Brinjal, Methi Muthiya) Slow-Cooked with Coconut, Peanuts and Sesame",
        level8_main_ingredient="mixed_winter_vegetables",
        level9_secondary_ingredients=["surti_papdi", "methi_muthiya", "peanuts", "sesame", "coconut", "green_garlic"],
        level10_cooking_method="Slow cooked / Baked in pot",
        level11_texture_consistency="Semi-dry",
        level12_portion_type="weight_grams",
        level13_weight_g_default=160.0,
        level14_nutrition_ref_id="ifct_surti_undhiyu"
    ),
    food_family="Regional Vegetarian Specialties",
    specific_dish="Undhiyu",
    region="West India",
    state_or_city="Gujarat / Surat",
    regional_names={"English": "Undhiyu", "Gujarati": "ઉંધિયું"},
    alternate_names=["undhiyu", "surti undhiyu", "kathiyawadi undhiyu", "gujarati undhiyu"],
    vegetarian=True,
    main_ingredient="mixed_winter_vegetables",
    secondary_ingredients=["methi_muthiya", "peanuts", "sesame", "green_garlic"],
    cooking_method="Slow cooked",
    consistency="Semi-dry",
    default_portion_grams=160.0,
    density_g_ml=1.06,
    nutrition_per_100g={"calories": 165.0, "protein_g": 4.5, "carbs_g": 18.0, "fat_g": 8.5, "fiber_g": 4.8, "sodium_mg": 280.0},
    uncertainty_factors=["fried_muthiya_ratio", "sesame_peanut_oil"],
    typical_oil_level="Moderate visible oil"
), alias_ids=["IND_VEG_GJ_UNDHIYU", "undhiyu"])

# 7.2 Maharashtrian Zunka / Pithla
register_veg_food_class(VegetarianFoodClassRecord(
    canonical_food_id="IND-VEG-MH-ZUNKA-001",
    canonical_name="Maharashtrian Zunka / Pithla",
    hierarchy=VegetarianHierarchy(
        level3_region="West India",
        level4_state="Maharashtra",
        level5_food_family="Regional Vegetarian Specialties",
        level6_specific_dish="Zunka",
        level7_variant="Gram Flour (Besan) Sautéed Dry with Mustard, Hing, Curry Leaves, Garlic and Chillies",
        level8_main_ingredient="gram_flour",
        level9_secondary_ingredients=["onion", "garlic", "green_chilli", "mustard"],
        level10_cooking_method="Pan-sautéed",
        level11_texture_consistency="Semi-dry",
        level12_portion_type="weight_grams",
        level13_weight_g_default=120.0,
        level14_nutrition_ref_id="ifct_zunka_pithla"
    ),
    food_family="Regional Vegetarian Specialties",
    specific_dish="Zunka",
    region="West India",
    state_or_city="Maharashtra",
    regional_names={"English": "Zunka", "Marathi": "झुborderका / पिठलं"},
    alternate_names=["zunka", "jhonka", "pithla", "pitla", "zunka bhakri"],
    vegetarian=True,
    main_ingredient="gram_flour",
    secondary_ingredients=["onion", "garlic", "green_chilli"],
    cooking_method="Pan-sautéed",
    consistency="Semi-dry",
    default_portion_grams=120.0,
    density_g_ml=1.02,
    nutrition_per_100g={"calories": 140.0, "protein_g": 6.8, "carbs_g": 14.5, "fat_g": 6.5, "fiber_g": 3.0, "sodium_mg": 290.0},
    uncertainty_factors=["besan_density", "oil_used_for_roasting"],
    typical_oil_level="Moderate visible oil"
), alias_ids=["IND_VEG_MH_ZUNKA", "zunka", "pithla"])

# 7.3 Bengal Aloo Posto
register_veg_food_class(VegetarianFoodClassRecord(
    canonical_food_id="IND-VEG-WB-ALOOPOSTO-001",
    canonical_name="Bengali Aloo Posto",
    hierarchy=VegetarianHierarchy(
        level3_region="East India",
        level4_state="West Bengal",
        level5_food_family="Potato Dishes",
        level6_specific_dish="Aloo Posto",
        level7_variant="Diced Potatoes Stewed in Ground Poppy Seed Paste and Slit Green Chillies in Mustard Oil",
        level8_main_ingredient="potato",
        level9_secondary_ingredients=["poppy_seeds", "mustard_oil", "green_chilli", "kalonji"],
        level10_cooking_method="Simmered",
        level11_texture_consistency="Semi-dry",
        level12_portion_type="weight_grams",
        level13_weight_g_default=140.0,
        level14_nutrition_ref_id="ifct_aloo_posto"
    ),
    food_family="Potato Dishes",
    specific_dish="Aloo Posto",
    region="East India",
    state_or_city="West Bengal",
    regional_names={"English": "Aloo Posto", "Bengali": "আলু পোস্ত"},
    alternate_names=["aloo posto", "alu posto", "potato with poppy seeds", "posto aloo"],
    vegetarian=True,
    main_ingredient="potato",
    secondary_ingredients=["poppy_seeds", "mustard_oil"],
    cooking_method="Simmered",
    consistency="Semi-dry",
    default_portion_grams=140.0,
    density_g_ml=1.08,
    nutrition_per_100g={"calories": 160.0, "protein_g": 3.8, "carbs_g": 17.5, "fat_g": 8.5, "fiber_g": 3.0, "sodium_mg": 210.0},
    uncertainty_factors=["poppy_seed_paste_density", "raw_mustard_oil_finish"],
    typical_oil_level="Moderate visible oil"
), alias_ids=["IND_VEG_WB_ALOO_POSTO", "aloo_posto"])

# 7.4 Odisha Dalma
register_veg_food_class(VegetarianFoodClassRecord(
    canonical_food_id="IND-VEG-OD-DALMA-001",
    canonical_name="Odia Temple Dalma",
    hierarchy=VegetarianHierarchy(
        level3_region="East India",
        level4_state="Odisha",
        level5_food_family="Lentil-Based Vegetarian Dishes",
        level6_specific_dish="Dalma",
        level7_variant="Toor Dal Boiled with Raw Papaya, Pumpkin, Raw Banana, Brinjal, Tempered with Panch Phoron, Ghee and Roasted Cumin-Chilli Powder",
        level8_main_ingredient="toor_dal",
        level9_secondary_ingredients=["raw_papaya", "pumpkin", "raw_banana", "panch_phoron", "roasted_cumin", "ghee"],
        level10_cooking_method="Boiled and tempered",
        level11_texture_consistency="Thick gravy",
        level12_portion_type="volume_ml",
        level13_weight_g_default=160.0,
        level14_nutrition_ref_id="ifct_odia_dalma"
    ),
    food_family="Lentil-Based Vegetarian Dishes",
    specific_dish="Dalma",
    region="East India",
    state_or_city="Odisha / Puri",
    regional_names={"English": "Dalma", "Odia": "ଡାଲମା"},
    alternate_names=["dalma", "odia dalma", "puri temple dalma", "dalma lentil stew"],
    vegetarian=True,
    main_ingredient="toor_dal",
    secondary_ingredients=["raw_papaya", "pumpkin", "panch_phoron", "ghee"],
    cooking_method="Boiled and tempered",
    consistency="Thick gravy",
    default_portion_grams=160.0,
    density_g_ml=1.09,
    nutrition_per_100g={"calories": 92.0, "protein_g": 4.5, "carbs_g": 13.5, "fat_g": 2.5, "fiber_g": 3.8, "sodium_mg": 240.0},
    uncertainty_factors=["vegetable_to_dal_ratio", "ghee_tadka"],
    typical_oil_level="Tempering visible"
), alias_ids=["IND_VEG_OD_DALMA", "dalma"])

# 7.5 Bihar / Jharkhand Baingan & Aloo Chokha
register_veg_food_class(VegetarianFoodClassRecord(
    canonical_food_id="IND-VEG-BR-CHOKHA-001",
    canonical_name="Bihari Baingan Aloo Chokha",
    hierarchy=VegetarianHierarchy(
        level3_region="East India",
        level4_state="Bihar / Jharkhand",
        level5_food_family="Regional Vegetarian Specialties",
        level6_specific_dish="Chokha",
        level7_variant="Fire-Roasted Eggplant and Boiled Potatoes Coarsely Mashed with Raw Mustard Oil, Green Chillies, Garlic and Onions",
        level8_main_ingredient="brinjal",
        level9_secondary_ingredients=["potato", "mustard_oil", "garlic", "green_chilli"],
        level10_cooking_method="Roasted and mashed",
        level11_texture_consistency="Mashed",
        level12_portion_type="weight_grams",
        level13_weight_g_default=120.0,
        level14_nutrition_ref_id="ifct_bihari_chokha"
    ),
    food_family="Regional Vegetarian Specialties",
    specific_dish="Chokha",
    region="East India",
    state_or_city="Bihar / Jharkhand",
    regional_names={"English": "Chokha", "Hindi": "चोखा (बैंगन / आलू)"},
    alternate_names=["chokha", "baingan chokha", "aloo chokha", "litti chokha accompaniment"],
    vegetarian=True,
    main_ingredient="brinjal",
    secondary_ingredients=["potato", "mustard_oil", "garlic"],
    cooking_method="Roasted and mashed",
    consistency="Mashed",
    default_portion_grams=120.0,
    density_g_ml=1.05,
    nutrition_per_100g={"calories": 88.0, "protein_g": 2.0, "carbs_g": 11.5, "fat_g": 4.0, "fiber_g": 2.8, "sodium_mg": 210.0},
    uncertainty_factors=["raw_mustard_oil_quantity"],
    typical_oil_level="Low visible oil"
), alias_ids=["IND_VEG_BR_CHOKHA", "chokha"])


# =============================================================================
# 8. JACKFRUIT & STUFFED VEGETABLE DATASETS (Sections 21, 26)
# =============================================================================

# 8.1 Kathal (Raw Jackfruit) Curry
register_veg_food_class(VegetarianFoodClassRecord(
    canonical_food_id="IND-VEG-JACKFRUIT-KATHAL-001",
    canonical_name="Raw Jackfruit Masala Curry (Kathal Sabzi)",
    hierarchy=VegetarianHierarchy(
        level3_region="Pan-India",
        level4_state="North / East / South India",
        level5_food_family="Jackfruit Dishes",
        level6_specific_dish="Kathal Curry",
        level7_variant="Fibrous Raw Jackfruit Chunks Deep/Shallow Fried and Simmered in Hearty Onion, Garlic, Tomato and Garam Masala Gravy",
        level8_main_ingredient="raw_jackfruit",
        level9_secondary_ingredients=["onion", "garlic", "tomato", "mustard_oil", "garam_masala"],
        level10_cooking_method="Fried and simmered",
        level11_texture_consistency="Thick gravy",
        level12_portion_type="weight_grams",
        level13_weight_g_default=160.0,
        level14_nutrition_ref_id="ifct_kathal_curry"
    ),
    food_family="Jackfruit Dishes",
    specific_dish="Kathal Curry",
    region="Pan-India",
    state_or_city="UP / Bihar / Bengal / Kerala",
    regional_names={"English": "Raw Jackfruit Curry", "Hindi": "कटहल की सब्जी", "Bengali": "এঁচোড়ের ডালনা", "Malayalam": "ചക്കക്കറി"},
    alternate_names=["kathal curry", "kathal sabzi", "jackfruit curry", "raw jackfruit masala", "enchor dalna", "chakka curry"],
    vegetarian=True,
    main_ingredient="raw_jackfruit",
    secondary_ingredients=["onion", "garlic", "tomato"],
    cooking_method="Fried and simmered",
    consistency="Thick gravy",
    default_portion_grams=160.0,
    density_g_ml=1.08,
    nutrition_per_100g={"calories": 135.0, "protein_g": 3.2, "carbs_g": 18.0, "fat_g": 5.8, "fiber_g": 4.5, "sodium_mg": 310.0},
    uncertainty_factors=["pre_fry_oil_absorption", "carpels_fibrous_texture"],
    typical_oil_level="Moderate visible oil"
), alias_ids=["IND_VEG_KATHAL_CURRY", "kathal_curry", "jackfruit_curry"])

# 8.2 Bharwa Shimla Mirch (Stuffed Capsicum)
register_veg_food_class(VegetarianFoodClassRecord(
    canonical_food_id="IND-VEG-STUFFED-CAPSICUM-001",
    canonical_name="Bharwa Shimla Mirch (Stuffed Capsicum)",
    hierarchy=VegetarianHierarchy(
        level3_region="North India",
        level4_state="Punjab / UP",
        level5_food_family="Stuffed Vegetables",
        level6_specific_dish="Bharwa Shimla Mirch",
        level7_variant="Hollowed Whole Bell Peppers Stuffed with Spiced Mashed Potato, Paneer, Peanuts and Pan-Roasted",
        level8_main_ingredient="capsicum",
        level9_secondary_ingredients=["potato", "paneer", "peanuts", "amchur", "cumin"],
        level10_cooking_method="Pan-roasted",
        level11_texture_consistency="Soft",
        level12_portion_type="piece_count",
        level13_weight_g_default=140.0,
        level14_nutrition_ref_id="ifct_stuffed_capsicum"
    ),
    food_family="Stuffed Vegetables",
    specific_dish="Bharwa Shimla Mirch",
    region="North India",
    state_or_city="North India",
    regional_names={"English": "Stuffed Bell Pepper", "Hindi": "भरवा शिमला मिर्च"},
    alternate_names=["bharwa shimla mirch", "stuffed capsicum", "bharwa mirch", "stuffed bell pepper"],
    vegetarian=True,
    main_ingredient="capsicum",
    secondary_ingredients=["potato", "paneer", "peanuts"],
    cooking_method="Pan-roasted",
    consistency="Soft",
    is_countable=True,
    piece_count_expected=2,
    default_portion_grams=140.0,
    density_g_ml=1.02,
    nutrition_per_100g={"calories": 120.0, "protein_g": 3.0, "carbs_g": 14.5, "fat_g": 5.8, "fiber_g": 2.8, "sodium_mg": 270.0},
    uncertainty_factors=["stuffing_potato_vs_paneer_ratio"],
    typical_oil_level="Moderate visible oil"
), alias_ids=["IND_VEG_STUFFED_CAPSICUM", "bharwa_shimla_mirch"])


# =============================================================================
# 9. FALLBACK UNCERTAINTY CLASSES (Sections 49, 75, 76)
# =============================================================================

# 9.1 Overall Unknown Vegetarian Dish
register_veg_food_class(VegetarianFoodClassRecord(
    canonical_food_id="IND-VEG-UNKNOWN-001",
    canonical_name="Indian vegetarian dish — exact identity uncertain",
    hierarchy=VegetarianHierarchy(
        level3_region="Pan-India",
        level4_state="Unknown",
        level5_food_family="Regional Vegetarian Specialties",
        level6_specific_dish="Unknown Vegetarian Dish",
        level7_variant="Unverified Indian vegetarian preparation due to insufficient visual cues",
        level8_main_ingredient="unknown",
        level9_secondary_ingredients=[],
        level10_cooking_method="Unknown",
        level11_texture_consistency="Mixed",
        level12_portion_type="weight_grams",
        level13_weight_g_default=140.0,
        level14_nutrition_ref_id="ifct_veg_unknown"
    ),
    food_family="Regional Vegetarian Specialties",
    specific_dish="Unknown Vegetarian Dish",
    region="Pan-India",
    state_or_city="Unknown",
    regional_names={"English": "Indian Vegetarian Dish", "Hindi": "अज्ञात भारतीय शाकाहारी व्यंजन"},
    alternate_names=["unknown vegetarian dish", "unverified veg dish", "veg dish uncertain"],
    vegetarian=True,
    main_ingredient="unknown",
    cooking_method="Unknown",
    consistency="Mixed",
    default_portion_grams=140.0,
    density_g_ml=1.05,
    nutrition_per_100g={"calories": 110.0, "protein_g": 3.0, "carbs_g": 12.0, "fat_g": 5.5, "fiber_g": 2.5, "sodium_mg": 280.0},
    uncertainty_factors=["insufficient_visual_evidence", "unknown_recipe_composition"],
    typical_oil_level="Moderate visible oil"
), alias_ids=["IND_VEG_UNKNOWN", "unknown_vegetarian"])

# 9.2 Vegetable Curry Unknown
register_veg_food_class(VegetarianFoodClassRecord(
    canonical_food_id="IND-VEG-CURRY-UNKNOWN-001",
    canonical_name="Vegetable curry — exact type uncertain",
    hierarchy=VegetarianHierarchy(
        level3_region="Pan-India",
        level4_state="Unknown",
        level5_food_family="Vegetable Curry",
        level6_specific_dish="Unknown Vegetable Curry",
        level7_variant="Simmered vegetable preparation with unidentified vegetable mix and gravy base",
        level8_main_ingredient="mixed_vegetables",
        level9_secondary_ingredients=[],
        level10_cooking_method="Simmered",
        level11_texture_consistency="Thick gravy",
        level12_portion_type="volume_ml",
        level13_weight_g_default=150.0,
        level14_nutrition_ref_id="ifct_curry_unknown"
    ),
    food_family="Vegetable Curry",
    specific_dish="Unknown Vegetable Curry",
    region="Pan-India",
    state_or_city="Unknown",
    regional_names={"English": "Vegetable Curry", "Hindi": "सब्जी करी (अज्ञात)"},
    alternate_names=["vegetable curry uncertain", "unknown veg curry", "unidentified vegetable curry"],
    vegetarian=True,
    main_ingredient="mixed_vegetables",
    cooking_method="Simmered",
    consistency="Thick gravy",
    default_portion_grams=150.0,
    density_g_ml=1.08,
    nutrition_per_100g={"calories": 105.0, "protein_g": 2.8, "carbs_g": 11.5, "fat_g": 5.2, "fiber_g": 2.8, "sodium_mg": 300.0},
    uncertainty_factors=["partial_vegetables_visible", "recipe_variation"],
    typical_oil_level="Moderate visible oil"
), alias_ids=["IND_VEG_CURRY_UNKNOWN", "veg_curry_uncertain"])

# 9.3 Paneer Dish Unknown
register_veg_food_class(VegetarianFoodClassRecord(
    canonical_food_id="IND-VEG-PANEER-UNKNOWN-001",
    canonical_name="Paneer-based dish — exact recipe uncertain",
    hierarchy=VegetarianHierarchy(
        level3_region="North India",
        level4_state="Unknown",
        level5_food_family="Paneer Dishes",
        level6_specific_dish="Unknown Paneer Dish",
        level7_variant="Verified paneer cubes in unconfirmed gravy or spice blend",
        level8_main_ingredient="paneer",
        level9_secondary_ingredients=[],
        level10_cooking_method="Simmered",
        level11_texture_consistency="Creamy",
        level12_portion_type="weight_grams",
        level13_weight_g_default=180.0,
        level14_nutrition_ref_id="ifct_paneer_unknown"
    ),
    food_family="Paneer Dishes",
    specific_dish="Unknown Paneer Dish",
    region="North India",
    state_or_city="North India",
    regional_names={"English": "Paneer Dish", "Hindi": "पनीर व्यंजन (अज्ञात)"},
    alternate_names=["paneer dish uncertain", "unknown paneer curry", "unverified paneer gravy"],
    vegetarian=True,
    main_ingredient="paneer",
    cooking_method="Simmered",
    consistency="Creamy",
    is_countable=True,
    piece_count_expected=5,
    default_portion_grams=180.0,
    density_g_ml=1.12,
    nutrition_per_100g={"calories": 170.0, "protein_g": 7.8, "carbs_g": 7.0, "fat_g": 12.5, "fiber_g": 1.6, "sodium_mg": 340.0},
    uncertainty_factors=["gravy_butter_cream_ratio_uncertain"],
    typical_oil_level="Moderate visible oil"
), alias_ids=["IND_VEG_PANEER_UNKNOWN", "paneer_unknown"])


# =============================================================================
# LOOKUP & HELPER UTILITIES
# =============================================================================

def get_veg_food_class(canonical_id: str) -> Optional[VegetarianFoodClassRecord]:
    """Retrieve record by canonical ID."""
    return VEGETARIAN_TAXONOMY_REGISTRY.get(canonical_id) or VEGETARIAN_TAXONOMY_REGISTRY.get(canonical_id.lower())


def resolve_veg_food_by_name(query: str) -> Optional[VegetarianFoodClassRecord]:
    """
    Resolves any query string (canonical name, English alias, regional script)
    into the canonical VegetarianFoodClassRecord. Returns None if unmapped.
    """
    if not query:
        return None
    q = query.lower().strip()
    if q in VEGETARIAN_SYNONYM_LOOKUP:
        return VEGETARIAN_TAXONOMY_REGISTRY.get(VEGETARIAN_SYNONYM_LOOKUP[q])
    for alt, cid in VEGETARIAN_SYNONYM_LOOKUP.items():
        if alt in q or q in alt:
            return VEGETARIAN_TAXONOMY_REGISTRY.get(cid)
    return None


def filter_veg_by_family(food_family: str) -> List[VegetarianFoodClassRecord]:
    """Returns all registered vegetarian classes in a given family."""
    fam = food_family.lower().strip()
    return [
        rec for rec in VEGETARIAN_TAXONOMY_REGISTRY.values()
        if rec.food_family.lower() == fam or fam in rec.hierarchy.level5_food_family.lower()
    ]
