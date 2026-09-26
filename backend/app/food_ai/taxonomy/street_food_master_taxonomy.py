"""
Indian Street Food Master Taxonomy & Identity Hierarchy (Part 8)
Implements Sections 0-3, 6-33, 37, 40-55, 60, 63, 66-74, 91, 93 of Part 8 Master Training Specification.

Guarantees:
- Strict Hierarchical Identity Traversal:
  Indian Food -> Indian Street Food -> Master Food Family (18 families) ->
  Sub-Family / Canonical Food -> Regional Variant -> Ingredients -> Cooking Method -> Portion -> Nutrition
- 18 Master Street Food Families:
  1. Chaat
  2. Fried Snacks
  3. Tiffin / Quick Meals
  4. Street Breads
  5. Rolls / Wraps
  6. Sandwiches
  7. Pav-Based Foods
  8. Rice-Based Street Foods
  9. Noodles / Indo-Chinese
  10. Momos / Dumplings
  11. South Indian Street Food
  12. North Indian Street Food
  13. West Indian Street Food
  14. East Indian Street Food
  15. Northeast Indian Street Food
  16. Sweets
  17. Beverages
  18. Regional Specialities
- Permanent Canonical IDs:
  CHAAT_*, FRIED_*, PAV_*, ROLL_*, SANDWICH_*, INDOCHINESE_*, MOMO_*,
  SOUTH_STREET_*, NORTH_STREET_*, WEST_STREET_*, EAST_STREET_*, NE_STREET_*,
  FUSION_STREET_*, SWEET_STREET_*, BEV_STREET_*, and STREET_UNKNOWN.
- Multilingual mappings: Hindi, Marathi, Bengali, Tamil, Telugu, Gujarati, Punjabi, etc.
- Component breakdown: base, toppings, sauces, cooking methods, portion types, and calorie uncertainty factors.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class StreetFoodHierarchy(BaseModel):
    level1_food: str = "Indian Food"
    level2_macro_category: str = "Indian Street Food"
    level3_food_family: str  # Chaat, Fried Snacks, Pav-Based Foods, Rolls / Wraps, etc.
    level4_sub_family: str   # Pani Puri, Samosa, Vada Pav, Kathi Roll, Hakka Noodles, etc.
    level5_canonical_food: str
    level6_variant: str      # e.g., "Mumbai Ragda Style", "Delhi Boiled Aloo Style", "Kolkata Gondhoraj Style"
    level7_cooking_method: List[str]  # Deep Fried, Shallow Fried, Pan Fried, Steamed, Boiled, Roasted, Baked, Assembled
    level8_portion_type: str  # piece_count, unit_weight_g, bowl_weight_g, volume_ml
    level9_nutrition_ref_id: str


class StreetFoodClassRecord(BaseModel):
    canonical_food_id: str
    canonical_name: str
    hierarchy: StreetFoodHierarchy
    food_family: str
    sub_family: str
    region: str              # West India, North India, East India, South India, Northeast India, Pan-India
    state_or_city: str       # Maharashtra / Mumbai, Delhi, West Bengal / Kolkata, etc.
    regional_names: Dict[str, str] = Field(default_factory=dict)
    alternate_names: List[str] = Field(default_factory=list)
    vegetarian: bool = True
    base_components: List[str] = Field(default_factory=list)
    toppings: List[str] = Field(default_factory=list)
    sauces_and_chutneys: List[str] = Field(default_factory=list)
    cooking_methods: List[str] = Field(default_factory=list)
    default_portion_unit: str = "piece"  # "piece", "plate", "bowl", "cup", "wrap"
    default_unit_mass_g: float = 100.0
    density_g_cm3: float = 0.85
    nutrition_per_100g: Dict[str, float] = Field(default_factory=dict)
    uncertainty_factors: List[str] = Field(default_factory=list)
    oil_level_typical: str = "Medium"  # Low, Medium, High, Unknown


STREET_FOOD_TAXONOMY_REGISTRY: Dict[str, StreetFoodClassRecord] = {}
STREET_SYNONYM_LOOKUP: Dict[str, str] = {}


def register_street_food_class(record: StreetFoodClassRecord) -> StreetFoodClassRecord:
    STREET_FOOD_TAXONOMY_REGISTRY[record.canonical_food_id] = record
    STREET_SYNONYM_LOOKUP[record.canonical_name.lower().strip()] = record.canonical_food_id
    for alt in record.alternate_names:
        STREET_SYNONYM_LOOKUP[alt.lower().strip()] = record.canonical_food_id
    for reg_name in record.regional_names.values():
        STREET_SYNONYM_LOOKUP[reg_name.lower().strip()] = record.canonical_food_id
    return record


# =============================================================================
# 1. CHAAT MASTER DATASET (Sections 2 - 14)
# =============================================================================

# 1.1 Pani Puri / Golgappa / Puchka (Sections 2, 3, 4, 5)
register_street_food_class(StreetFoodClassRecord(
    canonical_food_id="CHAAT_PANI_PURI_MUMBAI",
    canonical_name="Mumbai Pani Puri",
    hierarchy=StreetFoodHierarchy(
        level3_food_family="Chaat",
        level4_sub_family="Pani Puri",
        level5_canonical_food="Pani Puri",
        level6_variant="Mumbai Warm Ragda & Spicy Mint-Coriander Water",
        level7_cooking_method=["Deep Fried (Puri)", "Boiled (Ragda)", "Assembled"],
        level8_portion_type="piece_count",
        level9_nutrition_ref_id="ifct_chaat_pani_puri_mumbai"
    ),
    food_family="Chaat",
    sub_family="Pani Puri",
    region="West India",
    state_or_city="Maharashtra / Mumbai",
    regional_names={"English": "Mumbai Pani Puri", "Hindi": "पानी पूरी", "Marathi": "पाणीपुरी", "Gujarati": "પાણીપુરી"},
    alternate_names=["pani puri", "bombay pani puri", "mumbai golgappa", "ragda pani puri"],
    vegetarian=True,
    base_components=["crispy suji/semolina puri", "warm ragda (white peas)", "chilled spiced mint-coriander water"],
    toppings=["sweet tamarind-date chutney", "fine nylon sev", "chopped raw onion", "boondi"],
    sauces_and_chutneys=["teekha green pani", "meetha tamarind chutney"],
    cooking_methods=["Deep Fried", "Boiled", "Assembled"],
    default_portion_unit="piece",
    default_unit_mass_g=28.0,
    density_g_cm3=0.82,
    nutrition_per_100g={"calories": 165.0, "protein_g": 3.8, "carbs_g": 30.5, "fat_g": 3.2, "fiber_g": 2.4, "sodium_mg": 380.0},
    uncertainty_factors=["puri_count", "ragda_vs_potato_ratio", "meetha_chutney_sugar_level", "water_volume"],
    oil_level_typical="Medium"
))

register_street_food_class(StreetFoodClassRecord(
    canonical_food_id="CHAAT_GOLGAPPA_DELHI",
    canonical_name="Delhi Golgappa",
    hierarchy=StreetFoodHierarchy(
        level3_food_family="Chaat",
        level4_sub_family="Pani Puri",
        level5_canonical_food="Golgappa",
        level6_variant="Delhi Spiced Boiled Potato & Boondi with Heeng-Jeera Water",
        level7_cooking_method=["Deep Fried (Puri)", "Boiled (Potato/Chickpea)", "Assembled"],
        level8_portion_type="piece_count",
        level9_nutrition_ref_id="ifct_chaat_golgappa_delhi"
    ),
    food_family="Chaat",
    sub_family="Pani Puri",
    region="North India",
    state_or_city="Delhi / NCR",
    regional_names={"English": "Delhi Golgappa", "Hindi": "गोलगप्पा", "Punjabi": "ਗੋਲਗੱਪੇ"},
    alternate_names=["golgappa", "gol gappa", "delhi pani puri", "ata golgappa", "sooji golgappa"],
    vegetarian=True,
    base_components=["crispy whole wheat / semolina puri", "mashed spiced boiled potato", "black chickpeas", "boondi"],
    toppings=["saunth (sweet dry ginger chutney)", "black salt masala", "roasted cumin"],
    sauces_and_chutneys=["heeng-jeera pudina pani", "sweet sonth chutney"],
    cooking_methods=["Deep Fried", "Boiled", "Assembled"],
    default_portion_unit="piece",
    default_unit_mass_g=30.0,
    density_g_cm3=0.84,
    nutrition_per_100g={"calories": 158.0, "protein_g": 3.4, "carbs_g": 29.8, "fat_g": 3.0, "fiber_g": 2.2, "sodium_mg": 410.0},
    uncertainty_factors=["puri_thickness", "potato_filling_volume", "saunth_sugar_content"],
    oil_level_typical="Medium"
))

register_street_food_class(StreetFoodClassRecord(
    canonical_food_id="CHAAT_PUCHKA_KOLKATA",
    canonical_name="Kolkata Puchka",
    hierarchy=StreetFoodHierarchy(
        level3_food_family="Chaat",
        level4_sub_family="Pani Puri",
        level5_canonical_food="Puchka",
        level6_variant="Kolkata Spicy Mashed Potato with Gondhoraj Lime & Tamarind Pulp",
        level7_cooking_method=["Deep Fried (Flour Shell)", "Boiled", "Assembled"],
        level8_portion_type="piece_count",
        level9_nutrition_ref_id="ifct_chaat_puchka_kolkata"
    ),
    food_family="Chaat",
    sub_family="Pani Puri",
    region="East India",
    state_or_city="West Bengal / Kolkata",
    regional_names={"English": "Kolkata Puchka", "Bengali": "ফুচকা", "Odia": "ଗୁପଚୁପ୍"},
    alternate_names=["puchka", "phuchka", "fuchka", "gupchup", "kolkata puchka"],
    vegetarian=True,
    base_components=["crispy thin flour/semolina ball", "spiced boiled potato mash with yellow peas & roasted bhaja masala", "sour tamarind-gondhoraj lime water"],
    toppings=["chopped green chilli", "coriander", "black salt"],
    sauces_and_chutneys=["tart imli gondhoraj jol (tamarind lime water)"],
    cooking_methods=["Deep Fried", "Boiled", "Assembled"],
    default_portion_unit="piece",
    default_unit_mass_g=26.0,
    density_g_cm3=0.80,
    nutrition_per_100g={"calories": 142.0, "protein_g": 3.1, "carbs_g": 27.2, "fat_g": 2.4, "fiber_g": 2.1, "sodium_mg": 360.0},
    uncertainty_factors=["bhaja_masala_spice", "potato_density", "tamarind_concentration"],
    oil_level_typical="Medium"
))

# 1.2 Bhel Puri & Jhalmuri (Section 6 & 43)
register_street_food_class(StreetFoodClassRecord(
    canonical_food_id="CHAAT_BHEL_PURI_MUMBAI",
    canonical_name="Mumbai Bhel Puri",
    hierarchy=StreetFoodHierarchy(
        level3_food_family="Chaat",
        level4_sub_family="Bhel Puri",
        level5_canonical_food="Bhel Puri",
        level6_variant="Mumbai Wet / Dry Puffed Rice Chaat",
        level7_cooking_method=["Assembled / Raw Mixed"],
        level8_portion_type="bowl_weight_g",
        level9_nutrition_ref_id="ifct_chaat_bhel_puri_mumbai"
    ),
    food_family="Chaat",
    sub_family="Bhel Puri",
    region="West India",
    state_or_city="Maharashtra / Mumbai",
    regional_names={"English": "Mumbai Bhel Puri", "Hindi": "भेल पूरी", "Marathi": "भेळ"},
    alternate_names=["bhel", "bhelpuri", "geeli bhel", "sukha bhel", "mumbai bhel"],
    vegetarian=True,
    base_components=["crispy puffed rice (kurmura/murmura)", "fine nylon sev", "boiled potato cubes", "chopped onion", "chopped tomato", "crushed flat papdi"],
    toppings=["roasted peanuts", "chopped coriander", "raw mango slices (seasonal)", "lemon squeeze"],
    sauces_and_chutneys=["spicy green coriander-chilli chutney", "sweet tamarind-jaggery chutney", "garlic red chutney"],
    cooking_methods=["Assembled"],
    default_portion_unit="bowl",
    default_unit_mass_g=180.0,
    density_g_cm3=0.62,
    nutrition_per_100g={"calories": 178.0, "protein_g": 4.5, "carbs_g": 32.0, "fat_g": 3.8, "fiber_g": 2.6, "sodium_mg": 420.0},
    uncertainty_factors=["wet_vs_dry_chutney_volume", "sev_quantity", "fried_papdi_ratio"],
    oil_level_typical="Low"
))

# 1.3 Sev Puri & Dahi Puri (Section 7 & 8)
register_street_food_class(StreetFoodClassRecord(
    canonical_food_id="CHAAT_SEV_PURI",
    canonical_name="Classic Sev Puri",
    hierarchy=StreetFoodHierarchy(
        level3_food_family="Chaat",
        level4_sub_family="Sev Puri",
        level5_canonical_food="Sev Puri",
        level6_variant="Flat Crispy Papdi with Potato, Chutneys and Thick Sev Blanket",
        level7_cooking_method=["Deep Fried (Papdi)", "Boiled (Potato)", "Assembled"],
        level8_portion_type="plate",
        level9_nutrition_ref_id="ifct_chaat_sev_puri"
    ),
    food_family="Chaat",
    sub_family="Sev Puri",
    region="West India",
    state_or_city="Maharashtra / Gujarat",
    regional_names={"English": "Sev Puri", "Hindi": "सेव पूरी", "Marathi": "शेवपुरी"},
    alternate_names=["sev batata puri", "sev poori", "spdp (sev puri part)"],
    vegetarian=True,
    base_components=["flat crisp flour papdi discs (6 pieces)", "boiled spiced potato cubes", "finely chopped raw onion"],
    toppings=["copious nylon sev blanket", "raw mango shreds", "fresh chopped coriander", "chaat masala"],
    sauces_and_chutneys=["spicy mint-coriander green chutney", "sweet date-tamarind chutney", "spicy garlic red chutney"],
    cooking_methods=["Deep Fried", "Assembled"],
    default_portion_unit="plate",
    default_unit_mass_g=190.0,
    density_g_cm3=0.78,
    nutrition_per_100g={"calories": 215.0, "protein_g": 4.8, "carbs_g": 31.5, "fat_g": 8.2, "fiber_g": 2.8, "sodium_mg": 460.0},
    uncertainty_factors=["sev_blanket_thickness", "tamarind_chutney_sugar", "papdi_oil_retention"],
    oil_level_typical="Medium"
))

register_street_food_class(StreetFoodClassRecord(
    canonical_food_id="CHAAT_DAHI_PURI",
    canonical_name="Dahi Puri",
    hierarchy=StreetFoodHierarchy(
        level3_food_family="Chaat",
        level4_sub_family="Dahi Puri",
        level5_canonical_food="Dahi Puri",
        level6_variant="Puffed Hollow Puris Filled with Potato, Whisked Sweet Curd & Chutneys",
        level7_cooking_method=["Deep Fried (Puri)", "Assembled"],
        level8_portion_type="plate",
        level9_nutrition_ref_id="ifct_chaat_dahi_puri"
    ),
    food_family="Chaat",
    sub_family="Dahi Puri",
    region="Pan-India",
    state_or_city="Mumbai / Delhi / Ahmedabad",
    regional_names={"English": "Dahi Puri", "Hindi": "दही पूरी", "Marathi": "दहीपुरी"},
    alternate_names=["dahi batata puri", "dahi sev batata puri", "dsbp", "dahi puchka"],
    vegetarian=True,
    base_components=["hollow crispy puris (6 pieces)", "boiled spiced potato", "boiled black chickpeas / ragda"],
    toppings=["whisked chilled sweetened yogurt (curd)", "nylon sev", "chaat masala", "roasted jeera", "coriander"],
    sauces_and_chutneys=["sweet tamarind chutney", "spicy mint green chutney"],
    cooking_methods=["Deep Fried", "Assembled"],
    default_portion_unit="plate",
    default_unit_mass_g=230.0,
    density_g_cm3=0.92,
    nutrition_per_100g={"calories": 195.0, "protein_g": 5.2, "carbs_g": 28.5, "fat_g": 6.8, "fiber_g": 2.1, "sodium_mg": 390.0},
    uncertainty_factors=["yogurt_quantity_and_sugar", "sev_quantity", "puri_oil"],
    oil_level_typical="Medium"
))

# 1.4 Ragda Pattice (Section 9)
register_street_food_class(StreetFoodClassRecord(
    canonical_food_id="CHAAT_RAGDA_PATTICE",
    canonical_name="Ragda Pattice",
    hierarchy=StreetFoodHierarchy(
        level3_food_family="Chaat",
        level4_sub_family="Ragda Pattice",
        level5_canonical_food="Ragda Pattice",
        level6_variant="Pan-Fried Spiced Potato Patties with Spiced White Pea Curry",
        level7_cooking_method=["Shallow Fried (Pattice)", "Boiled / Stewed (Ragda)", "Assembled"],
        level8_portion_type="plate",
        level9_nutrition_ref_id="ifct_chaat_ragda_pattice"
    ),
    food_family="Chaat",
    sub_family="Ragda Pattice",
    region="West India",
    state_or_city="Maharashtra / Gujarat",
    regional_names={"English": "Ragda Pattice", "Hindi": "रगड़ा पेटिस", "Marathi": "रगडा पॅटिस"},
    alternate_names=["ragda patties", "ragda pattice chaat", "bombay ragda pattice"],
    vegetarian=True,
    base_components=["crispy golden mashed potato pattice (2 patties)", "warm spiced dried white pea curry (ragda)"],
    toppings=["nylon sev", "finely chopped raw onion", "fresh coriander", "pinch of roasted cumin & red chilli"],
    sauces_and_chutneys=["tangy tamarind chutney", "fiery green chilli-coriander chutney"],
    cooking_methods=["Shallow Fried", "Boiled", "Assembled"],
    default_portion_unit="plate",
    default_unit_mass_g=260.0,
    density_g_cm3=0.94,
    nutrition_per_100g={"calories": 162.0, "protein_g": 5.6, "carbs_g": 26.8, "fat_g": 4.1, "fiber_g": 3.8, "sodium_mg": 440.0},
    uncertainty_factors=["pattice_count", "shallow_fry_oil_in_pattice", "ragda_density_and_portion"],
    oil_level_typical="Medium"
))

# 1.5 Papdi Chaat & Samosa Chaat & Raj Kachori (Sections 10, 11, 12, 13, 14)
register_street_food_class(StreetFoodClassRecord(
    canonical_food_id="CHAAT_PAPDI_CHAAT",
    canonical_name="Delhi Papdi Chaat",
    hierarchy=StreetFoodHierarchy(
        level3_food_family="Chaat",
        level4_sub_family="Papdi Chaat",
        level5_canonical_food="Papdi Chaat",
        level6_variant="Delhi Layered Crispy Papdi with Chickpeas, Potatoes, Chilled Dahi & Chutneys",
        level7_cooking_method=["Deep Fried (Papdi)", "Boiled", "Assembled"],
        level8_portion_type="plate",
        level9_nutrition_ref_id="ifct_chaat_papdi_delhi"
    ),
    food_family="Chaat",
    sub_family="Papdi Chaat",
    region="North India",
    state_or_city="Delhi / Punjab",
    regional_names={"English": "Papdi Chaat", "Hindi": "पापड़ी चाट", "Punjabi": "ਪਾਪੜੀ ਚਾਟ"},
    alternate_names=["dahi papdi chaat", "papri chaat", "delhi chaat"],
    vegetarian=True,
    base_components=["crispy whole wheat papdi crackers", "boiled chickpeas (kabuli chana)", "diced boiled potatoes"],
    toppings=["thick sweetened curd (dahi)", "nylon sev", "pomegranate arils", "roasted cumin powder", "black salt"],
    sauces_and_chutneys=["sweet tamarind-sonth chutney", "spicy green coriander chutney"],
    cooking_methods=["Deep Fried", "Assembled"],
    default_portion_unit="plate",
    default_unit_mass_g=240.0,
    density_g_cm3=0.91,
    nutrition_per_100g={"calories": 188.0, "protein_g": 5.4, "carbs_g": 27.2, "fat_g": 6.5, "fiber_g": 2.5, "sodium_mg": 410.0},
    uncertainty_factors=["dahi_creaminess_and_sugar", "papdi_oil", "chutney_volume"],
    oil_level_typical="Medium"
))

register_street_food_class(StreetFoodClassRecord(
    canonical_food_id="CHAAT_SAMOSA_CHAAT",
    canonical_name="Samosa Chaat",
    hierarchy=StreetFoodHierarchy(
        level3_food_family="Chaat",
        level4_sub_family="Samosa Chaat",
        level5_canonical_food="Samosa Chaat",
        level6_variant="Crushed Crispy Samosa Topped with Spicy Chole Curry, Curd & Chutneys",
        level7_cooking_method=["Deep Fried (Samosa)", "Stewed (Chole)", "Assembled"],
        level8_portion_type="plate",
        level9_nutrition_ref_id="ifct_chaat_samosa_chaat"
    ),
    food_family="Chaat",
    sub_family="Samosa Chaat",
    region="Pan-India",
    state_or_city="North / Pan-India",
    regional_names={"English": "Samosa Chaat", "Hindi": "समोसा चाट", "Punjabi": "ਸਮੋਸਾ ਚਾਟ"},
    alternate_names=["chole samosa chaat", "crushed samosa chaat", "samosa chana chaat"],
    vegetarian=True,
    base_components=["broken fried potato samosa (1 or 2 pieces)", "spicy chickpea curry (chole)"],
    toppings=["whisked chilled dahi", "nylon sev", "finely diced raw onion", "fresh coriander", "chaat masala"],
    sauces_and_chutneys=["saunth sweet tamarind chutney", "fiery green mint chutney"],
    cooking_methods=["Deep Fried", "Stewed", "Assembled"],
    default_portion_unit="plate",
    default_unit_mass_g=310.0,
    density_g_cm3=0.95,
    nutrition_per_100g={"calories": 196.0, "protein_g": 5.8, "carbs_g": 26.5, "fat_g": 7.8, "fiber_g": 3.4, "sodium_mg": 480.0},
    uncertainty_factors=["samosa_piece_count", "underlying_samosa_crust_oil", "chole_gravy_volume"],
    oil_level_typical="High"
))

register_street_food_class(StreetFoodClassRecord(
    canonical_food_id="CHAAT_RAJ_KACHORI",
    canonical_name="Royal Raj Kachori",
    hierarchy=StreetFoodHierarchy(
        level3_food_family="Chaat",
        level4_sub_family="Raj Kachori",
        level5_canonical_food="Raj Kachori",
        level6_variant="Large Crispy Puffed Shell Stuffed with Sprouts, Potato, Bhalla, Dahi & Chutneys",
        level7_cooking_method=["Deep Fried (Shell)", "Assembled"],
        level8_portion_type="plate",
        level9_nutrition_ref_id="ifct_chaat_raj_kachori"
    ),
    food_family="Chaat",
    sub_family="Raj Kachori",
    region="North India",
    state_or_city="Rajasthan / Delhi",
    regional_names={"English": "Raj Kachori", "Hindi": "राज कचौरी"},
    alternate_names=["royal kachori chaat", "delhi raj kachori", "rajasthani raj kachori"],
    vegetarian=True,
    base_components=["large crispy semolina-flour dome shell", "sprouted moong beans", "boiled potato cubes", "soft dahi pakodi / bhalla pieces"],
    toppings=["thick sweetened curd", "nylon sev", "ruby pomegranate seeds", "beetroot juliennes", "cashews"],
    sauces_and_chutneys=["rich sonth tamarind chutney", "mint green chutney"],
    cooking_methods=["Deep Fried", "Assembled"],
    default_portion_unit="plate",
    default_unit_mass_g=360.0,
    density_g_cm3=0.88,
    nutrition_per_100g={"calories": 218.0, "protein_g": 5.2, "carbs_g": 29.4, "fat_g": 9.2, "fiber_g": 2.8, "sodium_mg": 450.0},
    uncertainty_factors=["shell_diameter_10_vs_15cm", "filling_density", "dry_fruit_toppings"],
    oil_level_typical="High"
))

register_street_food_class(StreetFoodClassRecord(
    canonical_food_id="CHAAT_ALOO_CHAAT_FRIED",
    canonical_name="Delhi Fried Aloo Chaat",
    hierarchy=StreetFoodHierarchy(
        level3_food_family="Chaat",
        level4_sub_family="Aloo Chaat",
        level5_canonical_food="Aloo Chaat",
        level6_variant="Deep Fried Golden Potato Cubes Tossed with Chaat Masala & Chutneys",
        level7_cooking_method=["Deep Fried (Potatoes)", "Tossed"],
        level8_portion_type="plate",
        level9_nutrition_ref_id="ifct_chaat_aloo_fried"
    ),
    food_family="Chaat",
    sub_family="Aloo Chaat",
    region="North India",
    state_or_city="Delhi / Uttar Pradesh",
    regional_names={"English": "Fried Aloo Chaat", "Hindi": "आलू चाट"},
    alternate_names=["delhi aloo chaat", "fried potato chaat", "tandoori aloo chaat"],
    vegetarian=True,
    base_components=["crisp deep-fried potato cubes"],
    toppings=["chaat masala", "roasted jeera", "lemon juice", "ginger juliennes", "chopped coriander"],
    sauces_and_chutneys=["spicy green chutney", "sweet tamarind sonth chutney"],
    cooking_methods=["Deep Fried", "Assembled"],
    default_portion_unit="plate",
    default_unit_mass_g=200.0,
    density_g_cm3=0.88,
    nutrition_per_100g={"calories": 235.0, "protein_g": 2.8, "carbs_g": 31.0, "fat_g": 11.2, "fiber_g": 3.1, "sodium_mg": 490.0},
    uncertainty_factors=["frying_oil_absorption", "boiled_vs_fried_potato_cooking_method"],
    oil_level_typical="High"
))


# =============================================================================
# 2. FRIED SNACKS (Sections 15 - 20)
# =============================================================================

# 2.1 Samosa & Kachori (Sections 16 & 17)
register_street_food_class(StreetFoodClassRecord(
    canonical_food_id="FRIED_SAMOSA_PUNJABI",
    canonical_name="Punjabi Aloo Samosa",
    hierarchy=StreetFoodHierarchy(
        level3_food_family="Fried Snacks",
        level4_sub_family="Samosa",
        level5_canonical_food="Samosa",
        level6_variant="Crispy Flaky Pastry Stuffed with Spiced Chunky Potato, Peas & Cashews",
        level7_cooking_method=["Deep Fried"],
        level8_portion_type="piece_count",
        level9_nutrition_ref_id="ifct_fried_samosa_punjabi"
    ),
    food_family="Fried Snacks",
    sub_family="Samosa",
    region="North India",
    state_or_city="Punjab / Delhi",
    regional_names={"English": "Punjabi Samosa", "Hindi": "समोसा", "Punjabi": "ਸਮੋਸਾ"},
    alternate_names=["samosa", "aloo samosa", "halwai samosa", "punjabi samosa"],
    vegetarian=True,
    base_components=["flaky maida pastry shell with ajwain", "spiced potato filling with green peas, coriander seeds & garam masala"],
    toppings=["fried green chilli"],
    sauces_and_chutneys=["mint-coriander chutney", "tamarind sweet chutney"],
    cooking_methods=["Deep Fried"],
    default_portion_unit="piece",
    default_unit_mass_g=105.0,
    density_g_cm3=0.82,
    nutrition_per_100g={"calories": 262.0, "protein_g": 4.5, "carbs_g": 32.5, "fat_g": 13.0, "fiber_g": 2.8, "sodium_mg": 380.0},
    uncertainty_factors=["crust_thickness", "oil_drainage", "cashew_raisin_inclusion"],
    oil_level_typical="High"
))

register_street_food_class(StreetFoodClassRecord(
    canonical_food_id="FRIED_KACHORI_PYAZ",
    canonical_name="Jodhpur Pyaz Kachori",
    hierarchy=StreetFoodHierarchy(
        level3_food_family="Fried Snacks",
        level4_sub_family="Kachori",
        level5_canonical_food="Kachori",
        level6_variant="Flaky Puffed Round Pastry with Spicy Caramelized Onion & Besan Filling",
        level7_cooking_method=["Deep Fried"],
        level8_portion_type="piece_count",
        level9_nutrition_ref_id="ifct_fried_kachori_pyaz"
    ),
    food_family="Fried Snacks",
    sub_family="Kachori",
    region="North India",
    state_or_city="Rajasthan / Jodhpur",
    regional_names={"English": "Pyaz Kachori", "Hindi": "प्याज़ कचौरी", "Rajasthani": "कांदा कचौरी"},
    alternate_names=["pyaaz kachori", "onion kachori", "jodhpuri pyaz kachori"],
    vegetarian=True,
    base_components=["crisp flaky all-purpose flour shell", "spicy roasted onion, gram flour (besan), saunf & hing stuffing"],
    toppings=["fried green chillies"],
    sauces_and_chutneys=["tamarind chutney", "green chilli chutney"],
    cooking_methods=["Deep Fried"],
    default_portion_unit="piece",
    default_unit_mass_g=120.0,
    density_g_cm3=0.84,
    nutrition_per_100g={"calories": 298.0, "protein_g": 5.6, "carbs_g": 34.0, "fat_g": 15.5, "fiber_g": 3.2, "sodium_mg": 460.0},
    uncertainty_factors=["shell_oil_absorption", "filling_quantity"],
    oil_level_typical="High"
))

# 2.2 Pakora / Bhajiya (Sections 18 & 19)
register_street_food_class(StreetFoodClassRecord(
    canonical_food_id="FRIED_PAKODA_ONION",
    canonical_name="Kanda Bhajiya / Onion Pakoda",
    hierarchy=StreetFoodHierarchy(
        level3_food_family="Fried Snacks",
        level4_sub_family="Pakora",
        level5_canonical_food="Pakoda",
        level6_variant="Thin Sliced Onion Coated in Spiced Gram Flour Batter Fried Crisp",
        level7_cooking_method=["Deep Fried"],
        level8_portion_type="plate",
        level9_nutrition_ref_id="ifct_fried_kanda_bhaji"
    ),
    food_family="Fried Snacks",
    sub_family="Pakora",
    region="Pan-India",
    state_or_city="Maharashtra / Pan-India",
    regional_names={"English": "Onion Pakoda", "Hindi": "प्याज़ के पकौड़े", "Marathi": "कांदा भजी", "Tamil": "வெங்காய பக்கோடா"},
    alternate_names=["kanda bhaji", "pyaz pakoda", "onion bhaji", "vengaya pakoda"],
    vegetarian=True,
    base_components=["sliced onions", "gram flour (besan)", "carom seeds (ajwain)", "green chillies", "rice flour for crispness"],
    toppings=["chaat masala", "fried salted green chilli"],
    sauces_and_chutneys=["green chutney", "fried dry garlic chutney"],
    cooking_methods=["Deep Fried"],
    default_portion_unit="plate",
    default_unit_mass_g=150.0,
    density_g_cm3=0.76,
    nutrition_per_100g={"calories": 312.0, "protein_g": 7.2, "carbs_g": 32.5, "fat_g": 17.5, "fiber_g": 4.1, "sodium_mg": 490.0},
    uncertainty_factors=["oil_absorption_ratio", "crisp_vs_soft_batter_density"],
    oil_level_typical="High"
))

register_street_food_class(StreetFoodClassRecord(
    canonical_food_id="FRIED_BREAD_PAKODA",
    canonical_name="Aloo Stuffed Bread Pakoda",
    hierarchy=StreetFoodHierarchy(
        level3_food_family="Fried Snacks",
        level4_sub_family="Pakora",
        level5_canonical_food="Bread Pakoda",
        level6_variant="Spiced Potato Sandwiched in Bread Slices Dipped in Besan Batter & Fried",
        level7_cooking_method=["Deep Fried"],
        level8_portion_type="piece_count",
        level9_nutrition_ref_id="ifct_fried_bread_pakoda"
    ),
    food_family="Fried Snacks",
    sub_family="Pakora",
    region="North India",
    state_or_city="Delhi / Punjab / UP",
    regional_names={"English": "Bread Pakoda", "Hindi": "ब्रेड पकौड़ा"},
    alternate_names=["bread pakora", "stuffed bread pakoda", "paneer bread pakoda"],
    vegetarian=True,
    base_components=["white bread triangle slices", "spiced mashed potato filling", "spiced gram flour (besan) batter"],
    toppings=["chaat masala"],
    sauces_and_chutneys=["mint chutney", "tomato ketchup"],
    cooking_methods=["Deep Fried"],
    default_portion_unit="piece",
    default_unit_mass_g=140.0,
    density_g_cm3=0.81,
    nutrition_per_100g={"calories": 278.0, "protein_g": 5.4, "carbs_g": 35.0, "fat_g": 13.2, "fiber_g": 2.2, "sodium_mg": 520.0},
    uncertainty_factors=["bread_oil_sponge_retention", "paneer_slice_presence"],
    oil_level_typical="High"
))

# 2.3 Vada / Bonda (Section 20)
register_street_food_class(StreetFoodClassRecord(
    canonical_food_id="FRIED_BATATA_VADA",
    canonical_name="Mumbai Batata Vada",
    hierarchy=StreetFoodHierarchy(
        level3_food_family="Fried Snacks",
        level4_sub_family="Vada",
        level5_canonical_food="Batata Vada",
        level6_variant="Spherical Spiced Mustard-Curry Leaf Potato Ball Fried in Besan Batter",
        level7_cooking_method=["Deep Fried"],
        level8_portion_type="piece_count",
        level9_nutrition_ref_id="ifct_fried_batata_vada"
    ),
    food_family="Fried Snacks",
    sub_family="Vada",
    region="West India",
    state_or_city="Maharashtra / Mumbai",
    regional_names={"English": "Batata Vada", "Hindi": "बटाटा वड़ा", "Marathi": "बटाटा वडा", "Gujarati": "બટાટા વડા"},
    alternate_names=["batata vada", "aloo bonda", "potato vada", "mumbai vada"],
    vegetarian=True,
    base_components=["spiced mashed potato filling tempered with mustard seeds, green chilli, ginger, curry leaves & turmeric", "gram flour (besan) batter"],
    toppings=["fried salted green chillies"],
    sauces_and_chutneys=["dry red garlic coconut chutney", "green chutney"],
    cooking_methods=["Deep Fried"],
    default_portion_unit="piece",
    default_unit_mass_g=75.0,
    density_g_cm3=0.86,
    nutrition_per_100g={"calories": 224.0, "protein_g": 4.5, "carbs_g": 26.5, "fat_g": 11.2, "fiber_g": 2.8, "sodium_mg": 410.0},
    uncertainty_factors=["batter_thickness", "oil_temperature_drainage"],
    oil_level_typical="High"
))


# =============================================================================
# 3. PAV-BASED STREET FOODS (Sections 21 - 26)
# =============================================================================

# 3.1 Vada Pav (Section 21)
register_street_food_class(StreetFoodClassRecord(
    canonical_food_id="PAV_VADA_PAV_CLASSIC",
    canonical_name="Classic Mumbai Vada Pav",
    hierarchy=StreetFoodHierarchy(
        level3_food_family="Pav-Based Foods",
        level4_sub_family="Vada Pav",
        level5_canonical_food="Vada Pav",
        level6_variant="Spiced Batata Vada Slotted Inside Ladi Pav with Dry Garlic & Green Chutneys",
        level7_cooking_method=["Deep Fried (Vada)", "Assembled"],
        level8_portion_type="piece_count",
        level9_nutrition_ref_id="ifct_pav_vada_pav_classic"
    ),
    food_family="Pav-Based Foods",
    sub_family="Vada Pav",
    region="West India",
    state_or_city="Maharashtra / Mumbai",
    regional_names={"English": "Vada Pav", "Hindi": "वड़ा पाव", "Marathi": "वडा पाव", "Gujarati": "વડાપાવ"},
    alternate_names=["vada pav", "wada pav", "vada pao", "bombay burger", "mumbai vada pav"],
    vegetarian=True,
    base_components=["soft white ladi pav (1 bun)", "golden batata vada (1 patty)"],
    toppings=["crunchy besan choora (fry bits)", "fried salted green chilli"],
    sauces_and_chutneys=["spicy red dry garlic chutney (lasun chutney)", "fiery green coriander-chilli chutney", "sweet tamarind chutney"],
    cooking_methods=["Deep Fried", "Assembled"],
    default_portion_unit="piece",
    default_unit_mass_g=135.0,
    density_g_cm3=0.74,
    nutrition_per_100g={"calories": 248.0, "protein_g": 5.8, "carbs_g": 38.0, "fat_g": 8.5, "fiber_g": 2.4, "sodium_mg": 480.0},
    uncertainty_factors=["butter_grilling_of_pav", "vada_size", "chutney_dryness"],
    oil_level_typical="Medium"
))

# 3.2 Pav Bhaji (Section 22)
register_street_food_class(StreetFoodClassRecord(
    canonical_food_id="PAV_BHAJI_BUTTER",
    canonical_name="Mumbai Butter Pav Bhaji",
    hierarchy=StreetFoodHierarchy(
        level3_food_family="Pav-Based Foods",
        level4_sub_family="Pav Bhaji",
        level5_canonical_food="Pav Bhaji",
        level6_variant="Mashed Vegetable Tomato Bhaji with Butter Slabs & Butter-Toasted Pavs",
        level7_cooking_method=["Boiled / Mashed / Tawa Sautéed", "Tawa Toasted (Pav)"],
        level8_portion_type="plate",
        level9_nutrition_ref_id="ifct_pav_bhaji_butter"
    ),
    food_family="Pav-Based Foods",
    sub_family="Pav Bhaji",
    region="West India",
    state_or_city="Maharashtra / Mumbai",
    regional_names={"English": "Pav Bhaji", "Hindi": "पाव भाजी", "Marathi": "पावभाजी", "Gujarati": "પાવભાજી"},
    alternate_names=["pav bhaji", "pao bhaji", "bombay pav bhaji", "amul butter pav bhaji"],
    vegetarian=True,
    base_components=["mashed vegetable bhaji (potatoes, peas, tomatoes, cauliflower, capsicum with pav bhaji masala)", "butter-griddled ladi pav (2 buns)"],
    toppings=["Amul butter slab (15-25g on bhaji)", "finely chopped raw red onion", "lemon wedge", "chopped coriander"],
    sauces_and_chutneys=["garlic butter tadka (optional)"],
    cooking_methods=["Tawa Sautéed", "Tawa Toasted"],
    default_portion_unit="plate",
    default_unit_mass_g=340.0,
    density_g_cm3=0.88,
    nutrition_per_100g={"calories": 182.0, "protein_g": 3.8, "carbs_g": 23.5, "fat_g": 8.2, "fiber_g": 2.8, "sodium_mg": 510.0},
    uncertainty_factors=["butter_slab_mass_10g_vs_30g", "extra_pav_count", "cheese_topping"],
    oil_level_typical="High"
))

# 3.3 Misal Pav & Usal Pav (Sections 23 & 24)
register_street_food_class(StreetFoodClassRecord(
    canonical_food_id="PAV_MISAL_KOLHAPURI",
    canonical_name="Kolhapuri Teekha Misal Pav",
    hierarchy=StreetFoodHierarchy(
        level3_food_family="Pav-Based Foods",
        level4_sub_family="Misal Pav",
        level5_canonical_food="Misal Pav",
        level6_variant="Fiery Red Sprouted Moth Bean Curry with Farsan, Tarri & Soft Pav",
        level7_cooking_method=["Stewed / Boiled (Usal)", "Assembled"],
        level8_portion_type="plate",
        level9_nutrition_ref_id="ifct_pav_misal_kolhapuri"
    ),
    food_family="Pav-Based Foods",
    sub_family="Misal Pav",
    region="West India",
    state_or_city="Maharashtra / Kolhapur",
    regional_names={"English": "Kolhapuri Misal Pav", "Hindi": "मिसल पाव", "Marathi": "कोल्हापुरी मिसळ पाव"},
    alternate_names=["misal pav", "kolhapuri misal", "puneri misal", "tarri misal", "kat misal"],
    vegetarian=True,
    base_components=["sprouted matki (moth beans) usal", "fiery red spicy oily gravy (tarri / kat / rassa)", "soft ladi pav (2 buns)"],
    toppings=["crispy mixed farsan / sev", "chopped raw red onions", "lemon wedge", "fresh coriander"],
    sauces_and_chutneys=["extra tarri bowl"],
    cooking_methods=["Stewed", "Assembled"],
    default_portion_unit="plate",
    default_unit_mass_g=330.0,
    density_g_cm3=0.89,
    nutrition_per_100g={"calories": 168.0, "protein_g": 5.4, "carbs_g": 24.2, "fat_g": 5.8, "fiber_g": 3.6, "sodium_mg": 530.0},
    uncertainty_factors=["tarri_oil_float_layer", "farsan_quantity", "pav_count"],
    oil_level_typical="High"
))

# 3.4 Dabeli (Section 25)
register_street_food_class(StreetFoodClassRecord(
    canonical_food_id="PAV_DABELI_KUTCHI",
    canonical_name="Kutchi Dabeli",
    hierarchy=StreetFoodHierarchy(
        level3_food_family="Pav-Based Foods",
        level4_sub_family="Dabeli",
        level5_canonical_food="Dabeli",
        level6_variant="Sweet-Spicy Mashed Potato Filling in Pav with Masala Peanuts, Pomegranate & Sev",
        level7_cooking_method=["Tawa Toasted (Pav)", "Assembled"],
        level8_portion_type="piece_count",
        level9_nutrition_ref_id="ifct_pav_dabeli_kutchi"
    ),
    food_family="Pav-Based Foods",
    sub_family="Dabeli",
    region="West India",
    state_or_city="Gujarat / Kutch",
    regional_names={"English": "Kutchi Dabeli", "Hindi": "दाबेली", "Gujarati": "દાબેલી", "Marathi": "दाबेली"},
    alternate_names=["dabeli", "kutchi dabeli", "double roti", "spicy burger"],
    vegetarian=True,
    base_components=["soft pav toasted with butter/oil", "spicy dabeli masala potato mash"],
    toppings=["spiced roasted masala peanuts (sing)", "fresh pomegranate arils (anar)", "fine nylon sev", "chopped coriander"],
    sauces_and_chutneys=["sweet tamarind-date chutney", "spicy red garlic-chilli chutney"],
    cooking_methods=["Tawa Toasted", "Assembled"],
    default_portion_unit="piece",
    default_unit_mass_g=140.0,
    density_g_cm3=0.76,
    nutrition_per_100g={"calories": 242.0, "protein_g": 5.6, "carbs_g": 36.5, "fat_g": 8.6, "fiber_g": 2.8, "sodium_mg": 460.0},
    uncertainty_factors=["peanuts_density", "butter_toasting", "cheese_addition"],
    oil_level_typical="Medium"
))


# =============================================================================
# 4. ROLLS & WRAPS (Sections 27 - 30)
# =============================================================================

# 4.1 Kathi Roll (Section 28)
register_street_food_class(StreetFoodClassRecord(
    canonical_food_id="ROLL_KATHI_CHICKEN",
    canonical_name="Kolkata Chicken Kathi Roll",
    hierarchy=StreetFoodHierarchy(
        level3_food_family="Rolls / Wraps",
        level4_sub_family="Kathi Roll",
        level5_canonical_food="Chicken Kathi Roll",
        level6_variant="Flaky Lachha Paratha Layered with Egg & Skewered Spiced Chicken Boti",
        level7_cooking_method=["Tawa Griddled (Paratha)", "Pan Sautéed / Skewered (Chicken)", "Assembled"],
        level8_portion_type="wrap",
        level9_nutrition_ref_id="ifct_roll_kathi_chicken"
    ),
    food_family="Rolls / Wraps",
    sub_family="Kathi Roll",
    region="East India",
    state_or_city="West Bengal / Kolkata",
    regional_names={"English": "Chicken Kathi Roll", "Bengali": "চিকেন কাঠি রোল", "Hindi": "काठी रोल"},
    alternate_names=["chicken roll", "kathi roll", "kolkata kathi roll", "egg chicken roll"],
    vegetarian=False,
    base_components=["crispy layered refined flour (maida) paratha", "egg lining (single or double egg on paratha)", "spiced marinated roasted chicken chunks"],
    toppings=["sliced raw red onions", "green chillies", "fresh coriander", "chaat masala", "fresh lime juice squeeze"],
    sauces_and_chutneys=["green chilli-coriander sauce", "kasundi / mustard dash (optional)", "tomato ketchup dash"],
    cooking_methods=["Tawa Griddled", "Assembled"],
    default_portion_unit="wrap",
    default_unit_mass_g=220.0,
    density_g_cm3=0.86,
    nutrition_per_100g={"calories": 238.0, "protein_g": 12.5, "carbs_g": 24.0, "fat_g": 10.5, "fiber_g": 1.4, "sodium_mg": 460.0},
    uncertainty_factors=["single_vs_double_egg", "paratha_oil_level", "mayo_vs_chutney"],
    oil_level_typical="High"
))

# 4.2 Frankie (Section 29)
register_street_food_class(StreetFoodClassRecord(
    canonical_food_id="ROLL_FRANKIE_VEG",
    canonical_name="Mumbai Veg Frankie",
    hierarchy=StreetFoodHierarchy(
        level3_food_family="Rolls / Wraps",
        level4_sub_family="Frankie",
        level5_canonical_food="Veg Frankie",
        level6_variant="Thin Roti Wrapped Spiced Potato Cutlet with Frankie Masala & Vinegar Chillies",
        level7_cooking_method=["Tawa Toasted", "Shallow Fried (Cutlet)", "Assembled"],
        level8_portion_type="wrap",
        level9_nutrition_ref_id="ifct_roll_frankie_veg"
    ),
    food_family="Rolls / Wraps",
    sub_family="Frankie",
    region="West India",
    state_or_city="Maharashtra / Mumbai",
    regional_names={"English": "Veg Frankie", "Hindi": "वेज फ्रेंकी", "Marathi": "फ्रँकी"},
    alternate_names=["frankie", "aloo frankie", "bombay frankie", "veg roll mumbai"],
    vegetarian=True,
    base_components=["thin warm flatbread / roti", "crisp spiced cylindrical mashed potato patty"],
    toppings=["shredded raw cabbage", "sliced raw onion", "secret tangy Frankie masala powder", "vinegar-infused green chillies"],
    sauces_and_chutneys=["tangy chilli sauce", "mint chutney"],
    cooking_methods=["Tawa Toasted", "Assembled"],
    default_portion_unit="wrap",
    default_unit_mass_g=190.0,
    density_g_cm3=0.80,
    nutrition_per_100g={"calories": 205.0, "protein_g": 4.6, "carbs_g": 31.0, "fat_g": 7.2, "fiber_g": 2.4, "sodium_mg": 440.0},
    uncertainty_factors=["cheese_grating_addition", "schezwan_sauce_dressing", "roti_butter"],
    oil_level_typical="Medium"
))

# 4.3 Shawarma (Section 30)
register_street_food_class(StreetFoodClassRecord(
    canonical_food_id="ROLL_SHAWARMA_CHICKEN",
    canonical_name="Indian Street Chicken Shawarma",
    hierarchy=StreetFoodHierarchy(
        level3_food_family="Rolls / Wraps",
        level4_sub_family="Shawarma",
        level5_canonical_food="Chicken Shawarma",
        level6_variant="Spit-Roasted Spiced Chicken Shavings in Kubbus/Pita with Garlic Mayo & Pickles",
        level7_cooking_method=["Vertical Rotisserie Spit Roasted", "Assembled"],
        level8_portion_type="wrap",
        level9_nutrition_ref_id="ifct_roll_shawarma_chicken"
    ),
    food_family="Rolls / Wraps",
    sub_family="Shawarma",
    region="Pan-India",
    state_or_city="Kerala / Hyderabad / Mumbai / Delhi",
    regional_names={"English": "Chicken Shawarma", "Hindi": "शवरमा", "Malayalam": "ഷവർമ", "Arabic": "شاورما"},
    alternate_names=["shawarma", "shwarma", "chicken roll shawarma", "kubbus shawarma"],
    vegetarian=False,
    base_components=["soft flatbread (kubbus, rumali roti or pita)", "shredded roasted spiced marinated chicken pieces"],
    toppings=["french fries inside", "pickled beetroot/cucumber", "shredded cabbage"],
    sauces_and_chutneys=["garlic mayonnaise (toum)", "tahini sauce", "spicy chilli sauce"],
    cooking_methods=["Spit Roasted", "Assembled"],
    default_portion_unit="wrap",
    default_unit_mass_g=230.0,
    density_g_cm3=0.88,
    nutrition_per_100g={"calories": 255.0, "protein_g": 13.8, "carbs_g": 22.0, "fat_g": 12.8, "fiber_g": 1.2, "sodium_mg": 540.0},
    uncertainty_factors=["mayo_quantity_30g_vs_60g", "french_fries_inside", "extra_cheese_addition"],
    oil_level_typical="High"
))


# =============================================================================
# 5. STREET SANDWICHES & TOASTS (Sections 31 - 32)
# =============================================================================

register_street_food_class(StreetFoodClassRecord(
    canonical_food_id="SANDWICH_BOMBAY_GRILLED_VEG",
    canonical_name="Bombay Grilled Vegetable Sandwich",
    hierarchy=StreetFoodHierarchy(
        level3_food_family="Sandwiches",
        level4_sub_family="Grilled Sandwich",
        level5_canonical_food="Bombay Sandwich",
        level6_variant="Triple-Decker Grilled Sandwich with Spiced Potatoes, Veggies, Cheese & Chutney",
        level7_cooking_method=["Cast-Iron / Electric Toaster Grilled"],
        level8_portion_type="piece_count",
        level9_nutrition_ref_id="ifct_sandwich_bombay_veg"
    ),
    food_family="Sandwiches",
    sub_family="Grilled Sandwich",
    region="West India",
    state_or_city="Maharashtra / Mumbai",
    regional_names={"English": "Bombay Grilled Sandwich", "Hindi": "बॉम्बे ग्रिल्ड सैंडविच", "Marathi": "सँडविच"},
    alternate_names=["bombay sandwich", "veg cheese grilled sandwich", "street sandwich"],
    vegetarian=True,
    base_components=["white sandwich bread slices (3 slices)", "boiled spiced potato rounds", "sliced beetroot", "cucumber rounds", "tomato slices", "capsicum rings", "onion slices"],
    toppings=["grated processed cheddar cheese (Amul cheese)", "sandwich masala (spiced cumin-black salt)", "butter coating"],
    sauces_and_chutneys=["spicy green coriander-mint chutney", "tomato ketchup"],
    cooking_methods=["Grilled"],
    default_portion_unit="piece",
    default_unit_mass_g=240.0,
    density_g_cm3=0.78,
    nutrition_per_100g={"calories": 218.0, "protein_g": 6.2, "carbs_g": 26.5, "fat_g": 9.8, "fiber_g": 2.6, "sodium_mg": 520.0},
    uncertainty_factors=["butter_spread_mass", "cheese_grating_volume", "bread_slice_count"],
    oil_level_typical="High"
))


# =============================================================================
# 6. INDO-CHINESE & NOODLES (Sections 47 - 50)
# =============================================================================

register_street_food_class(StreetFoodClassRecord(
    canonical_food_id="INDOCHINESE_HAKKA_NOODLES_VEG",
    canonical_name="Street Style Veg Hakka Noodles",
    hierarchy=StreetFoodHierarchy(
        level3_food_family="Noodles / Indo-Chinese",
        level4_sub_family="Hakka Noodles",
        level5_canonical_food="Hakka Noodles",
        level6_variant="High-Flame Wok Tossed Long Straight Noodles with Crunchy Juliennes & Soy-Vinegar",
        level7_cooking_method=["Boiled (Noodles)", "High-Flame Wok Stir-Fried"],
        level8_portion_type="plate",
        level9_nutrition_ref_id="ifct_indochinese_hakka_veg"
    ),
    food_family="Noodles / Indo-Chinese",
    sub_family="Hakka Noodles",
    region="Pan-India",
    state_or_city="Kolkata / Mumbai / Delhi / Pan-India",
    regional_names={"English": "Veg Hakka Noodles", "Hindi": "वेज हक्का नूडल्स", "Bengali": "চাউমিন"},
    alternate_names=["hakka noodles", "veg noodles", "chow mein", "street noodles", "deshi noodles"],
    vegetarian=True,
    base_components=["boiled refined wheat noodles", "julienned cabbage", "sliced carrots", "capsicum / bell pepper", "sliced onions", "chopped garlic"],
    toppings=["chopped spring onion greens", "white pepper", "ajinomoto/MSG dash"],
    sauces_and_chutneys=["dark soy sauce", "green chilli sauce", "synthetic vinegar", "chilli garlic dip"],
    cooking_methods=["Wok Stir-Fried"],
    default_portion_unit="plate",
    default_unit_mass_g=280.0,
    density_g_cm3=0.82,
    nutrition_per_100g={"calories": 172.0, "protein_g": 3.6, "carbs_g": 28.5, "fat_g": 5.2, "fiber_g": 2.0, "sodium_mg": 580.0},
    uncertainty_factors=["wok_oil_quantity", "msg_and_sodium", "sauce_density"],
    oil_level_typical="Medium"
))

register_street_food_class(StreetFoodClassRecord(
    canonical_food_id="INDOCHINESE_MAGGI_MASALA",
    canonical_name="Street Style Loaded Butter Masala Maggi",
    hierarchy=StreetFoodHierarchy(
        level3_food_family="Noodles / Indo-Chinese",
        level4_sub_family="Instant Noodles",
        level5_canonical_food="Masala Maggi",
        level6_variant="Wavy Curly Instant Wheat Noodles Cooked with Sautéed Veggies, Spices & Butter",
        level7_cooking_method=["Pan Sautéed / Simmered"],
        level8_portion_type="bowl_weight_g",
        level9_nutrition_ref_id="ifct_indochinese_maggi_masala"
    ),
    food_family="Noodles / Indo-Chinese",
    sub_family="Instant Noodles",
    region="Pan-India",
    state_or_city="Pan-India / Hill Stations / College Canteens",
    regional_names={"English": "Masala Maggi", "Hindi": "मसाला मैगी"},
    alternate_names=["maggi", "street maggi", "butter maggi", "cheese maggi", "tadka maggi"],
    vegetarian=True,
    base_components=["curly instant noodle cake (70g dry)", "tastemaker spice blend", "water/broth"],
    toppings=["diced onions", "green peas", "tomatoes", "green chillies", "dollop of butter", "chopped coriander"],
    sauces_and_chutneys=["tastemaker broth sauce"],
    cooking_methods=["Simmered", "Pan Sautéed"],
    default_portion_unit="bowl",
    default_unit_mass_g=240.0,
    density_g_cm3=0.85,
    nutrition_per_100g={"calories": 185.0, "protein_g": 3.8, "carbs_g": 26.0, "fat_g": 7.4, "fiber_g": 1.6, "sodium_mg": 680.0},
    uncertainty_factors=["dry_cake_count_single_vs_double", "butter_added", "cheese_grated_addition"],
    oil_level_typical="Medium"
))

register_street_food_class(StreetFoodClassRecord(
    canonical_food_id="INDOCHINESE_MANCHURIAN_GOBI",
    canonical_name="Street Gobi Manchurian Dry",
    hierarchy=StreetFoodHierarchy(
        level3_food_family="Noodles / Indo-Chinese",
        level4_sub_family="Manchurian",
        level5_canonical_food="Gobi Manchurian",
        level6_variant="Deep Fried Battered Cauliflower Florets Tossed in Tangy Spicy Soy-Garlic Glaze",
        level7_cooking_method=["Deep Fried (Florets)", "Wok Tossed"],
        level8_portion_type="plate",
        level9_nutrition_ref_id="ifct_indochinese_gobi_manchurian"
    ),
    food_family="Noodles / Indo-Chinese",
    sub_family="Manchurian",
    region="Pan-India",
    state_or_city="Bengaluru / Mumbai / Delhi / Pan-India",
    regional_names={"English": "Gobi Manchurian", "Hindi": "गोभी मंचूरियन", "Kannada": "ಗೋಬಿ ಮಂಚೂರಿಯನ್"},
    alternate_names=["gobi manchurian", "cauliflower manchurian", "dry manchurian"],
    vegetarian=True,
    base_components=["cauliflower florets in cornstarch-all purpose flour batter", "chopped garlic", "ginger", "green chillies", "spring onions"],
    toppings=["spring onion greens", "coriander"],
    sauces_and_chutneys=["dark soy sauce", "red chilli paste", "tomato ketchup", "vinegar"],
    cooking_methods=["Deep Fried", "Wok Tossed"],
    default_portion_unit="plate",
    default_unit_mass_g=230.0,
    density_g_cm3=0.82,
    nutrition_per_100g={"calories": 215.0, "protein_g": 3.4, "carbs_g": 24.5, "fat_g": 11.5, "fiber_g": 2.4, "sodium_mg": 620.0},
    uncertainty_factors=["cornstarch_batter_thickness", "deep_fry_oil_absorption"],
    oil_level_typical="High"
))


# =============================================================================
# 7. MOMOS & DUMPLINGS (Sections 45 - 46)
# =============================================================================

register_street_food_class(StreetFoodClassRecord(
    canonical_food_id="MOMO_CHICKEN_STEAMED",
    canonical_name="Steamed Chicken Momos",
    hierarchy=StreetFoodHierarchy(
        level3_food_family="Momos / Dumplings",
        level4_sub_family="Momo",
        level5_canonical_food="Steamed Momo",
        level6_variant="Thin Translucent Wheat Dough Pleated with Juicy Minced Chicken, Ginger & Onions",
        level7_cooking_method=["Steamed"],
        level8_portion_type="piece_count",
        level9_nutrition_ref_id="ifct_momo_chicken_steamed"
    ),
    food_family="Momos / Dumplings",
    sub_family="Momo",
    region="Northeast / Pan-India",
    state_or_city="Sikkim / Delhi / Pan-India",
    regional_names={"English": "Steamed Chicken Momo", "Hindi": "चिकन मोमोज़", "Nepali": "मम"},
    alternate_names=["chicken momos", "steamed momos", "dumplings", "delhi momos"],
    vegetarian=False,
    base_components=["thin pleated flour wrapper", "minced chicken with spring onion, ginger, garlic, cilantro and lard/oil for juiciness"],
    toppings=["coriander sprig"],
    sauces_and_chutneys=["fiery red tomato-garlic-dalle chilli chutney", "mayonnaise dollop (street style)"],
    cooking_methods=["Steamed"],
    default_portion_unit="piece",
    default_unit_mass_g=30.0,
    density_g_cm3=0.92,
    nutrition_per_100g={"calories": 165.0, "protein_g": 10.2, "carbs_g": 21.0, "fat_g": 4.5, "fiber_g": 1.1, "sodium_mg": 380.0},
    uncertainty_factors=["steamed_vs_fried_momo", "mayonnaise_dollop_mass", "chicken_fat_percentage"],
    oil_level_typical="Low"
))

register_street_food_class(StreetFoodClassRecord(
    canonical_food_id="MOMO_PORK_FRIED",
    canonical_name="Fried Pork Momos",
    hierarchy=StreetFoodHierarchy(
        level3_food_family="Momos / Dumplings",
        level4_sub_family="Momo",
        level5_canonical_food="Fried Momo",
        level6_variant="Crispy Golden Deep-Fried Pleated Dumplings Stuffed with Seasoned Minced Pork",
        level7_cooking_method=["Steamed then Deep Fried"],
        level8_portion_type="piece_count",
        level9_nutrition_ref_id="ifct_momo_pork_fried"
    ),
    food_family="Momos / Dumplings",
    sub_family="Momo",
    region="Northeast India",
    state_or_city="Sikkim / Meghalaya / Nagaland / Assam",
    regional_names={"English": "Fried Pork Momo", "Assamese": "পৰ্ক মমো", "Nepali": "फ्राइड मम"},
    alternate_names=["pork fried momo", "fried momos", "crispy momos"],
    vegetarian=False,
    base_components=["crispy fried flour dumpling shell", "minced fatty pork, ginger, scallions"],
    toppings=[],
    sauces_and_chutneys=["spicy bhoot jolokia / king chilli red chutney"],
    cooking_methods=["Deep Fried"],
    default_portion_unit="piece",
    default_unit_mass_g=32.0,
    density_g_cm3=0.88,
    nutrition_per_100g={"calories": 255.0, "protein_g": 11.5, "carbs_g": 22.0, "fat_g": 13.5, "fiber_g": 1.0, "sodium_mg": 410.0},
    uncertainty_factors=["deep_fry_oil", "pork_belly_fat_ratio"],
    oil_level_typical="High"
))


# =============================================================================
# 8. REGIONAL STREET FOODS (Sections 33 - 44)
# =============================================================================

# 8.1 South Indian Street Food (Sections 33 - 36)
register_street_food_class(StreetFoodClassRecord(
    canonical_food_id="SOUTH_STREET_KOTHU_PAROTTA_EGG",
    canonical_name="Madurai Egg Kothu Parotta",
    hierarchy=StreetFoodHierarchy(
        level3_food_family="South Indian Street Food",
        level4_sub_family="Kothu Parotta",
        level5_canonical_food="Kothu Parotta",
        level6_variant="Shredded Layered Parotta Minced on Cast Iron Tawa with Eggs, Spices & Salna",
        level7_cooking_method=["Tawa Shredded & Beaten / High Heat Stir-Fried"],
        level8_portion_type="plate",
        level9_nutrition_ref_id="ifct_south_kothu_parotta_egg"
    ),
    food_family="South Indian Street Food",
    sub_family="Kothu Parotta",
    region="South India",
    state_or_city="Tamil Nadu / Madurai / Chennai",
    regional_names={"English": "Egg Kothu Parotta", "Tamil": "முட்டை கொத்து பரோட்டா", "Malayalam": "മുട്ട കൊത്ത് പൊറോട്ട"},
    alternate_names=["kothu parotta", "kothu roti", "egg kothu", "madurai kothu parotta"],
    vegetarian=False,
    base_components=["flaky maida parotta shredded into small pieces (2 parottas)", "scrambled eggs (2 eggs)", "aromatic non-veg/veg salna (curry gravy)"],
    toppings=["chopped green chillies", "onions", "curry leaves", "coriander"],
    sauces_and_chutneys=["bowl of spicy chicken/mutton salna gravy", "onion raita"],
    cooking_methods=["Tawa Stir-Fried"],
    default_portion_unit="plate",
    default_unit_mass_g=320.0,
    density_g_cm3=0.88,
    nutrition_per_100g={"calories": 242.0, "protein_g": 8.8, "carbs_g": 26.5, "fat_g": 11.5, "fiber_g": 1.6, "sodium_mg": 520.0},
    uncertainty_factors=["parotta_count_1_vs_2_vs_3", "salna_oil_level", "egg_count"],
    oil_level_typical="High"
))

# 8.2 North Indian Street Food (Sections 37 - 39)
register_street_food_class(StreetFoodClassRecord(
    canonical_food_id="NORTH_STREET_CHOLE_BHATURE",
    canonical_name="Delhi Chole Bhature",
    hierarchy=StreetFoodHierarchy(
        level3_food_family="North Indian Street Food",
        level4_sub_family="Chole Bhature",
        level5_canonical_food="Chole Bhature",
        level6_variant="Puffed Deep-Fried Fermented Bhature with Dark Spicy Pindi Chole Curry",
        level7_cooking_method=["Deep Fried (Bhatura)", "Stewed (Chole)"],
        level8_portion_type="plate",
        level9_nutrition_ref_id="ifct_north_chole_bhature_delhi"
    ),
    food_family="North Indian Street Food",
    sub_family="Chole Bhature",
    region="North India",
    state_or_city="Delhi / Punjab",
    regional_names={"English": "Chole Bhature", "Hindi": "छोले भटूरे", "Punjabi": "ਛੋਲੇ ਭਟੂਰੇ"},
    alternate_names=["chole bhature", "chana bhatura", "delhi chole bhature", "pindi chole bhature"],
    vegetarian=True,
    base_components=["large puffed leavened flour bhature (2 pieces)", "dark spiced chickpea curry (chole simmered with tea leaves, anardana & amchoor)"],
    toppings=["sliced raw red onion rings", "pickled green chilli", "spiced carrot/amla pickle", "fresh coriander"],
    sauces_and_chutneys=["mint-coriander chutney"],
    cooking_methods=["Deep Fried", "Stewed"],
    default_portion_unit="plate",
    default_unit_mass_g=380.0,
    density_g_cm3=0.82,
    nutrition_per_100g={"calories": 235.0, "protein_g": 6.8, "carbs_g": 31.0, "fat_g": 9.5, "fiber_g": 3.8, "sodium_mg": 490.0},
    uncertainty_factors=["bhatura_diameter_15cm_vs_22cm", "bhatura_piece_count_1_vs_2", "oil_retention_in_bhatura"],
    oil_level_typical="High"
))

# 8.3 East Indian Street Food (Sections 42 - 44)
register_street_food_class(StreetFoodClassRecord(
    canonical_food_id="EAST_STREET_JHALMURI",
    canonical_name="Kolkata Jhalmuri",
    hierarchy=StreetFoodHierarchy(
        level3_food_family="East Indian Street Food",
        level4_sub_family="Jhalmuri",
        level5_canonical_food="Jhalmuri",
        level6_variant="Puffed Rice Tossed in Pungent Raw Mustard Oil, Bhaja Masala & Chanachur",
        level7_cooking_method=["Tossed / Assembled Raw"],
        level8_portion_type="bowl_weight_g",
        level9_nutrition_ref_id="ifct_east_jhalmuri_kolkata"
    ),
    food_family="East Indian Street Food",
    sub_family="Jhalmuri",
    region="East India",
    state_or_city="West Bengal / Kolkata",
    regional_names={"English": "Kolkata Jhalmuri", "Bengali": "ঝালমুড়ি", "Hindi": "झालमुड़ी", "Odia": "ଝାଲମୁଢ଼ି"},
    alternate_names=["jhalmuri", "jhal muri", "kolkata muri", "spicy puffed rice"],
    vegetarian=True,
    base_components=["crisp puffed rice (muri)", "spicy chanachur / mixture", "boiled potato cubes", "soaked/boiled brown chickpeas", "roasted peanuts"],
    toppings=["pungent raw mustard oil", "finely chopped raw red onion", "chopped green chillies", "fresh coconut slivers", "roasted bhaja cumin-coriander masala", "lemon juice"],
    sauces_and_chutneys=["raw cold-pressed mustard oil emulsion"],
    cooking_methods=["Assembled"],
    default_portion_unit="bowl",
    default_unit_mass_g=120.0,
    density_g_cm3=0.55,
    nutrition_per_100g={"calories": 240.0, "protein_g": 5.2, "carbs_g": 36.0, "fat_g": 8.5, "fiber_g": 2.8, "sodium_mg": 410.0},
    uncertainty_factors=["mustard_oil_tablespoons", "chanachur_fried_sev_ratio"],
    oil_level_typical="Medium"
))


# =============================================================================
# 9. STREET SWEETS (Sections 55 - 59)
# =============================================================================

register_street_food_class(StreetFoodClassRecord(
    canonical_food_id="SWEET_STREET_JALEBI",
    canonical_name="Street Crispy Hot Jalebi",
    hierarchy=StreetFoodHierarchy(
        level3_food_family="Sweets",
        level4_sub_family="Jalebi",
        level5_canonical_food="Jalebi",
        level6_variant="Fermented Flour Batter Swirled in Hot Oil & Soaked in Saffron-Cardamom Sugar Syrup",
        level7_cooking_method=["Deep Fried", "Syrup Soaked"],
        level8_portion_type="piece_count",
        level9_nutrition_ref_id="ifct_sweet_jalebi_crisp"
    ),
    food_family="Sweets",
    sub_family="Jalebi",
    region="Pan-India",
    state_or_city="Pan-India / North / West",
    regional_names={"English": "Jalebi", "Hindi": "जलेबी", "Gujarati": "જલેબી", "Bengali": "জিলিপি"},
    alternate_names=["jalebi", "crispy jalebi", "jilapi", "garam jalebi", "desi ghee jalebi"],
    vegetarian=True,
    base_components=["fermented all-purpose flour (maida) batter spirals", "concentrated sugar syrup with saffron, rose water & cardamom"],
    toppings=["pistachio slivers (occasional)"],
    sauces_and_chutneys=["sugar syrup glaze"],
    cooking_methods=["Deep Fried", "Syrup Soaked"],
    default_portion_unit="piece",
    default_unit_mass_g=30.0,
    density_g_cm3=1.12,
    nutrition_per_100g={"calories": 375.0, "protein_g": 2.1, "carbs_g": 72.0, "fat_g": 9.2, "fiber_g": 0.4, "sodium_mg": 95.0},
    uncertainty_factors=["piece_count", "syrup_absorption_weight", "thin_vs_thick_swirl"],
    oil_level_typical="High"
))

register_street_food_class(StreetFoodClassRecord(
    canonical_food_id="SWEET_STREET_KULFI_MALAI",
    canonical_name="Traditional Malai Matka Kulfi",
    hierarchy=StreetFoodHierarchy(
        level3_food_family="Sweets",
        level4_sub_family="Kulfi",
        level5_canonical_food="Kulfi",
        level6_variant="Slow-Simmered Dense Reduced Milk Frozen in Earthen Pot with Cardamom & Pistachios",
        level7_cooking_method=["Simmered / Reduced", "Frozen"],
        level8_portion_type="piece_count",
        level9_nutrition_ref_id="ifct_sweet_kulfi_malai"
    ),
    food_family="Sweets",
    sub_family="Kulfi",
    region="North / Pan-India",
    state_or_city="Delhi / Punjab / Rajasthan",
    regional_names={"English": "Malai Kulfi", "Hindi": "मलाई कुल्फी", "Punjabi": "ਮਲਾਈ ਕੁਲਫ਼ੀ"},
    alternate_names=["kulfi", "matka kulfi", "malai kulfi", "stick kulfi", "rabri kulfi"],
    vegetarian=True,
    base_components=["slow-reduced full-fat cow/buffalo milk (rabri)", "sugar", "crushed green cardamom"],
    toppings=["slivered almonds", "pistachios", "saffron strands"],
    sauces_and_chutneys=["rose syrup / falooda syrup drizzle (optional)"],
    cooking_methods=["Simmered", "Frozen"],
    default_portion_unit="piece",
    default_unit_mass_g=90.0,
    density_g_cm3=1.05,
    nutrition_per_100g={"calories": 248.0, "protein_g": 6.8, "carbs_g": 24.5, "fat_g": 14.0, "fiber_g": 0.2, "sodium_mg": 120.0},
    uncertainty_factors=["milk_fat_full_cream", "added_sugar", "stick_vs_matka_volume"],
    oil_level_typical="Low"
))

register_street_food_class(StreetFoodClassRecord(
    canonical_food_id="SWEET_STREET_FALOODA",
    canonical_name="Royal Rose Falooda",
    hierarchy=StreetFoodHierarchy(
        level3_food_family="Sweets",
        level4_sub_family="Falooda",
        level5_canonical_food="Falooda",
        level6_variant="Layered Cold Milk Dessert with Rose Syrup, Sabja Seeds, Vermicelli & Ice Cream",
        level7_cooking_method=["Assembled / Chilled"],
        level8_portion_type="volume_ml",
        level9_nutrition_ref_id="ifct_sweet_falooda_rose"
    ),
    food_family="Sweets",
    sub_family="Falooda",
    region="Pan-India",
    state_or_city="Mumbai / Delhi / Hyderabad",
    regional_names={"English": "Rose Falooda", "Hindi": "फालूदा", "Urdu": "فالودہ"},
    alternate_names=["falooda", "royal falooda", "rose falooda", "kulfi falooda"],
    vegetarian=True,
    base_components=["chilled full-fat milk", "cornstarch vermicelli (falooda sev)", "soaked sweet basil seeds (sabja)"],
    toppings=["scoop of vanilla or strawberry ice cream", "chopped pistachios and almonds", "tutti-frutti / jelly cubes"],
    sauces_and_chutneys=["concentrated rose syrup (Rooh Afza)"],
    cooking_methods=["Assembled"],
    default_portion_unit="cup",
    default_unit_mass_g=300.0,
    density_g_cm3=1.08,
    nutrition_per_100g={"calories": 160.0, "protein_g": 3.2, "carbs_g": 26.5, "fat_g": 4.8, "fiber_g": 1.2, "sodium_mg": 75.0},
    uncertainty_factors=["ice_cream_scoop_volume", "rose_syrup_sugar_concentration"],
    oil_level_typical="Low"
))


# =============================================================================
# 10. STREET BEVERAGES (Sections 60 - 63)
# =============================================================================

register_street_food_class(StreetFoodClassRecord(
    canonical_food_id="BEV_STREET_MASALA_CHAI_CUTTING",
    canonical_name="Mumbai Cutting Masala Chai",
    hierarchy=StreetFoodHierarchy(
        level3_food_family="Beverages",
        level4_sub_family="Tea",
        level5_canonical_food="Masala Chai",
        level6_variant="Strong Boiled CTC Black Tea with Milk, Sugar, Crushed Ginger & Green Cardamom",
        level7_cooking_method=["Boiled"],
        level8_portion_type="volume_ml",
        level9_nutrition_ref_id="ifct_bev_chai_cutting"
    ),
    food_family="Beverages",
    sub_family="Tea",
    region="Pan-India",
    state_or_city="Maharashtra / Pan-India",
    regional_names={"English": "Cutting Chai", "Hindi": "कटिंग चाय", "Marathi": "कटिंग चहा"},
    alternate_names=["chai", "cutting chai", "masala chai", "adrak chai", "tea"],
    vegetarian=True,
    base_components=["strong brewed CTC tea leaves", "boiled whole milk", "water"],
    toppings=["crushed fresh ginger", "crushed green cardamom pods", "clove/cinnamon pinch"],
    sauces_and_chutneys=[],
    cooking_methods=["Boiled"],
    default_portion_unit="cup",
    default_unit_mass_g=100.0,  # 100 ml ~ 103g
    density_g_cm3=1.03,
    nutrition_per_100g={"calories": 78.0, "protein_g": 2.2, "carbs_g": 10.5, "fat_g": 3.0, "fiber_g": 0.0, "sodium_mg": 45.0},
    uncertainty_factors=["sugar_spoons_undetectable_by_vision", "buffalo_vs_toned_milk"],
    oil_level_typical="Low"
))

register_street_food_class(StreetFoodClassRecord(
    canonical_food_id="BEV_STREET_SUGARCANE_JUICE",
    canonical_name="Street Fresh Sugarcane Juice with Ginger & Mint",
    hierarchy=StreetFoodHierarchy(
        level3_food_family="Beverages",
        level4_sub_family="Sugarcane Juice",
        level5_canonical_food="Sugarcane Juice",
        level6_variant="Freshly Cold-Pressed Cane Stalks Crushed with Ginger, Fresh Mint & Lime",
        level7_cooking_method=["Cold Pressed"],
        level8_portion_type="volume_ml",
        level9_nutrition_ref_id="ifct_bev_sugarcane_fresh"
    ),
    food_family="Beverages",
    sub_family="Sugarcane Juice",
    region="Pan-India",
    state_or_city="Pan-India",
    regional_names={"English": "Sugarcane Juice", "Hindi": "गन्ने का रस", "Marathi": "उसाचा रस", "Tamil": "கரும்பு சாறு"},
    alternate_names=["ganne ka ras", "sugarcane juice", "cane juice", "usacha ras"],
    vegetarian=True,
    base_components=["raw sugarcane juice", "crushed ice (optional)"],
    toppings=["fresh mint leaves", "fresh ginger juice", "lemon squeeze", "pinch of black salt"],
    sauces_and_chutneys=[],
    cooking_methods=["Cold Pressed"],
    default_portion_unit="cup",
    default_unit_mass_g=250.0,
    density_g_cm3=1.06,
    nutrition_per_100g={"calories": 68.0, "protein_g": 0.3, "carbs_g": 17.2, "fat_g": 0.1, "fiber_g": 0.0, "sodium_mg": 28.0},
    uncertainty_factors=["ice_dilution_percentage", "cane_sweetness_brix"],
    oil_level_typical="Low"
))

register_street_food_class(StreetFoodClassRecord(
    canonical_food_id="BEV_STREET_LASSI_SWEET",
    canonical_name="Amritsari Sweet Lassi with Malai",
    hierarchy=StreetFoodHierarchy(
        level3_food_family="Beverages",
        level4_sub_family="Lassi",
        level5_canonical_food="Sweet Lassi",
        level6_variant="Thick Churned Sweetened Curd Served in Clay Kulhad with Floating Malai Clot",
        level7_cooking_method=["Churned / Whipped"],
        level8_portion_type="volume_ml",
        level9_nutrition_ref_id="ifct_bev_lassi_sweet"
    ),
    food_family="Beverages",
    sub_family="Lassi",
    region="North India",
    state_or_city="Punjab / Amritsar / Delhi",
    regional_names={"English": "Sweet Lassi", "Hindi": "मीठी लस्सी", "Punjabi": "ਮਿੱਠੀ ਲੱਸੀ"},
    alternate_names=["lassi", "sweet lassi", "punjabi lassi", "malai lassi", "amritsari lassi"],
    vegetarian=True,
    base_components=["thick whole milk curd (dahi)", "sugar", "chilled water / ice"],
    toppings=["thick clotted cream (malai top)", "slivered pistachios and almonds", "cardamom powder", "rose water drop"],
    sauces_and_chutneys=[],
    cooking_methods=["Whisked"],
    default_portion_unit="cup",
    default_unit_mass_g=300.0,
    density_g_cm3=1.07,
    nutrition_per_100g={"calories": 115.0, "protein_g": 3.4, "carbs_g": 16.0, "fat_g": 4.2, "fiber_g": 0.1, "sodium_mg": 55.0},
    uncertainty_factors=["sugar_quantity", "malai_clot_mass", "curd_fat"],
    oil_level_typical="Low"
))


# =============================================================================
# 11. UNKNOWN STREET FOOD FALLBACK (Section 90 & 98)
# =============================================================================

register_street_food_class(StreetFoodClassRecord(
    canonical_food_id="STREET_UNKNOWN",
    canonical_name="Unknown Street Food",
    hierarchy=StreetFoodHierarchy(
        level3_food_family="Regional Specialities",
        level4_sub_family="Unknown",
        level5_canonical_food="Unknown Street Food",
        level6_variant="Unverified Street Food Preparation (Low Visual Evidence)",
        level7_cooking_method=["Unknown"],
        level8_portion_type="unit_weight_g",
        level9_nutrition_ref_id="ifct_unknown"
    ),
    food_family="Regional Specialities",
    sub_family="Unknown",
    region="Pan-India",
    state_or_city="Unknown",
    regional_names={"English": "Unknown Street Food", "Hindi": "अज्ञात स्ट्रीट फ़ूड"},
    alternate_names=["unknown", "unidentified street food", "unknown food"],
    vegetarian=True,
    base_components=[],
    toppings=[],
    sauces_and_chutneys=[],
    cooking_methods=["Unknown"],
    default_portion_unit="plate",
    default_unit_mass_g=150.0,
    density_g_cm3=0.80,
    nutrition_per_100g={"calories": 200.0, "protein_g": 5.0, "carbs_g": 25.0, "fat_g": 8.0, "fiber_g": 2.0, "sodium_mg": 400.0},
    uncertainty_factors=["unidentified_food_type", "insufficient_visual_evidence"],
    oil_level_typical="Unknown"
))


# =============================================================================
# LOOKUP & HELPER UTILITIES
# =============================================================================

def get_street_food_class(canonical_id: str) -> Optional[StreetFoodClassRecord]:
    """Retrieve record by canonical ID."""
    return STREET_FOOD_TAXONOMY_REGISTRY.get(canonical_id)


def resolve_street_food_by_name(query: str) -> Optional[StreetFoodClassRecord]:
    """
    Resolves any query string (canonical name, English alias, Hindi/regional name)
    into the canonical StreetFoodClassRecord. Returns None if unmapped.
    """
    if not query:
        return None
    q = query.lower().strip()
    if q in STREET_SYNONYM_LOOKUP:
        return STREET_FOOD_TAXONOMY_REGISTRY.get(STREET_SYNONYM_LOOKUP[q])
    for alt, cid in STREET_SYNONYM_LOOKUP.items():
        if alt in q or q in alt:
            return STREET_FOOD_TAXONOMY_REGISTRY.get(cid)
    return None


def filter_street_foods_by_family(food_family: str) -> List[StreetFoodClassRecord]:
    """Returns all registered street foods in a given food family."""
    fam = food_family.lower().strip()
    return [
        rec for rec in STREET_FOOD_TAXONOMY_REGISTRY.values()
        if rec.food_family.lower() == fam or fam in rec.hierarchy.level3_food_family.lower()
    ]
