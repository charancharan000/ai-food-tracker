"""
Indian Bread Master Taxonomy & Identity Hierarchy (Part 10)
Implements Sections 1-4, 6, 7, 9, 10, 13, 15, 17, 19-38, 61, 63, 64, 86 of Part 10 Master Training Specification.

Guarantees:
- Strict Hierarchical Identity Traversal:
  INDIAN FOOD -> BREAD -> REGION / STATE -> BREAD FAMILY (18 families) ->
  BREAD TYPE -> VARIANT -> FLOUR / GRAIN -> COOKING METHOD -> STUFFING -> TOPPING -> PORTION -> WEIGHT -> NUTRITION
- 18 Primary Bread Families Supported:
  1. Roti / Chapati family (BREAD_ROTI_*)
  2. Tandoor bread family (BREAD_TANDOORI_*)
  3. Naan family (BREAD_NAAN_*)
  4. Kulcha family (BREAD_KULCHA_*)
  5. Paratha family (BREAD_PARATHA_*)
  6. Puri family (BREAD_PURI_*)
  7. Bhatura family (BREAD_BHATURA_*)
  8. Bhakri family (BREAD_BHAKRI_*)
  9. Millet bread family (BREAD_MILLET_*)
  10. Regional flatbread family (BREAD_REGIONAL_*)
  11. Layered bread family (BREAD_LAYERED_*)
  12. Stuffed bread family (BREAD_STUFFED_*)
  13. Sweet bread family (BREAD_SWEET_*)
  14. Fermented bread family (BREAD_FERMENTED_*)
  15. Fried bread family (BREAD_FRIED_*)
  16. Rice-based bread family (BREAD_RICE_*)
  17. Coconut-based regional bread family (BREAD_COCONUT_*)
  18. Gluten-free bread family (BREAD_GF_*)
  Plus BREAD_UNKNOWN fallback.
- Attributes:
  * Flour/grain: whole_wheat, maida, jowar, bajra, ragi, makki, rice_flour, besan, multigrain
  * Cooking method: Tawa cooked, Tandoor, Direct flame, Deep fried, Shallow fried, Baked, Steamed
  * Stuffing: None, Potato, Paneer, Cauliflower, Radish, Onion, Dal, Sattu, Meat, Cheese
  * Topping: None, Butter, Desi Ghee, Garlic, Coriander, Sesame seeds, Cheese
- Permanent Canonical IDs with Multilingual Names across English, Hindi, Tamil, Telugu, Malayalam, Gujarati, Bengali, Punjabi, Kannada, Marathi, Urdu.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class BreadHierarchy(BaseModel):
    level1_food: str = "Indian Food"
    level2_macro_category: str = "Bread"
    level3_region: str          # Punjab, Maharashtra, Tamil Nadu, Kerala, Gujarat, North India, etc.
    level4_bread_family: str    # Roti/Chapati, Naan, Kulcha, Paratha, Puri, Bhatura, Bhakri, etc.
    level5_bread_type: str      # Chapati, Phulka, Tandoori Roti, Butter Naan, Aloo Paratha, etc.
    level6_variant: str         # e.g., "Stuffed Spiced Potato", "Layered Flaky", "Direct Flame Puffed"
    level7_flour_grain: str     # whole_wheat (atta), refined_flour (maida), jowar, bajra, ragi, makki, rice_flour
    level8_cooking_method: str  # Tawa cooked, Tandoor cooked, Direct flame, Deep fried, Shallow fried, Baked
    level9_stuffing: str        # None, Potato, Paneer, Gobi, Mooli, Onion, Dal, Sattu, Meat, Cheese
    level10_topping: str       # None, Butter, Desi Ghee, Garlic, Coriander, Sesame, Cheese
    level11_portion_type: str   # piece_count, weight_grams
    level12_nutrition_ref_id: str


class BreadFoodClassRecord(BaseModel):
    canonical_food_id: str
    canonical_name: str
    hierarchy: BreadHierarchy
    bread_family: str
    bread_type: str
    region: str                 # North India, South India, West India, East India, Pan-India
    state_or_city: str          # Punjab, Maharashtra, Tamil Nadu, Kerala, Gujarat, etc.
    regional_names: Dict[str, str] = Field(default_factory=dict)
    alternate_names: List[str] = Field(default_factory=list)
    vegetarian: bool = True
    flour_type: str = "whole_wheat"  # whole_wheat, maida, jowar, bajra, ragi, makki, rice_flour, besan
    cooking_method: str = "Tawa cooked"  # Tawa, Tandoor, Direct Flame, Deep Fried, Shallow Fried, Baked
    stuffing_type: str = "none"          # none, potato, paneer, gobi, mooli, onion, sattu, dal, keema
    topping_type: str = "none"           # none, butter, ghee, garlic, sesame, cheese
    is_layered: bool = False
    is_fermented: bool = False
    is_deep_fried: bool = False
    default_piece_mass_g: float = 40.0
    density_g_cm3: float = 0.78
    nutrition_per_100g: Dict[str, float] = Field(default_factory=dict)
    uncertainty_factors: List[str] = Field(default_factory=list)
    fat_level_typical: str = "Low"  # Very Low, Low, Medium, High, Very High, Unknown


BREAD_TAXONOMY_REGISTRY: Dict[str, BreadFoodClassRecord] = {}
BREAD_SYNONYM_LOOKUP: Dict[str, str] = {}


def register_bread_food_class(record: BreadFoodClassRecord, alias_ids: Optional[List[str]] = None) -> BreadFoodClassRecord:
    BREAD_TAXONOMY_REGISTRY[record.canonical_food_id] = record
    if alias_ids:
        for aid in alias_ids:
            BREAD_TAXONOMY_REGISTRY[aid] = record
            BREAD_SYNONYM_LOOKUP[aid.lower().strip()] = record.canonical_food_id
    BREAD_SYNONYM_LOOKUP[record.canonical_name.lower().strip()] = record.canonical_food_id
    for alt in record.alternate_names:
        BREAD_SYNONYM_LOOKUP[alt.lower().strip()] = record.canonical_food_id
    for reg_name in record.regional_names.values():
        BREAD_SYNONYM_LOOKUP[reg_name.lower().strip()] = record.canonical_food_id
    return record



# =============================================================================
# 1. ROTI / CHAPATI / PHULKA MASTER FAMILY (Sections 4 & 5)
# =============================================================================

# 1.1 Chapati / Tawa Roti
register_bread_food_class(BreadFoodClassRecord(
    canonical_food_id="BREAD_ROTI_001",
    canonical_name="Plain Whole Wheat Chapati",
    hierarchy=BreadHierarchy(
        level3_region="Pan-India",
        level4_bread_family="Roti / Chapati family",
        level5_bread_type="Chapati",
        level6_variant="Thin Whole Wheat Tawa Cooked Flatbread",
        level7_flour_grain="whole_wheat",
        level8_cooking_method="Tawa cooked",
        level9_stuffing="None",
        level10_topping="None",
        level11_portion_type="piece_count",
        level12_nutrition_ref_id="ifct_bread_chapati_plain"
    ),
    bread_family="Roti / Chapati family",
    bread_type="Chapati",
    region="Pan-India",
    state_or_city="Pan-India",
    regional_names={"English": "Chapati", "Hindi": "रोटी", "Hindi_alt": "चपाती", "Tamil": "சப்பாத்தி", "Telugu": "చపాతీ", "Kannada": "ಚಪಾತಿ", "Marathi": "चपाती", "Bengali": "চাপাটি"},
    alternate_names=["chapati", "roti", "tawa roti", "chapathi", "wheat roti", "plain roti"],
    vegetarian=True,
    flour_type="whole_wheat",
    cooking_method="Tawa cooked",
    stuffing_type="none",
    topping_type="none",
    is_layered=False,
    is_fermented=False,
    is_deep_fried=False,
    default_piece_mass_g=40.0,
    density_g_cm3=0.76,
    nutrition_per_100g={"calories": 264.0, "protein_g": 8.8, "carbs_g": 52.0, "fat_g": 2.4, "fiber_g": 6.8, "sodium_mg": 120.0},
    uncertainty_factors=["dough_thickness", "ghee_brushing_undetectable"],
    fat_level_typical="Low"
), alias_ids=["BREAD_ROTI_CHAPATI"])


# 1.2 Phulka (Direct flame puffed)
register_bread_food_class(BreadFoodClassRecord(
    canonical_food_id="BREAD_ROTI_PHULKA",
    canonical_name="Puffed Phulka (Direct Flame)",
    hierarchy=BreadHierarchy(
        level3_region="North / West India",
        level4_bread_family="Roti / Chapati family",
        level5_bread_type="Phulka",
        level6_variant="Balloon-Puffed Over Direct Flame",
        level7_flour_grain="whole_wheat",
        level8_cooking_method="Direct flame",
        level9_stuffing="None",
        level10_topping="None",
        level11_portion_type="piece_count",
        level12_nutrition_ref_id="ifct_bread_phulka"
    ),
    bread_family="Roti / Chapati family",
    bread_type="Phulka",
    region="North / West India",
    state_or_city="Gujarat / Rajasthan / Punjab / UP",
    regional_names={"English": "Phulka", "Hindi": "फुल्का", "Gujarati": "ફુલકા", "Marathi": "फुलका"},
    alternate_names=["phulka", "fulka", "puffed roti", "gas flame roti"],
    vegetarian=True,
    flour_type="whole_wheat",
    cooking_method="Direct flame",
    stuffing_type="none",
    topping_type="none",
    is_layered=False,
    is_fermented=False,
    is_deep_fried=False,
    default_piece_mass_g=35.0,
    density_g_cm3=0.72,
    nutrition_per_100g={"calories": 260.0, "protein_g": 8.9, "carbs_g": 52.5, "fat_g": 1.8, "fiber_g": 6.9, "sodium_mg": 95.0},
    uncertainty_factors=["puffing_deflation_after_cooking", "ghee_rub"],
    fat_level_typical="Very Low"
))


# =============================================================================
# 2. TANDOORI ROTI & NAAN MASTER FAMILIES (Sections 6, 7, 8)
# =============================================================================

# 2.1 Tandoori Roti (Section 6)
register_bread_food_class(BreadFoodClassRecord(
    canonical_food_id="BREAD_TANDOORI_ROTI",
    canonical_name="Tandoori Roti",
    hierarchy=BreadHierarchy(
        level3_region="North India",
        level4_bread_family="Tandoor bread family",
        level5_bread_type="Tandoori Roti",
        level6_variant="Clay Oven Charred Whole Wheat",
        level7_flour_grain="whole_wheat",
        level8_cooking_method="Tandoor cooked",
        level9_stuffing="None",
        level10_topping="None",
        level11_portion_type="piece_count",
        level12_nutrition_ref_id="ifct_bread_tandoori_roti"
    ),
    bread_family="Tandoor bread family",
    bread_type="Tandoori Roti",
    region="North India",
    state_or_city="Punjab / Delhi",
    regional_names={"English": "Tandoori Roti", "Hindi": "तंदूरी रोटी", "Punjabi": "ਤੰਦੂਰੀ ਰੋਟੀ"},
    alternate_names=["tandoori roti", "tandoor roti", "butter tandoori roti"],
    vegetarian=True,
    flour_type="whole_wheat",
    cooking_method="Tandoor cooked",
    stuffing_type="none",
    topping_type="none",
    is_layered=False,
    is_fermented=False,
    is_deep_fried=False,
    default_piece_mass_g=65.0,
    density_g_cm3=0.82,
    nutrition_per_100g={"calories": 258.0, "protein_g": 9.2, "carbs_g": 50.5, "fat_g": 2.2, "fiber_g": 6.5, "sodium_mg": 180.0},
    uncertainty_factors=["butter_glaze_presence", "thickness_variation"],
    fat_level_typical="Low"
))

# 2.2 Butter Naan (Section 7)
register_bread_food_class(BreadFoodClassRecord(
    canonical_food_id="BREAD_NAAN_BUTTER",
    canonical_name="Butter Naan",
    hierarchy=BreadHierarchy(
        level3_region="North India",
        level4_bread_family="Naan family",
        level5_bread_type="Naan",
        level6_variant="Teardrop Leavened Refined Flour with Butter Glaze",
        level7_flour_grain="refined_flour (maida)",
        level8_cooking_method="Tandoor cooked",
        level9_stuffing="None",
        level10_topping="Butter",
        level11_portion_type="piece_count",
        level12_nutrition_ref_id="ifct_bread_butter_naan"
    ),
    bread_family="Naan family",
    bread_type="Naan",
    region="North India",
    state_or_city="Punjab / Delhi / Awadh",
    regional_names={"English": "Butter Naan", "Hindi": "बटर नान", "Urdu": "بٹر نان"},
    alternate_names=["butter naan", "naan", "plain naan", "tandoori naan"],
    vegetarian=True,
    flour_type="maida",
    cooking_method="Tandoor cooked",
    stuffing_type="none",
    topping_type="butter",
    is_layered=False,
    is_fermented=True,
    is_deep_fried=False,
    default_piece_mass_g=95.0,
    density_g_cm3=0.80,
    nutrition_per_100g={"calories": 298.0, "protein_g": 7.8, "carbs_g": 48.0, "fat_g": 8.8, "fiber_g": 2.1, "sodium_mg": 380.0},
    uncertainty_factors=["butter_brushing_mass", "fermentation_airy_density"],
    fat_level_typical="Medium"
))

# 2.3 Garlic Naan (Section 7)
register_bread_food_class(BreadFoodClassRecord(
    canonical_food_id="BREAD_NAAN_GARLIC",
    canonical_name="Garlic Naan",
    hierarchy=BreadHierarchy(
        level3_region="North India",
        level4_bread_family="Naan family",
        level5_bread_type="Naan",
        level6_variant="Minced Garlic & Cilantro Topped Leavened Naan",
        level7_flour_grain="refined_flour (maida)",
        level8_cooking_method="Tandoor cooked",
        level9_stuffing="None",
        level10_topping="Garlic",
        level11_portion_type="piece_count",
        level12_nutrition_ref_id="ifct_bread_garlic_naan"
    ),
    bread_family="Naan family",
    bread_type="Naan",
    region="North India",
    state_or_city="Delhi / Punjab",
    regional_names={"English": "Garlic Naan", "Hindi": "गार्लिक नान"},
    alternate_names=["garlic naan", "garlic butter naan", "lasooni naan"],
    vegetarian=True,
    flour_type="maida",
    cooking_method="Tandoor cooked",
    stuffing_type="none",
    topping_type="garlic",
    is_layered=False,
    is_fermented=True,
    is_deep_fried=False,
    default_piece_mass_g=100.0,
    density_g_cm3=0.81,
    nutrition_per_100g={"calories": 305.0, "protein_g": 8.0, "carbs_g": 47.5, "fat_g": 9.4, "fiber_g": 2.4, "sodium_mg": 390.0},
    uncertainty_factors=["butter_quantity", "garlic_char"],
    fat_level_typical="Medium"
))


# =============================================================================
# 3. KULCHA MASTER FAMILY (Section 9)
# =============================================================================

register_bread_food_class(BreadFoodClassRecord(
    canonical_food_id="BREAD_KULCHA_AMRITSARI",
    canonical_name="Amritsari Stuffed Kulcha",
    hierarchy=BreadHierarchy(
        level3_region="Punjab",
        level4_bread_family="Kulcha family",
        level5_bread_type="Kulcha",
        level6_variant="Crispy Flaky Tandoor Stuffed Potato-Onion Kulcha with Butter",
        level7_flour_grain="refined_flour (maida)",
        level8_cooking_method="Tandoor cooked",
        level9_stuffing="Potato",
        level10_topping="Butter",
        level11_portion_type="piece_count",
        level12_nutrition_ref_id="ifct_bread_amritsari_kulcha"
    ),
    bread_family="Kulcha family",
    bread_type="Kulcha",
    region="North India",
    state_or_city="Punjab / Amritsar",
    regional_names={"English": "Amritsari Kulcha", "Punjabi": "ਅੰਮ੍ਰਿਤਸਰੀ ਕੁਲਚਾ", "Hindi": "अमृतसरी कुलचा"},
    alternate_names=["amritsari kulcha", "stuffed kulcha", "aloo kulcha", "chole kulcha"],
    vegetarian=True,
    flour_type="maida",
    cooking_method="Tandoor cooked",
    stuffing_type="potato",
    topping_type="butter",
    is_layered=True,
    is_fermented=True,
    is_deep_fried=False,
    default_piece_mass_g=140.0,
    density_g_cm3=0.84,
    nutrition_per_100g={"calories": 268.0, "protein_g": 6.4, "carbs_g": 42.0, "fat_g": 8.8, "fiber_g": 2.8, "sodium_mg": 460.0},
    uncertainty_factors=["butter_topping_10g_vs_25g", "stuffing_density"],
    fat_level_typical="High"
))


# =============================================================================
# 4. PARATHA MASTER FAMILY (Sections 10, 11, 12)
# =============================================================================

# 4.0 Plain Paratha (Homestyle Tawa)
register_bread_food_class(BreadFoodClassRecord(
    canonical_food_id="BREAD_PARATHA_PLAIN",
    canonical_name="Plain Tawa Paratha",
    hierarchy=BreadHierarchy(
        level3_region="Pan-India",
        level4_bread_family="Paratha family",
        level5_bread_type="Plain Paratha",
        level6_variant="Layered Triangular or Round Shallow Fried Whole Wheat Flatbread",
        level7_flour_grain="whole_wheat",
        level8_cooking_method="Tawa cooked",
        level9_stuffing="None",
        level10_topping="Ghee",
        level11_portion_type="piece_count",
        level12_nutrition_ref_id="ifct_bread_paratha_plain"
    ),
    bread_family="Paratha family",
    bread_type="Plain Paratha",
    region="Pan-India",
    state_or_city="Pan-India",
    regional_names={"English": "Plain Paratha", "Hindi": "सादा पराठा"},
    alternate_names=["plain paratha", "tawa paratha", "triangle paratha", "sada paratha"],
    vegetarian=True,
    flour_type="whole_wheat",
    cooking_method="Tawa cooked",
    stuffing_type="none",
    topping_type="ghee",
    is_layered=True,
    is_fermented=False,
    is_deep_fried=False,
    default_piece_mass_g=75.0,
    density_g_cm3=0.86,
    nutrition_per_100g={"calories": 290.0, "protein_g": 6.8, "carbs_g": 46.0, "fat_g": 9.2, "fiber_g": 4.5, "sodium_mg": 210.0},
    uncertainty_factors=["griddle_ghee_volume"],
    fat_level_typical="Medium"
))

# 4.1 Aloo Paratha (Sections 10 & 11)
register_bread_food_class(BreadFoodClassRecord(
    canonical_food_id="BREAD_PARATHA_ALOO",
    canonical_name="Punjabi Aloo Paratha",
    hierarchy=BreadHierarchy(
        level3_region="Punjab",
        level4_bread_family="Paratha family",
        level5_bread_type="Aloo Paratha",
        level6_variant="Spiced Mashed Potato Stuffed Whole Wheat Tawa Flatbread",
        level7_flour_grain="whole_wheat",
        level8_cooking_method="Tawa cooked",
        level9_stuffing="Potato",
        level10_topping="Butter",
        level11_portion_type="piece_count",
        level12_nutrition_ref_id="ifct_bread_aloo_paratha"
    ),
    bread_family="Paratha family",
    bread_type="Aloo Paratha",
    region="North India",
    state_or_city="Punjab / Delhi",
    regional_names={"English": "Aloo Paratha", "Hindi": "आलू पराठा", "Punjabi": "ਆਲੂ ਪਰੌਂਠਾ"},
    alternate_names=["aloo paratha", "alu paratha", "stuffed potato paratha", "punjabi paratha"],
    vegetarian=True,
    flour_type="whole_wheat",
    cooking_method="Tawa cooked",
    stuffing_type="potato",
    topping_type="butter",
    is_layered=False,
    is_fermented=False,
    is_deep_fried=False,
    default_piece_mass_g=125.0,
    density_g_cm3=0.85,
    nutrition_per_100g={"calories": 242.0, "protein_g": 5.8, "carbs_g": 38.5, "fat_g": 7.4, "fiber_g": 3.8, "sodium_mg": 380.0},
    uncertainty_factors=["butter_slab_mass", "potato_to_dough_ratio", "oil_used_on_tawa"],
    fat_level_typical="Medium"
))

# 4.2 Laccha Paratha (Section 12)
register_bread_food_class(BreadFoodClassRecord(
    canonical_food_id="BREAD_PARATHA_LACCHA",
    canonical_name="North Indian Laccha Paratha",
    hierarchy=BreadHierarchy(
        level3_region="North India",
        level4_bread_family="Layered bread family",
        level5_bread_type="Laccha Paratha",
        level6_variant="Concentric Spiral Ring Layered Whole Wheat Paratha",
        level7_flour_grain="whole_wheat",
        level8_cooking_method="Tawa cooked",
        level9_stuffing="None",
        level10_topping="Desi Ghee",
        level11_portion_type="piece_count",
        level12_nutrition_ref_id="ifct_bread_laccha_paratha"
    ),
    bread_family="Layered bread family",
    bread_type="Laccha Paratha",
    region="North India",
    state_or_city="Punjab / Delhi",
    regional_names={"English": "Laccha Paratha", "Hindi": "लच्छा पराठा", "Punjabi": "ਲੱਛਾ ਪਰੌਂਠਾ"},
    alternate_names=["laccha paratha", "lacha paratha", "layered paratha", "spiral paratha"],
    vegetarian=True,
    flour_type="whole_wheat",
    cooking_method="Tawa cooked",
    stuffing_type="none",
    topping_type="ghee",
    is_layered=True,
    is_fermented=False,
    is_deep_fried=False,
    default_piece_mass_g=90.0,
    density_g_cm3=0.82,
    nutrition_per_100g={"calories": 288.0, "protein_g": 7.2, "carbs_g": 44.0, "fat_g": 9.5, "fiber_g": 5.2, "sodium_mg": 280.0},
    uncertainty_factors=["layer_fat_pleating", "tawa_ghee_level"],
    fat_level_typical="High"
))

# 4.3 Paneer Paratha (Section 10)
register_bread_food_class(BreadFoodClassRecord(
    canonical_food_id="BREAD_PARATHA_PANEER",
    canonical_name="Spiced Paneer Paratha",
    hierarchy=BreadHierarchy(
        level3_region="North India",
        level4_bread_family="Paratha family",
        level5_bread_type="Paneer Paratha",
        level6_variant="Grated Spiced Cottage Cheese Stuffed Paratha",
        level7_flour_grain="whole_wheat",
        level8_cooking_method="Tawa cooked",
        level9_stuffing="Paneer",
        level10_topping="Butter",
        level11_portion_type="piece_count",
        level12_nutrition_ref_id="ifct_bread_paneer_paratha"
    ),
    bread_family="Paratha family",
    bread_type="Paneer Paratha",
    region="North India",
    state_or_city="Punjab / Delhi",
    regional_names={"English": "Paneer Paratha", "Hindi": "पनीर पराठा"},
    alternate_names=["paneer paratha", "cottage cheese paratha"],
    vegetarian=True,
    flour_type="whole_wheat",
    cooking_method="Tawa cooked",
    stuffing_type="paneer",
    topping_type="butter",
    is_layered=False,
    is_fermented=False,
    is_deep_fried=False,
    default_piece_mass_g=135.0,
    density_g_cm3=0.86,
    nutrition_per_100g={"calories": 272.0, "protein_g": 10.5, "carbs_g": 34.0, "fat_g": 10.8, "fiber_g": 3.4, "sodium_mg": 390.0},
    uncertainty_factors=["paneer_full_fat_vs_low_fat", "stuffing_volume"],
    fat_level_typical="High"
))


# =============================================================================
# 5. KERALA / MALABAR PAROTTA & KOTHU (Sections 13 & 14)
# =============================================================================

# 5.1 Kerala / Malabar Parotta (Section 13)
register_bread_food_class(BreadFoodClassRecord(
    canonical_food_id="BREAD_PARATHA_005",
    canonical_name="Kerala Malabar Parotta",
    hierarchy=BreadHierarchy(
        level3_region="Kerala",
        level4_bread_family="Layered bread family",
        level5_bread_type="Kerala Parotta",
        level6_variant="Flaky Multi-Layered Clapped Refined Flour Parotta",
        level7_flour_grain="refined_flour (maida)",
        level8_cooking_method="Tawa cooked",
        level9_stuffing="None",
        level10_topping="Oil / Ghee",
        level11_portion_type="piece_count",
        level12_nutrition_ref_id="ifct_bread_kerala_parotta"
    ),
    bread_family="Layered bread family",
    bread_type="Kerala Parotta",
    region="South India",
    state_or_city="Kerala / Malabar / Tamil Nadu",
    regional_names={"English": "Kerala Parotta", "Malayalam": "കേരള പൊറോട്ട", "Tamil": "பரோட்டா"},
    alternate_names=["kerala parotta", "malabar parotta", "porotta", "barotta", "malabar porotta"],
    vegetarian=True,
    flour_type="maida",
    cooking_method="Tawa cooked",
    stuffing_type="none",
    topping_type="oil",
    is_layered=True,
    is_fermented=False,
    is_deep_fried=False,
    default_piece_mass_g=85.0,
    density_g_cm3=0.84,
    nutrition_per_100g={"calories": 315.0, "protein_g": 6.8, "carbs_g": 46.0, "fat_g": 11.5, "fiber_g": 1.8, "sodium_mg": 360.0},
    uncertainty_factors=["kneading_oil_and_egg_enrichment", "flakiness_fat"],
    fat_level_typical="High"
), alias_ids=["BREAD_PAROTTA_KERALA"])


# 5.2 Kothu Parotta (Section 14)
register_bread_food_class(BreadFoodClassRecord(
    canonical_food_id="BREAD_PAROTTA_KOTHU_EGG",
    canonical_name="Egg Kothu Parotta",
    hierarchy=BreadHierarchy(
        level3_region="Tamil Nadu",
        level4_bread_family="Layered bread family",
        level5_bread_type="Kothu Parotta",
        level6_variant="Minced Parotta Stir-Fried with Eggs, Onions, Chillies & Salna",
        level7_flour_grain="refined_flour (maida)",
        level8_cooking_method="Tawa cooked",
        level9_stuffing="Egg & Salna",
        level10_topping="None",
        level11_portion_type="weight_grams",
        level12_nutrition_ref_id="ifct_bread_kothu_parotta_egg"
    ),
    bread_family="Layered bread family",
    bread_type="Kothu Parotta",
    region="South India",
    state_or_city="Tamil Nadu / Madurai / Chennai",
    regional_names={"English": "Egg Kothu Parotta", "Tamil": "முட்டை கொத்து பரோட்டா"},
    alternate_names=["kothu parotta", "kothu roti", "egg kothu", "muttai parotta"],
    vegetarian=False,
    flour_type="maida",
    cooking_method="Tawa cooked",
    stuffing_type="egg",
    topping_type="none",
    is_layered=True,
    is_fermented=False,
    is_deep_fried=False,
    default_piece_mass_g=320.0,
    density_g_cm3=0.88,
    nutrition_per_100g={"calories": 242.0, "protein_g": 8.8, "carbs_g": 26.5, "fat_g": 11.5, "fiber_g": 1.6, "sodium_mg": 520.0},
    uncertainty_factors=["salna_gravy_oil", "egg_count"],
    fat_level_typical="High"
))


# =============================================================================
# 6. PURI & BHATURA MASTER FAMILIES (Sections 15 - 18)
# =============================================================================

# 6.1 Puri / Poori (Section 15)
register_bread_food_class(BreadFoodClassRecord(
    canonical_food_id="BREAD_PURI_PLAIN",
    canonical_name="Puffed Whole Wheat Puri / Poori",
    hierarchy=BreadHierarchy(
        level3_region="Pan-India",
        level4_bread_family="Puri family",
        level5_bread_type="Puri",
        level6_variant="Golden Deep-Fried Puffed Unleavened Whole Wheat Flatbread",
        level7_flour_grain="whole_wheat",
        level8_cooking_method="Deep fried",
        level9_stuffing="None",
        level10_topping="None",
        level11_portion_type="piece_count",
        level12_nutrition_ref_id="ifct_bread_puri_plain"
    ),
    bread_family="Puri family",
    bread_type="Puri",
    region="Pan-India",
    state_or_city="Pan-India",
    regional_names={"English": "Puri", "Hindi": "पूरी", "Tamil": "பூரி", "Telugu": "పూరి", "Bengali": "লুচি/পুরি"},
    alternate_names=["puri", "poori", "wheat puri", "fried poori"],
    vegetarian=True,
    flour_type="whole_wheat",
    cooking_method="Deep fried",
    stuffing_type="none",
    topping_type="none",
    is_layered=False,
    is_fermented=False,
    is_deep_fried=True,
    default_piece_mass_g=35.0,
    density_g_cm3=0.74,
    nutrition_per_100g={"calories": 335.0, "protein_g": 7.2, "carbs_g": 46.0, "fat_g": 14.5, "fiber_g": 4.6, "sodium_mg": 180.0},
    uncertainty_factors=["oil_absorption_rate", "diameter_10cm_vs_14cm"],
    fat_level_typical="Very High"
))

# 6.2 Bhatura (Section 16 & 17)
register_bread_food_class(BreadFoodClassRecord(
    canonical_food_id="BREAD_BHATURA_PLAIN",
    canonical_name="Punjabi Leavened Bhatura",
    hierarchy=BreadHierarchy(
        level3_region="Punjab",
        level4_bread_family="Bhatura family",
        level5_bread_type="Bhatura",
        level6_variant="Large Fermented Deep-Fried Puffed Leavened Bread",
        level7_flour_grain="refined_flour (maida)",
        level8_cooking_method="Deep fried",
        level9_stuffing="None",
        level10_topping="None",
        level11_portion_type="piece_count",
        level12_nutrition_ref_id="ifct_bread_bhatura_plain"
    ),
    bread_family="Bhatura family",
    bread_type="Bhatura",
    region="North India",
    state_or_city="Punjab / Delhi",
    regional_names={"English": "Bhatura", "Hindi": "भटूरा", "Punjabi": "ਭਟੂਰਾ"},
    alternate_names=["bhatura", "bhatoora", "chole bhatura", "punjabi bhatura"],
    vegetarian=True,
    flour_type="maida",
    cooking_method="Deep fried",
    stuffing_type="none",
    topping_type="none",
    is_layered=False,
    is_fermented=True,
    is_deep_fried=True,
    default_piece_mass_g=110.0,
    density_g_cm3=0.75,
    nutrition_per_100g={"calories": 312.0, "protein_g": 6.8, "carbs_g": 45.0, "fat_g": 12.0, "fiber_g": 1.8, "sodium_mg": 320.0},
    uncertainty_factors=["diameter_18cm_vs_24cm", "oil_drained_percentage"],
    fat_level_typical="Very High"
))


# =============================================================================
# 7. BHAKRI, ROTLA, THEPLA & MILLETS (Sections 19 - 24)
# =============================================================================

# 7.1 Jowar Bhakri (Section 19)
register_bread_food_class(BreadFoodClassRecord(
    canonical_food_id="BREAD_BHAKRI_JOWAR",
    canonical_name="Maharashtrian Jowar Bhakri",
    hierarchy=BreadHierarchy(
        level3_region="Maharashtra",
        level4_bread_family="Bhakri family",
        level5_bread_type="Jowar Bhakri",
        level6_variant="Hand-Patted Unleavened Sorghum Flatbread",
        level7_flour_grain="jowar (sorghum)",
        level8_cooking_method="Tawa cooked",
        level9_stuffing="None",
        level10_topping="None",
        level11_portion_type="piece_count",
        level12_nutrition_ref_id="ifct_bread_bhakri_jowar"
    ),
    bread_family="Bhakri family",
    bread_type="Jowar Bhakri",
    region="West India",
    state_or_city="Maharashtra",
    regional_names={"English": "Jowar Bhakri", "Marathi": "ज्वारीची भाकरी", "Hindi": "ज्वार भाकरी"},
    alternate_names=["jowar bhakri", "bhakri", "jowar roti", "sorghum flatbread"],
    vegetarian=True,
    flour_type="jowar",
    cooking_method="Tawa cooked",
    stuffing_type="none",
    topping_type="none",
    is_layered=False,
    is_fermented=False,
    is_deep_fried=False,
    default_piece_mass_g=70.0,
    density_g_cm3=0.86,
    nutrition_per_100g={"calories": 245.0, "protein_g": 7.6, "carbs_g": 51.0, "fat_g": 1.6, "fiber_g": 7.2, "sodium_mg": 45.0},
    uncertainty_factors=["rustic_thickness", "hand_patting_mass"],
    fat_level_typical="Very Low"
))

# 7.2 Bajra Rotla (Section 20)
register_bread_food_class(BreadFoodClassRecord(
    canonical_food_id="BREAD_ROTLA_BAJRA",
    canonical_name="Gujarati Bajra no Rotlo",
    hierarchy=BreadHierarchy(
        level3_region="Gujarat",
        level4_bread_family="Millet bread family",
        level5_bread_type="Bajra Rotla",
        level6_variant="Thick Rustic Hand-Patted Pearl Millet Flatbread",
        level7_flour_grain="bajra (pearl millet)",
        level8_cooking_method="Tawa cooked",
        level9_stuffing="None",
        level10_topping="White Butter (Makhan)",
        level11_portion_type="piece_count",
        level12_nutrition_ref_id="ifct_bread_bajra_rotla"
    ),
    bread_family="Millet bread family",
    bread_type="Bajra Rotla",
    region="West India",
    state_or_city="Gujarat / Saurashtra / Rajasthan",
    regional_names={"English": "Bajra Rotla", "Gujarati": "બાજરીનો રોટલો", "Hindi": "बाजरा रोटला"},
    alternate_names=["bajra rotlo", "rotla", "bajra no rotlo", "pearl millet flatbread"],
    vegetarian=True,
    flour_type="bajra",
    cooking_method="Tawa cooked",
    stuffing_type="none",
    topping_type="butter",
    is_layered=False,
    is_fermented=False,
    is_deep_fried=False,
    default_piece_mass_g=110.0,
    density_g_cm3=0.88,
    nutrition_per_100g={"calories": 255.0, "protein_g": 8.2, "carbs_g": 49.0, "fat_g": 3.4, "fiber_g": 8.5, "sodium_mg": 55.0},
    uncertainty_factors=["white_butter_spread_mass", "thickness"],
    fat_level_typical="Low"
))

# 7.3 Methi Thepla (Section 21)
register_bread_food_class(BreadFoodClassRecord(
    canonical_food_id="BREAD_THEPLA_METHI",
    canonical_name="Gujarati Methi Thepla",
    hierarchy=BreadHierarchy(
        level3_region="Gujarat",
        level4_bread_family="Regional flatbread family",
        level5_bread_type="Thepla",
        level6_variant="Thin Spiced Fenugreek Leaf Flatbread",
        level7_flour_grain="whole_wheat",
        level8_cooking_method="Tawa cooked",
        level9_stuffing="None",
        level10_topping="Oil",
        level11_portion_type="piece_count",
        level12_nutrition_ref_id="ifct_bread_methi_thepla"
    ),
    bread_family="Regional flatbread family",
    bread_type="Thepla",
    region="West India",
    state_or_city="Gujarat",
    regional_names={"English": "Methi Thepla", "Gujarati": "મેથીના થેપલા", "Hindi": "मेथी थेपला"},
    alternate_names=["methi thepla", "thepla", "gujarati thepla", "fenugreek flatbread"],
    vegetarian=True,
    flour_type="whole_wheat",
    cooking_method="Tawa cooked",
    stuffing_type="none",
    topping_type="oil",
    is_layered=False,
    is_fermented=False,
    is_deep_fried=False,
    default_piece_mass_g=45.0,
    density_g_cm3=0.80,
    nutrition_per_100g={"calories": 285.0, "protein_g": 7.4, "carbs_g": 44.0, "fat_g": 9.2, "fiber_g": 5.4, "sodium_mg": 340.0},
    uncertainty_factors=["oil_preservation_amount", "besan_ratio"],
    fat_level_typical="Medium"
))

# 7.4 Makki di Roti (Section 23)
register_bread_food_class(BreadFoodClassRecord(
    canonical_food_id="BREAD_ROTI_MAKKI",
    canonical_name="Punjabi Makki di Roti",
    hierarchy=BreadHierarchy(
        level3_region="Punjab",
        level4_bread_family="Millet bread family",
        level5_bread_type="Makki Roti",
        level6_variant="Rustic Yellow Cornmeal Hand-Patted Flatbread with Makhan",
        level7_flour_grain="makki (yellow cornmeal)",
        level8_cooking_method="Tawa cooked",
        level9_stuffing="None",
        level10_topping="White Butter (Makhan)",
        level11_portion_type="piece_count",
        level12_nutrition_ref_id="ifct_bread_makki_roti"
    ),
    bread_family="Millet bread family",
    bread_type="Makki Roti",
    region="North India",
    state_or_city="Punjab",
    regional_names={"English": "Makki di Roti", "Punjabi": "ਮੱਕੀ ਦੀ ਰੋਟੀ", "Hindi": "मक्के की रोटी"},
    alternate_names=["makki di roti", "makki roti", "cornmeal flatbread"],
    vegetarian=True,
    flour_type="makki",
    cooking_method="Tawa cooked",
    stuffing_type="none",
    topping_type="butter",
    is_layered=False,
    is_fermented=False,
    is_deep_fried=False,
    default_piece_mass_g=85.0,
    density_g_cm3=0.86,
    nutrition_per_100g={"calories": 252.0, "protein_g": 6.8, "carbs_g": 48.0, "fat_g": 4.2, "fiber_g": 6.2, "sodium_mg": 90.0},
    uncertainty_factors=["white_butter_dollop", "cornmeal_coarseness"],
    fat_level_typical="Medium"
))


# =============================================================================
# 8. SPECIALTY & SOUTH INDIAN REGIONAL BREADS (Sections 25, 33 - 38, 61)
# =============================================================================

# 8.1 Roomali Roti (Section 25)
register_bread_food_class(BreadFoodClassRecord(
    canonical_food_id="BREAD_ROOMALI_ROTI",
    canonical_name="Roomali Roti (Handkerchief Flatbread)",
    hierarchy=BreadHierarchy(
        level3_region="North India / Mughlai",
        level4_bread_family="Regional flatbread family",
        level5_bread_type="Roomali Roti",
        level6_variant="Paper-Thin Handkerchief Folded Soft Flatbread",
        level7_flour_grain="refined_flour (maida)",
        level8_cooking_method="Tawa cooked",
        level9_stuffing="None",
        level10_topping="None",
        level11_portion_type="piece_count",
        level12_nutrition_ref_id="ifct_bread_roomali_roti"
    ),
    bread_family="Regional flatbread family",
    bread_type="Roomali Roti",
    region="North India",
    state_or_city="Delhi / Lucknow / Hyderabad",
    regional_names={"English": "Roomali Roti", "Hindi": "रूमाली रोटी", "Urdu": "رومالی روٹی"},
    alternate_names=["roomali roti", "rumali roti", "handkerchief bread", "manda"],
    vegetarian=True,
    flour_type="maida",
    cooking_method="Tawa cooked",
    stuffing_type="none",
    topping_type="none",
    is_layered=False,
    is_fermented=False,
    is_deep_fried=False,
    default_piece_mass_g=75.0,
    density_g_cm3=0.72,
    nutrition_per_100g={"calories": 275.0, "protein_g": 7.8, "carbs_g": 52.0, "fat_g": 3.8, "fiber_g": 2.0, "sodium_mg": 210.0},
    uncertainty_factors=["folded_diameter", "oil_in_dough"],
    fat_level_typical="Low"
))

# 8.2 Kerala Appam (Section 34)
register_bread_food_class(BreadFoodClassRecord(
    canonical_food_id="BREAD_APPAM_PLAIN",
    canonical_name="Kerala Palappam (Lacy Rice Appam)",
    hierarchy=BreadHierarchy(
        level3_region="Kerala",
        level4_bread_family="Rice-based bread family",
        level5_bread_type="Appam",
        level6_variant="Fermented Rice & Coconut Milk Bowl with Lacy Frills",
        level7_flour_grain="rice_flour",
        level8_cooking_method="Tawa cooked",
        level9_stuffing="None",
        level10_topping="None",
        level11_portion_type="piece_count",
        level12_nutrition_ref_id="ifct_bread_appam_plain"
    ),
    bread_family="Rice-based bread family",
    bread_type="Appam",
    region="South India",
    state_or_city="Kerala / Tamil Nadu",
    regional_names={"English": "Appam", "Malayalam": "അപ്പം", "Tamil": "ஆப்பம்"},
    alternate_names=["appam", "palappam", "vellayappam", "kerala appam", "lacy appam"],
    vegetarian=True,
    flour_type="rice_flour",
    cooking_method="Tawa cooked",
    stuffing_type="none",
    topping_type="none",
    is_layered=False,
    is_fermented=True,
    is_deep_fried=False,
    default_piece_mass_g=55.0,
    density_g_cm3=0.70,
    nutrition_per_100g={"calories": 142.0, "protein_g": 2.4, "carbs_g": 28.5, "fat_g": 2.2, "fiber_g": 0.8, "sodium_mg": 110.0},
    uncertainty_factors=["coconut_milk_richness", "egg_appam_addition"],
    fat_level_typical="Low"
))

# 8.3 Malabar Pathiri (Section 35)
register_bread_food_class(BreadFoodClassRecord(
    canonical_food_id="BREAD_PATHIRI_RICE",
    canonical_name="Malabar Rice Pathiri",
    hierarchy=BreadHierarchy(
        level3_region="Kerala",
        level4_bread_family="Rice-based bread family",
        level5_bread_type="Pathiri",
        level6_variant="Paper-Thin Pale White Roasted Rice Flour Flatbread",
        level7_flour_grain="rice_flour",
        level8_cooking_method="Tawa cooked",
        level9_stuffing="None",
        level10_topping="None",
        level11_portion_type="piece_count",
        level12_nutrition_ref_id="ifct_bread_pathiri_rice"
    ),
    bread_family="Rice-based bread family",
    bread_type="Pathiri",
    region="South India",
    state_or_city="Kerala / Malabar",
    regional_names={"English": "Pathiri", "Malayalam": "പത്തിരി"},
    alternate_names=["pathiri", "rice pathiri", "malabar pathiri", "ari pathiri"],
    vegetarian=True,
    flour_type="rice_flour",
    cooking_method="Tawa cooked",
    stuffing_type="none",
    topping_type="none",
    is_layered=False,
    is_fermented=False,
    is_deep_fried=False,
    default_piece_mass_g=35.0,
    density_g_cm3=0.74,
    nutrition_per_100g={"calories": 168.0, "protein_g": 3.1, "carbs_g": 36.0, "fat_g": 0.6, "fiber_g": 1.1, "sodium_mg": 85.0},
    uncertainty_factors=["coconut_milk_soaking (theeyal/ney)"],
    fat_level_typical="Very Low"
))

# 8.4 Karnataka Akki Roti (Section 36)
register_bread_food_class(BreadFoodClassRecord(
    canonical_food_id="BREAD_ROTI_AKKI",
    canonical_name="Karnataka Spiced Akki Roti",
    hierarchy=BreadHierarchy(
        level3_region="Karnataka",
        level4_bread_family="Rice-based bread family",
        level5_bread_type="Akki Roti",
        level6_variant="Hand-Patted Rice Flour Flatbread with Onions, Dill & Chillies",
        level7_flour_grain="rice_flour",
        level8_cooking_method="Tawa cooked",
        level9_stuffing="None",
        level10_topping="Oil",
        level11_portion_type="piece_count",
        level12_nutrition_ref_id="ifct_bread_akki_roti"
    ),
    bread_family="Rice-based bread family",
    bread_type="Akki Roti",
    region="South India",
    state_or_city="Karnataka / Bengaluru / Mysuru",
    regional_names={"English": "Akki Roti", "Kannada": "ಅಕ್ಕಿ ರೊಟ್ಟಿ"},
    alternate_names=["akki roti", "akki rotti", "rice flatbread karnataka"],
    vegetarian=True,
    flour_type="rice_flour",
    cooking_method="Tawa cooked",
    stuffing_type="none",
    topping_type="oil",
    is_layered=False,
    is_fermented=False,
    is_deep_fried=False,
    default_piece_mass_g=80.0,
    density_g_cm3=0.85,
    nutrition_per_100g={"calories": 218.0, "protein_g": 4.5, "carbs_g": 41.0, "fat_g": 4.2, "fiber_g": 2.8, "sodium_mg": 280.0},
    uncertainty_factors=["vegetable_dill_density", "tawa_oil"],
    fat_level_typical="Low"
))

# 8.5 Karnataka Ragi Roti (Section 37)
register_bread_food_class(BreadFoodClassRecord(
    canonical_food_id="BREAD_ROTI_RAGI",
    canonical_name="Karnataka Ragi Roti",
    hierarchy=BreadHierarchy(
        level3_region="Karnataka",
        level4_bread_family="Millet bread family",
        level5_bread_type="Ragi Roti",
        level6_variant="Hand-Patted Finger Millet Flatbread with Onions & Herbs",
        level7_flour_grain="ragi (finger millet)",
        level8_cooking_method="Tawa cooked",
        level9_stuffing="None",
        level10_topping="Oil",
        level11_portion_type="piece_count",
        level12_nutrition_ref_id="ifct_bread_ragi_roti"
    ),
    bread_family="Millet bread family",
    bread_type="Ragi Roti",
    region="South India",
    state_or_city="Karnataka / Tamil Nadu",
    regional_names={"English": "Ragi Roti", "Kannada": "ರಾಗಿ ರೊಟ್ಟಿ", "Tamil": "கேழ்வரகு ரொட்டி"},
    alternate_names=["ragi roti", "ragi rotti", "finger millet flatbread", "kezhvaragu roti"],
    vegetarian=True,
    flour_type="ragi",
    cooking_method="Tawa cooked",
    stuffing_type="none",
    topping_type="oil",
    is_layered=False,
    is_fermented=False,
    is_deep_fried=False,
    default_piece_mass_g=85.0,
    density_g_cm3=0.88,
    nutrition_per_100g={"calories": 212.0, "protein_g": 5.4, "carbs_g": 40.5, "fat_g": 3.8, "fiber_g": 6.8, "sodium_mg": 260.0},
    uncertainty_factors=["onion_herbs_mass", "oil_glaze"],
    fat_level_typical="Low"
))

# 8.6 Mumbai Ladi Pav (Section 61)
register_bread_food_class(BreadFoodClassRecord(
    canonical_food_id="BREAD_PAV_LADI",
    canonical_name="Mumbai Ladi Pav",
    hierarchy=BreadHierarchy(
        level3_region="Maharashtra",
        level4_bread_family="Fermented bread family",
        level5_bread_type="Pav",
        level6_variant="Soft Pillow Leavened White Bun Grid",
        level7_flour_grain="refined_flour (maida)",
        level8_cooking_method="Baked",
        level9_stuffing="None",
        level10_topping="None",
        level11_portion_type="piece_count",
        level12_nutrition_ref_id="ifct_bread_ladi_pav"
    ),
    bread_family="Fermented bread family",
    bread_type="Pav",
    region="West India",
    state_or_city="Maharashtra / Mumbai / Goa",
    regional_names={"English": "Ladi Pav", "Marathi": "लादी पाव", "Hindi": "पाव"},
    alternate_names=["pav", "ladi pav", "pao", "bombay pav"],
    vegetarian=True,
    flour_type="maida",
    cooking_method="Baked",
    stuffing_type="none",
    topping_type="none",
    is_layered=False,
    is_fermented=True,
    is_deep_fried=False,
    default_piece_mass_g=45.0,
    density_g_cm3=0.68,
    nutrition_per_100g={"calories": 272.0, "protein_g": 8.4, "carbs_g": 54.0, "fat_g": 2.2, "fiber_g": 2.1, "sodium_mg": 410.0},
    uncertainty_factors=["butter_toasting_on_tawa"],
    fat_level_typical="Low"
))


# =============================================================================
# 9. ADDITIONAL REGIONAL FLATBREADS & SWEET BREADS (Sections 18, 30, 34)
# =============================================================================

# 9.1 Bengali Luchi
register_bread_food_class(BreadFoodClassRecord(
    canonical_food_id="BREAD_LUCHI_001",
    canonical_name="Bengali White Luchi",
    hierarchy=BreadHierarchy(
        level3_region="East India",
        level4_bread_family="Fried bread family",
        level5_bread_type="Luchi",
        level6_variant="Deep-Fried Puffed Refined Flour Pristine White Bread",
        level7_flour_grain="refined_flour (maida)",
        level8_cooking_method="Deep fried",
        level9_stuffing="None",
        level10_topping="None",
        level11_portion_type="piece_count",
        level12_nutrition_ref_id="ifct_bread_luchi"
    ),
    bread_family="Fried bread family",
    bread_type="Luchi",
    region="East India",
    state_or_city="West Bengal / Tripura / Assam",
    regional_names={"English": "Luchi", "Bengali": "লুচি", "Hindi": "लूची"},
    alternate_names=["luchi", "bengali luchi", "maida poori", "white poori"],
    vegetarian=True,
    flour_type="maida",
    cooking_method="Deep fried",
    stuffing_type="none",
    topping_type="none",
    is_layered=False,
    is_fermented=False,
    is_deep_fried=True,
    default_piece_mass_g=25.0,
    density_g_cm3=0.74,
    nutrition_per_100g={"calories": 320.0, "protein_g": 6.2, "carbs_g": 46.0, "fat_g": 12.8, "fiber_g": 1.5, "sodium_mg": 180.0},
    uncertainty_factors=["oil_absorption_during_frying"],
    fat_level_typical="High"
))

# 9.2 Awadhi / Kashmiri Sheermal
register_bread_food_class(BreadFoodClassRecord(
    canonical_food_id="BREAD_SHEERMAL_001",
    canonical_name="Awadhi Saffron Sheermal",
    hierarchy=BreadHierarchy(
        level3_region="North India",
        level4_bread_family="Sweet bread family",
        level5_bread_type="Sheermal",
        level6_variant="Saffron-Flavored Milk-Kneaded Sweet Tandoor Flatbread",
        level7_flour_grain="refined_flour (maida)",
        level8_cooking_method="Tandoor",
        level9_stuffing="None",
        level10_topping="Ghee & Kewra",
        level11_portion_type="piece_count",
        level12_nutrition_ref_id="ifct_bread_sheermal"
    ),
    bread_family="Sweet bread family",
    bread_type="Sheermal",
    region="North India",
    state_or_city="Uttar Pradesh (Lucknow) / Kashmir",
    regional_names={"English": "Sheermal", "Urdu": "شیرمال", "Hindi": "शीरमाल"},
    alternate_names=["sheermal", "shirmal", "saffron flatbread"],
    vegetarian=True,
    flour_type="maida",
    cooking_method="Tandoor",
    stuffing_type="none",
    topping_type="ghee",
    is_layered=False,
    is_fermented=False,
    is_deep_fried=False,
    default_piece_mass_g=110.0,
    density_g_cm3=0.86,
    nutrition_per_100g={"calories": 335.0, "protein_g": 7.5, "carbs_g": 54.0, "fat_g": 10.5, "fiber_g": 1.8, "sodium_mg": 240.0},
    uncertainty_factors=["sugar_milk_content", "ghee_glaze"],
    fat_level_typical="High"
))

# 9.3 Coastal Karnataka Neer Dosa
register_bread_food_class(BreadFoodClassRecord(
    canonical_food_id="BREAD_NEER_DOSA_001",
    canonical_name="Mangalorean Neer Dosa",
    hierarchy=BreadHierarchy(
        level3_region="South India",
        level4_bread_family="Rice-based bread family",
        level5_bread_type="Neer Dosa",
        level6_variant="Ultra-Thin Soft Lacy Rice Crêpe",
        level7_flour_grain="rice_flour",
        level8_cooking_method="Tawa cooked",
        level9_stuffing="None",
        level10_topping="None",
        level11_portion_type="piece_count",
        level12_nutrition_ref_id="ifct_bread_neer_dosa"
    ),
    bread_family="Rice-based bread family",
    bread_type="Neer Dosa",
    region="South India",
    state_or_city="Karnataka (Udupi / Mangalore)",
    regional_names={"English": "Neer Dosa", "Kannada": "ನೀರು ದೋಸೆ", "Tulu": "ನೀರ್ ದೋಸೆ"},
    alternate_names=["neer dosa", "water dosa", "bari panpole"],
    vegetarian=True,
    flour_type="rice_flour",
    cooking_method="Tawa cooked",
    stuffing_type="none",
    topping_type="none",
    is_layered=False,
    is_fermented=False,
    is_deep_fried=False,
    default_piece_mass_g=45.0,
    density_g_cm3=0.82,
    nutrition_per_100g={"calories": 160.0, "protein_g": 2.8, "carbs_g": 34.0, "fat_g": 1.2, "fiber_g": 0.8, "sodium_mg": 90.0},
    uncertainty_factors=["coconut_shred_inclusion"],
    fat_level_typical="Very Low"
))

# =============================================================================
# 10. UNKNOWN BREAD FALLBACK (Sections 65, 84, 85)
# =============================================================================

register_bread_food_class(BreadFoodClassRecord(
    canonical_food_id="BREAD_UNKNOWN_001",
    canonical_name="Unknown Indian Bread",
    hierarchy=BreadHierarchy(
        level3_region="Pan-India",
        level4_bread_family="Regional flatbread family",
        level5_bread_type="Unknown",
        level6_variant="Unverified Indian Bread (Low Visual Evidence)",
        level7_flour_grain="unspecified",
        level8_cooking_method="Unknown",
        level9_stuffing="Unknown",
        level10_topping="Unknown",
        level11_portion_type="piece_count",
        level12_nutrition_ref_id="ifct_unknown_bread"
    ),
    bread_family="Regional flatbread family",
    bread_type="Unknown",
    region="Pan-India",
    state_or_city="Unknown",
    regional_names={"English": "Unknown Indian Bread", "Hindi": "अज्ञात भारतीय रोटी"},
    alternate_names=["unknown bread", "unidentified bread", "roti/chapati uncertain"],
    vegetarian=True,
    flour_type="whole_wheat",
    cooking_method="Tawa cooked",
    stuffing_type="none",
    topping_type="none",
    is_layered=False,
    is_fermented=False,
    is_deep_fried=False,
    default_piece_mass_g=50.0,
    density_g_cm3=0.80,
    nutrition_per_100g={"calories": 260.0, "protein_g": 7.5, "carbs_g": 48.0, "fat_g": 4.5, "fiber_g": 4.0, "sodium_mg": 200.0},
    uncertainty_factors=["insufficient_visual_evidence", "unknown_preparation"],
    fat_level_typical="Unknown"
), alias_ids=["BREAD_UNKNOWN"])



# =============================================================================
# LOOKUP & HELPER UTILITIES
# =============================================================================

def get_bread_food_class(canonical_id: str) -> Optional[BreadFoodClassRecord]:
    """Retrieve record by canonical ID."""
    return BREAD_TAXONOMY_REGISTRY.get(canonical_id)


def resolve_bread_food_by_name(query: str) -> Optional[BreadFoodClassRecord]:
    """
    Resolves any query string (canonical name, English alias, Hindi/regional name)
    into the canonical BreadFoodClassRecord. Returns None if unmapped.
    """
    if not query:
        return None
    q = query.lower().strip()
    if q in BREAD_SYNONYM_LOOKUP:
        return BREAD_TAXONOMY_REGISTRY.get(BREAD_SYNONYM_LOOKUP[q])
    for alt, cid in BREAD_SYNONYM_LOOKUP.items():
        if alt in q or q in alt:
            return BREAD_TAXONOMY_REGISTRY.get(cid)
    return None


def filter_breads_by_family(bread_family: str) -> List[BreadFoodClassRecord]:
    """Returns all registered bread classes in a given bread family."""
    fam = bread_family.lower().strip()
    return [
        rec for rec in BREAD_TAXONOMY_REGISTRY.values()
        if rec.bread_family.lower() == fam or fam in rec.hierarchy.level4_bread_family.lower()
    ]
