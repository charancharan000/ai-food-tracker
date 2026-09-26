"""
East Indian Master Food Taxonomy & Identity Hierarchy (Part 6)
Implements Sections 1-32, 36, 48, 54, 62 of Part 6 Training Specification.

Guarantees:
- Strict 9-Level Taxonomy:
  INDIAN FOOD -> EAST INDIAN FOOD -> STATE -> REGION -> CUISINE ->
  FOOD FAMILY -> FOOD TYPE -> FOOD VARIANT -> COOKING METHOD -> PORTION -> NUTRITION
- Primary States/Regions Covered:
  1. West Bengal (Kolkata, Rarh, North Bengal) - Bengali Cuisine
  2. Odisha (Coastal Odisha, Temple/Puri, Western Odisha) - Odia Cuisine
  3. Bihar (Mithila, Magadh, Bhojpuri/Champaran) - Bihari Cuisine
  4. Jharkhand (Chota Nagpur, Santhal Parganas, Tribal Regions) - Jharkhandi Cuisine
- Permanent Canonical IDs: WB_*, OD_*, BR_*, JH_*, EI_*
- Multilingual Name Mapping (English, Bengali বাংলা, Odia ଓଡ଼ିଆ, Hindi/Bhojpuri/Maithili हिन्दी/भोजपुरी/मैथिली)
- Comprehensive coverage across Rice, Fish/Seafood, Mustard Fish, Meat, Vegetarian,
  Dal, Breakfast, Street Food, Kathi Rolls, Jhalmuri, Sweets, Mishti Doi, Sandesh,
  Pitha, Dalma, Pakhala, Litti Chokha, Sattu, Champaran Mutton, Dhuska, Wild Saag,
  Temple/Mahaprasad preparations, and Thali platters.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class EastIndianHierarchy(BaseModel):
    level1_food: str = "Indian Food"
    level2_macro_region: str = "East Indian Food"
    level3_state: str # West Bengal, Odisha, Bihar, Jharkhand
    level4_region: str # e.g. Kolkata, Coastal Odisha, Mithila, Chota Nagpur
    level5_cuisine: str # Bengali, Odia, Bihari, Jharkhandi
    level6_food_family: str # Rice, Fish/Seafood, Meat, Vegetarian, Dal, Breakfast, Street Food, Sweets, Pitha, Thali, Beverages
    level7_food_type: str # e.g. Macher Jhol, Posto, Pakhala, Dalma, Litti, Dhuska
    level8_variant: str # e.g. Shorshe Ilish, Aloo Posto, Dahi Pakhala, Champaran Mutton
    level9_cooking_method: List[str] # steamed, shallow_fried, deep_fried, mustard_gravy, jhol, slow_cooked, baked_pot, fermented
    default_portion: str # e.g. "1 plate (200g)", "1 piece (100g)", "1 bowl (180g)"
    nutrition_ref_id: str

class EastIndianFoodClass(BaseModel):
    canonical_food_id: str # Stable permanent ID: WB_*, OD_*, BR_*, JH_*, EI_*
    canonical_name: str
    hierarchy: EastIndianHierarchy
    state: str
    region: str
    cuisine: str
    food_category: str
    regional_names: Dict[str, str] = Field(default_factory=dict)
    alternate_names: List[str] = Field(default_factory=list)
    vegetarian: bool = True
    gravy_type: Optional[str] = Field(
        default=None,
        description="dry, semi_gravy, jhol_thin_broth, mustard_gravy, coconut_gravy, dal_stew, curd_broth, syrup"
    )
    visual_features: Dict[str, Any] = Field(default_factory=dict)
    key_ingredients: List[str] = Field(default_factory=list)
    possible_ingredients: List[str] = Field(default_factory=list)
    fish_species: Optional[str] = None # When applicable: Rohu, Catla, Hilsa, Bhetki, Pabda, Koi, Tangra, Pomfret, Prawn, Crab
    hard_negatives: List[str] = Field(default_factory=list)
    density_g_cm3: float = 0.85
    default_serving_weight_g: float = 150.0
    nutrition_per_100g: Dict[str, float] = Field(default_factory=dict)

# Master East Indian Registry
EAST_INDIAN_TAXONOMY_REGISTRY: Dict[str, EastIndianFoodClass] = {}
EAST_INDIAN_SYNONYM_MAP: Dict[str, str] = {}

def register_east_food(food: EastIndianFoodClass):
    EAST_INDIAN_TAXONOMY_REGISTRY[food.canonical_food_id] = food
    EAST_INDIAN_SYNONYM_MAP[food.canonical_name.lower().strip()] = food.canonical_food_id
    for alt in food.alternate_names:
        EAST_INDIAN_SYNONYM_MAP[alt.lower().strip()] = food.canonical_food_id
    for reg_name in food.regional_names.values():
        EAST_INDIAN_SYNONYM_MAP[reg_name.lower().strip()] = food.canonical_food_id

def get_east_food_class(canonical_id: str) -> Optional[EastIndianFoodClass]:
    return EAST_INDIAN_TAXONOMY_REGISTRY.get(canonical_id)

def resolve_east_food_by_name(query: str) -> Optional[EastIndianFoodClass]:
    if not query:
        return None
    q = query.lower().strip()
    if q in EAST_INDIAN_SYNONYM_MAP:
        return EAST_INDIAN_TAXONOMY_REGISTRY[EAST_INDIAN_SYNONYM_MAP[q]]
    for cid, food in EAST_INDIAN_TAXONOMY_REGISTRY.items():
        if q == cid.lower() or q in food.canonical_name.lower():
            return food
        for alt in food.alternate_names:
            if q in alt.lower():
                return food
        for reg in food.regional_names.values():
            if q in reg.lower():
                return food
    return None

def list_all_east_food_ids() -> List[str]:
    return list(EAST_INDIAN_TAXONOMY_REGISTRY.keys())

# =============================================================================
# 1. WEST BENGAL: RICE DISHES (Section 2)
# =============================================================================

register_east_food(EastIndianFoodClass(
    canonical_food_id="WB_RICE_PLAIN",
    canonical_name="Plain Steamed Rice",
    state="West Bengal",
    region="Kolkata",
    cuisine="Bengali",
    food_category="Rice",
    regional_names={"English": "Plain Boiled Rice", "Bengali": "ভাত (Sada Bhat)", "Hindi": "चावल"},
    alternate_names=["sada bhat", "bengali plain rice", "boiled rice"],
    vegetarian=True,
    gravy_type=None,
    visual_features={"grain": "slender_separated_white_grains", "sheen": "matte_steam"},
    key_ingredients=["rice", "water"],
    density_g_cm3=0.82,
    default_serving_weight_g=200.0,
    nutrition_per_100g={"calories": 130.0, "protein_g": 2.7, "carbs_g": 28.2, "fat_g": 0.3, "fiber_g": 0.4, "sodium_mg": 2.0},
    hierarchy=EastIndianHierarchy(
        level3_state="West Bengal", level4_region="Kolkata", level5_cuisine="Bengali",
        level6_food_family="Rice", level7_food_type="Steamed Rice", level8_variant="Sada Bhat",
        level9_cooking_method=["boiled", "steamed"], default_portion="1 bowl (200g)",
        nutrition_ref_id="wb_rice_plain"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="WB_RICE_GOBINDOBHOG",
    canonical_name="Gobindobhog Rice",
    state="West Bengal",
    region="Rarh Bengal",
    cuisine="Bengali",
    food_category="Rice",
    regional_names={"English": "Aromatic Short-Grain Gobindobhog Rice", "Bengali": "গোবিন্দভোগ চালের ভাত", "Hindi": "गोबिंदोभोग चावल"},
    alternate_names=["gobindobhog bhat", "ghee gobindobhog"],
    vegetarian=True,
    gravy_type=None,
    visual_features={"grain": "short_oval_aromatic_pearl_grains", "sheen": "slight_ghee_gloss"},
    key_ingredients=["gobindobhog rice", "water", "ghee"],
    density_g_cm3=0.85,
    default_serving_weight_g=180.0,
    nutrition_per_100g={"calories": 145.0, "protein_g": 2.9, "carbs_g": 29.5, "fat_g": 1.5, "fiber_g": 0.6, "sodium_mg": 5.0},
    hierarchy=EastIndianHierarchy(
        level3_state="West Bengal", level4_region="Rarh Bengal", level5_cuisine="Bengali",
        level6_food_family="Rice", level7_food_type="Aromatic Rice", level8_variant="Gobindobhog",
        level9_cooking_method=["steamed", "boiled"], default_portion="1 bowl (180g)",
        nutrition_ref_id="wb_rice_gobindobhog"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="WB_RICE_BASANTI_PULAO",
    canonical_name="Basanti Pulao",
    state="West Bengal",
    region="Kolkata",
    cuisine="Bengali",
    food_category="Rice",
    regional_names={"English": "Bengali Fragrant Sweet Yellow Pulao", "Bengali": "বাসন্তী পোলাও", "Hindi": "बासंती पुलाव"},
    alternate_names=["mishti pulao", "bengali sweet pulao", "holud pulao"],
    vegetarian=True,
    gravy_type=None,
    visual_features={"grain": "golden_yellow_fragrant_gobindobhog", "garnishes": ["fried_cashews", "golden_raisins", "whole_cinnamon", "cardamom", "cloves"], "sheen": "ghee_glaze"},
    key_ingredients=["gobindobhog rice", "ghee", "saffron or turmeric", "sugar", "cashews", "raisins", "cinnamon", "cardamom", "cloves", "ginger paste"],
    hard_negatives=["WB_RICE_PLAIN", "WB_RICE_FRIED_RICE", "OD_RICE_KANIKA"],
    density_g_cm3=0.88,
    default_serving_weight_g=220.0,
    nutrition_per_100g={"calories": 210.0, "protein_g": 3.6, "carbs_g": 36.5, "fat_g": 5.8, "fiber_g": 1.1, "sodium_mg": 45.0},
    hierarchy=EastIndianHierarchy(
        level3_state="West Bengal", level4_region="Kolkata", level5_cuisine="Bengali",
        level6_food_family="Rice", level7_food_type="Pulao", level8_variant="Basanti Sweet Pulao",
        level9_cooking_method=["dum_cooked", "ghee_sauteed"], default_portion="1 plate (220g)",
        nutrition_ref_id="wb_rice_basanti_pulao"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="WB_RICE_BHOGER_KHICHURI",
    canonical_name="Bhoger Khichuri",
    state="West Bengal",
    region="Kolkata",
    cuisine="Bengali",
    food_category="Rice",
    regional_names={"English": "Bengali Temple Khichuri", "Bengali": "ভোগের খিচুড়ি", "Hindi": "भोज की खिचड़ी"},
    alternate_names=["durga puja khichuri", "bhog khichuri", "sonar moong dal khichuri"],
    vegetarian=True,
    gravy_type="semi_gravy",
    visual_features={"texture": "creamy_soft_grain_lentil_blend", "color": "deep_golden_yellow", "visible": ["fried_green_peas", "slit_green_chillies", "ginger_bits", "ghee_top"]},
    key_ingredients=["gobindobhog rice", "roasted yellow moong dal", "ghee", "ginger", "green chillies", "cumin seeds", "bay leaves", "garam masala", "turmeric", "green peas"],
    hard_negatives=["WB_RICE_BHUNA_KHICHURI", "OD_RICE_DALMA_RICE"],
    density_g_cm3=0.92,
    default_serving_weight_g=250.0,
    nutrition_per_100g={"calories": 175.0, "protein_g": 5.4, "carbs_g": 26.8, "fat_g": 5.2, "fiber_g": 2.4, "sodium_mg": 210.0},
    hierarchy=EastIndianHierarchy(
        level3_state="West Bengal", level4_region="Kolkata", level5_cuisine="Bengali",
        level6_food_family="Rice", level7_food_type="Khichuri", level8_variant="Bhoger Moong Dal Khichuri",
        level9_cooking_method=["slow_cooked", "boiled", "ghee_tempered"], default_portion="1 large bowl (250g)",
        nutrition_ref_id="wb_rice_bhoger_khichuri"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="WB_RICE_BHUNA_KHICHURI",
    canonical_name="Bhuna Khichuri",
    state="West Bengal",
    region="Kolkata",
    cuisine="Bengali",
    food_category="Rice",
    regional_names={"English": "Bengali Dry Roasted Khichuri", "Bengali": "ভুনা খিচুড়ি", "Hindi": "भूना खिचड़ी"},
    alternate_names=["bengali bhuna khichuri", "dry spiced khichuri"],
    vegetarian=True,
    gravy_type="dry",
    visual_features={"texture": "separated_dry_grains", "color": "spiced_amber_golden", "visible": ["fried_onions", "green_peas", "cashews"]},
    key_ingredients=["gobindobhog rice", "roasted moong dal", "onions", "ginger", "garlic", "ghee", "garam masala"],
    density_g_cm3=0.84,
    default_serving_weight_g=220.0,
    nutrition_per_100g={"calories": 195.0, "protein_g": 5.8, "carbs_g": 29.2, "fat_g": 6.5, "fiber_g": 2.1, "sodium_mg": 230.0},
    hierarchy=EastIndianHierarchy(
        level3_state="West Bengal", level4_region="Kolkata", level5_cuisine="Bengali",
        level6_food_family="Rice", level7_food_type="Khichuri", level8_variant="Bhuna Khichuri",
        level9_cooking_method=["pan_roasted", "dum_cooked"], default_portion="1 plate (220g)",
        nutrition_ref_id="wb_rice_bhuna_khichuri"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="WB_RICE_MACHER_PULAO",
    canonical_name="Macher Pulao",
    state="West Bengal",
    region="Kolkata",
    cuisine="Bengali",
    food_category="Rice",
    regional_names={"English": "Bengali Fragrant Fish Pulao", "Bengali": "মাছের পোলাও", "Hindi": "मछली पुलाव"},
    alternate_names=["fish pulao", "ilish pulao", "katla pulao"],
    vegetarian=False,
    gravy_type="dry",
    visual_features={"rice": "long_or_gobindobhog_spiced_rice", "protein": "golden_fried_fish_steaks_embedded", "garnishes": ["beresta", "green_chillies"]},
    key_ingredients=["rice", "fish steak (katla or ilish)", "ghee", "fried onions (beresta)", "curd", "ginger", "garam masala"],
    fish_species="Katla",
    density_g_cm3=0.86,
    default_serving_weight_g=280.0,
    nutrition_per_100g={"calories": 185.0, "protein_g": 9.2, "carbs_g": 23.4, "fat_g": 6.1, "fiber_g": 1.0, "sodium_mg": 280.0},
    hierarchy=EastIndianHierarchy(
        level3_state="West Bengal", level4_region="Kolkata", level5_cuisine="Bengali",
        level6_food_family="Rice", level7_food_type="Fish Rice", level8_variant="Macher Pulao",
        level9_cooking_method=["dum_cooked", "ghee_fried"], default_portion="1 plate with 1 fish steak (280g)",
        nutrition_ref_id="wb_rice_macher_pulao"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="WB_RICE_BENGALI_FRIED_RICE",
    canonical_name="Bengali Fried Rice",
    state="West Bengal",
    region="Kolkata",
    cuisine="Bengali",
    food_category="Rice",
    regional_names={"English": "Bengali Sweet Vegetable Fried Rice", "Bengali": "বাঙালি ফ্রায়েড রাইস", "Hindi": "बंगाली फ्राइड राइस"},
    alternate_names=["bengali veg fried rice", "sweet fried rice"],
    vegetarian=True,
    gravy_type=None,
    visual_features={"color": "white_or_light_ghee_yellow", "vegetables": ["fine_diced_carrots", "beans", "green_peas", "cashews", "raisins"]},
    key_ingredients=["basmati rice", "ghee", "carrots", "french beans", "peas", "cashews", "raisins", "sugar", "black pepper", "cardamom", "cinnamon"],
    hard_negatives=["WB_RICE_BASANTI_PULAO", "WB_RICE_PLAIN"],
    density_g_cm3=0.81,
    default_serving_weight_g=200.0,
    nutrition_per_100g={"calories": 180.0, "protein_g": 3.4, "carbs_g": 31.0, "fat_g": 4.8, "fiber_g": 1.5, "sodium_mg": 120.0},
    hierarchy=EastIndianHierarchy(
        level3_state="West Bengal", level4_region="Kolkata", level5_cuisine="Bengali",
        level6_food_family="Rice", level7_food_type="Fried Rice", level8_variant="Bengali Ghee Fried Rice",
        level9_cooking_method=["ghee_tossed", "sauteed"], default_portion="1 plate (200g)",
        nutrition_ref_id="wb_rice_bengali_fried_rice"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="WB_RICE_PANTA_BHAT",
    canonical_name="Panta Bhat",
    state="West Bengal",
    region="Rural Bengal",
    cuisine="Bengali",
    food_category="Rice",
    regional_names={"English": "Fermented Soaked Rice", "Bengali": "পান্তা ভাত", "Odia": "ପଖାଳ ଭାତ", "Hindi": "पांता भात"},
    alternate_names=["fermented rice", "pohela boishakh panta"],
    vegetarian=True,
    gravy_type="curd_broth",
    visual_features={"liquid": "clear_or_cloudy_fermented_rice_water", "sides": ["slit_green_chilli", "raw_onion_wedges", "mustard_oil_drizzle", "fried_fish_or_bora"]},
    key_ingredients=["cooked rice soaked overnight in water", "salt", "raw mustard oil", "raw onions", "green chillies"],
    hard_negatives=["OD_RICE_DAHI_PAKHALA", "WB_RICE_PLAIN"],
    density_g_cm3=0.96,
    default_serving_weight_g=300.0,
    nutrition_per_100g={"calories": 85.0, "protein_g": 1.8, "carbs_g": 17.5, "fat_g": 0.8, "fiber_g": 0.5, "sodium_mg": 180.0},
    hierarchy=EastIndianHierarchy(
        level3_state="West Bengal", level4_region="Rural Bengal", level5_cuisine="Bengali",
        level6_food_family="Rice", level7_food_type="Fermented Rice", level8_variant="Panta Bhat",
        level9_cooking_method=["fermented", "soaked"], default_portion="1 bowl with liquid (300g)",
        nutrition_ref_id="wb_rice_panta_bhat"
    )
))

# =============================================================================
# 2. WEST BENGAL: FISH & SEAFOOD MASTER DATASET (Sections 3 & 4)
# =============================================================================

register_east_food(EastIndianFoodClass(
    canonical_food_id="WB_FISH_MACHER_JHOL",
    canonical_name="Macher Jhol",
    state="West Bengal",
    region="Kolkata",
    cuisine="Bengali",
    food_category="Fish/Seafood",
    regional_names={"English": "Bengali Light Fish Curry", "Bengali": "মাছের ঝোল", "Hindi": "माछेर झोल"},
    alternate_names=["bengali fish curry", "macher patla jhol"],
    vegetarian=False,
    gravy_type="jhol_thin_broth",
    visual_features={"gravy": "thin_runny_reddish_yellow_broth", "floating": ["nigella_seeds (kalo jeere)", "green_chillies", "potato_wedges", "cauliflower_or_parwal_optional"], "fish": "bone_in_fried_carp_steak"},
    key_ingredients=["rohu or katla fish steak", "potatoes", "kalo jeere (nigella seeds)", "turmeric", "cumin paste", "ginger paste", "green chillies", "mustard oil"],
    fish_species="Rohu",
    hard_negatives=["WB_FISH_SHORSHE_MAACH", "WB_FISH_DOI_MAACH", "OD_FISH_MACHA_JHOLA"],
    density_g_cm3=0.98,
    default_serving_weight_g=220.0,
    nutrition_per_100g={"calories": 115.0, "protein_g": 10.5, "carbs_g": 3.8, "fat_g": 6.2, "fiber_g": 0.6, "sodium_mg": 280.0},
    hierarchy=EastIndianHierarchy(
        level3_state="West Bengal", level4_region="Kolkata", level5_cuisine="Bengali",
        level6_food_family="Fish/Seafood", level7_food_type="Macher Jhol", level8_variant="Patla Jhol with Aloo",
        level9_cooking_method=["mustard_oil_shallow_fried", "stewed_jhol"], default_portion="1 bowl with 1 fish piece + potato (220g)",
        nutrition_ref_id="wb_fish_macher_jhol"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="WB_FISH_RUI_JHOL",
    canonical_name="Rui Machher Jhol",
    state="West Bengal",
    region="Kolkata",
    cuisine="Bengali",
    food_category="Fish/Seafood",
    regional_names={"English": "Rohu Fish Curry with Potato", "Bengali": "রুই মাছের ঝোল", "Hindi": "रुई माछेर झोल"},
    alternate_names=["rohu macher jhol", "rui mach jhol"],
    vegetarian=False,
    gravy_type="jhol_thin_broth",
    visual_features={"fish": "oval_rohu_steak_with_skin", "broth": "light_cumin_ginger_gravy", "vegetables": ["large_potato_half"]},
    key_ingredients=["rohu (rui) fish", "potatoes", "cumin powder", "coriander powder", "turmeric", "mustard oil", "green chillies"],
    fish_species="Rohu",
    density_g_cm3=0.98,
    default_serving_weight_g=220.0,
    nutrition_per_100g={"calories": 118.0, "protein_g": 11.2, "carbs_g": 3.6, "fat_g": 6.4, "fiber_g": 0.5, "sodium_mg": 275.0},
    hierarchy=EastIndianHierarchy(
        level3_state="West Bengal", level4_region="Kolkata", level5_cuisine="Bengali",
        level6_food_family="Fish/Seafood", level7_food_type="Macher Jhol", level8_variant="Rui Machher Jhol",
        level9_cooking_method=["shallow_fried", "simmered"], default_portion="1 serving (220g)",
        nutrition_ref_id="wb_fish_rui_jhol"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="WB_FISH_KATLA_JHOL",
    canonical_name="Katla Machher Jhol",
    state="West Bengal",
    region="Kolkata",
    cuisine="Bengali",
    food_category="Fish/Seafood",
    regional_names={"English": "Catla Carp Fish Curry", "Bengali": "কাতলা মাছের ঝোল", "Hindi": "कातला माछेर झोल"},
    alternate_names=["katla jhol", "katla macher jhol"],
    vegetarian=False,
    gravy_type="jhol_thin_broth",
    visual_features={"fish": "broad_thick_catla_peti_or_gada_piece", "broth": "aromatic_cumin_ginger_broth"},
    key_ingredients=["katla fish steak", "potatoes", "cumin", "ginger", "mustard oil", "turmeric", "green chillies"],
    fish_species="Catla",
    density_g_cm3=0.98,
    default_serving_weight_g=230.0,
    nutrition_per_100g={"calories": 122.0, "protein_g": 11.8, "carbs_g": 3.5, "fat_g": 6.8, "fiber_g": 0.5, "sodium_mg": 280.0},
    hierarchy=EastIndianHierarchy(
        level3_state="West Bengal", level4_region="Kolkata", level5_cuisine="Bengali",
        level6_food_family="Fish/Seafood", level7_food_type="Macher Jhol", level8_variant="Katla Machher Jhol",
        level9_cooking_method=["shallow_fried", "simmered"], default_portion="1 serving (230g)",
        nutrition_ref_id="wb_fish_katla_jhol"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="WB_FISH_SHORSHE_ILISH",
    canonical_name="Shorshe Ilish",
    state="West Bengal",
    region="Kolkata",
    cuisine="Bengali",
    food_category="Fish/Seafood",
    regional_names={"English": "Hilsa in Mustard Gravy", "Bengali": "সর্ষে ইলিশ", "Hindi": "सोरषे इलिश"},
    alternate_names=["mustard hilsa", "ilish shorshe", "shorshe bata ilish"],
    vegetarian=False,
    gravy_type="mustard_gravy",
    visual_features={"gravy": "thick_yellow_pungent_mustard_paste", "oil": "floating_golden_mustard_oil_sheen", "fish": "broad_silvery_cut_hilsa_steak", "garnish": ["slit_bright_green_chillies", "black_mustard_seeds"]},
    key_ingredients=["hilsa (ilish) fish", "yellow and black mustard seeds ground", "green chillies", "raw mustard oil", "turmeric", "kalo jeere (nigella seeds)"],
    fish_species="Hilsa",
    hard_negatives=["WB_FISH_SHORSHE_RUI", "WB_FISH_MACHER_JHOL", "WB_FISH_ILISH_BHAPA"],
    density_g_cm3=1.02,
    default_serving_weight_g=200.0,
    nutrition_per_100g={"calories": 240.0, "protein_g": 14.5, "carbs_g": 3.2, "fat_g": 18.8, "fiber_g": 1.2, "sodium_mg": 310.0},
    hierarchy=EastIndianHierarchy(
        level3_state="West Bengal", level4_region="Kolkata", level5_cuisine="Bengali",
        level6_food_family="Fish/Seafood", level7_food_type="Mustard Fish", level8_variant="Shorshe Ilish",
        level9_cooking_method=["mustard_paste_simmered", "mustard_oil_tempered"], default_portion="1 fish piece with mustard gravy (200g)",
        nutrition_ref_id="wb_fish_shorshe_ilish"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="WB_FISH_ILISH_BHAPA",
    canonical_name="Ilish Bhapa",
    state="West Bengal",
    region="Kolkata",
    cuisine="Bengali",
    food_category="Fish/Seafood",
    regional_names={"English": "Steamed Hilsa in Mustard and Coconut", "Bengali": "ভাপা ইলিশ", "Hindi": "भापा इलिश"},
    alternate_names=["steamed hilsa", "bhapa ilish", "ilish bhapa"],
    vegetarian=False,
    gravy_type="mustard_gravy",
    visual_features={"coating": "creamy_pale_yellow_coconut_mustard_paste", "fish": "delicate_steamed_hilsa_steak_not_fried", "toppings": ["whole_green_chillies", "drizzle_of_raw_mustard_oil"]},
    key_ingredients=["hilsa fish", "fresh grated coconut paste", "mustard paste", "green chillies", "mustard oil", "turmeric", "curd optional"],
    fish_species="Hilsa",
    hard_negatives=["WB_FISH_SHORSHE_ILISH", "WB_FISH_ILISH_PATURI"],
    density_g_cm3=1.01,
    default_serving_weight_g=190.0,
    nutrition_per_100g={"calories": 235.0, "protein_g": 14.2, "carbs_g": 2.8, "fat_g": 18.5, "fiber_g": 1.0, "sodium_mg": 290.0},
    hierarchy=EastIndianHierarchy(
        level3_state="West Bengal", level4_region="Kolkata", level5_cuisine="Bengali",
        level6_food_family="Fish/Seafood", level7_food_type="Bhapa Fish", level8_variant="Ilish Bhapa",
        level9_cooking_method=["steamed_tiffin_box"], default_portion="1 steak with coating (190g)",
        nutrition_ref_id="wb_fish_ilish_bhapa"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="WB_FISH_ILISH_PATURI",
    canonical_name="Ilish Paturi",
    state="West Bengal",
    region="Kolkata",
    cuisine="Bengali",
    food_category="Fish/Seafood",
    regional_names={"English": "Hilsa in Banana Leaf Parcel", "Bengali": "ইলিশ পাতুড়ি", "Hindi": "इलिश पातुरी"},
    alternate_names=["banana leaf hilsa", "paturi ilish"],
    vegetarian=False,
    gravy_type="mustard_gravy",
    visual_features={"wrapper": "charred_glossy_green_banana_leaf_tied_with_thread", "inside": "hilsa_fillet_coated_in_mustard_paste_with_green_chilli"},
    key_ingredients=["hilsa steak", "banana leaf", "mustard paste", "green chilli", "mustard oil", "turmeric", "salt"],
    fish_species="Hilsa",
    hard_negatives=["WB_FISH_BHETKI_PATURI", "WB_FISH_ILISH_BHAPA"],
    density_g_cm3=0.98,
    default_serving_weight_g=170.0,
    nutrition_per_100g={"calories": 225.0, "protein_g": 15.0, "carbs_g": 2.5, "fat_g": 17.2, "fiber_g": 0.8, "sodium_mg": 280.0},
    hierarchy=EastIndianHierarchy(
        level3_state="West Bengal", level4_region="Kolkata", level5_cuisine="Bengali",
        level6_food_family="Fish/Seafood", level7_food_type="Paturi", level8_variant="Ilish Paturi",
        level9_cooking_method=["leaf_wrapped_pan_steamed"], default_portion="1 leaf parcel (170g)",
        nutrition_ref_id="wb_fish_ilish_paturi"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="WB_FISH_ILISH_JHOL",
    canonical_name="Ilish Jhol",
    state="West Bengal",
    region="Kolkata",
    cuisine="Bengali",
    food_category="Fish/Seafood",
    regional_names={"English": "Hilsa Light Stew with Eggplant & Nigella", "Bengali": "ইলিশের তেল ঝোল", "Hindi": "इलिश झोल"},
    alternate_names=["ilish tel jhol", "begun ilish jhol"],
    vegetarian=False,
    gravy_type="jhol_thin_broth",
    visual_features={"gravy": "very_thin_golden_broth", "floating": ["nigella_seeds", "slit_green_chillies", "long_sliced_eggplants_or_pointed_gourd"], "fish": "tender_hilsa"},
    key_ingredients=["hilsa fish", "eggplant slices", "kalo jeere", "green chillies", "turmeric", "mustard oil", "salt"],
    fish_species="Hilsa",
    density_g_cm3=0.98,
    default_serving_weight_g=210.0,
    nutrition_per_100g={"calories": 190.0, "protein_g": 12.8, "carbs_g": 2.4, "fat_g": 14.5, "fiber_g": 0.9, "sodium_mg": 260.0},
    hierarchy=EastIndianHierarchy(
        level3_state="West Bengal", level4_region="Kolkata", level5_cuisine="Bengali",
        level6_food_family="Fish/Seafood", level7_food_type="Macher Jhol", level8_variant="Ilish Tel Jhol",
        level9_cooking_method=["simmered"], default_portion="1 bowl (210g)",
        nutrition_ref_id="wb_fish_ilish_jhol"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="WB_FISH_SHORSHE_RUI",
    canonical_name="Shorshe Rui",
    state="West Bengal",
    region="Kolkata",
    cuisine="Bengali",
    food_category="Fish/Seafood",
    regional_names={"English": "Rohu Fish in Mustard Gravy", "Bengali": "সর্ষে রুই", "Hindi": "सोरषे रुई"},
    alternate_names=["mustard rohu", "rui shorshe"],
    vegetarian=False,
    gravy_type="mustard_gravy",
    visual_features={"gravy": "thick_yellow_mustard_curry", "fish": "fried_rohu_carp_steak", "garnish": ["green_chillies", "raw_mustard_oil"]},
    key_ingredients=["rohu fish", "yellow and black mustard paste", "green chillies", "kalo jeere", "mustard oil", "turmeric"],
    fish_species="Rohu",
    density_g_cm3=1.01,
    default_serving_weight_g=210.0,
    nutrition_per_100g={"calories": 170.0, "protein_g": 13.5, "carbs_g": 3.4, "fat_g": 11.2, "fiber_g": 1.1, "sodium_mg": 290.0},
    hierarchy=EastIndianHierarchy(
        level3_state="West Bengal", level4_region="Kolkata", level5_cuisine="Bengali",
        level6_food_family="Fish/Seafood", level7_food_type="Mustard Fish", level8_variant="Shorshe Rui",
        level9_cooking_method=["shallow_fried", "mustard_simmered"], default_portion="1 fish steak with gravy (210g)",
        nutrition_ref_id="wb_fish_shorshe_rui"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="WB_FISH_SHORSHE_KATLA",
    canonical_name="Shorshe Katla",
    state="West Bengal",
    region="Kolkata",
    cuisine="Bengali",
    food_category="Fish/Seafood",
    regional_names={"English": "Catla Fish in Mustard Gravy", "Bengali": "সর্ষে কাতলা", "Hindi": "सोरषे कातला"},
    alternate_names=["mustard katla", "katla shorshe"],
    vegetarian=False,
    gravy_type="mustard_gravy",
    visual_features={"gravy": "thick_yellow_mustard_gravy", "fish": "large_broad_catla_steak"},
    key_ingredients=["katla fish", "mustard paste", "green chillies", "kalo jeere", "mustard oil", "turmeric"],
    fish_species="Catla",
    density_g_cm3=1.01,
    default_serving_weight_g=220.0,
    nutrition_per_100g={"calories": 175.0, "protein_g": 13.8, "carbs_g": 3.4, "fat_g": 11.5, "fiber_g": 1.1, "sodium_mg": 295.0},
    hierarchy=EastIndianHierarchy(
        level3_state="West Bengal", level4_region="Kolkata", level5_cuisine="Bengali",
        level6_food_family="Fish/Seafood", level7_food_type="Mustard Fish", level8_variant="Shorshe Katla",
        level9_cooking_method=["shallow_fried", "mustard_simmered"], default_portion="1 serving (220g)",
        nutrition_ref_id="wb_fish_shorshe_katla"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="WB_FISH_SHORSHE_BHETKI",
    canonical_name="Shorshe Bhetki",
    state="West Bengal",
    region="Kolkata",
    cuisine="Bengali",
    food_category="Fish/Seafood",
    regional_names={"English": "Barramundi Fish in Mustard Gravy", "Bengali": "সর্ষে ভেটকি", "Hindi": "सोरषे भेटकी"},
    alternate_names=["mustard bhetki", "bhetki shorshe"],
    vegetarian=False,
    gravy_type="mustard_gravy",
    visual_features={"gravy": "yellow_mustard_paste", "fish": "boneless_or_steak_barramundi_fillets"},
    key_ingredients=["bhetki (barramundi)", "mustard paste", "green chillies", "mustard oil", "turmeric"],
    fish_species="Bhetki",
    density_g_cm3=1.01,
    default_serving_weight_g=200.0,
    nutrition_per_100g={"calories": 160.0, "protein_g": 14.5, "carbs_g": 3.0, "fat_g": 9.8, "fiber_g": 1.0, "sodium_mg": 280.0},
    hierarchy=EastIndianHierarchy(
        level3_state="West Bengal", level4_region="Kolkata", level5_cuisine="Bengali",
        level6_food_family="Fish/Seafood", level7_food_type="Mustard Fish", level8_variant="Shorshe Bhetki",
        level9_cooking_method=["simmered"], default_portion="1 serving (200g)",
        nutrition_ref_id="wb_fish_shorshe_bhetki"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="WB_FISH_DOI_MAACH",
    canonical_name="Doi Maach",
    state="West Bengal",
    region="Kolkata",
    cuisine="Bengali",
    food_category="Fish/Seafood",
    regional_names={"English": "Bengali Yogurt Fish Curry", "Bengali": "দই মাছ", "Hindi": "दही मछली"},
    alternate_names=["doi katla", "doi rui", "yogurt fish curry"],
    vegetarian=False,
    gravy_type="curd_broth",
    visual_features={"gravy": "creamy_pale_ivory_golden_yogurt_gravy", "floating": ["cinnamon_stick", "green_cardamom", "cloves", "raisins_optional", "slit_green_chillies"], "fish": "fried_carp_steak"},
    key_ingredients=["katla or rohu fish", "whisked curd (dahi)", "onion paste", "ginger paste", "garam masala", "mustard oil", "bay leaves", "green chillies", "sugar hint"],
    fish_species="Catla",
    hard_negatives=["WB_FISH_MACHER_JHOL", "WB_FISH_CHINGRI_MALAI_CURRY"],
    density_g_cm3=1.01,
    default_serving_weight_g=230.0,
    nutrition_per_100g={"calories": 165.0, "protein_g": 12.2, "carbs_g": 5.1, "fat_g": 10.8, "fiber_g": 0.6, "sodium_mg": 290.0},
    hierarchy=EastIndianHierarchy(
        level3_state="West Bengal", level4_region="Kolkata", level5_cuisine="Bengali",
        level6_food_family="Fish/Seafood", level7_food_type="Curd Fish", level8_variant="Doi Katla",
        level9_cooking_method=["shallow_fried", "yogurt_simmered"], default_portion="1 bowl with fish steak (230g)",
        nutrition_ref_id="wb_fish_doi_maach"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="WB_FISH_CHINGRI_MALAI_CURRY",
    canonical_name="Chingri Malai Curry",
    state="West Bengal",
    region="Kolkata",
    cuisine="Bengali",
    food_category="Fish/Seafood",
    regional_names={"English": "Prawn Coconut Cream Curry", "Bengali": "চিংড়ি মালাই কারি", "Hindi": "चिंगड़ी मलाई करी"},
    alternate_names=["prawn malai curry", "golda chingri malai curry", "bagda chingri malai"],
    vegetarian=False,
    gravy_type="coconut_gravy",
    visual_features={"gravy": "luxurious_golden_orange_coconut_cream_gravy", "prawns": "large_jumbo_prawns_with_head_and_tail", "sheen": "ghee_and_coconut_oil_surface"},
    key_ingredients=["jumbo prawns (golda or bagda chingri)", "thick coconut milk", "onion paste", "ginger paste", "whole garam masala", "sugar", "ghee", "mustard oil", "green chillies"],
    fish_species="Prawn",
    hard_negatives=["WB_FISH_DOI_MAACH", "OD_SEAFOOD_CHINGUDI_BESARA"],
    density_g_cm3=1.02,
    default_serving_weight_g=240.0,
    nutrition_per_100g={"calories": 195.0, "protein_g": 11.5, "carbs_g": 6.2, "fat_g": 14.2, "fiber_g": 1.0, "sodium_mg": 320.0},
    hierarchy=EastIndianHierarchy(
        level3_state="West Bengal", level4_region="Kolkata", level5_cuisine="Bengali",
        level6_food_family="Fish/Seafood", level7_food_type="Malai Curry", level8_variant="Chingri Malai Curry",
        level9_cooking_method=["ghee_sauteed", "coconut_milk_simmered"], default_portion="2-3 prawns with gravy (240g)",
        nutrition_ref_id="wb_fish_chingri_malai_curry"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="WB_FISH_CHINGRI_BHAPA",
    canonical_name="Chingri Bhapa",
    state="West Bengal",
    region="Kolkata",
    cuisine="Bengali",
    food_category="Fish/Seafood",
    regional_names={"English": "Steamed Mustard Coconut Prawns", "Bengali": "ভাপা চিংড়ি", "Hindi": "भापा चिंगड़ी"},
    alternate_names=["steamed prawns", "bhapa chingri"],
    vegetarian=False,
    gravy_type="mustard_gravy",
    visual_features={"coating": "yellow_mustard_coconut_paste", "prawns": "medium_prawns_coated"},
    key_ingredients=["prawns", "mustard paste", "coconut paste", "green chillies", "mustard oil", "turmeric"],
    fish_species="Prawn",
    density_g_cm3=1.01,
    default_serving_weight_g=180.0,
    nutrition_per_100g={"calories": 180.0, "protein_g": 13.8, "carbs_g": 3.8, "fat_g": 12.2, "fiber_g": 1.1, "sodium_mg": 300.0},
    hierarchy=EastIndianHierarchy(
        level3_state="West Bengal", level4_region="Kolkata", level5_cuisine="Bengali",
        level6_food_family="Fish/Seafood", level7_food_type="Bhapa Seafood", level8_variant="Chingri Bhapa",
        level9_cooking_method=["steamed_tiffin_box"], default_portion="1 serving (180g)",
        nutrition_ref_id="wb_fish_chingri_bhapa"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="WB_FISH_CHINGRI_PATURI",
    canonical_name="Chingri Paturi",
    state="West Bengal",
    region="Kolkata",
    cuisine="Bengali",
    food_category="Fish/Seafood",
    regional_names={"English": "Prawns in Banana Leaf Parcel", "Bengali": "চিংড়ি পাতুড়ি", "Hindi": "चिंगड़ी पातुरी"},
    alternate_names=["leaf wrapped prawns", "chingri paturi"],
    vegetarian=False,
    gravy_type="mustard_gravy",
    visual_features={"wrapper": "folded_toasted_banana_leaf_packet", "inside": "prawns_in_spicy_mustard_coating"},
    key_ingredients=["prawns", "banana leaf", "mustard paste", "green chilli", "mustard oil", "turmeric"],
    fish_species="Prawn",
    density_g_cm3=0.99,
    default_serving_weight_g=160.0,
    nutrition_per_100g={"calories": 175.0, "protein_g": 14.0, "carbs_g": 3.2, "fat_g": 11.5, "fiber_g": 0.8, "sodium_mg": 290.0},
    hierarchy=EastIndianHierarchy(
        level3_state="West Bengal", level4_region="Kolkata", level5_cuisine="Bengali",
        level6_food_family="Fish/Seafood", level7_food_type="Paturi", level8_variant="Chingri Paturi",
        level9_cooking_method=["leaf_wrapped_pan_steamed"], default_portion="1 packet (160g)",
        nutrition_ref_id="wb_fish_chingri_paturi"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="WB_FISH_BHETKI_PATURI",
    canonical_name="Bhetki Paturi",
    state="West Bengal",
    region="Kolkata",
    cuisine="Bengali",
    food_category="Fish/Seafood",
    regional_names={"English": "Barramundi Fish in Banana Leaf", "Bengali": "ভেটকি পাতুড়ি", "Hindi": "भेटकी पातुरी"},
    alternate_names=["barramundi paturi", "bhetki macher paturi"],
    vegetarian=False,
    gravy_type="mustard_gravy",
    visual_features={"wrapper": "charred_steamed_banana_leaf_secured_with_string", "inside": "tender_boneless_white_bhetki_fillet_coated_in_mustard_coconut_paste", "garnish": ["split_green_chilli"]},
    key_ingredients=["bhetki (barramundi) fillet", "mustard paste", "coconut paste", "green chillies", "mustard oil", "turmeric", "banana leaf"],
    fish_species="Bhetki",
    hard_negatives=["WB_FISH_ILISH_PATURI", "WB_FISH_BHETKI_FRY"],
    density_g_cm3=0.98,
    default_serving_weight_g=160.0,
    nutrition_per_100g={"calories": 165.0, "protein_g": 15.5, "carbs_g": 2.8, "fat_g": 10.2, "fiber_g": 0.8, "sodium_mg": 270.0},
    hierarchy=EastIndianHierarchy(
        level3_state="West Bengal", level4_region="Kolkata", level5_cuisine="Bengali",
        level6_food_family="Fish/Seafood", level7_food_type="Paturi", level8_variant="Bhetki Paturi",
        level9_cooking_method=["leaf_wrapped_pan_steamed"], default_portion="1 leaf parcel (160g)",
        nutrition_ref_id="wb_fish_bhetki_paturi"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="WB_FISH_BHETKI_FRY",
    canonical_name="Bhetki Fish Fry",
    state="West Bengal",
    region="Kolkata",
    cuisine="Bengali",
    food_category="Street Food",
    regional_names={"English": "Kolkata Style Crumbed Bhetki Fry", "Bengali": "কলকাতা ফিশ ফ্রাই", "Hindi": "कोलकाता फिश फ्राई"},
    alternate_names=["kolkata fish fry", "bengali fish cutlet", "fish fry"],
    vegetarian=False,
    gravy_type="dry",
    visual_features={"shape": "flat_rectangular_or_diamond_fillet", "crust": "golden_brown_crisp_breadcrumb_coating", "sides": ["kasundi (bengali mustard sauce)", "sliced_onions", "cucumber_salad"]},
    key_ingredients=["bhetki fish fillet marinated in coriander-mint-green chilli-onion paste", "bread crumbs", "egg wash", "mustard oil or refined oil", "kasundi accompaniment"],
    fish_species="Bhetki",
    hard_negatives=["WB_MEAT_CHICKEN_CUTLET", "WB_FISH_MAACH_BHAJA"],
    density_g_cm3=0.82,
    default_serving_weight_g=130.0,
    nutrition_per_100g={"calories": 245.0, "protein_g": 14.8, "carbs_g": 16.5, "fat_g": 13.5, "fiber_g": 1.2, "sodium_mg": 380.0},
    hierarchy=EastIndianHierarchy(
        level3_state="West Bengal", level4_region="Kolkata", level5_cuisine="Bengali",
        level6_food_family="Street Food", level7_food_type="Fish Cutlet", level8_variant="Bhetki Crumbed Fry",
        level9_cooking_method=["crumbed", "deep_fried"], default_portion="1 piece (130g)",
        nutrition_ref_id="wb_fish_bhetki_fry"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="WB_FISH_MAACH_BHAJA",
    canonical_name="Maach Bhaja",
    state="West Bengal",
    region="Kolkata",
    cuisine="Bengali",
    food_category="Fish/Seafood",
    regional_names={"English": "Crispy Turmeric Fried Fish", "Bengali": "মাছ ভাজা", "Hindi": "माछ भाजा"},
    alternate_names=["fried fish", "katla bhaja", "rui bhaja", "ilish bhaja"],
    vegetarian=False,
    gravy_type="dry",
    visual_features={"crust": "crispy_blistered_golden_turmeric_crust_without_breadcrumbs", "fish": "bone_in_carp_or_hilsa_steak", "sheen": "mustard_oil_shine"},
    key_ingredients=["fish steak", "turmeric powder", "salt", "pure mustard oil"],
    fish_species="Rohu",
    density_g_cm3=0.88,
    default_serving_weight_g=100.0,
    nutrition_per_100g={"calories": 195.0, "protein_g": 16.2, "carbs_g": 0.8, "fat_g": 14.2, "fiber_g": 0.0, "sodium_mg": 280.0},
    hierarchy=EastIndianHierarchy(
        level3_state="West Bengal", level4_region="Kolkata", level5_cuisine="Bengali",
        level6_food_family="Fish/Seafood", level7_food_type="Fried Fish", level8_variant="Maach Bhaja",
        level9_cooking_method=["mustard_oil_shallow_fried"], default_portion="1 steak (100g)",
        nutrition_ref_id="wb_fish_maach_bhaja"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="WB_FISH_PABDA_JHOL",
    canonical_name="Pabda Machher Jhol",
    state="West Bengal",
    region="Kolkata",
    cuisine="Bengali",
    food_category="Fish/Seafood",
    regional_names={"English": "Butterfish Light Nigella Gravy", "Bengali": "পাবদা মাছের ঝোল", "Hindi": "पाबदा माछेर झोल"},
    alternate_names=["pabda jhol", "pabda tel jhol", "shorshe pabda"],
    vegetarian=False,
    gravy_type="jhol_thin_broth",
    visual_features={"fish": "whole_slender_silvery_butterfish_with_long_whiskers", "gravy": "light_yellowish_cumin_nigella_broth", "garnish": ["green_chillies", "fresh_coriander"]},
    key_ingredients=["whole pabda fish", "kalo jeere", "green chillies", "turmeric", "cumin paste", "mustard oil", "coriander leaves"],
    fish_species="Pabda",
    density_g_cm3=0.97,
    default_serving_weight_g=190.0,
    nutrition_per_100g={"calories": 135.0, "protein_g": 12.0, "carbs_g": 2.2, "fat_g": 8.5, "fiber_g": 0.4, "sodium_mg": 260.0},
    hierarchy=EastIndianHierarchy(
        level3_state="West Bengal", level4_region="Kolkata", level5_cuisine="Bengali",
        level6_food_family="Fish/Seafood", level7_food_type="Macher Jhol", level8_variant="Pabda Machher Jhol",
        level9_cooking_method=["simmered"], default_portion="1 whole fish with broth (190g)",
        nutrition_ref_id="wb_fish_pabda_jhol"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="WB_FISH_TANGRA_JHOL",
    canonical_name="Tangra Machher Jhol",
    state="West Bengal",
    region="Kolkata",
    cuisine="Bengali",
    food_category="Fish/Seafood",
    regional_names={"English": "Freshwater Catfish Spicy Stew", "Bengali": "ট্যাংরা মাছের ঝোল", "Hindi": "टैंगरा माछेर झोल"},
    alternate_names=["tangra jhal", "tangra macher jhol"],
    vegetarian=False,
    gravy_type="semi_gravy",
    visual_features={"fish": "small_slender_catfish_with_barbels", "vegetables": ["potato_slivers", "onion_stalks_or_eggplant"], "gravy": "reddish_brown_onion_cumin_sauce"},
    key_ingredients=["tangra catfish", "potatoes", "onion paste", "ginger paste", "kalo jeere", "green chillies", "mustard oil"],
    fish_species="Tangra",
    density_g_cm3=0.99,
    default_serving_weight_g=190.0,
    nutrition_per_100g={"calories": 140.0, "protein_g": 12.5, "carbs_g": 3.8, "fat_g": 8.2, "fiber_g": 0.6, "sodium_mg": 270.0},
    hierarchy=EastIndianHierarchy(
        level3_state="West Bengal", level4_region="Kolkata", level5_cuisine="Bengali",
        level6_food_family="Fish/Seafood", level7_food_type="Macher Jhol", level8_variant="Tangra Machher Jhol",
        level9_cooking_method=["simmered"], default_portion="2-3 small fish with gravy (190g)",
        nutrition_ref_id="wb_fish_tangra_jhol"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="WB_FISH_TEL_KOI",
    canonical_name="Tel Koi",
    state="West Bengal",
    region="Kolkata",
    cuisine="Bengali",
    food_category="Fish/Seafood",
    regional_names={"English": "Climbing Perch in Rich Mustard Oil Gravy", "Bengali": "তেল কই", "Hindi": "तेल कोई"},
    alternate_names=["koi macher jhol", "tel koi mach"],
    vegetarian=False,
    gravy_type="semi_gravy",
    visual_features={"fish": "whole_climbing_perch_fish", "gravy": "pungent_dark_spiced_mustard_oil_rich_gravy"},
    key_ingredients=["koi fish (climbing perch)", "generous mustard oil", "ginger paste", "cumin powder", "red chilli powder", "kalo jeere", "green chillies"],
    fish_species="Koi",
    density_g_cm3=1.01,
    default_serving_weight_g=180.0,
    nutrition_per_100g={"calories": 210.0, "protein_g": 13.5, "carbs_g": 2.5, "fat_g": 16.5, "fiber_g": 0.5, "sodium_mg": 290.0},
    hierarchy=EastIndianHierarchy(
        level3_state="West Bengal", level4_region="Kolkata", level5_cuisine="Bengali",
        level6_food_family="Fish/Seafood", level7_food_type="Tel Koi", level8_variant="Authentic Tel Koi",
        level9_cooking_method=["slow_cooked", "mustard_oil_simmered"], default_portion="1 fish with gravy (180g)",
        nutrition_ref_id="wb_fish_tel_koi"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="WB_FISH_KATLA_KALIA",
    canonical_name="Katla Macher Kalia",
    state="West Bengal",
    region="Kolkata",
    cuisine="Bengali",
    food_category="Fish/Seafood",
    regional_names={"English": "Bengali Rich Festive Fish Kalia", "Bengali": "কাতলা মাছের কালিয়া", "Hindi": "कातला माछेर कालिया"},
    alternate_names=["macher kalia", "fish kalia"],
    vegetarian=False,
    gravy_type="semi_gravy",
    visual_features={"gravy": "rich_dark_caramel_onion_gravy", "garnishes": ["fried_raisins", "ghee_sheen"], "fish": "thick_fried_catla_steak"},
    key_ingredients=["katla fish steak", "onion paste", "ginger garlic paste", "curd", "whole garam masala", "raisins", "ghee", "mustard oil"],
    fish_species="Catla",
    density_g_cm3=1.02,
    default_serving_weight_g=240.0,
    nutrition_per_100g={"calories": 185.0, "protein_g": 12.8, "carbs_g": 5.8, "fat_g": 12.2, "fiber_g": 0.8, "sodium_mg": 310.0},
    hierarchy=EastIndianHierarchy(
        level3_state="West Bengal", level4_region="Kolkata", level5_cuisine="Bengali",
        level6_food_family="Fish/Seafood", level7_food_type="Kalia", level8_variant="Katla Kalia",
        level9_cooking_method=["slow_cooked_bhuna", "ghee_simmered"], default_portion="1 fish steak with rich kalia (240g)",
        nutrition_ref_id="wb_fish_katla_kalia"
    )
))

# =============================================================================
# 3. WEST BENGAL: MEAT MASTER DATASET (Section 5)
# =============================================================================

register_east_food(EastIndianFoodClass(
    canonical_food_id="WB_MEAT_KOSHA_MANGSHO",
    canonical_name="Kosha Mangsho",
    state="West Bengal",
    region="Kolkata",
    cuisine="Bengali",
    food_category="Meat",
    regional_names={"English": "Bengali Slow Cooked Dry Mutton", "Bengali": "কষা মাংস", "Hindi": "कशा मांगशो"},
    alternate_names=["bengali mutton kasha", "kosha khashi", "kolkata kosha mangsho"],
    vegetarian=False,
    gravy_type="semi_gravy",
    visual_features={"gravy": "glistening_dark_brown_caramelized_onion_coating", "meat": "tender_mutton_pieces_clinging_to_thick_masala", "oil": "pungent_mustard_oil_float", "vegetable": ["optional_large_halved_golden_fried_potato"]},
    key_ingredients=["goat mutton with bone", "caramelized onions", "ginger garlic paste", "curd", "mustard oil", "kashmiri chilli", "garam masala", "sugar caramel"],
    hard_negatives=["WB_MEAT_MUTTON_JHOL", "BR_MEAT_CHAMPARAN_MUTTON"],
    density_g_cm3=1.05,
    default_serving_weight_g=250.0,
    nutrition_per_100g={"calories": 265.0, "protein_g": 16.5, "carbs_g": 5.2, "fat_g": 19.8, "fiber_g": 1.2, "sodium_mg": 360.0},
    hierarchy=EastIndianHierarchy(
        level3_state="West Bengal", level4_region="Kolkata", level5_cuisine="Bengali",
        level6_food_family="Meat", level7_food_type="Kosha", level8_variant="Slow Cooked Kosha Mangsho",
        level9_cooking_method=["slow_cooked_kasha", "bhuna", "pressure_cooked"], default_portion="3-4 mutton pieces with thick gravy (250g)",
        nutrition_ref_id="wb_meat_kosha_mangsho"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="WB_MEAT_MUTTON_JHOL",
    canonical_name="Bengali Mutton Jhol",
    state="West Bengal",
    region="Kolkata",
    cuisine="Bengali",
    food_category="Meat",
    regional_names={"English": "Sunday Bengali Mutton Curry with Potatoes", "Bengali": "রবিবারের খাসির মাংসের লাল ঝোল", "Hindi": "बंगाली मटन लाल झोल"},
    alternate_names=["sunday mutton jhol", "mangsher jhol", "alur jhol mangsho"],
    vegetarian=False,
    gravy_type="jhol_thin_broth",
    visual_features={"gravy": "vibrant_reddish_thin_aromatic_broth", "potato": "prominent_large_halved_potato_softly_cooked", "meat": "bone_in_mutton_pieces"},
    key_ingredients=["mutton", "large halved potatoes (aloo)", "onions", "ginger", "garlic", "coriander powder", "cumin", "garam masala", "mustard oil"],
    density_g_cm3=1.00,
    default_serving_weight_g=280.0,
    nutrition_per_100g={"calories": 195.0, "protein_g": 13.5, "carbs_g": 6.8, "fat_g": 12.5, "fiber_g": 1.1, "sodium_mg": 330.0},
    hierarchy=EastIndianHierarchy(
        level3_state="West Bengal", level4_region="Kolkata", level5_cuisine="Bengali",
        level6_food_family="Meat", level7_food_type="Mutton Jhol", level8_variant="Sunday Mangsher Jhol",
        level9_cooking_method=["pressure_cooked", "stewed_jhol"], default_portion="1 bowl with 2 mutton pieces + 1 aloo (280g)",
        nutrition_ref_id="wb_meat_mutton_jhol"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="WB_MEAT_CHICKEN_KOSHA",
    canonical_name="Chicken Kosha",
    state="West Bengal",
    region="Kolkata",
    cuisine="Bengali",
    food_category="Meat",
    regional_names={"English": "Bengali Spiced Roast Chicken Gravy", "Bengali": "চিকেন কষা", "Hindi": "चिकन कशा"},
    alternate_names=["murgir kosha", "bengali chicken kasha"],
    vegetarian=False,
    gravy_type="semi_gravy",
    visual_features={"gravy": "thick_rich_brownish_red_masala", "chicken": "curry_cut_chicken_coated"},
    key_ingredients=["chicken pieces", "onions", "ginger garlic paste", "curd", "mustard oil", "turmeric", "red chilli", "garam masala"],
    density_g_cm3=1.03,
    default_serving_weight_g=240.0,
    nutrition_per_100g={"calories": 210.0, "protein_g": 16.8, "carbs_g": 4.5, "fat_g": 13.8, "fiber_g": 1.0, "sodium_mg": 340.0},
    hierarchy=EastIndianHierarchy(
        level3_state="West Bengal", level4_region="Kolkata", level5_cuisine="Bengali",
        level6_food_family="Meat", level7_food_type="Kosha", level8_variant="Chicken Kosha",
        level9_cooking_method=["slow_cooked_kasha"], default_portion="1 bowl (240g)",
        nutrition_ref_id="wb_meat_chicken_kosha"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="WB_MEAT_CHICKEN_JHOL",
    canonical_name="Bengali Chicken Curry",
    state="West Bengal",
    region="Kolkata",
    cuisine="Bengali",
    food_category="Meat",
    regional_names={"English": "Light Bengali Chicken Curry with Potatoes", "Bengali": "মুরগির লাল ঝোল", "Hindi": "मुर्गिर लाल झोल"},
    alternate_names=["murgir jhol", "chicken patla jhol"],
    vegetarian=False,
    gravy_type="jhol_thin_broth",
    visual_features={"gravy": "thin_runny_reddish_broth", "potato": "golden_fried_halved_potatoes", "chicken": "tender_bone_in_pieces"},
    key_ingredients=["chicken", "potatoes", "onions", "ginger garlic", "cumin powder", "mustard oil", "turmeric", "coriander"],
    density_g_cm3=0.99,
    default_serving_weight_g=260.0,
    nutrition_per_100g={"calories": 165.0, "protein_g": 14.2, "carbs_g": 5.5, "fat_g": 9.5, "fiber_g": 0.8, "sodium_mg": 310.0},
    hierarchy=EastIndianHierarchy(
        level3_state="West Bengal", level4_region="Kolkata", level5_cuisine="Bengali",
        level6_food_family="Meat", level7_food_type="Chicken Jhol", level8_variant="Murgir Jhol with Aloo",
        level9_cooking_method=["simmered_jhol"], default_portion="1 bowl with 2 chicken pieces + 1 aloo (260g)",
        nutrition_ref_id="wb_meat_chicken_jhol"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="WB_MEAT_DAK_BUNGALOW_CHICKEN",
    canonical_name="Chicken Dak Bungalow",
    state="West Bengal",
    region="Colonial Bengal",
    cuisine="Bengali",
    food_category="Meat",
    regional_names={"English": "Colonial Dak Bungalow Chicken Curry", "Bengali": "ডাকবাংলো চিকেন", "Hindi": "डाक बंगला चिकन"},
    alternate_names=["dak bungalow murgi", "dak bungalow curry"],
    vegetarian=False,
    gravy_type="semi_gravy",
    visual_features={"key_visuals": ["whole_boiled_eggs_with_fried_blistered_skin", "large_halved_potatoes", "chicken_pieces_in_spiced_gravy"]},
    key_ingredients=["chicken", "hard boiled eggs", "potatoes", "whole roasted spices", "mustard oil", "onion paste", "curd"],
    density_g_cm3=1.02,
    default_serving_weight_g=300.0,
    nutrition_per_100g={"calories": 190.0, "protein_g": 15.5, "carbs_g": 5.8, "fat_g": 11.8, "fiber_g": 1.0, "sodium_mg": 330.0},
    hierarchy=EastIndianHierarchy(
        level3_state="West Bengal", level4_region="Colonial Bengal", level5_cuisine="Bengali",
        level6_food_family="Meat", level7_food_type="Dak Bungalow", level8_variant="Chicken Dak Bungalow",
        level9_cooking_method=["slow_cooked", "stewed"], default_portion="1 plate with chicken + 1 egg + 1 aloo (300g)",
        nutrition_ref_id="wb_meat_dak_bungalow_chicken"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="WB_MEAT_MUTTON_REZALA",
    canonical_name="Mutton Rezala",
    state="West Bengal",
    region="Kolkata Mughlai",
    cuisine="Bengali",
    food_category="Meat",
    regional_names={"English": "Kolkata Awadhi-Bengali White Mutton Curry", "Bengali": "মটন রেজালা", "Hindi": "मटन रज़ाला"},
    alternate_names=["kolkata rezala", "mutton rezala"],
    vegetarian=False,
    gravy_type="curd_broth",
    visual_features={"gravy": "fragrant_pale_white_yogurt_cashew_poppy_gravy", "garnishes": ["whole_dried_red_chillies", "foxnuts (makhana)", "kewra_aroma_sheen"]},
    key_ingredients=["mutton pieces", "whisked curd", "cashew paste", "poppy seed (posto) paste", "kewra water", "whole red chillies", "makhana", "ghee"],
    hard_negatives=["WB_MEAT_KOSHA_MANGSHO", "WB_MEAT_MUTTON_JHOL"],
    density_g_cm3=1.01,
    default_serving_weight_g=250.0,
    nutrition_per_100g={"calories": 240.0, "protein_g": 14.8, "carbs_g": 4.8, "fat_g": 17.5, "fiber_g": 0.8, "sodium_mg": 320.0},
    hierarchy=EastIndianHierarchy(
        level3_state="West Bengal", level4_region="Kolkata Mughlai", level5_cuisine="Bengali",
        level6_food_family="Meat", level7_food_type="Rezala", level8_variant="Kolkata Mutton Rezala",
        level9_cooking_method=["slow_cooked", "curd_simmered"], default_portion="1 bowl (250g)",
        nutrition_ref_id="wb_meat_mutton_rezala"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="WB_EGG_DIM_KOSHA",
    canonical_name="Dim Kosha",
    state="West Bengal",
    region="Kolkata",
    cuisine="Bengali",
    food_category="Meat",
    regional_names={"English": "Bengali Spiced Egg Roast", "Bengali": "ডিম কষা", "Hindi": "डिम कशा"},
    alternate_names=["bengali egg curry", "dim-er dalna", "dim kosha"],
    vegetarian=False,
    gravy_type="semi_gravy",
    visual_features={"egg": "boiled_eggs_with_deep_fried_blistered_golden_skin", "gravy": "thick_spicy_red_brown_onion_tomato_masala"},
    key_ingredients=["poultry eggs boiled and deep-fried", "onions", "ginger garlic", "tomato", "mustard oil", "garam masala"],
    density_g_cm3=1.02,
    default_serving_weight_g=180.0,
    nutrition_per_100g={"calories": 170.0, "protein_g": 10.2, "carbs_g": 4.8, "fat_g": 12.0, "fiber_g": 0.9, "sodium_mg": 310.0},
    hierarchy=EastIndianHierarchy(
        level3_state="West Bengal", level4_region="Kolkata", level5_cuisine="Bengali",
        level6_food_family="Meat", level7_food_type="Egg Kosha", level8_variant="Dim Kosha",
        level9_cooking_method=["deep_fried_eggs", "bhuna"], default_portion="2 eggs with thick gravy (180g)",
        nutrition_ref_id="wb_egg_dim_kosha"
    )
))

# =============================================================================
# 4. WEST BENGAL: VEGETARIAN MASTER DATASET (Section 6)
# =============================================================================

register_east_food(EastIndianFoodClass(
    canonical_food_id="WB_VEG_ALOO_POSTO",
    canonical_name="Aloo Posto",
    state="West Bengal",
    region="Rarh Bengal",
    cuisine="Bengali",
    food_category="Vegetarian",
    regional_names={"English": "Potatoes in Poppy Seed Paste", "Bengali": "আলু পোস্ত", "Hindi": "आलू पोस्तो"},
    alternate_names=["bengali aloo posto", "posto aloo"],
    vegetarian=True,
    gravy_type="semi_gravy",
    visual_features={"texture": "creamy_granular_pale_beige_poppy_seed_coating", "potatoes": "cubed_soft_potatoes", "garnishes": ["raw_pungent_mustard_oil_drizzle", "slit_green_chillies"], "kalo_jeere": "black_nigella_seeds_scattered"},
    key_ingredients=["potatoes cubed", "poppy seed (posto / khashkhash) paste", "kalo jeere (nigella seeds)", "green chillies", "raw mustard oil", "turmeric (very subtle or none)", "salt"],
    hard_negatives=["WB_VEG_JHINGE_POSTO", "WB_VEG_POTOL_POSTO"],
    density_g_cm3=0.92,
    default_serving_weight_g=180.0,
    nutrition_per_100g={"calories": 170.0, "protein_g": 3.8, "carbs_g": 18.2, "fat_g": 9.5, "fiber_g": 2.5, "sodium_mg": 210.0},
    hierarchy=EastIndianHierarchy(
        level3_state="West Bengal", level4_region="Rarh Bengal", level5_cuisine="Bengali",
        level6_food_family="Vegetarian", level7_food_type="Posto", level8_variant="Aloo Posto",
        level9_cooking_method=["sauteed", "posto_paste_simmered"], default_portion="1 bowl (180g)",
        nutrition_ref_id="wb_veg_aloo_posto"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="WB_VEG_JHINGE_POSTO",
    canonical_name="Jhinge Posto",
    state="West Bengal",
    region="Rarh Bengal",
    cuisine="Bengali",
    food_category="Vegetarian",
    regional_names={"English": "Ridge Gourd in Poppy Seed Paste", "Bengali": "ঝিঙে পোস্ত", "Hindi": "झिंगे पोस्तो"},
    alternate_names=["ridge gourd posto", "jhinge aloo posto"],
    vegetarian=True,
    gravy_type="semi_gravy",
    visual_features={"vegetable": "soft_translucent_cut_ridge_gourd_chunks", "coating": "creamy_granular_white_poppy_paste"},
    key_ingredients=["ridge gourd (jhinge)", "poppy seed paste", "kalo jeere", "green chillies", "mustard oil", "salt"],
    density_g_cm3=0.94,
    default_serving_weight_g=180.0,
    nutrition_per_100g={"calories": 120.0, "protein_g": 2.8, "carbs_g": 8.5, "fat_g": 8.2, "fiber_g": 2.0, "sodium_mg": 190.0},
    hierarchy=EastIndianHierarchy(
        level3_state="West Bengal", level4_region="Rarh Bengal", level5_cuisine="Bengali",
        level6_food_family="Vegetarian", level7_food_type="Posto", level8_variant="Jhinge Posto",
        level9_cooking_method=["sauteed"], default_portion="1 bowl (180g)",
        nutrition_ref_id="wb_veg_jhinge_posto"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="WB_VEG_POTOL_POSTO",
    canonical_name="Potol Posto",
    state="West Bengal",
    region="Rarh Bengal",
    cuisine="Bengali",
    food_category="Vegetarian",
    regional_names={"English": "Pointed Gourd in Poppy Seed Paste", "Bengali": "পটল পোস্ত", "Hindi": "परवल पोस्तो"},
    alternate_names=["parwal posto", "potol posto"],
    vegetarian=True,
    gravy_type="semi_gravy",
    visual_features={"vegetable": "slit_golden_shallow_fried_pointed_gourd (potol)", "coating": "beige_poppy_paste"},
    key_ingredients=["pointed gourd (potol)", "poppy seed paste", "mustard oil", "kalo jeere", "green chillies"],
    density_g_cm3=0.93,
    default_serving_weight_g=180.0,
    nutrition_per_100g={"calories": 135.0, "protein_g": 3.0, "carbs_g": 9.5, "fat_g": 9.2, "fiber_g": 2.2, "sodium_mg": 200.0},
    hierarchy=EastIndianHierarchy(
        level3_state="West Bengal", level4_region="Rarh Bengal", level5_cuisine="Bengali",
        level6_food_family="Vegetarian", level7_food_type="Posto", level8_variant="Potol Posto",
        level9_cooking_method=["shallow_fried", "sauteed"], default_portion="1 bowl (180g)",
        nutrition_ref_id="wb_veg_potol_posto"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="WB_VEG_SHUKTO",
    canonical_name="Shukto",
    state="West Bengal",
    region="Kolkata",
    cuisine="Bengali",
    food_category="Vegetarian",
    regional_names={"English": "Bengali Bitter-Sweet Mixed Vegetable Stew", "Bengali": "শুক্তো", "Hindi": "शुक्तो"},
    alternate_names=["dudh shukto", "bengali shukto", "traditional shukto"],
    vegetarian=True,
    gravy_type="semi_gravy",
    visual_features={"gravy": "milky_white_or_pale_yellowish_herbaceous_broth", "distinctive_vegetables": ["bitter_gourd (karola)", "raw_banana (kanchkola)", "drumstick (sojne danta)", "sweet_potato (ranga aloo)", "white_radish (mulo)", "crispy_lentil_dumplings (bori)"], "spice": "radhuni_and_ginger_paste_aroma"},
    key_ingredients=["bitter gourd", "raw banana", "sweet potato", "drumstick", "radish", "fried bori (dal dumplings)", "milk", "radhuni (wild celery seed) paste", "ginger paste", "ghee", "panch phoron", "mustard oil"],
    hard_negatives=["WB_VEG_CHORCHORI", "WB_VEG_LABRA"],
    density_g_cm3=0.95,
    default_serving_weight_g=200.0,
    nutrition_per_100g={"calories": 95.0, "protein_g": 2.8, "carbs_g": 13.5, "fat_g": 3.5, "fiber_g": 2.8, "sodium_mg": 180.0},
    hierarchy=EastIndianHierarchy(
        level3_state="West Bengal", level4_region="Kolkata", level5_cuisine="Bengali",
        level6_food_family="Vegetarian", level7_food_type="Shukto", level8_variant="Dudh Shukto with Bori",
        level9_cooking_method=["stewed", "milk_simmered", "ghee_tempered"], default_portion="1 bowl (200g)",
        nutrition_ref_id="wb_veg_shukto"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="WB_VEG_CHORCHORI",
    canonical_name="Chorchori",
    state="West Bengal",
    region="Kolkata",
    cuisine="Bengali",
    food_category="Vegetarian",
    regional_names={"English": "Bengali Charred Mixed Vegetable Medley with Mustard", "Bengali": "চচ্চড়ি", "Hindi": "चड़चड़ी"},
    alternate_names=["pui saag chorchori", "sobji chorchori", "chorchori"],
    vegetarian=True,
    gravy_type="semi_gravy",
    visual_features={"texture": "slightly_charred_dry_mixed_vegetable_batons", "coating": "pungent_mustard_paste_film", "visible": ["broad_beans (sheem)", "eggplant", "pumpkin", "potatoes", "mustard_seeds"]},
    key_ingredients=["potatoes", "eggplant", "pumpkin", "sheem (flat beans)", "mustard paste", "panch phoron", "green chillies", "mustard oil"],
    density_g_cm3=0.91,
    default_serving_weight_g=180.0,
    nutrition_per_100g={"calories": 115.0, "protein_g": 2.5, "carbs_g": 14.2, "fat_g": 5.5, "fiber_g": 3.1, "sodium_mg": 190.0},
    hierarchy=EastIndianHierarchy(
        level3_state="West Bengal", level4_region="Kolkata", level5_cuisine="Bengali",
        level6_food_family="Vegetarian", level7_food_type="Chorchori", level8_variant="Sobji Chorchori",
        level9_cooking_method=["charred_pan_braised"], default_portion="1 bowl (180g)",
        nutrition_ref_id="wb_veg_chorchori"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="WB_VEG_LABRA",
    canonical_name="Labra",
    state="West Bengal",
    region="Kolkata",
    cuisine="Bengali",
    food_category="Vegetarian",
    regional_names={"English": "Bengali Temple-Style Slow Cooked Vegetable Mash", "Bengali": "লাবড়া", "Hindi": "लाबड़ा"},
    alternate_names=["bhoger labra", "mishit labra"],
    vegetarian=True,
    gravy_type="semi_gravy",
    visual_features={"texture": "soft_melded_comforting_vegetable_mash", "color": "dark_amber_brown", "visible": ["pumpkin", "eggplant", "sweet_potato", "cabbage", "radish"]},
    key_ingredients=["pumpkin", "eggplant", "potatoes", "sweet potatoes", "radish", "panch phoron", "ginger", "ghee", "sugar", "roasted cumin powder"],
    density_g_cm3=0.94,
    default_serving_weight_g=200.0,
    nutrition_per_100g={"calories": 110.0, "protein_g": 2.2, "carbs_g": 16.5, "fat_g": 4.2, "fiber_g": 3.2, "sodium_mg": 180.0},
    hierarchy=EastIndianHierarchy(
        level3_state="West Bengal", level4_region="Kolkata", level5_cuisine="Bengali",
        level6_food_family="Vegetarian", level7_food_type="Labra", level8_variant="Bhoger Labra",
        level9_cooking_method=["slow_cooked_mash"], default_portion="1 bowl (200g)",
        nutrition_ref_id="wb_veg_labra"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="WB_VEG_BEGUN_BHAJA",
    canonical_name="Begun Bhaja",
    state="West Bengal",
    region="Kolkata",
    cuisine="Bengali",
    food_category="Vegetarian",
    regional_names={"English": "Pan Fried Eggplant Slices in Mustard Oil", "Bengali": "বেগুন ভাজা", "Hindi": "बैंगन भाजा"},
    alternate_names=["fried eggplant", "baingan bhaja"],
    vegetarian=True,
    gravy_type="dry",
    visual_features={"shape": "round_thick_disc_or_lengthwise_sliced_eggplant", "crust": "golden_brown_blistered_turmeric_salt_crust", "sheen": "glistening_mustard_oil"},
    key_ingredients=["large purple eggplant roundels", "turmeric powder", "salt", "sugar sprinkle", "pure mustard oil", "rice flour optional for crispness"],
    hard_negatives=["WB_STREET_BEGUNI", "OD_VEG_BAIGANA_BHAJA"],
    density_g_cm3=0.88,
    default_serving_weight_g=120.0,
    nutrition_per_100g={"calories": 155.0, "protein_g": 1.8, "carbs_g": 9.2, "fat_g": 12.8, "fiber_g": 3.2, "sodium_mg": 210.0},
    hierarchy=EastIndianHierarchy(
        level3_state="West Bengal", level4_region="Kolkata", level5_cuisine="Bengali",
        level6_food_family="Vegetarian", level7_food_type="Bhaja", level8_variant="Begun Bhaja",
        level9_cooking_method=["mustard_oil_shallow_fried"], default_portion="2 round slices (120g)",
        nutrition_ref_id="wb_veg_begun_bhaja"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="WB_VEG_ALOO_BHAJA",
    canonical_name="Jhuri Aloo Bhaja",
    state="West Bengal",
    region="Kolkata",
    cuisine="Bengali",
    food_category="Vegetarian",
    regional_names={"English": "Crisp Matchstick Fried Potatoes with Peanuts", "Bengali": "ঝুড়ি আলু ভাজা", "Hindi": "झुरी आलू भाजा"},
    alternate_names=["aloo bhaja", "jhuri aloo bhaja", "crisp matchstick potatoes"],
    vegetarian=True,
    gravy_type="dry",
    visual_features={"texture": "ultra_fine_crispy_golden_yellow_potato_threads", "garnishes": ["fried_peanuts", "crisp_curry_leaves"]},
    key_ingredients=["potatoes grated into matchsticks", "turmeric", "salt", "mustard oil or refined oil", "fried peanuts"],
    density_g_cm3=0.65,
    default_serving_weight_g=60.0,
    nutrition_per_100g={"calories": 420.0, "protein_g": 4.5, "carbs_g": 48.0, "fat_g": 24.0, "fiber_g": 3.5, "sodium_mg": 290.0},
    hierarchy=EastIndianHierarchy(
        level3_state="West Bengal", level4_region="Kolkata", level5_cuisine="Bengali",
        level6_food_family="Vegetarian", level7_food_type="Bhaja", level8_variant="Jhuri Aloo Bhaja",
        level9_cooking_method=["deep_fried"], default_portion="1 bowl (60g)",
        nutrition_ref_id="wb_veg_aloo_bhaja"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="WB_VEG_CHANAR_DALNA",
    canonical_name="Chanar Dalna",
    state="West Bengal",
    region="Kolkata",
    cuisine="Bengali",
    food_category="Vegetarian",
    regional_names={"English": "Fresh Cottage Cheese Kofta Curry with Potatoes", "Bengali": "ছানার ডালনা", "Hindi": "छेना डलना"},
    alternate_names=["chhena dalna", "paneer dalna bengali"],
    vegetarian=True,
    gravy_type="semi_gravy",
    visual_features={"protein": "golden_fried_delicate_chhana_cakes_or_cubes", "gravy": "fragrant_amber_ginger_cumin_tomato_gravy", "potatoes": "golden_fried_potato_cubes"},
    key_ingredients=["fresh chhana (cottage cheese)", "potatoes", "ginger paste", "cumin powder", "garam masala", "ghee", "bay leaves", "tomatoes"],
    density_g_cm3=1.01,
    default_serving_weight_g=220.0,
    nutrition_per_100g={"calories": 175.0, "protein_g": 8.5, "carbs_g": 10.2, "fat_g": 11.5, "fiber_g": 1.2, "sodium_mg": 260.0},
    hierarchy=EastIndianHierarchy(
        level3_state="West Bengal", level4_region="Kolkata", level5_cuisine="Bengali",
        level6_food_family="Vegetarian", level7_food_type="Dalna", level8_variant="Chanar Dalna",
        level9_cooking_method=["shallow_fried_chhana", "simmered_gravy"], default_portion="1 bowl with 3 chhana cakes (220g)",
        nutrition_ref_id="wb_veg_chanar_dalna"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="WB_VEG_DHOKAR_DALNA",
    canonical_name="Dhokar Dalna",
    state="West Bengal",
    region="Kolkata",
    cuisine="Bengali",
    food_category="Vegetarian",
    regional_names={"English": "Bengali Fried Lentil Cake Curry", "Bengali": "ধোঁকার ডালনা", "Hindi": "धोका डलना"},
    alternate_names=["dhoka dalna", "chana dal cake curry"],
    vegetarian=True,
    gravy_type="semi_gravy",
    visual_features={"dhoka": "distinct_diamond_shaped_fried_yellow_lentil_cakes", "gravy": "rich_ginger_cumin_hing_scented_gravy", "potatoes": "fried_potato_wedges"},
    key_ingredients=["chana dal paste", "hing (asafoetida)", "ginger", "potatoes", "cumin powder", "mustard oil", "ghee", "green chillies"],
    hard_negatives=["WB_VEG_CHANAR_DALNA", "GJ_FARSAN_DHOKLA_KHAMAN"],
    density_g_cm3=1.02,
    default_serving_weight_g=230.0,
    nutrition_per_100g={"calories": 190.0, "protein_g": 7.8, "carbs_g": 16.5, "fat_g": 10.5, "fiber_g": 3.0, "sodium_mg": 270.0},
    hierarchy=EastIndianHierarchy(
        level3_state="West Bengal", level4_region="Kolkata", level5_cuisine="Bengali",
        level6_food_family="Vegetarian", level7_food_type="Dalna", level8_variant="Dhokar Dalna",
        level9_cooking_method=["steamed_fried_lentil_cakes", "simmered_gravy"], default_portion="3 diamond cakes with gravy (230g)",
        nutrition_ref_id="wb_veg_dhokar_dalna"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="WB_VEG_MOCHAR_GHONTO",
    canonical_name="Mochar Ghonto",
    state="West Bengal",
    region="Kolkata",
    cuisine="Bengali",
    food_category="Vegetarian",
    regional_names={"English": "Spiced Banana Blossom Dry Curry with Coconut", "Bengali": "মোচার ঘণ্ট", "Hindi": "मोचा घंटो"},
    alternate_names=["mocha ghonto", "banana flower curry"],
    vegetarian=True,
    gravy_type="dry",
    visual_features={"texture": "dark_brown_finely_chopped_cooked_banana_florets", "garnishes": ["fried_coconut_slivers", "boiled_black_chana", "ghee_sheen"]},
    key_ingredients=["banana blossom (mocha) cleaned and chopped", "grated coconut and fried coconut bits", "boiled black chickpeas (kala chana)", "potatoes", "cumin", "ginger", "ghee", "garam masala"],
    density_g_cm3=0.92,
    default_serving_weight_g=180.0,
    nutrition_per_100g={"calories": 130.0, "protein_g": 3.4, "carbs_g": 14.8, "fat_g": 6.8, "fiber_g": 5.2, "sodium_mg": 210.0},
    hierarchy=EastIndianHierarchy(
        level3_state="West Bengal", level4_region="Kolkata", level5_cuisine="Bengali",
        level6_food_family="Vegetarian", level7_food_type="Ghonto", level8_variant="Mochar Ghonto",
        level9_cooking_method=["boiled", "ghee_sauteed_slow"], default_portion="1 bowl (180g)",
        nutrition_ref_id="wb_veg_mochar_ghonto"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="WB_VEG_ECHORER_DALNA",
    canonical_name="Echorer Dalna",
    state="West Bengal",
    region="Kolkata",
    cuisine="Bengali",
    food_category="Vegetarian",
    regional_names={"English": "Bengali Green Raw Jackfruit Curry", "Bengali": "এঁচোড়ের ডালনা (গাছ পাঁঠা)", "Hindi": "कटहल की सब्ज़ी"},
    alternate_names=["enchor dalna", "gachh patha", "raw jackfruit curry"],
    vegetarian=True,
    gravy_type="semi_gravy",
    visual_features={"texture": "fibrous_meat_like_jackfruit_chunks", "potatoes": "golden_fried_potatoes", "gravy": "rich_aromatic_red_brown_onion_garlic_gravy"},
    key_ingredients=["raw green tender jackfruit (echor)", "potatoes", "onions", "ginger garlic", "garam masala", "mustard oil", "bay leaves"],
    density_g_cm3=0.98,
    default_serving_weight_g=220.0,
    nutrition_per_100g={"calories": 135.0, "protein_g": 3.2, "carbs_g": 17.5, "fat_g": 6.2, "fiber_g": 4.5, "sodium_mg": 250.0},
    hierarchy=EastIndianHierarchy(
        level3_state="West Bengal", level4_region="Kolkata", level5_cuisine="Bengali",
        level6_food_family="Vegetarian", level7_food_type="Dalna", level8_variant="Echorer Dalna",
        level9_cooking_method=["boiled", "mustard_oil_kasha"], default_portion="1 bowl (220g)",
        nutrition_ref_id="wb_veg_echorer_dalna"
    )
))

# =============================================================================
# 5. WEST BENGAL: DAL MASTER DATASET (Section 7)
# =============================================================================

register_east_food(EastIndianFoodClass(
    canonical_food_id="WB_DAL_CHOLAR_DAL",
    canonical_name="Cholar Dal",
    state="West Bengal",
    region="Kolkata",
    cuisine="Bengali",
    food_category="Dal",
    regional_names={"English": "Bengali Chana Dal with Coconut & Raisins", "Bengali": "ছোলার ডাল নারকেল দিয়ে", "Hindi": "छोलार दाल"},
    alternate_names=["bengali chana dal", "narkel cholar dal"],
    vegetarian=True,
    gravy_type="dal_stew",
    visual_features={"lentils": "chunky_intact_yellow_bengal_gram", "distinctive_toppings": ["fried_crunchy_coconut_bits (narkel bhaja)", "golden_raisins", "whole_dried_red_chillies", "bay_leaf", "ghee_film"], "aroma": "hing_ginger_garam_masala"},
    key_ingredients=["chana dal (bengal gram)", "fried coconut pieces", "raisins", "hing (asafoetida)", "ginger paste", "ghee", "cumin seeds", "cinnamon", "cardamom", "sugar hint"],
    hard_negatives=["WB_DAL_MUSUR_DAL", "WB_DAL_MOONG_DAL", "OD_DAL_DALMA"],
    density_g_cm3=1.04,
    default_serving_weight_g=180.0,
    nutrition_per_100g={"calories": 165.0, "protein_g": 7.5, "carbs_g": 20.8, "fat_g": 6.2, "fiber_g": 4.5, "sodium_mg": 210.0},
    hierarchy=EastIndianHierarchy(
        level3_state="West Bengal", level4_region="Kolkata", level5_cuisine="Bengali",
        level6_food_family="Dal", level7_food_type="Cholar Dal", level8_variant="Cholar Dal with Coconut",
        level9_cooking_method=["pressure_cooked", "ghee_tempered"], default_portion="1 katori (180g)",
        nutrition_ref_id="wb_dal_cholar_dal"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="WB_DAL_MUSUR_DAL",
    canonical_name="Musur Dal",
    state="West Bengal",
    region="Kolkata",
    cuisine="Bengali",
    food_category="Dal",
    regional_names={"English": "Red Lentil Dal with Onion and Nigella", "Bengali": "মুসুর ডাল", "Hindi": "मसूर दाल"},
    alternate_names=["masoor dal bengali", "peyaj diye musur dal"],
    vegetarian=True,
    gravy_type="dal_stew",
    visual_features={"soup": "thin_golden_orange_pureed_red_lentils", "tempering": ["fried_sliced_onions (peyaj)", "kalo_jeere", "green_chillies"]},
    key_ingredients=["red lentils (musur dal)", "sliced onions", "kalo jeere", "green chillies", "turmeric", "mustard oil"],
    density_g_cm3=1.02,
    default_serving_weight_g=180.0,
    nutrition_per_100g={"calories": 110.0, "protein_g": 6.8, "carbs_g": 15.2, "fat_g": 2.8, "fiber_g": 3.2, "sodium_mg": 190.0},
    hierarchy=EastIndianHierarchy(
        level3_state="West Bengal", level4_region="Kolkata", level5_cuisine="Bengali",
        level6_food_family="Dal", level7_food_type="Musur Dal", level8_variant="Peyaj Diye Musur Dal",
        level9_cooking_method=["boiled", "mustard_tempered"], default_portion="1 katori (180g)",
        nutrition_ref_id="wb_dal_musur_dal"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="WB_DAL_BHAJA_MOONG_DAL",
    canonical_name="Bhaja Moong Dal",
    state="West Bengal",
    region="Kolkata",
    cuisine="Bengali",
    food_category="Dal",
    regional_names={"English": "Roasted Yellow Moong Dal with Peas", "Bengali": "ভাজা মুগের ডাল", "Hindi": "भाजा मूंग दाल"},
    alternate_names=["roasted moong dal", "sobji diye moong dal"],
    vegetarian=True,
    gravy_type="dal_stew",
    visual_features={"color": "warm_golden_yellow", "visible": ["green_peas", "cauliflower_florets_optional", "ginger_bits", "ghee"]},
    key_ingredients=["dry roasted yellow moong dal", "green peas", "ginger", "cumin seeds", "ghee", "bay leaf"],
    density_g_cm3=1.03,
    default_serving_weight_g=180.0,
    nutrition_per_100g={"calories": 125.0, "protein_g": 7.2, "carbs_g": 16.5, "fat_g": 3.8, "fiber_g": 3.4, "sodium_mg": 195.0},
    hierarchy=EastIndianHierarchy(
        level3_state="West Bengal", level4_region="Kolkata", level5_cuisine="Bengali",
        level6_food_family="Dal", level7_food_type="Moong Dal", level8_variant="Bhaja Moong Dal",
        level9_cooking_method=["roasted", "boiled", "ghee_tempered"], default_portion="1 katori (180g)",
        nutrition_ref_id="wb_dal_bhaja_moong_dal"
    )
))

# =============================================================================
# 6. WEST BENGAL: BREAKFAST, BREADS & COMBINATIONS (Section 8)
# =============================================================================

register_east_food(EastIndianFoodClass(
    canonical_food_id="WB_BREAD_LUCHI",
    canonical_name="Luchi",
    state="West Bengal",
    region="Kolkata",
    cuisine="Bengali",
    food_category="Breakfast",
    regional_names={"English": "Bengali Deep-Fried Puffed White Flour Bread", "Bengali": "লুচি", "Hindi": "लुची"},
    alternate_names=["maida puri", "bengali luchi"],
    vegetarian=True,
    gravy_type="dry",
    visual_features={"color": "pale_white_to_ivory_not_golden_brown", "shape": "thin_puffed_spherical_hollow_disc", "surface": "delicate_soft_paper_thin_crisp_crust_without_blisters"},
    key_ingredients=["refined all-purpose flour (maida)", "ghee or refined oil for moyan (shortening)", "warm water", "oil for deep frying"],
    hard_negatives=["NI_BREAD_PURI_WHEAT", "WB_BREAD_KOCHURI", "BR_BREAD_LITTI"],
    density_g_cm3=0.45,
    default_serving_weight_g=30.0,
    nutrition_per_100g={"calories": 360.0, "protein_g": 6.5, "carbs_g": 48.0, "fat_g": 16.5, "fiber_g": 1.2, "sodium_mg": 190.0},
    hierarchy=EastIndianHierarchy(
        level3_state="West Bengal", level4_region="Kolkata", level5_cuisine="Bengali",
        level6_food_family="Breakfast", level7_food_type="Deep Fried Bread", level8_variant="Luchi",
        level9_cooking_method=["deep_fried"], default_portion="4 pieces (120g)",
        nutrition_ref_id="wb_bread_luchi"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="WB_CURRY_ALUR_DOM",
    canonical_name="Bengali Alur Dom",
    state="West Bengal",
    region="Kolkata",
    cuisine="Bengali",
    food_category="Breakfast",
    regional_names={"English": "Bengali Spiced Baby Potato Curry", "Bengali": "আলুর দম", "Hindi": "आलुर दम"},
    alternate_names=["alur dom", "dum aloo bengali", "luchi alur dom curry"],
    vegetarian=True,
    gravy_type="semi_gravy",
    visual_features={"potato": "whole_tender_baby_potatoes_fork_pricked", "gravy": "thick_spicy_tangy_tomato_ginger_cumin_masala", "garnishes": ["green_peas", "fresh_coriander"]},
    key_ingredients=["baby potatoes", "tomato puree", "ginger paste", "hing", "cumin", "kashmiri red chilli", "mustard oil", "garam masala", "green peas"],
    hard_negatives=["NI_CURRY_ALOO_DUM_KASHMIRI", "OD_CURRY_ALOO_DUM"],
    density_g_cm3=0.98,
    default_serving_weight_g=180.0,
    nutrition_per_100g={"calories": 140.0, "protein_g": 2.8, "carbs_g": 19.5, "fat_g": 5.8, "fiber_g": 2.5, "sodium_mg": 280.0},
    hierarchy=EastIndianHierarchy(
        level3_state="West Bengal", level4_region="Kolkata", level5_cuisine="Bengali",
        level6_food_family="Breakfast", level7_food_type="Potato Curry", level8_variant="Alur Dom",
        level9_cooking_method=["fried_potatoes", "simmered_gravy"], default_portion="1 bowl (180g)",
        nutrition_ref_id="wb_curry_alur_dom"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="WB_BREAD_RADHA_BALLAVI",
    canonical_name="Radha Ballavi",
    state="West Bengal",
    region="Kolkata",
    cuisine="Bengali",
    food_category="Breakfast",
    regional_names={"English": "Spiced Urad Dal Stuffed Bengali Puffed Bread", "Bengali": "রাধাবল্লভী", "Hindi": "राधाबल्लभी"},
    alternate_names=["radhaballabhi", "radhaballavi"],
    vegetarian=True,
    gravy_type="dry",
    visual_features={"shape": "larger_puffed_bread_slightly_heavier_than_luchi", "filling": "inner_layer_of_dark_spiced_urad_dal_paste_scented_with_fennel_and_hing"},
    key_ingredients=["maida", "urad dal paste (biuli dal)", "mouri (fennel seed) paste", "ginger paste", "hing", "mustard oil or ghee for frying"],
    hard_negatives=["WB_BREAD_LUCHI", "WB_BREAD_KOCHURI", "NI_BREAD_KACHORI"],
    density_g_cm3=0.52,
    default_serving_weight_g=55.0,
    nutrition_per_100g={"calories": 330.0, "protein_g": 8.5, "carbs_g": 46.0, "fat_g": 13.5, "fiber_g": 2.8, "sodium_mg": 240.0},
    hierarchy=EastIndianHierarchy(
        level3_state="West Bengal", level4_region="Kolkata", level5_cuisine="Bengali",
        level6_food_family="Breakfast", level7_food_type="Stuffed Fried Bread", level8_variant="Radhaballabhi",
        level9_cooking_method=["stuffed", "deep_fried"], default_portion="2 pieces (110g)",
        nutrition_ref_id="wb_bread_radha_ballavi"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="WB_BREAD_KOCHURI",
    canonical_name="Koraishutir Kochuri",
    state="West Bengal",
    region="Kolkata",
    cuisine="Bengali",
    food_category="Breakfast",
    regional_names={"English": "Green Peas Stuffed Bengali Kachori", "Bengali": "কড়াইশুঁটির কচুরি", "Hindi": "कढ़ाईशुटीर कचोरी"},
    alternate_names=["peas kochuri", "koraishuti kochuri", "bengali kachori"],
    vegetarian=True,
    gravy_type="dry",
    visual_features={"color": "pale_green_hint_showing_through_thin_white_crust", "filling": "sweet_spicy_green_pea_mash_scented_with_hing_and_ginger"},
    key_ingredients=["fresh green peas paste", "hing", "ginger", "fennel", "maida", "ghee"],
    hard_negatives=["WB_BREAD_LUCHI", "NI_BREAD_KACHORI"],
    density_g_cm3=0.55,
    default_serving_weight_g=50.0,
    nutrition_per_100g={"calories": 310.0, "protein_g": 7.2, "carbs_g": 44.0, "fat_g": 12.0, "fiber_g": 3.2, "sodium_mg": 220.0},
    hierarchy=EastIndianHierarchy(
        level3_state="West Bengal", level4_region="Kolkata", level5_cuisine="Bengali",
        level6_food_family="Breakfast", level7_food_type="Stuffed Fried Bread", level8_variant="Koraishutir Kochuri",
        level9_cooking_method=["stuffed", "deep_fried"], default_portion="3 pieces (150g)",
        nutrition_ref_id="wb_bread_kochuri"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="WB_CURRY_GHUGNI",
    canonical_name="Ghugni",
    state="West Bengal",
    region="Kolkata",
    cuisine="Bengali",
    food_category="Street Food",
    regional_names={"English": "Bengali Yellow Dried Pea Curry", "Bengali": "ঘুগনি", "Odia": "ଘୁଗୁନି", "Hindi": "घुघनी"},
    alternate_names=["matar ghugni", "bengali ghugni"],
    vegetarian=True,
    gravy_type="semi_gravy",
    visual_features={"lentils": "whole_tender_yellow_dried_peas (motor)", "garnishes": ["chopped_raw_onions", "green_chillies", "fried_coconut_bits", "fresh_coriander", "bhaja_moshla (roasted spice powder)", "tamarind_water_drizzle"]},
    key_ingredients=["yellow dried peas (motor)", "onions", "ginger garlic", "bhaja moshla (cumin-coriander-dry chilli roasted powder)", "coconut bits", "tamarind", "mustard oil"],
    hard_negatives=["NI_CURRY_CHOLE_PUNJABI", "OD_STREET_DAHIBARA_ALOODUM"],
    density_g_cm3=1.02,
    default_serving_weight_g=200.0,
    nutrition_per_100g={"calories": 135.0, "protein_g": 6.8, "carbs_g": 21.5, "fat_g": 3.2, "fiber_g": 5.2, "sodium_mg": 280.0},
    hierarchy=EastIndianHierarchy(
        level3_state="West Bengal", level4_region="Kolkata", level5_cuisine="Bengali",
        level6_food_family="Street Food", level7_food_type="Ghugni", level8_variant="Yellow Motor Ghugni",
        level9_cooking_method=["boiled", "tempered_spiced"], default_portion="1 bowl (200g)",
        nutrition_ref_id="wb_curry_ghugni"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="WB_SNACK_BENGALI_SINGARA",
    canonical_name="Bengali Singara",
    state="West Bengal",
    region="Kolkata",
    cuisine="Bengali",
    food_category="Street Food",
    regional_names={"English": "Bengali Cauliflower & Potato Samosa", "Bengali": "সিঙাড়া", "Hindi": "सिंगाड़ा"},
    alternate_names=["kolkata singara", "phulkopir singara"],
    vegetarian=True,
    gravy_type="dry",
    visual_features={"shape": "distinctive_tetrahedral_pyramid_with_thin_flaky_crust", "filling": "diced_potatoes_with_tender_cauliflower_florets_roasted_peanuts_and_panch_phoron"},
    key_ingredients=["flaky maida crust with kalonji", "diced potatoes", "cauliflower florets", "fried peanuts", "panch phoron", "ginger", "green chillies"],
    hard_negatives=["NI_SNACK_SAMOSA_PUNJABI"],
    density_g_cm3=0.72,
    default_serving_weight_g=65.0,
    nutrition_per_100g={"calories": 285.0, "protein_g": 4.5, "carbs_g": 34.0, "fat_g": 14.8, "fiber_g": 2.4, "sodium_mg": 260.0},
    hierarchy=EastIndianHierarchy(
        level3_state="West Bengal", level4_region="Kolkata", level5_cuisine="Bengali",
        level6_food_family="Street Food", level7_food_type="Singara", level8_variant="Kolkata Singara",
        level9_cooking_method=["deep_fried_slow"], default_portion="2 pieces (130g)",
        nutrition_ref_id="wb_snack_bengali_singara"
    )
))

# =============================================================================
# 7. WEST BENGAL: STREET FOOD, KATHI ROLLS & JHALMURI (Sections 9, 10, 11)
# =============================================================================

register_east_food(EastIndianFoodClass(
    canonical_food_id="WB_STREET_KATHI_ROLL_EGG_CHICKEN",
    canonical_name="Double Egg Chicken Kathi Roll",
    state="West Bengal",
    region="Kolkata",
    cuisine="Bengali",
    food_category="Street Food",
    regional_names={"English": "Kolkata Double Egg Chicken Kathi Roll", "Bengali": "ডাবল এগ চিকেন কাঠি রোল", "Hindi": "कोलकाता काठी रोल"},
    alternate_names=["kolkata chicken roll", "egg chicken roll", "kathi roll"],
    vegetarian=False,
    gravy_type="dry",
    visual_features={"wrapper": "crisp_flaky_paratha_layered_with_beaten_egg", "filling": "chargrilled_spiced_chicken_boti_kebab", "toppings": ["thinly_sliced_raw_onions", "green_chillies", "chaat_masala", "lemon_juice", "kasundi_or_tomato_chilli_sauce", "wrapped_in_paper"]},
    key_ingredients=["maida paratha", "2 eggs", "marinated chicken tikka / kebab", "sliced onions", "green chillies", "lime", "chaat masala", "mustard sauce (kasundi)"],
    hard_negatives=["MUM_STREET_FRANKIE_CHICKEN", "NI_BREAD_CHICKEN_ROLL"],
    density_g_cm3=0.78,
    default_serving_weight_g=230.0,
    nutrition_per_100g={"calories": 245.0, "protein_g": 13.8, "carbs_g": 24.5, "fat_g": 11.2, "fiber_g": 1.4, "sodium_mg": 380.0},
    hierarchy=EastIndianHierarchy(
        level3_state="West Bengal", level4_region="Kolkata", level5_cuisine="Bengali",
        level6_food_family="Street Food", level7_food_type="Kathi Roll", level8_variant="Double Egg Chicken Kathi Roll",
        level9_cooking_method=["tawa_fried_paratha", "pan_roasted_filling"], default_portion="1 roll (230g)",
        nutrition_ref_id="wb_street_kathi_roll_egg_chicken"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="WB_STREET_KATHI_ROLL_EGG",
    canonical_name="Egg Kathi Roll",
    state="West Bengal",
    region="Kolkata",
    cuisine="Bengali",
    food_category="Street Food",
    regional_names={"English": "Kolkata Egg Roll", "Bengali": "এগ রোল", "Hindi": "एग रोल"},
    alternate_names=["kolkata egg roll", "egg roll"],
    vegetarian=False,
    gravy_type="dry",
    visual_features={"wrapper": "flaky_paratha_lined_with_crisp_fried_egg", "filling": "crunchy_onions_chillies_sauce"},
    key_ingredients=["maida paratha", "egg", "sliced onions", "chillies", "chaat masala", "lemon"],
    density_g_cm3=0.76,
    default_serving_weight_g=180.0,
    nutrition_per_100g={"calories": 230.0, "protein_g": 8.5, "carbs_g": 28.0, "fat_g": 10.0, "fiber_g": 1.2, "sodium_mg": 340.0},
    hierarchy=EastIndianHierarchy(
        level3_state="West Bengal", level4_region="Kolkata", level5_cuisine="Bengali",
        level6_food_family="Street Food", level7_food_type="Kathi Roll", level8_variant="Egg Roll",
        level9_cooking_method=["tawa_fried"], default_portion="1 roll (180g)",
        nutrition_ref_id="wb_street_kathi_roll_egg"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="WB_STREET_KATHI_ROLL_MUTTON",
    canonical_name="Mutton Kathi Roll",
    state="West Bengal",
    region="Kolkata",
    cuisine="Bengali",
    food_category="Street Food",
    regional_names={"English": "Kolkata Mutton Kathi Roll", "Bengali": "মটন কাঠি রোল", "Hindi": "मटन काठी रोल"},
    alternate_names=["kolkata mutton roll", "mutton roll"],
    vegetarian=False,
    gravy_type="dry",
    visual_features={"wrapper": "paratha_with_egg_optional", "filling": "tender_spiced_mutton_boti_cubes", "onions": "sliced_onions"},
    key_ingredients=["maida paratha", "spiced mutton boti", "onions", "green chillies", "lime", "chaat masala"],
    density_g_cm3=0.82,
    default_serving_weight_g=230.0,
    nutrition_per_100g={"calories": 265.0, "protein_g": 14.5, "carbs_g": 23.0, "fat_g": 13.5, "fiber_g": 1.3, "sodium_mg": 390.0},
    hierarchy=EastIndianHierarchy(
        level3_state="West Bengal", level4_region="Kolkata", level5_cuisine="Bengali",
        level6_food_family="Street Food", level7_food_type="Kathi Roll", level8_variant="Mutton Kathi Roll",
        level9_cooking_method=["tawa_fried", "roasted"], default_portion="1 roll (230g)",
        nutrition_ref_id="wb_street_kathi_roll_mutton"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="WB_STREET_MUGHLAI_PARATHA",
    canonical_name="Mughlai Paratha",
    state="West Bengal",
    region="Kolkata",
    cuisine="Bengali",
    food_category="Street Food",
    regional_names={"English": "Bengali Stuffed Egg & Minced Meat Square Paratha", "Bengali": "মুঘলাই পরোটা", "Hindi": "मुग़लाई पराठा"},
    alternate_names=["moglai paratha", "kolkata mughlai paratha"],
    vegetarian=False,
    gravy_type="dry",
    visual_features={"shape": "large_golden_crisp_square_folded_envelope", "inside": "beaten_egg_green_chillies_onions_and_minced_chicken_or_mutton", "sides": ["alur dom", "cucumber_onion_salad", "kasundi"]},
    key_ingredients=["maida dough envelope", "eggs", "keema (minced meat) or chopped veggies", "green chillies", "onions", "coriander", "deep shallow fried in oil/ghee"],
    density_g_cm3=0.82,
    default_serving_weight_g=240.0,
    nutrition_per_100g={"calories": 275.0, "protein_g": 10.8, "carbs_g": 26.5, "fat_g": 14.5, "fiber_g": 1.4, "sodium_mg": 360.0},
    hierarchy=EastIndianHierarchy(
        level3_state="West Bengal", level4_region="Kolkata", level5_cuisine="Bengali",
        level6_food_family="Street Food", level7_food_type="Stuffed Paratha", level8_variant="Mughlai Paratha",
        level9_cooking_method=["shallow_fried_pan"], default_portion="1 square cut into 4 pieces (240g)",
        nutrition_ref_id="wb_street_mughlai_paratha"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="WB_STREET_JHALMURI",
    canonical_name="Kolkata Jhalmuri",
    state="West Bengal",
    region="Kolkata",
    cuisine="Bengali",
    food_category="Street Food",
    regional_names={"English": "Spiced Bengali Puffed Rice Street Snack", "Bengali": "ঝালমুড়ি", "Hindi": "झालमुड़ी"},
    alternate_names=["jhal muri", "bengali spicy puffed rice", "kolkata jhalmuri"],
    vegetarian=True,
    gravy_type="dry",
    visual_features={"texture": "tossed_puffed_rice_mix_in_newspaper_cone (thonga)", "visible": ["puffed_rice (muri)", "roasted_peanuts", "chopped_onions", "diced_boiled_potatoes", "fresh_cucumber_bits", "sev_chanachur", "fresh_coconut_slivers", "green_chillies", "coriander", "mustard_oil_sheen"]},
    key_ingredients=["puffed rice (muri)", "chanachur (spicy farsan)", "roasted peanuts", "chopped onions", "boiled potatoes", "green chillies", "raw pungent mustard oil", "special roasted spice powder (bhaja moshla)", "lemon juice"],
    hard_negatives=["MUM_STREET_BHEL_PURI", "BH_SNACK_CHURA"],
    density_g_cm3=0.42,
    default_serving_weight_g=100.0,
    nutrition_per_100g={"calories": 365.0, "protein_g": 7.2, "carbs_g": 56.5, "fat_g": 13.0, "fiber_g": 4.5, "sodium_mg": 410.0},
    hierarchy=EastIndianHierarchy(
        level3_state="West Bengal", level4_region="Kolkata", level5_cuisine="Bengali",
        level6_food_family="Street Food", level7_food_type="Jhalmuri", level8_variant="Kolkata Jhalmuri",
        level9_cooking_method=["raw_mixed", "mustard_oil_dressed"], default_portion="1 thonga cone (100g)",
        nutrition_ref_id="wb_street_jhalmuri"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="WB_STREET_TELEBHAJA_BEGUNI",
    canonical_name="Beguni",
    state="West Bengal",
    region="Kolkata",
    cuisine="Bengali",
    food_category="Street Food",
    regional_names={"English": "Crispy Gram Flour Battered Eggplant Fritters", "Bengali": "বেগুনি", "Hindi": "बेगुनी"},
    alternate_names=["bengali beguni", "telebhaja beguni"],
    vegetarian=True,
    gravy_type="dry",
    visual_features={"shape": "flat_oval_elongated_crisp_fritter", "crust": "golden_yellow_besan_crust_with_kalonji_seeds"},
    key_ingredients=["thin lengthwise eggplant slices", "besan (gram flour)", "kalo jeere", "turmeric", "baking soda", "mustard oil for deep frying"],
    hard_negatives=["WB_VEG_BEGUN_BHAJA", "MH_SNACK_BATATA_VADA"],
    density_g_cm3=0.68,
    default_serving_weight_g=45.0,
    nutrition_per_100g={"calories": 260.0, "protein_g": 6.2, "carbs_g": 24.5, "fat_g": 15.8, "fiber_g": 3.8, "sodium_mg": 280.0},
    hierarchy=EastIndianHierarchy(
        level3_state="West Bengal", level4_region="Kolkata", level5_cuisine="Bengali",
        level6_food_family="Street Food", level7_food_type="Telebhaja", level8_variant="Beguni",
        level9_cooking_method=["batter_coated", "deep_fried"], default_portion="2 pieces (90g)",
        nutrition_ref_id="wb_street_telebhaja_beguni"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="WB_STREET_VEGETABLE_CHOP",
    canonical_name="Vegetable Chop",
    state="West Bengal",
    region="Kolkata",
    cuisine="Bengali",
    food_category="Street Food",
    regional_names={"English": "Bengali Beetroot & Peanut Croquette", "Bengali": "ভেজিটেবল চপ", "Hindi": "वेजिटेबल चॉप"},
    alternate_names=["kolkata veg chop", "beetroot chop"],
    vegetarian=True,
    gravy_type="dry",
    visual_features={"shape": "cylindrical_or_oval_croquette", "inside": "deep_crimson_beetroot_potato_filling_with_crunchy_peanuts", "crust": "crunchy_golden_breadcrumb_coating"},
    key_ingredients=["beetroot", "potatoes", "carrots", "roasted peanuts", "bhaja moshla", "breadcrumbs", "kasundi"],
    density_g_cm3=0.85,
    default_serving_weight_g=100.0,
    nutrition_per_100g={"calories": 220.0, "protein_g": 4.5, "carbs_g": 28.5, "fat_g": 10.2, "fiber_g": 3.5, "sodium_mg": 310.0},
    hierarchy=EastIndianHierarchy(
        level3_state="West Bengal", level4_region="Kolkata", level5_cuisine="Bengali",
        level6_food_family="Street Food", level7_food_type="Chop", level8_variant="Kolkata Vegetable Chop",
        level9_cooking_method=["crumbed", "deep_fried"], default_portion="1 chop (100g)",
        nutrition_ref_id="wb_street_vegetable_chop"
    )
))

# =============================================================================
# 8. WEST BENGAL: SWEETS MASTER DATASET (Sections 12, 13, 14, 15)
# =============================================================================

register_east_food(EastIndianFoodClass(
    canonical_food_id="WB_SWEET_RASGULLA",
    canonical_name="Kolkata Rasgulla",
    state="West Bengal",
    region="Kolkata",
    cuisine="Bengali",
    food_category="Sweets",
    regional_names={"English": "Bengali Spongy Cottage Cheese Ball in Sugar Syrup", "Bengali": "রসগোল্লা (Roshogolla)", "Hindi": "रसगुल्ला"},
    alternate_names=["roshogolla", "bengali rasgulla", "spongy rasgulla"],
    vegetarian=True,
    gravy_type="syrup",
    visual_features={"color": "pristine_pure_snow_white", "shape": "spherical_spongy_porous_chhana_ball", "liquid": "thin_clear_translucent_light_sugar_syrup"},
    key_ingredients=["fresh cow milk chhana (curd cheese)", "semolina (suji) trace", "sugar", "water", "cardamom hint"],
    hard_negatives=["OD_SWEET_RASGULLA", "NI_SWEET_GULAB_JAMUN", "WB_SWEET_RAJBHOG"],
    density_g_cm3=1.08,
    default_serving_weight_g=50.0,
    nutrition_per_100g={"calories": 185.0, "protein_g": 4.2, "carbs_g": 38.5, "fat_g": 2.0, "fiber_g": 0.0, "sodium_mg": 35.0},
    hierarchy=EastIndianHierarchy(
        level3_state="West Bengal", level4_region="Kolkata", level5_cuisine="Bengali",
        level6_food_family="Sweets", level7_food_type="Chhana Sweet", level8_variant="Kolkata Roshogolla",
        level9_cooking_method=["boiled_in_sugar_syrup"], default_portion="2 pieces with syrup (100g)",
        nutrition_ref_id="wb_sweet_rasgulla"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="WB_SWEET_RAJBHOG",
    canonical_name="Rajbhog",
    state="West Bengal",
    region="Kolkata",
    cuisine="Bengali",
    food_category="Sweets",
    regional_names={"English": "Saffron Stuffed Royal Rasgulla", "Bengali": "রাজভোগ", "Hindi": "राजभोग"},
    alternate_names=["kesar rajbhog", "stuffed rasgulla"],
    vegetarian=True,
    gravy_type="syrup",
    visual_features={"color": "vibrant_saffron_yellow", "size": "larger_than_rasgulla", "stuffing": "center_filled_with_almonds_pistachios_cardamom"},
    key_ingredients=["chhana", "saffron", "mava or dry fruit stuffing", "sugar syrup"],
    density_g_cm3=1.10,
    default_serving_weight_g=75.0,
    nutrition_per_100g={"calories": 210.0, "protein_g": 5.2, "carbs_g": 40.0, "fat_g": 3.8, "fiber_g": 0.5, "sodium_mg": 40.0},
    hierarchy=EastIndianHierarchy(
        level3_state="West Bengal", level4_region="Kolkata", level5_cuisine="Bengali",
        level6_food_family="Sweets", level7_food_type="Chhana Sweet", level8_variant="Rajbhog",
        level9_cooking_method=["boiled_in_syrup"], default_portion="1 piece (75g)",
        nutrition_ref_id="wb_sweet_rajbhog"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="WB_SWEET_MISHTI_DOI",
    canonical_name="Mishti Doi",
    state="West Bengal",
    region="Kolkata",
    cuisine="Bengali",
    food_category="Sweets",
    regional_names={"English": "Bengali Caramelized Sweet Fermented Yogurt", "Bengali": "মিষ্টি দই", "Hindi": "मिष्टी दोई"},
    alternate_names=["bengali sweet curd", "red dahi", "lal doi"],
    vegetarian=True,
    gravy_type="curd_broth",
    visual_features={"container": "rustic_earthen_unpainted_clay_pot (matka / bhar)", "color": "pale_caramel_pinkish_light_tan", "texture": "thick_set_creamy_pudding_glossy_surface_without_whey_separation"},
    key_ingredients=["full cream milk reduced slowly", "caramelized sugar / cane sugar", "live yogurt culture", "earthen clay pot porous walls"],
    hard_negatives=["WB_SWEET_BHAPA_DOI", "NI_SWEET_KHEER", "NI_SWEET_RABRI", "DAIRY_PLAIN_YOGURT"],
    density_g_cm3=1.08,
    default_serving_weight_g=150.0,
    nutrition_per_100g={"calories": 160.0, "protein_g": 4.5, "carbs_g": 22.0, "fat_g": 6.2, "fiber_g": 0.0, "sodium_mg": 55.0},
    hierarchy=EastIndianHierarchy(
        level3_state="West Bengal", level4_region="Kolkata", level5_cuisine="Bengali",
        level6_food_family="Sweets", level7_food_type="Fermented Curd", level8_variant="Traditional Caramelized Mishti Doi",
        level9_cooking_method=["slow_reduction", "earthen_pot_fermented"], default_portion="1 clay pot / bhar (150g)",
        nutrition_ref_id="wb_sweet_mishti_doi"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="WB_SWEET_BHAPA_DOI",
    canonical_name="Bhapa Doi",
    state="West Bengal",
    region="Kolkata",
    cuisine="Bengali",
    food_category="Sweets",
    regional_names={"English": "Bengali Steamed Yogurt Cheesecake", "Bengali": "ভাপা দই", "Hindi": "भापा दोई"},
    alternate_names=["steamed mishti doi", "steamed curd"],
    vegetarian=True,
    gravy_type=None,
    visual_features={"texture": "smooth_dense_velvety_sliceable_set_cake", "garnishes": ["pistachio_slivers", "saffron_strands"]},
    key_ingredients=["hung curd", "condensed milk", "cardamom", "saffron", "pistachios"],
    density_g_cm3=1.12,
    default_serving_weight_g=120.0,
    nutrition_per_100g={"calories": 210.0, "protein_g": 6.8, "carbs_g": 28.5, "fat_g": 8.2, "fiber_g": 0.0, "sodium_mg": 70.0},
    hierarchy=EastIndianHierarchy(
        level3_state="West Bengal", level4_region="Kolkata", level5_cuisine="Bengali",
        level6_food_family="Sweets", level7_food_type="Steamed Curd", level8_variant="Bhapa Doi",
        level9_cooking_method=["steamed"], default_portion="1 slice (120g)",
        nutrition_ref_id="wb_sweet_bhapa_doi"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="WB_SWEET_NOLEN_GUR_SANDESH",
    canonical_name="Nolen Gur Sandesh",
    state="West Bengal",
    region="Kolkata",
    cuisine="Bengali",
    food_category="Sweets",
    regional_names={"English": "Date Palm Jaggery Cottage Cheese Sweet", "Bengali": "নলেন গুড়ের সন্দেশ", "Hindi": "नोलन गुड़ संदेश"},
    alternate_names=["nolen gurer sandesh", "notun gur sandesh", "sandesh"],
    vegetarian=True,
    gravy_type="dry",
    visual_features={"color": "pale_caramel_to_light_golden_brown", "shape": "intricately_moulded_conch_shell (shankha)_or_flower", "texture": "soft_melt_in_mouth_granular_kneaded_chhana"},
    key_ingredients=["fresh chhana", "nolen gur (winter liquid date palm jaggery)", "cardamom"],
    hard_negatives=["NI_SWEET_PEDA", "OD_SWEET_CHHENA_PODA", "WB_SWEET_PLAIN_SANDESH"],
    density_g_cm3=0.88,
    default_serving_weight_g=35.0,
    nutrition_per_100g={"calories": 270.0, "protein_g": 9.5, "carbs_g": 42.0, "fat_g": 7.5, "fiber_g": 0.0, "sodium_mg": 45.0},
    hierarchy=EastIndianHierarchy(
        level3_state="West Bengal", level4_region="Kolkata", level5_cuisine="Bengali",
        level6_food_family="Sweets", level7_food_type="Sandesh", level8_variant="Nolen Gur Sandesh",
        level9_cooking_method=["pan_cooked_mild", "moulded"], default_portion="2 pieces (70g)",
        nutrition_ref_id="wb_sweet_nolen_gur_sandesh"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="WB_SWEET_PLAIN_SANDESH",
    canonical_name="Kanchagolla / Plain Sandesh",
    state="West Bengal",
    region="Kolkata",
    cuisine="Bengali",
    food_category="Sweets",
    regional_names={"English": "Fresh Soft Cottage Cheese Sweet", "Bengali": "কাঁচাগোল্লা / সাদা সন্দেশ", "Hindi": "सादा संदेश"},
    alternate_names=["kanchagolla", "plain sandesh", "norom pak sandesh"],
    vegetarian=True,
    gravy_type="dry",
    visual_features={"color": "ivory_white", "texture": "extremely_soft_unfired_granular_chhana_ball_or_mould"},
    key_ingredients=["fresh cow milk chhana", "powdered sugar", "green cardamom"],
    density_g_cm3=0.85,
    default_serving_weight_g=35.0,
    nutrition_per_100g={"calories": 260.0, "protein_g": 10.0, "carbs_g": 38.0, "fat_g": 7.8, "fiber_g": 0.0, "sodium_mg": 40.0},
    hierarchy=EastIndianHierarchy(
        level3_state="West Bengal", level4_region="Kolkata", level5_cuisine="Bengali",
        level6_food_family="Sweets", level7_food_type="Sandesh", level8_variant="Kanchagolla",
        level9_cooking_method=["raw_kneaded_lightly_warmed"], default_portion="2 pieces (70g)",
        nutrition_ref_id="wb_sweet_plain_sandesh"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="WB_SWEET_PATISHAPTA",
    canonical_name="Patishapta Pitha",
    state="West Bengal",
    region="Rural & Urban Bengal",
    cuisine="Bengali",
    food_category="Pitha",
    regional_names={"English": "Bengali Rice Crepe with Coconut-Kheer Filling", "Bengali": "পাটিসাপটা পিঠে", "Hindi": "पाटिशापटा"},
    alternate_names=["patishapta", "bengali crepe pitha"],
    vegetarian=True,
    gravy_type="dry",
    visual_features={"crepe": "thin_soft_rolled_cylindrical_pale_yellow_rice_flour_crepe", "filling_showing_at_ends": "grated_coconut_cooked_in_jaggery_or_condensed_milk_khoya"},
    key_ingredients=["rice flour", "maida", "suji (semolina)", "milk", "grated coconut or kheer/khoya", "date palm jaggery (nolen gur) or sugar", "ghee for tawa"],
    hard_negatives=["FRENCH_CREPE", "SOUTH_INDIAN_DOSA", "WB_SWEET_PULI_PITHA"],
    density_g_cm3=0.85,
    default_serving_weight_g=50.0,
    nutrition_per_100g={"calories": 240.0, "protein_g": 5.2, "carbs_g": 42.0, "fat_g": 6.2, "fiber_g": 1.5, "sodium_mg": 50.0},
    hierarchy=EastIndianHierarchy(
        level3_state="West Bengal", level4_region="Rural & Urban Bengal", level5_cuisine="Bengali",
        level6_food_family="Pitha", level7_food_type="Rolled Crepe Pitha", level8_variant="Patishapta",
        level9_cooking_method=["tawa_rolled"], default_portion="2 crepes (100g)",
        nutrition_ref_id="wb_sweet_patishapta"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="WB_SWEET_DOODH_PULI",
    canonical_name="Doodh Puli Pitha",
    state="West Bengal",
    region="Rural Bengal",
    cuisine="Bengali",
    food_category="Pitha",
    regional_names={"English": "Stuffed Rice Dumplings Simmered in Thick Milk", "Bengali": "দুধ পুলি", "Hindi": "दूध पुली"},
    alternate_names=["dudh puli", "puli pitha in milk"],
    vegetarian=True,
    gravy_type="syrup",
    visual_features={"dumpling": "crescent_shaped_tender_white_rice_flour_parcels", "milk": "thickened_ivory_cardamom_nolen_gur_scented_condensed_milk_bath"},
    key_ingredients=["rice flour dough", "coconut jaggery filling", "thickened milk", "nolen gur", "cardamom"],
    density_g_cm3=1.05,
    default_serving_weight_g=180.0,
    nutrition_per_100g={"calories": 195.0, "protein_g": 4.8, "carbs_g": 32.5, "fat_g": 5.5, "fiber_g": 0.8, "sodium_mg": 60.0},
    hierarchy=EastIndianHierarchy(
        level3_state="West Bengal", level4_region="Rural Bengal", level5_cuisine="Bengali",
        level6_food_family="Pitha", level7_food_type="Milk Puli", level8_variant="Doodh Puli",
        level9_cooking_method=["steamed_dumpling", "milk_simmered"], default_portion="1 bowl with 3 puli (180g)",
        nutrition_ref_id="wb_sweet_doodh_puli"
    )
))

# =============================================================================
# 9. ODISHA: RICE & PAKHALA DATASET (Sections 16 & 17)
# =============================================================================

register_east_food(EastIndianFoodClass(
    canonical_food_id="OD_RICE_DAHI_PAKHALA",
    canonical_name="Dahi Pakhala",
    state="Odisha",
    region="Coastal Odisha",
    cuisine="Odia",
    food_category="Rice",
    regional_names={"English": "Odia Tempered Curd Fermented Rice", "Odia": "ଦହି ପଖାଳ", "Hindi": "दही पखाला"},
    alternate_names=["odia dahi pakhala", "pakhala bhata with curd"],
    vegetarian=True,
    gravy_type="curd_broth",
    visual_features={"liquid": "creamy_cooling_curd_water_bath", "tempering": ["spluttered_mustard_seeds", "crisp_curry_leaves", "slit_green_chillies", "crushed_ginger", "mint_leaves"], "grain": "soft_fermented_rice_submerged"},
    key_ingredients=["cooked rice fermented in water", "fresh curd (dahi)", "mustard seeds", "curry leaves", "green chillies", "roasted cumin powder", "ginger", "salt"],
    hard_negatives=["WB_RICE_PANTA_BHAT", "SOUTH_INDIAN_CURD_RICE", "OD_RICE_BASI_PAKHALA"],
    density_g_cm3=0.98,
    default_serving_weight_g=350.0,
    nutrition_per_100g={"calories": 92.0, "protein_g": 2.4, "carbs_g": 16.5, "fat_g": 1.8, "fiber_g": 0.5, "sodium_mg": 190.0},
    hierarchy=EastIndianHierarchy(
        level3_state="Odisha", level4_region="Coastal Odisha", level5_cuisine="Odia",
        level6_food_family="Rice", level7_food_type="Pakhala", level8_variant="Dahi Pakhala",
        level9_cooking_method=["fermented", "soaked", "curd_tempered"], default_portion="1 large bowl with liquid (350g)",
        nutrition_ref_id="od_rice_dahi_pakhala"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="OD_RICE_BASI_PAKHALA",
    canonical_name="Basi Pakhala",
    state="Odisha",
    region="Rural Odisha",
    cuisine="Odia",
    food_category="Rice",
    regional_names={"English": "Overnight Fermented Odia Rice", "Odia": "ବାସି ପଖାଳ", "Hindi": "बासी पखाला"},
    alternate_names=["fermented pakhala", "basi torani"],
    vegetarian=True,
    gravy_type="curd_broth",
    visual_features={"liquid": "sour_fermented_clear_torani_water", "sides": ["badi_chura", "saga_bhaja", "green_chilli"]},
    key_ingredients=["cooked rice soaked 12+ hours in water (torani)", "salt", "green chillies", "lemon"],
    density_g_cm3=0.96,
    default_serving_weight_g=320.0,
    nutrition_per_100g={"calories": 78.0, "protein_g": 1.7, "carbs_g": 16.0, "fat_g": 0.4, "fiber_g": 0.5, "sodium_mg": 180.0},
    hierarchy=EastIndianHierarchy(
        level3_state="Odisha", level4_region="Rural Odisha", level5_cuisine="Odia",
        level6_food_family="Rice", level7_food_type="Pakhala", level8_variant="Basi Pakhala",
        level9_cooking_method=["fermented_overnight"], default_portion="1 bowl (320g)",
        nutrition_ref_id="od_rice_basi_pakhala"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="OD_RICE_KANIKA",
    canonical_name="Kanika",
    state="Odisha",
    region="Puri Temple",
    cuisine="Odia",
    food_category="Rice",
    regional_names={"English": "Sweet Fragrant Temple Rice of Lord Jagannath", "Odia": "କାନିକା", "Hindi": "कनिका"},
    alternate_names=["jagannath puri kanika", "meetha kanika"],
    vegetarian=True,
    gravy_type=None,
    visual_features={"color": "bright_golden_yellow", "grain": "fine_aromatic_rice_coated_in_ghee", "aromatics": ["cloves", "cinnamon", "cardamom", "nutmeg", "fried_cashews", "raisins"]},
    key_ingredients=["rice", "ghee", "sugar or jaggery", "cloves", "cinnamon", "bay leaf", "cardamom", "cashews", "raisins", "turmeric"],
    hard_negatives=["WB_RICE_BASANTI_PULAO", "NI_RICE_MEETHA_CHAWAL"],
    density_g_cm3=0.88,
    default_serving_weight_g=200.0,
    nutrition_per_100g={"calories": 215.0, "protein_g": 3.4, "carbs_g": 38.0, "fat_g": 5.8, "fiber_g": 1.0, "sodium_mg": 30.0},
    hierarchy=EastIndianHierarchy(
        level3_state="Odisha", level4_region="Puri Temple", level5_cuisine="Odia",
        level6_food_family="Rice", level7_food_type="Temple Sweet Rice", level8_variant="Kanika",
        level9_cooking_method=["earthen_pot_steamed", "ghee_cooked"], default_portion="1 plate (200g)",
        nutrition_ref_id="od_rice_kanika"
    )
))

# =============================================================================
# 10. ODISHA: DALMA & VEGETARIAN MASTER DATASET (Sections 18 & 19)
# =============================================================================

register_east_food(EastIndianFoodClass(
    canonical_food_id="OD_CURRY_DALMA",
    canonical_name="Odia Dalma",
    state="Odisha",
    region="Coastal Odisha / Puri",
    cuisine="Odia",
    food_category="Dal",
    regional_names={"English": "Odia Lentils Stewed with Wholesome Vegetables", "Odia": "ଡାଲମା", "Hindi": "डालमा"},
    alternate_names=["odia dalma", "temple dalma", "puri mahaprasad dalma"],
    vegetarian=True,
    gravy_type="dal_stew",
    visual_features={"base": "thick_yellow_toor_or_moong_dal_broth", "chunky_vegetables": ["yellow_pumpkin (boiti kakharu)", "raw_papaya (amrutabhanda)", "raw_banana (kancha kadali)", "taro_root (saru)", "drumstick (sajana chhuin)"], "tempering": ["bhaja_jeera_lanka_gunda (roasted cumin & dry chilli powder sprinkled on top)", "pure_desi_ghee_sheen", "grated_fresh_coconut_optional"]},
    key_ingredients=["toor dal or roasted moong dal", "pumpkin", "raw papaya", "plantain", "colocasia (saru)", "bhaja jeera lanka gunda (roasted cumin & dry chilli powder)", "panch phoron", "ghee", "ginger", "salt", "turmeric"],
    hard_negatives=["SOUTH_INDIAN_SAMBAR", "WB_DAL_CHOLAR_DAL", "NORTH_INDIAN_DAL_TADKA"],
    density_g_cm3=1.04,
    default_serving_weight_g=220.0,
    nutrition_per_100g={"calories": 105.0, "protein_g": 4.8, "carbs_g": 16.2, "fat_g": 2.5, "fiber_g": 3.8, "sodium_mg": 210.0},
    hierarchy=EastIndianHierarchy(
        level3_state="Odisha", level4_region="Coastal Odisha / Puri", level5_cuisine="Odia",
        level6_food_family="Dal", level7_food_type="Dalma", level8_variant="Traditional Odia Dalma",
        level9_cooking_method=["boiled", "ghee_roasted_spice_tempered"], default_portion="1 bowl (220g)",
        nutrition_ref_id="od_curry_dalma"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="OD_VEG_SANTULA",
    canonical_name="Santula",
    state="Odisha",
    region="Coastal Odisha",
    cuisine="Odia",
    food_category="Vegetarian",
    regional_names={"English": "Odia Steamed Vegetables in Milk/Water Tempering", "Odia": "ସନ୍ତୁଳା", "Hindi": "संतुला"},
    alternate_names=["pani santula", "khira santula", "odia boiled vegetables"],
    vegetarian=True,
    gravy_type="semi_gravy",
    visual_features={"texture": "tender_lightly_boiled_vegetables", "color": "pale_ivory_white_or_light_green", "tempering": ["spluttered_panch_phoron", "crushed_garlic", "green_chillies"]},
    key_ingredients=["raw papaya", "potatoes", "string beans", "brinjal", "pumpkin", "crushed garlic", "panch phoron", "milk optional", "salt"],
    density_g_cm3=0.96,
    default_serving_weight_g=200.0,
    nutrition_per_100g={"calories": 75.0, "protein_g": 2.0, "carbs_g": 12.0, "fat_g": 2.1, "fiber_g": 3.0, "sodium_mg": 170.0},
    hierarchy=EastIndianHierarchy(
        level3_state="Odisha", level4_region="Coastal Odisha", level5_cuisine="Odia",
        level6_food_family="Vegetarian", level7_food_type="Santula", level8_variant="Pani/Khira Santula",
        level9_cooking_method=["steamed", "garlic_tempered"], default_portion="1 bowl (200g)",
        nutrition_ref_id="od_veg_santula"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="OD_VEG_BESARA",
    canonical_name="Odia Besara",
    state="Odisha",
    region="Puri / Coastal Odisha",
    cuisine="Odia",
    food_category="Vegetarian",
    regional_names={"English": "Odia Mixed Vegetables in Mustard Garlic Paste with Badi", "Odia": "ବେସର", "Hindi": "बेसरा"},
    alternate_names=["vegetable besara", "odia besara"],
    vegetarian=True,
    gravy_type="mustard_gravy",
    visual_features={"gravy": "fragrant_yellow_mustard_garlic_gravy", "toppings": ["crunchy_fried_urad_dal_dumplings (badi)", "parwal", "taro", "plantain"]},
    key_ingredients=["mixed vegetables (drumsticks, raw banana, colocasia, parwal)", "mustard paste with garlic", "fried badi", "panch phoron", "mustard oil"],
    density_g_cm3=0.98,
    default_serving_weight_g=200.0,
    nutrition_per_100g={"calories": 115.0, "protein_g": 3.4, "carbs_g": 14.5, "fat_g": 5.2, "fiber_g": 3.2, "sodium_mg": 210.0},
    hierarchy=EastIndianHierarchy(
        level3_state="Odisha", level4_region="Puri / Coastal Odisha", level5_cuisine="Odia",
        level6_food_family="Vegetarian", level7_food_type="Besara", level8_variant="Mixed Veg Besara",
        level9_cooking_method=["mustard_simmered"], default_portion="1 bowl (200g)",
        nutrition_ref_id="od_veg_besara"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="OD_VEG_DAHI_BAINGAN",
    canonical_name="Dahi Baingan",
    state="Odisha",
    region="Coastal Odisha",
    cuisine="Odia",
    food_category="Vegetarian",
    regional_names={"English": "Odia Fried Eggplant in Tempered Yogurt", "Odia": "ଦହି ବାଇଗଣ", "Hindi": "दही बैंगन"},
    alternate_names=["dahi baigana", "odia dahi baigana"],
    vegetarian=True,
    gravy_type="curd_broth",
    visual_features={"eggplant": "golden_pan_fried_tender_brinjal_slices", "yogurt": "whisked_spiced_yogurt_bath", "tempering": ["spluttered_mustard_seeds", "curry_leaves", "roasted_cumin_powder"]},
    key_ingredients=["eggplant", "curd (dahi)", "mustard seeds", "curry leaves", "green chillies", "bhaja jeera powder", "mustard oil"],
    density_g_cm3=1.00,
    default_serving_weight_g=180.0,
    nutrition_per_100g={"calories": 120.0, "protein_g": 3.2, "carbs_g": 9.5, "fat_g": 7.8, "fiber_g": 2.5, "sodium_mg": 190.0},
    hierarchy=EastIndianHierarchy(
        level3_state="Odisha", level4_region="Coastal Odisha", level5_cuisine="Odia",
        level6_food_family="Vegetarian", level7_food_type="Dahi Dish", level8_variant="Dahi Baigana",
        level9_cooking_method=["pan_fried", "curd_mixed"], default_portion="1 bowl (180g)",
        nutrition_ref_id="od_veg_dahi_baingan"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="OD_VEG_SAGA_BHAJA",
    canonical_name="Odia Saga Bhaja",
    state="Odisha",
    region="Coastal Odisha",
    cuisine="Odia",
    food_category="Vegetarian",
    regional_names={"English": "Stir-Fried Odia Leafy Greens with Garlic & Badi", "Odia": "ଶାଗ ଭଜା", "Hindi": "साग भाजा"},
    alternate_names=["koshila saga", "palanga saga", "saga badi bhaja"],
    vegetarian=True,
    gravy_type="dry",
    visual_features={"greens": "vibrant_dark_green_chopped_leafy_greens", "crunch": ["fried_crushed_badi_chunks", "golden_brown_fried_garlic_slivers"]},
    key_ingredients=["local green leaves (koshila, leutia, or palanga)", "fried badi bits", "sliced garlic", "dry red chilli", "mustard oil", "salt"],
    density_g_cm3=0.75,
    default_serving_weight_g=120.0,
    nutrition_per_100g={"calories": 95.0, "protein_g": 3.8, "carbs_g": 8.0, "fat_g": 5.2, "fiber_g": 3.5, "sodium_mg": 180.0},
    hierarchy=EastIndianHierarchy(
        level3_state="Odisha", level4_region="Coastal Odisha", level5_cuisine="Odia",
        level6_food_family="Vegetarian", level7_food_type="Saga", level8_variant="Saga Badi Bhaja",
        level9_cooking_method=["stir_fried", "garlic_tempered"], default_portion="1 cup (120g)",
        nutrition_ref_id="od_veg_saga_bhaja"
    )
))

# =============================================================================
# 11. ODISHA: SEAFOOD MASTER DATASET (Section 20)
# =============================================================================

register_east_food(EastIndianFoodClass(
    canonical_food_id="OD_SEAFOOD_MACHA_BESARA",
    canonical_name="Macha Besara",
    state="Odisha",
    region="Coastal Odisha",
    cuisine="Odia",
    food_category="Fish/Seafood",
    regional_names={"English": "Odia Fish Curry in Mustard Paste with Raw Mango / Ambula", "Odia": "ମାଛ ବେସର", "Hindi": "माछ बेसरा"},
    alternate_names=["odia mustard fish", "macha besara"],
    vegetarian=False,
    gravy_type="mustard_gravy",
    visual_features={"gravy": "thick_sharp_yellow_mustard_garlic_paste", "sour_agent": "sun_dried_mango (ambula)_or_tomato_wedges", "fish": "fried_rohu_or_catla_steak"},
    key_ingredients=["rohu or hilsa fish", "yellow mustard and garlic paste", "ambula (sun-dried salted mango)", "panch phoron", "green chillies", "mustard oil", "turmeric"],
    fish_species="Rohu",
    hard_negatives=["WB_FISH_SHORSHE_MAACH", "OD_SEAFOOD_MACHA_JHOLA"],
    density_g_cm3=1.01,
    default_serving_weight_g=210.0,
    nutrition_per_100g={"calories": 165.0, "protein_g": 13.0, "carbs_g": 3.5, "fat_g": 10.8, "fiber_g": 1.1, "sodium_mg": 310.0},
    hierarchy=EastIndianHierarchy(
        level3_state="Odisha", level4_region="Coastal Odisha", level5_cuisine="Odia",
        level6_food_family="Fish/Seafood", level7_food_type="Macha Besara", level8_variant="Macha Besara with Ambula",
        level9_cooking_method=["shallow_fried", "mustard_simmered"], default_portion="1 piece with gravy (210g)",
        nutrition_ref_id="od_seafood_macha_besara"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="OD_SEAFOOD_MACHA_JHOLA",
    canonical_name="Macha Jhola",
    state="Odisha",
    region="Coastal Odisha",
    cuisine="Odia",
    food_category="Fish/Seafood",
    regional_names={"English": "Traditional Odia Fish Curry", "Odia": "ମାଛ ଝୋଳ", "Hindi": "माछ झोल"},
    alternate_names=["odia fish curry", "macha jhola"],
    vegetarian=False,
    gravy_type="jhol_thin_broth",
    visual_features={"gravy": "rich_reddish_brown_onion_ginger_garlic_gravy", "potatoes": "fried_potato_halves", "fish": "bone_in_fried_fish_steak"},
    key_ingredients=["rohu or freshwater carp", "potatoes", "onions", "ginger garlic paste", "tomato", "panch phoron", "mustard oil"],
    fish_species="Rohu",
    density_g_cm3=0.99,
    default_serving_weight_g=220.0,
    nutrition_per_100g={"calories": 125.0, "protein_g": 11.5, "carbs_g": 4.2, "fat_g": 6.8, "fiber_g": 0.6, "sodium_mg": 280.0},
    hierarchy=EastIndianHierarchy(
        level3_state="Odisha", level4_region="Coastal Odisha", level5_cuisine="Odia",
        level6_food_family="Fish/Seafood", level7_food_type="Macha Jhola", level8_variant="Macha Jhola with Aloo",
        level9_cooking_method=["pan_fried", "stewed_gravy"], default_portion="1 serving (220g)",
        nutrition_ref_id="od_seafood_macha_jhola"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="OD_SEAFOOD_CHINGUDI_BESARA",
    canonical_name="Chingudi Besara",
    state="Odisha",
    region="Chilika Lake / Coastal Odisha",
    cuisine="Odia",
    food_category="Fish/Seafood",
    regional_names={"English": "Chilika Prawns in Mustard Garlic Gravy", "Odia": "ଚିଙ୍ଗୁଡ଼ି ବେସର", "Hindi": "चिंगुड़ी बेसरा"},
    alternate_names=["prawn besara", "chilika prawn curry"],
    vegetarian=False,
    gravy_type="mustard_gravy",
    visual_features={"prawns": "whole_curled_pinkish_prawns", "gravy": "yellow_mustard_curry_with_mustard_seeds"},
    key_ingredients=["prawns (chingudi)", "mustard garlic paste", "panch phoron", "ambula", "mustard oil", "green chillies"],
    fish_species="Prawn",
    density_g_cm3=1.01,
    default_serving_weight_g=200.0,
    nutrition_per_100g={"calories": 170.0, "protein_g": 13.5, "carbs_g": 3.8, "fat_g": 11.0, "fiber_g": 1.0, "sodium_mg": 320.0},
    hierarchy=EastIndianHierarchy(
        level3_state="Odisha", level4_region="Chilika Lake / Coastal Odisha", level5_cuisine="Odia",
        level6_food_family="Fish/Seafood", level7_food_type="Chingudi Curry", level8_variant="Chingudi Besara",
        level9_cooking_method=["sauteed", "mustard_simmered"], default_portion="1 bowl (200g)",
        nutrition_ref_id="od_seafood_chingudi_besara"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="OD_SEAFOOD_CRAB_CURRY",
    canonical_name="Kankada Jhola",
    state="Odisha",
    region="Coastal Odisha",
    cuisine="Odia",
    food_category="Fish/Seafood",
    regional_names={"English": "Odia Spiced Crab Curry", "Odia": "କଙ୍କଡ଼ା ଝୋଳ", "Hindi": "कंकड़ा झोल"},
    alternate_names=["crab curry odia", "kankada curry"],
    vegetarian=False,
    gravy_type="semi_gravy",
    visual_features={"shell": "whole_or_halved_cooked_orange_red_crab_claws_and_body", "gravy": "dark_spiced_onion_garlic_gravy"},
    key_ingredients=["mud crabs (kankada)", "onions", "ginger garlic paste", "potatoes", "garam masala", "mustard oil"],
    fish_species="Crab",
    density_g_cm3=0.98,
    default_serving_weight_g=250.0,
    nutrition_per_100g={"calories": 120.0, "protein_g": 12.0, "carbs_g": 3.5, "fat_g": 6.2, "fiber_g": 0.5, "sodium_mg": 360.0},
    hierarchy=EastIndianHierarchy(
        level3_state="Odisha", level4_region="Coastal Odisha", level5_cuisine="Odia",
        level6_food_family="Fish/Seafood", level7_food_type="Crab Curry", level8_variant="Kankada Jhola",
        level9_cooking_method=["slow_cooked_simmered"], default_portion="1 bowl with crabs (250g)",
        nutrition_ref_id="od_seafood_crab_curry"
    )
))

# =============================================================================
# 12. ODISHA: SWEETS & DAHIBARA ALOODUM (Sections 22, 34, 35)
# =============================================================================

register_east_food(EastIndianFoodClass(
    canonical_food_id="OD_SWEET_CHHENA_PODA",
    canonical_name="Chhena Poda",
    state="Odisha",
    region="Nayagarh / Coastal Odisha",
    cuisine="Odia",
    food_category="Sweets",
    regional_names={"English": "Odia Baked Caramelized Cottage Cheese Cake", "Odia": "ଛେନାପୋଡ଼", "Hindi": "छेना पोड़ा"},
    alternate_names=["chhenapoda", "baked cheese sweet odisha"],
    vegetarian=True,
    gravy_type="dry",
    visual_features={"crust": "distinctive_deep_caramelized_dark_burnt_brown_exterior_crust", "interior": "soft_creamy_moist_honeycombed_chhana_crumb", "garnishes": ["cashews", "cardamom_specks", "charred_sal_leaf_traces"]},
    key_ingredients=["fresh cow milk chhana", "sugar (caramelized while baking)", "suji (semolina) a pinch", "ghee", "green cardamom", "cashews and raisins", "sal leaves for baking wrap"],
    hard_negatives=["WESTERN_CHEESECAKE", "NI_SWEET_MILK_CAKE", "WB_SWEET_SANDESH"],
    density_g_cm3=0.88,
    default_serving_weight_g=100.0,
    nutrition_per_100g={"calories": 290.0, "protein_g": 11.2, "carbs_g": 38.0, "fat_g": 10.5, "fiber_g": 0.4, "sodium_mg": 65.0},
    hierarchy=EastIndianHierarchy(
        level3_state="Odisha", level4_region="Nayagarh / Coastal Odisha", level5_cuisine="Odia",
        level6_food_family="Sweets", level7_food_type="Baked Sweet", level8_variant="Authentic Chhena Poda",
        level9_cooking_method=["slow_baked_wood_fire"], default_portion="1 thick slice (100g)",
        nutrition_ref_id="od_sweet_chhena_poda"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="OD_SWEET_CHHENA_GAJA",
    canonical_name="Chhena Gaja",
    state="Odisha",
    region="Puri / Coastal Odisha",
    cuisine="Odia",
    food_category="Sweets",
    regional_names={"English": "Deep-Fried Rectangular Chhena Soaked in Sugar Syrup", "Odia": "ଛେନା ଗଜା", "Hindi": "छेना गजा"},
    alternate_names=["chhena gaja", "odia gaja"],
    vegetarian=True,
    gravy_type="syrup",
    visual_features={"shape": "dense_rectangular_brick", "surface": "deep_golden_brown_fried_crystallized_sugar_coating"},
    key_ingredients=["chhana", "semolina", "sugar syrup", "cardamom", "ghee for frying"],
    density_g_cm3=1.12,
    default_serving_weight_g=60.0,
    nutrition_per_100g={"calories": 330.0, "protein_g": 8.0, "carbs_g": 52.0, "fat_g": 10.2, "fiber_g": 0.2, "sodium_mg": 50.0},
    hierarchy=EastIndianHierarchy(
        level3_state="Odisha", level4_region="Puri / Coastal Odisha", level5_cuisine="Odia",
        level6_food_family="Sweets", level7_food_type="Chhana Sweet", level8_variant="Chhena Gaja",
        level9_cooking_method=["deep_fried", "syrup_soaked"], default_portion="1 piece (60g)",
        nutrition_ref_id="od_sweet_chhena_gaja"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="OD_SWEET_RASABALI",
    canonical_name="Rasabali",
    state="Odisha",
    region="Kendrapara / Coastal Odisha",
    cuisine="Odia",
    food_category="Sweets",
    regional_names={"English": "Flattened Fried Chhena Patties in Thickened Milk", "Odia": "ରସାବଳି", "Hindi": "रसाबली"},
    alternate_names=["kendrapara rasabali", "rasabali sweet"],
    vegetarian=True,
    gravy_type="syrup",
    visual_features={"patties": "deep_reddish_brown_flattened_perforated_chhana_discs", "milk": "thickened_rabri_like_cardamom_scented_milk_bath"},
    key_ingredients=["chhana", "wheat flour", "sugar", "thickened milk", "cardamom", "ghee for frying"],
    density_g_cm3=1.06,
    default_serving_weight_g=120.0,
    nutrition_per_100g={"calories": 260.0, "protein_g": 7.5, "carbs_g": 36.0, "fat_g": 9.8, "fiber_g": 0.3, "sodium_mg": 60.0},
    hierarchy=EastIndianHierarchy(
        level3_state="Odisha", level4_region="Kendrapara / Coastal Odisha", level5_cuisine="Odia",
        level6_food_family="Sweets", level7_food_type="Chhana Sweet", level8_variant="Rasabali",
        level9_cooking_method=["deep_fried_patties", "milk_soaked"], default_portion="2 patties with milk (120g)",
        nutrition_ref_id="od_sweet_rasabali"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="OD_SWEET_PURI_KHAJA",
    canonical_name="Puri Jagannath Khaja",
    state="Odisha",
    region="Puri Temple",
    cuisine="Odia",
    food_category="Sweets",
    regional_names={"English": "Crisp Multi-Layered Puri Temple Wafer in Sugar Glaze", "Odia": "ଖଜା (ଜଗନ୍ନାଥ ଖଜା)", "Hindi": "पूरी खाजा"},
    alternate_names=["pheni khaja", "puri mahaprasad khaja", "crisp layered khaja"],
    vegetarian=True,
    gravy_type="dry",
    visual_features={"texture": "visible_hundreds_of_delicate_wafer_thin_crispy_fried_pastry_layers", "coating": "clear_dry_glistening_crystallized_sugar_glaze"},
    key_ingredients=["maida (refined flour)", "pure desi ghee for layering (sata)", "sugar syrup coating", "water"],
    hard_negatives=["BR_SWEET_SILAO_KHAJA", "WESTERN_CROISSANT", "WESTERN_BAKLAVA"],
    density_g_cm3=0.55,
    default_serving_weight_g=70.0,
    nutrition_per_100g={"calories": 440.0, "protein_g": 4.5, "carbs_g": 62.0, "fat_g": 19.5, "fiber_g": 1.0, "sodium_mg": 40.0},
    hierarchy=EastIndianHierarchy(
        level3_state="Odisha", level4_region="Puri Temple", level5_cuisine="Odia",
        level6_food_family="Sweets", level7_food_type="Khaja", level8_variant="Puri Jagannath Mahaprasad Khaja",
        level9_cooking_method=["layered_dough", "deep_fried_in_ghee", "sugar_glazed"], default_portion="1 piece (70g)",
        nutrition_ref_id="od_sweet_puri_khaja"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="OD_STREET_DAHIBARA_ALOODUM",
    canonical_name="Cuttack Dahibara Aloodum",
    state="Odisha",
    region="Cuttack",
    cuisine="Odia",
    food_category="Street Food",
    regional_names={"English": "Cuttack Tempered Spiced Yogurt Vadas with Potato & Pea Curry", "Odia": "ଦହିବରା ଆଳୁଦମ", "Hindi": "दहीबरा आलूदम"},
    alternate_names=["cuttack dahibara", "odia dahi vada aloo dum"],
    vegetarian=True,
    gravy_type="curd_broth",
    visual_features={"base": "urad_dal_vadas_soaked_in_thin_sour_tempered_buttermilk (dahi_pani)", "layered_toppings": ["spicy_dark_potato_curry (aloodum)", "yellow_dried_pea_curry (ghugni)", "thin_cooling_yogurt_splash", "sweet_tangy_chutney", "crunchy_fine_sev", "chopped_raw_onions", "fresh_coriander", "bhaja_jeera_lanka_gunda"]},
    key_ingredients=["urad dal vadas", "thin curd water with mustard & curry leaf tempering", "spicy potato curry (aloodum)", "yellow pea ghugni", "chopped onions", "sev", "coriander", "black salt", "bhaja jeera powder"],
    hard_negatives=["NI_STREET_DAHI_VADA", "NI_STREET_DAHI_BHALLA", "MUM_STREET_DAHI_PURI"],
    density_g_cm3=0.98,
    default_serving_weight_g=280.0,
    nutrition_per_100g={"calories": 145.0, "protein_g": 5.2, "carbs_g": 19.8, "fat_g": 5.0, "fiber_g": 3.2, "sodium_mg": 380.0},
    hierarchy=EastIndianHierarchy(
        level3_state="Odisha", level4_region="Cuttack", level5_cuisine="Odia",
        level6_food_family="Street Food", level7_food_type="Dahibara Aloodum", level8_variant="Cuttack Famous Dahibara Aloodum",
        level9_cooking_method=["soaked_fried_vadas", "composite_curry_assembly"], default_portion="1 bowl with 2-3 vadas + aloodum + ghugni (280g)",
        nutrition_ref_id="od_street_dahibara_aloodum"
    )
))

# =============================================================================
# 13. BIHAR: LITTI, CHOKHA, SATTU & MEAT (Sections 23, 24, 25, 26, 27, 28)
# =============================================================================

register_east_food(EastIndianFoodClass(
    canonical_food_id="BR_BREAD_LITTI",
    canonical_name="Bihari Litti",
    state="Bihar",
    region="Bhojpur / Magadh",
    cuisine="Bihari",
    food_category="Breakfast",
    regional_names={"English": "Roasted Whole Wheat Dough Ball Stuffed with Spiced Sattu", "Hindi": "लिट्टी", "Bhojpuri": "लिट्टी", "Maithili": "लिट्टी"},
    alternate_names=["sattu litti", "ghee litti", "bihari litti"],
    vegetarian=True,
    gravy_type="dry",
    visual_features={"exterior": "charred_golden_brown_spots_from_cow_dung_or_charcoal_ash_baking", "shape": "dense_round_rustic_cracked_ball", "ghee": "often_dipped_in_molten_desi_ghee", "interior": "crumbly_yellowish_brown_spiced_roasted_gram_flour (sattu)_filling"},
    key_ingredients=["whole wheat flour (atta)", "sattu (roasted gram flour)", "pure desi ghee for dipping", "kalonji (nigella seeds)", "ajwain (carom seeds)", "mustard oil", "green chillies", "lemon juice", "pickle masala (amchoor)"],
    hard_negatives=["NI_BREAD_BAATI_RAJASTHANI", "WB_BREAD_LUCHI", "NI_BREAD_KACHORI"],
    density_g_cm3=0.82,
    default_serving_weight_g=75.0,
    nutrition_per_100g={"calories": 265.0, "protein_g": 9.8, "carbs_g": 41.5, "fat_g": 7.2, "fiber_g": 5.8, "sodium_mg": 280.0},
    hierarchy=EastIndianHierarchy(
        level3_state="Bihar", level4_region="Bhojpur / Magadh", level5_cuisine="Bihari",
        level6_food_family="Breakfast", level7_food_type="Litti", level8_variant="Sattu Stuffed Roasted Litti",
        level9_cooking_method=["charcoal_roasted", "ash_baked", "ghee_dipped"], default_portion="2 littis dipped in ghee (150g)",
        nutrition_ref_id="br_bread_litti"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="BR_CHOKHA_BAINGAN",
    canonical_name="Baingan Chokha",
    state="Bihar",
    region="Bhojpur / Magadh",
    cuisine="Bihari",
    food_category="Vegetarian",
    regional_names={"English": "Roasted Smoked Eggplant Mash with Raw Mustard Oil", "Hindi": "बैंगन चोखा", "Bhojpuri": "भंटा के चोखा"},
    alternate_names=["baingan ka chokha", "bhanta chokha", "roasted eggplant mash"],
    vegetarian=True,
    gravy_type="semi_gravy",
    visual_features={"texture": "rustic_chunky_smoky_mash", "color": "dark_charcoal_flecked_olive_brown", "visible": ["crushed_roasted_garlic", "finely_chopped_raw_onions", "green_chillies", "fresh_coriander", "mustard_oil_sheen"]},
    key_ingredients=["large purple eggplant roasted over open flame", "crushed garlic roasted inside eggplant", "raw mustard oil", "chopped onions", "green chillies", "salt", "fresh coriander"],
    hard_negatives=["NI_VEG_BAINGAN_BHARTA", "WB_VEG_BEGUN_PORA"],
    density_g_cm3=0.92,
    default_serving_weight_g=120.0,
    nutrition_per_100g={"calories": 85.0, "protein_g": 1.9, "carbs_g": 8.5, "fat_g": 5.2, "fiber_g": 3.0, "sodium_mg": 220.0},
    hierarchy=EastIndianHierarchy(
        level3_state="Bihar", level4_region="Bhojpur / Magadh", level5_cuisine="Bihari",
        level6_food_family="Vegetarian", level7_food_type="Chokha", level8_variant="Flame Roasted Baingan Chokha",
        level9_cooking_method=["open_flame_roasted", "raw_mustard_oil_mashed"], default_portion="1 bowl (120g)",
        nutrition_ref_id="br_chokha_baingan"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="BR_CHOKHA_ALOO",
    canonical_name="Aloo Chokha",
    state="Bihar",
    region="Bhojpur / Magadh",
    cuisine="Bihari",
    food_category="Vegetarian",
    regional_names={"English": "Spiced Rustic Mashed Potatoes with Mustard Oil", "Hindi": "आलू चोखा", "Bhojpuri": "आलू के चोखा"},
    alternate_names=["aloo bharta", "bihari mashed potatoes"],
    vegetarian=True,
    gravy_type="dry",
    visual_features={"texture": "chunky_coarse_hand_mashed_potatoes", "visible": ["chopped_raw_onions", "roasted_red_or_green_chillies", "raw_mustard_oil_tinge"]},
    key_ingredients=["boiled or fire-roasted potatoes", "raw mustard oil", "chopped onions", "green chillies", "salt", "roasted red chilli"],
    density_g_cm3=0.94,
    default_serving_weight_g=120.0,
    nutrition_per_100g={"calories": 115.0, "protein_g": 2.2, "carbs_g": 18.5, "fat_g": 3.8, "fiber_g": 2.1, "sodium_mg": 210.0},
    hierarchy=EastIndianHierarchy(
        level3_state="Bihar", level4_region="Bhojpur / Magadh", level5_cuisine="Bihari",
        level6_food_family="Vegetarian", level7_food_type="Chokha", level8_variant="Aloo Chokha",
        level9_cooking_method=["boiled", "mashed"], default_portion="1 bowl (120g)",
        nutrition_ref_id="br_chokha_aloo"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="BR_CHOKHA_TOMATO",
    canonical_name="Tamatar Chokha",
    state="Bihar",
    region="Bhojpur / Magadh",
    cuisine="Bihari",
    food_category="Vegetarian",
    regional_names={"English": "Fire-Roasted Tomato Mash with Mustard Oil", "Hindi": "टमाटर चोखा", "Bhojpuri": "टमाटर के चोखा"},
    alternate_names=["tomato chokha", "bhuna tamatar mash"],
    vegetarian=True,
    gravy_type="semi_gravy",
    visual_features={"color": "rustic_red_with_black_char_flecks", "texture": "chunky_pulpy_releasing_tangy_juices"},
    key_ingredients=["ripe tomatoes charred on direct fire", "raw mustard oil", "finely chopped onions", "green chillies", "coriander", "salt"],
    density_g_cm3=0.96,
    default_serving_weight_g=100.0,
    nutrition_per_100g={"calories": 60.0, "protein_g": 1.2, "carbs_g": 6.8, "fat_g": 3.2, "fiber_g": 1.8, "sodium_mg": 200.0},
    hierarchy=EastIndianHierarchy(
        level3_state="Bihar", level4_region="Bhojpur / Magadh", level5_cuisine="Bihari",
        level6_food_family="Vegetarian", level7_food_type="Chokha", level8_variant="Tamatar Chokha",
        level9_cooking_method=["flame_roasted", "mashed"], default_portion="1 bowl (100g)",
        nutrition_ref_id="br_chokha_tomato"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="BR_BREAD_SATTU_PARATHA",
    canonical_name="Sattu Paratha",
    state="Bihar",
    region="Magadh / Mithila",
    cuisine="Bihari",
    food_category="Breakfast",
    regional_names={"English": "Whole Wheat Flatbread Stuffed with Spiced Roasted Gram", "Hindi": "सत्तू पराठा", "Bhojpuri": "सत्तू के पराठा"},
    alternate_names=["makuni", "sattu roti"],
    vegetarian=True,
    gravy_type="dry",
    visual_features={"shape": "flat_circular_tawa_toasted_bread", "spots": "golden_brown_tawa_blisters", "interior": "powdery_tangy_herbal_sattu_layer"},
    key_ingredients=["atta (whole wheat flour)", "sattu", "ajwain", "mangrela (kalonji)", "mustard oil", "green chillies", "amchoor / lemon", "ghee for tawa"],
    hard_negatives=["NI_BREAD_ALOO_PARATHA", "NI_BREAD_PANEER_PARATHA"],
    density_g_cm3=0.72,
    default_serving_weight_g=110.0,
    nutrition_per_100g={"calories": 255.0, "protein_g": 8.8, "carbs_g": 40.5, "fat_g": 7.0, "fiber_g": 5.2, "sodium_mg": 260.0},
    hierarchy=EastIndianHierarchy(
        level3_state="Bihar", level4_region="Magadh / Mithila", level5_cuisine="Bihari",
        level6_food_family="Breakfast", level7_food_type="Stuffed Paratha", level8_variant="Sattu Paratha",
        level9_cooking_method=["tawa_roasted"], default_portion="2 parathas (220g)",
        nutrition_ref_id="br_bread_sattu_paratha"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="BR_DRINK_SATTU_SHARBAT",
    canonical_name="Sattu Drink (Namkeen)",
    state="Bihar",
    region="Magadh",
    cuisine="Bihari",
    food_category="Beverages",
    regional_names={"English": "Savory Roasted Gram Flour Summer Cooler", "Hindi": "सत्तू का नमकीन शरबत", "Bhojpuri": "सत्तू के घोल"},
    alternate_names=["sattu sharbat", "sattu drink", "bihari protein drink"],
    vegetarian=True,
    gravy_type="curd_broth",
    visual_features={"liquid": "earthy_pale_tan_liquid_drink_in_tall_glass", "garnishes": ["roasted_cumin_powder_float", "finely_chopped_mint_and_green_chilli", "raw_onion_bits"]},
    key_ingredients=["roasted chana sattu", "cold water", "lemon juice", "roasted cumin powder", "black salt", "mint leaves", "chopped green chillies"],
    density_g_cm3=1.02,
    default_serving_weight_g=250.0,
    nutrition_per_100g={"calories": 68.0, "protein_g": 3.8, "carbs_g": 10.5, "fat_g": 1.2, "fiber_g": 2.2, "sodium_mg": 240.0},
    hierarchy=EastIndianHierarchy(
        level3_state="Bihar", level4_region="Magadh", level5_cuisine="Bihari",
        level6_food_family="Beverages", level7_food_type="Sattu Beverage", level8_variant="Namkeen Sattu Sharbat",
        level9_cooking_method=["whisked_cold"], default_portion="1 glass (250ml)",
        nutrition_ref_id="br_drink_sattu_sharbat"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="BR_MEAT_CHAMPARAN_MUTTON",
    canonical_name="Champaran Mutton (Ahuna)",
    state="Bihar",
    region="Champaran",
    cuisine="Bihari",
    food_category="Meat",
    regional_names={"English": "Clay Pot Slow Cooked Mutton with Whole Garlic Bulbs", "Hindi": "चंपारण मटन (अहुना)", "Bhojpuri": "अहुना मटन"},
    alternate_names=["ahuna mutton", "champaran meat", "matka mutton"],
    vegetarian=False,
    gravy_type="semi_gravy",
    visual_features={"cooking_vessel": "earthen_unpainted_clay_handi (matka)_with_flour_dough_seal (dum)", "signature_visual": "entire_intact_unpeeled_whole_garlic_bulb (lahsun ki ganth)_stewed_in_gravy", "gravy": "dark_amber_brown_thick_onion_gravy_with_heavy_mustard_oil_layer", "spices": "visible_whole_black_peppercorns_cloves_cinnamon"},
    key_ingredients=["mutton on the bone", "entire whole garlic heads (intact)", "raw mustard oil", "sliced onions", "whole garam masala", "ginger garlic paste", "bay leaves", "sealed clay pot dum"],
    hard_negatives=["WB_MEAT_KOSHA_MANGSHO", "NI_MEAT_ROGANI_MUTTON"],
    density_g_cm3=1.05,
    default_serving_weight_g=260.0,
    nutrition_per_100g={"calories": 275.0, "protein_g": 15.8, "carbs_g": 4.5, "fat_g": 21.5, "fiber_g": 1.0, "sodium_mg": 370.0},
    hierarchy=EastIndianHierarchy(
        level3_state="Bihar", level4_region="Champaran", level5_cuisine="Bihari",
        level6_food_family="Meat", level7_food_type="Champaran Mutton", level8_variant="Ahuna Clay Pot Mutton",
        level9_cooking_method=["earthen_handi_dum", "slow_cooked_charcoal"], default_portion="1 clay bowl with mutton + whole garlic (260g)",
        nutrition_ref_id="br_meat_champaran_mutton"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="BR_SWEET_THEKUA",
    canonical_name="Bihari Thekua",
    state="Bihar",
    region="Mithila / Magadh / Chhath",
    cuisine="Bihari",
    food_category="Sweets",
    regional_names={"English": "Chhath Puja Holy Jaggery & Whole Wheat Cookie", "Hindi": "ठेकूआ", "Bhojpuri": "ठेकूआ", "Maithili": "ठकुआ"},
    alternate_names=["khajuria", "thakuwa", "chhath thekua"],
    vegetarian=True,
    gravy_type="dry",
    visual_features={"shape": "oval_or_leaf_shaped_thick_hard_cookie", "embossing": "intricate_geometric_die_patterns_from_wooden_mould (sancha)", "color": "dark_golden_brown_from_jaggery_and_ghee", "texture": "hard_crisp_crumbly"},
    key_ingredients=["whole wheat flour (atta)", "gud (unrefined jaggery) or sugar", "pure desi ghee", "crushed fennel seeds (saunf)", "dry coconut slivers", "green cardamom"],
    hard_negatives=["WESTERN_COOKIE", "NI_SWEET_MATHRI", "WESTERN_BISCUIT"],
    density_g_cm3=0.85,
    default_serving_weight_g=40.0,
    nutrition_per_100g={"calories": 435.0, "protein_g": 6.8, "carbs_g": 64.0, "fat_g": 17.5, "fiber_g": 3.8, "sodium_mg": 45.0},
    hierarchy=EastIndianHierarchy(
        level3_state="Bihar", level4_region="Mithila / Magadh / Chhath", level5_cuisine="Bihari",
        level6_food_family="Sweets", level7_food_type="Thekua", level8_variant="Traditional Gur Thekua",
        level9_cooking_method=["moulded_wooden_die", "deep_fried_in_ghee"], default_portion="2 pieces (80g)",
        nutrition_ref_id="br_sweet_thekua"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="BR_SWEET_TILKUT",
    canonical_name="Gaya Tilkut",
    state="Bihar",
    region="Gaya",
    cuisine="Bihari",
    food_category="Sweets",
    regional_names={"English": "Pounded Sesame & Jaggery Crisp Wafer", "Hindi": "गया तिलकुट", "Bhojpuri": "तिलकुट"},
    alternate_names=["bihari tilkut", "gaya sesame sweet"],
    vegetarian=True,
    gravy_type="dry",
    visual_features={"shape": "round_flat_disc_or_crumbly_wedge", "surface": "dense_coating_of_white_sesame_seeds", "interior": "porous_flaky_pounded_jaggery_sesame_matrix"},
    key_ingredients=["white sesame seeds (til)", "melted jaggery or sugar", "cardamom"],
    density_g_cm3=0.72,
    default_serving_weight_g=50.0,
    nutrition_per_100g={"calories": 480.0, "protein_g": 11.5, "carbs_g": 54.0, "fat_g": 24.5, "fiber_g": 5.2, "sodium_mg": 35.0},
    hierarchy=EastIndianHierarchy(
        level3_state="Bihar", level4_region="Gaya", level5_cuisine="Bihari",
        level6_food_family="Sweets", level7_food_type="Tilkut", level8_variant="Gaya Tilkut",
        level9_cooking_method=["hand_pounded", "pulled"], default_portion="1 piece (50g)",
        nutrition_ref_id="br_sweet_tilkut"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="BR_SWEET_SILAO_KHAJA",
    canonical_name="Silao Khaja",
    state="Bihar",
    region="Nalanda / Silao",
    cuisine="Bihari",
    food_category="Sweets",
    regional_names={"English": "GI-Tagged Silao Layered Crisp Sweet Wafer", "Hindi": "सिलाव का खाजा", "Bhojpuri": "सिलाव खाजा"},
    alternate_names=["silao khaja", "bihari khaja"],
    vegetarian=True,
    gravy_type="dry",
    visual_features={"texture": "extremely_brittle_multiple_paper_thin_layers", "color": "pale_golden_ivory_not_dark", "sheen": "light_sugar_glaze"},
    key_ingredients=["maida", "ghee for sheeting", "sugar syrup dipping", "water"],
    hard_negatives=["OD_SWEET_PURI_KHAJA", "WESTERN_CROISSANT"],
    density_g_cm3=0.52,
    default_serving_weight_g=60.0,
    nutrition_per_100g={"calories": 430.0, "protein_g": 4.2, "carbs_g": 65.0, "fat_g": 17.5, "fiber_g": 0.8, "sodium_mg": 35.0},
    hierarchy=EastIndianHierarchy(
        level3_state="Bihar", level4_region="Nalanda / Silao", level5_cuisine="Bihari",
        level6_food_family="Sweets", level7_food_type="Khaja", level8_variant="Silao Khaja",
        level9_cooking_method=["deep_fried", "syrup_dipped"], default_portion="1 piece (60g)",
        nutrition_ref_id="br_sweet_silao_khaja"
    )
))

# =============================================================================
# 14. JHARKHAND: DHUSKA, WILD FOODS & SAAG (Sections 30, 31, 32)
# =============================================================================

register_east_food(EastIndianFoodClass(
    canonical_food_id="JH_SNACK_DHUSKA",
    canonical_name="Jharkhandi Dhuska",
    state="Jharkhand",
    region="Chota Nagpur / Ranchi",
    cuisine="Jharkhandi",
    food_category="Breakfast",
    regional_names={"English": "Deep-Fried Fermented Rice & Chana Dal Savory Bread", "Hindi": "धुस्का", "Bhojpuri": "धुस्का"},
    alternate_names=["dhuska", "ranchi dhuska", "dhuska with ghugni"],
    vegetarian=True,
    gravy_type="dry",
    visual_features={"shape": "round_puffed_golden_yellow_disc", "crust": "crispy_exterior_with_soft_spongy_interior", "sides": ["chana_ghugni", "aloo_dum", "spicy_tomato_garlic_chutney"]},
    key_ingredients=["soaked rice", "chana dal (bengal gram)", "urad dal minor", "cumin seeds", "ginger paste", "green chillies", "hing", "turmeric", "mustard oil for deep frying"],
    hard_negatives=["SOUTH_INDIAN_MEDU_VADA", "NI_BREAD_PURI_WHEAT", "WB_BREAD_LUCHI"],
    density_g_cm3=0.62,
    default_serving_weight_g=45.0,
    nutrition_per_100g={"calories": 285.0, "protein_g": 6.8, "carbs_g": 38.5, "fat_g": 12.0, "fiber_g": 3.0, "sodium_mg": 240.0},
    hierarchy=EastIndianHierarchy(
        level3_state="Jharkhand", level4_region="Chota Nagpur / Ranchi", level5_cuisine="Jharkhandi",
        level6_food_family="Breakfast", level7_food_type="Dhuska", level8_variant="Ranchi Dhuska",
        level9_cooking_method=["batter_ground", "deep_fried"], default_portion="3 discs (135g)",
        nutrition_ref_id="jh_snack_dhuska"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="JH_BREAD_CHILKA_ROTI",
    canonical_name="Chilka Roti",
    state="Jharkhand",
    region="Chota Nagpur",
    cuisine="Jharkhandi",
    food_category="Breakfast",
    regional_names={"English": "Jharkhandi Rice & Lentil Crepe", "Hindi": "चिल्का रोटी"},
    alternate_names=["chilka pitha", "rice crepe jharkhand"],
    vegetarian=True,
    gravy_type="dry",
    visual_features={"shape": "thin_soft_flexible_crepe", "color": "pale_ivory_yellowish", "surface": "mild_tawa_brown_spots"},
    key_ingredients=["rice", "chana dal or urad dal", "water", "salt", "light oil for tawa"],
    hard_negatives=["SOUTH_INDIAN_DOSA", "WB_SWEET_PATISHAPTA"],
    density_g_cm3=0.74,
    default_serving_weight_g=70.0,
    nutrition_per_100g={"calories": 180.0, "protein_g": 4.8, "carbs_g": 34.0, "fat_g": 2.8, "fiber_g": 1.8, "sodium_mg": 180.0},
    hierarchy=EastIndianHierarchy(
        level3_state="Jharkhand", level4_region="Chota Nagpur", level5_cuisine="Jharkhandi",
        level6_food_family="Breakfast", level7_food_type="Crepe", level8_variant="Chilka Roti",
        level9_cooking_method=["tawa_griddled"], default_portion="2 rotis (140g)",
        nutrition_ref_id="jh_bread_chilka_roti"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="JH_CURRY_RUGRA",
    canonical_name="Rugra Mushroom Curry",
    state="Jharkhand",
    region="Chota Nagpur Forests",
    cuisine="Jharkhandi",
    food_category="Vegetarian",
    regional_names={"English": "Wild Terrestrial Sal-Forest Puffball Mushroom Curry", "Hindi": "रुगड़ा की सब्जी", "Bhojpuri": "रुगड़ा"},
    alternate_names=["rugda", "phutka", "sal mushroom curry"],
    vegetarian=True,
    gravy_type="semi_gravy",
    visual_features={"mushroom": "small_round_hard_black_or_grey_globes_with_white_or_black_meaty_interior", "gravy": "thick_spicy_dark_onion_garlic_garam_masala_gravy"},
    key_ingredients=["wild indigenous rugra / rugda puffball mushrooms", "onions", "ginger garlic paste", "garam masala", "mustard oil", "green chillies"],
    density_g_cm3=0.98,
    default_serving_weight_g=180.0,
    nutrition_per_100g={"calories": 125.0, "protein_g": 4.8, "carbs_g": 8.5, "fat_g": 7.8, "fiber_g": 3.8, "sodium_mg": 260.0},
    hierarchy=EastIndianHierarchy(
        level3_state="Jharkhand", level4_region="Chota Nagpur Forests", level5_cuisine="Jharkhandi",
        level6_food_family="Vegetarian", level7_food_type="Wild Mushroom Curry", level8_variant="Rugra Masala",
        level9_cooking_method=["sauteed", "slow_simmered"], default_portion="1 bowl (180g)",
        nutrition_ref_id="jh_curry_rugra"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="JH_SAAG_KOINAR",
    canonical_name="Koinar Saag",
    state="Jharkhand",
    region="Tribal Jharkhand",
    cuisine="Jharkhandi",
    food_category="Vegetarian",
    regional_names={"English": "Indigenous Bauhinia Leaf Stir Fry", "Hindi": "कोइनार साग"},
    alternate_names=["kachnar leaves", "koinar bhaji"],
    vegetarian=True,
    gravy_type="dry",
    visual_features={"leaves": "dark_green_folded_young_bauhinia_leaves", "tempering": ["garlic_cloves", "dry_red_chilli", "mustard_oil"]},
    key_ingredients=["tender koinar leaves", "garlic", "green/dry red chilli", "mustard oil", "salt"],
    density_g_cm3=0.80,
    default_serving_weight_g=120.0,
    nutrition_per_100g={"calories": 85.0, "protein_g": 3.2, "carbs_g": 7.5, "fat_g": 4.8, "fiber_g": 3.9, "sodium_mg": 170.0},
    hierarchy=EastIndianHierarchy(
        level3_state="Jharkhand", level4_region="Tribal Jharkhand", level5_cuisine="Jharkhandi",
        level6_food_family="Vegetarian", level7_food_type="Saag", level8_variant="Koinar Saag",
        level9_cooking_method=["boiled", "stir_fried"], default_portion="1 cup (120g)",
        nutrition_ref_id="jh_saag_koinar"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="JH_CURRY_BAMBOO_SHOOT",
    canonical_name="Karil (Bamboo Shoot) Curry",
    state="Jharkhand",
    region="Tribal Jharkhand",
    cuisine="Jharkhandi",
    food_category="Vegetarian",
    regional_names={"English": "Tender Wild Bamboo Shoot Curry", "Hindi": "करील (बांस की सब्जी)"},
    alternate_names=["bamboo shoot curry", "sandhna", "karil sabzi"],
    vegetarian=True,
    gravy_type="semi_gravy",
    visual_features={"vegetable": "fibrous_pale_yellow_shredded_or_chunked_shoots", "gravy": "mustard_or_onion_spiced_gravy"},
    key_ingredients=["fermented or fresh tender bamboo shoots (karil)", "mustard oil", "garlic", "onion", "turmeric", "spices"],
    density_g_cm3=0.92,
    default_serving_weight_g=180.0,
    nutrition_per_100g={"calories": 95.0, "protein_g": 2.6, "carbs_g": 9.2, "fat_g": 5.4, "fiber_g": 4.2, "sodium_mg": 220.0},
    hierarchy=EastIndianHierarchy(
        level3_state="Jharkhand", level4_region="Tribal Jharkhand", level5_cuisine="Jharkhandi",
        level6_food_family="Vegetarian", level7_food_type="Bamboo Shoot Curry", level8_variant="Karil Curry",
        level9_cooking_method=["stewed"], default_portion="1 bowl (180g)",
        nutrition_ref_id="jh_curry_bamboo_shoot"
    )
))

# =============================================================================
# 15. EAST INDIAN THALIS & UNKNOWN / OOD CLASS (Sections 33, 48)
# =============================================================================

register_east_food(EastIndianFoodClass(
    canonical_food_id="EI_THALI_BENGALI",
    canonical_name="Bengali Feast Thali",
    state="West Bengal",
    region="Kolkata",
    cuisine="Bengali",
    food_category="Thali",
    regional_names={"English": "Traditional Multi-Course Bengali Meal", "Bengali": "বাঙালি থালা", "Hindi": "बंगाली थाली"},
    alternate_names=["bengali thali", "bhoj thali"],
    vegetarian=False,
    gravy_type=None,
    visual_features={"layout": "central_steamed_rice_surrounded_by_katoris", "items": ["rice", "dal", "shukto", "begun_bhaja", "fish_or_mutton", "chutney", "mishti_doi"]},
    key_ingredients=["rice", "dal", "fish or meat", "vegetable dishes", "chutney", "mishti doi"],
    density_g_cm3=0.88,
    default_serving_weight_g=650.0,
    nutrition_per_100g={"calories": 165.0, "protein_g": 7.2, "carbs_g": 22.0, "fat_g": 5.5, "fiber_g": 1.8, "sodium_mg": 280.0},
    hierarchy=EastIndianHierarchy(
        level3_state="West Bengal", level4_region="Kolkata", level5_cuisine="Bengali",
        level6_food_family="Thali", level7_food_type="Thali Platter", level8_variant="Bengali Full Thali",
        level9_cooking_method=["composite_service"], default_portion="1 full meal (650g)",
        nutrition_ref_id="ei_thali_bengali"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="EI_THALI_ODIA",
    canonical_name="Odia Traditional Thali",
    state="Odisha",
    region="Coastal Odisha",
    cuisine="Odia",
    food_category="Thali",
    regional_names={"English": "Traditional Odia Thali", "Odia": "ଓଡ଼ିଆ ଥାଳି", "Hindi": "ओड़िया थाली"},
    alternate_names=["odia thali", "odia bhojan"],
    vegetarian=False,
    gravy_type=None,
    visual_features={"layout": "rice_surrounded_by_dalma_santula_bhaja_fish_or_chhena_sweets"},
    key_ingredients=["rice", "dalma", "santula", "baigana bhaja", "fish or besara", "khatta", "chhena sweet"],
    density_g_cm3=0.88,
    default_serving_weight_g=620.0,
    nutrition_per_100g={"calories": 150.0, "protein_g": 6.5, "carbs_g": 21.0, "fat_g": 4.8, "fiber_g": 2.2, "sodium_mg": 260.0},
    hierarchy=EastIndianHierarchy(
        level3_state="Odisha", level4_region="Coastal Odisha", level5_cuisine="Odia",
        level6_food_family="Thali", level7_food_type="Thali Platter", level8_variant="Odia Traditional Thali",
        level9_cooking_method=["composite_service"], default_portion="1 full meal (620g)",
        nutrition_ref_id="ei_thali_odia"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="EI_THALI_BIHARI",
    canonical_name="Bihari Litti Thali",
    state="Bihar",
    region="Bhojpur / Magadh",
    cuisine="Bihari",
    food_category="Thali",
    regional_names={"English": "Traditional Bihari Litti Chokha Meal", "Hindi": "बिहारी थाली", "Bhojpuri": "बिहारी थाली"},
    alternate_names=["litti chokha thali", "bihari meal"],
    vegetarian=False,
    gravy_type=None,
    visual_features={"items": ["litti", "baingan_chokha", "aloo_chokha", "dal", "ghee", "mutton_or_chicken", "salad"]},
    key_ingredients=["litti", "baingan chokha", "aloo chokha", "dal", "ghee", "pickle"],
    density_g_cm3=0.90,
    default_serving_weight_g=600.0,
    nutrition_per_100g={"calories": 175.0, "protein_g": 7.5, "carbs_g": 24.0, "fat_g": 5.8, "fiber_g": 3.2, "sodium_mg": 290.0},
    hierarchy=EastIndianHierarchy(
        level3_state="Bihar", level4_region="Bhojpur / Magadh", level5_cuisine="Bihari",
        level6_food_family="Thali", level7_food_type="Thali Platter", level8_variant="Bihari Litti Meal",
        level9_cooking_method=["composite_service"], default_portion="1 full meal (600g)",
        nutrition_ref_id="ei_thali_bihari"
    )
))

register_east_food(EastIndianFoodClass(
    canonical_food_id="EAST_INDIAN_UNKNOWN",
    canonical_name="East Indian Unknown / Needs Confirmation",
    state="East India",
    region="Uncertain",
    cuisine="East Indian",
    food_category="Unknown",
    regional_names={"English": "Unknown East Indian Food", "Bengali": "অজ্ঞাত পূর্ব ভারতীয় খাবার", "Hindi": "अज्ञात पूर्वी भारतीय भोजन"},
    alternate_names=["unknown", "unrecognized", "needs confirmation"],
    vegetarian=True,
    gravy_type=None,
    visual_features={"evidence": "insufficient_or_ambiguous"},
    key_ingredients=[],
    density_g_cm3=0.85,
    default_serving_weight_g=150.0,
    nutrition_per_100g={"calories": 0.0, "protein_g": 0.0, "carbs_g": 0.0, "fat_g": 0.0, "fiber_g": 0.0, "sodium_mg": 0.0},
    hierarchy=EastIndianHierarchy(
        level3_state="East India", level4_region="Uncertain", level5_cuisine="East Indian",
        level6_food_family="Unknown", level7_food_type="Unknown", level8_variant="Unknown",
        level9_cooking_method=["unknown"], default_portion="unknown",
        nutrition_ref_id="ei_unknown"
    )
))
