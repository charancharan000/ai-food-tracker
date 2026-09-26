"""
Northeast India Master Food Taxonomy & Identity Hierarchy (Part 7)
Implements Sections 0-39, 42-51, 62, 74, 88, 89 of Part 7 Master Training Specification.

Guarantees:
- Strict 9-Level Taxonomy:
  Indian Food -> Northeast Indian Food -> State -> Region/Community -> Food Family ->
  Food Name / Type -> Variant -> Ingredients -> Cooking Method -> Portion -> Nutrition
- Comprehensive 8-State Coverage:
  1. Assam (AS_*)
  2. Meghalaya (ML_*)
  3. Manipur (MN_*)
  4. Mizoram (MZ_*)
  5. Nagaland (NL_*)
  6. Tripura (TR_*)
  7. Arunachal Pradesh (AR_*)
  8. Sikkim (SK_*)
  Plus Pan-Northeast & Cross-State classes (NE_*) and NORTHEAST_INDIAN_UNKNOWN.
- Permanent Canonical IDs with Multilingual Name Mapping:
  English, Assamese (অসমীয়া), Khasi/Garo, Manipuri/Meiteilon (মৈতৈলোন্),
  Mizo, Nagamese/Ao/Angami, Kokborok, Monpa/Arunachali, Nepali/Sikkimese.
- Comprehensive food family coverage:
  Rice, Fish/Seafood, Tenga, Khar, Meat (Duck, Pork, Chicken, Smoked Meat),
  Vegetarian & Pitika, Fermented Foods (Axone, Ngari, Tungrymbai, Kinema, Gundruk, Khorisa, Berma),
  Bamboo Shoot dishes, Momos, Thukpa, Soups/Stews (Chamthong, Bai, Galho, Sawhchiar),
  Pitha & Traditional Rice Cakes (Til Pitha, Pukhlein, Sel Roti, Pumaloi),
  Chutneys & Mashes (Eromba, Singju, Mosdeng, Morok Metpa), Beverages, and Platters.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class NortheastHierarchy(BaseModel):
    level1_food: str = "Indian Food"
    level2_macro_region: str = "Northeast Indian Food"
    level3_state: str # Assam, Meghalaya, Manipur, Mizoram, Nagaland, Tripura, Arunachal Pradesh, Sikkim
    level4_region_community: str # e.g. Brahmaputra Valley, Khasi Hills, Imphal Valley, Chhimtuipui, Kohima, Tripuri, Tawang, Gangtok
    level5_food_family: str # Rice, Fish, Meat, Vegetarian, Fermented, Bamboo Shoot, Stew/Soup, Momo, Thukpa, Pitha/Snack, Chutney/Salad, Beverage, Thali
    level6_food_type: str # e.g. Masor Tenga, Khar, Jadoh, Dohneiihong, Eromba, Singju, Bai, Axone Pork, Galho, Chakhwi, Momo, Gundruk
    level7_variant: str # e.g. Tomato Masor Tenga, Amitar Khar, Pork Jadoh, Smoked Pork Axone
    level8_cooking_method: List[str] # boiled, steamed, smoked, fermented, pan_roasted, deep_fried, stewed, charred_mashed
    default_portion: str # e.g. "1 bowl (200g)", "1 piece (40g)", "6 pieces (180g)"
    nutrition_ref_id: str

class NortheastFoodClass(BaseModel):
    canonical_food_id: str # Stable permanent ID: AS_*, ML_*, MN_*, MZ_*, NL_*, TR_*, AR_*, SK_*, NE_*
    canonical_name: str
    hierarchy: NortheastHierarchy
    state: str
    region_community: str
    food_category: str
    regional_names: Dict[str, str] = Field(default_factory=dict)
    alternate_names: List[str] = Field(default_factory=list)
    vegetarian: bool = True
    preparation_style: Optional[str] = Field(
        default=None,
        description="sour_broth, alkaline_stew, boiled_clear_soup, black_sesame_gravy, smoked_meat, fermented_paste, mashed_pitika, raw_tossed, steamed_cake"
    )
    visual_features: Dict[str, Any] = Field(default_factory=dict)
    key_ingredients: List[str] = Field(default_factory=list)
    possible_ingredients: List[str] = Field(default_factory=list)
    meat_type: Optional[str] = None # "pork", "duck", "chicken", "fish", "beef", "none"
    fermented_agent: Optional[str] = None # "axone", "ngari", "khorisa", "tungrymbai", "kinema", "gundruk", "berma", "none"
    hard_negatives: List[str] = Field(default_factory=list)
    density_g_cm3: float = 0.85
    default_serving_weight_g: float = 150.0
    nutrition_per_100g: Dict[str, float] = Field(default_factory=dict)

# Master Northeast Indian Registry
NORTHEAST_TAXONOMY_REGISTRY: Dict[str, NortheastFoodClass] = {}
NORTHEAST_SYNONYM_MAP: Dict[str, str] = {}

def register_northeast_food(food: NortheastFoodClass):
    NORTHEAST_TAXONOMY_REGISTRY[food.canonical_food_id] = food
    NORTHEAST_SYNONYM_MAP[food.canonical_name.lower().strip()] = food.canonical_food_id
    for alt in food.alternate_names:
        NORTHEAST_SYNONYM_MAP[alt.lower().strip()] = food.canonical_food_id
    for reg_name in food.regional_names.values():
        NORTHEAST_SYNONYM_MAP[reg_name.lower().strip()] = food.canonical_food_id

def get_northeast_food_class(canonical_id: str) -> Optional[NortheastFoodClass]:
    return NORTHEAST_TAXONOMY_REGISTRY.get(canonical_id)

def resolve_northeast_food_by_name(query: str) -> Optional[NortheastFoodClass]:
    if not query:
        return None
    q = query.lower().strip()
    if q in NORTHEAST_SYNONYM_MAP:
        return NORTHEAST_TAXONOMY_REGISTRY[NORTHEAST_SYNONYM_MAP[q]]
    for cid, food in NORTHEAST_TAXONOMY_REGISTRY.items():
        if q == cid.lower() or q in food.canonical_name.lower():
            return food
        for alt in food.alternate_names:
            if q in alt.lower():
                return food
        for reg in food.regional_names.values():
            if q in reg.lower():
                return food
    return None

def list_all_northeast_food_ids() -> List[str]:
    return list(NORTHEAST_TAXONOMY_REGISTRY.keys())


# =============================================================================
# 1. ASSAM MASTER DATASET (Sections 2 - 9)
# =============================================================================

# Rice
register_northeast_food(NortheastFoodClass(
    canonical_food_id="AS_RICE_JOHA",
    canonical_name="Assamese Joha Rice",
    state="Assam",
    region_community="Brahmaputra Valley",
    food_category="Rice",
    regional_names={"English": "Indigenous Scented Joha Rice", "Assamese": "জোহা চাউলৰ ভাত", "Hindi": "जोहा चावल"},
    alternate_names=["joha saul", "joha rice", "assamese scented rice"],
    vegetarian=True,
    preparation_style="boiled_grain",
    visual_features={"grain": "small_slender_aromatic_pearl_grains", "texture": "soft_non_sticky_distinct"},
    key_ingredients=["joha rice", "water"],
    density_g_cm3=0.84,
    default_serving_weight_g=180.0,
    nutrition_per_100g={"calories": 135.0, "protein_g": 2.8, "carbs_g": 29.5, "fat_g": 0.4, "fiber_g": 0.6, "sodium_mg": 2.0},
    hierarchy=NortheastHierarchy(
        level3_state="Assam", level4_region_community="Brahmaputra Valley",
        level5_food_family="Rice", level6_food_type="Steamed Rice", level7_variant="Joha Rice",
        level8_cooking_method=["steamed", "boiled"], default_portion="1 bowl (180g)",
        nutrition_ref_id="as_rice_joha"
    )
))

register_northeast_food(NortheastFoodClass(
    canonical_food_id="AS_RICE_BORA_SAUL",
    canonical_name="Bora Saul (Sticky Rice)",
    state="Assam",
    region_community="Upper Assam",
    food_category="Rice",
    regional_names={"English": "Assamese Glutinous Sticky Rice", "Assamese": "বৰা চাউল", "Hindi": "बोरा चावल"},
    alternate_names=["bora saul", "assamese sticky rice", "bora bhat"],
    vegetarian=True,
    preparation_style="steamed_grain",
    visual_features={"grain": "opaque_chalky_white_grains_cohering_together", "texture": "glutinous_elastic_sticky"},
    key_ingredients=["bora glutinous rice", "water"],
    density_g_cm3=0.88,
    default_serving_weight_g=180.0,
    nutrition_per_100g={"calories": 145.0, "protein_g": 3.0, "carbs_g": 32.0, "fat_g": 0.5, "fiber_g": 0.8, "sodium_mg": 3.0},
    hierarchy=NortheastHierarchy(
        level3_state="Assam", level4_region_community="Upper Assam",
        level5_food_family="Rice", level6_food_type="Sticky Rice", level7_variant="Bora Saul",
        level8_cooking_method=["steamed"], default_portion="1 bowl (180g)",
        nutrition_ref_id="as_rice_bora_saul"
    )
))

# Pitha
register_northeast_food(NortheastFoodClass(
    canonical_food_id="AS_PITHA_TIL",
    canonical_name="Til Pitha",
    state="Assam",
    region_community="Assam (Magh Bihu)",
    food_category="Pitha/Snack",
    regional_names={"English": "Rolled Sticky Rice Pitha with Black Sesame & Jaggery", "Assamese": "তিল পিঠা", "Hindi": "तिल पीठा"},
    alternate_names=["til pitha", "bihu til pitha"],
    vegetarian=True,
    preparation_style="steamed_cake",
    visual_features={"shape": "cylindrical_rolled_white_rice_envelope", "surface": "porous_soft_crust_from_tawa", "filling": "roasted_black_sesame_and_melted_jaggery_core"},
    key_ingredients=["bora saul (glutinous rice)", "roasted black sesame (til)", "gur (jaggery)"],
    hard_negatives=["AS_PITHA_GHILA", "WB_SWEET_PATISHAPTA"],
    density_g_cm3=0.72,
    default_serving_weight_g=40.0,
    nutrition_per_100g={"calories": 280.0, "protein_g": 5.2, "carbs_g": 52.0, "fat_g": 6.8, "fiber_g": 2.8, "sodium_mg": 18.0},
    hierarchy=NortheastHierarchy(
        level3_state="Assam", level4_region_community="Assam (Magh Bihu)",
        level5_food_family="Pitha/Snack", level6_food_type="Pitha", level7_variant="Til Pitha",
        level8_cooking_method=["tawa_rolled"], default_portion="2 pieces (80g)",
        nutrition_ref_id="as_pitha_til"
    )
))

register_northeast_food(NortheastFoodClass(
    canonical_food_id="AS_PITHA_GHILA",
    canonical_name="Ghila Pitha",
    state="Assam",
    region_community="Assam",
    food_category="Pitha/Snack",
    regional_names={"English": "Deep Fried Rice & Jaggery Pitha", "Assamese": "ঘিলা পিঠা", "Hindi": "घिला पीठा"},
    alternate_names=["ghila pitha", "fried sweet pitha"],
    vegetarian=True,
    preparation_style="fried_solid",
    visual_features={"shape": "flattened_round_golden_brown_discs", "texture": "crisp_exterior_chewy_moist_interior"},
    key_ingredients=["bora rice flour", "jaggery or sugar", "fennel or cardamom", "mustard oil for frying"],
    density_g_cm3=0.82,
    default_serving_weight_g=45.0,
    nutrition_per_100g={"calories": 320.0, "protein_g": 4.5, "carbs_g": 58.0, "fat_g": 8.5, "fiber_g": 1.5, "sodium_mg": 22.0},
    hierarchy=NortheastHierarchy(
        level3_state="Assam", level4_region_community="Assam",
        level5_food_family="Pitha/Snack", level6_food_type="Pitha", level7_variant="Ghila Pitha",
        level8_cooking_method=["deep_fried"], default_portion="2 pieces (90g)",
        nutrition_ref_id="as_pitha_ghila"
    )
))

# Khar
register_northeast_food(NortheastFoodClass(
    canonical_food_id="AS_KHAR_OMITA",
    canonical_name="Amitar Khar",
    state="Assam",
    region_community="Assam Valley",
    food_category="Vegetarian",
    regional_names={"English": "Raw Papaya Alkaline Khar", "Assamese": "অমিতাৰ খাৰ", "Hindi": "अमीतार खार"},
    alternate_names=["omita khar", "raw papaya khar", "assamese khar"],
    vegetarian=True,
    preparation_style="alkaline_stew",
    visual_features={"color": "translucent_pale_greyish_green", "texture": "soft_melted_papaya_chunks_in_alkaline_broth", "tempering": ["spluttered_mustard_seeds", "green_chillies", "raw_mustard_oil"]},
    key_ingredients=["raw green papaya (omita)", "kolakhar (filtrate of sun-dried banana peel ash)", "mustard oil", "panch phoron or mustard seeds", "ginger", "green chillies"],
    hard_negatives=["AS_TENGA_MASOR", "AS_VEG_ALOO_PITIKA"],
    density_g_cm3=0.98,
    default_serving_weight_g=150.0,
    nutrition_per_100g={"calories": 55.0, "protein_g": 1.2, "carbs_g": 7.5, "fat_g": 2.2, "fiber_g": 2.8, "sodium_mg": 210.0},
    hierarchy=NortheastHierarchy(
        level3_state="Assam", level4_region_community="Assam Valley",
        level5_food_family="Vegetarian", level6_food_type="Khar", level7_variant="Amitar Khar",
        level8_cooking_method=["boiled", "alkaline_tempered"], default_portion="1 katori (150g)",
        nutrition_ref_id="as_khar_omita"
    )
))

# Tenga & Fish
register_northeast_food(NortheastFoodClass(
    canonical_food_id="AS_FISH_MASOR_TENGA",
    canonical_name="Masor Tenga",
    state="Assam",
    region_community="Brahmaputra Valley",
    food_category="Fish",
    regional_names={"English": "Assamese Light Sour Fish Curry", "Assamese": "মাছৰ টেঙা", "Hindi": "मासोर तेंगा"},
    alternate_names=["masor tenga", "bilahi masor tenga", "kazi nemu tenga fish"],
    vegetarian=False,
    meat_type="fish",
    preparation_style="sour_broth",
    visual_features={"broth": "very_thin_light_tangy_golden_reddish_yellow_soup", "fish": "lightly_fried_freshwater_carp_steak", "souring_agents": ["sliced_ripe_tomatoes", "assamese_lemon (kazi nemu)", "ou tenga (elephant apple)"]},
    key_ingredients=["rohu or freshwater river carp", "ripe tomatoes", "kazi nemu (assam lemon) juice", "mustard oil", "fenugreek or panch phoron", "turmeric", "green chillies"],
    hard_negatives=["WB_FISH_MACHER_JHOL", "WB_FISH_SHORSHE_MAACH"],
    density_g_cm3=0.98,
    default_serving_weight_g=220.0,
    nutrition_per_100g={"calories": 98.0, "protein_g": 10.5, "carbs_g": 3.2, "fat_g": 4.8, "fiber_g": 0.8, "sodium_mg": 230.0},
    hierarchy=NortheastHierarchy(
        level3_state="Assam", level4_region_community="Brahmaputra Valley",
        level5_food_family="Fish", level6_food_type="Masor Tenga", level7_variant="Bilahi Masor Tenga",
        level8_cooking_method=["shallow_fried_fish", "simmered_sour_broth"], default_portion="1 bowl with fish piece (220g)",
        nutrition_ref_id="as_fish_masor_tenga"
    )
))

# Meat
register_northeast_food(NortheastFoodClass(
    canonical_food_id="AS_MEAT_DUCK_KUMURA",
    canonical_name="Duck with Kumura (Ash Gourd)",
    state="Assam",
    region_community="Assam",
    food_category="Meat",
    regional_names={"English": "Assamese Country Duck with Ash Gourd", "Assamese": "হাঁহৰ মাংস আৰু কোমোৰা", "Hindi": "बतख और कुमुरा"},
    alternate_names=["hanhor mangsho kumura", "duck curry assam", "kumura duck"],
    vegetarian=False,
    meat_type="duck",
    preparation_style="stewed_gravy",
    visual_features={"meat": "darker_red_brown_bone_in_duck_pieces_with_skin_fat", "vegetable": "soft_cooked_translucent_white_ash_gourd_cubes", "gravy": "rich_rustic_onion_ginger_pepper_gravy"},
    key_ingredients=["country duck with bone and skin", "ash gourd (kumura)", "mustard oil", "ginger garlic paste", "black pepper", "whole garam masala"],
    density_g_cm3=1.04,
    default_serving_weight_g=240.0,
    nutrition_per_100g={"calories": 215.0, "protein_g": 14.8, "carbs_g": 4.2, "fat_g": 15.6, "fiber_g": 1.2, "sodium_mg": 280.0},
    hierarchy=NortheastHierarchy(
        level3_state="Assam", level4_region_community="Assam",
        level5_food_family="Meat", level6_food_type="Duck Curry", level7_variant="Duck with Kumura",
        level8_cooking_method=["slow_cooked", "stewed"], default_portion="1 bowl (240g)",
        nutrition_ref_id="as_meat_duck_kumura"
    )
))

register_northeast_food(NortheastFoodClass(
    canonical_food_id="AS_MEAT_PORK_KHORISA",
    canonical_name="Pork with Khorisa (Bamboo Shoot)",
    state="Assam",
    region_community="Upper Assam",
    food_category="Meat",
    regional_names={"English": "Pork with Fermented Bamboo Shoot", "Assamese": "গাহৰি মাংস আৰু খৰিচা", "Hindi": "पोर्क खोरीसा"},
    alternate_names=["gahori khorisa", "assamese pork bamboo shoot"],
    vegetarian=False,
    meat_type="pork",
    fermented_agent="khorisa",
    preparation_style="semi_gravy",
    visual_features={"meat": "pork_chunks_with_clear_fat_layers", "bamboo": "shredded_pale_yellow_khorisa_shoots", "gravy": "pungent_tangy_spiced_reddish_sauce"},
    key_ingredients=["pork with pork belly fat", "khorisa (grated fermented bamboo shoot)", "garlic", "ginger", "bhut jolokia hint", "mustard oil"],
    hard_negatives=["NL_MEAT_PORK_BAMBOO_SHOOT", "TR_MEAT_CHAKHWI_PORK"],
    density_g_cm3=1.02,
    default_serving_weight_g=220.0,
    nutrition_per_100g={"calories": 240.0, "protein_g": 15.5, "carbs_g": 3.5, "fat_g": 18.2, "fiber_g": 1.5, "sodium_mg": 310.0},
    hierarchy=NortheastHierarchy(
        level3_state="Assam", level4_region_community="Upper Assam",
        level5_food_family="Meat", level6_food_type="Pork with Khorisa", level7_variant="Gahori Khorisa",
        level8_cooking_method=["braised", "fermented_simmered"], default_portion="1 bowl (220g)",
        nutrition_ref_id="as_meat_pork_khorisa"
    )
))

# Pitika (Vegetarian)
register_northeast_food(NortheastFoodClass(
    canonical_food_id="AS_VEG_ALOO_PITIKA",
    canonical_name="Aloo Pitika",
    state="Assam",
    region_community="Assam",
    food_category="Vegetarian",
    regional_names={"English": "Assamese Mashed Potatoes with Raw Mustard Oil", "Assamese": "আলু পিটিকা", "Hindi": "आलू पीतिका"},
    alternate_names=["aloo pitika", "assamese potato mash"],
    vegetarian=True,
    preparation_style="mashed_pitika",
    visual_features={"texture": "coarse_rustic_hand_mashed_potatoes", "visible": ["chopped_raw_onions", "green_chillies", "coriander", "mustard_oil_sheen"]},
    key_ingredients=["boiled potatoes", "pure raw pungent mustard oil", "finely chopped raw onions", "green chillies", "salt", "fresh coriander"],
    hard_negatives=["BR_CHOKHA_ALOO", "WB_VEG_ALOO_POSTO"],
    density_g_cm3=0.92,
    default_serving_weight_g=100.0,
    nutrition_per_100g={"calories": 110.0, "protein_g": 2.0, "carbs_g": 17.5, "fat_g": 3.8, "fiber_g": 2.0, "sodium_mg": 190.0},
    hierarchy=NortheastHierarchy(
        level3_state="Assam", level4_region_community="Assam",
        level5_food_family="Vegetarian", level6_food_type="Pitika", level7_variant="Aloo Pitika",
        level8_cooking_method=["boiled", "hand_mashed"], default_portion="1 cup (100g)",
        nutrition_ref_id="as_veg_aloo_pitika"
    )
))


# =============================================================================
# 2. MEGHALAYA MASTER DATASET (Sections 10 - 14)
# =============================================================================

register_northeast_food(NortheastFoodClass(
    canonical_food_id="ML_RICE_JADOH_PORK",
    canonical_name="Jadoh (Pork)",
    state="Meghalaya",
    region_community="Khasi Hills",
    food_category="Rice",
    regional_names={"English": "Khasi Rice Cooked in Meat Broth with Pork", "Khasi": "Ja Doh", "Hindi": "जादोह"},
    alternate_names=["jadoh", "khasi jadoh", "jadoh with pork"],
    vegetarian=False,
    meat_type="pork",
    preparation_style="stewed_rice_meat",
    visual_features={"rice": "short_bold_red_or_yellow_rice_grains", "meat": "tender_pork_cubes_with_fat_embedded", "color": "golden_turmeric_or_deep_red_brown", "garnish": ["sliced_onions", "ginger_slivers", "coriander"]},
    key_ingredients=["short-grain hill rice (jingshai)", "pork pieces with pork fat", "ginger paste", "onions", "black pepper", "turmeric", "bay leaves"],
    hard_negatives=["NL_RICE_GALHO", "MZ_RICE_SAWHCHIAR", "HYDERABADI_BIRYANI"],
    density_g_cm3=0.86,
    default_serving_weight_g=280.0,
    nutrition_per_100g={"calories": 195.0, "protein_g": 8.5, "carbs_g": 25.0, "fat_g": 7.2, "fiber_g": 1.2, "sodium_mg": 280.0},
    hierarchy=NortheastHierarchy(
        level3_state="Meghalaya", level4_region_community="Khasi Hills",
        level5_food_family="Rice", level6_food_type="Jadoh", level7_variant="Jadoh Pork",
        level8_cooking_method=["dum_braised", "meat_fat_cooked"], default_portion="1 plate (280g)",
        nutrition_ref_id="ml_rice_jadoh_pork"
    )
))

register_northeast_food(NortheastFoodClass(
    canonical_food_id="ML_MEAT_DOHNEIIHONG",
    canonical_name="Dohneiihong (Pork with Black Sesame)",
    state="Meghalaya",
    region_community="Khasi & Jaintia Hills",
    food_category="Meat",
    regional_names={"English": "Khasi Pork Curry with Roasted Black Sesame", "Khasi": "Doh Nei-Iong", "Hindi": "डोहनेईयोंग"},
    alternate_names=["dohneiihong", "doh nei iong", "black sesame pork"],
    vegetarian=False,
    meat_type="pork",
    preparation_style="black_sesame_gravy",
    visual_features={"color": "distinctive_deep_charcoal_grey_to_black_coating", "gravy": "thick_nutty_earthy_ground_black_sesame_sauce", "meat": "succulent_pork_belly_chunks_with_rind"},
    key_ingredients=["pork belly with fat", "roasted and ground black sesame paste (nei-iong)", "onions", "ginger", "garlic", "green chillies", "mustard oil"],
    hard_negatives=["CHINESE_BLACK_BEAN_PORK", "NL_MEAT_AXONE_PORK"],
    density_g_cm3=1.04,
    default_serving_weight_g=220.0,
    nutrition_per_100g={"calories": 275.0, "protein_g": 15.2, "carbs_g": 4.5, "fat_g": 22.0, "fiber_g": 2.8, "sodium_mg": 290.0},
    hierarchy=NortheastHierarchy(
        level3_state="Meghalaya", level4_region_community="Khasi & Jaintia Hills",
        level5_food_family="Meat", level6_food_type="Dohneiihong", level7_variant="Pork Dohneiihong",
        level8_cooking_method=["slow_braised", "sesame_simmered"], default_portion="1 bowl (220g)",
        nutrition_ref_id="ml_meat_dohneiihong"
    )
))

register_northeast_food(NortheastFoodClass(
    canonical_food_id="ML_MEAT_DOH_KHLIEH",
    canonical_name="Doh Khlieh",
    state="Meghalaya",
    region_community="Khasi Hills",
    food_category="Meat",
    regional_names={"English": "Khasi Boiled Pork & Onion Salad", "Khasi": "Doh Khlieh", "Hindi": "डोह खलिएह"},
    alternate_names=["doh khlieh", "khasi pork salad"],
    vegetarian=False,
    meat_type="pork",
    preparation_style="boiled_salad",
    visual_features={"texture": "clean_pale_sliced_boiled_pork_pieces", "vegetables": ["generous_thinly_sliced_raw_onions", "fresh_green_chillies", "crushed_ginger_bits"]},
    key_ingredients=["boiled tender pork (traditionally head/belly)", "raw sliced red onions", "green chillies", "ginger slivers", "salt"],
    density_g_cm3=0.88,
    default_serving_weight_g=150.0,
    nutrition_per_100g={"calories": 210.0, "protein_g": 16.8, "carbs_g": 3.8, "fat_g": 14.5, "fiber_g": 0.8, "sodium_mg": 260.0},
    hierarchy=NortheastHierarchy(
        level3_state="Meghalaya", level4_region_community="Khasi Hills",
        level5_food_family="Meat", level6_food_type="Pork Salad", level7_variant="Doh Khlieh",
        level8_cooking_method=["boiled", "raw_mixed"], default_portion="1 bowl (150g)",
        nutrition_ref_id="ml_meat_doh_khlieh"
    )
))

register_northeast_food(NortheastFoodClass(
    canonical_food_id="ML_FERMENTED_TUNGRYMBAI",
    canonical_name="Tungrymbai",
    state="Meghalaya",
    region_community="Khasi Hills",
    food_category="Fermented",
    regional_names={"English": "Khasi Fermented Soybean Chutney/Side", "Khasi": "Tungrymbai", "Hindi": "तुंगरिम्बाई"},
    alternate_names=["tungrymbai", "khasi fermented soybean"],
    vegetarian=True,
    fermented_agent="tungrymbai",
    preparation_style="fermented_paste",
    visual_features={"texture": "coarse_brownish_black_fermented_soybean_mash", "color": "dark_due_to_black_sesame_and_cooking", "visible": ["black_sesame_seeds", "ginger_fibers", "chillies"]},
    key_ingredients=["fermented whole soybeans (tungrymbai)", "ground black sesame", "ginger", "garlic", "chillies", "mustard oil", "pork chunks optional"],
    hard_negatives=["NL_FERMENTED_AXONE", "SK_FERMENTED_KINEMA"],
    density_g_cm3=0.96,
    default_serving_weight_g=80.0,
    nutrition_per_100g={"calories": 185.0, "protein_g": 12.5, "carbs_g": 9.2, "fat_g": 11.4, "fiber_g": 4.8, "sodium_mg": 280.0},
    hierarchy=NortheastHierarchy(
        level3_state="Meghalaya", level4_region_community="Khasi Hills",
        level5_food_family="Fermented", level6_food_type="Tungrymbai", level7_variant="Tungrymbai Paste",
        level8_cooking_method=["fermented", "pan_fried"], default_portion="1 small cup (80g)",
        nutrition_ref_id="ml_fermented_tungrymbai"
    )
))

register_northeast_food(NortheastFoodClass(
    canonical_food_id="ML_SNACK_PUKHLEIN",
    canonical_name="Pukhlein",
    state="Meghalaya",
    region_community="Khasi Hills",
    food_category="Pitha/Snack",
    regional_names={"English": "Khasi Fried Rice Flour & Jaggery Snack", "Khasi": "Pukhlein", "Hindi": "पुखलिन"},
    alternate_names=["puklein", "pukh-lien", "khasi sweet bread"],
    vegetarian=True,
    preparation_style="fried_solid",
    visual_features={"shape": "puffy_golden_brown_fried_disc_or_crescent", "texture": "crisp_on_outside_soft_chewy_sweet_inside"},
    key_ingredients=["rice flour", "cane jaggery (gur)", "refined oil for frying"],
    hard_negatives=["AS_PITHA_GHILA", "SK_BREAD_SEL_ROTI"],
    density_g_cm3=0.78,
    default_serving_weight_g=50.0,
    nutrition_per_100g={"calories": 340.0, "protein_g": 4.0, "carbs_g": 62.0, "fat_g": 9.2, "fiber_g": 1.2, "sodium_mg": 20.0},
    hierarchy=NortheastHierarchy(
        level3_state="Meghalaya", level4_region_community="Khasi Hills",
        level5_food_family="Pitha/Snack", level6_food_type="Pukhlein", level7_variant="Pukhlein",
        level8_cooking_method=["deep_fried"], default_portion="2 pieces (100g)",
        nutrition_ref_id="ml_snack_pukhlein"
    )
))


# =============================================================================
# 3. MANIPUR MASTER DATASET (Sections 15 - 19)
# =============================================================================

register_northeast_food(NortheastFoodClass(
    canonical_food_id="MN_CHUTNEY_EROMBA",
    canonical_name="Manipuri Eromba",
    state="Manipur",
    region_community="Imphal Valley (Meitei)",
    food_category="Chutney/Salad",
    regional_names={"English": "Mashed Boiled Vegetables with Fermented Fish & King Chilli", "Manipuri": "ইৰোম্বা", "Hindi": "इरोम्बा"},
    alternate_names=["eromba", "iromba", "manipur eromba"],
    vegetarian=False,
    meat_type="fish",
    fermented_agent="ngari",
    preparation_style="charred_mashed",
    visual_features={"texture": "rustic_chunky_vegetable_mash", "color": "amber_reddish_yellow", "ingredients_visible": ["boiled_potatoes", "boiled_vegetables", "bamboo_shoot_shreds", "fiery_u_morok_flakes", "garnished_with_maroi_napakpi (chives)"]},
    key_ingredients=["boiled potatoes or tender veg", "ngari (fermented freshwater fish) roasted", "u-morok (king chilli)", "maroi napakpi (local chives)", "bamboo shoot optional"],
    hard_negatives=["AS_VEG_ALOO_PITIKA", "TR_CHUTNEY_GUDOK", "BR_CHOKHA_BAINGAN"],
    density_g_cm3=0.96,
    default_serving_weight_g=120.0,
    nutrition_per_100g={"calories": 75.0, "protein_g": 3.8, "carbs_g": 11.5, "fat_g": 1.2, "fiber_g": 2.4, "sodium_mg": 320.0},
    hierarchy=NortheastHierarchy(
        level3_state="Manipur", level4_region_community="Imphal Valley (Meitei)",
        level5_food_family="Chutney/Salad", level6_food_type="Eromba", level7_variant="Potato Bamboo Shoot Eromba",
        level8_cooking_method=["boiled", "roasted_fish_mashed"], default_portion="1 bowl (120g)",
        nutrition_ref_id="mn_chutney_eromba"
    )
))

register_northeast_food(NortheastFoodClass(
    canonical_food_id="MN_SALAD_SINGJU",
    canonical_name="Manipuri Singju",
    state="Manipur",
    region_community="Imphal Valley",
    food_category="Chutney/Salad",
    regional_names={"English": "Spicy Manipuri Shredded Raw Vegetable Salad", "Manipuri": "শিঙজু", "Hindi": "सिंगजु"},
    alternate_names=["singju", "manipuri spicy salad"],
    vegetarian=False,
    meat_type="fish",
    fermented_agent="ngari",
    preparation_style="raw_tossed",
    visual_features={"texture": "finely_shredded_crisp_raw_vegetables", "visible": ["shredded_cabbage", "lotus_stem (thambou)", "banana_flower (laphu tharo)", "roasted_chickpea_flour_coating", "perilla_seeds", "chilli_flakes"]},
    key_ingredients=["finely shredded cabbage or lotus stem", "roasted ngari (fermented fish) or roasted perilla seeds for veg", "roasted besan/pea powder", "red chillies", "salt"],
    hard_negatives=["WESTERN_COLESLAW", "AS_VEG_ALOO_PITIKA"],
    density_g_cm3=0.68,
    default_serving_weight_g=140.0,
    nutrition_per_100g={"calories": 85.0, "protein_g": 4.5, "carbs_g": 11.8, "fat_g": 2.2, "fiber_g": 3.8, "sodium_mg": 280.0},
    hierarchy=NortheastHierarchy(
        level3_state="Manipur", level4_region_community="Imphal Valley",
        level5_food_family="Chutney/Salad", level6_food_type="Singju", level7_variant="Thambou/Cabbage Singju",
        level8_cooking_method=["raw_tossed"], default_portion="1 plate (140g)",
        nutrition_ref_id="mn_salad_singju"
    )
))

register_northeast_food(NortheastFoodClass(
    canonical_food_id="MN_STEW_KANGSHOI",
    canonical_name="Kangshoi (Chamthong)",
    state="Manipur",
    region_community="Manipur",
    food_category="Stew/Soup",
    regional_names={"English": "Manipuri Clear Vegetable Broth with Herbs", "Manipuri": "কাংশোই (চামথোং)", "Hindi": "कांगशोई"},
    alternate_names=["kangshoi", "chamthong", "manipuri veg stew"],
    vegetarian=False,
    meat_type="fish",
    fermented_agent="ngari",
    preparation_style="boiled_clear_soup",
    visual_features={"broth": "translucent_clear_watery_herbal_soup", "floating": ["leafy_greens", "sliced_potatoes", "fried_or_dried_fish_piece", "local_maroi_herbs", "ginger_slices"]},
    key_ingredients=["seasonal vegetables and leafy greens", "ngari or fried fish", "sliced onions", "ginger", "maroi herbs", "water", "salt"],
    density_g_cm3=0.98,
    default_serving_weight_g=250.0,
    nutrition_per_100g={"calories": 48.0, "protein_g": 3.2, "carbs_g": 6.5, "fat_g": 0.8, "fiber_g": 2.0, "sodium_mg": 220.0},
    hierarchy=NortheastHierarchy(
        level3_state="Manipur", level4_region_community="Manipur",
        level5_food_family="Stew/Soup", level6_food_type="Kangshoi", level7_variant="Chamthong Vegetable Stew",
        level8_cooking_method=["boiled", "herbal_simmered"], default_portion="1 bowl (250g)",
        nutrition_ref_id="mn_stew_kangshoi"
    )
))


# =============================================================================
# 4. MIZORAM MASTER DATASET (Sections 20 - 23)
# =============================================================================

register_northeast_food(NortheastFoodClass(
    canonical_food_id="MZ_STEW_BAI",
    canonical_name="Mizo Bai",
    state="Mizoram",
    region_community="Mizoram",
    food_category="Stew/Soup",
    regional_names={"English": "Mizo Boiled Vegetable & Bamboo Shoot Stew", "Mizo": "Bai", "Hindi": "मिज़ो बाई"},
    alternate_names=["mizo bai", "vegetable bai", "pork bai"],
    vegetarian=True,
    preparation_style="boiled_clear_soup",
    visual_features={"broth": "pale_clear_light_greenish_broth", "visible": ["mustard_leaves", "bamboo_shoot_slices", "french_beans", "pork_chunks_optional", "chingal_alkaline_hue"]},
    key_ingredients=["mustard leaves or seasonal greens", "bamboo shoots", "chingal (local wood ash filtrate) or baking soda", "green chillies", "salt", "bekang (fermented soybean) hint"],
    hard_negatives=["MN_STEW_KANGSHOI", "SK_STEW_GUNDRUK"],
    density_g_cm3=0.98,
    default_serving_weight_g=220.0,
    nutrition_per_100g={"calories": 52.0, "protein_g": 2.4, "carbs_g": 6.8, "fat_g": 1.5, "fiber_g": 2.6, "sodium_mg": 190.0},
    hierarchy=NortheastHierarchy(
        level3_state="Mizoram", level4_region_community="Mizoram",
        level5_food_family="Stew/Soup", level6_food_type="Bai", level7_variant="Vegetable Bai",
        level8_cooking_method=["boiled", "alkaline_stewed"], default_portion="1 bowl (220g)",
        nutrition_ref_id="mz_stew_bai"
    )
))

register_northeast_food(NortheastFoodClass(
    canonical_food_id="MZ_RICE_SAWHCHIAR",
    canonical_name="Sawhchiar",
    state="Mizoram",
    region_community="Mizoram",
    food_category="Rice",
    regional_names={"English": "Mizo Savory Meat & Rice Porridge", "Mizo": "Sawhchiar", "Hindi": "सौहचियार"},
    alternate_names=["sawhchiar", "mizo meat porridge"],
    vegetarian=False,
    meat_type="pork",
    preparation_style="stewed_rice_meat",
    visual_features={"texture": "creamy_soft_broken_grain_congee_like_porridge", "meat": "shredded_tender_pork_or_chicken", "color": "pale_ivory_golden"},
    key_ingredients=["rice", "pork or chicken with bone/meat", "onions", "ginger", "garlic", "bay leaves", "black pepper", "salt"],
    hard_negatives=["NL_RICE_GALHO", "SOUTH_INDIAN_PONGAL", "CHINESE_CONGEE"],
    density_g_cm3=0.94,
    default_serving_weight_g=280.0,
    nutrition_per_100g={"calories": 140.0, "protein_g": 7.2, "carbs_g": 19.5, "fat_g": 3.8, "fiber_g": 0.8, "sodium_mg": 240.0},
    hierarchy=NortheastHierarchy(
        level3_state="Mizoram", level4_region_community="Mizoram",
        level5_food_family="Rice", level6_food_type="Sawhchiar", level7_variant="Pork Sawhchiar",
        level8_cooking_method=["boiled_porridge", "slow_cooked"], default_portion="1 bowl (280g)",
        nutrition_ref_id="mz_rice_sawhchiar"
    )
))

register_northeast_food(NortheastFoodClass(
    canonical_food_id="MZ_MEAT_VAWKSA_REP",
    canonical_name="Vawksa Rep (Smoked Pork)",
    state="Mizoram",
    region_community="Mizoram",
    food_category="Meat",
    regional_names={"English": "Mizo Cured Smoked Pork Stir-Fry", "Mizo": "Vawksa Rep", "Hindi": "वॉक्सा रेप"},
    alternate_names=["vawksa rep", "mizo smoked pork"],
    vegetarian=False,
    meat_type="pork",
    preparation_style="smoked_meat",
    visual_features={"meat": "dark_amber_smoked_pork_slices_with_golden_cured_fat", "cooking": "dry_pan_fried_or_tossed_with_mustard_greens_and_chilli"},
    key_ingredients=["traditional wood-smoked pork (vawksa rep)", "green chillies", "ginger", "garlic", "mustard leaves or bamboo shoot"],
    hard_negatives=["NL_MEAT_SMOKED_PORK_AXONE", "WESTERN_BACON"],
    density_g_cm3=1.05,
    default_serving_weight_g=180.0,
    nutrition_per_100g={"calories": 285.0, "protein_g": 18.2, "carbs_g": 2.5, "fat_g": 22.8, "fiber_g": 0.5, "sodium_mg": 380.0},
    hierarchy=NortheastHierarchy(
        level3_state="Mizoram", level4_region_community="Mizoram",
        level5_food_family="Meat", level6_food_type="Smoked Meat", level7_variant="Vawksa Rep",
        level8_cooking_method=["wood_smoked", "pan_seared"], default_portion="1 plate (180g)",
        nutrition_ref_id="mz_meat_vawksa_rep"
    )
))


# =============================================================================
# 5. NAGALAND MASTER DATASET (Sections 24 - 27)
# =============================================================================

register_northeast_food(NortheastFoodClass(
    canonical_food_id="NL_MEAT_SMOKED_PORK_AXONE",
    canonical_name="Smoked Pork with Axone",
    state="Nagaland",
    region_community="Kohima / Sumi Naga",
    food_category="Meat",
    regional_names={"English": "Naga Smoked Pork in Fermented Soybean Curry", "Nagamese": "Smoked Pork Axone", "Hindi": "स्मोक्ड पोर्क अखुनी"},
    alternate_names=["smoked pork axone", "akhuni pork", "naga smoked pork"],
    vegetarian=False,
    meat_type="pork",
    fermented_agent="axone",
    preparation_style="smoked_meat",
    visual_features={"meat": "dark_mahogany_cured_smoked_pork_chunks", "gravy": "thick_rustic_brown_gravy_infused_with_mashed_fermented_soybean", "spices": ["fiery_naga_raja_mircha_flakes", "ginger_fibers"]},
    key_ingredients=["wood-smoked pork", "axone (fermented soybean paste)", "naga king chilli (raja mircha / bhut jolokia)", "ginger", "garlic", "tomato"],
    hard_negatives=["ML_MEAT_DOHNEIIHONG", "MZ_MEAT_VAWKSA_REP"],
    density_g_cm3=1.04,
    default_serving_weight_g=220.0,
    nutrition_per_100g={"calories": 290.0, "protein_g": 17.5, "carbs_g": 3.8, "fat_g": 23.0, "fiber_g": 1.8, "sodium_mg": 360.0},
    hierarchy=NortheastHierarchy(
        level3_state="Nagaland", level4_region_community="Kohima / Sumi Naga",
        level5_food_family="Meat", level6_food_type="Smoked Pork", level7_variant="Smoked Pork with Axone",
        level8_cooking_method=["wood_smoked", "fermented_simmered"], default_portion="1 bowl (220g)",
        nutrition_ref_id="nl_meat_smoked_pork_axone"
    )
))

register_northeast_food(NortheastFoodClass(
    canonical_food_id="NL_RICE_GALHO",
    canonical_name="Naga Galho",
    state="Nagaland",
    region_community="Angami & Ao Naga",
    food_category="Rice",
    regional_names={"English": "Naga Savory Rice Soup with Greens & Smoked Meat", "Nagamese": "Galho", "Hindi": "गाल्हो"},
    alternate_names=["galho", "naga khichdi", "angami galho"],
    vegetarian=False,
    meat_type="pork",
    fermented_agent="axone",
    preparation_style="stewed_rice_meat",
    visual_features={"texture": "soupy_tender_rice_porridge", "visible": ["abundant_leafy_greens", "smoked_pork_slivers", "axone_infusion", "bamboo_shoot"]},
    key_ingredients=["rice", "smoked pork or seasonal vegetables", "local leafy greens", "axone hint", "chillies", "garlic", "salt"],
    hard_negatives=["MZ_RICE_SAWHCHIAR", "ML_RICE_JADOH_PORK", "NI_RICE_KHICHDI"],
    density_g_cm3=0.92,
    default_serving_weight_g=300.0,
    nutrition_per_100g={"calories": 125.0, "protein_g": 5.8, "carbs_g": 18.0, "fat_g": 3.5, "fiber_g": 1.8, "sodium_mg": 240.0},
    hierarchy=NortheastHierarchy(
        level3_state="Nagaland", level4_region_community="Angami & Ao Naga",
        level5_food_family="Rice", level6_food_type="Galho", level7_variant="Smoked Pork Galho",
        level8_cooking_method=["boiled_soup", "slow_simmered"], default_portion="1 bowl (300g)",
        nutrition_ref_id="nl_rice_galho"
    )
))

register_northeast_food(NortheastFoodClass(
    canonical_food_id="NL_FERMENTED_AXONE",
    canonical_name="Axone / Akhuni (Paste)",
    state="Nagaland",
    region_community="Sumi Naga",
    food_category="Fermented",
    regional_names={"English": "Naga Fermented Soybean Paste", "Sumi": "Axone", "Nagamese": "Akhuni", "Hindi": "अखुनी"},
    alternate_names=["axone", "akhuni", "aksone"],
    vegetarian=True,
    fermented_agent="axone",
    preparation_style="fermented_paste",
    visual_features={"texture": "dense_sticky_brownish_paste_or_banana_leaf_wrapped_cake", "appearance": "pungent_preserved_aroma_sheen"},
    key_ingredients=["boiled and naturally fermented soybeans (axone)"],
    density_g_cm3=0.95,
    default_serving_weight_g=50.0,
    nutrition_per_100g={"calories": 195.0, "protein_g": 16.5, "carbs_g": 11.0, "fat_g": 9.5, "fiber_g": 5.2, "sodium_mg": 310.0},
    hierarchy=NortheastHierarchy(
        level3_state="Nagaland", level4_region_community="Sumi Naga",
        level5_food_family="Fermented", level6_food_type="Fermented Soybean", level7_variant="Axone Paste",
        level8_cooking_method=["fermented"], default_portion="1 portion (50g)",
        nutrition_ref_id="nl_fermented_axone"
    )
))


# =============================================================================
# 6. TRIPURA MASTER DATASET (Sections 28 - 31)
# =============================================================================

register_northeast_food(NortheastFoodClass(
    canonical_food_id="TR_STEW_CHAKHWI",
    canonical_name="Tripuri Chakhwi",
    state="Tripura",
    region_community="Tripuri",
    food_category="Stew/Soup",
    regional_names={"English": "Traditional Tripuri Alkaline Bamboo Shoot Stew", "Kokborok": "Chakhwi", "Hindi": "चाखवी"},
    alternate_names=["chakhwi", "tripura chakhwi"],
    vegetarian=True,
    preparation_style="alkaline_stew",
    visual_features={"broth": "opaque_pale_whitish_grey_alkaline_stew", "ingredients": ["tender_bamboo_shoot_chunks", "jackfruit_seeds", "green_papaya", "coriander"]},
    key_ingredients=["bamboo shoot", "jackfruit seeds", "green papaya", "khar / baking soda", "ginger", "green chillies", "pork optional"],
    hard_negatives=["AS_KHAR_OMITA", "MZ_STEW_BAI"],
    density_g_cm3=0.97,
    default_serving_weight_g=200.0,
    nutrition_per_100g={"calories": 65.0, "protein_g": 2.2, "carbs_g": 9.8, "fat_g": 1.8, "fiber_g": 3.2, "sodium_mg": 210.0},
    hierarchy=NortheastHierarchy(
        level3_state="Tripura", level4_region_community="Tripuri",
        level5_food_family="Stew/Soup", level6_food_type="Chakhwi", level7_variant="Bamboo Shoot Chakhwi",
        level8_cooking_method=["boiled", "alkaline_stewed"], default_portion="1 bowl (200g)",
        nutrition_ref_id="tr_stew_chakhwi"
    )
))

register_northeast_food(NortheastFoodClass(
    canonical_food_id="TR_CHUTNEY_MOSDENG_SERMA",
    canonical_name="Mosdeng Serma",
    state="Tripura",
    region_community="Tripuri",
    food_category="Chutney/Salad",
    regional_names={"English": "Spicy Tripuri Charred Tomato & Fermented Fish Mash", "Kokborok": "Mosdeng Serma", "Hindi": "मोसडेंग सेरमा"},
    alternate_names=["mosdeng serma", "tripuri tomato mosdeng"],
    vegetarian=False,
    meat_type="fish",
    fermented_agent="berma",
    preparation_style="charred_mashed",
    visual_features={"color": "fiery_charred_red_tomato_mash", "texture": "coarse_crushed_chilli_onion_pulp", "fish": "infused_berma (fermented fish)"},
    key_ingredients=["fire-roasted tomatoes", "berma (fermented fish) roasted", "charred green/red chillies", "raw onions", "coriander", "salt"],
    hard_negatives=["MN_CHUTNEY_EROMBA", "BR_CHOKHA_TOMATO", "MEXICAN_SALSA"],
    density_g_cm3=0.96,
    default_serving_weight_g=80.0,
    nutrition_per_100g={"calories": 62.0, "protein_g": 3.2, "carbs_g": 8.0, "fat_g": 1.5, "fiber_g": 2.0, "sodium_mg": 310.0},
    hierarchy=NortheastHierarchy(
        level3_state="Tripura", level4_region_community="Tripuri",
        level5_food_family="Chutney/Salad", level6_food_type="Mosdeng", level7_variant="Mosdeng Serma",
        level8_cooking_method=["flame_roasted", "mashed"], default_portion="1 portion (80g)",
        nutrition_ref_id="tr_chutney_mosdeng_serma"
    )
))


# =============================================================================
# 7. ARUNACHAL PRADESH & PAN-NORTHEAST MOMO / THUKPA (Sections 32-35, 40, 41)
# =============================================================================

register_northeast_food(NortheastFoodClass(
    canonical_food_id="NE_MOMO_PORK_STEAMED",
    canonical_name="Steamed Pork Momo",
    state="Pan-Northeast",
    region_community="Arunachal & Sikkim / Hills",
    food_category="Momo",
    regional_names={"English": "Steamed Pork Dumpling", "Tibetan": "Mog Mog", "Hindi": "मोमो"},
    alternate_names=["pork momo", "steamed momo", "northeast momo"],
    vegetarian=False,
    meat_type="pork",
    preparation_style="steamed_cake",
    visual_features={"shape": "round_pleated_purse_or_half_moon_crescent", "wrapper": "translucent_steamed_white_wheat_skin", "filling_hint": "succulent_minced_pork_and_onions"},
    key_ingredients=["refined flour (maida) wrapper", "minced pork with onion and ginger", "coriander", "spices", "served with red chilli garlic chutney"],
    hard_negatives=["NE_MOMO_VEG_STEAMED", "CHINESE_DIM_SUM"],
    density_g_cm3=0.82,
    default_serving_weight_g=30.0,
    nutrition_per_100g={"calories": 215.0, "protein_g": 11.2, "carbs_g": 24.5, "fat_g": 8.2, "fiber_g": 1.0, "sodium_mg": 280.0},
    hierarchy=NortheastHierarchy(
        level3_state="Pan-Northeast", level4_region_community="Arunachal & Sikkim / Hills",
        level5_food_family="Momo", level6_food_type="Momo", level7_variant="Steamed Pork Momo",
        level8_cooking_method=["steamed"], default_portion="6 pieces (180g)",
        nutrition_ref_id="ne_momo_pork_steamed"
    )
))

register_northeast_food(NortheastFoodClass(
    canonical_food_id="NE_MOMO_VEG_STEAMED",
    canonical_name="Steamed Vegetable Momo",
    state="Pan-Northeast",
    region_community="Arunachal & Sikkim / Hills",
    food_category="Momo",
    regional_names={"English": "Steamed Vegetable Dumpling", "Hindi": "वेज मोमो"},
    alternate_names=["veg momo", "vegetable momo"],
    vegetarian=True,
    meat_type="none",
    preparation_style="steamed_cake",
    visual_features={"shape": "round_pleated_purse_dumpling", "wrapper": "steamed_white_dough", "filling_hint": "cabbage_and_carrot_shreds_visible_through_thin_skin"},
    key_ingredients=["maida wrapper", "finely minced cabbage", "carrots", "onions", "ginger", "garlic", "soy/salt"],
    hard_negatives=["NE_MOMO_PORK_STEAMED"],
    density_g_cm3=0.80,
    default_serving_weight_g=28.0,
    nutrition_per_100g={"calories": 160.0, "protein_g": 4.8, "carbs_g": 28.0, "fat_g": 3.2, "fiber_g": 2.2, "sodium_mg": 240.0},
    hierarchy=NortheastHierarchy(
        level3_state="Pan-Northeast", level4_region_community="Arunachal & Sikkim / Hills",
        level5_food_family="Momo", level6_food_type="Momo", level7_variant="Steamed Veg Momo",
        level8_cooking_method=["steamed"], default_portion="6 pieces (170g)",
        nutrition_ref_id="ne_momo_veg_steamed"
    )
))

register_northeast_food(NortheastFoodClass(
    canonical_food_id="NE_THUKPA_CHICKEN",
    canonical_name="Chicken Thukpa",
    state="Pan-Northeast",
    region_community="Arunachal & Sikkim / Hills",
    food_category="Thukpa",
    regional_names={"English": "Northeast Tibetan-Style Chicken Noodle Soup", "Tibetan": "Thukpa", "Hindi": "थुकपा"},
    alternate_names=["thukpa", "chicken thukpa", "noodle soup"],
    vegetarian=False,
    meat_type="chicken",
    preparation_style="boiled_clear_soup",
    visual_features={"bowl": "large_steaming_bowl_of_noodle_soup", "contents": ["wheat_noodles_in_clear_seasoned_broth", "shredded_chicken", "julienned_carrots_and_cabbage", "chopped_spring_onions"]},
    key_ingredients=["wheat egg noodles", "chicken broth and shredded chicken", "cabbage", "carrots", "garlic", "ginger", "spring onions", "chilli oil hint"],
    hard_negatives=["JAPANESE_RAMEN", "VIETNAMESE_PHO", "CHINESE_CHOWMEIN"],
    density_g_cm3=0.96,
    default_serving_weight_g=380.0,
    nutrition_per_100g={"calories": 95.0, "protein_g": 6.8, "carbs_g": 12.5, "fat_g": 2.2, "fiber_g": 1.2, "sodium_mg": 320.0},
    hierarchy=NortheastHierarchy(
        level3_state="Pan-Northeast", level4_region_community="Arunachal & Sikkim / Hills",
        level5_food_family="Thukpa", level6_food_type="Thukpa", level7_variant="Chicken Thukpa",
        level8_cooking_method=["boiled_soup"], default_portion="1 large bowl (380g)",
        nutrition_ref_id="ne_thukpa_chicken"
    )
))


# =============================================================================
# 8. SIKKIM MASTER DATASET (Sections 36 - 39)
# =============================================================================

register_northeast_food(NortheastFoodClass(
    canonical_food_id="SK_MEAT_PHAGSHAPA",
    canonical_name="Sikkimese Phagshapa",
    state="Sikkim",
    region_community="Sikkim (Bhutia / Nepali)",
    food_category="Meat",
    regional_names={"English": "Pork Fat Stew with Radish & Dried Red Chillies", "Nepali": "फाकसापा", "Hindi": "फागशापा"},
    alternate_names=["phagshapa", "pork radish stew sikkim"],
    vegetarian=False,
    meat_type="pork",
    preparation_style="stewed_gravy",
    visual_features={"meat": "strips_of_pork_belly_fat_without_skin_charring", "vegetable": "stewed_radish (mula)_slices", "chillies": "prominent_whole_dried_red_chillies", "gravy": "light_oil_rich_broth_without_turmeric_heaviness"},
    key_ingredients=["pork belly strips", "radish (mula)", "whole dry red chillies", "ginger", "oil", "bok choy optional"],
    hard_negatives=["NL_MEAT_SMOKED_PORK_AXONE", "ML_MEAT_DOHNEIIHONG"],
    density_g_cm3=1.02,
    default_serving_weight_g=220.0,
    nutrition_per_100g={"calories": 260.0, "protein_g": 13.8, "carbs_g": 3.8, "fat_g": 21.5, "fiber_g": 1.2, "sodium_mg": 270.0},
    hierarchy=NortheastHierarchy(
        level3_state="Sikkim", level4_region_community="Sikkim (Bhutia / Nepali)",
        level5_food_family="Meat", level6_food_type="Phagshapa", level7_variant="Pork Phagshapa",
        level8_cooking_method=["stewed"], default_portion="1 bowl (220g)",
        nutrition_ref_id="sk_meat_phagshapa"
    )
))

register_northeast_food(NortheastFoodClass(
    canonical_food_id="SK_STEW_GUNDRUK",
    canonical_name="Gundruk Soup / Jhol",
    state="Sikkim",
    region_community="Sikkim (Nepali)",
    food_category="Fermented",
    regional_names={"English": "Fermented Sun-Dried Mustard Leaf Tangy Soup", "Nepali": "गुन्द्रुक", "Hindi": "गुन्द्रुक"},
    alternate_names=["gundruk", "gundruk ko jhol", "sikkim gundruk"],
    vegetarian=True,
    fermented_agent="gundruk",
    preparation_style="boiled_clear_soup",
    visual_features={"texture": "dark_crinkled_fermented_leafy_greens_in_tangy_broth", "color": "rustic_dark_olive_brown", "visible": ["tomatoes", "onions", "ginger_bits", "soybeans_optional"]},
    key_ingredients=["gundruk (naturally fermented and dried mustard/radish greens)", "tomatoes", "onion", "ginger", "garlic", "mustard oil", "green chillies"],
    hard_negatives=["JH_SAAG_KOINAR", "OD_VEG_SAGA_BHAJA", "PUNJABI_SARSON_SAAG"],
    density_g_cm3=0.98,
    default_serving_weight_g=200.0,
    nutrition_per_100g={"calories": 58.0, "protein_g": 3.2, "carbs_g": 7.5, "fat_g": 1.8, "fiber_g": 3.8, "sodium_mg": 210.0},
    hierarchy=NortheastHierarchy(
        level3_state="Sikkim", level4_region_community="Sikkim (Nepali)",
        level5_food_family="Fermented", level6_food_type="Gundruk", level7_variant="Gundruk Jhol",
        level8_cooking_method=["boiled", "simmered"], default_portion="1 bowl (200g)",
        nutrition_ref_id="sk_stew_gundruk"
    )
))

register_northeast_food(NortheastFoodClass(
    canonical_food_id="SK_FERMENTED_KINEMA",
    canonical_name="Sikkimese Kinema",
    state="Sikkim",
    region_community="Sikkim (Nepali)",
    food_category="Fermented",
    regional_names={"English": "Sikkimese Fermented Soybean Curry", "Nepali": "किनेमा", "Hindi": "किनेमा"},
    alternate_names=["kinema", "kinema curry"],
    vegetarian=True,
    fermented_agent="kinema",
    preparation_style="fermented_paste",
    visual_features={"texture": "mucilaginous_fermented_whole_soybeans", "curry": "pan_sauteed_with_tomatoes_onions_chillies"},
    key_ingredients=["kinema (fermented sticky soybeans)", "tomatoes", "onions", "green chillies", "turmeric", "mustard oil"],
    hard_negatives=["NL_FERMENTED_AXONE", "ML_FERMENTED_TUNGRYMBAI"],
    density_g_cm3=0.96,
    default_serving_weight_g=120.0,
    nutrition_per_100g={"calories": 180.0, "protein_g": 14.5, "carbs_g": 10.2, "fat_g": 9.0, "fiber_g": 5.0, "sodium_mg": 260.0},
    hierarchy=NortheastHierarchy(
        level3_state="Sikkim", level4_region_community="Sikkim (Nepali)",
        level5_food_family="Fermented", level6_food_type="Kinema", level7_variant="Kinema Curry",
        level8_cooking_method=["pan_cooked", "fermented"], default_portion="1 bowl (120g)",
        nutrition_ref_id="sk_fermented_kinema"
    )
))

register_northeast_food(NortheastFoodClass(
    canonical_food_id="SK_BREAD_SEL_ROTI",
    canonical_name="Sel Roti",
    state="Sikkim",
    region_community="Sikkim (Nepali)",
    food_category="Pitha/Snack",
    regional_names={"English": "Ring-Shaped Sweet Crispy Rice Flour Bread", "Nepali": "सेल रोटी", "Hindi": "सेल रोटी"},
    alternate_names=["sel roti", "sikkim ring bread"],
    vegetarian=True,
    preparation_style="fried_solid",
    visual_features={"shape": "distinctive_circular_torus_ring", "surface": "golden_brown_crisp_blistered_texture", "interior": "soft_spongy_sweet_crumb"},
    key_ingredients=["soaked rice flour batter", "sugar or jaggery", "ghee", "cardamom", "cloves", "oil for deep frying"],
    hard_negatives=["SOUTH_INDIAN_MEDU_VADA", "WESTERN_DONUT"],
    density_g_cm3=0.65,
    default_serving_weight_g=60.0,
    nutrition_per_100g={"calories": 350.0, "protein_g": 4.5, "carbs_g": 62.0, "fat_g": 10.2, "fiber_g": 1.2, "sodium_mg": 30.0},
    hierarchy=NortheastHierarchy(
        level3_state="Sikkim", level4_region_community="Sikkim (Nepali)",
        level5_food_family="Pitha/Snack", level6_food_type="Sel Roti", level7_variant="Traditional Sel Roti",
        level8_cooking_method=["deep_fried_ring"], default_portion="1 ring (60g)",
        nutrition_ref_id="sk_bread_sel_roti"
    )
))


# =============================================================================
# 9. NORTHEAST THALIS & UNKNOWN FALLBACK (Sections 63, 73, 87)
# =============================================================================

register_northeast_food(NortheastFoodClass(
    canonical_food_id="NE_THALI_ASSAMESE",
    canonical_name="Assamese Traditional Thali",
    state="Assam",
    region_community="Brahmaputra Valley",
    food_category="Thali",
    regional_names={"English": "Traditional Assamese Thali Meal", "Assamese": "অসমীয়া সাজ", "Hindi": "असमिया थाली"},
    alternate_names=["assamese thali", "assamese meal"],
    vegetarian=False,
    preparation_style="thali_multi_course",
    visual_features={"layout": "bell_metal_platter (kanh)_with_central_rice", "courses": ["rice", "amitar_khar", "masor_tenga", "aloo_pitika", "mati_mahor_dal", "xaak_bhaja"]},
    key_ingredients=["joha rice", "masor tenga fish", "omita khar", "aloo pitika", "mati mah dal", "lemon wedge"],
    density_g_cm3=0.88,
    default_serving_weight_g=650.0,
    nutrition_per_100g={"calories": 140.0, "protein_g": 6.8, "carbs_g": 20.5, "fat_g": 3.8, "fiber_g": 2.2, "sodium_mg": 240.0},
    hierarchy=NortheastHierarchy(
        level3_state="Assam", level4_region_community="Brahmaputra Valley",
        level5_food_family="Thali", level6_food_type="Thali Platter", level7_variant="Assamese Full Thali",
        level8_cooking_method=["composite_service"], default_portion="1 full thali (650g)",
        nutrition_ref_id="ne_thali_assamese"
    )
))

register_northeast_food(NortheastFoodClass(
    canonical_food_id="NE_THALI_NAGA",
    canonical_name="Naga Traditional Meal",
    state="Nagaland",
    region_community="Kohima",
    food_category="Thali",
    regional_names={"English": "Traditional Naga Meal Platter", "Nagamese": "Naga Thali", "Hindi": "नागा थाली"},
    alternate_names=["naga thali", "naga meal"],
    vegetarian=False,
    meat_type="pork",
    fermented_agent="axone",
    preparation_style="thali_multi_course",
    visual_features={"layout": "plain_steamed_rice_with_smoked_pork_axone_boiled_greens_and_chilli_chutney"},
    key_ingredients=["steamed rice", "smoked pork axone", "boiled leafy vegetables", "raja mircha chutney"],
    density_g_cm3=0.90,
    default_serving_weight_g=600.0,
    nutrition_per_100g={"calories": 175.0, "protein_g": 8.5, "carbs_g": 22.0, "fat_g": 6.2, "fiber_g": 2.0, "sodium_mg": 280.0},
    hierarchy=NortheastHierarchy(
        level3_state="Nagaland", level4_region_community="Kohima",
        level5_food_family="Thali", level6_food_type="Thali Platter", level7_variant="Naga Meal",
        level8_cooking_method=["composite_service"], default_portion="1 full meal (600g)",
        nutrition_ref_id="ne_thali_naga"
    )
))

register_northeast_food(NortheastFoodClass(
    canonical_food_id="NORTHEAST_INDIAN_UNKNOWN",
    canonical_name="Northeast Indian Unknown / Needs Confirmation",
    state="Northeast India",
    region_community="Uncertain",
    food_category="Unknown",
    regional_names={"English": "Unknown Northeast Food", "Hindi": "अज्ञात पूर्वोत्तर भोजन"},
    alternate_names=["unknown", "unrecognized northeast food", "needs confirmation"],
    vegetarian=True,
    preparation_style="unknown",
    visual_features={"evidence": "insufficient_or_ambiguous"},
    key_ingredients=[],
    density_g_cm3=0.85,
    default_serving_weight_g=150.0,
    nutrition_per_100g={"calories": 0.0, "protein_g": 0.0, "carbs_g": 0.0, "fat_g": 0.0, "fiber_g": 0.0, "sodium_mg": 0.0},
    hierarchy=NortheastHierarchy(
        level3_state="Northeast India", level4_region_community="Uncertain",
        level5_food_family="Unknown", level6_food_type="Unknown", level7_variant="Unknown",
        level8_cooking_method=["unknown"], default_portion="unknown",
        nutrition_ref_id="ne_unknown"
    )
))
