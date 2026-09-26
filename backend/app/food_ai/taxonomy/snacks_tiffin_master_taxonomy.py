"""
Indian Snacks & Tiffin Master Taxonomy & Identity Hierarchy (Part 15)
Implements Sections 1–13, 17–29, 40, 41, 51, 63, 64, 74, 75 of Part 15 Specification.

Guarantees:
- Strict 14-Level Identity Traversal:
  Indian Food -> Snacks & Tiffin -> Region -> State -> Snack Family -> Specific Food -> Variant ->
  Main Ingredient -> Flour/Grain/Base -> Cooking Method -> Filling/Topping -> Accompaniment -> Portion -> Weight & Nutrition Ref
- Stable Class ID System: IND-SNK-* and IND-TIF-* formats.
- 30 Master Snack Families (Section 3).
- Comprehensive Regional Coverage:
  * South India (Tamil Nadu, Kerala, Karnataka, Andhra Pradesh, Telangana):
    Medhu Vadai, Masala Vadai, Keerai Vadai, Sambar Vadai, Bajji (Onion, Banana, Chilli, Potato),
    Bonda, Pakoda, Murukku, Thattai, Seedai, Kuzhi Paniyaram, Idiyappam, Puttu, Kozhukattai,
    Sundal, Madras Mixture, Pazham Pori, Unniyappam, Neyyappam, Achappam, Mutta/Veg/Chicken Puffs,
    Maddur Vada, Mysore Bonda, Kodubale, Punugulu, Sarvapindi, Chekkalu, Sakinalu,
    Idli, Dosa, Pongal, Upma, Poori Masala, Appam, Pesarattu, Adai.
  * North India (Punjab, Delhi, UP, Rajasthan, Haryana, etc.):
    Samosa (Punjabi, Mini, Cocktail, Paneer, Keema), Kachori (Khasta Dal, Pyaz, Raj, Matar),
    Pakora (Onion, Paneer, Bread, Palak), Aloo Tikki (Plain, Chole, Stuffed), Bread Roll,
    Dahi Bhalla, Papdi Chaat, Pani Puri, Sev Puri, Bhel Puri, Mathri, Chole Bhature.
  * West India (Maharashtra, Gujarat, Goa):
    Vada Pav, Misal Pav, Sabudana Vada, Sabudana Khichdi, Kothimbir Vadi, Alu Vadi, Thalipeeth,
    Kanda Poha, Pav Bhaji, Bakarwadi, Dhokla, Khaman, Khandvi, Fafda, Gathiya, Handvo,
    Methi Muthia, Khakhra, Thepla, Dabeli, Goan Cutlets.
  * East India (West Bengal, Odisha, Bihar, Jharkhand):
    Singara, Aloo Chop, Beguni, Vegetable Chop, Fish Cutlet, Jhalmuri, Ghugni, Dahibara Aloodum,
    Litti Chokha, Sattu Paratha, Dhuska.
  * Northeast India:
    Momo (Veg, Chicken, Pork, Steamed, Fried, Kothey), Regional Pitha.
  * Namkeen & Street Snacks:
    Mixture, Sev, Bhujia, Kara Boondi, Masala Peanuts.
- Robust Fallback System (Section 51):
  * "Indian snack — exact type uncertain" (IND-SNK-UNKNOWN-001)
  * "Indian fried snack — exact type uncertain" (IND-SNK-FRIED-UNKNOWN-001)
  * "Indian steamed snack — exact type uncertain" (IND-SNK-STEAMED-UNKNOWN-001)
  * "Indian tiffin — exact dish uncertain" (IND-TIF-UNKNOWN-001)
  * "Indian chaat — exact type uncertain" (IND-SNK-CHAAT-UNKNOWN-001)
  * "Mixed snack box — individual components uncertain" (IND-SNK-BOX-UNKNOWN-001)
- Multilingual synonym mappings across 12 Indian languages (Section 41).
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class SnackTiffinHierarchy(BaseModel):
    level1_food: str = "Indian Food"
    level2_macro_category: str = "Snacks & Tiffin"
    level3_region: str              # South India, North India, West India, East India, Northeast India, Pan-India
    level4_state: str               # Tamil Nadu, Kerala, Karnataka, Maharashtra, Gujarat, Punjab, West Bengal, etc.
    level5_snack_family: str        # Steamed Snacks, Fried Snacks, Tiffin, Chaat, Namkeen, Baked Snacks, etc.
    level6_specific_food: str       # Medhu Vadai, Samosa, Dhokla, Khaman, Vada Pav, Pani Puri, Idli, etc.
    level7_variant: str             # e.g., "Crisp fried urad dal doughnut with whole peppercorns & curry leaves"
    level8_main_ingredient: str     # Urad Dal, Potato, Besan, Maida, Rice, Semolina, Sprouted Moth Beans, etc.
    level9_flour_grain_base: str    # Urad dal batter, Besan, Refined flour (Maida), Rice flour, Semolina/Rava, Fermented batter
    level10_cooking_method: str     # Deep Fried, Steamed, Shallow Fried, Pan Fried, Baked, Roasted, Raw/Assembled
    level11_filling_or_topping: str # Spiced potato & peas, Moong dal, Sev, Farsan, Chole, Onion, None
    level12_accompaniment: str      # Coconut chutney, Sambar, Green mint chutney, Saunth, Pav, Lemon wedge
    level13_portion_type: str       # countable_pieces, weight_grams, plate_serving, bowl_serving
    level14_nutrition_ref_id: str


class SnackFoodClassRecord(BaseModel):
    canonical_food_id: str          # Stable ID: IND-SNK-TN-MEDHUVADAI-001, etc.
    canonical_name: str             # Canonical English name
    hierarchy: SnackTiffinHierarchy
    snack_family: str               # High-level family from Section 3
    specific_food: str
    region: str                     # South India, North India, West India, East India, Northeast India, Pan-India
    state_or_city: str
    regional_names: Dict[str, str] = Field(default_factory=dict)
    alternate_names: List[str] = Field(default_factory=list)
    base_ingredient: str            # Urad dal, Besan, Potato, Maida, Rice, Poha, etc.
    cooking_method: str = "Deep Fried" # Deep Fried, Steamed, Shallow Fried, Baked, Assembled
    shape_profile: str = "Round"    # Toroid/Doughnut, Triangular, Spherical, Flat disc, Steamed cake, Roll, Flakes
    is_fried: bool = True
    is_steamed: bool = False
    is_baked: bool = False
    is_chaat: bool = False
    is_tiffin: bool = False
    is_countable: bool = True
    piece_count_expected: Optional[int] = 1
    piece_weight_typical_g: Optional[float] = 45.0
    default_portion_grams: float = 90.0
    density_g_ml: float = 1.05
    nutrition_per_100g: Dict[str, float] = Field(default_factory=dict)
    uncertainty_factors: List[str] = Field(default_factory=list)
    visible_oil_typical: str = "High visible oil" # Low visible oil, Moderate visible oil, High visible oil, Deep-fried
    filling_detected: Optional[str] = None
    common_accompaniments: List[str] = Field(default_factory=list)


SNACKS_TAXONOMY_REGISTRY: Dict[str, SnackFoodClassRecord] = {}
SNACKS_SYNONYM_LOOKUP: Dict[str, str] = {}


def register_snack_food_class(record: SnackFoodClassRecord, alias_ids: Optional[List[str]] = None) -> SnackFoodClassRecord:
    SNACKS_TAXONOMY_REGISTRY[record.canonical_food_id] = record
    SNACKS_TAXONOMY_REGISTRY[record.canonical_food_id.lower()] = record
    if alias_ids:
        for aid in alias_ids:
            SNACKS_TAXONOMY_REGISTRY[aid] = record
            SNACKS_TAXONOMY_REGISTRY[aid.lower()] = record
            SNACKS_SYNONYM_LOOKUP[aid.lower().strip()] = record.canonical_food_id
    SNACKS_SYNONYM_LOOKUP[record.canonical_name.lower().strip()] = record.canonical_food_id
    for alt in record.alternate_names:
        SNACKS_SYNONYM_LOOKUP[alt.lower().strip()] = record.canonical_food_id
    for reg_name in record.regional_names.values():
        SNACKS_SYNONYM_LOOKUP[reg_name.lower().strip()] = record.canonical_food_id
    return record


# =============================================================================
# 1. SOUTH INDIA — TAMIL NADU SNACKS & TIFFIN (Sections 4, 5, 24, 25, 26, 27)
# =============================================================================

# Medhu Vadai / Ulundhu Vadai
register_snack_food_class(
    SnackFoodClassRecord(
        canonical_food_id="IND-SNK-TN-MEDHUVADAI-001",
        canonical_name="Medhu Vadai",
        hierarchy=SnackTiffinHierarchy(
            level3_region="South India",
            level4_state="Tamil Nadu",
            level5_snack_family="Fried Snacks",
            level6_specific_food="Medhu Vadai",
            level7_variant="Crispy golden urad dal doughnut with hole, black peppercorns & curry leaves",
            level8_main_ingredient="Urad Dal",
            level9_flour_grain_base="Wet ground urad dal batter",
            level10_cooking_method="Deep Fried",
            level11_filling_or_topping="Black peppercorns, green chillies, curry leaves, ginger",
            level12_accompaniment="Coconut Chutney, Sambar",
            level13_portion_type="countable_pieces",
            level14_nutrition_ref_id="NUT-SNK-MEDHUVADAI-001",
        ),
        snack_family="Fried Snacks",
        specific_food="Medhu Vadai",
        region="South India",
        state_or_city="Tamil Nadu",
        regional_names={
            "ta": "மெது வடை / உளுந்து வடை",
            "te": "గారెలు / మినప గారెలు",
            "kn": "ಉದ್ದಿನ ವಡೆ",
            "ml": "ഉഴുന്ന് വട",
            "hi": "मेदु वड़ा",
        },
        alternate_names=["Medu Vada", "Ulundhu Vadai", "Urad Vada", "Garelu"],
        base_ingredient="Urad Dal",
        cooking_method="Deep Fried",
        shape_profile="Toroid/Doughnut",
        is_fried=True,
        is_tiffin=True,
        piece_count_expected=2,
        piece_weight_typical_g=45.0,
        default_portion_grams=90.0,
        visible_oil_typical="Deep-fried",
        common_accompaniments=["Coconut Chutney", "Sambar"],
        nutrition_per_100g={"calories": 262.0, "protein": 9.5, "carbs": 28.5, "fat": 12.8, "fiber": 4.8},
        uncertainty_factors=["Oil absorption during deep frying", "Piece size variation (35g to 60g)"],
    ),
    alias_ids=["IND-SNK-TN-ULUNDHUVADAI-001", "IND-TIF-TN-MEDUVADA-001"],
)

# Masala Vadai / Paruppu Vadai / Aama Vadai
register_snack_food_class(
    SnackFoodClassRecord(
        canonical_food_id="IND-SNK-TN-MASALAVADAI-001",
        canonical_name="Masala Vadai",
        hierarchy=SnackTiffinHierarchy(
            level3_region="South India",
            level4_state="Tamil Nadu",
            level5_snack_family="Fried Snacks",
            level6_specific_food="Masala Vadai",
            level7_variant="Coarse, crunchy chana dal flat patty with fennel seeds, onion & dry red chillies",
            level8_main_ingredient="Chana Dal",
            level9_flour_grain_base="Coarsely crushed chana dal",
            level10_cooking_method="Deep Fried",
            level11_filling_or_topping="Fennel seeds (saunf), onions, curry leaves, red chillies",
            level12_accompaniment="Coconut Chutney, Hot Tea",
            level13_portion_type="countable_pieces",
            level14_nutrition_ref_id="NUT-SNK-MASALAVADAI-001",
        ),
        snack_family="Fried Snacks",
        specific_food="Masala Vadai",
        region="South India",
        state_or_city="Tamil Nadu",
        regional_names={
            "ta": "மசால் வடை / பருப்பு வடை",
            "te": "మసాలా వడ",
            "kn": "ಮಸಾಲೆ ವಡೆ",
            "ml": "പരിപ്പ് വട",
            "hi": "मसाला वड़ा",
        },
        alternate_names=["Paruppu Vadai", "Aama Vadai", "Chana Dal Vada", "Parippu Vada"],
        base_ingredient="Chana Dal",
        cooking_method="Deep Fried",
        shape_profile="Flat disc",
        is_fried=True,
        piece_count_expected=2,
        piece_weight_typical_g=40.0,
        default_portion_grams=80.0,
        visible_oil_typical="Deep-fried",
        common_accompaniments=["Coconut Chutney", "Chai"],
        nutrition_per_100g={"calories": 284.0, "protein": 11.2, "carbs": 33.6, "fat": 12.0, "fiber": 6.5},
        uncertainty_factors=["Coarseness of chana dal grind", "Deep frying temperature"],
    ),
    alias_ids=["IND-SNK-TN-PARUPPUVADAI-001", "IND-SNK-KL-PARIPPUVADA-001"],
)

# Sambar Vadai
register_snack_food_class(
    SnackFoodClassRecord(
        canonical_food_id="IND-SNK-TN-SAMBARVADAI-001",
        canonical_name="Sambar Vadai",
        hierarchy=SnackTiffinHierarchy(
            level3_region="South India",
            level4_state="Tamil Nadu",
            level5_snack_family="Tiffin",
            level6_specific_food="Sambar Vadai",
            level7_variant="Deep fried medhu vada submerged and soaked in hot spiced lentil sambar with ghee drop",
            level8_main_ingredient="Urad Dal & Toor Dal",
            level9_flour_grain_base="Soaked urad dal & cooked toor dal gravy",
            level10_cooking_method="Deep Fried then Soaked",
            level11_filling_or_topping="Finely chopped onions, fresh coriander, drop of ghee",
            level12_accompaniment="Coconut Chutney",
            level13_portion_type="plate_serving",
            level14_nutrition_ref_id="NUT-SNK-SAMBARVADAI-001",
        ),
        snack_family="Tiffin",
        specific_food="Sambar Vadai",
        region="South India",
        state_or_city="Tamil Nadu",
        regional_names={"ta": "சாம்பார் வடை", "te": "సాంబార్ వడ", "kn": "ಸಾಂಬಾರ್ ವಡೆ", "hi": "सांबर वड़ा"},
        alternate_names=["Sambar Vada", "Soaked Sambar Vadai"],
        base_ingredient="Urad Dal",
        cooking_method="Deep Fried then Soaked",
        shape_profile="Toroid/Doughnut in gravy",
        is_fried=True,
        is_tiffin=True,
        piece_count_expected=2,
        piece_weight_typical_g=95.0,
        default_portion_grams=190.0,
        visible_oil_typical="Moderate visible oil",
        common_accompaniments=["Coconut Chutney", "Ghee"],
        nutrition_per_100g={"calories": 165.0, "protein": 6.2, "carbs": 21.0, "fat": 6.4, "fiber": 3.8},
        uncertainty_factors=["Sambar absorption ratio (50-80% added weight)", "Ghee topping volume"],
    ),
)

# Thayir Vadai / Dahi Vada (South Indian Style)
register_snack_food_class(
    SnackFoodClassRecord(
        canonical_food_id="IND-SNK-TN-THAYIRVADAI-001",
        canonical_name="Thayir Vadai",
        hierarchy=SnackTiffinHierarchy(
            level3_region="South India",
            level4_state="Tamil Nadu",
            level5_snack_family="Tiffin",
            level6_specific_food="Thayir Vadai",
            level7_variant="Medhu vada soaked in beaten spiced curd with mustard, ginger, green chillies & boondi",
            level8_main_ingredient="Urad Dal & Yogurt",
            level9_flour_grain_base="Urad dal & thick curd",
            level10_cooking_method="Deep Fried then Soaked in Curd",
            level11_filling_or_topping="Mustard-curry leaf tadka, grated carrot, coriander, boondi",
            level12_accompaniment="None",
            level13_portion_type="plate_serving",
            level14_nutrition_ref_id="NUT-SNK-THAYIRVADAI-001",
        ),
        snack_family="Tiffin",
        specific_food="Thayir Vadai",
        region="South India",
        state_or_city="Tamil Nadu",
        regional_names={"ta": "தயிர் வடை", "te": "పెరుగు గారెలు", "kn": "ಮೊಸರು ವಡೆ", "hi": "दही वड़ा दक्षिण भारतीय"},
        alternate_names=["Perugu Garelu", "Mosaru Vade", "Curd Vada"],
        base_ingredient="Urad Dal & Curd",
        cooking_method="Deep Fried then Soaked in Curd",
        shape_profile="Toroid/Doughnut in yogurt",
        is_fried=True,
        is_tiffin=True,
        piece_count_expected=2,
        piece_weight_typical_g=110.0,
        default_portion_grams=220.0,
        visible_oil_typical="Moderate visible oil",
        common_accompaniments=["Kara Boondi", "Grated Carrot"],
        nutrition_per_100g={"calories": 158.0, "protein": 6.5, "carbs": 18.2, "fat": 6.8, "fiber": 2.2},
        uncertainty_factors=["Curd fat percentage (whole milk vs toned)", "Boondi topping quantity"],
    ),
)

# Onion Bajji / Vazhaikkai Bajji / Chilli Bajji (Tamil Nadu)
register_snack_food_class(
    SnackFoodClassRecord(
        canonical_food_id="IND-SNK-TN-ONIONBAJJI-001",
        canonical_name="Onion Bajji",
        hierarchy=SnackTiffinHierarchy(
            level3_region="South India",
            level4_state="Tamil Nadu",
            level5_snack_family="Fried Snacks",
            level6_specific_food="Bajji",
            level7_variant="Thick onion rings dipped in spiced besan-rice flour batter and deep fried golden",
            level8_main_ingredient="Onion & Besan",
            level9_flour_grain_base="Besan & rice flour batter with asafoetida",
            level10_cooking_method="Deep Fried",
            level11_filling_or_topping="Onion slice encased in crisp batter",
            level12_accompaniment="Coconut Chutney",
            level13_portion_type="countable_pieces",
            level14_nutrition_ref_id="NUT-SNK-ONIONBAJJI-001",
        ),
        snack_family="Fried Snacks",
        specific_food="Bajji",
        region="South India",
        state_or_city="Tamil Nadu",
        regional_names={"ta": "வெங்காய பஜ்ஜி", "te": "ఉల్లిపాయ బజ్జి", "kn": "ಈರುಳ್ಳಿ ಬಜ್ಜಿ", "hi": "प्याज भज्जी"},
        alternate_names=["Vengaya Bajji", "Kanda Bhajji South Style", "Onion Fritter"],
        base_ingredient="Besan & Onion",
        cooking_method="Deep Fried",
        shape_profile="Flat disc",
        is_fried=True,
        piece_count_expected=3,
        piece_weight_typical_g=35.0,
        default_portion_grams=105.0,
        visible_oil_typical="Deep-fried",
        common_accompaniments=["Coconut Chutney", "Chilli Sauce"],
        nutrition_per_100g={"calories": 255.0, "protein": 6.8, "carbs": 29.5, "fat": 12.6, "fiber": 3.4},
        uncertainty_factors=["Batter thickness", "Oil absorption"],
    ),
)

register_snack_food_class(
    SnackFoodClassRecord(
        canonical_food_id="IND-SNK-TN-VAZHAIKAIBAJJI-001",
        canonical_name="Banana Bajji",
        hierarchy=SnackTiffinHierarchy(
            level3_region="South India",
            level4_state="Tamil Nadu",
            level5_snack_family="Fried Snacks",
            level6_specific_food="Bajji",
            level7_variant="Thin raw plantain slice dipped in spiced besan batter and fried puffy",
            level8_main_ingredient="Raw Plantain / Raw Banana",
            level9_flour_grain_base="Besan & rice flour batter",
            level10_cooking_method="Deep Fried",
            level11_filling_or_topping="Raw green plantain strip",
            level12_accompaniment="Coconut Chutney",
            level13_portion_type="countable_pieces",
            level14_nutrition_ref_id="NUT-SNK-VAZHAIKAIBAJJI-001",
        ),
        snack_family="Fried Snacks",
        specific_food="Bajji",
        region="South India",
        state_or_city="Tamil Nadu",
        regional_names={"ta": "வாழைக்காய் பஜ்ஜி", "te": "అరటికాయ బజ్జి", "ml": "വാഴക്ക ബജ്ജി", "kn": "ಬಾಳೆಕಾಯಿ ಬಜ್ಜಿ"},
        alternate_names=["Vazhaikkai Bajji", "Raw Banana Bajji", "Plantain Bajji"],
        base_ingredient="Raw Plantain & Besan",
        cooking_method="Deep Fried",
        shape_profile="Oblong slice",
        is_fried=True,
        piece_count_expected=2,
        piece_weight_typical_g=40.0,
        default_portion_grams=80.0,
        visible_oil_typical="Deep-fried",
        common_accompaniments=["Coconut Chutney"],
        nutrition_per_100g={"calories": 240.0, "protein": 5.4, "carbs": 33.2, "fat": 10.2, "fiber": 4.1},
        uncertainty_factors=["Slice thickness", "Oil absorption"],
    ),
)

# Potato Bonda / Aloo Bonda (South Indian Style)
register_snack_food_class(
    SnackFoodClassRecord(
        canonical_food_id="IND-SNK-TN-POTATOBONDA-001",
        canonical_name="Potato Bonda",
        hierarchy=SnackTiffinHierarchy(
            level3_region="South India",
            level4_state="Tamil Nadu",
            level5_snack_family="Fried Snacks",
            level6_specific_food="Bonda",
            level7_variant="Spherical spiced mashed potato ball coated in golden gram flour batter",
            level8_main_ingredient="Potato",
            level9_flour_grain_base="Gram flour (Besan) outer shell",
            level10_cooking_method="Deep Fried",
            level11_filling_or_topping="Mashed potato tempered with mustard, turmeric, ginger, green chillies",
            level12_accompaniment="Coconut Chutney",
            level13_portion_type="countable_pieces",
            level14_nutrition_ref_id="NUT-SNK-POTATOBONDA-001",
        ),
        snack_family="Fried Snacks",
        specific_food="Bonda",
        region="South India",
        state_or_city="Tamil Nadu",
        regional_names={"ta": "உருளைக்கிழங்கு போண்டா", "te": "ఆలూ బోండా", "kn": "ಆಲೂ ಬೋಂಡಾ", "ml": "ബോണ്ട"},
        alternate_names=["Urulaikizhangu Bonda", "Aloo Bonda", "Batata Bonda South"],
        base_ingredient="Potato & Besan",
        cooking_method="Deep Fried",
        shape_profile="Spherical",
        is_fried=True,
        piece_count_expected=2,
        piece_weight_typical_g=55.0,
        default_portion_grams=110.0,
        visible_oil_typical="Deep-fried",
        common_accompaniments=["Coconut Chutney"],
        nutrition_per_100g={"calories": 228.0, "protein": 4.8, "carbs": 31.0, "fat": 9.6, "fiber": 3.0},
        uncertainty_factors=["Potato mash moisture", "Batter coating thickness"],
    ),
)

# Murukku / Thenkuzhal (Tamil Nadu)
register_snack_food_class(
    SnackFoodClassRecord(
        canonical_food_id="IND-SNK-TN-MURUKKU-001",
        canonical_name="Murukku",
        hierarchy=SnackTiffinHierarchy(
            level3_region="South India",
            level4_state="Tamil Nadu",
            level5_snack_family="Namkeen",
            level6_specific_food="Murukku",
            level7_variant="Crisp crunchy spiral extruded from rice flour and urad dal flour with cumin / sesame",
            level8_main_ingredient="Rice Flour & Urad Dal Flour",
            level9_flour_grain_base="Rice flour, roasted urad dal flour, butter",
            level10_cooking_method="Deep Fried",
            level11_filling_or_topping="Sesame seeds, cumin seeds, asafoetida",
            level12_accompaniment="Chai",
            level13_portion_type="weight_grams",
            level14_nutrition_ref_id="NUT-SNK-MURUKKU-001",
        ),
        snack_family="Namkeen",
        specific_food="Murukku",
        region="South India",
        state_or_city="Tamil Nadu",
        regional_names={"ta": "முறுக்கு / தேன்குழல்", "te": "మురుకులు / జంతికలు", "kn": "ಮುರುಕು / ಚಕ್ಕುಲಿ", "ml": "മുറുക്ക്"},
        alternate_names=["Thenkuzhal", "Chakli South Style", "Murukulu", "Jantikalu"],
        base_ingredient="Rice Flour",
        cooking_method="Deep Fried",
        shape_profile="Spiral coil",
        is_fried=True,
        piece_count_expected=3,
        piece_weight_typical_g=20.0,
        default_portion_grams=60.0,
        visible_oil_typical="High visible oil",
        common_accompaniments=["Filter Coffee", "Tea"],
        nutrition_per_100g={"calories": 512.0, "protein": 6.8, "carbs": 63.4, "fat": 26.2, "fiber": 3.8},
        uncertainty_factors=["Butter/ghee addition to dough", "Commercial frying oil reuse"],
    ),
    alias_ids=["IND-SNK-TN-THENKUZHAL-001"],
)

# Thattai / Nippattu (South Indian Crisp Disc)
register_snack_food_class(
    SnackFoodClassRecord(
        canonical_food_id="IND-SNK-TN-THATTAI-001",
        canonical_name="Thattai",
        hierarchy=SnackTiffinHierarchy(
            level3_region="South India",
            level4_state="Tamil Nadu",
            level5_snack_family="Namkeen",
            level6_specific_food="Thattai",
            level7_variant="Crispy, thin flattened round crackers made of rice flour, chana dal & curry leaves",
            level8_main_ingredient="Rice Flour",
            level9_flour_grain_base="Rice flour, roasted gram flour, soaked chana dal",
            level10_cooking_method="Deep Fried",
            level11_filling_or_topping="Soaked chana dal, sesame seeds, curry leaves, red chilli powder",
            level12_accompaniment="Chai",
            level13_portion_type="countable_pieces",
            level14_nutrition_ref_id="NUT-SNK-THATTAI-001",
        ),
        snack_family="Namkeen",
        specific_food="Thattai",
        region="South India",
        state_or_city="Tamil Nadu",
        regional_names={"ta": "தட்டை", "te": "చెక్కలు", "kn": "ನಿಪ್ಪಟ್ಟು", "ml": "തട്ട"},
        alternate_names=["Nippattu", "Chekkalu", "Pappu Chekkalu"],
        base_ingredient="Rice Flour",
        cooking_method="Deep Fried",
        shape_profile="Flat disc",
        is_fried=True,
        piece_count_expected=3,
        piece_weight_typical_g=15.0,
        default_portion_grams=45.0,
        visible_oil_typical="High visible oil",
        common_accompaniments=["Coffee", "Tea"],
        nutrition_per_100g={"calories": 498.0, "protein": 7.4, "carbs": 61.2, "fat": 24.8, "fiber": 4.2},
        uncertainty_factors=["Disc thickness", "Nut/seed density"],
    ),
)

# Kuzhi Paniyaram (Kara / Savory Paniyaram)
register_snack_food_class(
    SnackFoodClassRecord(
        canonical_food_id="IND-SNK-TN-PANIYARAM-001",
        canonical_name="Kuzhi Paniyaram",
        hierarchy=SnackTiffinHierarchy(
            level3_region="South India",
            level4_state="Tamil Nadu",
            level5_snack_family="Pan-Fried Snacks",
            level6_specific_food="Paniyaram",
            level7_variant="Fermented rice and urad dal batter pan-fried in special indented appe/paniyaram pan",
            level8_main_ingredient="Fermented Rice & Urad Dal Batter",
            level9_flour_grain_base="Idli-dosa fermented batter with onions & mustard tempering",
            level10_cooking_method="Pan Fried",
            level11_filling_or_topping="Mustard seeds, green chillies, curry leaves, chopped shallots",
            level12_accompaniment="Kara Chutney, Coconut Chutney",
            level13_portion_type="countable_pieces",
            level14_nutrition_ref_id="NUT-SNK-PANIYARAM-001",
        ),
        snack_family="Pan-Fried Snacks",
        specific_food="Paniyaram",
        region="South India",
        state_or_city="Tamil Nadu",
        regional_names={"ta": "குழி பணியாரம் / கார பணியாரம்", "te": "గుంత పొంగనాలు", "kn": "ಪಡ್ಡು", "ml": "ഉണ്ണിയപ്പം സ്റ്റൈൽ പണിയാരം", "mr": "आप्पे"},
        alternate_names=["Kara Paniyaram", "Gunta Ponganalu", "Paddu", "Appe"],
        base_ingredient="Fermented Rice & Dal Batter",
        cooking_method="Pan Fried",
        shape_profile="Hemispherical dumpling",
        is_fried=False,
        is_tiffin=True,
        piece_count_expected=6,
        piece_weight_typical_g=25.0,
        default_portion_grams=150.0,
        visible_oil_typical="Moderate visible oil",
        common_accompaniments=["Tomato Kara Chutney", "Coconut Chutney"],
        nutrition_per_100g={"calories": 182.0, "protein": 5.1, "carbs": 31.4, "fat": 4.2, "fiber": 2.5},
        uncertainty_factors=["Oil applied per mold cavity", "Batter fermentation acidity"],
    ),
    alias_ids=["IND-SNK-AP-PONGANALU-001", "IND-SNK-KA-PADDU-001", "IND-SNK-MH-APPE-001"],
)

# Idli (South Indian Steamed Rice Cake - Master Tiffin)
register_snack_food_class(
    SnackFoodClassRecord(
        canonical_food_id="IND-TIF-TN-IDLI-001",
        canonical_name="Idli",
        hierarchy=SnackTiffinHierarchy(
            level3_region="South India",
            level4_state="Tamil Nadu",
            level5_snack_family="Steamed Snacks",
            level6_specific_food="Idli",
            level7_variant="Fluffy, soft, pillowy steamed fermented rice and black gram (urad dal) disc",
            level8_main_ingredient="Parboiled Rice & Urad Dal",
            level9_flour_grain_base="Fermented rice & urad dal wet batter",
            level10_cooking_method="Steamed",
            level11_filling_or_topping="None",
            level12_accompaniment="Sambar, Coconut Chutney, Tomato Chutney, Idli Podi with Sesame Oil",
            level13_portion_type="countable_pieces",
            level14_nutrition_ref_id="NUT-TIF-IDLI-001",
        ),
        snack_family="Steamed Snacks",
        specific_food="Idli",
        region="South India",
        state_or_city="Tamil Nadu",
        regional_names={"ta": "இட்லி", "te": "ఇడ్లీ", "kn": "ಇಡ್ಲಿ", "ml": "ഇഡ്ഡലി", "hi": "इडली"},
        alternate_names=["Steamed Rice Cake", "Malli Poo Idli"],
        base_ingredient="Rice & Urad Dal",
        cooking_method="Steamed",
        shape_profile="Disc",
        is_fried=False,
        is_steamed=True,
        is_tiffin=True,
        piece_count_expected=3,
        piece_weight_typical_g=45.0,
        default_portion_grams=135.0,
        visible_oil_typical="Low visible oil",
        common_accompaniments=["Sambar", "Coconut Chutney", "Idli Podi"],
        nutrition_per_100g={"calories": 136.0, "protein": 4.8, "carbs": 27.2, "fat": 0.6, "fiber": 2.1},
        uncertainty_factors=["Piece size (regular 45g vs thatte 120g vs mini button 10g)", "Added oil on plate"],
    ),
)

# Masala Dosa (Master South Indian Tiffin)
register_snack_food_class(
    SnackFoodClassRecord(
        canonical_food_id="IND-TIF-TN-MASALADOSA-001",
        canonical_name="Masala Dosa",
        hierarchy=SnackTiffinHierarchy(
            level3_region="South India",
            level4_state="Tamil Nadu",
            level5_snack_family="Tiffin",
            level6_specific_food="Dosa",
            level7_variant="Crispy, thin golden fermented crepe folded over spiced mashed potato-onion filling",
            level8_main_ingredient="Rice & Urad Dal",
            level9_flour_grain_base="Fermented rice and urad dal batter",
            level10_cooking_method="Shallow Fried",
            level11_filling_or_topping="Spiced potato masala (boiled potato, onion, green chilli, turmeric)",
            level12_accompaniment="Sambar, Coconut Chutney, Tomato Chutney",
            level13_portion_type="plate_serving",
            level14_nutrition_ref_id="NUT-TIF-MASALADOSA-001",
        ),
        snack_family="Tiffin",
        specific_food="Dosa",
        region="South India",
        state_or_city="Tamil Nadu",
        regional_names={"ta": "மசாலா தோசை", "te": "మసాలా దోశ", "kn": "ಮಸಾಲೆ ದೋಸೆ", "ml": "മസാല ദോശ", "hi": "मसाला डोसा"},
        alternate_names=["Mysore Masala Dosa", "Crispy Masala Dosai"],
        base_ingredient="Rice & Urad Dal",
        cooking_method="Shallow Fried",
        shape_profile="Rolled/Folded crepe",
        is_fried=False,
        is_tiffin=True,
        piece_count_expected=1,
        piece_weight_typical_g=180.0,
        default_portion_grams=180.0,
        visible_oil_typical="Moderate visible oil",
        common_accompaniments=["Sambar", "Coconut Chutney"],
        nutrition_per_100g={"calories": 185.0, "protein": 4.2, "carbs": 29.8, "fat": 5.6, "fiber": 2.4},
        uncertainty_factors=["Ghee / oil brushed onto crepe (5g to 25g)", "Potato filling mass"],
    ),
    alias_ids=["IND-TIF-KA-MYSOREMASALADOSA-001"],
)

# Ven Pongal (South Indian Tiffin)
register_snack_food_class(
    SnackFoodClassRecord(
        canonical_food_id="IND-TIF-TN-VENPONGAL-001",
        canonical_name="Ven Pongal",
        hierarchy=SnackTiffinHierarchy(
            level3_region="South India",
            level4_state="Tamil Nadu",
            level5_snack_family="Tiffin",
            level6_specific_food="Pongal",
            level7_variant="Comforting savory porridge of rice and moong dal tempered with ghee, cumin, pepper & cashews",
            level8_main_ingredient="Raw Rice & Moong Dal",
            level9_flour_grain_base="Rice and split yellow moong dal cooked to soft mash",
            level10_cooking_method="Boiled and Tempered",
            level11_filling_or_topping="Ghee, whole black peppercorns, cumin seeds, ginger, curry leaves, roasted cashews",
            level12_accompaniment="Sambar, Coconut Chutney, Medhu Vadai",
            level13_portion_type="bowl_serving",
            level14_nutrition_ref_id="NUT-TIF-VENPONGAL-001",
        ),
        snack_family="Tiffin",
        specific_food="Pongal",
        region="South India",
        state_or_city="Tamil Nadu",
        regional_names={"ta": "வெண் பொங்கல்", "te": "వెన్న పొంగలి / కట్టు పొంగలి", "kn": "ಖಾರಾ ಪೊಂಗಲ್", "ml": "വെൺ പൊങ്കൽ", "hi": "वेन पोंगल"},
        alternate_names=["Khara Pongal", "Katla Pongali", "Ghee Pongal"],
        base_ingredient="Rice & Moong Dal",
        cooking_method="Boiled and Tempered",
        shape_profile="Mound/Porridge",
        is_fried=False,
        is_tiffin=True,
        piece_count_expected=None,
        piece_weight_typical_g=None,
        default_portion_grams=200.0,
        visible_oil_typical="High visible oil",
        common_accompaniments=["Sambar", "Coconut Chutney", "Medhu Vadai"],
        nutrition_per_100g={"calories": 194.0, "protein": 5.2, "carbs": 26.5, "fat": 7.8, "fiber": 2.2},
        uncertainty_factors=["Ghee quantity added (generous halwai style vs light homemade)"],
    ),
)


# =============================================================================
# 2. SOUTH INDIA — KERALA SNACKS & TIFFIN (Section 6)
# =============================================================================

# Pazham Pori (Ethakka Appam - Kerala Ripe Banana Fritters)
register_snack_food_class(
    SnackFoodClassRecord(
        canonical_food_id="IND-SNK-KL-PAZHAMPORI-001",
        canonical_name="Pazham Pori",
        hierarchy=SnackTiffinHierarchy(
            level3_region="South India",
            level4_state="Kerala",
            level5_snack_family="Fried Snacks",
            level6_specific_food="Pazham Pori",
            level7_variant="Ripe Nendran banana slices dipped in lightly sweetened all-purpose flour batter and deep fried",
            level8_main_ingredient="Nendran Banana",
            level9_flour_grain_base="Maida, pinch of turmeric, sugar & cumin/cardamom",
            level10_cooking_method="Deep Fried",
            level11_filling_or_topping="Sweet ripe banana core",
            level12_accompaniment="Chai",
            level13_portion_type="countable_pieces",
            level14_nutrition_ref_id="NUT-SNK-PAZHAMPORI-001",
        ),
        snack_family="Fried Snacks",
        specific_food="Pazham Pori",
        region="South India",
        state_or_city="Kerala",
        regional_names={"ml": "പഴം പൊരി / ഏത്തക്ക അപ്പം", "ta": "பழம் பொரி", "hi": "पझम पोरी / केला पकौड़ा"},
        alternate_names=["Ethakka Appam", "Kerala Banana Fritter", "Pazham Baji"],
        base_ingredient="Ripe Nendran Banana",
        cooking_method="Deep Fried",
        shape_profile="Oblong slice",
        is_fried=True,
        piece_count_expected=2,
        piece_weight_typical_g=60.0,
        default_portion_grams=120.0,
        visible_oil_typical="Deep-fried",
        common_accompaniments=["Kerala Black Tea", "Milk Tea"],
        nutrition_per_100g={"calories": 242.0, "protein": 3.1, "carbs": 43.5, "fat": 6.8, "fiber": 3.2},
        uncertainty_factors=["Sugar content of banana and batter", "Oil frying duration"],
    ),
)

# Unniyappam (Kerala Sweet Rice & Jaggery Fritter)
register_snack_food_class(
    SnackFoodClassRecord(
        canonical_food_id="IND-SNK-KL-UNNIYAPPAM-001",
        canonical_name="Unniyappam",
        hierarchy=SnackTiffinHierarchy(
            level3_region="South India",
            level4_state="Kerala",
            level5_snack_family="Pan-Fried Snacks",
            level6_specific_food="Unniyappam",
            level7_variant="Small round spongy sweet fritter made of rice, jaggery, mashed banana & fried coconut bites",
            level8_main_ingredient="Rice & Jaggery",
            level9_flour_grain_base="Ground raw rice, melted jaggery syrup, banana mash",
            level10_cooking_method="Pan Fried in Oil/Ghee",
            level11_filling_or_topping="Ghee-roasted coconut bits (thenga kothu), sesame seeds, cardamom",
            level12_accompaniment="Tea",
            level13_portion_type="countable_pieces",
            level14_nutrition_ref_id="NUT-SNK-UNNIYAPPAM-001",
        ),
        snack_family="Pan-Fried Snacks",
        specific_food="Unniyappam",
        region="South India",
        state_or_city="Kerala",
        regional_names={"ml": "ഉണ്ണിയപ്പം", "ta": "உண்ணியப்பம்", "hi": "उन्नियप्पम"},
        alternate_names=["Neyyappam Variant", "Kerala Sweet Paniyaram"],
        base_ingredient="Rice & Jaggery",
        cooking_method="Pan Fried",
        shape_profile="Hemispherical dumpling",
        is_fried=True,
        piece_count_expected=4,
        piece_weight_typical_g=30.0,
        default_portion_grams=120.0,
        visible_oil_typical="High visible oil",
        common_accompaniments=["Chai"],
        nutrition_per_100g={"calories": 310.0, "protein": 3.8, "carbs": 56.4, "fat": 8.5, "fiber": 2.4},
        uncertainty_factors=["Ghee vs coconut oil frying", "Jaggery sweetness concentration"],
    ),
)

# Egg Puffs / Mutta Puffs (Kerala Bakery Snack)
register_snack_food_class(
    SnackFoodClassRecord(
        canonical_food_id="IND-SNK-KL-EGGBPUFF-001",
        canonical_name="Egg Puff",
        hierarchy=SnackTiffinHierarchy(
            level3_region="South India",
            level4_state="Kerala",
            level5_snack_family="Baked Snacks",
            level6_specific_food="Egg Puff",
            level7_variant="Flaky laminated golden puff pastry encasing hard-boiled egg half in spicy onion-tomato masala",
            level8_main_ingredient="Egg & All-Purpose Flour",
            level9_flour_grain_base="Laminated puff pastry dough with butter/shortening",
            level10_cooking_method="Baked",
            level11_filling_or_topping="Half hard-boiled egg with caramelized onion, ginger, garam masala",
            level12_accompaniment="Tomato Ketchup",
            level13_portion_type="countable_pieces",
            level14_nutrition_ref_id="NUT-SNK-EGGPUFF-001",
        ),
        snack_family="Baked Snacks",
        specific_food="Egg Puff",
        region="South India",
        state_or_city="Kerala",
        regional_names={"ml": "മുട്ട പഫ്സ്", "ta": "முட்டை பஃப்ஸ்", "hi": "अंडा पफ"},
        alternate_names=["Mutta Puffs", "Bakery Egg Puff"],
        base_ingredient="Puff Pastry & Egg",
        cooking_method="Baked",
        shape_profile="Rectangular folded pastry",
        is_fried=False,
        is_baked=True,
        piece_count_expected=1,
        piece_weight_typical_g=110.0,
        default_portion_grams=110.0,
        visible_oil_typical="Moderate visible oil",
        common_accompaniments=["Tomato Ketchup"],
        nutrition_per_100g={"calories": 325.0, "protein": 8.5, "carbs": 32.0, "fat": 18.2, "fiber": 1.8},
        uncertainty_factors=["Bakery margarine/butter lamination ratio", "Masala volume"],
    ),
)


# =============================================================================
# 3. SOUTH INDIA — KARNATAKA SNACKS (Section 7)
# =============================================================================

# Maddur Vada (Karnataka Classic)
register_snack_food_class(
    SnackFoodClassRecord(
        canonical_food_id="IND-SNK-KA-MADDURVADA-001",
        canonical_name="Maddur Vada",
        hierarchy=SnackTiffinHierarchy(
            level3_region="South India",
            level4_state="Karnataka",
            level5_snack_family="Fried Snacks",
            level6_specific_food="Maddur Vada",
            level7_variant="Crispy outer edges with soft chewy center; semolina, rice flour, maida dough packed with sliced onions",
            level8_main_ingredient="Semolina, Rice Flour & Onions",
            level9_flour_grain_base="Rava, maida, rice flour rubbed with hot oil",
            level10_cooking_method="Deep Fried",
            level11_filling_or_topping="Abundant thinly sliced onions, green chillies, ginger, curry leaves",
            level12_accompaniment="Coconut Chutney",
            level13_portion_type="countable_pieces",
            level14_nutrition_ref_id="NUT-SNK-MADDURVADA-001",
        ),
        snack_family="Fried Snacks",
        specific_food="Maddur Vada",
        region="South India",
        state_or_city="Karnataka",
        regional_names={"kn": "ಮದ್ದೂರು ವಡೆ", "ta": "மத்தூர் வடை", "te": "మద్దూరు వడ", "hi": "मद्दूर वड़ा"},
        alternate_names=["Maddur Vadai", "Karnataka Maddur Vada"],
        base_ingredient="Rava, Rice Flour & Onions",
        cooking_method="Deep Fried",
        shape_profile="Flat disc with ruffled edges",
        is_fried=True,
        piece_count_expected=2,
        piece_weight_typical_g=50.0,
        default_portion_grams=100.0,
        visible_oil_typical="Deep-fried",
        common_accompaniments=["Coconut Chutney", "Filter Coffee"],
        nutrition_per_100g={"calories": 340.0, "protein": 6.2, "carbs": 44.5, "fat": 15.6, "fiber": 3.2},
        uncertainty_factors=["Hot oil dough-kneading ratio", "Fried crispness level"],
    ),
)

# Mysore Bonda / Mangalore Bonda
register_snack_food_class(
    SnackFoodClassRecord(
        canonical_food_id="IND-SNK-KA-MYSOREBONDA-001",
        canonical_name="Mysore Bonda",
        hierarchy=SnackTiffinHierarchy(
            level3_region="South India",
            level4_state="Karnataka",
            level5_snack_family="Fried Snacks",
            level6_specific_food="Mysore Bonda",
            level7_variant="Golden spherical fritter, crispy crust with pillowy soft aerated sour curd & maida crumb",
            level8_main_ingredient="Maida & Curd",
            level9_flour_grain_base="Refined flour fermented briefly with sour yogurt and cumin",
            level10_cooking_method="Deep Fried",
            level11_filling_or_topping="Crushed cumin, ginger, chopped green chillies, fresh coconut pieces",
            level12_accompaniment="Coconut Chutney, Ginger Chutney",
            level13_portion_type="countable_pieces",
            level14_nutrition_ref_id="NUT-SNK-MYSOREBONDA-001",
        ),
        snack_family="Fried Snacks",
        specific_food="Mysore Bonda",
        region="South India",
        state_or_city="Karnataka",
        regional_names={"kn": "ಮಂಗಳೂರು ಬೋಂಡಾ / ಮೈಸೂರು ಬೋಂಡಾ", "te": "మైసూర్ బోండా", "ta": "மைசூர் போண்டா", "hi": "मैसूर बोंडा"},
        alternate_names=["Mangalore Bonda", "Goli Baje", "Mysore Baji"],
        base_ingredient="Maida & Curd",
        cooking_method="Deep Fried",
        shape_profile="Spherical",
        is_fried=True,
        piece_count_expected=4,
        piece_weight_typical_g=35.0,
        default_portion_grams=140.0,
        visible_oil_typical="Deep-fried",
        common_accompaniments=["Coconut Chutney", "Allam Chutney"],
        nutrition_per_100g={"calories": 286.0, "protein": 6.0, "carbs": 38.4, "fat": 12.2, "fiber": 1.8},
        uncertainty_factors=["Maida to curd fermentation time", "Oil entrapment in spongy crumb"],
    ),
    alias_ids=["IND-SNK-KA-GOLIBAJE-001", "IND-SNK-AP-MYSOREBONDA-001"],
)


# =============================================================================
# 4. SOUTH INDIA — ANDHRA PRADESH & TELANGANA (Sections 8, 9)
# =============================================================================

# Punugulu (Andhra Crisp Street Fritters)
register_snack_food_class(
    SnackFoodClassRecord(
        canonical_food_id="IND-SNK-AP-PUNUGULU-001",
        canonical_name="Punugulu",
        hierarchy=SnackTiffinHierarchy(
            level3_region="South India",
            level4_state="Andhra Pradesh",
            level5_snack_family="Street Snacks",
            level6_specific_food="Punugulu",
            level7_variant="Bite-sized crispy deep-fried drop fritters made from slightly sour leftover dosa/idli batter",
            level8_main_ingredient="Fermented Dosa Batter & Maida/Rice Flour",
            level9_flour_grain_base="Fermented rice-dal batter bound with a little flour",
            level10_cooking_method="Deep Fried",
            level11_filling_or_topping="Cumin seeds, onions, green chillies, curry leaves",
            level12_accompaniment="Peanut Chutney, Tomato Chutney",
            level13_portion_type="countable_pieces",
            level14_nutrition_ref_id="NUT-SNK-PUNUGULU-001",
        ),
        snack_family="Street Snacks",
        specific_food="Punugulu",
        region="South India",
        state_or_city="Andhra Pradesh",
        regional_names={"te": "పునుగులు", "ta": "புனுகுலு", "kn": "ಪುನುಗುಲು", "hi": "पुनुगुलु"},
        alternate_names=["Punukulu", "Andhra Bonda Drops", "Street Punugulu"],
        base_ingredient="Fermented Dosa Batter",
        cooking_method="Deep Fried",
        shape_profile="Small spherical drops",
        is_fried=True,
        piece_count_expected=8,
        piece_weight_typical_g=15.0,
        default_portion_grams=120.0,
        visible_oil_typical="Deep-fried",
        common_accompaniments=["Palli Chutney", "Tomato Chutney", "Onions"],
        nutrition_per_100g={"calories": 272.0, "protein": 5.8, "carbs": 37.6, "fat": 11.5, "fiber": 2.6},
        uncertainty_factors=["Piece count (6 to 12 pieces per serving)", "Oil absorption"],
    ),
    alias_ids=["IND-SNK-TS-PUNUGULU-001"],
)

# Sarvapindi (Telangana Rice Flour Pan-Crisp)
register_snack_food_class(
    SnackFoodClassRecord(
        canonical_food_id="IND-SNK-TS-SARVAPINDI-001",
        canonical_name="Sarvapindi",
        hierarchy=SnackTiffinHierarchy(
            level3_region="South India",
            level4_state="Telangana",
            level5_snack_family="Pan-Fried Snacks",
            level6_specific_food="Sarvapindi",
            level7_variant="Rustic savory rice flour pancake pressed into deep metal pan with characteristic vent holes",
            level8_main_ingredient="Rice Flour & Chana Dal",
            level9_flour_grain_base="Rice flour dough with peanuts, chana dal & sesame",
            level10_cooking_method="Shallow/Pan Fried",
            level11_filling_or_topping="Soaked chana dal, peanuts, white sesame seeds, spring onions, curry leaves",
            level12_accompaniment="Tomato Chutney, Curd",
            level13_portion_type="countable_pieces",
            level14_nutrition_ref_id="NUT-SNK-SARVAPINDI-001",
        ),
        snack_family="Pan-Fried Snacks",
        specific_food="Sarvapindi",
        region="South India",
        state_or_city="Telangana",
        regional_names={"te": "సర్వపిండి / గిన్నెప్ప", "hi": "सर्वपिंडी"},
        alternate_names=["Ginnappa", "Tappachinchalu", "Telangana Rice Crisp"],
        base_ingredient="Rice Flour",
        cooking_method="Pan Fried",
        shape_profile="Large disc with holes",
        is_fried=False,
        piece_count_expected=1,
        piece_weight_typical_g=120.0,
        default_portion_grams=120.0,
        visible_oil_typical="Moderate visible oil",
        common_accompaniments=["Tomato Chutney"],
        nutrition_per_100g={"calories": 268.0, "protein": 6.8, "carbs": 44.0, "fat": 7.5, "fiber": 3.8},
        uncertainty_factors=["Peanut and sesame seed density", "Oil used in pan depressions"],
    ),
)


# =============================================================================
# 5. NORTH INDIA — SAMOSA, KACHORI, FRIED SNACKS & CHAAT (Sections 10–16)
# =============================================================================

# Aloo Samosa / Punjabi Samosa (Master Samosa Class)
register_snack_food_class(
    SnackFoodClassRecord(
        canonical_food_id="IND-SNK-NI-SAMOSA-001",
        canonical_name="Samosa",
        hierarchy=SnackTiffinHierarchy(
            level3_region="North India",
            level4_state="Punjab",
            level5_snack_family="Fried Snacks",
            level6_specific_food="Samosa",
            level7_variant="Pyramidal/triangular crispy flaky pastry stuffed with spiced potatoes, green peas, cumin & coriander",
            level8_main_ingredient="Potato & Refined Flour (Maida)",
            level9_flour_grain_base="Maida shortcrust pastry kneaded with ajwain and moin (ghee/oil)",
            level10_cooking_method="Deep Fried",
            level11_filling_or_topping="Boiled potatoes, green peas, garam masala, whole coriander seeds, amchur",
            level12_accompaniment="Mint Coriander Chutney, Saunth (Tamarind Sweet Chutney)",
            level13_portion_type="countable_pieces",
            level14_nutrition_ref_id="NUT-SNK-SAMOSA-001",
        ),
        snack_family="Fried Snacks",
        specific_food="Samosa",
        region="North India",
        state_or_city="Punjab",
        regional_names={
            "hi": "समोसा / पंजाबी समोसा",
            "pa": "ਸਮੋਸਾ",
            "bn": "সিঙাড়া",
            "te": "సమోసా",
            "ta": "சமோசா",
            "gu": "સમોસા",
            "mr": "समोसा",
        },
        alternate_names=["Punjabi Samosa", "Aloo Samosa", "Halwai Samosa"],
        base_ingredient="Potato & Maida",
        cooking_method="Deep Fried",
        shape_profile="Pyramidal/Triangular",
        is_fried=True,
        piece_count_expected=2,
        piece_weight_typical_g=85.0,
        default_portion_grams=170.0,
        visible_oil_typical="Deep-fried",
        filling_detected="Spiced Potato & Green Peas",
        common_accompaniments=["Green Mint Chutney", "Saunth Tamarind Chutney", "Fried Green Chilli"],
        nutrition_per_100g={"calories": 262.0, "protein": 4.5, "carbs": 32.8, "fat": 12.8, "fiber": 3.2},
        uncertainty_factors=["Crust thickness and moin fat content", "Commercial frying oil absorption", "Piece weight (60g to 110g)"],
    ),
    alias_ids=["IND-SNK-NI-PUNJABISAMOSA-001", "IND-SNK-NI-ALOOSAMOSA-001"],
)

# Pyaz Kachori (Rajasthan Classic)
register_snack_food_class(
    SnackFoodClassRecord(
        canonical_food_id="IND-SNK-NI-PYAZKACHORI-001",
        canonical_name="Pyaz Kachori",
        hierarchy=SnackTiffinHierarchy(
            level3_region="North India",
            level4_state="Rajasthan",
            level5_snack_family="Fried Snacks",
            level6_specific_food="Kachori",
            level7_variant="Large flaky puffed disc stuffed with spicy caramelized onion, gram flour & aromatic spices",
            level8_main_ingredient="Onion & Maida",
            level9_flour_grain_base="Maida flaky crust fried low and slow",
            level10_cooking_method="Deep Fried",
            level11_filling_or_topping="Caramelized onions, roasted besan, fennel seeds, nigella (kalonji), chilli powder",
            level12_accompaniment="Saunth Tamarind Chutney, Mint Chutney",
            level13_portion_type="countable_pieces",
            level14_nutrition_ref_id="NUT-SNK-PYAZKACHORI-001",
        ),
        snack_family="Fried Snacks",
        specific_food="Kachori",
        region="North India",
        state_or_city="Rajasthan",
        regional_names={"hi": "प्याज की कचौड़ी", "rj": "कांदा कचौरी", "gu": "ડુંગળી કચોરી"},
        alternate_names=["Pyaaz Kachori", "Jodhpur Pyaz Kachori", "Onion Kachori"],
        base_ingredient="Onion & Maida",
        cooking_method="Deep Fried",
        shape_profile="Puffed disc",
        is_fried=True,
        piece_count_expected=1,
        piece_weight_typical_g=120.0,
        default_portion_grams=120.0,
        visible_oil_typical="Deep-fried",
        filling_detected="Spiced Onion & Roasted Besan",
        common_accompaniments=["Saunth", "Hari Chutney"],
        nutrition_per_100g={"calories": 320.0, "protein": 5.4, "carbs": 38.6, "fat": 16.4, "fiber": 3.6},
        uncertainty_factors=["Large piece size (100g to 150g)", "High fat absorption in flaky crust"],
    ),
)

# Khasta Dal Kachori (Moong Dal Kachori)
register_snack_food_class(
    SnackFoodClassRecord(
        canonical_food_id="IND-SNK-NI-DALKACHORI-001",
        canonical_name="Dal Kachori",
        hierarchy=SnackTiffinHierarchy(
            level3_region="North India",
            level4_state="Uttar Pradesh",
            level5_snack_family="Fried Snacks",
            level6_specific_food="Kachori",
            level7_variant="Crisp, hollow, flaky golden fried ball stuffed with spicy coarse moong dal masala & hing",
            level8_main_ingredient="Moong Dal & Maida",
            level9_flour_grain_base="Crisp flaky maida shell",
            level10_cooking_method="Deep Fried",
            level11_filling_or_topping="Coarse ground moong dal sautéed with asafoetida (hing), fennel & garam masala",
            level12_accompaniment="Aloo Rasedar Curry, Tamarind Chutney",
            level13_portion_type="countable_pieces",
            level14_nutrition_ref_id="NUT-SNK-DALKACHORI-001",
        ),
        snack_family="Fried Snacks",
        specific_food="Kachori",
        region="North India",
        state_or_city="Uttar Pradesh",
        regional_names={"hi": "खस्ता दाल कचौड़ी", "bn": "ডাল কচুরি", "gu": "દાળ કચોરી"},
        alternate_names=["Moong Dal Kachori", "Khasta Kachori", "Hing Kachori"],
        base_ingredient="Moong Dal & Maida",
        cooking_method="Deep Fried",
        shape_profile="Puffed sphere/disc",
        is_fried=True,
        piece_count_expected=2,
        piece_weight_typical_g=65.0,
        default_portion_grams=130.0,
        visible_oil_typical="Deep-fried",
        filling_detected="Spiced Moong Dal with Hing",
        common_accompaniments=["Aloo Sabzi", "Tamarind Chutney"],
        nutrition_per_100g={"calories": 338.0, "protein": 7.8, "carbs": 42.0, "fat": 15.8, "fiber": 4.5},
        uncertainty_factors=["Crust thickness vs dry hollow cavity"],
    ),
)

# Aloo Tikki (Section 14)
register_snack_food_class(
    SnackFoodClassRecord(
        canonical_food_id="IND-SNK-NI-ALOOTIKKI-001",
        canonical_name="Aloo Tikki",
        hierarchy=SnackTiffinHierarchy(
            level3_region="North India",
            level4_state="Delhi",
            level5_snack_family="Pan-Fried Snacks",
            level6_specific_food="Aloo Tikki",
            level7_variant="Shallow fried crispy spiced potato patty seared on large flat tawa until golden brown",
            level8_main_ingredient="Potato",
            level9_flour_grain_base="Boiled mashed potato bound with cornstarch/bread crumbs or pure potato starch",
            level10_cooking_method="Shallow Fried",
            level11_filling_or_topping="Optional spiced chana dal or green peas core",
            level12_accompaniment="Chole, Sweet Tamarind Chutney, Mint Green Chutney, Dahi, Sev, Onions",
            level13_portion_type="countable_pieces",
            level14_nutrition_ref_id="NUT-SNK-ALOOTIKKI-001",
        ),
        snack_family="Pan-Fried Snacks",
        specific_food="Aloo Tikki",
        region="North India",
        state_or_city="Delhi",
        regional_names={"hi": "आलू टिक्की", "pa": "ਆਲੂ ਟਿੱਕੀ", "bn": "আলু টিক্কি"},
        alternate_names=["Crispy Aloo Patty", "Tawa Tikki", "Delhi Aloo Tikki"],
        base_ingredient="Potato",
        cooking_method="Shallow Fried",
        shape_profile="Flat disc",
        is_fried=False,
        is_chaat=True,
        piece_count_expected=2,
        piece_weight_typical_g=70.0,
        default_portion_grams=140.0,
        visible_oil_typical="Moderate visible oil",
        common_accompaniments=["Chole Gravy", "Sweet Tamarind Chutney", "Green Chutney", "Dahi"],
        nutrition_per_100g={"calories": 195.0, "protein": 3.4, "carbs": 28.5, "fat": 7.8, "fiber": 2.8},
        uncertainty_factors=["Tawa shallow frying oil/ghee absorption", "Stuffed chana dal core vs plain"],
    ),
)

# Pani Puri / Golgappa / Puchka (Sections 15, 16)
register_snack_food_class(
    SnackFoodClassRecord(
        canonical_food_id="IND-SNK-NI-PANIPURI-001",
        canonical_name="Pani Puri",
        hierarchy=SnackTiffinHierarchy(
            level3_region="Pan-India",
            level4_state="Delhi",
            level5_snack_family="Chaat",
            level6_specific_food="Pani Puri",
            level7_variant="Crispy, hollow spherical semolina/flour puri filled with spiced potato/chana and tangy-spicy herb water",
            level8_main_ingredient="Semolina/Wheat Puri & Flavored Water",
            level9_flour_grain_base="Suji (semolina) or atta thin fried crisp spheres",
            level10_cooking_method="Deep Fried Shell with Assembled Fillings",
            level11_filling_or_topping="Mashed potato, boiled black chana/white peas ragda, boondi",
            level12_accompaniment="Teekha Pani (mint-coriander-chilli), Meetha Pani (tamarind-jaggery)",
            level13_portion_type="countable_pieces",
            level14_nutrition_ref_id="NUT-SNK-PANIPURI-001",
        ),
        snack_family="Chaat",
        specific_food="Pani Puri",
        region="Pan-India",
        state_or_city="Delhi",
        regional_names={
            "hi": "गोलगप्पा / पानी पूरी",
            "bn": "ফুচকা",
            "od": "ଗୁପଚୁପ",
            "mr": "पाणीपुरी",
            "gu": "પાણીપુરી",
            "te": "పానీ పూరి",
            "ta": "பானி பூரி",
        },
        alternate_names=["Golgappa", "Puchka", "Gupchup", "Pakodi Chaat Gujarat"],
        base_ingredient="Suji / Wheat Shell & Flavored Water",
        cooking_method="Assembled",
        shape_profile="Hollow sphere",
        is_fried=True,
        is_chaat=True,
        piece_count_expected=6,
        piece_weight_typical_g=30.0,
        default_portion_grams=180.0,
        visible_oil_typical="Low visible oil",
        common_accompaniments=["Teekha Spicy Water", "Meetha Tamarind Water", "Boondi"],
        nutrition_per_100g={"calories": 142.0, "protein": 2.8, "carbs": 26.5, "fat": 3.2, "fiber": 2.0},
        uncertainty_factors=["Puri shell oil content", "Sweet tamarind syrup sugar concentration"],
    ),
    alias_ids=["IND-SNK-NI-GOLGAPPA-001", "IND-SNK-WB-PUCHKA-001", "IND-SNK-OD-GUPCHUP-001"],
)

# Sev Puri / Bhel Puri (Chaat Classics)
register_snack_food_class(
    SnackFoodClassRecord(
        canonical_food_id="IND-SNK-MH-SEVPURI-001",
        canonical_name="Sev Puri",
        hierarchy=SnackTiffinHierarchy(
            level3_region="West India",
            level4_state="Maharashtra",
            level5_snack_family="Chaat",
            level6_specific_food="Sev Puri",
            level7_variant="Crispy flat papdis topped with diced potato, onion, trio of chutneys and covered in a mountain of nylon sev",
            level8_main_ingredient="Papdi & Nylon Sev",
            level9_flour_grain_base="Fried maida discs & chickpea flour extruded fine vermicelli (nylon sev)",
            level10_cooking_method="Assembled",
            level11_filling_or_topping="Diced potatoes, onions, raw mango, chaat masala, generous nylon sev, coriander",
            level12_accompaniment="Mint Chutney, Saunth, Garlic Red Chutney",
            level13_portion_type="plate_serving",
            level14_nutrition_ref_id="NUT-SNK-SEVPURI-001",
        ),
        snack_family="Chaat",
        specific_food="Sev Puri",
        region="West India",
        state_or_city="Maharashtra",
        regional_names={"mr": "शेव पुरी", "hi": "सेव पूरी", "gu": "સેવ પુરી"},
        alternate_names=["Bombay Sev Puri", "Street Sev Puri"],
        base_ingredient="Papdi & Sev",
        cooking_method="Assembled",
        shape_profile="Flat assembled discs",
        is_fried=True,
        is_chaat=True,
        piece_count_expected=6,
        piece_weight_typical_g=25.0,
        default_portion_grams=150.0,
        visible_oil_typical="Moderate visible oil",
        common_accompaniments=["Garlic Chutney", "Sweet Chutney", "Green Chutney"],
        nutrition_per_100g={"calories": 235.0, "protein": 4.6, "carbs": 33.8, "fat": 9.5, "fiber": 3.0},
        uncertainty_factors=["Sev topping mass", "Chutney sugar contribution"],
    ),
)


# =============================================================================
# 6. WEST INDIA — MAHARASHTRA & GUJARAT SNACKS (Sections 17, 18, 19)
# =============================================================================

# Vada Pav (Maharashtra Iconic)
register_snack_food_class(
    SnackFoodClassRecord(
        canonical_food_id="IND-SNK-MH-VADAPAV-001",
        canonical_name="Vada Pav",
        hierarchy=SnackTiffinHierarchy(
            level3_region="West India",
            level4_state="Maharashtra",
            level5_snack_family="Street Snacks",
            level6_specific_food="Vada Pav",
            level7_variant="Golden deep-fried spiced potato ball (Batata Vada) nestled inside a soft sliced pav with dry garlic chutney",
            level8_main_ingredient="Potato, Besan & Pav Bread",
            level9_flour_grain_base="Besan batter-coated potato inside refined wheat pav bun",
            level10_cooking_method="Deep Fried Patty Assembled in Bread",
            level11_filling_or_topping="Dry red garlic peanut coconut chutney, fried salted green chilli, sweet tamarind & green chutney",
            level12_accompaniment="Fried Salted Green Chilli",
            level13_portion_type="countable_pieces",
            level14_nutrition_ref_id="NUT-SNK-VADAPAV-001",
        ),
        snack_family="Street Snacks",
        specific_food="Vada Pav",
        region="West India",
        state_or_city="Maharashtra",
        regional_names={"mr": "वडा पाव", "hi": "वड़ा पाव", "gu": "વડા પાઉં"},
        alternate_names=["Bombay Burger", "Batata Vada Pav", "Wada Pav"],
        base_ingredient="Potato, Besan & Bread Pav",
        cooking_method="Assembled",
        shape_profile="Burger/Bun sandwich",
        is_fried=True,
        piece_count_expected=1,
        piece_weight_typical_g=140.0,
        default_portion_grams=140.0,
        visible_oil_typical="Deep-fried",
        common_accompaniments=["Dry Garlic Chutney", "Fried Salted Chilli", "Green Chutney"],
        nutrition_per_100g={"calories": 242.0, "protein": 5.8, "carbs": 35.6, "fat": 8.8, "fiber": 2.8},
        uncertainty_factors=["Butter applied to pav (dry vs toasted in butter)", "Vada size (50g to 85g)"],
    ),
)

# Misal Pav (Maharashtra Iconic)
register_snack_food_class(
    SnackFoodClassRecord(
        canonical_food_id="IND-SNK-MH-MISALPAV-001",
        canonical_name="Misal Pav",
        hierarchy=SnackTiffinHierarchy(
            level3_region="West India",
            level4_state="Maharashtra",
            level5_snack_family="Street Snacks",
            level6_specific_food="Misal Pav",
            level7_variant="Fiery sprouted moth bean (matki) curry topped with crispy farsan, sev, onions, served with soft pav buns",
            level8_main_ingredient="Sprouted Moth Beans (Matki) & Farsan",
            level9_flour_grain_base="Legume sprouts & chickpea flour farsan with pav bread",
            level10_cooking_method="Simmered Curry with Assembled Crisp Toppings",
            level11_filling_or_topping="Crunchy mix farsan, diced onions, fresh coriander, lemon wedge, fiery rassa/tarri oil float",
            level12_accompaniment="Pav Buns (2), Extra Kat/Rassa Gravy, Lemon Wedge",
            level13_portion_type="plate_serving",
            level14_nutrition_ref_id="NUT-SNK-MISALPAV-001",
        ),
        snack_family="Street Snacks",
        specific_food="Misal Pav",
        region="West India",
        state_or_city="Maharashtra",
        regional_names={"mr": "मिसळ पाव", "hi": "मिसल पाव"},
        alternate_names=["Kolhapuri Misal", "Puneri Misal", "Mumbai Misal"],
        base_ingredient="Sprouted Matki & Farsan",
        cooking_method="Assembled",
        shape_profile="Bowl of gravy with buns",
        is_fried=False,
        is_tiffin=True,
        piece_count_expected=1,
        piece_weight_typical_g=300.0,
        default_portion_grams=300.0,
        visible_oil_typical="High visible oil",
        common_accompaniments=["Pav (2)", "Extra Rassa", "Chopped Onions", "Lemon"],
        nutrition_per_100g={"calories": 178.0, "protein": 6.2, "carbs": 24.5, "fat": 6.8, "fiber": 3.8},
        uncertainty_factors=["Tarri floating oil volume", "Farsan topping quantity (25g to 60g)"],
    ),
)

# Sabudana Vada (Maharashtra Fasting & Tea-Time Snack)
register_snack_food_class(
    SnackFoodClassRecord(
        canonical_food_id="IND-SNK-MH-SABUDANAVADA-001",
        canonical_name="Sabudana Vada",
        hierarchy=SnackTiffinHierarchy(
            level3_region="West India",
            level4_state="Maharashtra",
            level5_snack_family="Fried Snacks",
            level6_specific_food="Sabudana Vada",
            level7_variant="Crispy, golden deep-fried patties made of soaked tapioca pearls, mashed potatoes & roasted crushed peanuts",
            level8_main_ingredient="Tapioca Pearls (Sabudana) & Peanuts",
            level9_flour_grain_base="Sabudana, mashed potato, coarse peanut powder",
            level10_cooking_method="Deep Fried",
            level11_filling_or_topping="Crushed roasted peanuts, cumin, green chillies, lemon juice",
            level12_accompaniment="Sweet Spiced Yogurt / Dahi Chutney",
            level13_portion_type="countable_pieces",
            level14_nutrition_ref_id="NUT-SNK-SABUDANAVADA-001",
        ),
        snack_family="Fried Snacks",
        specific_food="Sabudana Vada",
        region="West India",
        state_or_city="Maharashtra",
        regional_names={"mr": "साबुदाणा वडा", "hi": "साबूदाना वड़ा", "gu": "સાબુદાણા વડા"},
        alternate_names=["Sago Vada", "Tapioca Pearl Fritter", "Upvas Vada"],
        base_ingredient="Sabudana & Potato",
        cooking_method="Deep Fried",
        shape_profile="Flat disc",
        is_fried=True,
        piece_count_expected=2,
        piece_weight_typical_g=60.0,
        default_portion_grams=120.0,
        visible_oil_typical="Deep-fried",
        common_accompaniments=["Dahi Chutney", "Green Chilli"],
        nutrition_per_100g={"calories": 288.0, "protein": 4.5, "carbs": 44.0, "fat": 10.8, "fiber": 2.2},
        uncertainty_factors=["High oil absorption of tapioca pearls during frying", "Peanut proportion"],
    ),
)

# Dhokla (Fermented Chana Dal / Rice - Gujarat Classic)
register_snack_food_class(
    SnackFoodClassRecord(
        canonical_food_id="IND-SNK-GJ-DHOKLA-001",
        canonical_name="Dhokla",
        hierarchy=SnackTiffinHierarchy(
            level3_region="West India",
            level4_state="Gujarat",
            level5_snack_family="Steamed Snacks",
            level6_specific_food="Dhokla",
            level7_variant="Traditional fermented rice and chana dal steamed savory cake with slight sour fermented tang",
            level8_main_ingredient="Rice & Chana Dal",
            level9_flour_grain_base="Fermented coarse ground rice and split chickpea batter",
            level10_cooking_method="Steamed",
            level11_filling_or_topping="Mustard seeds, green chillies, curry leaves, grated coconut, coriander tempering",
            level12_accompaniment="Green Chutney, Papaya Sambharo",
            level13_portion_type="countable_pieces",
            level14_nutrition_ref_id="NUT-SNK-DHOKLA-001",
        ),
        snack_family="Steamed Snacks",
        specific_food="Dhokla",
        region="West India",
        state_or_city="Gujarat",
        regional_names={"gu": "ખાટા ઢોકળા / ઢોકળા", "hi": "ढोकला / खट्टा ढोकला", "mr": "ढोकळा"},
        alternate_names=["Khatta Dhokla", "White Dhokla", "Fermented Dal Dhokla"],
        base_ingredient="Rice & Chana Dal",
        cooking_method="Steamed",
        shape_profile="Square / Diamond steamed cube",
        is_fried=False,
        is_steamed=True,
        is_tiffin=True,
        piece_count_expected=4,
        piece_weight_typical_g=35.0,
        default_portion_grams=140.0,
        visible_oil_typical="Low visible oil",
        common_accompaniments=["Green Chutney", "Methi Chutney"],
        nutrition_per_100g={"calories": 145.0, "protein": 6.8, "carbs": 24.2, "fat": 2.4, "fiber": 3.6},
        uncertainty_factors=["Tadka oil volume", "Fermentation density"],
    ),
)

# Khaman (Instant Spongy Besan - Gujarat)
register_snack_food_class(
    SnackFoodClassRecord(
        canonical_food_id="IND-SNK-GJ-KHAMAN-001",
        canonical_name="Khaman",
        hierarchy=SnackTiffinHierarchy(
            level3_region="West India",
            level4_state="Gujarat",
            level5_snack_family="Steamed Snacks",
            level6_specific_food="Khaman",
            level7_variant="Airy, spongy, juicy yellow steamed gram flour cake soaked in mustard-sugar-chilli warm water syrup",
            level8_main_ingredient="Besan (Gram Flour)",
            level9_flour_grain_base="Fine besan batter aerated with eno/fruit salt and turmeric",
            level10_cooking_method="Steamed and Sugar-Mustard Syrup Soaked",
            level11_filling_or_topping="Tempered mustard seeds, green chillies, sugar-lemon water soak, fresh coriander, coconut",
            level12_accompaniment="Besan Green Chutney, Fried Green Chilli",
            level13_portion_type="countable_pieces",
            level14_nutrition_ref_id="NUT-SNK-KHAMAN-001",
        ),
        snack_family="Steamed Snacks",
        specific_food="Khaman",
        region="West India",
        state_or_city="Gujarat",
        regional_names={"gu": "ખમણ / નાયલોન ખમણ", "hi": "खमन / नायलॉन खमन", "mr": "खमण"},
        alternate_names=["Nylon Khaman", "Yellow Dhokla", "Surati Khaman"],
        base_ingredient="Besan",
        cooking_method="Steamed",
        shape_profile="Square yellow spongy cube",
        is_fried=False,
        is_steamed=True,
        piece_count_expected=4,
        piece_weight_typical_g=40.0,
        default_portion_grams=160.0,
        visible_oil_typical="Low visible oil",
        common_accompaniments=["Sweet Kadhi Chutney", "Fried Chillies"],
        nutrition_per_100g={"calories": 160.0, "protein": 6.2, "carbs": 26.5, "fat": 3.5, "fiber": 2.8},
        uncertainty_factors=["Sugar syrup soak absorption (adds 20-30% weight and quick carbs)"],
    ),
    alias_ids=["IND-SNK-GJ-NYLONKHAMAN-001"],
)

# Khandvi (Gujarat Besan Roll)
register_snack_food_class(
    SnackFoodClassRecord(
        canonical_food_id="IND-SNK-GJ-KHANDVI-001",
        canonical_name="Khandvi",
        hierarchy=SnackTiffinHierarchy(
            level3_region="West India",
            level4_state="Gujarat",
            level5_snack_family="Steamed Snacks",
            level6_specific_food="Khandvi",
            level7_variant="Delicate, silky, tightly rolled yellow spirals made of cooked besan and buttermilk paste",
            level8_main_ingredient="Besan & Buttermilk",
            level9_flour_grain_base="Gram flour cooked with spiced buttermilk until gelatinized then spread thin and rolled",
            level10_cooking_method="Cooked Paste Rolled and Steamed/Cooled",
            level11_filling_or_topping="Tadka of mustard seeds, sesame seeds, green chillies, grated coconut, coriander",
            level12_accompaniment="Green Chutney",
            level13_portion_type="countable_pieces",
            level14_nutrition_ref_id="NUT-SNK-KHANDVI-001",
        ),
        snack_family="Steamed Snacks",
        specific_food="Khandvi",
        region="West India",
        state_or_city="Gujarat",
        regional_names={"gu": "ખાંડવી", "hi": "खांडवी", "mr": "सुरळीची वडी"},
        alternate_names=["Suralichi Vadi", "Patuli", "Gujarati Khandvi"],
        base_ingredient="Besan & Buttermilk",
        cooking_method="Cooked and Rolled",
        shape_profile="Tight cylindrical roll",
        is_fried=False,
        is_steamed=True,
        piece_count_expected=4,
        piece_weight_typical_g=25.0,
        default_portion_grams=100.0,
        visible_oil_typical="Low visible oil",
        common_accompaniments=["Green Chutney"],
        nutrition_per_100g={"calories": 152.0, "protein": 6.5, "carbs": 21.0, "fat": 4.5, "fiber": 3.1},
        uncertainty_factors=["Sesame and tadka oil volume"],
    ),
    alias_ids=["IND-SNK-MH-SURALICHIVADI-001"],
)

# Fafda (Gujarat Breakfast Farsan)
register_snack_food_class(
    SnackFoodClassRecord(
        canonical_food_id="IND-SNK-GJ-FAFDA-001",
        canonical_name="Fafda",
        hierarchy=SnackTiffinHierarchy(
            level3_region="West India",
            level4_state="Gujarat",
            level5_snack_family="Fried Snacks",
            level6_specific_food="Fafda",
            level7_variant="Long, flat, crisp yellow strips made of besan seasoned with carom seeds (ajwain) and papad khar",
            level8_main_ingredient="Besan (Gram Flour)",
            level9_flour_grain_base="Besan kneaded with ajwain, black pepper and alkaline salt (papad khar)",
            level10_cooking_method="Deep Fried",
            level11_filling_or_topping="Coarsely crushed black pepper, carom seeds",
            level12_accompaniment="Jalebi, Papaya Sambharo, Besan Kadhi Chutney, Fried Green Chillies",
            level13_portion_type="countable_pieces",
            level14_nutrition_ref_id="NUT-SNK-FAFDA-001",
        ),
        snack_family="Fried Snacks",
        specific_food="Fafda",
        region="West India",
        state_or_city="Gujarat",
        regional_names={"gu": "ફાફડા", "hi": "फाफड़ा"},
        alternate_names=["Fafda Gathiya", "Crisp Besan Strips"],
        base_ingredient="Besan",
        cooking_method="Deep Fried",
        shape_profile="Long flat ribbon strip",
        is_fried=True,
        piece_count_expected=4,
        piece_weight_typical_g=20.0,
        default_portion_grams=80.0,
        visible_oil_typical="High visible oil",
        common_accompaniments=["Jalebi", "Kadhi Chutney", "Papaya Sambharo", "Fried Green Chilli"],
        nutrition_per_100g={"calories": 482.0, "protein": 11.5, "carbs": 52.8, "fat": 25.4, "fiber": 5.2},
        uncertainty_factors=["Commercial frying oil temperature and absorption"],
    ),
)


# =============================================================================
# 7. EAST INDIA — WEST BENGAL, ODISHA, BIHAR, JHARKHAND (Section 21)
# =============================================================================

# Singara (Bengali Samosa)
register_snack_food_class(
    SnackFoodClassRecord(
        canonical_food_id="IND-SNK-WB-SINGARA-001",
        canonical_name="Singara",
        hierarchy=SnackTiffinHierarchy(
            level3_region="East India",
            level4_state="West Bengal",
            level5_snack_family="Fried Snacks",
            level6_specific_food="Singara",
            level7_variant="Delicate, thin-crusted pyramidal pastry stuffed with diced potatoes, cauliflower florets & roasted peanuts",
            level8_main_ingredient="Potato, Cauliflower & Maida",
            level9_flour_grain_base="Thin rolled maida dough with nigella seeds (kalonji)",
            level10_cooking_method="Deep Fried",
            level11_filling_or_topping="Diced potatoes, cauliflower (fulkopi), peanuts, panch phoron, ginger",
            level12_accompaniment="Chai, Sweet Tomato Chutney",
            level13_portion_type="countable_pieces",
            level14_nutrition_ref_id="NUT-SNK-SINGARA-001",
        ),
        snack_family="Fried Snacks",
        specific_food="Singara",
        region="East India",
        state_or_city="West Bengal",
        regional_names={"bn": "সিঙাড়া / ফুলকপির সিঙাড়া", "hi": "सिंगाड़ा", "od": "ସିଙ୍ଗଡ଼ା"},
        alternate_names=["Fulkopir Singara", "Bengali Samosa", "Kolkatta Singara"],
        base_ingredient="Potato & Cauliflower",
        cooking_method="Deep Fried",
        shape_profile="Pyramidal/Triangular",
        is_fried=True,
        piece_count_expected=2,
        piece_weight_typical_g=65.0,
        default_portion_grams=130.0,
        visible_oil_typical="Deep-fried",
        filling_detected="Potato, Cauliflower & Peanuts",
        common_accompaniments=["Chai", "Tomato Chutney"],
        nutrition_per_100g={"calories": 248.0, "protein": 4.8, "carbs": 31.5, "fat": 11.5, "fiber": 3.4},
        uncertainty_factors=["Cauliflower seasonal ratio", "Crust thinner than Punjabi samosa"],
    ),
)

# Jhalmuri (Kolkata Street Puffed Rice Mix)
register_snack_food_class(
    SnackFoodClassRecord(
        canonical_food_id="IND-SNK-WB-JHALMURI-001",
        canonical_name="Jhalmuri",
        hierarchy=SnackTiffinHierarchy(
            level3_region="East India",
            level4_state="West Bengal",
            level5_snack_family="Street Snacks",
            level6_specific_food="Jhalmuri",
            level7_variant="Spicy Kolkata street mix of crispy puffed rice tossed with mustard oil, boiled potatoes, sprouted gram & coconut",
            level8_main_ingredient="Puffed Rice (Muri) & Raw Mustard Oil",
            level9_flour_grain_base="Puffed rice, boiled brown chana, chanachur / mixture",
            level10_cooking_method="Assembled / Tossed in Tin",
            level11_filling_or_topping="Pungent raw mustard oil, fresh coconut slivers, diced boiled potatoes, onions, green chillies, special masala",
            level12_accompaniment="None (served in paper thonga)",
            level13_portion_type="bowl_serving",
            level14_nutrition_ref_id="NUT-SNK-JHALMURI-001",
        ),
        snack_family="Street Snacks",
        specific_food="Jhalmuri",
        region="East India",
        state_or_city="West Bengal",
        regional_names={"bn": "ঝালমুড়ি", "hi": "झालमुड़ी", "od": "ଝାଲମୁଢ଼ି"},
        alternate_names=["Kolkata Jhal Muri", "Spicy Puffed Rice"],
        base_ingredient="Puffed Rice & Mustard Oil",
        cooking_method="Assembled",
        shape_profile="Loose tossed flakes",
        is_fried=False,
        piece_count_expected=None,
        piece_weight_typical_g=None,
        default_portion_grams=100.0,
        visible_oil_typical="Moderate visible oil",
        common_accompaniments=["Coconut Slice", "Chilli"],
        nutrition_per_100g={"calories": 365.0, "protein": 7.2, "carbs": 62.0, "fat": 9.8, "fiber": 4.6},
        uncertainty_factors=["Mustard oil tablespoons drizzled", "Chanachur (fried sev) ratio"],
    ),
)

# Dahibara Aloodum (Odisha Street Iconic)
register_snack_food_class(
    SnackFoodClassRecord(
        canonical_food_id="IND-SNK-OD-DAHIBARA-001",
        canonical_name="Dahibara Aloodum",
        hierarchy=SnackTiffinHierarchy(
            level3_region="East India",
            level4_state="Odisha",
            level5_snack_family="Street Snacks",
            level6_specific_food="Dahibara Aloodum",
            level7_variant="Light urad dal baras soaked in thin seasoned buttermilk, topped with spicy potato curry & ghugni",
            level8_main_ingredient="Urad Dal, Curd & Potatoes",
            level9_flour_grain_base="Fermented urad dal fried and soaked in spiced dahi-pani",
            level10_cooking_method="Deep Fried then Soaked with Simmered Gravy",
            level11_filling_or_topping="Spicy aloo dum, yellow pea ghugni, roasted cumin-chilli powder, black salt, chopped onions, sev",
            level12_accompaniment="Spiced Buttermilk Water (Dahi Pani)",
            level13_portion_type="plate_serving",
            level14_nutrition_ref_id="NUT-SNK-DAHIBARA-001",
        ),
        snack_family="Street Snacks",
        specific_food="Dahibara Aloodum",
        region="East India",
        state_or_city="Odisha",
        regional_names={"od": "ଦହିବରା ଆଳୁଦମ", "hi": "दही बड़ा आलू दम", "bn": "দইবড়া আলুরদম"},
        alternate_names=["Cuttack Dahibara Aloodum", "Dahibara Aloo Dum Ghugni"],
        base_ingredient="Urad Dal, Dahi & Potato",
        cooking_method="Assembled",
        shape_profile="Soaked baras in spiced curry",
        is_fried=True,
        is_tiffin=True,
        piece_count_expected=3,
        piece_weight_typical_g=90.0,
        default_portion_grams=270.0,
        visible_oil_typical="Moderate visible oil",
        common_accompaniments=["Dahi Pani Drink", "Sev", "Chopped Onions"],
        nutrition_per_100g={"calories": 148.0, "protein": 5.4, "carbs": 21.6, "fat": 4.8, "fiber": 3.2},
        uncertainty_factors=["Aloo dum oil and gravy portion", "Bara buttermilk hydration weight"],
    ),
)

# Litti Chokha (Bihar Classic)
register_snack_food_class(
    SnackFoodClassRecord(
        canonical_food_id="IND-SNK-BR-LITTICHOKHA-001",
        canonical_name="Litti Chokha",
        hierarchy=SnackTiffinHierarchy(
            level3_region="East India",
            level4_state="Bihar",
            level5_snack_family="Roasted Snacks",
            level6_specific_food="Litti Chokha",
            level7_variant="Hard, rustic roasted whole wheat balls filled with spiced roasted gram flour (sattu) dipped in melted ghee",
            level8_main_ingredient="Whole Wheat Flour & Roasted Chana Flour (Sattu)",
            level9_flour_grain_base="Atta whole wheat dough filled with sattu",
            level10_cooking_method="Roasted on Cow Dung/Charcoal or Baked then Ghee Dipped",
            level11_filling_or_topping="Sattu seasoned with kalonji, ajwain, pickle masala, garlic, mustard oil; dipped in ghee",
            level12_accompaniment="Baingan Bharta (Chokha), Aloo Chokha, Tomato Chokha, Green Chutney",
            level13_portion_type="plate_serving",
            level14_nutrition_ref_id="NUT-SNK-LITTICHOKHA-001",
        ),
        snack_family="Roasted Snacks",
        specific_food="Litti Chokha",
        region="East India",
        state_or_city="Bihar",
        regional_names={"hi": "लिट्टी चोखा", "bho": "लिट्टी चोखा", "bn": "লিট্টি চোখা"},
        alternate_names=["Bihari Litti", "Sattu Litti", "Litti with Chokha"],
        base_ingredient="Wheat Flour & Sattu",
        cooking_method="Roasted",
        shape_profile="Hard rustic round ball",
        is_fried=False,
        is_tiffin=True,
        piece_count_expected=2,
        piece_weight_typical_g=90.0,
        default_portion_grams=280.0,
        visible_oil_typical="High visible oil",
        filling_detected="Spiced Sattu with Mustard Oil & Pickle Masala",
        common_accompaniments=["Baingan Chokha", "Aloo Chokha", "Pure Ghee Dip"],
        nutrition_per_100g={"calories": 215.0, "protein": 7.8, "carbs": 34.0, "fat": 5.8, "fiber": 5.5},
        uncertainty_factors=["Ghee dipping immersion duration (adds 10g to 30g pure fat per plate)"],
    ),
    alias_ids=["IND-SNK-JH-LITTI-001"],
)

# Dhuska (Jharkhand Classic)
register_snack_food_class(
    SnackFoodClassRecord(
        canonical_food_id="IND-SNK-JH-DHUSKA-001",
        canonical_name="Dhuska",
        hierarchy=SnackTiffinHierarchy(
            level3_region="East India",
            level4_state="Jharkhand",
            level5_snack_family="Fried Snacks",
            level6_specific_food="Dhuska",
            level7_variant="Crispy, golden deep-fried savory pancake puffed from soaked rice and chana dal batter",
            level8_main_ingredient="Rice & Chana Dal",
            level9_flour_grain_base="Coarsely ground soaked rice and Bengal gram batter with cumin and turmeric",
            level10_cooking_method="Deep Fried",
            level11_filling_or_topping="Cumin seeds, green chillies, garlic, asafoetida",
            level12_accompaniment="Aloo Chana Sabzi, Ghugni, Chutney",
            level13_portion_type="countable_pieces",
            level14_nutrition_ref_id="NUT-SNK-DHUSKA-001",
        ),
        snack_family="Fried Snacks",
        specific_food="Dhuska",
        region="East India",
        state_or_city="Jharkhand",
        regional_names={"hi": "धुस्का", "bn": "ধুসকা"},
        alternate_names=["Jharkhand Dhuska", "Rice Dal Puri Fritter"],
        base_ingredient="Rice & Chana Dal",
        cooking_method="Deep Fried",
        shape_profile="Puffed disc",
        is_fried=True,
        piece_count_expected=3,
        piece_weight_typical_g=40.0,
        default_portion_grams=120.0,
        visible_oil_typical="Deep-fried",
        common_accompaniments=["Aloo Chana Sabzi", "Ghugni"],
        nutrition_per_100g={"calories": 278.0, "protein": 6.8, "carbs": 38.5, "fat": 10.8, "fiber": 3.8},
        uncertainty_factors=["Puff oil absorption"],
    ),
)


# =============================================================================
# 8. NORTHEAST INDIA — MOMOS & DUMPLINGS (Sections 22, 23)
# =============================================================================

# Steamed Veg Momo (Northeast / Himalayan Master)
register_snack_food_class(
    SnackFoodClassRecord(
        canonical_food_id="IND-SNK-NE-VEGMOMO-001",
        canonical_name="Steamed Veg Momo",
        hierarchy=SnackTiffinHierarchy(
            level3_region="Northeast India",
            level4_state="Sikkim",
            level5_snack_family="Steamed Snacks",
            level6_specific_food="Momo",
            level7_variant="Delicate, pleated thin white refined flour pouch filled with finely minced spiced vegetables",
            level8_main_ingredient="Mixed Vegetables & Maida",
            level9_flour_grain_base="Thin rolled maida wrapper pleated tightly",
            level10_cooking_method="Steamed",
            level11_filling_or_topping="Finely shredded cabbage, carrots, onions, ginger, garlic, soy, black pepper",
            level12_accompaniment="Spicy Red Chilli Garlic Chutney, Clear Vegetable Soup (Momo Soup)",
            level13_portion_type="countable_pieces",
            level14_nutrition_ref_id="NUT-SNK-VEGMOMO-001",
        ),
        snack_family="Steamed Snacks",
        specific_food="Momo",
        region="Northeast India",
        state_or_city="Sikkim",
        regional_names={"hi": "वेज मोमो", "ne": "मम: (मोमो)", "bn": "ভেজ মোমো", "ta": "மோமோ"},
        alternate_names=["Veg Steamed Dumpling", "Sikkim Momo", "Darjeeling Veg Momo"],
        base_ingredient="Vegetables & Maida",
        cooking_method="Steamed",
        shape_profile="Pleated crescent / round purse",
        is_fried=False,
        is_steamed=True,
        piece_count_expected=6,
        piece_weight_typical_g=28.0,
        default_portion_grams=168.0,
        visible_oil_typical="Low visible oil",
        filling_detected="Cabbage, Carrot & Onion",
        common_accompaniments=["Red Chilli Garlic Chutney", "Momo Soup"],
        nutrition_per_100g={"calories": 140.0, "protein": 4.2, "carbs": 26.5, "fat": 2.1, "fiber": 2.4},
        uncertainty_factors=["Piece count (5, 6, 8 or 10 pieces)", "Chutney oil and chilli concentration"],
    ),
    alias_ids=["IND-SNK-NE-MOMO-001"],
)

# Steamed Chicken Momo
register_snack_food_class(
    SnackFoodClassRecord(
        canonical_food_id="IND-SNK-NE-CHICKENMOMO-001",
        canonical_name="Steamed Chicken Momo",
        hierarchy=SnackTiffinHierarchy(
            level3_region="Northeast India",
            level4_state="Sikkim",
            level5_snack_family="Steamed Snacks",
            level6_specific_food="Momo",
            level7_variant="Juicy pleated steamed dumpling packed with savory minced chicken, spring onions & ginger",
            level8_main_ingredient="Chicken & Maida",
            level9_flour_grain_base="Thin maida translucent wrapper",
            level10_cooking_method="Steamed",
            level11_filling_or_topping="Juicy minced chicken, onions, ginger, garlic, coriander, butter/fat for juiciness",
            level12_accompaniment="Fiery Dalle Khursani Red Chutney, Chicken Bone Broth",
            level13_portion_type="countable_pieces",
            level14_nutrition_ref_id="NUT-SNK-CHICKENMOMO-001",
        ),
        snack_family="Steamed Snacks",
        specific_food="Momo",
        region="Northeast India",
        state_or_city="Sikkim",
        regional_names={"hi": "चिकन मोमो", "ne": "चिकेन मम:", "bn": "চিকেন মোমো"},
        alternate_names=["Chicken Steamed Momo", "Himalayan Chicken Dumpling"],
        base_ingredient="Chicken & Maida",
        cooking_method="Steamed",
        shape_profile="Pleated crescent",
        is_fried=False,
        is_steamed=True,
        piece_count_expected=6,
        piece_weight_typical_g=32.0,
        default_portion_grams=192.0,
        visible_oil_typical="Low visible oil",
        filling_detected="Minced Chicken with Ginger & Scallions",
        common_accompaniments=["Dalle Chilli Sauce", "Clear Chicken Soup"],
        nutrition_per_100g={"calories": 175.0, "protein": 11.8, "carbs": 22.0, "fat": 4.5, "fiber": 1.2},
        uncertainty_factors=["Chicken fat/butter added to mince for succulence", "Wrapper thickness"],
    ),
)

# Fried Chicken Momo
register_snack_food_class(
    SnackFoodClassRecord(
        canonical_food_id="IND-SNK-NE-FRIEDCHICKENMOMO-001",
        canonical_name="Fried Chicken Momo",
        hierarchy=SnackTiffinHierarchy(
            level3_region="Northeast India",
            level4_state="Sikkim",
            level5_snack_family="Fried Snacks",
            level6_specific_food="Momo",
            level7_variant="Crispy, deep-fried golden chicken dumpling with crunchy bubbly exterior and juicy chicken center",
            level8_main_ingredient="Chicken & Maida",
            level9_flour_grain_base="Deep-fried maida wrapper",
            level10_cooking_method="Deep Fried",
            level11_filling_or_topping="Minced chicken, onions, ginger, spices",
            level12_accompaniment="Spicy Garlic Chutney, Mayo",
            level13_portion_type="countable_pieces",
            level14_nutrition_ref_id="NUT-SNK-FRIEDMOMO-001",
        ),
        snack_family="Fried Snacks",
        specific_food="Momo",
        region="Northeast India",
        state_or_city="Sikkim",
        regional_names={"hi": "फ्राइड चिकन मोमो", "bn": "ফ্রাইড চিকেন মোমো"},
        alternate_names=["Deep Fried Chicken Momo", "Crispy Momo"],
        base_ingredient="Chicken & Maida",
        cooking_method="Deep Fried",
        shape_profile="Deep-fried golden crescent",
        is_fried=True,
        piece_count_expected=6,
        piece_weight_typical_g=35.0,
        default_portion_grams=210.0,
        visible_oil_typical="Deep-fried",
        filling_detected="Minced Chicken",
        common_accompaniments=["Garlic Chilli Sauce"],
        nutrition_per_100g={"calories": 255.0, "protein": 11.2, "carbs": 24.5, "fat": 12.8, "fiber": 1.2},
        uncertainty_factors=["Deep frying oil uptake", "Mayonnaise dipping sauce presence"],
    ),
)


# =============================================================================
# 9. NAMKEEN, MIXTURES & PACKAGED SNACKS (Section 29)
# =============================================================================

# Madras Mixture (South India Classic)
register_snack_food_class(
    SnackFoodClassRecord(
        canonical_food_id="IND-SNK-TN-MIXTURE-001",
        canonical_name="Madras Mixture",
        hierarchy=SnackTiffinHierarchy(
            level3_region="South India",
            level4_state="Tamil Nadu",
            level5_snack_family="Namkeen",
            level6_specific_food="Mixture",
            level7_variant="Crunchy savory blend of omapodi sev, ribbon pakoda, boondi, fried peanuts, roasted gram & curry leaves",
            level8_main_ingredient="Besan & Rice Flour",
            level9_flour_grain_base="Extruded fried gram flour vermicelli and ribbons",
            level10_cooking_method="Deep Fried Blend",
            level11_filling_or_topping="Fried peanuts, roasted chana dal, cashews, crispy curry leaves, hing, chilli powder",
            level12_accompaniment="Filter Coffee / Tea",
            level13_portion_type="weight_grams",
            level14_nutrition_ref_id="NUT-SNK-MIXTURE-001",
        ),
        snack_family="Namkeen",
        specific_food="Mixture",
        region="South India",
        state_or_city="Tamil Nadu",
        regional_names={"ta": "மதராஸ் மிக்ஸர் / கார மிக்ஸர்", "te": "మిశ్రమం / మిక్చర్", "kn": "ಮಿಕ್ಸ್ಚರ್", "hi": "मद्रास मिक्सचर"},
        alternate_names=["South Indian Mixture", "Kara Mixture", "Spicy Mixture"],
        base_ingredient="Besan & Peanuts",
        cooking_method="Deep Fried",
        shape_profile="Assorted fried shreds & drops",
        is_fried=True,
        piece_count_expected=None,
        piece_weight_typical_g=None,
        default_portion_grams=50.0,
        visible_oil_typical="High visible oil",
        common_accompaniments=["Coffee", "Chai"],
        nutrition_per_100g={"calories": 535.0, "protein": 12.0, "carbs": 48.5, "fat": 32.5, "fiber": 6.2},
        uncertainty_factors=["Nut ratio (peanuts and cashews increase calories)", "Fried oil drainage"],
    ),
    alias_ids=["IND-SNK-SI-MIXTURE-001"],
)

# Bhujia / Bikaneri Bhujia (Rajasthan Namkeen)
register_snack_food_class(
    SnackFoodClassRecord(
        canonical_food_id="IND-SNK-RJ-BHUJIA-001",
        canonical_name="Bikaneri Bhujia",
        hierarchy=SnackTiffinHierarchy(
            level3_region="North India",
            level4_state="Rajasthan",
            level5_snack_family="Namkeen",
            level6_specific_food="Bhujia",
            level7_variant="Crispy, fine, pungent fried vermicelli made from moth dal flour and besan seasoned with black pepper and cardamom",
            level8_main_ingredient="Moth Dal & Besan",
            level9_flour_grain_base="Ground moth bean flour and Bengal gram flour dough",
            level10_cooking_method="Deep Fried",
            level11_filling_or_topping="Black pepper, red chilli, cardamom, cloves, hing",
            level12_accompaniment="Tea",
            level13_portion_type="weight_grams",
            level14_nutrition_ref_id="NUT-SNK-BHUJIA-001",
        ),
        snack_family="Namkeen",
        specific_food="Bhujia",
        region="North India",
        state_or_city="Rajasthan",
        regional_names={"hi": "बीकानेरी भुजिया", "rj": "भुजिया", "gu": "ભુજિયા"},
        alternate_names=["Bikaner Bhujia", "Moth Bhujia", "Sev Bhujia"],
        base_ingredient="Moth Dal & Besan",
        cooking_method="Deep Fried",
        shape_profile="Fine extruded vermicelli",
        is_fried=True,
        piece_count_expected=None,
        piece_weight_typical_g=None,
        default_portion_grams=45.0,
        visible_oil_typical="High visible oil",
        common_accompaniments=["Chai"],
        nutrition_per_100g={"calories": 558.0, "protein": 13.5, "carbs": 42.0, "fat": 36.8, "fiber": 5.8},
        uncertainty_factors=["Oil retention in fine strand diameter"],
    ),
)


# =============================================================================
# 10. STANDARDIZED UNKNOWN & FALLBACK CLASSES (Section 51)
# =============================================================================

# 1. Indian snack — exact type uncertain
register_snack_food_class(
    SnackFoodClassRecord(
        canonical_food_id="IND-SNK-UNKNOWN-001",
        canonical_name="Indian Snack (Type Uncertain)",
        hierarchy=SnackTiffinHierarchy(
            level3_region="Pan-India",
            level4_state="All",
            level5_snack_family="Regional Snacks",
            level6_specific_food="Unclassified Indian Snack",
            level7_variant="Uncertain Indian snack requiring user visual disambiguation",
            level8_main_ingredient="Mixed grain/pulse base",
            level9_flour_grain_base="Flour or lentil base",
            level10_cooking_method="Unknown",
            level11_filling_or_topping="Uncertain",
            level12_accompaniment="Uncertain",
            level13_portion_type="plate_serving",
            level14_nutrition_ref_id="NUT-SNK-UNKNOWN-001",
        ),
        snack_family="Regional Snacks",
        specific_food="Unclassified Indian Snack",
        region="Pan-India",
        state_or_city="Unknown",
        regional_names={"hi": "भारतीय नाश्ता (अस्पष्ट)", "ta": "இந்திய சிற்றுண்டி (தெளிவற்றது)"},
        alternate_names=["Indian snack — exact type uncertain", "Unknown Indian Snack"],
        base_ingredient="Grain or Dal",
        cooking_method="Unknown",
        shape_profile="Irregular",
        is_fried=False,
        piece_count_expected=1,
        piece_weight_typical_g=70.0,
        default_portion_grams=100.0,
        visible_oil_typical="Moderate visible oil",
        nutrition_per_100g={"calories": 250.0, "protein": 6.0, "carbs": 35.0, "fat": 10.0, "fiber": 3.0},
        uncertainty_factors=["Insufficient visual features to isolate canonical snack class"],
    ),
)

# 2. Indian fried snack — exact type uncertain
register_snack_food_class(
    SnackFoodClassRecord(
        canonical_food_id="IND-SNK-FRIED-UNKNOWN-001",
        canonical_name="Indian Fried Snack (Type Uncertain)",
        hierarchy=SnackTiffinHierarchy(
            level3_region="Pan-India",
            level4_state="All",
            level5_snack_family="Fried Snacks",
            level6_specific_food="Unclassified Fried Snack",
            level7_variant="Golden brown deep-fried savory item; specific dough or stuffing not fully resolved",
            level8_main_ingredient="Flour/Dal Batter",
            level9_flour_grain_base="Besan or Maida or Dal batter",
            level10_cooking_method="Deep Fried",
            level11_filling_or_topping="Uncertain",
            level12_accompaniment="Chutney/Sauce",
            level13_portion_type="countable_pieces",
            level14_nutrition_ref_id="NUT-SNK-FRIED-UNKNOWN-001",
        ),
        snack_family="Fried Snacks",
        specific_food="Unclassified Fried Snack",
        region="Pan-India",
        state_or_city="Unknown",
        regional_names={"hi": "तला हुआ नाश्ता (अस्पष्ट)", "ta": "பொரித்த தின்பண்டம் (தெளிவற்றது)"},
        alternate_names=["Indian fried snack — exact type uncertain", "Unknown Fried Snack"],
        base_ingredient="Flour / Dal",
        cooking_method="Deep Fried",
        shape_profile="Irregular Fried",
        is_fried=True,
        piece_count_expected=2,
        piece_weight_typical_g=50.0,
        default_portion_grams=100.0,
        visible_oil_typical="Deep-fried",
        nutrition_per_100g={"calories": 310.0, "protein": 6.5, "carbs": 38.0, "fat": 15.0, "fiber": 3.2},
        uncertainty_factors=["High oil absorption uncertainty across different fried snack batters"],
    ),
)

# 3. Indian steamed snack — exact type uncertain
register_snack_food_class(
    SnackFoodClassRecord(
        canonical_food_id="IND-SNK-STEAMED-UNKNOWN-001",
        canonical_name="Indian Steamed Snack (Type Uncertain)",
        hierarchy=SnackTiffinHierarchy(
            level3_region="Pan-India",
            level4_state="All",
            level5_snack_family="Steamed Snacks",
            level6_specific_food="Unclassified Steamed Snack",
            level7_variant="Steamed white or yellow cake/dumpling without heavy grease; requires visual clarification",
            level8_main_ingredient="Rice/Dal/Flour",
            level9_flour_grain_base="Fermented or leavened batter",
            level10_cooking_method="Steamed",
            level11_filling_or_topping="Uncertain",
            level12_accompaniment="Chutney",
            level13_portion_type="countable_pieces",
            level14_nutrition_ref_id="NUT-SNK-STEAMED-UNKNOWN-001",
        ),
        snack_family="Steamed Snacks",
        specific_food="Unclassified Steamed Snack",
        region="Pan-India",
        state_or_city="Unknown",
        regional_names={"hi": "भाप में पका नाश्ता (अस्पष्ट)", "ta": "வேகவைத்த தின்பண்டம் (தெளிவற்றது)"},
        alternate_names=["Indian steamed snack — exact type uncertain", "Unknown Steamed Snack"],
        base_ingredient="Rice or Dal",
        cooking_method="Steamed",
        shape_profile="Steamed Cake",
        is_fried=False,
        is_steamed=True,
        piece_count_expected=3,
        piece_weight_typical_g=40.0,
        default_portion_grams=120.0,
        visible_oil_typical="Low visible oil",
        nutrition_per_100g={"calories": 140.0, "protein": 5.2, "carbs": 26.5, "fat": 1.2, "fiber": 2.2},
        uncertainty_factors=["Oil tempering presence and sugar content in soak"],
    ),
)

# 4. Indian tiffin — exact dish uncertain
register_snack_food_class(
    SnackFoodClassRecord(
        canonical_food_id="IND-TIF-UNKNOWN-001",
        canonical_name="Indian Tiffin (Dish Uncertain)",
        hierarchy=SnackTiffinHierarchy(
            level3_region="South India",
            level4_state="All",
            level5_snack_family="Tiffin",
            level6_specific_food="Unclassified Tiffin Dish",
            level7_variant="Traditional breakfast/tiffin item served with sambar or chutney",
            level8_main_ingredient="Rice / Lentil / Wheat",
            level9_flour_grain_base="Grain or dal base",
            level10_cooking_method="Steamed or Pan Fried",
            level11_filling_or_topping="Uncertain",
            level12_accompaniment="Sambar, Chutney",
            level13_portion_type="plate_serving",
            level14_nutrition_ref_id="NUT-TIF-UNKNOWN-001",
        ),
        snack_family="Tiffin",
        specific_food="Unclassified Tiffin Dish",
        region="South India",
        state_or_city="Unknown",
        regional_names={"hi": "टिफिन (अस्पष्ट)", "ta": "டிபன் (தெளிவற்றது)", "te": "టిఫిన్ (అస్పష్టం)"},
        alternate_names=["Indian tiffin — exact dish uncertain", "Unknown Tiffin Dish"],
        base_ingredient="Rice or Dal",
        cooking_method="Varies",
        shape_profile="Plate",
        is_tiffin=True,
        piece_count_expected=1,
        piece_weight_typical_g=150.0,
        default_portion_grams=150.0,
        visible_oil_typical="Moderate visible oil",
        nutrition_per_100g={"calories": 170.0, "protein": 4.8, "carbs": 29.0, "fat": 4.2, "fiber": 2.4},
        uncertainty_factors=["Wide macronutrient spread between steamed idli vs oily dosa or poori"],
    ),
)

# 5. Indian chaat — exact type uncertain
register_snack_food_class(
    SnackFoodClassRecord(
        canonical_food_id="IND-SNK-CHAAT-UNKNOWN-001",
        canonical_name="Indian Chaat (Type Uncertain)",
        hierarchy=SnackTiffinHierarchy(
            level3_region="Pan-India",
            level4_state="All",
            level5_snack_family="Chaat",
            level6_specific_food="Unclassified Chaat",
            level7_variant="Assembled street chaat plate containing crisps, potato, curd or chutneys",
            level8_main_ingredient="Papdi/Sev, Potato & Chutneys",
            level9_flour_grain_base="Fried pastry and chickpea sev",
            level10_cooking_method="Assembled",
            level11_filling_or_topping="Curd, chutneys, sev, onion",
            level12_accompaniment="Chutneys",
            level13_portion_type="plate_serving",
            level14_nutrition_ref_id="NUT-SNK-CHAAT-UNKNOWN-001",
        ),
        snack_family="Chaat",
        specific_food="Unclassified Chaat",
        region="Pan-India",
        state_or_city="Unknown",
        regional_names={"hi": "चाट (अस्पष्ट)", "mr": "चाट (अस्पष्ट)"},
        alternate_names=["Indian chaat — exact type uncertain", "Unknown Chaat"],
        base_ingredient="Flour crisps & Chutneys",
        cooking_method="Assembled",
        shape_profile="Assembled plate",
        is_chaat=True,
        piece_count_expected=1,
        piece_weight_typical_g=180.0,
        default_portion_grams=180.0,
        visible_oil_typical="Moderate visible oil",
        nutrition_per_100g={"calories": 210.0, "protein": 4.2, "carbs": 32.0, "fat": 7.5, "fiber": 2.8},
        uncertainty_factors=["Sweet chutney sugar vs fried sev fat contribution"],
    ),
)


def get_snack_record_by_id(canonical_id: str) -> Optional[SnackFoodClassRecord]:
    """Retrieve canonical record by ID."""
    return SNACKS_TAXONOMY_REGISTRY.get(canonical_id) or SNACKS_TAXONOMY_REGISTRY.get(canonical_id.lower())


def resolve_snack_alias(name_or_alias: str) -> Optional[SnackFoodClassRecord]:
    """Resolve an informal or regional snack alias to its canonical record."""
    clean = name_or_alias.lower().strip()
    if clean in SNACKS_SYNONYM_LOOKUP:
        can_id = SNACKS_SYNONYM_LOOKUP[clean]
        return SNACKS_TAXONOMY_REGISTRY.get(can_id)
    return SNACKS_TAXONOMY_REGISTRY.get(clean)
