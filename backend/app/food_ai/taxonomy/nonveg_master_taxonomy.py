"""
Indian Non-Vegetarian Master Taxonomy & Identity Hierarchy (Part 13)
Implements Sections 1–4, 9, 10, 13, 16–21, 25, 27, 45–54, 61, 65, 66, 88, 89 of Part 13 Specification.

Guarantees:
- Strict 12-Level Identity Traversal:
  Protein -> Region -> State -> Food Family -> Specific Dish -> Variant ->
  Cooking Method -> Bone State -> Piece Count -> Portion -> Weight -> Nutrition
- Stable Class ID System (Section 66): IND-NV-* format.
- 79 Primary Non-Veg Families (Section 3).
- Comprehensive Protein Datasets:
  * Chicken: Chettinad, Butter Chicken, 65, Tikka, Ghee Roast, Korma, Tandoori, Kebab, Biryani, Sukka, Curry, etc.
  * Mutton/Goat/Lamb: Rogan Josh, Kosha Mangsho, Chukka, Sukka, Keema, Seekh Kebab, Biryani, Curry, etc.
  * Fish: Kerala Meen Curry, Karimeen Pollichathu, Fish Moilee, Macher Jhol, Shorshe Ilish, Goan Fish Curry, Amritsari, etc.
  * Seafood: Prawn Curry/Roast/Balchao/Malai, Crab Masala/Fry, Squid Fry/Roast, Shellfish/Clams.
  * Egg: Boiled, Half-boiled, Masala Omelette, Bhurji, Egg Curry, Egg Roast, Egg Biryani.
  * Regional Specialties: Pork (Goa Vindaloo, Naga Bamboo Shoot), Beef/Buffalo (Kerala Ularthiyathu, Curry).
- Robust Fallback System (Section 61 & 83):
  * "Indian non-vegetarian dish — exact identity uncertain" (IND-NV-UNKNOWN-001)
  * "Chicken-based dish — exact recipe uncertain" (IND-NV-CH-UNKNOWN-001)
  * "Mutton/goat-style meat dish — exact species uncertain" (IND-NV-MT-UNKNOWN-001)
  * "Fish curry/fry — species uncertain" (IND-NV-FS-UNKNOWN-001)
  * "Seafood dish — exact type uncertain" (IND-NV-SF-UNKNOWN-001)
  * "Egg preparation — exact variant uncertain" (IND-NV-EG-UNKNOWN-001)
  * "Red meat dish — exact species uncertain" (IND-NV-RM-UNKNOWN-001)
- Multilingual synonym mappings across 12 Indian languages (Section 65).
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class NonVegHierarchy(BaseModel):
    level1_food: str = "Indian Food"
    level2_macro_category: str = "Non-Vegetarian Food"
    level3_protein: str         # Chicken, Mutton/Goat/Lamb, Fish, Seafood, Egg, Regional Pork, Regional Beef, Mixed Non-Veg
    level4_region: str          # South India, North India, West India, East India, Northeast India, Pan-India
    level5_state: str           # Tamil Nadu, Kerala, Karnataka, Andhra/Telangana, Punjab, Delhi, Bengal, Goa, etc.
    level6_food_family: str     # Chicken Curry, Chicken Fry, Tandoori, Biryani, Mutton Curry, Fish Fry, Prawn Masala, etc.
    level7_specific_dish: str   # Chicken Chettinad, Butter Chicken, Fish Moilee, Prawn Roast, Rogan Josh, etc.
    level8_variant: str         # e.g., "Bone-in country chicken slow simmered in stone-ground roasted coconut and black pepper"
    level9_cooking_method: str  # Stewed, Simmered, Deep-fried, Tawa-fried, Grilled, Tandoor-roasted, Pan-roasted, Boiled, Steamed
    level10_bone_state: str     # bone_in, boneless, mixed, bone_visible, bone_not_visible, unknown
    level11_portion_type: str   # weight_grams, piece_count, volume_ml
    level12_nutrition_ref_id: str


class NonVegFoodClassRecord(BaseModel):
    canonical_food_id: str      # Stable ID: IND-NV-CH-TN-CHE-001, etc.
    canonical_name: str         # Canonical English name
    hierarchy: NonVegHierarchy
    protein_type: str           # Chicken, Mutton, Goat, Fish, Prawn, Crab, Squid, Seafood, Egg, Pork, Beef
    food_family: str            # High-level family from Section 3
    specific_dish: str
    region: str                 # South India, North India, West India, East India, Northeast India, Pan-India
    state_or_city: str
    regional_names: Dict[str, str] = Field(default_factory=dict)
    alternate_names: List[str] = Field(default_factory=list)
    cooking_method: str = "Simmered"
    bone_state_default: str = "bone_in"  # bone_in, boneless, mixed, unknown
    typical_cut: str = "curry_cut"       # drumstick, wing, breast, thigh, steak, cube, whole, mince, sliced
    consistency: str = "Thick gravy"     # Dry, Semi-dry, Thick gravy, Thin gravy, Soup/stew, Roasted, Fried
    gravy_base: List[str] = Field(default_factory=list) # tomato, onion, coconut, coconut_milk, yogurt, mustard, pepper
    is_countable: bool = False
    piece_count_expected: Optional[int] = None
    default_portion_grams: float = 160.0
    edible_meat_ratio: float = 0.72      # e.g. 0.72 for bone-in chicken (28% bone weight deduction)
    density_g_ml: float = 1.05
    nutrition_per_100g: Dict[str, float] = Field(default_factory=dict)
    uncertainty_factors: List[str] = Field(default_factory=list)
    typical_oil_level: str = "Moderate visible oil" # Low, Moderate, High, Excess oil pooling, Ghee roast, Dry char


NONVEG_TAXONOMY_REGISTRY: Dict[str, NonVegFoodClassRecord] = {}
NONVEG_SYNONYM_LOOKUP: Dict[str, str] = {}


def register_nonveg_food_class(record: NonVegFoodClassRecord, alias_ids: Optional[List[str]] = None) -> NonVegFoodClassRecord:
    NONVEG_TAXONOMY_REGISTRY[record.canonical_food_id] = record
    NONVEG_TAXONOMY_REGISTRY[record.canonical_food_id.lower()] = record
    if alias_ids:
        for aid in alias_ids:
            NONVEG_TAXONOMY_REGISTRY[aid] = record
            NONVEG_TAXONOMY_REGISTRY[aid.lower()] = record
            NONVEG_SYNONYM_LOOKUP[aid.lower().strip()] = record.canonical_food_id
    NONVEG_SYNONYM_LOOKUP[record.canonical_name.lower().strip()] = record.canonical_food_id
    for alt in record.alternate_names:
        NONVEG_SYNONYM_LOOKUP[alt.lower().strip()] = record.canonical_food_id
    for reg_name in record.regional_names.values():
        NONVEG_SYNONYM_LOOKUP[reg_name.lower().strip()] = record.canonical_food_id
    return record


# =============================================================================
# 1. CHICKEN MASTER DATASET (Sections 3, 4, 5, 6, 7, 8, 9)
# =============================================================================

# Chicken Chettinad (Tamil Nadu)
register_nonveg_food_class(
    NonVegFoodClassRecord(
        canonical_food_id="IND-NV-CH-TN-CHE-001",
        canonical_name="Chicken Chettinad",
        hierarchy=NonVegHierarchy(
            level3_protein="Chicken",
            level4_region="South India",
            level5_state="Tamil Nadu",
            level6_food_family="Chicken Chettinad",
            level7_specific_dish="Chicken Chettinad",
            level8_variant="Bone-in chicken simmered in freshly roasted Chettinad spices, fennel, poppy seeds and coconut",
            level9_cooking_method="Simmered",
            level10_bone_state="bone_in",
            level11_portion_type="weight_grams",
            level12_nutrition_ref_id="REF-NV-CH-TN-CHE-001"
        ),
        protein_type="Chicken",
        food_family="Chicken Chettinad",
        specific_dish="Chicken Chettinad",
        region="South India",
        state_or_city="Tamil Nadu",
        regional_names={
            "ta": "செட்டிநாடு சிக்கன் / கோழி வறுவல்",
            "te": "చెట్టినాడు చికెన్",
            "kn": "ಚೆಟ್ಟಿನಾಡ್ ಚಿಕನ್",
            "ml": "ചെട്ടിനാട് ചിക്കൻ",
            "hi": "चेट्टिनाड चिकन"
        },
        alternate_names=["chettinad chicken", "chettinad koli kuzhambu", "chettinad chicken curry", "cheti koli"],
        cooking_method="Simmered",
        bone_state_default="bone_in",
        typical_cut="curry_cut",
        consistency="Thick gravy",
        gravy_base=["onion", "tomato", "coconut", "pepper"],
        is_countable=True,
        piece_count_expected=5,
        default_portion_grams=180.0,
        edible_meat_ratio=0.72,
        nutrition_per_100g={"calories": 182.0, "protein": 17.5, "carbs": 4.5, "fat": 10.8, "fiber": 1.4},
        uncertainty_factors=["bone_weight_deduction", "coconut_paste_quantity", "oil_layer"],
        typical_oil_level="High visible oil"
    ),
    alias_ids=["IND-NV-CH-CHETTINAD", "IND-CH-CHETTINAD-001"]
)

# Chicken 65 (South India / Pan-India)
register_nonveg_food_class(
    NonVegFoodClassRecord(
        canonical_food_id="IND-NV-CH-PAN-65-001",
        canonical_name="Chicken 65",
        hierarchy=NonVegHierarchy(
            level3_protein="Chicken",
            level4_region="Pan-India",
            level5_state="Tamil Nadu / Telangana",
            level6_food_family="Chicken 65",
            level7_specific_dish="Chicken 65",
            level8_variant="Deep-fried crisp chicken morsels tempered with fresh curry leaves, green chillies and garlic yogurt glaze",
            level9_cooking_method="Deep-fried",
            level10_bone_state="boneless",
            level11_portion_type="piece_count",
            level12_nutrition_ref_id="REF-NV-CH-PAN-65-001"
        ),
        protein_type="Chicken",
        food_family="Chicken 65",
        specific_dish="Chicken 65",
        region="Pan-India",
        state_or_city="Chennai / Hyderabad",
        regional_names={
            "ta": "சிக்கன் 65",
            "te": "చికెన్ 65",
            "hi": "चिकन 65",
            "ml": "ചിക്കൻ 65",
            "kn": "ಚಿಕನ್ 65"
        },
        alternate_names=["chicken 65", "restaurant chicken 65", "spicy chicken 65", "boneless chicken 65"],
        cooking_method="Deep-fried",
        bone_state_default="boneless",
        typical_cut="boneless_chunks",
        consistency="Dry",
        gravy_base=[],
        is_countable=True,
        piece_count_expected=8,
        default_portion_grams=150.0,
        edible_meat_ratio=1.0,
        nutrition_per_100g={"calories": 255.0, "protein": 22.0, "carbs": 8.5, "fat": 15.0, "fiber": 0.8},
        uncertainty_factors=["deep_fry_oil_absorption", "cornstarch_coating_thickness"],
        typical_oil_level="High visible oil"
    ),
    alias_ids=["IND-NV-CH-65", "IND-CH-65-001"]
)

# Butter Chicken / Murgh Makhani (North India)
register_nonveg_food_class(
    NonVegFoodClassRecord(
        canonical_food_id="IND-NV-CH-PB-BUTTER-001",
        canonical_name="Butter Chicken (Murgh Makhani)",
        hierarchy=NonVegHierarchy(
            level3_protein="Chicken",
            level4_region="North India",
            level5_state="Punjab / Delhi",
            level6_food_family="Butter Chicken",
            level7_specific_dish="Butter Chicken",
            level8_variant="Tandoor-grilled chicken tikka pieces simmered in silky buttery tomato-cashew cream gravy with dried fenugreek",
            level9_cooking_method="Simmered",
            level10_bone_state="boneless",
            level11_portion_type="weight_grams",
            level12_nutrition_ref_id="REF-NV-CH-PB-BUTTER-001"
        ),
        protein_type="Chicken",
        food_family="Butter Chicken",
        specific_dish="Butter Chicken",
        region="North India",
        state_or_city="Delhi / Punjab",
        regional_names={
            "hi": "बटर चिकन / मुर्ग मखनी",
            "pa": "ਮੱਖਣ ਚਿਕਨ",
            "ur": "بٹر چکن",
            "ta": "பட்டர் சிக்கன்"
        },
        alternate_names=["butter chicken", "murgh makhani", "chicken makhani", "delhi butter chicken"],
        cooking_method="Simmered",
        bone_state_default="boneless",
        typical_cut="boneless_chunks",
        consistency="Thick gravy",
        gravy_base=["tomato", "cream", "cashew", "butter"],
        is_countable=True,
        piece_count_expected=6,
        default_portion_grams=200.0,
        edible_meat_ratio=1.0,
        nutrition_per_100g={"calories": 230.0, "protein": 14.5, "carbs": 6.8, "fat": 16.5, "fiber": 0.9},
        uncertainty_factors=["butter_quantity", "heavy_cream_ratio", "cashew_paste_density"],
        typical_oil_level="High visible oil"
    ),
    alias_ids=["IND-NV-CH-BUTTER-CHICKEN", "IND-CH-MURGH-MAKHANI"]
)

# Chicken Tikka Masala (North India / Pan-India)
register_nonveg_food_class(
    NonVegFoodClassRecord(
        canonical_food_id="IND-NV-CH-NI-TIKKAMASALA-001",
        canonical_name="Chicken Tikka Masala",
        hierarchy=NonVegHierarchy(
            level3_protein="Chicken",
            level4_region="North India",
            level5_state="Punjab / Delhi",
            level6_food_family="Chicken Tikka Masala",
            level7_specific_dish="Chicken Tikka Masala",
            level8_variant="Charred spiced chicken breast chunks folded in an onion-tomato spiced masala with capsicum",
            level9_cooking_method="Simmered",
            level10_bone_state="boneless",
            level11_portion_type="weight_grams",
            level12_nutrition_ref_id="REF-NV-CH-NI-TIKKAMASALA-001"
        ),
        protein_type="Chicken",
        food_family="Chicken Tikka Masala",
        specific_dish="Chicken Tikka Masala",
        region="North India",
        state_or_city="Delhi / Punjab",
        regional_names={"hi": "चिकन टिक्का मसाला", "ta": "சிக்கன் டிக்கா மசாலா"},
        alternate_names=["chicken tikka masala", "murgh tikka masala", "ctm"],
        cooking_method="Simmered",
        bone_state_default="boneless",
        typical_cut="boneless_chunks",
        consistency="Thick gravy",
        gravy_base=["tomato", "onion", "cream"],
        is_countable=True,
        piece_count_expected=6,
        default_portion_grams=200.0,
        edible_meat_ratio=1.0,
        nutrition_per_100g={"calories": 195.0, "protein": 16.2, "carbs": 6.0, "fat": 11.8, "fiber": 1.1},
        uncertainty_factors=["cream_level", "charred_tikka_oil"],
        typical_oil_level="Moderate visible oil"
    ),
    alias_ids=["IND-NV-CH-TIKKA-MASALA"]
)

# Tandoori Chicken (North India / Pan-India)
register_nonveg_food_class(
    NonVegFoodClassRecord(
        canonical_food_id="IND-NV-CH-PB-TANDOORI-001",
        canonical_name="Tandoori Chicken",
        hierarchy=NonVegHierarchy(
            level3_protein="Chicken",
            level4_region="North India",
            level5_state="Punjab",
            level6_food_family="Tandoori Chicken",
            level7_specific_dish="Tandoori Chicken",
            level8_variant="Bone-in chicken whole legs marinated in hung curd, Kashmiri red chilli and mustard oil roasted in clay tandoor",
            level9_cooking_method="Tandoor-roasted",
            level10_bone_state="bone_in",
            level11_portion_type="piece_count",
            level12_nutrition_ref_id="REF-NV-CH-PB-TANDOORI-001"
        ),
        protein_type="Chicken",
        food_family="Tandoori Chicken",
        specific_dish="Tandoori Chicken",
        region="North India",
        state_or_city="Punjab",
        regional_names={"hi": "तंदूरी चिकन", "pa": "ਤੰਦੂਰੀ ਚਿਕਨ", "ta": "தந்தூரி சிக்கன்"},
        alternate_names=["tandoori chicken", "tandoori leg", "tandoori murgh", "charcoal roasted chicken"],
        cooking_method="Tandoor-roasted",
        bone_state_default="bone_in",
        typical_cut="drumstick",
        consistency="Dry",
        gravy_base=[],
        is_countable=True,
        piece_count_expected=2,
        default_portion_grams=220.0,
        edible_meat_ratio=0.68,
        nutrition_per_100g={"calories": 190.0, "protein": 24.5, "carbs": 2.2, "fat": 9.2, "fiber": 0.4},
        uncertainty_factors=["bone_weight_deduction", "skin_presence", "basting_butter"],
        typical_oil_level="Moderate visible oil"
    ),
    alias_ids=["IND-NV-CH-TANDOORI", "IND-CH-TANDOORI-001"]
)

# Chicken Tikka Kebab (North India)
register_nonveg_food_class(
    NonVegFoodClassRecord(
        canonical_food_id="IND-NV-CH-DEL-TIKKA-001",
        canonical_name="Chicken Tikka",
        hierarchy=NonVegHierarchy(
            level3_protein="Chicken",
            level4_region="North India",
            level5_state="Delhi",
            level6_food_family="Chicken Tikka",
            level7_specific_dish="Chicken Tikka",
            level8_variant="Skewered boneless spiced chicken cubes char-grilled with mint and lemon glaze",
            level9_cooking_method="Grilled",
            level10_bone_state="boneless",
            level11_portion_type="piece_count",
            level12_nutrition_ref_id="REF-NV-CH-DEL-TIKKA-001"
        ),
        protein_type="Chicken",
        food_family="Chicken Tikka",
        specific_dish="Chicken Tikka",
        region="North India",
        state_or_city="Delhi",
        regional_names={"hi": "चिकन टिक्का", "ta": "சிக்கன் டிக்கா"},
        alternate_names=["chicken tikka", "murgh tikka", "tandoori tikka"],
        cooking_method="Grilled",
        bone_state_default="boneless",
        typical_cut="boneless_chunks",
        consistency="Dry",
        gravy_base=[],
        is_countable=True,
        piece_count_expected=6,
        default_portion_grams=160.0,
        edible_meat_ratio=1.0,
        nutrition_per_100g={"calories": 185.0, "protein": 26.0, "carbs": 3.0, "fat": 7.5, "fiber": 0.4},
        uncertainty_factors=["butter_basting", "char_crust"],
        typical_oil_level="Moderate visible oil"
    ),
    alias_ids=["IND-NV-CH-TIKKA"]
)

# Chicken Ghee Roast (Karnataka - Mangalore)
register_nonveg_food_class(
    NonVegFoodClassRecord(
        canonical_food_id="IND-NV-CH-KA-GHEEROAST-001",
        canonical_name="Chicken Ghee Roast",
        hierarchy=NonVegHierarchy(
            level3_protein="Chicken",
            level4_region="South India",
            level5_state="Karnataka",
            level6_food_family="Chicken Ghee Roast",
            level7_specific_dish="Chicken Ghee Roast",
            level8_variant="Kundapur style chicken pan-roasted in generous aromatic desi ghee with Byadgi chilli and tamarind paste",
            level9_cooking_method="Pan-roasted",
            level10_bone_state="bone_in",
            level11_portion_type="weight_grams",
            level12_nutrition_ref_id="REF-NV-CH-KA-GHEEROAST-001"
        ),
        protein_type="Chicken",
        food_family="Chicken Ghee Roast",
        specific_dish="Chicken Ghee Roast",
        region="South India",
        state_or_city="Mangalore / Coastal Karnataka",
        regional_names={"kn": "ಕೋಳಿ ತುಪ್ಪ ರೋಸ್ಟ್ / ಚಿಕನ್ ತುಪ್ಪ ರೋಸ್ಟ್", "ta": "சிக்கன் நெய் ரோஸ்ட்", "hi": "चिकन घी रोस्ट"},
        alternate_names=["chicken ghee roast", "mangalore chicken ghee roast", "kori ghee roast"],
        cooking_method="Pan-roasted",
        bone_state_default="bone_in",
        typical_cut="curry_cut",
        consistency="Semi-dry",
        gravy_base=["ghee", "byadgi_chilli", "tamarind"],
        is_countable=True,
        piece_count_expected=5,
        default_portion_grams=180.0,
        edible_meat_ratio=0.72,
        nutrition_per_100g={"calories": 265.0, "protein": 18.0, "carbs": 4.2, "fat": 20.0, "fiber": 0.8},
        uncertainty_factors=["ghee_level", "bone_weight_deduction"],
        typical_oil_level="Ghee roast visible ghee"
    ),
    alias_ids=["IND-NV-CH-GHEEROAST", "IND-CH-KA-GHEEROAST"]
)

# Chicken Chukka / Varuval (Tamil Nadu)
register_nonveg_food_class(
    NonVegFoodClassRecord(
        canonical_food_id="IND-NV-CH-TN-CHUKKA-001",
        canonical_name="Chicken Chukka (Varuval)",
        hierarchy=NonVegHierarchy(
            level3_protein="Chicken",
            level4_region="South India",
            level5_state="Tamil Nadu",
            level6_food_family="Chicken Chukka",
            level7_specific_dish="Chicken Chukka",
            level8_variant="Dry roasted chicken pieces with caramelized shallots, curry leaves, crushed black pepper and fennel",
            level9_cooking_method="Pan-roasted",
            level10_bone_state="bone_in",
            level11_portion_type="weight_grams",
            level12_nutrition_ref_id="REF-NV-CH-TN-CHUKKA-001"
        ),
        protein_type="Chicken",
        food_family="Chicken Chukka",
        specific_dish="Chicken Chukka",
        region="South India",
        state_or_city="Madurai / Tamil Nadu",
        regional_names={"ta": "சிக்கன் சுக்கா / கோழி வறுவல்", "te": "చికెన్ చుక్కా", "hi": "चिकन चुक्का"},
        alternate_names=["chicken chukka", "chicken varuval", "madurai chicken chukka", "chicken sukka"],
        cooking_method="Pan-roasted",
        bone_state_default="bone_in",
        typical_cut="curry_cut",
        consistency="Dry",
        gravy_base=["shallots", "pepper", "curry_leaves"],
        is_countable=True,
        piece_count_expected=6,
        default_portion_grams=160.0,
        edible_meat_ratio=0.72,
        nutrition_per_100g={"calories": 210.0, "protein": 21.0, "carbs": 3.8, "fat": 12.2, "fiber": 1.0},
        uncertainty_factors=["bone_weight_deduction", "shallots_caramelization_oil"],
        typical_oil_level="High visible oil"
    ),
    alias_ids=["IND-NV-CH-CHUKKA", "IND-CH-VARUVAL-001"]
)

# Kerala Chicken Roast (Kerala)
register_nonveg_food_class(
    NonVegFoodClassRecord(
        canonical_food_id="IND-NV-CH-KL-ROAST-001",
        canonical_name="Kerala Chicken Roast",
        hierarchy=NonVegHierarchy(
            level3_protein="Chicken",
            level4_region="South India",
            level5_state="Kerala",
            level6_food_family="Chicken Roast",
            level7_specific_dish="Kerala Chicken Roast",
            level8_variant="Shallow fried chicken braised in a dark caramelized onion, tomato, coconut slice and pepper masala",
            level9_cooking_method="Pan-roasted",
            level10_bone_state="bone_in",
            level11_portion_type="weight_grams",
            level12_nutrition_ref_id="REF-NV-CH-KL-ROAST-001"
        ),
        protein_type="Chicken",
        food_family="Chicken Roast",
        specific_dish="Kerala Chicken Roast",
        region="South India",
        state_or_city="Kerala",
        regional_names={"ml": "കേരള ചിക്കൻ റോസ്റ്റ്", "ta": "கேரளா சிக்கன் ரோஸ்ட்", "hi": "केरल चिकन रोस्ट"},
        alternate_names=["kerala chicken roast", "nadan chicken roast", "chicken peralan"],
        cooking_method="Pan-roasted",
        bone_state_default="bone_in",
        typical_cut="curry_cut",
        consistency="Semi-dry",
        gravy_base=["onion", "coconut_slices", "tomato", "pepper"],
        is_countable=True,
        piece_count_expected=5,
        default_portion_grams=180.0,
        edible_meat_ratio=0.72,
        nutrition_per_100g={"calories": 215.0, "protein": 19.5, "carbs": 5.0, "fat": 13.0, "fiber": 1.1},
        uncertainty_factors=["coconut_oil_quantity", "fried_chicken_fat"],
        typical_oil_level="High visible oil"
    ),
    alias_ids=["IND-NV-CH-KL-ROAST"]
)

# Andhra Kodi Kura (Andhra / Telangana)
register_nonveg_food_class(
    NonVegFoodClassRecord(
        canonical_food_id="IND-NV-CH-AP-KODI-001",
        canonical_name="Andhra Chicken Curry (Kodi Kura)",
        hierarchy=NonVegHierarchy(
            level3_protein="Chicken",
            level4_region="South India",
            level5_state="Andhra Pradesh / Telangana",
            level6_food_family="Chicken Curry",
            level7_specific_dish="Andhra Kodi Kura",
            level8_variant="Fiery country chicken simmered in poppy seeds, coriander, guntur chillies and ginger-garlic broth",
            level9_cooking_method="Simmered",
            level10_bone_state="bone_in",
            level11_portion_type="weight_grams",
            level12_nutrition_ref_id="REF-NV-CH-AP-KODI-001"
        ),
        protein_type="Chicken",
        food_family="Chicken Curry",
        specific_dish="Andhra Kodi Kura",
        region="South India",
        state_or_city="Andhra Pradesh",
        regional_names={"te": "కోడి కూర / ఆంధ్రా చికెన్ కర్రీ", "ta": "ஆந்திரா கோழி குழம்பு", "hi": "आंध्रा चिकन करी"},
        alternate_names=["andhra chicken curry", "kodi kura", "guntur chicken curry", "telangana chicken curry"],
        cooking_method="Simmered",
        bone_state_default="bone_in",
        typical_cut="curry_cut",
        consistency="Thick gravy",
        gravy_base=["onion", "guntur_chilli", "poppy_seeds", "tomato"],
        is_countable=True,
        piece_count_expected=5,
        default_portion_grams=190.0,
        edible_meat_ratio=0.72,
        nutrition_per_100g={"calories": 178.0, "protein": 17.8, "carbs": 3.8, "fat": 10.4, "fiber": 1.2},
        uncertainty_factors=["bone_weight_deduction", "chilli_oil_layer"],
        typical_oil_level="High visible oil"
    ),
    alias_ids=["IND-NV-CH-KODIKURA"]
)

# Bengali Murgir Jhol (West Bengal)
register_nonveg_food_class(
    NonVegFoodClassRecord(
        canonical_food_id="IND-NV-CH-WB-JHOL-001",
        canonical_name="Bengali Chicken Curry (Murgir Jhol)",
        hierarchy=NonVegHierarchy(
            level3_protein="Chicken",
            level4_region="East India",
            level5_state="West Bengal",
            level6_food_family="Chicken Curry",
            level7_specific_dish="Bengali Murgir Jhol",
            level8_variant="Light homestyle chicken curry cooked with large halved potatoes, ginger-cumin paste and mustard oil",
            level9_cooking_method="Simmered",
            level10_bone_state="bone_in",
            level11_portion_type="weight_grams",
            level12_nutrition_ref_id="REF-NV-CH-WB-JHOL-001"
        ),
        protein_type="Chicken",
        food_family="Chicken Curry",
        specific_dish="Bengali Murgir Jhol",
        region="East India",
        state_or_city="West Bengal",
        regional_names={"bn": "মুরগির লাল ঝোল", "hi": "बंगाली मुर्गी झोल"},
        alternate_names=["bengali chicken curry", "murgir jhol", "murgir lal jhol", "chicken potato jhol"],
        cooking_method="Simmered",
        bone_state_default="bone_in",
        typical_cut="curry_cut",
        consistency="Thin gravy",
        gravy_base=["onion", "ginger_cumin", "mustard_oil", "potato"],
        is_countable=True,
        piece_count_expected=4,
        default_portion_grams=210.0,
        edible_meat_ratio=0.72,
        nutrition_per_100g={"calories": 145.0, "protein": 13.5, "carbs": 5.8, "fat": 7.5, "fiber": 0.8},
        uncertainty_factors=["potato_portion_inclusion", "bone_weight_deduction"],
        typical_oil_level="Moderate visible oil"
    ),
    alias_ids=["IND-NV-CH-MURGIR-JHOL"]
)

# Chicken Lollipop (Pan-Indian Indo-Chinese / Bar Starter)
register_nonveg_food_class(
    NonVegFoodClassRecord(
        canonical_food_id="IND-NV-CH-PAN-LOLLIPOP-001",
        canonical_name="Chicken Lollipop",
        hierarchy=NonVegHierarchy(
            level3_protein="Chicken",
            level4_region="Pan-India",
            level5_state="Pan-India",
            level6_food_family="Chicken Lollipop",
            level7_specific_dish="Chicken Lollipop",
            level8_variant="Frenched chicken winglet drumette coated in spicy red batter, deep-fried with bone handle exposed",
            level9_cooking_method="Deep-fried",
            level10_bone_state="bone_in",
            level11_portion_type="piece_count",
            level12_nutrition_ref_id="REF-NV-CH-PAN-LOLLIPOP-001"
        ),
        protein_type="Chicken",
        food_family="Chicken Lollipop",
        specific_dish="Chicken Lollipop",
        region="Pan-India",
        state_or_city="Pan-India",
        regional_names={"hi": "चिकन लॉलीपॉप", "ta": "சிக்கன் லாலிபாப்"},
        alternate_names=["chicken lollipop", "fried chicken wings", "drums of heaven"],
        cooking_method="Deep-fried",
        bone_state_default="bone_in",
        typical_cut="wing",
        consistency="Crispy",
        gravy_base=[],
        is_countable=True,
        piece_count_expected=4,
        default_portion_grams=160.0,
        edible_meat_ratio=0.65,
        nutrition_per_100g={"calories": 240.0, "protein": 20.0, "carbs": 8.0, "fat": 14.2, "fiber": 0.4},
        uncertainty_factors=["wing_bone_deduction", "batter_thickness"],
        typical_oil_level="High visible oil"
    ),
    alias_ids=["IND-NV-CH-LOLLIPOP"]
)


# =============================================================================
# 2. MUTTON & GOAT MASTER DATASET (Sections 3, 10, 11, 12)
# =============================================================================

# Mutton Chukka (Tamil Nadu)
register_nonveg_food_class(
    NonVegFoodClassRecord(
        canonical_food_id="IND-NV-MT-TN-CHUKKA-001",
        canonical_name="Mutton Chukka (Madurai Varuval)",
        hierarchy=NonVegHierarchy(
            level3_protein="Mutton/Goat/Lamb",
            level4_region="South India",
            level5_state="Tamil Nadu",
            level6_food_family="Mutton Chukka",
            level7_specific_dish="Mutton Chukka",
            level8_variant="Tender bone-in goat meat slow-braised and pan-roasted with shallots, curry leaves and ground black pepper",
            level9_cooking_method="Pan-roasted",
            level10_bone_state="bone_in",
            level11_portion_type="weight_grams",
            level12_nutrition_ref_id="REF-NV-MT-TN-CHUKKA-001"
        ),
        protein_type="Goat",
        food_family="Mutton Chukka",
        specific_dish="Mutton Chukka",
        region="South India",
        state_or_city="Madurai / Tamil Nadu",
        regional_names={"ta": "மட்டன் சுக்கா / ஆட்டுக்கறி வறுவல்", "te": "మటన్ చుక్కా", "hi": "मटन चुक्का"},
        alternate_names=["mutton chukka", "goat chukka", "madurai mutton chukka", "mutton sukka"],
        cooking_method="Pan-roasted",
        bone_state_default="bone_in",
        typical_cut="curry_cut",
        consistency="Dry",
        gravy_base=["shallots", "black_pepper", "curry_leaves"],
        is_countable=True,
        piece_count_expected=6,
        default_portion_grams=160.0,
        edible_meat_ratio=0.68,
        nutrition_per_100g={"calories": 245.0, "protein": 21.5, "carbs": 3.0, "fat": 16.5, "fiber": 0.8},
        uncertainty_factors=["goat_bone_weight_deduction", "fat_marbling_level"],
        typical_oil_level="High visible oil"
    ),
    alias_ids=["IND-NV-MT-CHUKKA", "IND-MT-CHUKKA-001"]
)

# Rogan Josh (Kashmir / North India)
register_nonveg_food_class(
    NonVegFoodClassRecord(
        canonical_food_id="IND-NV-MT-KS-ROGAN-001",
        canonical_name="Mutton Rogan Josh",
        hierarchy=NonVegHierarchy(
            level3_protein="Mutton/Goat/Lamb",
            level4_region="North India",
            level5_state="Kashmir",
            level6_food_family="Mutton Rogan-style preparations",
            level7_specific_dish="Rogan Josh",
            level8_variant="Slow-braised lamb/goat shanks in an aromatic crimson sauce of Kashmiri mirch, fennel, ginger and yogurt/maval flower",
            level9_cooking_method="Simmered",
            level10_bone_state="bone_in",
            level11_portion_type="weight_grams",
            level12_nutrition_ref_id="REF-NV-MT-KS-ROGAN-001"
        ),
        protein_type="Mutton",
        food_family="Mutton Rogan-style preparations",
        specific_dish="Rogan Josh",
        region="North India",
        state_or_city="Kashmir",
        regional_names={"hi": "रोगन जोश", "ur": "روغن جوش", "ta": "ரோகன் ஜோஷ்"},
        alternate_names=["rogan josh", "mutton rogan josh", "kashmiri rogan josh"],
        cooking_method="Simmered",
        bone_state_default="bone_in",
        typical_cut="curry_cut",
        consistency="Thick gravy",
        gravy_base=["yogurt", "kashmiri_chilli", "fennel", "mustard_oil"],
        is_countable=True,
        piece_count_expected=4,
        default_portion_grams=200.0,
        edible_meat_ratio=0.68,
        nutrition_per_100g={"calories": 220.0, "protein": 18.0, "carbs": 3.5, "fat": 15.0, "fiber": 0.8},
        uncertainty_factors=["bone_marrow_weight", "floating_tarri_fat"],
        typical_oil_level="Excess visible oil / oil pooling"
    ),
    alias_ids=["IND-NV-MT-ROGAN-JOSH"]
)

# Kosha Mangsho (West Bengal)
register_nonveg_food_class(
    NonVegFoodClassRecord(
        canonical_food_id="IND-NV-MT-WB-KOSHA-001",
        canonical_name="Bengali Kosha Mangsho",
        hierarchy=NonVegHierarchy(
            level3_protein="Mutton/Goat/Lamb",
            level4_region="East India",
            level5_state="West Bengal",
            level6_food_family="Mutton Curry",
            level7_specific_dish="Kosha Mangsho",
            level8_variant="Richly browned slow-roasted mutton cooked with dark caramelized onions, whole garam masala and mustard oil",
            level9_cooking_method="Simmered",
            level10_bone_state="bone_in",
            level11_portion_type="weight_grams",
            level12_nutrition_ref_id="REF-NV-MT-WB-KOSHA-001"
        ),
        protein_type="Goat",
        food_family="Mutton Curry",
        specific_dish="Kosha Mangsho",
        region="East India",
        state_or_city="West Bengal",
        regional_names={"bn": "কষা মাংস", "hi": "कोशा मांग्शो"},
        alternate_names=["kosha mangsho", "bengali mutton kasha", "khasir mangsho kosha"],
        cooking_method="Simmered",
        bone_state_default="bone_in",
        typical_cut="curry_cut",
        consistency="Thick gravy",
        gravy_base=["caramelized_onion", "mustard_oil", "yogurt"],
        is_countable=True,
        piece_count_expected=5,
        default_portion_grams=190.0,
        edible_meat_ratio=0.68,
        nutrition_per_100g={"calories": 255.0, "protein": 19.5, "carbs": 4.8, "fat": 17.8, "fiber": 0.7},
        uncertainty_factors=["mustard_oil_layer", "bone_deduction"],
        typical_oil_level="Excess visible oil / oil pooling"
    ),
    alias_ids=["IND-NV-MT-KOSHA"]
)

# Mutton Keema Matar (North India / Pan-India)
register_nonveg_food_class(
    NonVegFoodClassRecord(
        canonical_food_id="IND-NV-MT-NI-KEEMA-001",
        canonical_name="Mutton Keema Matar",
        hierarchy=NonVegHierarchy(
            level3_protein="Mutton/Goat/Lamb",
            level4_region="North India",
            level5_state="Delhi / Punjab",
            level6_food_family="Mutton Keema",
            level7_specific_dish="Mutton Keema Matar",
            level8_variant="Minced mutton braised with green peas, onions, tomatoes and whole spices",
            level9_cooking_method="Simmered",
            level10_bone_state="boneless",
            level11_portion_type="weight_grams",
            level12_nutrition_ref_id="REF-NV-MT-NI-KEEMA-001"
        ),
        protein_type="Mutton",
        food_family="Mutton Keema",
        specific_dish="Mutton Keema Matar",
        region="North India",
        state_or_city="Delhi / Punjab",
        regional_names={"hi": "मटन कीमा मटर", "ur": "قیمہ مٹر", "ta": "மட்டன் கீமா"},
        alternate_names=["mutton keema", "keema matar", "minced mutton"],
        cooking_method="Simmered",
        bone_state_default="boneless",
        typical_cut="mince",
        consistency="Semi-dry",
        gravy_base=["onion", "tomato", "green_peas"],
        is_countable=False,
        piece_count_expected=None,
        default_portion_grams=180.0,
        edible_meat_ratio=1.0,
        nutrition_per_100g={"calories": 210.0, "protein": 18.5, "carbs": 5.2, "fat": 13.0, "fiber": 1.5},
        uncertainty_factors=["mince_fat_percentage", "peas_ratio"],
        typical_oil_level="Moderate visible oil"
    ),
    alias_ids=["IND-NV-MT-KEEMA"]
)

# Mutton Seekh Kebab (North India)
register_nonveg_food_class(
    NonVegFoodClassRecord(
        canonical_food_id="IND-NV-MT-DEL-SEEKH-001",
        canonical_name="Mutton Seekh Kebab",
        hierarchy=NonVegHierarchy(
            level3_protein="Mutton/Goat/Lamb",
            level4_region="North India",
            level5_state="Delhi",
            level6_food_family="Mutton Seekh Kebab",
            level7_specific_dish="Mutton Seekh Kebab",
            level8_variant="Finely spiced minced goat meat molded onto skewers and grilled over hot coals",
            level9_cooking_method="Grilled",
            level10_bone_state="boneless",
            level11_portion_type="piece_count",
            level12_nutrition_ref_id="REF-NV-MT-DEL-SEEKH-001"
        ),
        protein_type="Mutton",
        food_family="Mutton Seekh Kebab",
        specific_dish="Mutton Seekh Kebab",
        region="North India",
        state_or_city="Delhi / Lucknow",
        regional_names={"hi": "मटन सीक कबाब", "ur": "سیخ کباب", "ta": "மட்டன் சீக் கபாப்"},
        alternate_names=["mutton seekh kebab", "seekh kebab", "lamb seekh kebab"],
        cooking_method="Grilled",
        bone_state_default="boneless",
        typical_cut="seekh",
        consistency="Dry",
        gravy_base=[],
        is_countable=True,
        piece_count_expected=2,
        default_portion_grams=140.0,
        edible_meat_ratio=1.0,
        nutrition_per_100g={"calories": 235.0, "protein": 20.0, "carbs": 3.2, "fat": 15.8, "fiber": 0.5},
        uncertainty_factors=["butter_basting", "mince_fat_ratio"],
        typical_oil_level="Moderate visible oil"
    ),
    alias_ids=["IND-NV-MT-SEEKH"]
)


# =============================================================================
# 3. FISH MASTER DATASET (Sections 3, 13, 14, 15, 16)
# =============================================================================

# Kerala Meen Curry (Kerala)
register_nonveg_food_class(
    NonVegFoodClassRecord(
        canonical_food_id="IND-NV-FS-KL-MEEN-001",
        canonical_name="Kerala Fish Curry (Kottayam Meen Curry)",
        hierarchy=NonVegHierarchy(
            level3_protein="Fish",
            level4_region="South India",
            level5_state="Kerala",
            level6_food_family="Fish Curry",
            level7_specific_dish="Kerala Meen Curry",
            level8_variant="Spicy tangy fish steaks cooked in earthen clay chatti with Kudampuli (Malabar tamarind), shallots and coconut oil",
            level9_cooking_method="Simmered",
            level10_bone_state="bone_in",
            level11_portion_type="weight_grams",
            level12_nutrition_ref_id="REF-NV-FS-KL-MEEN-001"
        ),
        protein_type="Fish",
        food_family="Fish Curry",
        specific_dish="Kerala Meen Curry",
        region="South India",
        state_or_city="Kottayam / Kerala",
        regional_names={"ml": "കേരള മീൻ കറി / കോട്ടയം മീൻ കറി", "ta": "கேரளா மீன் குழம்பு", "hi": "केरल मछली करी"},
        alternate_names=["kerala fish curry", "kottayam meen curry", "kudampuli meen curry", "nadan meen curry"],
        cooking_method="Simmered",
        bone_state_default="bone_in",
        typical_cut="steak",
        consistency="Thick gravy",
        gravy_base=["kudampuli", "shallots", "coconut_oil", "chilli"],
        is_countable=True,
        piece_count_expected=2,
        default_portion_grams=180.0,
        edible_meat_ratio=0.82,
        nutrition_per_100g={"calories": 135.0, "protein": 16.5, "carbs": 2.5, "fat": 6.8, "fiber": 0.4},
        uncertainty_factors=["fish_spine_bone_weight", "coconut_oil_sheen"],
        typical_oil_level="Moderate visible oil"
    ),
    alias_ids=["IND-NV-FS-KL-MEEN", "IND-FS-KOTTAYAM-MEEN"]
)

# Karimeen Pollichathu (Kerala)
register_nonveg_food_class(
    NonVegFoodClassRecord(
        canonical_food_id="IND-NV-FS-KL-POLLICHATHU-001",
        canonical_name="Karimeen Pollichathu",
        hierarchy=NonVegHierarchy(
            level3_protein="Fish",
            level4_region="South India",
            level5_state="Kerala",
            level6_food_family="Fish Pollichathu",
            level7_specific_dish="Karimeen Pollichathu",
            level8_variant="Pearl spot fish coated in fiery shallot-tomato masala wrapped in banana leaf and slow tawa pan-fried",
            level9_cooking_method="Tawa-fried",
            level10_bone_state="bone_in",
            level11_portion_type="piece_count",
            level12_nutrition_ref_id="REF-NV-FS-KL-POLLICHATHU-001"
        ),
        protein_type="Fish",
        food_family="Fish Pollichathu",
        specific_dish="Karimeen Pollichathu",
        region="South India",
        state_or_city="Alappuzha / Kerala Backwaters",
        regional_names={"ml": "കരിമീൻ പൊള്ളിച്ചത്", "ta": "கரிமீன் பொல்லிச்சது", "hi": "करीमीन पोल्लिचाथु"},
        alternate_names=["karimeen pollichathu", "banana leaf wrapped fish", "pearl spot pollichathu"],
        cooking_method="Tawa-fried",
        bone_state_default="bone_in",
        typical_cut="whole",
        consistency="Semi-dry",
        gravy_base=["shallots", "tomato", "coconut_oil"],
        is_countable=True,
        piece_count_expected=1,
        default_portion_grams=220.0,
        edible_meat_ratio=0.75,
        nutrition_per_100g={"calories": 155.0, "protein": 18.0, "carbs": 3.8, "fat": 7.5, "fiber": 0.6},
        uncertainty_factors=["whole_fish_bone_weight", "banana_leaf_tare_weight"],
        typical_oil_level="Moderate visible oil"
    ),
    alias_ids=["IND-NV-FS-POLLICHATHU"]
)

# Fish Moilee / Molee (Kerala)
register_nonveg_food_class(
    NonVegFoodClassRecord(
        canonical_food_id="IND-NV-FS-KL-MOILEE-001",
        canonical_name="Fish Moilee (Fish Molee)",
        hierarchy=NonVegHierarchy(
            level3_protein="Fish",
            level4_region="South India",
            level5_state="Kerala",
            level6_food_family="Fish Molee/Moilee",
            level7_specific_dish="Fish Moilee",
            level8_variant="Seer fish or Pomfret steaks gently poached in delicate mild coconut milk, ginger and green chillies",
            level9_cooking_method="Simmered",
            level10_bone_state="bone_in",
            level11_portion_type="weight_grams",
            level12_nutrition_ref_id="REF-NV-FS-KL-MOILEE-001"
        ),
        protein_type="Fish",
        food_family="Fish Molee/Moilee",
        specific_dish="Fish Moilee",
        region="South India",
        state_or_city="Kochi / Central Kerala",
        regional_names={"ml": "മീൻ മോളി", "ta": "மீன் மோலி", "hi": "फिश मोइली"},
        alternate_names=["fish moilee", "fish molee", "kerala coconut fish stew", "meen moilee"],
        cooking_method="Simmered",
        bone_state_default="bone_in",
        typical_cut="steak",
        consistency="Thin gravy",
        gravy_base=["coconut_milk", "ginger", "curry_leaves"],
        is_countable=True,
        piece_count_expected=2,
        default_portion_grams=190.0,
        edible_meat_ratio=0.82,
        nutrition_per_100g={"calories": 160.0, "protein": 14.5, "carbs": 3.0, "fat": 10.2, "fiber": 0.4},
        uncertainty_factors=["coconut_milk_fat_thickness", "bone_deduction"],
        typical_oil_level="Moderate visible oil"
    ),
    alias_ids=["IND-NV-FS-MOILEE"]
)

# Bengali Macher Jhol (West Bengal - Rohu/Katla)
register_nonveg_food_class(
    NonVegFoodClassRecord(
        canonical_food_id="IND-NV-FS-WB-JHOL-001",
        canonical_name="Bengali Macher Jhol (Rohu/Katla)",
        hierarchy=NonVegHierarchy(
            level3_protein="Fish",
            level4_region="East India",
            level5_state="West Bengal",
            level6_food_family="Fish Curry",
            level7_specific_dish="Macher Jhol",
            level8_variant="Light comfort fish stew of Rohu/Katla with potatoes, pointed gourd (potol) and kalonji cumin tempering",
            level9_cooking_method="Simmered",
            level10_bone_state="bone_in",
            level11_portion_type="weight_grams",
            level12_nutrition_ref_id="REF-NV-FS-WB-JHOL-001"
        ),
        protein_type="Fish",
        food_family="Fish Curry",
        specific_dish="Macher Jhol",
        region="East India",
        state_or_city="West Bengal",
        regional_names={"bn": "মাছের পাতলা ঝোল", "hi": "माछेर झोल", "or": "ମାଛ ଝୋଳ"},
        alternate_names=["macher jhol", "bengali fish curry", "rohu fish curry", "patla macher jhol"],
        cooking_method="Simmered",
        bone_state_default="bone_in",
        typical_cut="steak",
        consistency="Thin gravy",
        gravy_base=["ginger_cumin", "mustard_oil", "potato"],
        is_countable=True,
        piece_count_expected=2,
        default_portion_grams=200.0,
        edible_meat_ratio=0.80,
        nutrition_per_100g={"calories": 125.0, "protein": 14.0, "carbs": 4.5, "fat": 5.8, "fiber": 0.6},
        uncertainty_factors=["potato_portion_inclusion", "bone_weight_deduction"],
        typical_oil_level="Moderate visible oil"
    ),
    alias_ids=["IND-NV-FS-MACHER-JHOL"]
)

# Shorshe Ilish (West Bengal)
register_nonveg_food_class(
    NonVegFoodClassRecord(
        canonical_food_id="IND-NV-FS-WB-SHORSHE-001",
        canonical_name="Shorshe Ilish (Hilsa in Mustard)",
        hierarchy=NonVegHierarchy(
            level3_protein="Fish",
            level4_region="East India",
            level5_state="West Bengal",
            level6_food_family="Fish Curry",
            level7_specific_dish="Shorshe Ilish",
            level8_variant="Hilsa fish steaks steamed in pungent ground yellow and black mustard paste with green chillies and raw mustard oil",
            level9_cooking_method="Steamed",
            level10_bone_state="bone_in",
            level11_portion_type="piece_count",
            level12_nutrition_ref_id="REF-NV-FS-WB-SHORSHE-001"
        ),
        protein_type="Fish",
        food_family="Fish Curry",
        specific_dish="Shorshe Ilish",
        region="East India",
        state_or_city="West Bengal",
        regional_names={"bn": "সর্ষে ইলিশ", "hi": "सोरषे इलिश", "or": "ସୋରିଷ ଇଲିଶି"},
        alternate_names=["shorshe ilish", "sorshe ilish", "hilsa fish mustard", "ilish macher shorshe"],
        cooking_method="Steamed",
        bone_state_default="bone_in",
        typical_cut="steak",
        consistency="Thick gravy",
        gravy_base=["mustard_paste", "mustard_oil", "green_chilli"],
        is_countable=True,
        piece_count_expected=2,
        default_portion_grams=180.0,
        edible_meat_ratio=0.78,
        nutrition_per_100g={"calories": 235.0, "protein": 17.5, "carbs": 2.8, "fat": 17.2, "fiber": 0.5},
        uncertainty_factors=["hilsa_intrinsic_omega_fat", "mustard_oil_quantity"],
        typical_oil_level="High visible oil"
    ),
    alias_ids=["IND-NV-FS-SHORSHE-ILISH"]
)

# Vanjaram Tawa Fish Fry (Tamil Nadu)
register_nonveg_food_class(
    NonVegFoodClassRecord(
        canonical_food_id="IND-NV-FS-TN-VANJARAMFRY-001",
        canonical_name="Vanjaram Fish Fry (Seer Fish Tawa Fry)",
        hierarchy=NonVegHierarchy(
            level3_protein="Fish",
            level4_region="South India",
            level5_state="Tamil Nadu",
            level6_food_family="Fish Tawa Fry",
            level7_specific_dish="Vanjaram Fish Fry",
            level8_variant="Center-cut King Seer fish steak marinated in red chilli, turmeric and lemon, pan-roasted crisp on hot iron tawa",
            level9_cooking_method="Tawa-fried",
            level10_bone_state="bone_in",
            level11_portion_type="piece_count",
            level12_nutrition_ref_id="REF-NV-FS-TN-VANJARAMFRY-001"
        ),
        protein_type="Fish",
        food_family="Fish Tawa Fry",
        specific_dish="Vanjaram Fish Fry",
        region="South India",
        state_or_city="Chennai / Coastal Tamil Nadu",
        regional_names={"ta": "வஞ்சிரம் மீன் வறுவல்", "te": "వంజరం చేపల వేపుడు", "kn": "ಅಂಜಲ್ ಫ್ರೈ", "hi": "सुरमई तवा फ्राई"},
        alternate_names=["vanjaram fish fry", "seer fish tawa fry", "king fish fry", "surmai tawa fry"],
        cooking_method="Tawa-fried",
        bone_state_default="bone_in",
        typical_cut="steak",
        consistency="Crispy",
        gravy_base=[],
        is_countable=True,
        piece_count_expected=1,
        default_portion_grams=150.0,
        edible_meat_ratio=0.85,
        nutrition_per_100g={"calories": 195.0, "protein": 22.0, "carbs": 2.5, "fat": 10.8, "fiber": 0.3},
        uncertainty_factors=["tawa_shallow_oil", "central_spine_bone_deduction"],
        typical_oil_level="Moderate visible oil"
    ),
    alias_ids=["IND-NV-FS-VANJARAM-FRY"]
)

# Amritsari Fish Fry (Punjab)
register_nonveg_food_class(
    NonVegFoodClassRecord(
        canonical_food_id="IND-NV-FS-PB-AMRITSARI-001",
        canonical_name="Amritsari Fish Fry",
        hierarchy=NonVegHierarchy(
            level3_protein="Fish",
            level4_region="North India",
            level5_state="Punjab",
            level6_food_family="Fish Amritsari",
            level7_specific_dish="Amritsari Fish",
            level8_variant="Crispy boneless sole/singhara fish fillets coated in carom seed (ajwain) spiced gram flour batter and deep-fried",
            level9_cooking_method="Deep-fried",
            level10_bone_state="boneless",
            level11_portion_type="piece_count",
            level12_nutrition_ref_id="REF-NV-FS-PB-AMRITSARI-001"
        ),
        protein_type="Fish",
        food_family="Fish Amritsari",
        specific_dish="Amritsari Fish",
        region="North India",
        state_or_city="Amritsar / Punjab",
        regional_names={"pa": "ਅੰਮ੍ਰਿਤਸਰੀ ਮੱਛੀ ਫਰਾਈ", "hi": "अमृतसरी फिश फ्राई", "ta": "அமிர்தசரஸ் மீன் வறுவல்"},
        alternate_names=["amritsari fish", "amritsari fish fry", "punjabi fish pakora"],
        cooking_method="Deep-fried",
        bone_state_default="boneless",
        typical_cut="boneless_chunks",
        consistency="Crispy",
        gravy_base=[],
        is_countable=True,
        piece_count_expected=4,
        default_portion_grams=160.0,
        edible_meat_ratio=1.0,
        nutrition_per_100g={"calories": 225.0, "protein": 19.0, "carbs": 8.0, "fat": 13.0, "fiber": 0.8},
        uncertainty_factors=["besan_batter_absorption", "deep_frying_oil"],
        typical_oil_level="High visible oil"
    ),
    alias_ids=["IND-NV-FS-AMRITSARI"]
)


# =============================================================================
# 4. SEAFOOD: PRAWN, CRAB, SQUID (Sections 3, 17, 18, 19, 20)
# =============================================================================

# Kerala Prawn Roast (Kerala)
register_nonveg_food_class(
    NonVegFoodClassRecord(
        canonical_food_id="IND-NV-PR-KL-ROAST-001",
        canonical_name="Kerala Prawn Roast (Chemmeen Roast)",
        hierarchy=NonVegHierarchy(
            level3_protein="Seafood",
            level4_region="South India",
            level5_state="Kerala",
            level6_food_family="Prawn Roast",
            level7_specific_dish="Kerala Prawn Roast",
            level8_variant="Juicy prawns pan-roasted with shallots, crushed ginger-garlic, curry leaves and coconut slices",
            level9_cooking_method="Pan-roasted",
            level10_bone_state="boneless",
            level11_portion_type="piece_count",
            level12_nutrition_ref_id="REF-NV-PR-KL-ROAST-001"
        ),
        protein_type="Prawn",
        food_family="Prawn Roast",
        specific_dish="Kerala Prawn Roast",
        region="South India",
        state_or_city="Kerala",
        regional_names={"ml": "ചെമ്മീൻ റോസ്റ്റ്", "ta": "இறால் ரோஸ்ட்", "hi": "झींगा रोस्ट", "te": "రొయ్యల వేపుడు"},
        alternate_names=["chemmeen roast", "kerala prawn roast", "prawn fry kerala style"],
        cooking_method="Pan-roasted",
        bone_state_default="boneless",
        typical_cut="whole",
        consistency="Semi-dry",
        gravy_base=["shallots", "coconut_slices", "black_pepper"],
        is_countable=True,
        piece_count_expected=8,
        default_portion_grams=160.0,
        edible_meat_ratio=0.95,
        nutrition_per_100g={"calories": 165.0, "protein": 19.2, "carbs": 3.8, "fat": 8.0, "fiber": 0.5},
        uncertainty_factors=["coconut_oil_quantity", "tail_shell_tare"],
        typical_oil_level="Moderate visible oil"
    ),
    alias_ids=["IND-NV-PR-KL-ROAST", "IND-CHEMMEEN-ROAST"]
)

# Bengali Chingri Malai Curry (West Bengal)
register_nonveg_food_class(
    NonVegFoodClassRecord(
        canonical_food_id="IND-NV-PR-WB-MALAI-001",
        canonical_name="Chingri Malai Curry (Prawn Malai Curry)",
        hierarchy=NonVegHierarchy(
            level3_protein="Seafood",
            level4_region="East India",
            level5_state="West Bengal",
            level6_food_family="Prawn Curry",
            level7_specific_dish="Chingri Malai Curry",
            level8_variant="Jumbo tiger prawns simmered in velvety coconut milk, aromatic whole spices and a dash of ghee",
            level9_cooking_method="Simmered",
            level10_bone_state="boneless",
            level11_portion_type="piece_count",
            level12_nutrition_ref_id="REF-NV-PR-WB-MALAI-001"
        ),
        protein_type="Prawn",
        food_family="Prawn Curry",
        specific_dish="Chingri Malai Curry",
        region="East India",
        state_or_city="West Bengal",
        regional_names={"bn": "চিংড়ি মালাই কারি", "hi": "चिंगरी मलाई करी", "or": "ଚିଙ୍ଗୁଡ଼ି ମଲାଇ କରୀ"},
        alternate_names=["chingri malai curry", "prawn malai curry", "bengali prawn coconut curry"],
        cooking_method="Simmered",
        bone_state_default="boneless",
        typical_cut="whole",
        consistency="Thick gravy",
        gravy_base=["coconut_milk", "mustard_oil", "cinnamon_cardamom"],
        is_countable=True,
        piece_count_expected=4,
        default_portion_grams=200.0,
        edible_meat_ratio=0.90,
        nutrition_per_100g={"calories": 190.0, "protein": 15.0, "carbs": 4.5, "fat": 12.5, "fiber": 0.4},
        uncertainty_factors=["coconut_cream_thickness", "prawn_head_shell_inclusion"],
        typical_oil_level="Moderate visible oil"
    ),
    alias_ids=["IND-NV-PR-MALAI"]
)

# Chettinad Crab Masala / Nandu Masala (Tamil Nadu)
register_nonveg_food_class(
    NonVegFoodClassRecord(
        canonical_food_id="IND-NV-CR-TN-MASALA-001",
        canonical_name="Chettinad Crab Masala (Nandu Masala)",
        hierarchy=NonVegHierarchy(
            level3_protein="Seafood",
            level4_region="South India",
            level5_state="Tamil Nadu",
            level6_food_family="Crab Masala",
            level7_specific_dish="Crab Masala",
            level8_variant="Hard-shelled sea crab cracked and simmered in an intensely peppered Chettinad shallot-fennel masala",
            level9_cooking_method="Simmered",
            level10_bone_state="bone_in",
            level11_portion_type="weight_grams",
            level12_nutrition_ref_id="REF-NV-CR-TN-MASALA-001"
        ),
        protein_type="Crab",
        food_family="Crab Masala",
        specific_dish="Crab Masala",
        region="South India",
        state_or_city="Chettinad / Coastal Tamil Nadu",
        regional_names={"ta": "நண்டு மசாலா / செட்டிநாடு நண்டு கறி", "ml": "ഞണ്ട് റോസ്റ്റ്", "te": "పీతల కూర", "hi": "केकड़ा मसाला"},
        alternate_names=["nandu masala", "chettinad crab masala", "crab curry", "crab pepper masala"],
        cooking_method="Simmered",
        bone_state_default="bone_in",
        typical_cut="whole",
        consistency="Thick gravy",
        gravy_base=["shallots", "black_pepper", "fennel", "tomato"],
        is_countable=True,
        piece_count_expected=3,
        default_portion_grams=250.0,
        edible_meat_ratio=0.45,
        nutrition_per_100g={"calories": 115.0, "protein": 14.0, "carbs": 3.2, "fat": 5.0, "fiber": 0.5},
        uncertainty_factors=["crab_hard_shell_tare_deduction", "claw_meat_percentage"],
        typical_oil_level="Moderate visible oil"
    ),
    alias_ids=["IND-NV-CR-NANDU"]
)

# Kerala Squid Roast (Kerala)
register_nonveg_food_class(
    NonVegFoodClassRecord(
        canonical_food_id="IND-NV-SQ-KL-ROAST-001",
        canonical_name="Kerala Squid Roast (Koonthal Roast)",
        hierarchy=NonVegHierarchy(
            level3_protein="Seafood",
            level4_region="South India",
            level5_state="Kerala",
            level6_food_family="Squid Roast",
            level7_specific_dish="Squid Roast",
            level8_variant="Tender calamari squid rings stir-roasted with caramelized shallots, coconut bits, curry leaves and coarse pepper",
            level9_cooking_method="Pan-roasted",
            level10_bone_state="boneless",
            level11_portion_type="weight_grams",
            level12_nutrition_ref_id="REF-NV-SQ-KL-ROAST-001"
        ),
        protein_type="Squid",
        food_family="Squid Roast",
        specific_dish="Squid Roast",
        region="South India",
        state_or_city="Kerala",
        regional_names={"ml": "കൂന്തൽ റോസ്റ്റ് / കണവ റോസ്റ്റ്", "ta": "கணவா ரோஸ்ட்", "hi": "स्क्वीड रोस्ट"},
        alternate_names=["koonthal roast", "kanava roast", "squid roast", "calamari roast"],
        cooking_method="Pan-roasted",
        bone_state_default="boneless",
        typical_cut="sliced",
        consistency="Semi-dry",
        gravy_base=["shallots", "coconut_slices", "black_pepper"],
        is_countable=False,
        piece_count_expected=None,
        default_portion_grams=150.0,
        edible_meat_ratio=1.0,
        nutrition_per_100g={"calories": 140.0, "protein": 17.0, "carbs": 3.5, "fat": 6.2, "fiber": 0.4},
        uncertainty_factors=["coconut_oil_level"],
        typical_oil_level="Moderate visible oil"
    ),
    alias_ids=["IND-NV-SQ-KOONTHAL"]
)


# =============================================================================
# 5. EGG MASTER DATASET (Sections 3, 21, 22, 23, 24)
# =============================================================================

# Whole Boiled Egg (Pan-India)
register_nonveg_food_class(
    NonVegFoodClassRecord(
        canonical_food_id="IND-NV-EG-PAN-BOILED-001",
        canonical_name="Hard-Boiled Egg",
        hierarchy=NonVegHierarchy(
            level3_protein="Egg",
            level4_region="Pan-India",
            level5_state="Pan-India",
            level6_food_family="Boiled Egg",
            level7_specific_dish="Boiled Egg",
            level8_variant="Hard boiled peeled whole egg",
            level9_cooking_method="Boiled",
            level10_bone_state="boneless",
            level11_portion_type="piece_count",
            level12_nutrition_ref_id="REF-NV-EG-PAN-BOILED-001"
        ),
        protein_type="Egg",
        food_family="Boiled Egg",
        specific_dish="Boiled Egg",
        region="Pan-India",
        state_or_city="Pan-India",
        regional_names={"hi": "उबला अंडा", "ta": "அவித்த முட்டை", "te": "ఉడికించిన గుడ్డు", "ml": "പുഴുങ്ങിയ മുട്ട", "kn": "ಬೇಯಿಸಿದ ಮೊಟ್ಟೆ", "bn": "সেদ্ধ ডিম"},
        alternate_names=["boiled egg", "hard boiled egg", "whole boiled egg", "anda"],
        cooking_method="Boiled",
        bone_state_default="boneless",
        typical_cut="whole",
        consistency="Dry",
        gravy_base=[],
        is_countable=True,
        piece_count_expected=1,
        default_portion_grams=50.0,
        edible_meat_ratio=1.0,
        nutrition_per_100g={"calories": 155.0, "protein": 12.6, "carbs": 1.1, "fat": 10.6, "fiber": 0.0},
        uncertainty_factors=["egg_size_variance_small_medium_large"],
        typical_oil_level="Low visible oil"
    ),
    alias_ids=["IND-NV-EG-BOILED"]
)

# Masala Omelette (Pan-India)
register_nonveg_food_class(
    NonVegFoodClassRecord(
        canonical_food_id="IND-NV-EG-PAN-OMELETTE-001",
        canonical_name="Masala Omelette",
        hierarchy=NonVegHierarchy(
            level3_protein="Egg",
            level4_region="Pan-India",
            level5_state="Pan-India",
            level6_food_family="Omelette",
            level7_specific_dish="Masala Omelette",
            level8_variant="Whisked 2-egg omelette folded with chopped onions, green chillies, fresh coriander and black pepper",
            level9_cooking_method="Pan-roasted",
            level10_bone_state="boneless",
            level11_portion_type="piece_count",
            level12_nutrition_ref_id="REF-NV-EG-PAN-OMELETTE-001"
        ),
        protein_type="Egg",
        food_family="Omelette",
        specific_dish="Masala Omelette",
        region="Pan-India",
        state_or_city="Pan-India",
        regional_names={"hi": "मसाला आमलेट", "ta": "முட்டை ஆம்லெட்", "te": "ఆమ్లెట్", "ml": "മുട്ട ഓംലെറ്റ്"},
        alternate_names=["masala omelette", "indian omelette", "onion omelette", "egg omelet"],
        cooking_method="Pan-roasted",
        bone_state_default="boneless",
        typical_cut="whole",
        consistency="Soft",
        gravy_base=[],
        is_countable=True,
        piece_count_expected=1,
        default_portion_grams=110.0,
        edible_meat_ratio=1.0,
        nutrition_per_100g={"calories": 175.0, "protein": 11.8, "carbs": 2.8, "fat": 12.5, "fiber": 0.4},
        uncertainty_factors=["egg_count_uncertainty_1_vs_2_eggs", "butter_or_oil_used"],
        typical_oil_level="Moderate visible oil"
    ),
    alias_ids=["IND-NV-EG-OMELETTE"]
)

# Egg Bhurji (Pan-India)
register_nonveg_food_class(
    NonVegFoodClassRecord(
        canonical_food_id="IND-NV-EG-PAN-BHURJI-001",
        canonical_name="Egg Bhurji (Scrambled Spiced Egg)",
        hierarchy=NonVegHierarchy(
            level3_protein="Egg",
            level4_region="Pan-India",
            level5_state="Pan-India",
            level6_food_family="Egg Bhurji",
            level7_specific_dish="Egg Bhurji",
            level8_variant="Eggs scrambled over high heat with sautéed onions, tomatoes, ginger and green chillies",
            level9_cooking_method="Stir-fried",
            level10_bone_state="boneless",
            level11_portion_type="weight_grams",
            level12_nutrition_ref_id="REF-NV-EG-PAN-BHURJI-001"
        ),
        protein_type="Egg",
        food_family="Egg Bhurji",
        specific_dish="Egg Bhurji",
        region="Pan-India",
        state_or_city="Pan-India / Street Food",
        regional_names={"hi": "अंडा भुर्जी", "ta": "முட்டை பொடிமாஸ்", "te": "ఎగ్ భూర్జీ", "ml": "മുട്ട പൊരിച്ചത്"},
        alternate_names=["egg bhurji", "anda bhurji", "muttai podimas", "scrambled egg"],
        cooking_method="Stir-fried",
        bone_state_default="boneless",
        typical_cut="scrambled",
        consistency="Dry",
        gravy_base=["onion", "tomato"],
        is_countable=False,
        piece_count_expected=None,
        default_portion_grams=140.0,
        edible_meat_ratio=1.0,
        nutrition_per_100g={"calories": 180.0, "protein": 12.2, "carbs": 3.4, "fat": 13.0, "fiber": 0.5},
        uncertainty_factors=["number_of_eggs_scrambled", "butter_oil_quantity"],
        typical_oil_level="Moderate visible oil"
    ),
    alias_ids=["IND-NV-EG-BHURJI"]
)

# Kerala Mutta Roast (Kerala)
register_nonveg_food_class(
    NonVegFoodClassRecord(
        canonical_food_id="IND-NV-EG-KL-ROAST-001",
        canonical_name="Kerala Egg Roast (Mutta Roast)",
        hierarchy=NonVegHierarchy(
            level3_protein="Egg",
            level4_region="South India",
            level5_state="Kerala",
            level6_food_family="Egg Roast",
            level7_specific_dish="Kerala Egg Roast",
            level8_variant="Hard boiled eggs smothered in a thick caramelized onion-tomato and fennel gravy",
            level9_cooking_method="Simmered",
            level10_bone_state="boneless",
            level11_portion_type="piece_count",
            level12_nutrition_ref_id="REF-NV-EG-KL-ROAST-001"
        ),
        protein_type="Egg",
        food_family="Egg Roast",
        specific_dish="Kerala Egg Roast",
        region="South India",
        state_or_city="Kerala",
        regional_names={"ml": "മുട്ട റോസ്റ്റ്", "ta": "முட்டை ரோஸ்ட்", "hi": "अंडा रोस्ट"},
        alternate_names=["mutta roast", "kerala egg roast", "egg roast for appam"],
        cooking_method="Simmered",
        bone_state_default="boneless",
        typical_cut="whole",
        consistency="Thick gravy",
        gravy_base=["caramelized_onion", "tomato", "fennel"],
        is_countable=True,
        piece_count_expected=2,
        default_portion_grams=170.0,
        edible_meat_ratio=1.0,
        nutrition_per_100g={"calories": 160.0, "protein": 10.5, "carbs": 6.0, "fat": 10.5, "fiber": 0.9},
        uncertainty_factors=["visible_oil_sheen", "egg_count"],
        typical_oil_level="High visible oil"
    ),
    alias_ids=["IND-NV-EG-MUTTA-ROAST"]
)


# =============================================================================
# 6. NON-VEG BIRYANI DATASET (Sections 3, 25, 26, 41, 69, 80)
# =============================================================================

# Hyderabadi Chicken Dum Biryani
register_nonveg_food_class(
    NonVegFoodClassRecord(
        canonical_food_id="IND-NV-BY-HYD-CHICKEN-001",
        canonical_name="Hyderabadi Chicken Dum Biryani",
        hierarchy=NonVegHierarchy(
            level3_protein="Chicken",
            level4_region="South India",
            level5_state="Telangana",
            level6_food_family="Chicken Biryani",
            level7_specific_dish="Hyderabadi Chicken Biryani",
            level8_variant="Kacchi yakhni marinated bone-in chicken slow cooked under sealed dum with fragrant basmati, fried onions and saffron",
            level9_cooking_method="Steamed",
            level10_bone_state="bone_in",
            level11_portion_type="weight_grams",
            level12_nutrition_ref_id="REF-NV-BY-HYD-CHICKEN-001"
        ),
        protein_type="Chicken",
        food_family="Chicken Biryani",
        specific_dish="Hyderabadi Chicken Biryani",
        region="South India",
        state_or_city="Hyderabad / Telangana",
        regional_names={"te": "హైదరాబాదీ చికెన్ దమ్ బిర్యానీ", "ur": "حیدرآبادی چکن بریانی", "hi": "हैदराबादी चिकन बिरयानी", "ta": "ஹைதராபாத் சிக்கன் பிரியாணி"},
        alternate_names=["hyderabadi chicken biryani", "chicken dum biryani", "hyderabadi biryani"],
        cooking_method="Steamed",
        bone_state_default="bone_in",
        typical_cut="curry_cut",
        consistency="Dry",
        gravy_base=["fried_onion", "yogurt", "ghee", "saffron"],
        is_countable=False,
        piece_count_expected=2,
        default_portion_grams=350.0,
        edible_meat_ratio=0.88,
        nutrition_per_100g={"calories": 195.0, "protein": 9.5, "carbs": 24.5, "fat": 6.8, "fiber": 0.8},
        uncertainty_factors=["rice_to_meat_ratio", "bone_weight_deduction", "ghee_infusion"],
        typical_oil_level="Moderate visible oil"
    ),
    alias_ids=["IND-NV-BY-HYD-CHICKEN", "IND-CH-HYD-BIRYANI"]
)

# Hyderabadi Mutton Dum Biryani
register_nonveg_food_class(
    NonVegFoodClassRecord(
        canonical_food_id="IND-NV-BY-HYD-MUTTON-001",
        canonical_name="Hyderabadi Mutton Dum Biryani",
        hierarchy=NonVegHierarchy(
            level3_protein="Mutton/Goat/Lamb",
            level4_region="South India",
            level5_state="Telangana",
            level6_food_family="Mutton Biryani",
            level7_specific_dish="Hyderabadi Mutton Biryani",
            level8_variant="Tender marinated goat meat layered with aged basmati rice cooked in dough-sealed handi with mint, coriander and saffron milk",
            level9_cooking_method="Steamed",
            level10_bone_state="bone_in",
            level11_portion_type="weight_grams",
            level12_nutrition_ref_id="REF-NV-BY-HYD-MUTTON-001"
        ),
        protein_type="Mutton",
        food_family="Mutton Biryani",
        specific_dish="Hyderabadi Mutton Biryani",
        region="South India",
        state_or_city="Hyderabad / Telangana",
        regional_names={"te": "హైదరాబాదీ మటన్ దమ్ బిర్యానీ", "ur": "حیدرآبادی مٹن بریانی", "hi": "हैदराबादी मटन बिरयानी"},
        alternate_names=["hyderabadi mutton biryani", "mutton dum biryani", "gosht biryani"],
        cooking_method="Steamed",
        bone_state_default="bone_in",
        typical_cut="curry_cut",
        consistency="Dry",
        gravy_base=["fried_onion", "yogurt", "ghee", "saffron"],
        is_countable=False,
        piece_count_expected=3,
        default_portion_grams=350.0,
        edible_meat_ratio=0.86,
        nutrition_per_100g={"calories": 210.0, "protein": 10.5, "carbs": 23.0, "fat": 8.5, "fiber": 0.7},
        uncertainty_factors=["mutton_bone_weight_deduction", "fat_rendered_into_rice"],
        typical_oil_level="Moderate visible oil"
    ),
    alias_ids=["IND-NV-BY-HYD-MUTTON"]
)


# =============================================================================
# 7. REGIONAL SPECIALTIES: PORK & BEEF (Sections 53, 54)
# =============================================================================

# Goan Pork Vindaloo (Goa)
register_nonveg_food_class(
    NonVegFoodClassRecord(
        canonical_food_id="IND-NV-PK-GOA-VINDALOO-001",
        canonical_name="Goan Pork Vindaloo",
        hierarchy=NonVegHierarchy(
            level3_protein="Regional Pork",
            level4_region="West India",
            level5_state="Goa",
            level6_food_family="Pork Curry",
            level7_specific_dish="Pork Vindaloo",
            level8_variant="Portuguese influenced pork curry marinated in tangy toddy palm vinegar, dried Kashmiri chillies, garlic and warm spices",
            level9_cooking_method="Simmered",
            level10_bone_state="boneless",
            level11_portion_type="weight_grams",
            level12_nutrition_ref_id="REF-NV-PK-GOA-VINDALOO-001"
        ),
        protein_type="Pork",
        food_family="Pork Curry",
        specific_dish="Pork Vindaloo",
        region="West India",
        state_or_city="Goa",
        regional_names={"hi": "पोर्क विंदालू", "ta": "போர்க் விண்டாலூ"},
        alternate_names=["pork vindaloo", "goan vindaloo", "traditional pork vindaloo"],
        cooking_method="Simmered",
        bone_state_default="boneless",
        typical_cut="cube",
        consistency="Thick gravy",
        gravy_base=["toddy_vinegar", "kashmiri_chilli", "garlic"],
        is_countable=False,
        piece_count_expected=None,
        default_portion_grams=180.0,
        edible_meat_ratio=1.0,
        nutrition_per_100g={"calories": 240.0, "protein": 18.0, "carbs": 4.0, "fat": 16.8, "fiber": 0.6},
        uncertainty_factors=["pork_belly_fat_ratio"],
        typical_oil_level="High visible oil"
    ),
    alias_ids=["IND-NV-PK-VINDALOO"]
)

# Kerala Beef / Meat Ularthiyathu (Kerala)
register_nonveg_food_class(
    NonVegFoodClassRecord(
        canonical_food_id="IND-NV-BF-KL-ULARTHU-001",
        canonical_name="Kerala Beef Ularthiyathu (Meat Roast)",
        hierarchy=NonVegHierarchy(
            level3_protein="Regional Beef",
            level4_region="South India",
            level5_state="Kerala",
            level6_food_family="Beef Roast",
            level7_specific_dish="Beef Ularthiyathu",
            level8_variant="Tender beef chunks pressure cooked and slow roasted in an iron kadai with coconut tidbits, shallots and crushed black pepper",
            level9_cooking_method="Pan-roasted",
            level10_bone_state="boneless",
            level11_portion_type="weight_grams",
            level12_nutrition_ref_id="REF-NV-BF-KL-ULARTHU-001"
        ),
        protein_type="Beef",
        food_family="Beef Roast",
        specific_dish="Beef Ularthiyathu",
        region="South India",
        state_or_city="Kottayam / Kerala",
        regional_names={"ml": "ബീഫ് ഉലർത്തിയത്", "ta": "பீப் உலர்த்தியது", "hi": "केरल बीफ रोस्ट"},
        alternate_names=["beef ularthiyathu", "kerala beef fry", "beef roast", "nadan beef fry"],
        cooking_method="Pan-roasted",
        bone_state_default="boneless",
        typical_cut="cube",
        consistency="Dry",
        gravy_base=["shallots", "coconut_slices", "black_pepper"],
        is_countable=False,
        piece_count_expected=None,
        default_portion_grams=160.0,
        edible_meat_ratio=1.0,
        nutrition_per_100g={"calories": 250.0, "protein": 22.0, "carbs": 3.0, "fat": 16.5, "fiber": 0.8},
        uncertainty_factors=["coconut_oil_absorption", "meat_fat_strip"],
        typical_oil_level="High visible oil"
    ),
    alias_ids=["IND-NV-BF-ULARTHIYATHU"]
)


# =============================================================================
# 8. FALLBACK CLASSES (Sections 61 & 83)
# =============================================================================

# Unknown Non-Veg General Fallback
register_nonveg_food_class(
    NonVegFoodClassRecord(
        canonical_food_id="IND-NV-UNKNOWN-001",
        canonical_name="Indian Non-Vegetarian Dish (Exact Identity Uncertain)",
        hierarchy=NonVegHierarchy(
            level3_protein="Mixed Non-Veg",
            level4_region="Pan-India",
            level5_state="Unknown",
            level6_food_family="Unknown Non-Veg",
            level7_specific_dish="Unknown Non-Veg Dish",
            level8_variant="Uncertain non-vegetarian preparation requiring user confirmation or multiscale visual cues",
            level9_cooking_method="Simmered",
            level10_bone_state="unknown",
            level11_portion_type="weight_grams",
            level12_nutrition_ref_id="REF-NV-FALLBACK-001"
        ),
        protein_type="Mixed Non-Veg",
        food_family="Unknown Non-Veg",
        specific_dish="Unknown Non-Veg Dish",
        region="Pan-India",
        state_or_city="Pan-India",
        regional_names={"hi": "अज्ञात मांसाहारी व्यंजन", "ta": "அடையாளம் தெரியாத அசைவ உணவு"},
        alternate_names=["unknown non veg dish", "unidentified meat curry", "non veg unknown"],
        cooking_method="Simmered",
        bone_state_default="unknown",
        typical_cut="curry_cut",
        consistency="Thick gravy",
        gravy_base=[],
        is_countable=False,
        piece_count_expected=None,
        default_portion_grams=180.0,
        edible_meat_ratio=0.75,
        nutrition_per_100g={"calories": 185.0, "protein": 16.0, "carbs": 5.0, "fat": 11.0, "fiber": 0.8},
        uncertainty_factors=["protein_type_unknown", "bone_state_unverified"],
        typical_oil_level="Moderate visible oil"
    )
)

# Chicken-based Dish Fallback
register_nonveg_food_class(
    NonVegFoodClassRecord(
        canonical_food_id="IND-NV-CH-UNKNOWN-001",
        canonical_name="Chicken-Based Dish (Exact Recipe Uncertain)",
        hierarchy=NonVegHierarchy(
            level3_protein="Chicken",
            level4_region="Pan-India",
            level5_state="Unknown",
            level6_food_family="Chicken Curry",
            level7_specific_dish="Chicken Dish (Recipe Uncertain)",
            level8_variant="Identified as poultry/chicken with visible bone or fibers, but exact regional recipe unknown",
            level9_cooking_method="Simmered",
            level10_bone_state="bone_in",
            level11_portion_type="weight_grams",
            level12_nutrition_ref_id="REF-NV-CH-FALLBACK-001"
        ),
        protein_type="Chicken",
        food_family="Chicken Curry",
        specific_dish="Chicken Dish (Recipe Uncertain)",
        region="Pan-India",
        state_or_city="Pan-India",
        regional_names={"hi": "चिकन व्यंजन (सटीक रेसिपी अनिश्चित)", "ta": "சிக்கன் உணவு (சமையல் முறை உறுதியற்றது)"},
        alternate_names=["chicken dish uncertain", "generic chicken curry", "unidentified chicken dish"],
        cooking_method="Simmered",
        bone_state_default="bone_in",
        typical_cut="curry_cut",
        consistency="Thick gravy",
        gravy_base=["onion", "tomato"],
        is_countable=True,
        piece_count_expected=4,
        default_portion_grams=180.0,
        edible_meat_ratio=0.72,
        nutrition_per_100g={"calories": 175.0, "protein": 17.0, "carbs": 4.5, "fat": 10.0, "fiber": 0.8},
        uncertainty_factors=["recipe_variation", "bone_deduction"],
        typical_oil_level="Moderate visible oil"
    )
)

# Mutton/Goat-style Dish Fallback
register_nonveg_food_class(
    NonVegFoodClassRecord(
        canonical_food_id="IND-NV-MT-UNKNOWN-001",
        canonical_name="Mutton/Goat Meat Dish (Exact Species Uncertain)",
        hierarchy=NonVegHierarchy(
            level3_protein="Mutton/Goat/Lamb",
            level4_region="Pan-India",
            level5_state="Unknown",
            level6_food_family="Mutton Curry",
            level7_specific_dish="Mutton/Goat Dish (Species Uncertain)",
            level8_variant="Red meat curry with bone and dark fibers; exact species (goat vs lamb) unconfirmed",
            level9_cooking_method="Simmered",
            level10_bone_state="bone_in",
            level11_portion_type="weight_grams",
            level12_nutrition_ref_id="REF-NV-MT-FALLBACK-001"
        ),
        protein_type="Goat",
        food_family="Mutton Curry",
        specific_dish="Mutton/Goat Dish (Species Uncertain)",
        region="Pan-India",
        state_or_city="Pan-India",
        regional_names={"hi": "मटन/बकरा मीट (प्रजाति अनिश्चित)", "ta": "ஆட்டுக்கறி உணவு (துல்லியமற்றது)"},
        alternate_names=["mutton dish uncertain", "goat meat curry uncertain", "generic mutton gravy"],
        cooking_method="Simmered",
        bone_state_default="bone_in",
        typical_cut="curry_cut",
        consistency="Thick gravy",
        gravy_base=["onion", "tomato"],
        is_countable=True,
        piece_count_expected=4,
        default_portion_grams=190.0,
        edible_meat_ratio=0.68,
        nutrition_per_100g={"calories": 220.0, "protein": 18.5, "carbs": 3.8, "fat": 14.8, "fiber": 0.7},
        uncertainty_factors=["species_uncertainty", "bone_weight_deduction"],
        typical_oil_level="High visible oil"
    )
)

# Fish Dish Fallback
register_nonveg_food_class(
    NonVegFoodClassRecord(
        canonical_food_id="IND-NV-FS-UNKNOWN-001",
        canonical_name="Fish Curry/Fry (Species Uncertain)",
        hierarchy=NonVegHierarchy(
            level3_protein="Fish",
            level4_region="Pan-India",
            level5_state="Unknown",
            level6_food_family="Fish Curry",
            level7_specific_dish="Fish Dish (Species Uncertain)",
            level8_variant="Flaky fish piece/steak verified, but species unprovable from small curry photo",
            level9_cooking_method="Simmered",
            level10_bone_state="bone_in",
            level11_portion_type="weight_grams",
            level12_nutrition_ref_id="REF-NV-FS-FALLBACK-001"
        ),
        protein_type="Fish",
        food_family="Fish Curry",
        specific_dish="Fish Dish (Species Uncertain)",
        region="Pan-India",
        state_or_city="Pan-India",
        regional_names={"hi": "मछली करी/फ्राई (प्रजाति अनिश्चित)", "ta": "மீன் உணவு (வகை உறுதியற்றது)"},
        alternate_names=["fish curry species uncertain", "fish fry uncertain", "generic fish curry"],
        cooking_method="Simmered",
        bone_state_default="bone_in",
        typical_cut="steak",
        consistency="Thick gravy",
        gravy_base=[],
        is_countable=True,
        piece_count_expected=2,
        default_portion_grams=175.0,
        edible_meat_ratio=0.80,
        nutrition_per_100g={"calories": 145.0, "protein": 16.0, "carbs": 3.0, "fat": 7.5, "fiber": 0.4},
        uncertainty_factors=["fish_species_unverified", "bone_deduction"],
        typical_oil_level="Moderate visible oil"
    )
)

# Seafood Fallback
register_nonveg_food_class(
    NonVegFoodClassRecord(
        canonical_food_id="IND-NV-SF-UNKNOWN-001",
        canonical_name="Seafood Dish (Exact Type Uncertain)",
        hierarchy=NonVegHierarchy(
            level3_protein="Seafood",
            level4_region="Pan-India",
            level5_state="Unknown",
            level6_food_family="Seafood Curry",
            level7_specific_dish="Seafood Dish (Type Uncertain)",
            level8_variant="Seafood pieces (squid, shell, or mixed bits) visible, exact genus uncertain",
            level9_cooking_method="Simmered",
            level10_bone_state="boneless",
            level11_portion_type="weight_grams",
            level12_nutrition_ref_id="REF-NV-SF-FALLBACK-001"
        ),
        protein_type="Seafood",
        food_family="Seafood Curry",
        specific_dish="Seafood Dish (Type Uncertain)",
        region="Pan-India",
        state_or_city="Pan-India",
        regional_names={"hi": "समुद्री भोजन (प्रकार अनिश्चित)", "ta": "கடல் உணவு (வகை உறுதியற்றது)"},
        alternate_names=["seafood uncertain", "shellfish dish uncertain", "generic seafood curry"],
        cooking_method="Simmered",
        bone_state_default="boneless",
        typical_cut="whole",
        consistency="Thick gravy",
        gravy_base=[],
        is_countable=False,
        piece_count_expected=None,
        default_portion_grams=170.0,
        edible_meat_ratio=0.85,
        nutrition_per_100g={"calories": 140.0, "protein": 16.5, "carbs": 3.2, "fat": 6.8, "fiber": 0.4},
        uncertainty_factors=["seafood_type_unverified"],
        typical_oil_level="Moderate visible oil"
    )
)

# Egg Fallback
register_nonveg_food_class(
    NonVegFoodClassRecord(
        canonical_food_id="IND-NV-EG-UNKNOWN-001",
        canonical_name="Egg Dish (Exact Variant Uncertain)",
        hierarchy=NonVegHierarchy(
            level3_protein="Egg",
            level4_region="Pan-India",
            level5_state="Unknown",
            level6_food_family="Egg Curry",
            level7_specific_dish="Egg Dish (Variant Uncertain)",
            level8_variant="Identified egg presence; cooking preparation or count requiring clarification",
            level9_cooking_method="Simmered",
            level10_bone_state="boneless",
            level11_portion_type="piece_count",
            level12_nutrition_ref_id="REF-NV-EG-FALLBACK-001"
        ),
        protein_type="Egg",
        food_family="Egg Curry",
        specific_dish="Egg Dish (Variant Uncertain)",
        region="Pan-India",
        state_or_city="Pan-India",
        regional_names={"hi": "अंडा व्यंजन (प्रकार अनिश्चित)", "ta": "முட்டை உணவு (வகை உறுதியற்றது)"},
        alternate_names=["egg dish uncertain", "generic egg curry", "egg preparation uncertain"],
        cooking_method="Simmered",
        bone_state_default="boneless",
        typical_cut="whole",
        consistency="Thick gravy",
        gravy_base=[],
        is_countable=True,
        piece_count_expected=2,
        default_portion_grams=130.0,
        edible_meat_ratio=1.0,
        nutrition_per_100g={"calories": 165.0, "protein": 11.5, "carbs": 3.5, "fat": 11.5, "fiber": 0.4},
        uncertainty_factors=["egg_count_unverified"],
        typical_oil_level="Moderate visible oil"
    )
)

# Red Meat Fallback (Rule 28 & Section 54)
register_nonveg_food_class(
    NonVegFoodClassRecord(
        canonical_food_id="IND-NV-RM-UNKNOWN-001",
        canonical_name="Red Meat Dish (Exact Species Uncertain)",
        hierarchy=NonVegHierarchy(
            level3_protein="Mutton/Goat/Lamb",
            level4_region="Pan-India",
            level5_state="Unknown",
            level6_food_family="Mutton Curry",
            level7_specific_dish="Red Meat Dish (Species Uncertain)",
            level8_variant="Dark mammalian red meat dish where exact species cannot be established purely from photograph",
            level9_cooking_method="Simmered",
            level10_bone_state="bone_in",
            level11_portion_type="weight_grams",
            level12_nutrition_ref_id="REF-NV-RM-FALLBACK-001"
        ),
        protein_type="Mutton",
        food_family="Mutton Curry",
        specific_dish="Red Meat Dish (Species Uncertain)",
        region="Pan-India",
        state_or_city="Pan-India",
        regional_names={"hi": "लाल मांस व्यंजन (प्रजाति अनिश्चित)", "ta": "சிகப்பு இறைச்சி (வகை உறுதியற்றது)"},
        alternate_names=["red meat dish uncertain", "mammalian meat curry", "unidentified red meat"],
        cooking_method="Simmered",
        bone_state_default="bone_in",
        typical_cut="curry_cut",
        consistency="Thick gravy",
        gravy_base=["onion", "tomato"],
        is_countable=True,
        piece_count_expected=4,
        default_portion_grams=180.0,
        edible_meat_ratio=0.70,
        nutrition_per_100g={"calories": 225.0, "protein": 19.0, "carbs": 3.5, "fat": 15.5, "fiber": 0.6},
        uncertainty_factors=["species_unverified_mutton_vs_beef_vs_pork", "bone_weight_deduction"],
        typical_oil_level="High visible oil"
    )
)


def get_nonveg_food_class(food_id: str) -> Optional[NonVegFoodClassRecord]:
    """Look up a NonVegFoodClassRecord by canonical ID or alias."""
    return NONVEG_TAXONOMY_REGISTRY.get(food_id) or NONVEG_TAXONOMY_REGISTRY.get(food_id.lower())


def resolve_nonveg_food_by_name(name: str) -> Optional[NonVegFoodClassRecord]:
    """Resolve a dish by any English, Hindi, Tamil, regional or alternate name."""
    clean_name = name.lower().strip()
    if clean_name in NONVEG_SYNONYM_LOOKUP:
        canon_id = NONVEG_SYNONYM_LOOKUP[clean_name]
        return NONVEG_TAXONOMY_REGISTRY.get(canon_id)

    # Substring search
    for synonym, canon_id in NONVEG_SYNONYM_LOOKUP.items():
        if len(clean_name) >= 3 and (clean_name in synonym or synonym in clean_name):
            return NONVEG_TAXONOMY_REGISTRY.get(canon_id)

    return None
