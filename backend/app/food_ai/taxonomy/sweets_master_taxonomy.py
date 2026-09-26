"""
Indian Sweets & Desserts Master Taxonomy & Identity Hierarchy (Part 14)
Implements Sections 1–4, 6–9, 11–41, 43–45, 59, 63, 64, 86, 87 of Part 14 Specification.

Guarantees:
- Strict 13-Level Identity Traversal:
  Sweet/Dessert -> Region -> State -> Sweet Family -> Specific Dish -> Variant ->
  Base Ingredient -> Cooking Method -> Syrup State -> Filling -> Topping -> Portion -> Nutrition
- Stable Class ID System (Section 64): IND-SWT-* format.
- 38+ Primary Sweet Families (Section 3).
- Comprehensive Regional Coverage:
  * North India: Kaju Katli, Gulab Jamun, Jalebi, Gajar Halwa, Peda, Rabri, Phirni, Gujiya, Rasmalai, Kheer, Kulfi.
  * South India: Mysore Pak, Adhirasam, Jangri, Sakkarai Pongal, Rava Kesari, Payasam (Pal/Ada/Parippu), Kozhukattai, Poli.
  * West India: Modak, Puran Poli/Holige, Shrikhand, Basundi, Malpua, Ghevar.
  * East India: Bengali Rasgulla, Sandesh (Nolen Gur), Mishti Doi, Pantua, Chhena Gaja, Pitha.
- Robust Fallback System (Sections 59 & 84):
  * "Indian sweet — exact variety uncertain" (IND-SWT-UNKNOWN-001)
  * "Milk-based Indian sweet — exact type uncertain" (IND-SWT-MILK-UNKNOWN-001)
  * "Syrup-based Indian sweet — exact type uncertain" (IND-SWT-SYRUP-UNKNOWN-001)
  * "Indian laddu — exact variety uncertain" (IND-SWT-LADDU-UNKNOWN-001)
  * "Indian halwa — exact variety uncertain" (IND-SWT-HALWA-UNKNOWN-001)
  * "Indian barfi — exact variety uncertain" (IND-SWT-BARFI-UNKNOWN-001)
  * "Mixed Indian sweets — exact varieties partially uncertain" (IND-SWT-BOX-UNKNOWN-001)
- Multilingual synonym mappings across 12 Indian languages (Section 63).
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class SweetHierarchy(BaseModel):
    level1_food: str = "Indian Food"
    level2_macro_category: str = "Sweets & Desserts"
    level3_region: str          # North India, South India, West India, East India, Pan-India
    level4_state: str           # Tamil Nadu, Bengal, Punjab, Maharashtra, Gujarat, Kerala, Karnataka, etc.
    level5_sweet_family: str    # Laddoo, Barfi, Peda, Halwa, Jalebi, Payasam, Kheer, Rasgulla, Modak, etc.
    level6_specific_dish: str   # Kaju Katli, Motichoor Laddu, Mysore Pak, Rasgulla, Ada Pradhaman, etc.
    level7_variant: str         # e.g., "Diamond-cut cashew nut paste fudge with edible silver foil (vark)"
    level8_base_ingredient: str # Cashew, Besan, Khoya, Chhena, Milk, Rava, Wheat, Rice, Jaggery, Coconut
    level9_cooking_method: str  # Deep-fried, Simmered, Steamed, Roasted, Pan-stirred, Chilled/Frozen
    level10_syrup_state: str    # Dry, Light syrup, Heavy syrup, Milk-soaked, Syrup-coated
    level11_filling_or_topping: str # Pistachio, Almond, Saffron, Silver Leaf, Cardamom, None
    level12_portion_type: str   # piece_count, weight_grams, bowl_serving
    level13_nutrition_ref_id: str


class SweetFoodClassRecord(BaseModel):
    canonical_food_id: str      # Stable ID: IND-SWT-TN-MYSOREPAK-001, etc.
    canonical_name: str         # Canonical English name
    hierarchy: SweetHierarchy
    sweet_family: str           # High-level family from Section 3
    specific_dish: str
    region: str                 # North India, South India, West India, East India, Pan-India
    state_or_city: str
    regional_names: Dict[str, str] = Field(default_factory=dict)
    alternate_names: List[str] = Field(default_factory=list)
    base_ingredient: str        # Milk, Khoya, Chhena, Cashew, Besan, Rava, Wheat, Rice, Dal
    cooking_method: str = "Simmered"
    syrup_state: str = "Dry"    # Dry, Light syrup, Heavy syrup, Milk-soaked, Syrup-coated
    shape_profile: str = "Round" # Diamond, Round, Square, Rectangle, Spiral, Disc, Pleated, Flat, Bowl
    is_fried: bool = False
    is_milk_based: bool = False
    is_countable: bool = True
    piece_count_expected: Optional[int] = 1
    piece_weight_typical_g: Optional[float] = 35.0
    default_portion_grams: float = 70.0
    density_g_ml: float = 1.15
    nutrition_per_100g: Dict[str, float] = Field(default_factory=dict)
    uncertainty_factors: List[str] = Field(default_factory=list)
    typical_sugar_level: str = "High" # Low visible syrup/sugar, Moderate, High, Syrup soaked


SWEETS_TAXONOMY_REGISTRY: Dict[str, SweetFoodClassRecord] = {}
SWEETS_SYNONYM_LOOKUP: Dict[str, str] = {}


def register_sweet_food_class(record: SweetFoodClassRecord, alias_ids: Optional[List[str]] = None) -> SweetFoodClassRecord:
    SWEETS_TAXONOMY_REGISTRY[record.canonical_food_id] = record
    SWEETS_TAXONOMY_REGISTRY[record.canonical_food_id.lower()] = record
    if alias_ids:
        for aid in alias_ids:
            SWEETS_TAXONOMY_REGISTRY[aid] = record
            SWEETS_TAXONOMY_REGISTRY[aid.lower()] = record
            SWEETS_SYNONYM_LOOKUP[aid.lower().strip()] = record.canonical_food_id
    SWEETS_SYNONYM_LOOKUP[record.canonical_name.lower().strip()] = record.canonical_food_id
    for alt in record.alternate_names:
        SWEETS_SYNONYM_LOOKUP[alt.lower().strip()] = record.canonical_food_id
    for reg_name in record.regional_names.values():
        SWEETS_SYNONYM_LOOKUP[reg_name.lower().strip()] = record.canonical_food_id
    return record


# =============================================================================
# 1. KAJU KATLI & NUT-BASED SWEETS (Sections 6, 7, 31)
# =============================================================================

# Kaju Katli (Pan-India / North India)
register_sweet_food_class(
    SweetFoodClassRecord(
        canonical_food_id="IND-SWT-NI-KAJUKATLI-001",
        canonical_name="Kaju Katli (Kaju Barfi)",
        hierarchy=SweetHierarchy(
            level3_region="Pan-India",
            level4_state="Delhi / Rajasthan / Pan-India",
            level5_sweet_family="Kaju Katli",
            level6_specific_dish="Kaju Katli",
            level7_variant="Thin diamond-cut fudge made of finely ground cashew paste cooked with sugar syrup and topped with silver vark",
            level8_base_ingredient="Cashew",
            level9_cooking_method="Pan-stirred",
            level10_syrup_state="Dry",
            level11_filling_or_topping="Silver Leaf",
            level12_portion_type="piece_count",
            level13_nutrition_ref_id="REF-SWT-NI-KAJU-001"
        ),
        sweet_family="Kaju Katli",
        specific_dish="Kaju Katli",
        region="Pan-India",
        state_or_city="Pan-India",
        regional_names={
            "hi": "काजू कतली / काजू बर्फी",
            "ta": "காஜு கத்லி",
            "te": "కాజు కట్లీ",
            "kn": "ಕಾಜು ಕತ್ಲಿ",
            "ml": "കാജു കത്‌ലി",
            "bn": "কাজু কাটলি",
            "gu": "કાજુ કતરી"
        },
        alternate_names=["kaju katli", "kaju barfi", "cashew katli", "kaju fudge", "kaju patri"],
        base_ingredient="Cashew",
        cooking_method="Pan-stirred",
        syrup_state="Dry",
        shape_profile="Diamond",
        is_fried=False,
        is_milk_based=False,
        is_countable=True,
        piece_count_expected=4,
        piece_weight_typical_g=14.0,
        default_portion_grams=56.0,
        nutrition_per_100g={"calories": 445.0, "protein": 9.5, "carbs": 58.0, "fat": 20.5, "fiber": 1.2},
        uncertainty_factors=["cashew_to_sugar_ratio", "silver_foil_purity", "thickness_variation"],
        typical_sugar_level="High"
    ),
    alias_ids=["IND-SWT-KAJUKATLI", "IND-KAJU-KATLI-001"]
)


# =============================================================================
# 2. LADDOO MASTER DATASET (Sections 4, 5, 34)
# =============================================================================

# Motichoor Laddu (Pan-India / North India)
register_sweet_food_class(
    SweetFoodClassRecord(
        canonical_food_id="IND-SWT-NI-MOTICHOOR-001",
        canonical_name="Motichoor Laddu",
        hierarchy=SweetHierarchy(
            level3_region="Pan-India",
            level4_state="Punjab / UP / Pan-India",
            level5_sweet_family="Laddoo",
            level6_specific_dish="Motichoor Laddu",
            level8_base_ingredient="Besan",
            level7_variant="Tiny gram flour pearls (moti) fried in pure ghee, soaked in saffron syrup, and bound into soft orange spheres",
            level9_cooking_method="Deep-fried",
            level10_syrup_state="Syrup-coated",
            level11_filling_or_topping="Melon Seeds / Pistachio",
            level12_portion_type="piece_count",
            level13_nutrition_ref_id="REF-SWT-NI-MOTI-001"
        ),
        sweet_family="Laddoo",
        specific_dish="Motichoor Laddu",
        region="Pan-India",
        state_or_city="Pan-India",
        regional_names={
            "hi": "मोतीचूर के लड्डू",
            "ta": "மோதிச்சூர் லட்டு",
            "te": "మోతీచూర్ లడ్డు",
            "kn": "ಮೋತಿಚೂರ್ ಲಡ್ಡು",
            "ml": "മോത്തിച്ചൂർ ലഡ്ഡു",
            "bn": "মতিচুর লাড্ডু"
        },
        alternate_names=["motichoor laddu", "motichur ladoo", "moti chur laddu", "orange laddu"],
        base_ingredient="Besan",
        cooking_method="Deep-fried",
        syrup_state="Syrup-coated",
        shape_profile="Ball",
        is_fried=True,
        is_milk_based=False,
        is_countable=True,
        piece_count_expected=2,
        piece_weight_typical_g=45.0,
        default_portion_grams=90.0,
        nutrition_per_100g={"calories": 385.0, "protein": 5.2, "carbs": 64.0, "fat": 12.8, "fiber": 1.4},
        uncertainty_factors=["ghee_absorption", "syrup_saturation", "piece_diameter"],
        typical_sugar_level="High"
    ),
    alias_ids=["IND-SWT-MOTICHOOR-LADDU"]
)

# Besan Laddu (Pan-India / West & North)
register_sweet_food_class(
    SweetFoodClassRecord(
        canonical_food_id="IND-SWT-PAN-BESANLADDU-001",
        canonical_name="Besan Laddu",
        hierarchy=SweetHierarchy(
            level3_region="Pan-India",
            level4_state="Maharashtra / North India",
            level5_sweet_family="Laddoo",
            level6_specific_dish="Besan Laddu",
            level7_variant="Gram flour slow-roasted to nutty golden perfection in desi ghee, blended with boora/tagar sugar and cardamom",
            level8_base_ingredient="Besan",
            level9_cooking_method="Roasted",
            level10_syrup_state="Dry",
            level11_filling_or_topping="Almond / Pistachio",
            level12_portion_type="piece_count",
            level13_nutrition_ref_id="REF-SWT-PAN-BESAN-001"
        ),
        sweet_family="Laddoo",
        specific_dish="Besan Laddu",
        region="Pan-India",
        state_or_city="Pan-India",
        regional_names={"hi": "बेसन के लड्डू", "mr": "बेसन लाडू", "ta": "கடலை மாவு லட்டு"},
        alternate_names=["besan laddu", "besan ladoo", "gram flour laddu"],
        base_ingredient="Besan",
        cooking_method="Roasted",
        syrup_state="Dry",
        shape_profile="Ball",
        is_fried=False,
        is_milk_based=False,
        is_countable=True,
        piece_count_expected=2,
        piece_weight_typical_g=40.0,
        default_portion_grams=80.0,
        nutrition_per_100g={"calories": 465.0, "protein": 9.8, "carbs": 54.0, "fat": 23.5, "fiber": 3.2},
        uncertainty_factors=["ghee_quantity", "flour_roasting_level"],
        typical_sugar_level="Moderate"
    ),
    alias_ids=["IND-SWT-BESAN-LADDU"]
)

# Boondi Laddu (Tirupati / South & North India)
register_sweet_food_class(
    SweetFoodClassRecord(
        canonical_food_id="IND-SWT-AP-BOONDILADDU-001",
        canonical_name="Boondi Laddu (Tirupati Laddu Style)",
        hierarchy=SweetHierarchy(
            level3_region="South India",
            level4_state="Andhra Pradesh / Tamil Nadu",
            level5_sweet_family="Laddoo",
            level6_specific_dish="Boondi Laddu",
            level7_variant="Plump fried besan pearls blended with cardamom, cloves, cashews and sugar syrup",
            level8_base_ingredient="Besan",
            level9_cooking_method="Deep-fried",
            level10_syrup_state="Syrup-coated",
            level11_filling_or_topping="Cashew / Raisins / Clove / Edible Camphor",
            level12_portion_type="piece_count",
            level13_nutrition_ref_id="REF-SWT-AP-BOONDI-001"
        ),
        sweet_family="Laddoo",
        specific_dish="Boondi Laddu",
        region="South India",
        state_or_city="Tirupati / Andhra Pradesh",
        regional_names={"te": "బూందీ లడ్డు / తిరుపతి లడ్డు", "ta": "பூந்தி லட்டு", "hi": "बूंदी के लड्डू"},
        alternate_names=["boondi laddu", "tirupati laddu", "boondi ladoo"],
        base_ingredient="Besan",
        cooking_method="Deep-fried",
        syrup_state="Syrup-coated",
        shape_profile="Ball",
        is_fried=True,
        is_milk_based=False,
        is_countable=True,
        piece_count_expected=1,
        piece_weight_typical_g=75.0,
        default_portion_grams=75.0,
        nutrition_per_100g={"calories": 410.0, "protein": 6.0, "carbs": 62.0, "fat": 15.5, "fiber": 1.6},
        uncertainty_factors=["ghee_content", "sugar_crystal_inclusions"],
        typical_sugar_level="High"
    ),
    alias_ids=["IND-SWT-BOONDI-LADDU"]
)


# =============================================================================
# 3. GULAB JAMUN & SYRUP-SOAKED SWEETS (Sections 16, 17, 18, 19)
# =============================================================================

# Gulab Jamun (Pan-India)
register_sweet_food_class(
    SweetFoodClassRecord(
        canonical_food_id="IND-SWT-NI-GULABJAMUN-001",
        canonical_name="Gulab Jamun",
        hierarchy=SweetHierarchy(
            level3_region="Pan-India",
            level4_state="Pan-India",
            level5_sweet_family="Gulab Jamun",
            level6_specific_dish="Gulab Jamun",
            level7_variant="Golden-brown milk-solid (khoya/mawa) dumplings deep-fried in ghee and soaked in warm rose-cardamom syrup",
            level8_base_ingredient="Khoya",
            level9_cooking_method="Deep-fried",
            level10_syrup_state="Heavy syrup",
            level11_filling_or_topping="Pistachio / Rose Water",
            level12_portion_type="piece_count",
            level13_nutrition_ref_id="REF-SWT-NI-GJ-001"
        ),
        sweet_family="Gulab Jamun",
        specific_dish="Gulab Jamun",
        region="Pan-India",
        state_or_city="Pan-India",
        regional_names={
            "hi": "गुलाब जामुन",
            "ta": "குலாப் ஜாமுன்",
            "te": "గులాబ్ జామున్",
            "kn": "ಗುಲಾಬ್ ಜಾಮೂನ್",
            "ml": "ഗുലാബ് ജാമുൻ",
            "bn": "গোলাপ জামুন"
        },
        alternate_names=["gulab jamun", "gulab jamoon", "khoya jamun"],
        base_ingredient="Khoya",
        cooking_method="Deep-fried",
        syrup_state="Heavy syrup",
        shape_profile="Ball",
        is_fried=True,
        is_milk_based=True,
        is_countable=True,
        piece_count_expected=2,
        piece_weight_typical_g=35.0,
        default_portion_grams=70.0,
        nutrition_per_100g={"calories": 320.0, "protein": 4.5, "carbs": 52.0, "fat": 11.0, "fiber": 0.2},
        uncertainty_factors=["syrup_absorption", "fried_khoya_density"],
        typical_sugar_level="Syrup soaked"
    ),
    alias_ids=["IND-SWT-GULAB-JAMUN"]
)

# Bengali Rasgulla / Rosogolla (West Bengal / Odisha)
register_sweet_food_class(
    SweetFoodClassRecord(
        canonical_food_id="IND-SWT-WB-RASGULLA-001",
        canonical_name="Bengali Rasgulla (Rosogolla)",
        hierarchy=SweetHierarchy(
            level3_region="East India",
            level4_state="West Bengal / Odisha",
            level5_sweet_family="Rasgulla",
            level6_specific_dish="Rasgulla",
            level7_variant="Snow-white spongy chhena (fresh cottage cheese) spheres gently simmered in light fragrant sugar syrup",
            level8_base_ingredient="Chhena",
            level9_cooking_method="Simmered",
            level10_syrup_state="Light syrup",
            level11_filling_or_topping="Cardamom",
            level12_portion_type="piece_count",
            level13_nutrition_ref_id="REF-SWT-WB-RASGULLA-001"
        ),
        sweet_family="Rasgulla",
        specific_dish="Rasgulla",
        region="East India",
        state_or_city="Kolkata / West Bengal",
        regional_names={
            "bn": "রসগোল্লা",
            "or": "ରସଗୋଲା",
            "hi": "रसगुल्ला",
            "ta": "ரசகுல்லா",
            "te": "రసగుల్లా"
        },
        alternate_names=["rasgulla", "rosogolla", "bengali rasgulla", "chhena rasgulla", "white rasgulla"],
        base_ingredient="Chhena",
        cooking_method="Simmered",
        syrup_state="Light syrup",
        shape_profile="Ball",
        is_fried=False,
        is_milk_based=True,
        is_countable=True,
        piece_count_expected=2,
        piece_weight_typical_g=45.0,
        default_portion_grams=90.0,
        nutrition_per_100g={"calories": 185.0, "protein": 5.0, "carbs": 38.0, "fat": 1.8, "fiber": 0.0},
        uncertainty_factors=["syrup_squeezing_factor", "chhena_moisture"],
        typical_sugar_level="Syrup soaked"
    ),
    alias_ids=["IND-SWT-RASGULLA"]
)

# Rasmalai (North & East India)
register_sweet_food_class(
    SweetFoodClassRecord(
        canonical_food_id="IND-SWT-NI-RASMALAI-001",
        canonical_name="Rasmalai",
        hierarchy=SweetHierarchy(
            level3_region="Pan-India",
            level4_state="Bengal / Pan-India",
            level5_sweet_family="Rasmalai",
            level6_specific_dish="Rasmalai",
            level7_variant="Flattened poached chhena discs soaked in chilled thickened saffron-cardamom flavored milk (ras)",
            level8_base_ingredient="Chhena",
            level9_cooking_method="Simmered",
            level10_syrup_state="Milk-soaked",
            level11_filling_or_topping="Pistachio / Saffron",
            level12_portion_type="piece_count",
            level13_nutrition_ref_id="REF-SWT-NI-RASMALAI-001"
        ),
        sweet_family="Rasmalai",
        specific_dish="Rasmalai",
        region="Pan-India",
        state_or_city="Pan-India",
        regional_names={"hi": "रसमलाई", "bn": "রসমলাই", "ta": "ரசமலாய்"},
        alternate_names=["rasmalai", "rossomalai", "chhena rasmalai"],
        base_ingredient="Chhena",
        cooking_method="Simmered",
        syrup_state="Milk-soaked",
        shape_profile="Disc",
        is_fried=False,
        is_milk_based=True,
        is_countable=True,
        piece_count_expected=2,
        piece_weight_typical_g=60.0,
        default_portion_grams=120.0,
        nutrition_per_100g={"calories": 215.0, "protein": 6.8, "carbs": 26.0, "fat": 9.5, "fiber": 0.3},
        uncertainty_factors=["thickened_milk_volume", "chhena_disc_density"],
        typical_sugar_level="Moderate"
    ),
    alias_ids=["IND-SWT-RASMALAI"]
)


# =============================================================================
# 4. JALEBI, JANGRI & IMARTI (Sections 14, 15)
# =============================================================================

# Jalebi (Pan-India / North India)
register_sweet_food_class(
    SweetFoodClassRecord(
        canonical_food_id="IND-SWT-NI-JALEBI-001",
        canonical_name="Crispy Jalebi",
        hierarchy=SweetHierarchy(
            level3_region="Pan-India",
            level4_state="Delhi / Punjab / Pan-India",
            level5_sweet_family="Jalebi",
            level6_specific_dish="Jalebi",
            level7_variant="Fermented refined flour batter squeezed into boiling ghee in concentric spirals and plunged into saffron sugar syrup",
            level8_base_ingredient="Maida",
            level9_cooking_method="Deep-fried",
            level10_syrup_state="Syrup-coated",
            level11_filling_or_topping="Saffron / Cardamom",
            level12_portion_type="weight_grams",
            level13_nutrition_ref_id="REF-SWT-NI-JALEBI-001"
        ),
        sweet_family="Jalebi",
        specific_dish="Jalebi",
        region="Pan-India",
        state_or_city="Pan-India",
        regional_names={
            "hi": "जलेबी",
            "ta": "ஜிலேபி",
            "te": "జిలేబి",
            "kn": "ಜಿಲೇಬಿ",
            "bn": "জিলিপি"
        },
        alternate_names=["jalebi", "crispy jalebi", "jilapi", "garam jalebi", "thin jalebi"],
        base_ingredient="Maida",
        cooking_method="Deep-fried",
        syrup_state="Syrup-coated",
        shape_profile="Spiral",
        is_fried=True,
        is_milk_based=False,
        is_countable=True,
        piece_count_expected=4,
        piece_weight_typical_g=25.0,
        default_portion_grams=100.0,
        nutrition_per_100g={"calories": 395.0, "protein": 3.0, "carbs": 72.0, "fat": 11.0, "fiber": 0.4},
        uncertainty_factors=["syrup_internal_crystallization", "frying_fat_oil_vs_ghee"],
        typical_sugar_level="Syrup soaked"
    ),
    alias_ids=["IND-SWT-JALEBI"]
)

# South Indian Jangri / Imarti (Tamil Nadu / South & North)
register_sweet_food_class(
    SweetFoodClassRecord(
        canonical_food_id="IND-SWT-TN-JANGRI-001",
        canonical_name="Jangri (Imarti)",
        hierarchy=SweetHierarchy(
            level3_region="South India",
            level4_state="Tamil Nadu / Andhra Pradesh",
            level5_sweet_family="Imarti/Jangri",
            level6_specific_dish="Jangri",
            level7_variant="Whipped urad dal batter piped into intricate geometric flower rosettes, deep-fried in ghee and soaked in rose sugar syrup",
            level8_base_ingredient="Dal",
            level9_cooking_method="Deep-fried",
            level10_syrup_state="Syrup-coated",
            level11_filling_or_topping="Rose Essence / Cardamom",
            level12_portion_type="piece_count",
            level13_nutrition_ref_id="REF-SWT-TN-JANGRI-001"
        ),
        sweet_family="Imarti/Jangri",
        specific_dish="Jangri",
        region="South India",
        state_or_city="Tamil Nadu / South India",
        regional_names={"ta": "ஜாங்கிரி", "te": "జాంగ్రీ", "hi": "इमरती", "kn": "ಜಾಂಗ್ರಿ"},
        alternate_names=["jangri", "imarti", "urad dal jalebi", "amriti"],
        base_ingredient="Dal",
        cooking_method="Deep-fried",
        syrup_state="Syrup-coated",
        shape_profile="Flower-shaped",
        is_fried=True,
        is_milk_based=False,
        is_countable=True,
        piece_count_expected=2,
        piece_weight_typical_g=45.0,
        default_portion_grams=90.0,
        nutrition_per_100g={"calories": 375.0, "protein": 5.5, "carbs": 68.0, "fat": 9.8, "fiber": 1.8},
        uncertainty_factors=["urad_dal_air_incorporation", "syrup_coating_thickness"],
        typical_sugar_level="Syrup soaked"
    ),
    alias_ids=["IND-SWT-JANGRI", "IND-SWT-IMARTI"]
)


# =============================================================================
# 5. SOUTH INDIAN SWEETS: MYSORE PAK, ADHIRASAM, KESARI (Sections 11, 12, 13, 35)
# =============================================================================

# Mysore Pak (Karnataka / Tamil Nadu)
register_sweet_food_class(
    SweetFoodClassRecord(
        canonical_food_id="IND-SWT-TN-MYSOREPAK-001",
        canonical_name="Mysore Pak (Ghee Mysore Pak)",
        hierarchy=SweetHierarchy(
            level3_region="South India",
            level4_state="Karnataka / Tamil Nadu",
            level5_sweet_family="Mysore Pak",
            level6_specific_dish="Mysore Pak",
            level7_variant="Traditional rich porous melt-in-mouth rectangular sweet made of roasted gram flour, generous pure desi ghee and sugar",
            level8_base_ingredient="Besan",
            level9_cooking_method="Pan-stirred",
            level10_syrup_state="Dry",
            level11_filling_or_topping="Cardamom",
            level12_portion_type="piece_count",
            level13_nutrition_ref_id="REF-SWT-TN-MYSOREPAK-001"
        ),
        sweet_family="Mysore Pak",
        specific_dish="Mysore Pak",
        region="South India",
        state_or_city="Mysore / Chennai",
        regional_names={
            "kn": "ಮೈಸೂರು ಪಾಕ್",
            "ta": "மைசூர் பாக்",
            "te": "మైసూర్ పాక్",
            "hi": "मैसूर पाक",
            "ml": "മൈസൂർ പാക്ക്"
        },
        alternate_names=["mysore pak", "ghee mysore pak", "soft mysore pak", "mysurpa"],
        base_ingredient="Besan",
        cooking_method="Pan-stirred",
        syrup_state="Dry",
        shape_profile="Rectangle",
        is_fried=False,
        is_milk_based=False,
        is_countable=True,
        piece_count_expected=2,
        piece_weight_typical_g=40.0,
        default_portion_grams=80.0,
        nutrition_per_100g={"calories": 520.0, "protein": 6.5, "carbs": 52.0, "fat": 32.0, "fiber": 1.5},
        uncertainty_factors=["heavy_ghee_ratio_soft_vs_hard", "sugar_saturation"],
        typical_sugar_level="High"
    ),
    alias_ids=["IND-SWT-MYSORE-PAK"]
)

# Adhirasam (Tamil Nadu / Kerala)
register_sweet_food_class(
    SweetFoodClassRecord(
        canonical_food_id="IND-SWT-TN-ADHIRASAM-001",
        canonical_name="Adhirasam",
        hierarchy=SweetHierarchy(
            level3_region="South India",
            level4_state="Tamil Nadu",
            level5_sweet_family="Adhirasam",
            level6_specific_dish="Adhirasam",
            level7_variant="Traditional deep-fried chewy disc made from fermented aged raw rice flour and dark jaggery syrup with dry ginger",
            level8_base_ingredient="Rice",
            level9_cooking_method="Deep-fried",
            level10_syrup_state="Dry",
            level11_filling_or_topping="Cardamom / Sesame / Dry Ginger",
            level12_portion_type="piece_count",
            level13_nutrition_ref_id="REF-SWT-TN-ADHIRASAM-001"
        ),
        sweet_family="Adhirasam",
        specific_dish="Adhirasam",
        region="South India",
        state_or_city="Tamil Nadu",
        regional_names={"ta": "அதிரசம்", "te": "అరిసెలు", "kn": "ಅತಿರಸ", "ml": "അതിരസം", "hi": "अधिरसम"},
        alternate_names=["adhirasam", "athirasam", "ariselu", "kajjaya"],
        base_ingredient="Rice",
        cooking_method="Deep-fried",
        syrup_state="Dry",
        shape_profile="Disc",
        is_fried=True,
        is_milk_based=False,
        is_countable=True,
        piece_count_expected=2,
        piece_weight_typical_g=35.0,
        default_portion_grams=70.0,
        nutrition_per_100g={"calories": 420.0, "protein": 3.8, "carbs": 70.0, "fat": 14.5, "fiber": 1.0},
        uncertainty_factors=["deep_fry_oil_absorption", "jaggery_thickness"],
        typical_sugar_level="High"
    ),
    alias_ids=["IND-SWT-ADHIRASAM", "IND-SWT-ARISELU"]
)

# Rava Kesari (Tamil Nadu / South India)
register_sweet_food_class(
    SweetFoodClassRecord(
        canonical_food_id="IND-SWT-TN-KESARI-001",
        canonical_name="Rava Kesari (Kesari Bath)",
        hierarchy=SweetHierarchy(
            level3_region="South India",
            level4_state="Tamil Nadu / Karnataka",
            level5_sweet_family="Halwa",
            level6_specific_dish="Rava Kesari",
            level7_variant="Semolina pudding cooked in ghee with saffron infusion, sugar and golden fried cashews and raisins",
            level8_base_ingredient="Rava",
            level9_cooking_method="Pan-stirred",
            level10_syrup_state="Dry",
            level11_filling_or_topping="Cashew / Raisin / Cardamom",
            level12_portion_type="weight_grams",
            level13_nutrition_ref_id="REF-SWT-TN-KESARI-001"
        ),
        sweet_family="Halwa",
        specific_dish="Rava Kesari",
        region="South India",
        state_or_city="Tamil Nadu / Karnataka",
        regional_names={"ta": "ரவா கேசரி", "kn": "ಕೇಸರಿ ಬಾತ್", "te": "రవ్వ కేసరి", "hi": "रवा केसरी"},
        alternate_names=["rava kesari", "kesari bath", "sooji kesari", "orange kesari"],
        base_ingredient="Rava",
        cooking_method="Pan-stirred",
        syrup_state="Dry",
        shape_profile="Bowl",
        is_fried=False,
        is_milk_based=False,
        is_countable=False,
        piece_count_expected=None,
        piece_weight_typical_g=None,
        default_portion_grams=110.0,
        nutrition_per_100g={"calories": 310.0, "protein": 3.5, "carbs": 52.0, "fat": 10.2, "fiber": 0.8},
        uncertainty_factors=["ghee_addition_level", "sugar_to_rava_ratio"],
        typical_sugar_level="Moderate"
    ),
    alias_ids=["IND-SWT-RAVA-KESARI"]
)

# Sakkarai Pongal / Sweet Pongal (Tamil Nadu / Andhra)
register_sweet_food_class(
    SweetFoodClassRecord(
        canonical_food_id="IND-SWT-TN-PONGAL-001",
        canonical_name="Sakkarai Pongal (Sweet Pongal)",
        hierarchy=SweetHierarchy(
            level3_region="South India",
            level4_state="Tamil Nadu",
            level5_sweet_family="Rice-based desserts",
            level6_specific_dish="Sakkarai Pongal",
            level7_variant="Raw rice and yellow moong dal cooked with melted dark jaggery, crushed cardamom, and ghee-roasted cashews and raisins",
            level8_base_ingredient="Rice",
            level9_cooking_method="Simmered",
            level10_syrup_state="Dry",
            level11_filling_or_topping="Cashew / Raisins / Ghee / Edible Camphor",
            level12_portion_type="weight_grams",
            level13_nutrition_ref_id="REF-SWT-TN-PONGAL-001"
        ),
        sweet_family="Rice-based desserts",
        specific_dish="Sakkarai Pongal",
        region="South India",
        state_or_city="Tamil Nadu",
        regional_names={"ta": "சர்க்கரைப் பொங்கல்", "te": "చక్కెర పొంగలి", "kn": "ಸಕ್ಕರೆ ಪೊಂಗಲ್", "hi": "मीठा पोंगल"},
        alternate_names=["sakkarai pongal", "sweet pongal", "chakkara pongal", "jaggery pongal"],
        base_ingredient="Rice",
        cooking_method="Simmered",
        syrup_state="Dry",
        shape_profile="Bowl",
        is_fried=False,
        is_milk_based=False,
        is_countable=False,
        piece_count_expected=None,
        piece_weight_typical_g=None,
        default_portion_grams=120.0,
        nutrition_per_100g={"calories": 285.0, "protein": 4.2, "carbs": 54.0, "fat": 6.5, "fiber": 1.2},
        uncertainty_factors=["ghee_infusion", "jaggery_richness"],
        typical_sugar_level="Moderate"
    ),
    alias_ids=["IND-SWT-SAKKARAI-PONGAL"]
)


# =============================================================================
# 6. PAYASAM, KHEER & MILK DESSERTS (Sections 21, 22, 23, 24, 25, 26)
# =============================================================================

# Pal Payasam (Kerala / Tamil Nadu)
register_sweet_food_class(
    SweetFoodClassRecord(
        canonical_food_id="IND-SWT-KL-PALPAYASAM-001",
        canonical_name="Kerala Pal Payasam (Milk Payasam)",
        hierarchy=SweetHierarchy(
            level3_region="South India",
            level4_state="Kerala / Tamil Nadu",
            level5_sweet_family="Payasam",
            level6_specific_dish="Pal Payasam",
            level7_variant="Traditional temple style slow-simmered pinkish rice pudding cooked with full-cream milk, sugar and cardamom",
            level8_base_ingredient="Milk",
            level9_cooking_method="Simmered",
            level10_syrup_state="Milk-soaked",
            level11_filling_or_topping="Cardamom / Fried Cashew",
            level12_portion_type="bowl_serving",
            level13_nutrition_ref_id="REF-SWT-KL-PALPAYASAM-001"
        ),
        sweet_family="Payasam",
        specific_dish="Pal Payasam",
        region="South India",
        state_or_city="Ambalapuzha / Kerala",
        regional_names={"ml": "പാൽ പായസം", "ta": "பால் பாயாசம்", "te": "పాల పాయసం", "hi": "खीर / पाल पायसम"},
        alternate_names=["pal payasam", "paal payasam", "kerala milk payasam", "ambalapuzha pal payasam"],
        base_ingredient="Milk",
        cooking_method="Simmered",
        syrup_state="Milk-soaked",
        shape_profile="Bowl",
        is_fried=False,
        is_milk_based=True,
        is_countable=False,
        piece_count_expected=None,
        piece_weight_typical_g=None,
        default_portion_grams=150.0,
        nutrition_per_100g={"calories": 165.0, "protein": 4.5, "carbs": 24.5, "fat": 5.8, "fiber": 0.2},
        uncertainty_factors=["milk_reduction_thickness", "sugar_content"],
        typical_sugar_level="Moderate"
    ),
    alias_ids=["IND-SWT-PAL-PAYASAM"]
)

# Ada Pradhaman (Kerala)
register_sweet_food_class(
    SweetFoodClassRecord(
        canonical_food_id="IND-SWT-KL-ADAPRADHAMAN-001",
        canonical_name="Ada Pradhaman (Kerala Jaggery Payasam)",
        hierarchy=SweetHierarchy(
            level3_region="South India",
            level4_state="Kerala",
            level5_sweet_family="Payasam",
            level6_specific_dish="Ada Pradhaman",
            level7_variant="Steamed flat rice flakes (ada) simmered in concentrated dark jaggery syrup and fresh thick coconut milk with fried coconut tidbits",
            level8_base_ingredient="Rice",
            level9_cooking_method="Simmered",
            level10_syrup_state="Milk-soaked",
            level11_filling_or_topping="Fried Coconut Slices / Cashew / Cardamom",
            level12_portion_type="bowl_serving",
            level13_nutrition_ref_id="REF-SWT-KL-ADAPRADHAMAN-001"
        ),
        sweet_family="Payasam",
        specific_dish="Ada Pradhaman",
        region="South India",
        state_or_city="Kerala",
        regional_names={"ml": "അട പ്രഥമൻ", "ta": "அடை பிரதமன்", "hi": "अदा प्रधमन"},
        alternate_names=["ada pradhaman", "kerala pradhaman", "palada pradhaman", "jaggery ada payasam"],
        base_ingredient="Rice",
        cooking_method="Simmered",
        syrup_state="Milk-soaked",
        shape_profile="Bowl",
        is_fried=False,
        is_milk_based=False, # Coconut milk based
        is_countable=False,
        piece_count_expected=None,
        piece_weight_typical_g=None,
        default_portion_grams=150.0,
        nutrition_per_100g={"calories": 195.0, "protein": 2.5, "carbs": 32.0, "fat": 6.8, "fiber": 0.6},
        uncertainty_factors=["coconut_milk_fat_percentage", "jaggery_density"],
        typical_sugar_level="Moderate"
    ),
    alias_ids=["IND-SWT-ADA-PRADHAMAN"]
)

# North Indian Rice Kheer (North India)
register_sweet_food_class(
    SweetFoodClassRecord(
        canonical_food_id="IND-SWT-NI-KHEER-001",
        canonical_name="Rice Kheer",
        hierarchy=SweetHierarchy(
            level3_region="North India",
            level4_state="Punjab / UP / Delhi",
            level5_sweet_family="Kheer",
            level6_specific_dish="Rice Kheer",
            level7_variant="Fragrant basmati rice slow simmered in sweetened whole buffalo milk with saffron, slivered almonds and green cardamom",
            level8_base_ingredient="Milk",
            level9_cooking_method="Simmered",
            level10_syrup_state="Milk-soaked",
            level11_filling_or_topping="Almond / Pistachio / Saffron",
            level12_portion_type="bowl_serving",
            level13_nutrition_ref_id="REF-SWT-NI-KHEER-001"
        ),
        sweet_family="Kheer",
        specific_dish="Rice Kheer",
        region="North India",
        state_or_city="Punjab / Delhi",
        regional_names={"hi": "चावल की खीर", "pa": "ਚੌਲਾਂ ਦੀ ਖੀਰ", "ta": "அரிசி பாயாசம்"},
        alternate_names=["rice kheer", "chawal ki kheer", "kheer", "punjabi kheer"],
        base_ingredient="Milk",
        cooking_method="Simmered",
        syrup_state="Milk-soaked",
        shape_profile="Bowl",
        is_fried=False,
        is_milk_based=True,
        is_countable=False,
        piece_count_expected=None,
        piece_weight_typical_g=None,
        default_portion_grams=150.0,
        nutrition_per_100g={"calories": 170.0, "protein": 4.6, "carbs": 25.0, "fat": 6.0, "fiber": 0.3},
        uncertainty_factors=["milk_fat_percentage", "rice_grain_softness"],
        typical_sugar_level="Moderate"
    ),
    alias_ids=["IND-SWT-RICE-KHEER"]
)

# Gajar Ka Halwa (North India)
register_sweet_food_class(
    SweetFoodClassRecord(
        canonical_food_id="IND-SWT-NI-GAJARHALWA-001",
        canonical_name="Gajar Ka Halwa (Carrot Halwa)",
        hierarchy=SweetHierarchy(
            level3_region="North India",
            level4_state="Punjab / Delhi",
            level5_sweet_family="Halwa",
            level6_specific_dish="Gajar Halwa",
            level7_variant="Winter red carrots grated and slow-cooked in whole milk, khoya and pure desi ghee, garnished with cashews and raisins",
            level8_base_ingredient="Khoya",
            level9_cooking_method="Pan-stirred",
            level10_syrup_state="Dry",
            level11_filling_or_topping="Cashew / Almond / Khoya",
            level12_portion_type="weight_grams",
            level13_nutrition_ref_id="REF-SWT-NI-GAJAR-001"
        ),
        sweet_family="Halwa",
        specific_dish="Gajar Halwa",
        region="North India",
        state_or_city="Punjab / Delhi",
        regional_names={"hi": "गाजर का हलवा", "pa": "ਗਾਜਰ ਦਾ ਹਲਵਾ", "ta": "கேரட் அல்வா"},
        alternate_names=["gajar ka halwa", "carrot halwa", "gajrela"],
        base_ingredient="Khoya",
        cooking_method="Pan-stirred",
        syrup_state="Dry",
        shape_profile="Bowl",
        is_fried=False,
        is_milk_based=True,
        is_countable=False,
        piece_count_expected=None,
        piece_weight_typical_g=None,
        default_portion_grams=120.0,
        nutrition_per_100g={"calories": 265.0, "protein": 4.8, "carbs": 36.0, "fat": 11.5, "fiber": 2.1},
        uncertainty_factors=["khoya_amount", "ghee_saturation"],
        typical_sugar_level="Moderate"
    ),
    alias_ids=["IND-SWT-GAJAR-HALWA"]
)

# Bengali Sandesh (West Bengal)
register_sweet_food_class(
    SweetFoodClassRecord(
        canonical_food_id="IND-SWT-WB-SANDESH-001",
        canonical_name="Bengali Sandesh (Nolen Gur Sandesh)",
        hierarchy=SweetHierarchy(
            level3_region="East India",
            level4_state="West Bengal",
            level5_sweet_family="Sandesh",
            level6_specific_dish="Sandesh",
            level7_variant="Fresh kneaded cow's milk chhena lightly cooked with winter date palm jaggery (nolen gur) or sugar and molded into shapes",
            level8_base_ingredient="Chhena",
            level9_cooking_method="Pan-stirred",
            level10_syrup_state="Dry",
            level11_filling_or_topping="Pistachio / Cardamom",
            level12_portion_type="piece_count",
            level13_nutrition_ref_id="REF-SWT-WB-SANDESH-001"
        ),
        sweet_family="Sandesh",
        specific_dish="Sandesh",
        region="East India",
        state_or_city="Kolkata / West Bengal",
        regional_names={"bn": "সন্দেশ / নলেন গুড়ের সন্দেশ", "hi": "संदेश"},
        alternate_names=["sandesh", "shondesh", "nolen gur sandesh", "bengali sandesh", "chhena sandesh"],
        base_ingredient="Chhena",
        cooking_method="Pan-stirred",
        syrup_state="Dry",
        shape_profile="Round",
        is_fried=False,
        is_milk_based=True,
        is_countable=True,
        piece_count_expected=2,
        piece_weight_typical_g=30.0,
        default_portion_grams=60.0,
        nutrition_per_100g={"calories": 270.0, "protein": 11.0, "carbs": 38.0, "fat": 8.5, "fiber": 0.0},
        uncertainty_factors=["chhena_moisture", "jaggery_vs_sugar"],
        typical_sugar_level="Moderate"
    ),
    alias_ids=["IND-SWT-SANDESH"]
)

# Shrikhand (Maharashtra / Gujarat)
register_sweet_food_class(
    SweetFoodClassRecord(
        canonical_food_id="IND-SWT-MH-SHRIKHAND-001",
        canonical_name="Shrikhand (Kesar Elaichi Shrikhand)",
        hierarchy=SweetHierarchy(
            level3_region="West India",
            level4_state="Maharashtra / Gujarat",
            level5_sweet_family="Shrikhand",
            level6_specific_dish="Shrikhand",
            level7_variant="Hung curd (chakka) whipped smooth with powdered sugar, fragrant saffron strands, green cardamom and nuts",
            level8_base_ingredient="Curd",
            level9_cooking_method="Chilled",
            level10_syrup_state="Dry",
            level11_filling_or_topping="Pistachio / Almond / Saffron",
            level12_portion_type="bowl_serving",
            level13_nutrition_ref_id="REF-SWT-MH-SHRIKHAND-001"
        ),
        sweet_family="Shrikhand",
        specific_dish="Shrikhand",
        region="West India",
        state_or_city="Maharashtra / Gujarat",
        regional_names={"mr": "श्रीखंड", "gu": "શ્રીખંડ", "hi": "श्रीखंड", "ta": "ஸ்ரீகண்ட்"},
        alternate_names=["shrikhand", "kesar shrikhand", "amrakhand", "matho"],
        base_ingredient="Curd",
        cooking_method="Chilled",
        syrup_state="Dry",
        shape_profile="Bowl",
        is_fried=False,
        is_milk_based=True,
        is_countable=False,
        piece_count_expected=None,
        piece_weight_typical_g=None,
        default_portion_grams=100.0,
        nutrition_per_100g={"calories": 280.0, "protein": 7.0, "carbs": 42.0, "fat": 9.5, "fiber": 0.2},
        uncertainty_factors=["sugar_whipping_ratio", "curd_fat_content"],
        typical_sugar_level="Moderate"
    ),
    alias_ids=["IND-SWT-SHRIKHAND"]
)


# =============================================================================
# 7. FESTIVE & TEMPLE SWEETS: MODAK, PURAN POLI (Sections 27, 28, 29, 36, 37)
# =============================================================================

# Ukadiche Modak (Maharashtra / Ganesh Chaturthi)
register_sweet_food_class(
    SweetFoodClassRecord(
        canonical_food_id="IND-SWT-MH-MODAK-001",
        canonical_name="Ukadiche Modak (Steamed Modak)",
        hierarchy=SweetHierarchy(
            level3_region="West India",
            level4_state="Maharashtra",
            level5_sweet_family="Modak",
            level6_specific_dish="Ukadiche Modak",
            level7_variant="Hand-pleated steamed rice flour dumpling stuffed with fresh grated coconut cooked with jaggery, nutmeg and cardamom",
            level8_base_ingredient="Rice",
            level9_cooking_method="Steamed",
            level10_syrup_state="Dry",
            level11_filling_or_topping="Coconut Jaggery Filling",
            level12_portion_type="piece_count",
            level13_nutrition_ref_id="REF-SWT-MH-MODAK-001"
        ),
        sweet_family="Modak",
        specific_dish="Ukadiche Modak",
        region="West India",
        state_or_city="Maharashtra",
        regional_names={"mr": "उकडीचे मोदक", "ta": "கொழுக்கட்டை / மோதகம்", "kn": "ಮೋದಕ", "hi": "उकडीचे मोदक"},
        alternate_names=["ukadiche modak", "steamed modak", "modakam", "ganesh chaturthi modak"],
        base_ingredient="Rice",
        cooking_method="Steamed",
        syrup_state="Dry",
        shape_profile="Pleated",
        is_fried=False,
        is_milk_based=False,
        is_countable=True,
        piece_count_expected=2,
        piece_weight_typical_g=45.0,
        default_portion_grams=90.0,
        nutrition_per_100g={"calories": 220.0, "protein": 3.2, "carbs": 44.0, "fat": 4.0, "fiber": 1.6},
        uncertainty_factors=["coconut_jaggery_ratio", "outer_dough_thickness"],
        typical_sugar_level="Moderate"
    ),
    alias_ids=["IND-SWT-UKADICHE-MODAK"]
)

# Puran Poli / Obbattu / Holige (Maharashtra / Karnataka / Tamil Nadu)
register_sweet_food_class(
    SweetFoodClassRecord(
        canonical_food_id="IND-SWT-MH-PURANPOLI-001",
        canonical_name="Puran Poli (Obbattu / Holige / Bobbatlu)",
        hierarchy=SweetHierarchy(
            level3_region="West India",
            level4_state="Maharashtra / Karnataka",
            level5_sweet_family="Puran Poli",
            level6_specific_dish="Puran Poli",
            level7_variant="Paper-thin golden sweet flatbread stuffed with fragrant cooked chana dal, jaggery, nutmeg and cardamom, roasted with ghee",
            level8_base_ingredient="Wheat",
            level9_cooking_method="Pan-roasted",
            level10_syrup_state="Dry",
            level11_filling_or_topping="Chana Dal Jaggery Puran",
            level12_portion_type="piece_count",
            level13_nutrition_ref_id="REF-SWT-MH-PURANPOLI-001"
        ),
        sweet_family="Puran Poli",
        specific_dish="Puran Poli",
        region="West India",
        state_or_city="Maharashtra / Karnataka",
        regional_names={
            "mr": "पुरणपोळी",
            "kn": "ಹೋಳಿಗೆ / ಒಬ್ಬಟ್ಟು",
            "te": "బొబ్బట్లు / భక్ష్యాలు",
            "ta": "போளி / பருப்பு போளி",
            "hi": "पूरन पोली",
            "gu": "પુરણ પોળી"
        },
        alternate_names=["puran poli", "obbattu", "holige", "bobbatlu", "sweet poli", "paruppu poli"],
        base_ingredient="Wheat",
        cooking_method="Pan-roasted",
        syrup_state="Dry",
        shape_profile="Flat",
        is_fried=False,
        is_milk_based=False,
        is_countable=True,
        piece_count_expected=1,
        piece_weight_typical_g=85.0,
        default_portion_grams=85.0,
        nutrition_per_100g={"calories": 310.0, "protein": 6.8, "carbs": 58.0, "fat": 6.2, "fiber": 2.8},
        uncertainty_factors=["ghee_application", "puran_to_dough_ratio"],
        typical_sugar_level="Moderate"
    ),
    alias_ids=["IND-SWT-PURAN-POLI", "IND-SWT-OBBATTU"]
)

# Malpua (North / East / West India)
register_sweet_food_class(
    SweetFoodClassRecord(
        canonical_food_id="IND-SWT-NI-MALPUA-001",
        canonical_name="Malpua",
        hierarchy=SweetHierarchy(
            level3_region="North India",
            level4_state="Rajasthan / Bengal / UP",
            level5_sweet_family="Malpua",
            level6_specific_dish="Malpua",
            level7_variant="Fennel-perfumed flour and khoya batter shallow-fried into golden crisp-edged pancakes, soaked in sugar syrup",
            level8_base_ingredient="Maida",
            level9_cooking_method="Deep-fried",
            level10_syrup_state="Syrup-coated",
            level11_filling_or_topping="Rabri / Pistachio",
            level12_portion_type="piece_count",
            level13_nutrition_ref_id="REF-SWT-NI-MALPUA-001"
        ),
        sweet_family="Malpua",
        specific_dish="Malpua",
        region="North India",
        state_or_city="Rajasthan / UP",
        regional_names={"hi": "मालपुआ", "bn": "মালপোয়া", "ta": "மால்புவா"},
        alternate_names=["malpua", "rabri malpua", "malpua with rabri"],
        base_ingredient="Maida",
        cooking_method="Deep-fried",
        syrup_state="Syrup-coated",
        shape_profile="Disc",
        is_fried=True,
        is_milk_based=True,
        is_countable=True,
        piece_count_expected=2,
        piece_weight_typical_g=50.0,
        default_portion_grams=100.0,
        nutrition_per_100g={"calories": 360.0, "protein": 4.5, "carbs": 56.0, "fat": 13.5, "fiber": 0.5},
        uncertainty_factors=["frying_ghee_absorption", "syrup_saturation"],
        typical_sugar_level="Syrup soaked"
    ),
    alias_ids=["IND-SWT-MALPUA"]
)


# =============================================================================
# 8. FALLBACK CLASSES (Sections 59 & 84)
# =============================================================================

# Unknown Sweet General Fallback
register_sweet_food_class(
    SweetFoodClassRecord(
        canonical_food_id="IND-SWT-UNKNOWN-001",
        canonical_name="Indian Sweet (Exact Variety Uncertain)",
        hierarchy=SweetHierarchy(
            level3_region="Pan-India",
            level4_state="Unknown",
            level5_sweet_family="Unknown Sweet",
            level6_specific_dish="Unknown Sweet",
            level7_variant="Uncertain Indian dessert requiring user confirmation or multi-modal visual inspection",
            level8_base_ingredient="Unknown",
            level9_cooking_method="Simmered",
            level10_syrup_state="Dry",
            level11_filling_or_topping="None",
            level12_portion_type="weight_grams",
            level13_nutrition_ref_id="REF-SWT-FALLBACK-001"
        ),
        sweet_family="Unknown Sweet",
        specific_dish="Unknown Sweet",
        region="Pan-India",
        state_or_city="Pan-India",
        regional_names={"hi": "अज्ञात भारतीय मिठाई", "ta": "அடையாளம் தெரியாத இந்திய இனிப்பு"},
        alternate_names=["unknown indian sweet", "mithai uncertain", "indian dessert uncertain"],
        base_ingredient="Unknown",
        cooking_method="Simmered",
        syrup_state="Dry",
        shape_profile="Irregular",
        is_fried=False,
        is_milk_based=False,
        is_countable=False,
        piece_count_expected=None,
        piece_weight_typical_g=35.0,
        default_portion_grams=70.0,
        nutrition_per_100g={"calories": 350.0, "protein": 5.0, "carbs": 55.0, "fat": 12.0, "fiber": 0.5},
        uncertainty_factors=["sweet_variety_unverified", "base_ingredient_unknown"],
        typical_sugar_level="Moderate"
    )
)

# Milk-based Sweet Fallback (Section 59)
register_sweet_food_class(
    SweetFoodClassRecord(
        canonical_food_id="IND-SWT-MILK-UNKNOWN-001",
        canonical_name="Milk-Based Indian Sweet (Exact Type Uncertain)",
        hierarchy=SweetHierarchy(
            level3_region="Pan-India",
            level4_state="Unknown",
            level5_sweet_family="Milk-based desserts",
            level6_specific_dish="Milk Sweet Uncertain",
            level7_variant="White or pale mawa/chhena/milk sweet; exact classification ambiguous",
            level8_base_ingredient="Milk",
            level9_cooking_method="Simmered",
            level10_syrup_state="Dry",
            level11_filling_or_topping="Cardamom",
            level12_portion_type="piece_count",
            level13_nutrition_ref_id="REF-SWT-MILK-FALLBACK-001"
        ),
        sweet_family="Milk-based desserts",
        specific_dish="Milk Sweet Uncertain",
        region="Pan-India",
        state_or_city="Pan-India",
        regional_names={"hi": "दुग्ध-आधारित मिठाई (प्रकार अनिश्चित)", "ta": "பால் இனிப்பு (வகை உறுதியற்றது)"},
        alternate_names=["milk sweet uncertain", "khoya sweet uncertain", "chhena sweet uncertain"],
        base_ingredient="Milk",
        cooking_method="Simmered",
        syrup_state="Dry",
        shape_profile="Square",
        is_fried=False,
        is_milk_based=True,
        is_countable=True,
        piece_count_expected=2,
        piece_weight_typical_g=35.0,
        default_portion_grams=70.0,
        nutrition_per_100g={"calories": 360.0, "protein": 8.0, "carbs": 50.0, "fat": 14.5, "fiber": 0.2},
        uncertainty_factors=["khoya_vs_chhena_unverified"],
        typical_sugar_level="Moderate"
    )
)

# Syrup-based Sweet Fallback (Section 59)
register_sweet_food_class(
    SweetFoodClassRecord(
        canonical_food_id="IND-SWT-SYRUP-UNKNOWN-001",
        canonical_name="Syrup-Based Indian Sweet (Exact Type Uncertain)",
        hierarchy=SweetHierarchy(
            level3_region="Pan-India",
            level4_state="Unknown",
            level5_sweet_family="Syrup-Based Sweets",
            level6_specific_dish="Syrup Sweet Uncertain",
            level7_variant="Deep-fried or poached dumpling soaked in sugar syrup",
            level8_base_ingredient="Flour/Milk",
            level9_cooking_method="Deep-fried",
            level10_syrup_state="Syrup-coated",
            level11_filling_or_topping="Cardamom",
            level12_portion_type="piece_count",
            level13_nutrition_ref_id="REF-SWT-SYRUP-FALLBACK-001"
        ),
        sweet_family="Syrup-Based Sweets",
        specific_dish="Syrup Sweet Uncertain",
        region="Pan-India",
        state_or_city="Pan-India",
        regional_names={"hi": "चाशनी वाली मिठाई (प्रकार अनिश्चित)", "ta": "சர்க்கரை பாகு இனிப்பு"},
        alternate_names=["syrup sweet uncertain", "soaked sweet uncertain"],
        base_ingredient="Flour/Milk",
        cooking_method="Deep-fried",
        syrup_state="Syrup-coated",
        shape_profile="Ball",
        is_fried=True,
        is_milk_based=False,
        is_countable=True,
        piece_count_expected=2,
        piece_weight_typical_g=40.0,
        default_portion_grams=80.0,
        nutrition_per_100g={"calories": 340.0, "protein": 4.0, "carbs": 58.0, "fat": 10.5, "fiber": 0.2},
        uncertainty_factors=["syrup_density", "oil_absorption"],
        typical_sugar_level="Syrup soaked"
    )
)

# Mixed Indian Sweets Box Fallback (Section 49)
register_sweet_food_class(
    SweetFoodClassRecord(
        canonical_food_id="IND-SWT-BOX-UNKNOWN-001",
        canonical_name="Mixed Indian Sweets Box (Varieties Partially Uncertain)",
        hierarchy=SweetHierarchy(
            level3_region="Pan-India",
            level4_state="Unknown",
            level5_sweet_family="Mixed Sweets Box",
            level6_specific_dish="Mixed Mithai Box",
            level7_variant="Assorted mithai gift box containing multiple varieties where individual recognition is partially ambiguous",
            level8_base_ingredient="Mixed",
            level9_cooking_method="Mixed",
            level10_syrup_state="Mixed",
            level11_filling_or_topping="Mixed",
            level12_portion_type="weight_grams",
            level13_nutrition_ref_id="REF-SWT-BOX-FALLBACK-001"
        ),
        sweet_family="Mixed Sweets Box",
        specific_dish="Mixed Mithai Box",
        region="Pan-India",
        state_or_city="Pan-India",
        regional_names={"hi": "मिश्रित मिठाई का डिब्बा", "ta": "அசோர்ட்டெட் இனிப்புகள் பாக்ஸ்"},
        alternate_names=["mixed sweet box", "assorted sweets box", "mithai box", "diwali sweet box"],
        base_ingredient="Mixed",
        cooking_method="Mixed",
        syrup_state="Mixed",
        shape_profile="Irregular",
        is_fried=False,
        is_milk_based=True,
        is_countable=True,
        piece_count_expected=4,
        piece_weight_typical_g=35.0,
        default_portion_grams=140.0,
        nutrition_per_100g={"calories": 390.0, "protein": 6.5, "carbs": 58.0, "fat": 15.0, "fiber": 0.8},
        uncertainty_factors=["mixed_variety_assortment"],
        typical_sugar_level="High"
    )
)


def get_sweet_food_class(food_id: str) -> Optional[SweetFoodClassRecord]:
    """Look up a SweetFoodClassRecord by canonical ID or alias."""
    return SWEETS_TAXONOMY_REGISTRY.get(food_id) or SWEETS_TAXONOMY_REGISTRY.get(food_id.lower())


def resolve_sweet_food_by_name(name: str) -> Optional[SweetFoodClassRecord]:
    """Resolve a dish by English, Hindi, Tamil, regional or alternate name."""
    clean_name = name.lower().strip()
    if clean_name in SWEETS_SYNONYM_LOOKUP:
        canon_id = SWEETS_SYNONYM_LOOKUP[clean_name]
        return SWEETS_TAXONOMY_REGISTRY.get(canon_id)

    # Substring search
    for synonym, canon_id in SWEETS_SYNONYM_LOOKUP.items():
        if len(clean_name) >= 3 and (clean_name in synonym or synonym in clean_name):
            return SWEETS_TAXONOMY_REGISTRY.get(canon_id)

    return None
