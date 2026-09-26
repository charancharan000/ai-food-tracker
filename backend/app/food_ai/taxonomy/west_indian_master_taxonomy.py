"""
West Indian Master Food Taxonomy & Identity Hierarchy
Implements Sections 1, 2, 3, 4, 7, 8, 10, 11, 12, 13, 14, 16, 24, 25, 28, 36, and 50 of Part 5.
Guarantees:
- Strict 9-Level Taxonomy:
  INDIAN FOOD -> WEST INDIAN FOOD -> STATE/REGION -> CUISINE -> 
  FOOD FAMILY -> FOOD TYPE -> FOOD VARIANT -> COOKING METHOD -> PORTION -> NUTRITION
- Covers all 5 Primary Western Regions:
  Maharashtra, Gujarat, Goa, Konkan, and Mumbai Street Food Ecosystem
- Permanent Canonical Class IDs (MH_, GJ_, GA_, KN_, MUM_, WI_)
- Multi-lingual Regional Name Mapping (English, Marathi, Gujarati, Konkani, Hindi)
- Gravy texture & color classification (dry, semi_gravy, thin_gravy, coconut_gravy, oily_gravy)
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class WestIndianHierarchy(BaseModel):
    level1_food: str = "Indian Food"
    level2_macro_region: str = "West Indian Food"
    level3_state_region: str # Maharashtra, Gujarat, Goa, Konkan, Mumbai
    level4_cuisine: str # Maharashtrian, Gujarati, Goan, Malvani, Mumbai Street Food, Parsi
    level5_food_family: str # Breakfast/Tiffin, Breads, Curries/Usal, Street Food, Farsan, Seafood, Sweets, Beverages, Thali
    level6_food_type: str # e.g. Poha, Misal, Bhakri, Dhokla, Thepla, Fish Curry, Modak
    level7_variant: str # e.g. Kanda Poha, Kolhapuri Misal, Surti Undhiyu, Goan Fish Curry
    level8_cooking_method: List[str] # steamed, shallow_fried, tawa_cooked, deep_fried, coconut_curry, slow_cooked
    level9_default_portion: str # 1 bowl (180g), 1 piece (120g), 1 plate (250g)
    nutrition_ref_id: str

class WestIndianFoodClass(BaseModel):
    permanent_id: str # e.g. MH_BREAKFAST_POHA_KANDA, GJ_FARSAN_DHOKLA_NYLON, GA_CURRY_FISH_GOAN
    hierarchy: WestIndianHierarchy
    canonical_name: str
    alternate_names: List[str] = Field(default_factory=list)
    regional_names: Dict[str, str] = Field(default_factory=dict)
    vegetarian: bool = True
    gravy_type: Optional[str] = Field(
        default=None,
        description="dry, semi_gravy, thin_gravy, coconut_gravy, oily_gravy, yogurt_gravy"
    )
    visual_features: Dict[str, Any] = Field(default_factory=dict)
    key_ingredients: List[str] = Field(default_factory=list)
    possible_ingredients: List[str] = Field(default_factory=list)
    hard_negatives: List[str] = Field(default_factory=list)
    density_g_cm3: float = 0.85
    default_serving_weight_g: float = 150.0
    nutrition_per_100g: Dict[str, float] = Field(default_factory=dict)

    @property
    def state(self) -> str:
        s = self.hierarchy.level3_state_region
        if s in ["Mumbai", "Konkan"]:
            return "Maharashtra"
        return s

# Master West Indian Registry
WEST_INDIAN_TAXONOMY_REGISTRY: Dict[str, WestIndianFoodClass] = {}
WEST_INDIAN_SYNONYM_MAP: Dict[str, str] = {}

def register_west_food(food: WestIndianFoodClass):
    WEST_INDIAN_TAXONOMY_REGISTRY[food.permanent_id] = food
    WEST_INDIAN_SYNONYM_MAP[food.canonical_name.lower().strip()] = food.permanent_id
    for alt in food.alternate_names:
        WEST_INDIAN_SYNONYM_MAP[alt.lower().strip()] = food.permanent_id
    for reg_name in food.regional_names.values():
        WEST_INDIAN_SYNONYM_MAP[reg_name.lower().strip()] = food.permanent_id

# =============================================================================
# 1. MAHARASHTRA BREAKFAST & TIFFIN (POHA, THALIPEETH, SABUDANA, MISAL, ETC.)
# =============================================================================

register_west_food(WestIndianFoodClass(
    permanent_id="MH_BREAKFAST_POHA_KANDA",
    canonical_name="Kanda Poha",
    alternate_names=["kanda poha", "kande pohe", "maharashtrian poha", "onion poha"],
    regional_names={"English": "Flattened Rice with Caramelized Onions", "Marathi": "कांदे पोहे", "Hindi": "कांदा पोहा"},
    vegetarian=True,
    gravy_type="dry",
    visual_features={
        "texture": "fluffy_soft_separated_yellow_flattened_rice_flakes",
        "color": "bright_turmeric_yellow",
        "key_visuals": ["abundant_translucent_diced_onions", "roasted_brown_peanuts", "mustard_seeds", "green_chillies", "fresh_coriander", "lemon_wedge"]
    },
    key_ingredients=["flattened rice (thick poha)", "onions (kanda)", "raw peanuts", "mustard seeds", "green chillies", "curry leaves", "turmeric", "fresh coriander", "lemon"],
    possible_ingredients=["fresh grated coconut garnish", "fine sev topping"],
    hard_negatives=["MH_BREAKFAST_POHA_BATATA", "MH_BREAKFAST_POHA_DADPE", "TN_BREAKFAST_UPMA_RAVA"],
    density_g_cm3=0.72,
    default_serving_weight_g=180.0,
    nutrition_per_100g={"calories": 160.0, "protein_g": 3.8, "carbs_g": 28.0, "fat_g": 4.2, "fiber_g": 2.2, "sodium_mg": 210.0},
    hierarchy=WestIndianHierarchy(
        level3_state_region="Maharashtra",
        level4_cuisine="Maharashtrian",
        level5_food_family="Breakfast/Tiffin",
        level6_food_type="Poha",
        level7_variant="Kanda Poha",
        level8_cooking_method=["steamed_pan_sauteed"],
        level9_default_portion="1 medium bowl (180g)",
        nutrition_ref_id="wi_poha_kanda"
    )
))

register_west_food(WestIndianFoodClass(
    permanent_id="MH_BREAKFAST_POHA_BATATA",
    canonical_name="Batata Poha",
    alternate_names=["batata poha", "aloo poha", "potato poha"],
    regional_names={"English": "Flattened Rice with Diced Potatoes & Peanuts", "Marathi": "बटाटा पोहे", "Hindi": "बटाटा पोहा"},
    vegetarian=True,
    gravy_type="dry",
    visual_features={
        "texture": "fluffy_soft_yellow_poha",
        "key_visuals": ["distinct_fried_or_boiled_cubed_potatoes", "roasted_peanuts", "curry_leaves", "mustard_seeds"]
    },
    key_ingredients=["flattened rice (poha)", "potatoes (batata cubed)", "peanuts", "mustard seeds", "turmeric", "green chillies", "lemon"],
    possible_ingredients=["onion (if Kanda-Batata Poha)"],
    hard_negatives=["MH_BREAKFAST_POHA_KANDA", "MH_BREAKFAST_SABUDANA_KHICHDI", "PB_CURRY_ALOO_JEERA"],
    density_g_cm3=0.76,
    default_serving_weight_g=200.0,
    nutrition_per_100g={"calories": 185.0, "protein_g": 3.5, "carbs_g": 32.5, "fat_g": 5.0, "fiber_g": 2.5, "sodium_mg": 220.0},
    hierarchy=WestIndianHierarchy(
        level3_state_region="Maharashtra",
        level4_cuisine="Maharashtrian",
        level5_food_family="Breakfast/Tiffin",
        level6_food_type="Poha",
        level7_variant="Batata Poha",
        level8_cooking_method=["pan_sauteed"],
        level9_default_portion="1 medium bowl (200g)",
        nutrition_ref_id="wi_poha_batata"
    )
))

register_west_food(WestIndianFoodClass(
    permanent_id="MH_BREAKFAST_POHA_DADPE",
    canonical_name="Dadpe Pohe",
    alternate_names=["dadpe pohe", "raw poha salad", "konkani dadpe pohe"],
    regional_names={"English": "Uncooked Tempered Poha with Fresh Coconut & Lime", "Marathi": "दडपे पोहे"},
    vegetarian=True,
    gravy_type="dry",
    visual_features={
        "texture": "raw_soaked_soft_white_flaky_poha_not_cooked_on_fire",
        "color": "pearly_white_with_green_and_mustard_tadka_accents",
        "key_visuals": ["grated_white_coconut", "raw_crunchy_onions", "pomegranate_pearls", "fried_peanuts"]
    },
    key_ingredients=["thin poha (raw soaked in coconut water/curd)", "fresh grated coconut", "finely chopped onions", "green chillies", "mustard seeds", "asafoetida", "lemon juice"],
    possible_ingredients=["pomegranate seeds"],
    hard_negatives=["MH_BREAKFAST_POHA_KANDA", "TN_BREAKFAST_AVAL_UPMA"],
    density_g_cm3=0.74,
    default_serving_weight_g=160.0,
    nutrition_per_100g={"calories": 150.0, "protein_g": 3.2, "carbs_g": 26.0, "fat_g": 4.5, "fiber_g": 2.8, "sodium_mg": 180.0},
    hierarchy=WestIndianHierarchy(
        level3_state_region="Maharashtra",
        level4_cuisine="Maharashtrian",
        level5_food_family="Breakfast/Tiffin",
        level6_food_type="Poha",
        level7_variant="Dadpe Pohe",
        level8_cooking_method=["soaked_tempered_uncooked"],
        level9_default_portion="1 bowl (160g)",
        nutrition_ref_id="wi_poha_dadpe"
    )
))

register_west_food(WestIndianFoodClass(
    permanent_id="MH_BREAKFAST_THALIPEETH_BHAJANI",
    canonical_name="Bhajani Thalipeeth",
    alternate_names=["thalipeeth", "bhajani thalipeeth", "multigrain savory flatbread"],
    regional_names={"English": "Spiced Multi-Grain Roasted Flatbread", "Marathi": "भाजणीचे थालीपीठ"},
    vegetarian=True,
    gravy_type="dry",
    visual_features={
        "shape": "rustic_hand_patted_circular_disc_with_3_to_5_punctured_steam_holes",
        "thickness_mm": 4.5,
        "diameter_cm": 17.0,
        "surface": "crisp_golden_brown_roasted_crust_with_white_sesame_seeds",
        "color": "earthy_mottled_tan_brown",
        "visible_toppings": ["white sesame seeds (til)", "chopped onions", "fresh coriander"]
    },
    key_ingredients=["bhajani flour (roasted blend of jowar, bajra, chana dal, urad dal, rice, wheat)", "onions", "white sesame seeds", "green chillies", "ajwain", "ghee/butter"],
    possible_ingredients=["grated cucumber (khamang thalipeeth)"],
    hard_negatives=["MH_BREAD_BHAKRI_JOWAR", "GJ_BREAD_THEPLA_METHI", "PB_PARATHA_PLAIN"],
    density_g_cm3=0.86,
    default_serving_weight_g=120.0,
    nutrition_per_100g={"calories": 240.0, "protein_g": 7.2, "carbs_g": 38.0, "fat_g": 7.5, "fiber_g": 5.8, "sodium_mg": 280.0},
    hierarchy=WestIndianHierarchy(
        level3_state_region="Maharashtra",
        level4_cuisine="Maharashtrian",
        level5_food_family="Breakfast/Tiffin",
        level6_food_type="Thalipeeth",
        level7_variant="Bhajani Thalipeeth",
        level8_cooking_method=["hand_patted", "tawa_roasted"],
        level9_default_portion="1 piece (120g)",
        nutrition_ref_id="wi_thalipeeth_bhajani"
    )
))

register_west_food(WestIndianFoodClass(
    permanent_id="MH_BREAKFAST_SABUDANA_KHICHDI",
    canonical_name="Sabudana Khichdi",
    alternate_names=["sabudana khichdi", "sago khichdi", "upvas khichdi", "tapioca pearl pilaf"],
    regional_names={"English": "Tapioca Pearls with Roasted Crushed Peanuts & Green Chillies", "Marathi": "साबुदाणा खिचडी", "Hindi": "साबूदाना खिचड़ी"},
    vegetarian=True,
    gravy_type="dry",
    visual_features={
        "pearls": "translucent_glistening_chewy_spherical_tapioca_pearls",
        "color": "ivory_to_golden_caramelized_pearly",
        "inclusions": ["coarsely_crushed_roasted_peanut_powder_(danyache_kut)", "diced_boiled_potatoes", "slit_green_chillies", "cumin_seeds", "ghee_sheen"]
    },
    key_ingredients=["tapioca pearls (sabudana)", "roasted peanut powder", "boiled potatoes", "green chillies", "cumin seeds (jeera)", "pure ghee", "lemon", "sendha namak (rock salt)"],
    possible_ingredients=["fresh coriander garnish (non-fasting)"],
    hard_negatives=["MH_BREAKFAST_POHA_KANDA", "TN_BREAKFAST_PONGAL_VEN", "GJ_SNACK_KHICHU"],
    density_g_cm3=0.88,
    default_serving_weight_g=200.0,
    nutrition_per_100g={"calories": 265.0, "protein_g": 4.2, "carbs_g": 44.0, "fat_g": 8.8, "fiber_g": 2.0, "sodium_mg": 190.0},
    hierarchy=WestIndianHierarchy(
        level3_state_region="Maharashtra",
        level4_cuisine="Maharashtrian",
        level5_food_family="Breakfast/Tiffin",
        level6_food_type="Sabudana",
        level7_variant="Sabudana Khichdi",
        level8_cooking_method=["pan_sauteed_in_ghee"],
        level9_default_portion="1 bowl (200g)",
        nutrition_ref_id="wi_sabudana_khichdi"
    )
))

register_west_food(WestIndianFoodClass(
    permanent_id="MH_BREAKFAST_SABUDANA_VADA",
    canonical_name="Sabudana Vada",
    alternate_names=["sabudana vada", "sago fritters", "upvas vada"],
    regional_names={"English": "Deep-Fried Crisp Tapioca & Peanut Fritters", "Marathi": "साबुदाणा वडा"},
    vegetarian=True,
    gravy_type="dry",
    visual_features={
        "shape": "flattened_circular_golden_patties",
        "crust": "shatteringly_crisp_bubbled_surface_studded_with_pearls_and_peanuts",
        "diameter_cm": 6.5,
        "thickness_mm": 18.0,
        "interior": "soft_chewy_translucent_mash"
    },
    key_ingredients=["soaked sabudana", "boiled mashed potatoes", "coarsely ground roasted peanuts", "green chillies", "cumin seeds", "lemon juice", "oil for deep frying"],
    possible_ingredients=["curd dip accompaniment"],
    hard_negatives=["MUM_STREET_BATATA_VADA", "TN_BREAKFAST_MEDU_VADA", "DL_STREET_ALOO_TIKKI_CHAAT"],
    density_g_cm3=0.84,
    default_serving_weight_g=90.0,
    nutrition_per_100g={"calories": 295.0, "protein_g": 4.5, "carbs_g": 38.0, "fat_g": 14.5, "fiber_g": 2.4, "sodium_mg": 240.0},
    hierarchy=WestIndianHierarchy(
        level3_state_region="Maharashtra",
        level4_cuisine="Maharashtrian",
        level5_food_family="Breakfast/Tiffin",
        level6_food_type="Sabudana",
        level7_variant="Sabudana Vada",
        level8_cooking_method=["deep_fried"],
        level9_default_portion="2 pieces (90g)",
        nutrition_ref_id="wi_sabudana_vada"
    )
))

register_west_food(WestIndianFoodClass(
    permanent_id="MH_CURRY_MISAL_KOLHAPURI",
    canonical_name="Kolhapuri Misal",
    alternate_names=["kolhapuri misal", "tikhat misal", "kat misal", "spicy misal"],
    regional_names={"English": "Fiery Sprouted Moth Bean Curry with Farsan & Tarri", "Marathi": "कोल्हापूरी मिसळ"},
    vegetarian=True,
    gravy_type="oily_gravy",
    visual_features={
        "viscosity": "thin_broth_with_heavy_red_oil_layer_(tarri/kat)",
        "color": "fiery_crimson_red_with_dark_chilli_oil_halo",
        "toppings": ["crunchy_spicy_farsan", "fine_sev", "diced_raw_red_onions", "fresh_coriander", "lemon_slice"],
        "base": "sprouted_matki_beans_simmered_in_kanda_lasun_masala"
    },
    key_ingredients=["sprouted moth beans (matki)", "kolhapuri kanda-lasun masala", "red chilli oil (tarri)", "farsan (mixed savoury crisps)", "sev", "onions", "coriander", "lemon"],
    possible_ingredients=["boiled potato cubes", "poha layer at base (Puneri style)"],
    hard_negatives=["MH_CURRY_USAL_MATKI", "MH_CURRY_MISAL_PUNERI", "DL_STREET_CHOLE_BHATURE"],
    density_g_cm3=1.04,
    default_serving_weight_g=250.0,
    nutrition_per_100g={"calories": 165.0, "protein_g": 5.8, "carbs_g": 18.5, "fat_g": 8.5, "fiber_g": 4.5, "sodium_mg": 460.0},
    hierarchy=WestIndianHierarchy(
        level3_state_region="Maharashtra",
        level4_cuisine="Maharashtrian",
        level5_food_family="Curries/Usal",
        level6_food_type="Misal",
        level7_variant="Kolhapuri Misal",
        level8_cooking_method=["boiled_sprouts", "layered_assembly", "tarri_ladled"],
        level9_default_portion="1 bowl misal + 2 pav (350g)",
        nutrition_ref_id="wi_misal_kolhapuri"
    )
))

register_west_food(WestIndianFoodClass(
    permanent_id="MH_CURRY_USAL_MATKI",
    canonical_name="Matki Usal",
    alternate_names=["matki usal", "usal", "sprouted bean usal", "moong usal"],
    regional_names={"English": "Spiced Sprouted Moth Bean Curry without Farsan", "Marathi": "मटकीची उसळ"},
    vegetarian=True,
    gravy_type="semi_gravy",
    visual_features={
        "beans": "tender_sprouted_moth_beans_with_tiny_white_tails",
        "gravy": "medium_onion_tomato_coconut_gravy_with_curry_leaves",
        "absence": "zero_farsan_zero_sev_topping_(distinguishes_usal_from_misal)",
        "color": "golden_brownish_red"
    },
    key_ingredients=["sprouted moth beans (matki)", "onions", "tomatoes", "fresh grated coconut", "goda masala / garam masala", "mustard seeds", "curry leaves"],
    possible_ingredients=["jaggery pinch"],
    hard_negatives=["MH_CURRY_MISAL_KOLHAPURI", "PB_CURRY_CHOLE_PUNJABI", "TN_CURRY_SUNDAL"],
    density_g_cm3=1.02,
    default_serving_weight_g=180.0,
    nutrition_per_100g={"calories": 125.0, "protein_g": 6.8, "carbs_g": 17.0, "fat_g": 3.8, "fiber_g": 5.2, "sodium_mg": 280.0},
    hierarchy=WestIndianHierarchy(
        level3_state_region="Maharashtra",
        level4_cuisine="Maharashtrian",
        level5_food_family="Curries/Usal",
        level6_food_type="Usal",
        level7_variant="Matki Usal",
        level8_cooking_method=["pressure_cooked", "simmered"],
        level9_default_portion="1 bowl (180g)",
        nutrition_ref_id="wi_usal_matki"
    )
))

register_west_food(WestIndianFoodClass(
    permanent_id="MH_SNACK_KOTHIMBIR_VADI",
    canonical_name="Kothimbir Vadi",
    alternate_names=["kothimbir vadi", "coriander fritters", "cilantro cakes"],
    regional_names={"English": "Crisp Steamed & Fried Coriander-Gram Flour Diamond Cakes", "Marathi": "कोथिंबीर वडी"},
    vegetarian=True,
    gravy_type="dry",
    visual_features={
        "shape": "geometric_diamond_or_square_sliced_cakes",
        "color": "deep_olive_green_packed_with_cilantro_leaves_in_golden_besan_matrix",
        "crust": "crisp_pan_fried_exterior",
        "visible_toppings": ["roasted_white_sesame_seeds"]
    },
    key_ingredients=["fresh coriander leaves (kothimbir - 60% by volume)", "gram flour (besan)", "rice flour", "white sesame seeds", "ginger garlic chilli paste", "turmeric", "oil"],
    possible_ingredients=["steamed only version (dietary)"],
    hard_negatives=["MH_SNACK_ALU_VADI", "GJ_FARSAN_KHANDVI", "TN_BREAKFAST_MEDU_VADA"],
    density_g_cm3=0.88,
    default_serving_weight_g=100.0,
    nutrition_per_100g={"calories": 220.0, "protein_g": 7.5, "carbs_g": 24.0, "fat_g": 11.0, "fiber_g": 4.8, "sodium_mg": 310.0},
    hierarchy=WestIndianHierarchy(
        level3_state_region="Maharashtra",
        level4_cuisine="Maharashtrian",
        level5_food_family="Breakfast/Tiffin",
        level6_food_type="Vadi",
        level7_variant="Kothimbir Vadi",
        level8_cooking_method=["steamed_then_shallow_fried"],
        level9_default_portion="4 pieces (100g)",
        nutrition_ref_id="wi_kothimbir_vadi"
    )
))

register_west_food(WestIndianFoodClass(
    permanent_id="MH_SNACK_ALU_VADI",
    canonical_name="Alu Vadi (Patra)",
    alternate_names=["alu vadi", "patra", "colocasia leaf rolls", "arbi ke patte ke pakode"],
    regional_names={"English": "Spiced Colocasia Leaf Pinwheel Rolls", "Marathi": "अळू वडी", "Gujarati": "પાતરા"},
    vegetarian=True,
    gravy_type="dry",
    visual_features={
        "shape": "concentric_spiral_pinwheel_circular_slices",
        "color": "dark_emerald_green_leaf_layers_interleaved_with_golden_brown_besan_paste",
        "diameter_cm": 5.0,
        "thickness_mm": 12.0,
        "toppings": ["mustard_seeds", "sesame_seeds", "fresh_grated_coconut"]
    },
    key_ingredients=["colocasia leaves (alu / arbi patta)", "besan (gram flour)", "tamarind pulp", "jaggery", "white sesame seeds", "mustard seeds", "hing", "oil"],
    possible_ingredients=["coconut garnish"],
    hard_negatives=["MH_SNACK_KOTHIMBIR_VADI", "GJ_FARSAN_KHANDVI", "MH_MAIN_PITHLA"],
    density_g_cm3=0.86,
    default_serving_weight_g=100.0,
    nutrition_per_100g={"calories": 215.0, "protein_g": 6.8, "carbs_g": 26.5, "fat_g": 9.8, "fiber_g": 4.2, "sodium_mg": 290.0},
    hierarchy=WestIndianHierarchy(
        level3_state_region="Maharashtra",
        level4_cuisine="Maharashtrian",
        level5_food_family="Breakfast/Tiffin",
        level6_food_type="Vadi",
        level7_variant="Alu Vadi",
        level8_cooking_method=["steamed_then_sliced_and_tempered"],
        level9_default_portion="4 slices (100g)",
        nutrition_ref_id="wi_alu_vadi"
    )
))

register_west_food(WestIndianFoodClass(
    permanent_id="MH_MAIN_PITHLA",
    canonical_name="Pithla (Pithla Bhakri)",
    alternate_names=["pithla", "pitla", "zunka", "besan pithla"],
    regional_names={"English": "Rustic Savory Gram Flour Stew", "Marathi": "पिठलं", "Hindi": "पिठला"},
    vegetarian=True,
    gravy_type="semi_gravy",
    visual_features={
        "viscosity": "thick_creamy_custard_like_gram_flour_porridge",
        "color": "sunny_golden_yellow",
        "surface": "mustard_cumin_green_chilli_curry_leaf_tadka_sheen",
        "accompaniments": ["jowar_bhakri", "thecha_(pounded_green_chilli_garlic_relish)", "raw_onion_wedges"]
    },
    key_ingredients=["gram flour (besan)", "water", "onions", "green chillies", "garlic", "mustard seeds", "turmeric", "curry leaves", "oil"],
    possible_ingredients=["coriander"],
    hard_negatives=["MH_MAIN_ZUNKA", "RJ_CURRY_KADHI", "PB_CURRY_DAL_TADKA"],
    density_g_cm3=1.04,
    default_serving_weight_g=180.0,
    nutrition_per_100g={"calories": 135.0, "protein_g": 5.8, "carbs_g": 14.5, "fat_g": 6.2, "fiber_g": 3.0, "sodium_mg": 310.0},
    hierarchy=WestIndianHierarchy(
        level3_state_region="Maharashtra",
        level4_cuisine="Maharashtrian",
        level5_food_family="Curries/Usal",
        level6_food_type="Pithla",
        level7_variant="Pithla",
        level8_cooking_method=["whisked_simmered_stew"],
        level9_default_portion="1 bowl (180g)",
        nutrition_ref_id="wi_pithla"
    )
))

register_west_food(WestIndianFoodClass(
    permanent_id="MH_MAIN_ZUNKA",
    canonical_name="Zunka (Dry Besan Sabzi)",
    alternate_names=["zunka", "jhunka", "dry pithla"],
    regional_names={"English": "Dry Stir-Fried Spiced Gram Flour Crumb", "Marathi": "झुणका"},
    vegetarian=True,
    gravy_type="dry",
    visual_features={
        "viscosity": "completely_dry_coarse_granular_crumbly",
        "color": "rustic_golden_yellow_with_charred_onion_bits",
        "absence": "no_liquid_runny_gravy_(distinguishes_zunka_from_pithla)"
    },
    key_ingredients=["besan (gram flour)", "sliced onions", "crushed garlic", "green chillies", "mustard seeds", "coriander", "oil"],
    possible_ingredients=["spring onions (kandyachya paticha zunka)"],
    hard_negatives=["MH_MAIN_PITHLA", "GJ_SNACK_SEV_KHAMANI", "PB_CURRY_ALOO_JEERA"],
    density_g_cm3=0.82,
    default_serving_weight_g=140.0,
    nutrition_per_100g={"calories": 210.0, "protein_g": 8.5, "carbs_g": 22.0, "fat_g": 9.8, "fiber_g": 4.2, "sodium_mg": 320.0},
    hierarchy=WestIndianHierarchy(
        level3_state_region="Maharashtra",
        level4_cuisine="Maharashtrian",
        level5_food_family="Curries/Usal",
        level6_food_type="Zunka",
        level7_variant="Zunka",
        level8_cooking_method=["pan_roasted_stir_fried"],
        level9_default_portion="1 bowl (140g)",
        nutrition_ref_id="wi_zunka"
    )
))

# =============================================================================
# 2. MAHARASHTRIAN BREAD DATASET (BHAKRI, PURAN POLI, GHAVAN)
# =============================================================================

register_west_food(WestIndianFoodClass(
    permanent_id="MH_BREAD_BHAKRI_JOWAR",
    canonical_name="Jowar Bhakri",
    alternate_names=["jowar bhakri", "jowar chi bhakri", "sorghum bhakri"],
    regional_names={"English": "Hand-Patted Unleavened Sorghum Flatbread", "Marathi": "ज्वारीची भाकरी"},
    vegetarian=True,
    gravy_type="dry",
    visual_features={
        "shape": "rustic_hand_patted_round_disc",
        "thickness_mm": 3.0,
        "diameter_cm": 18.0,
        "surface": "smooth_puffed_skin_separating_from_lower_base_layer",
        "color": "chalky_pale_off_white_to_buff_with_brown_tawa_freckles",
        "cracks": "delicate_fine_concentric_edge_cracks_from_water_patting"
    },
    key_ingredients=["sorghum flour (jowar)", "hot water", "salt"],
    possible_ingredients=["sesame seeds on top"],
    hard_negatives=["MH_BREAD_BHAKRI_BAJRA", "MH_BREAD_BHAKRI_RICE", "MH_BREAD_BHAKRI_NACHNI"],
    density_g_cm3=0.82,
    default_serving_weight_g=60.0,
    nutrition_per_100g={"calories": 240.0, "protein_g": 7.0, "carbs_g": 49.0, "fat_g": 1.8, "fiber_g": 6.8, "sodium_mg": 140.0},
    hierarchy=WestIndianHierarchy(
        level3_state_region="Maharashtra",
        level4_cuisine="Maharashtrian",
        level5_food_family="Breads",
        level6_food_type="Bhakri",
        level7_variant="Jowar Bhakri",
        level8_cooking_method=["hand_patted", "tawa_cooked", "flame_roasted"],
        level9_default_portion="1 piece (60g)",
        nutrition_ref_id="wi_bhakri_jowar"
    )
))

register_west_food(WestIndianFoodClass(
    permanent_id="MH_BREAD_BHAKRI_BAJRA",
    canonical_name="Bajra Bhakri",
    alternate_names=["bajra bhakri", "bajrichi bhakri", "pearl millet bhakri"],
    regional_names={"English": "Hand-Patted Pearl Millet Flatbread", "Marathi": "बाजरीची भाकरी"},
    vegetarian=True,
    gravy_type="dry",
    visual_features={
        "shape": "rustic_thick_disc",
        "thickness_mm": 4.0,
        "diameter_cm": 18.0,
        "surface": "coarse_cracked_matte_surface_often_sprinkled_with_white_til",
        "color": "deep_ash_greyish_brown_to_khaki_charcoal"
    },
    key_ingredients=["pearl millet flour (bajra)", "hot water", "white sesame seeds (til)", "salt"],
    possible_ingredients=["white butter (loni) spread"],
    hard_negatives=["MH_BREAD_BHAKRI_JOWAR", "MH_BREAD_BHAKRI_NACHNI", "RJ_BREAD_BAJRA_ROTI"],
    density_g_cm3=0.86,
    default_serving_weight_g=70.0,
    nutrition_per_100g={"calories": 250.0, "protein_g": 7.8, "carbs_g": 46.5, "fat_g": 4.2, "fiber_g": 7.5, "sodium_mg": 150.0},
    hierarchy=WestIndianHierarchy(
        level3_state_region="Maharashtra",
        level4_cuisine="Maharashtrian",
        level5_food_family="Breads",
        level6_food_type="Bhakri",
        level7_variant="Bajra Bhakri",
        level8_cooking_method=["hand_patted", "tawa_flame_cooked"],
        level9_default_portion="1 piece (70g)",
        nutrition_ref_id="wi_bhakri_bajra"
    )
))

register_west_food(WestIndianFoodClass(
    permanent_id="MH_BREAD_BHAKRI_RICE",
    canonical_name="Rice Bhakri (Tandlachi Bhakri)",
    alternate_names=["rice bhakri", "tandlachi bhakri", "konkani rice bread"],
    regional_names={"English": "Soft White Rice Flour Flatbread", "Marathi": "तांदळाची भाकरी"},
    vegetarian=True,
    gravy_type="dry",
    visual_features={
        "shape": "circular_flatbread",
        "thickness_mm": 2.5,
        "diameter_cm": 17.0,
        "color": "pure_snow_white_with_faint_translucent_golden_patches",
        "texture": "softer_and_more_flexible_than_millet_bhakris"
    },
    key_ingredients=["fine rice flour (tandool pith)", "warm water", "pinch of salt"],
    possible_ingredients=["ghee brush"],
    hard_negatives=["MH_BREAD_BHAKRI_JOWAR", "MH_BREAD_GHAVAN", "PB_BREAD_ROTI_TAWA"],
    density_g_cm3=0.80,
    default_serving_weight_g=55.0,
    nutrition_per_100g={"calories": 230.0, "protein_g": 4.8, "carbs_g": 50.0, "fat_g": 0.8, "fiber_g": 2.2, "sodium_mg": 120.0},
    hierarchy=WestIndianHierarchy(
        level3_state_region="Maharashtra",
        level4_cuisine="Konkani",
        level5_food_family="Breads",
        level6_food_type="Bhakri",
        level7_variant="Rice Bhakri",
        level8_cooking_method=["hand_patted", "tawa_cooked"],
        level9_default_portion="1 piece (55g)",
        nutrition_ref_id="wi_bhakri_rice"
    )
))

register_west_food(WestIndianFoodClass(
    permanent_id="MH_BREAD_BHAKRI_NACHNI",
    canonical_name="Nachni Bhakri (Ragi Bhakri)",
    alternate_names=["nachni bhakri", "ragi bhakri", "finger millet bhakri"],
    regional_names={"English": "Rustic Finger Millet Flatbread", "Marathi": "नाचणीची भाकरी"},
    vegetarian=True,
    gravy_type="dry",
    visual_features={
        "shape": "circular_rustic_disc",
        "thickness_mm": 3.2,
        "diameter_cm": 17.0,
        "color": "deep_chocolate_brown_to_dark_slate_purple",
        "surface": "matte_cracked_rustic_texture"
    },
    key_ingredients=["finger millet flour (nachni/ragi)", "hot water", "salt"],
    possible_ingredients=["white butter accompaniment"],
    hard_negatives=["MH_BREAD_BHAKRI_BAJRA", "UK_BREAD_MANDUA_ROTI", "MH_BREAD_BHAKRI_JOWAR"],
    density_g_cm3=0.84,
    default_serving_weight_g=60.0,
    nutrition_per_100g={"calories": 235.0, "protein_g": 6.5, "carbs_g": 48.0, "fat_g": 1.6, "fiber_g": 8.5, "sodium_mg": 140.0},
    hierarchy=WestIndianHierarchy(
        level3_state_region="Maharashtra",
        level4_cuisine="Maharashtrian",
        level5_food_family="Breads",
        level6_food_type="Bhakri",
        level7_variant="Nachni Bhakri",
        level8_cooking_method=["hand_patted", "tawa_cooked"],
        level9_default_portion="1 piece (60g)",
        nutrition_ref_id="wi_bhakri_nachni"
    )
))

register_west_food(WestIndianFoodClass(
    permanent_id="MH_SWEET_PURAN_POLI",
    canonical_name="Maharashtrian Puran Poli",
    alternate_names=["puran poli", "vedmi", "puranachi poli", "sweet lentil flatbread"],
    regional_names={"English": "Sweet Lentil & Jaggery Stuffed Delicate Flatbread", "Marathi": "पुरणपोळी", "Gujarati": "પુરણ પોળી"},
    vegetarian=True,
    gravy_type="dry",
    visual_features={
        "shape": "thin_delicate_circular_flatbread",
        "thickness_mm": 2.2,
        "diameter_cm": 22.0,
        "surface": "golden_yellow_sheen_with_faint_brown_blisters_and_amber_filling_showing_through",
        "serving": "copious_pool_of_pure_melted_desi_ghee_(tup)"
    },
    key_ingredients=["puran (cooked chana dal mashed with jaggery & cardamom)", "outer dough (maida or wheat flour + turmeric)", "nutmeg", "pure desi ghee"],
    possible_ingredients=["katachi amti accompaniment", "warm milk accompaniment"],
    hard_negatives=["PB_PARATHA_ALOO", "PB_PARATHA_PLAIN", "GJ_BREAD_THEPLA_METHI"],
    density_g_cm3=0.86,
    default_serving_weight_g=110.0,
    nutrition_per_100g={"calories": 295.0, "protein_g": 6.8, "carbs_g": 52.0, "fat_g": 7.2, "fiber_g": 3.8, "sugar_g": 26.0, "sodium_mg": 110.0},
    hierarchy=WestIndianHierarchy(
        level3_state_region="Maharashtra",
        level4_cuisine="Maharashtrian",
        level5_food_family="Sweets",
        level6_food_type="Puran Poli",
        level7_variant="Maharashtrian Puran Poli",
        level8_cooking_method=["rolled_thin", "tawa_cooked_in_ghee"],
        level9_default_portion="1 piece (110g)",
        nutrition_ref_id="wi_puran_poli"
    )
))

register_west_food(WestIndianFoodClass(
    permanent_id="KN_BREAD_GHAVAN",
    canonical_name="Konkani Ghavan",
    alternate_names=["ghavan", "ghavane", "konkani rice crepe", "neer dosa konkan"],
    regional_names={"English": "Lacy Perforated Rice Flour Crepe", "Marathi": "घावणे"},
    vegetarian=True,
    gravy_type="dry",
    visual_features={
        "shape": "folded_triangular_or_semi_circular_crepe",
        "thickness_mm": 1.2,
        "texture": "delicate_lacy_honeycomb_net_mesh_soft_and_elastic",
        "color": "pure_snow_white"
    },
    key_ingredients=["fine rice flour", "water", "salt"],
    possible_ingredients=["coconut chutney accompaniment", "sweet coconut milk accompaniment"],
    hard_negatives=["TN_BREAKFAST_DOSA_PLAIN", "MH_BREAD_BHAKRI_RICE", "GJ_FARSAN_KHANDVI"],
    density_g_cm3=0.75,
    default_serving_weight_g=50.0,
    nutrition_per_100g={"calories": 165.0, "protein_g": 3.0, "carbs_g": 35.0, "fat_g": 1.0, "fiber_g": 1.0, "sodium_mg": 140.0},
    hierarchy=WestIndianHierarchy(
        level3_state_region="Konkan",
        level4_cuisine="Konkani",
        level5_food_family="Breads",
        level6_food_type="Crepe",
        level7_variant="Konkani Ghavan",
        level8_cooking_method=["poured_batter", "tawa_steamed"],
        level9_default_portion="2 pieces (100g)",
        nutrition_ref_id="wi_ghavan"
    )
))

# =============================================================================
# 3. MUMBAI STREET FOOD ECOSYSTEM (VADA PAV, PAV BHAJI, BHEL, SEV PURI, SANDWICH)
# =============================================================================

register_west_food(WestIndianFoodClass(
    permanent_id="MUM_STREET_VADA_PAV",
    canonical_name="Mumbai Vada Pav",
    alternate_names=["vada pav", "wada pav", "bombay burger", "batata vada pav"],
    regional_names={"English": "Deep-Fried Spiced Potato Dumpling in Pav Bun", "Marathi": "वडा पाव", "Hindi": "वड़ा पाव"},
    vegetarian=True,
    gravy_type="dry",
    visual_features={
        "bun": "sliced_soft_white_yeast_leavened_laadi_pav_bun",
        "filling": "golden_crisp_round_besan_battered_spiced_potato_patty",
        "chutneys": ["fiery_red_dry_garlic_coconut_chutney_(lasun_chutney)", "green_mint_coriander_chutney", "sweet_tamarind"],
        "accompaniment": "deep_fried_salted_green_chilli_(bharli_mirchi)"
    },
    key_ingredients=["pav bread bun", "batata vada (mashed spiced potatoes, mustard, curry leaves, ginger-garlic, turmeric, gram flour batter)", "dry red garlic chutney", "green chutney", "fried green chilli"],
    possible_ingredients=["cheese slice (Cheese Vada Pav)", "butter grill"],
    hard_negatives=["MUM_STREET_BATATA_VADA", "UP_SNACK_SAMOSA", "DL_STREET_ALOO_TIKKI_CHAAT"],
    density_g_cm3=0.78,
    default_serving_weight_g=140.0,
    nutrition_per_100g={"calories": 250.0, "protein_g": 6.2, "carbs_g": 36.5, "fat_g": 9.5, "fiber_g": 3.2, "sodium_mg": 480.0},
    hierarchy=WestIndianHierarchy(
        level3_state_region="Mumbai",
        level4_cuisine="Mumbai Street Food",
        level5_food_family="Street Food",
        level6_food_type="Vada Pav",
        level7_variant="Classic Mumbai Vada Pav",
        level8_cooking_method=["deep_fried_vada", "assembled_bun"],
        level9_default_portion="1 piece (140g)",
        nutrition_ref_id="wi_vada_pav"
    )
))

register_west_food(WestIndianFoodClass(
    permanent_id="MUM_STREET_BATATA_VADA",
    canonical_name="Batata Vada (Standalone)",
    alternate_names=["batata vada", "aloo bonda maharashtrian", "potato vada"],
    regional_names={"English": "Crisp Gram Flour Coated Spiced Potato Ball", "Marathi": "बटाटा वडा"},
    vegetarian=True,
    gravy_type="dry",
    visual_features={
        "shape": "spherical_or_slightly_flattened_golden_yellow_ball",
        "crust": "thin_smooth_crisp_besan_coating",
        "diameter_cm": 5.5,
        "interior": "yellow_turmeric_potato_mash_with_mustard_seeds_and_curry_leaves"
    },
    key_ingredients=["boiled mashed potatoes", "mustard seeds", "hing", "curry leaves", "green chillies", "ginger-garlic", "besan (gram flour batter)", "oil for deep frying"],
    possible_ingredients=["fried green chilli"],
    hard_negatives=["MUM_STREET_VADA_PAV", "MH_BREAKFAST_SABUDANA_VADA", "TN_BREAKFAST_MEDU_VADA"],
    density_g_cm3=0.86,
    default_serving_weight_g=75.0,
    nutrition_per_100g={"calories": 210.0, "protein_g": 4.5, "carbs_g": 26.0, "fat_g": 10.2, "fiber_g": 2.8, "sodium_mg": 340.0},
    hierarchy=WestIndianHierarchy(
        level3_state_region="Mumbai",
        level4_cuisine="Mumbai Street Food",
        level5_food_family="Street Food",
        level6_food_type="Batata Vada",
        level7_variant="Batata Vada Standalone",
        level8_cooking_method=["deep_fried"],
        level9_default_portion="1 piece (75g)",
        nutrition_ref_id="wi_batata_vada"
    )
))

register_west_food(WestIndianFoodClass(
    permanent_id="MUM_STREET_PAV_BHAJI",
    canonical_name="Mumbai Pav Bhaji",
    alternate_names=["pav bhaji", "bombay pav bhaji", "butter pav bhaji"],
    regional_names={"English": "Spiced Mashed Vegetable Curry with Buttered Pav", "Marathi": "पाव भाजी", "Hindi": "पाव भाजी"},
    vegetarian=True,
    gravy_type="semi_gravy",
    visual_features={
        "bhaji": "dense_coarse_reddish_brown_vegetable_mash",
        "surface": "melting_cube_of_amul_butter_forming_golden_pool",
        "bread": "2_to_4_laadi_pav_halves_slathered_in_butter_and_tawa_toasted",
        "sides": ["finely_chopped_red_onions", "fresh_lemon_wedge", "chopped_coriander"]
    },
    key_ingredients=["potatoes", "cauliflower", "green peas", "tomatoes", "capsicum", "pav bhaji masala", "pure butter (Amul)", "laadi pav buns", "onions", "lemon"],
    possible_ingredients=["cheese topping (Cheese Pav Bhaji)"],
    hard_negatives=["DL_STREET_CHOLE_BHATURE", "PB_CURRY_RAJMA_MASALA", "UP_BREAKFAST_POORI_SABZI"],
    density_g_cm3=1.05,
    default_serving_weight_g=350.0,
    nutrition_per_100g={"calories": 175.0, "protein_g": 4.2, "carbs_g": 22.0, "fat_g": 8.0, "fiber_g": 3.8, "sodium_mg": 440.0},
    hierarchy=WestIndianHierarchy(
        level3_state_region="Mumbai",
        level4_cuisine="Mumbai Street Food",
        level5_food_family="Street Food",
        level6_food_type="Pav Bhaji",
        level7_variant="Classic Mumbai Pav Bhaji",
        level8_cooking_method=["mashed_tawa_simmered", "buttered_tawa_toasted_pav"],
        level9_default_portion="1 plate (1 bhaji bowl + 2 pav, 350g)",
        nutrition_ref_id="wi_pav_bhaji"
    )
))

register_west_food(WestIndianFoodClass(
    permanent_id="MUM_STREET_BHEL_PURI",
    canonical_name="Bhel Puri",
    alternate_names=["bhel puri", "bombay bhel", "sukha bhel", "geela bhel"],
    regional_names={"English": "Puffed Rice Chaat with Tangy Chutneys & Sev", "Hindi": "भेल पूरी", "Marathi": "भेळ"},
    vegetarian=True,
    gravy_type="dry",
    visual_features={
        "base": "crunchy_puffed_rice_(kurmura)",
        "inclusions": ["fine_yellow_sev", "crushed_crisp_papdis", "boiled_potato_cubes", "diced_onions", "diced_tomatoes", "roasted_peanuts"],
        "dressings": ["tangy_tamarind_saunth_chutney", "spicy_green_chilli_coriander_chutney", "garlic_chutney"],
        "garnishes": ["fresh_coriander", "lemon_squeeze", "raw_mango_pieces_(seasonal)"]
    },
    key_ingredients=["puffed rice (kurmura)", "nylon sev", "flat papdis", "boiled potatoes", "onions", "tamarind chutney", "green chutney", "coriander", "chaat masala"],
    possible_ingredients=["fried masala chana dal", "raw mango dices"],
    hard_negatives=["MUM_STREET_SEV_PURI", "DL_STREET_PAPDI_CHAAT", "MUM_STREET_DAHI_PURI"],
    density_g_cm3=0.62,
    default_serving_weight_g=160.0,
    nutrition_per_100g={"calories": 195.0, "protein_g": 4.5, "carbs_g": 34.0, "fat_g": 5.2, "fiber_g": 2.8, "sodium_mg": 380.0},
    hierarchy=WestIndianHierarchy(
        level3_state_region="Mumbai",
        level4_cuisine="Mumbai Street Food",
        level5_food_family="Street Food",
        level6_food_type="Chaat",
        level7_variant="Bhel Puri",
        level8_cooking_method=["tossed_raw_assembled"],
        level9_default_portion="1 plate (160g)",
        nutrition_ref_id="wi_bhel_puri"
    )
))

register_west_food(WestIndianFoodClass(
    permanent_id="MUM_STREET_SEV_PURI",
    canonical_name="Sev Puri (Sev Batata Puri)",
    alternate_names=["sev puri", "sev batata puri", "bombay sev puri"],
    regional_names={"English": "Crisp Flat Puris Topped with Potatoes, Chutneys & Mountain of Sev", "Hindi": "सेव पूरी", "Marathi": "शेव बटाटा पुरी"},
    vegetarian=True,
    gravy_type="dry",
    visual_features={
        "layout": "6_to_8_flat_crisp_round_puris_arranged_symmetrically",
        "layers": ["mashed_or_cubed_potatoes", "finely_chopped_onions", "tamarind_and_green_chutneys"],
        "dominant_feature": "heavy_snowfall_of_bright_yellow_nylon_sev_completely_blanketing_the_puris",
        "garnishes": ["coriander_leaves", "raw_mango_shreds"]
    },
    key_ingredients=["flat crisp puris (papdi)", "boiled potatoes", "onions", "nylon sev (50g)", "tamarind chutney", "green chilli chutney", "garlic chutney", "chaat masala"],
    possible_ingredients=["raw mango strips"],
    hard_negatives=["MUM_STREET_BHEL_PURI", "MUM_STREET_DAHI_PURI", "DL_STREET_PAPDI_CHAAT"],
    density_g_cm3=0.82,
    default_serving_weight_g=180.0,
    nutrition_per_100g={"calories": 235.0, "protein_g": 4.8, "carbs_g": 36.0, "fat_g": 8.5, "fiber_g": 3.0, "sodium_mg": 420.0},
    hierarchy=WestIndianHierarchy(
        level3_state_region="Mumbai",
        level4_cuisine="Mumbai Street Food",
        level5_food_family="Street Food",
        level6_food_type="Chaat",
        level7_variant="Sev Puri",
        level8_cooking_method=["assembled"],
        level9_default_portion="6 pieces (180g)",
        nutrition_ref_id="wi_sev_puri"
    )
))

register_west_food(WestIndianFoodClass(
    permanent_id="MUM_STREET_BOMBAY_SANDWICH",
    canonical_name="Bombay Vegetable Sandwich",
    alternate_names=["bombay sandwich", "veg sandwich", "bombay toast sandwich", "grilled sandwich"],
    regional_names={"English": "Layered Multicolored Vegetable & Green Chutney Sandwich", "Hindi": "बॉम्बे सैंडविच"},
    vegetarian=True,
    gravy_type="dry",
    visual_features={
        "bread": "white_bread_slices_trimmed_and_quartered_into_triangles",
        "visible_layers": ["red_beetroot_rounds", "green_cucumber_slices", "red_tomato_slices", "yellow_boiled_potato_slices", "green_capsicum"],
        "spread": "vibrant_spicy_mint_coriander_chutney_and_butter",
        "surface": "toasted_or_grilled_grid_marks_with_sev_and_chaat_masala_on_top"
    },
    key_ingredients=["white bread slices", "boiled beetroot", "cucumber", "potatoes", "tomatoes", "onions", "spicy green chutney", "butter", "sandwich masala"],
    possible_ingredients=["grated processed cheese (Cheese Grilled Sandwich)"],
    hard_negatives=["DL_STREET_ALOO_TIKKI_CHAAT", "MUM_STREET_VADA_PAV"],
    density_g_cm3=0.76,
    default_serving_weight_g=200.0,
    nutrition_per_100g={"calories": 185.0, "protein_g": 4.5, "carbs_g": 28.0, "fat_g": 6.5, "fiber_g": 3.2, "sodium_mg": 380.0},
    hierarchy=WestIndianHierarchy(
        level3_state_region="Mumbai",
        level4_cuisine="Mumbai Street Food",
        level5_food_family="Street Food",
        level6_food_type="Sandwich",
        level7_variant="Bombay Vegetable Sandwich",
        level8_cooking_method=["assembled", "grilled_optional"],
        level9_default_portion="1 whole sandwich (200g)",
        nutrition_ref_id="wi_bombay_sandwich"
    )
))

# =============================================================================
# 4. GUJARAT MASTER DATASET (DHOKLA FAMILY, KHANDVI, UNDHIYU, THEPLA, FAFDA)
# =============================================================================

register_west_food(WestIndianFoodClass(
    permanent_id="GJ_FARSAN_KHAMAN_NYLON",
    canonical_name="Nylon Khaman",
    alternate_names=["khaman", "nylon khaman", "surti khaman", "yellow dhokla"],
    regional_names={"English": "Ultra-Spongy Juicy Steamed Gram Flour Cake", "Gujarati": "નાયલોન ખમણ", "Hindi": "नायलॉन खमन"},
    vegetarian=True,
    gravy_type="dry",
    visual_features={
        "shape": "cubical_cut_square_blocks",
        "texture": "ultra_spongy_airy_porous_juicy_springs_back_when_pressed",
        "color": "uniform_bright_canary_yellow",
        "moisture": "soaked_in_sweet_tangy_lemon_sugar_water",
        "tempering": ["crackled_mustard_seeds", "slit_green_chillies", "sesame_seeds", "fresh_coriander", "grated_coconut"]
    },
    key_ingredients=["gram flour (besan)", "fruit salt / eno", "sugar syrup water", "lemon juice", "mustard seeds", "sesame seeds", "green chillies", "coriander"],
    possible_ingredients=["grated coconut topping"],
    hard_negatives=["GJ_FARSAN_DHOKLA_WHITE", "TN_BREAKFAST_IDLI_PLAIN", "GJ_SNACK_HANDVO"],
    density_g_cm3=0.65,
    default_serving_weight_g=120.0,
    nutrition_per_100g={"calories": 160.0, "protein_g": 6.2, "carbs_g": 24.5, "fat_g": 4.5, "fiber_g": 2.0, "sugar_g": 8.0, "sodium_mg": 320.0},
    hierarchy=WestIndianHierarchy(
        level3_state_region="Gujarat",
        level4_cuisine="Gujarati",
        level5_food_family="Farsan",
        level6_food_type="Dhokla Family",
        level7_variant="Nylon Khaman",
        level8_cooking_method=["steamed", "syrup_infused_tempered"],
        level9_default_portion="4 pieces (120g)",
        nutrition_ref_id="wi_khaman_nylon"
    )
))

register_west_food(WestIndianFoodClass(
    permanent_id="GJ_FARSAN_DHOKLA_WHITE",
    canonical_name="White Dhokla (Khatta Dhokla)",
    alternate_names=["white dhokla", "khatta dhokla", "rice dhokla", "idada"],
    regional_names={"English": "Fermented Rice & Urad Savory Steamed Cake", "Gujarati": "ખાટા ઢોકળા / ઇદડા", "Hindi": "सफेद ढोकला"},
    vegetarian=True,
    gravy_type="dry",
    visual_features={
        "shape": "geometric_diamond_or_square_sliced_steamed_cakes",
        "color": "pure_pearl_white_not_yellow",
        "surface": "liberally_sprinkled_with_coarse_black_pepper_and_red_chilli_powder",
        "texture": "fermented_medium_sponge_grain"
    },
    key_ingredients=["rice and urad dal fermented batter", "sour curd", "cracked black pepper", "red chilli powder", "ginger green chilli paste", "oil"],
    possible_ingredients=["mustard seed tempering"],
    hard_negatives=["GJ_FARSAN_KHAMAN_NYLON", "TN_BREAKFAST_IDLI_PLAIN", "GJ_SNACK_HANDVO"],
    density_g_cm3=0.72,
    default_serving_weight_g=120.0,
    nutrition_per_100g={"calories": 145.0, "protein_g": 5.4, "carbs_g": 26.0, "fat_g": 2.5, "fiber_g": 2.2, "sodium_mg": 210.0},
    hierarchy=WestIndianHierarchy(
        level3_state_region="Gujarat",
        level4_cuisine="Gujarati",
        level5_food_family="Farsan",
        level6_food_type="Dhokla Family",
        level7_variant="White Khatta Dhokla",
        level8_cooking_method=["fermented", "steamed"],
        level9_default_portion="4 pieces (120g)",
        nutrition_ref_id="wi_dhokla_white"
    )
))

register_west_food(WestIndianFoodClass(
    permanent_id="GJ_FARSAN_KHANDVI",
    canonical_name="Gujarati Khandvi",
    alternate_names=["khandvi", "patuli", "surti khandvi", "gram flour rolls"],
    regional_names={"English": "Tightly Rolled Silky Gram Flour & Buttermilk Pinwheels", "Gujarati": "ખાંડવી", "Hindi": "खांडवी"},
    vegetarian=True,
    gravy_type="dry",
    visual_features={
        "shape": "tightly_coiled_cylindrical_finger_rolls",
        "texture": "silky_smooth_melt_in_mouth_glossy_sheen",
        "color": "soft_pastel_yellow",
        "length_cm": 5.0,
        "diameter_cm": 1.8,
        "garnishes": ["fresh_grated_white_coconut", "mustard_seeds", "sesame_seeds", "finely_chopped_cilantro"]
    },
    key_ingredients=["gram flour (besan)", "sour buttermilk / curd", "turmeric", "ginger-green chilli paste", "mustard seeds", "sesame seeds", "fresh coconut", "coriander"],
    possible_ingredients=["spiced coconut-paneer stuffing inside"],
    hard_negatives=["MH_SNACK_ALU_VADI", "TN_BREAKFAST_DOSA_PLAIN", "GJ_FARSAN_KHAMAN_NYLON"],
    density_g_cm3=0.84,
    default_serving_weight_g=110.0,
    nutrition_per_100g={"calories": 155.0, "protein_g": 5.8, "carbs_g": 18.0, "fat_g": 6.8, "fiber_g": 2.4, "sodium_mg": 260.0},
    hierarchy=WestIndianHierarchy(
        level3_state_region="Gujarat",
        level4_cuisine="Gujarati",
        level5_food_family="Farsan",
        level6_food_type="Khandvi",
        level7_variant="Classic Khandvi",
        level8_cooking_method=["slow_cooked_paste", "thinly_spread", "rolled", "tempered"],
        level9_default_portion="6 rolls (110g)",
        nutrition_ref_id="wi_khandvi"
    )
))

register_west_food(WestIndianFoodClass(
    permanent_id="GJ_MAIN_UNDHIYU_SURTI",
    canonical_name="Surti Undhiyu",
    alternate_names=["undhiyu", "surti undhiyu", "gujarati winter vegetable casserole"],
    regional_names={"English": "Traditional Mixed Winter Root & Bean Casserole with Muthia", "Gujarati": "સૂરતી ઊંધિયું", "Hindi": "उंधियू"},
    vegetarian=True,
    gravy_type="semi_gravy",
    visual_features={
        "presentation": "rich_multi_vegetable_medley_in_green_coconut_coriander_masala",
        "color": "earthy_olive_green_to_amber_with_oil_gloss",
        "identifiable_components": [
            "green_papdi_beans_(surti_papdi)",
            "purple_yam_cubes_(kand)",
            "sweet_potato_cubes_(shakariya)",
            "baby_brinjals_stuffed_with_masala",
            "golden_fried_methi_muthias_(fenugreek_dumplings)",
            "raw_banana_pieces"
        ]
    },
    key_ingredients=["surti papdi / flat beans", "purple yam (kand)", "baby brinjals", "sweet potatoes", "methi muthia (fenugreek besan dumplings)", "fresh coconut", "green garlic", "coriander", "ajwain", "peanut oil"],
    possible_ingredients=["pigeon peas (tuvar lilva)"],
    hard_negatives=["PB_CURRY_SARSON_KA_SAAG", "MH_CURRY_BHARLI_VANGI", "TN_CURRY_AVIYAL"],
    density_g_cm3=1.02,
    default_serving_weight_g=220.0,
    nutrition_per_100g={"calories": 185.0, "protein_g": 4.8, "carbs_g": 21.0, "fat_g": 9.5, "fiber_g": 5.2, "sodium_mg": 310.0},
    hierarchy=WestIndianHierarchy(
        level3_state_region="Gujarat",
        level4_cuisine="Gujarati",
        level5_food_family="Curries/Usal",
        level6_food_type="Undhiyu",
        level7_variant="Surti Undhiyu",
        level8_cooking_method=["slow_simmered_pot", "dum_cooked"],
        level9_default_portion="1 bowl (220g)",
        nutrition_ref_id="wi_undhiyu_surti"
    )
))

register_west_food(WestIndianFoodClass(
    permanent_id="GJ_MAIN_DAL_DHOKLI",
    canonical_name="Gujarati Dal Dhokli",
    alternate_names=["dal dhokli", "daal dhokli", "gujarati pasta stew"],
    regional_names={"English": "Spiced Whole Wheat Pasta Diamonds in Sweet-Sour Tuvar Dal", "Gujarati": "દાળ ઢોકળી"},
    vegetarian=True,
    gravy_type="thin_gravy",
    visual_features={
        "dal": "thin_aromatic_golden_amber_tuvar_dal_with_mustard_cumin_clove_tempering",
        "pasta": "diamond_cut_unleavened_spiced_wheat_flour_dumpling_sheets_floating_inside",
        "garnishes": ["roasted_peanuts", "fresh_coriander", "dollop_of_desi_ghee", "lemon_squeeze"]
    },
    key_ingredients=["toor dal (pigeon pea)", "wheat flour dhokli pieces", "jaggery", "kokum / lemon", "peanuts", "mustard seeds", "cloves", "cinnamon", "desi ghee"],
    possible_ingredients=["curry leaves"],
    hard_negatives=["PB_CURRY_DAL_TADKA", "RJ_CURRY_GATTE_KI_SABZI", "GJ_CURRY_KADHI"],
    density_g_cm3=1.04,
    default_serving_weight_g=250.0,
    nutrition_per_100g={"calories": 140.0, "protein_g": 5.2, "carbs_g": 22.0, "fat_g": 3.8, "fiber_g": 3.2, "sodium_mg": 280.0},
    hierarchy=WestIndianHierarchy(
        level3_state_region="Gujarat",
        level4_cuisine="Gujarati",
        level5_food_family="Curries/Usal",
        level6_food_type="Dal Dhokli",
        level7_variant="Gujarati Dal Dhokli",
        level8_cooking_method=["simmered_pasta_in_dal"],
        level9_default_portion="1 large bowl (250g)",
        nutrition_ref_id="wi_dal_dhokli"
    )
))

register_west_food(WestIndianFoodClass(
    permanent_id="GJ_BREAD_THEPLA_METHI",
    canonical_name="Gujarati Methi Thepla",
    alternate_names=["methi thepla", "thepla", "gujarati flatbread", "masala thepla"],
    regional_names={"English": "Spiced Fenugreek & Yogurt Unleavened Flatbread", "Gujarati": "મેથીના થેપલા", "Hindi": "मेथी थेपला"},
    vegetarian=True,
    gravy_type="dry",
    visual_features={
        "shape": "ultra_thin_flexible_circular_disc",
        "thickness_mm": 1.5,
        "diameter_cm": 18.0,
        "surface": "densely_flecked_with_chopped_dark_green_methi_leaves_and_white_sesame",
        "color": "golden_yellow_tan_with_brown_roasting_spots",
        "texture": "pliable_soft_can_be_rolled_up_without_cracking"
    },
    key_ingredients=["whole wheat flour", "fresh fenugreek leaves (methi)", "yogurt (curd)", "white sesame seeds", "turmeric", "ajwain", "red chilli powder", "peanut oil"],
    possible_ingredients=["besan addition for softness"],
    hard_negatives=["PB_PARATHA_METHI", "PB_BREAD_ROTI_TAWA", "MH_BREAD_BHAKRI_JOWAR"],
    density_g_cm3=0.80,
    default_serving_weight_g=45.0,
    nutrition_per_100g={"calories": 275.0, "protein_g": 7.5, "carbs_g": 42.0, "fat_g": 9.5, "fiber_g": 5.0, "sodium_mg": 290.0},
    hierarchy=WestIndianHierarchy(
        level3_state_region="Gujarat",
        level4_cuisine="Gujarati",
        level5_food_family="Breads",
        level6_food_type="Thepla",
        level7_variant="Methi Thepla",
        level8_cooking_method=["rolled_thin", "tawa_roasted_in_oil"],
        level9_default_portion="2 pieces (90g)",
        nutrition_ref_id="wi_thepla_methi"
    )
))

register_west_food(WestIndianFoodClass(
    permanent_id="GJ_BREAD_ROTLA_BAJRA",
    canonical_name="Gujarati Bajra Rotla",
    alternate_names=["bajra rotla", "kathiyawadi rotla", "gujarati rotla"],
    regional_names={"English": "Kathiyawadi Rustic Thick Pearl Millet Flatbread", "Gujarati": "બાજરીનો રોટલો"},
    vegetarian=True,
    gravy_type="dry",
    visual_features={
        "shape": "thick_rustic_hand_patted_disc",
        "thickness_mm": 6.0,
        "diameter_cm": 18.0,
        "surface": "charred_clay_tavdi_spots_cracked_rustic_edges",
        "color": "earthy_ash_greyish_brown",
        "serving": "liberal_coating_of_white_butter_(safed_makhan)_or_ghee_with_jaggery"
    },
    key_ingredients=["pearl millet flour (bajra)", "warm water", "salt", "desi white butter"],
    possible_ingredients=["garlic chutney accompaniment"],
    hard_negatives=["RJ_BREAD_BAJRA_ROTI", "MH_BREAD_BHAKRI_BAJRA", "PB_BREAD_ROTI_MAKKI"],
    density_g_cm3=0.88,
    default_serving_weight_g=100.0,
    nutrition_per_100g={"calories": 255.0, "protein_g": 7.8, "carbs_g": 47.0, "fat_g": 4.5, "fiber_g": 7.2, "sodium_mg": 160.0},
    hierarchy=WestIndianHierarchy(
        level3_state_region="Gujarat",
        level4_cuisine="Gujarati",
        level5_food_family="Breads",
        level6_food_type="Rotla",
        level7_variant="Bajra Rotla",
        level8_cooking_method=["hand_patted", "clay_pan_tavdi_roasted"],
        level9_default_portion="1 piece (100g)",
        nutrition_ref_id="wi_rotla_bajra"
    )
))

register_west_food(WestIndianFoodClass(
    permanent_id="GJ_FARSAN_FAFDA_JALEBI",
    canonical_name="Fafda Jalebi Combo",
    alternate_names=["fafda jalebi", "fafda", "gujarati fafda"],
    regional_names={"English": "Crisp Gram Flour Strips with Sweet Saffron Jalebi & Papaya Sambharo", "Gujarati": "ફાફડા જલેબી"},
    vegetarian=True,
    gravy_type="dry",
    visual_features={
        "fafda": "long_flat_golden_yellow_brittle_ribbon_strips_speckled_with_ajwain",
        "jalebi": "bright_orange_crystalline_spiral_pretzels_dripping_with_saffron_syrup",
        "accompaniments": ["warm_shredded_raw_papaya_sambharo", "fried_salted_green_chillies", "besan_kadhi_chutney"]
    },
    key_ingredients=["besan", "carom seeds (ajwain)", "black pepper", "papad khar (alkaline salt)", "maida", "saffron syrup", "raw papaya", "green chillies"],
    possible_ingredients=["asafoetida"],
    hard_negatives=["NI_SWEET_JALEBI", "RJ_SNACK_PYAZ_KACHORI"],
    density_g_cm3=0.82,
    default_serving_weight_g=220.0,
    nutrition_per_100g={"calories": 360.0, "protein_g": 5.5, "carbs_g": 56.0, "fat_g": 13.5, "fiber_g": 2.5, "sugar_g": 32.0, "sodium_mg": 380.0},
    hierarchy=WestIndianHierarchy(
        level3_state_region="Gujarat",
        level4_cuisine="Gujarati",
        level5_food_family="Farsan",
        level6_food_type="Fafda",
        level7_variant="Fafda Jalebi Combo",
        level8_cooking_method=["deep_fried"],
        level9_default_portion="1 combo plate (100g fafda + 100g jalebi + sides, 220g)",
        nutrition_ref_id="wi_fafda_jalebi"
    )
))

register_west_food(WestIndianFoodClass(
    permanent_id="GJ_THALI_GUJARATI",
    canonical_name="Traditional Gujarati Thali",
    alternate_names=["gujarati thali", "kathiyawadi thali", "gujarati feast"],
    regional_names={"English": "Multi-Course Gujarati Vegetarian Platter", "Gujarati": "ગુજરાતી થાળી"},
    vegetarian=True,
    gravy_type="semi_gravy",
    visual_features={
        "presentation": "large_kansa_or_steel_platter_ringed_with_8_to_14_katori_bowls",
        "dishes": ["phulka/puri", "thepla", "gujarati_dal", "gujarati_kadhi", "undhiyu/shaak", "khaman/farsan", "khichdi", "kachumber", "papad", "shrikhand/sweet", "chaas"]
    },
    key_ingredients=["toor dal", "buttermilk", "vegetables", "wheat", "besan", "jaggery", "ghee", "spices"],
    possible_ingredients=["pickle", "chutney"],
    hard_negatives=["PB_THALI_PUNJABI", "HP_MAIN_DHAM_FULL_MEAL", "TN_MEAL_BANANA_LEAF_FEAST"],
    density_g_cm3=0.94,
    default_serving_weight_g=620.0,
    nutrition_per_100g={"calories": 165.0, "protein_g": 4.8, "carbs_g": 25.0, "fat_g": 5.5, "fiber_g": 3.4, "sodium_mg": 310.0},
    hierarchy=WestIndianHierarchy(
        level3_state_region="Gujarat",
        level4_cuisine="Gujarati",
        level5_food_family="Thali",
        level6_food_type="Platter",
        level7_variant="Traditional Gujarati Thali",
        level8_cooking_method=["assembled_multi_course"],
        level9_default_portion="Full Thali (620g)",
        nutrition_ref_id="wi_thali_gujarati"
    )
))

# =============================================================================
# 5. GOA & KONKAN SEAFOOD / CURRIES (FISH CURRY, VINDALOO, CAFREAL, SOL KADHI)
# =============================================================================

register_west_food(WestIndianFoodClass(
    permanent_id="GA_CURRY_FISH_GOAN",
    canonical_name="Goan Fish Curry (Xitt Codi)",
    alternate_names=["goan fish curry", "xitt codi", "goan coconut fish curry", "fish curry rice"],
    regional_names={"English": "Kingfish Simmered in Tangy Coconut & Kokum Orange Curry", "Konkani": "कडी निस्तां", "Portuguese": "Caril de Peixe"},
    vegetarian=False,
    gravy_type="coconut_gravy",
    visual_features={
        "gravy_color": "vibrant_warm_orange_to_coral_red",
        "texture": "silky_medium_thick_coconut_milk_emulsion",
        "fish": "tender_steak_cuts_of_kingfish_(surmai)_or_pomfret_with_skin_and_central_bone",
        "tangy_marker": "dark_purple_black_kokum_petals_visible_in_broth"
    },
    key_ingredients=["fresh kingfish/pomfret steaks", "fresh grated coconut / coconut milk", "kashmiri chillies", "kokum (solam / amsul)", "coriander seeds", "garlic", "turmeric", "fenugreek"],
    possible_ingredients=["tirphal / teppal (sichuan pepper relative)"],
    hard_negatives=["GA_CURRY_PORK_VINDALOO", "KL_CURRY_MEEN_KERALA", "GA_CURRY_CHICKEN_CAFREAL"],
    density_g_cm3=1.05,
    default_serving_weight_g=240.0,
    nutrition_per_100g={"calories": 145.0, "protein_g": 12.5, "carbs_g": 4.2, "fat_g": 8.8, "fiber_g": 1.5, "sodium_mg": 380.0},
    hierarchy=WestIndianHierarchy(
        level3_state_region="Goa",
        level4_cuisine="Goan",
        level5_food_family="Seafood",
        level6_food_type="Fish Curry",
        level7_variant="Goan Fish Curry",
        level8_cooking_method=["coconut_gravy", "gentle_simmer"],
        level9_default_portion="1 bowl (240g)",
        nutrition_ref_id="wi_curry_fish_goan"
    )
))

register_west_food(WestIndianFoodClass(
    permanent_id="GA_CURRY_PORK_VINDALOO",
    canonical_name="Goan Pork Vindaloo",
    alternate_names=["pork vindaloo", "vindaloo", "goan vindaloo", "vinha d'alhos"],
    regional_names={"English": "Fiery Tangy Pork Braised in Toddy Vinegar & Garlic Masala", "Konkani": "विंडालू", "Portuguese": "Carne de Vinha d'Alhos"},
    vegetarian=False,
    gravy_type="oily_gravy",
    visual_features={
        "viscosity": "thick_rich_dark_gravy_with_spicy_red_vinegar_oil_sheen",
        "color": "deep_dark_blood_red_to_mahogany",
        "meat": "succulent_cubed_pork_belly_or_shoulder_with_fat_layers",
        "absence": "zero_coconut_zero_cream_(key_discriminator_from_other_goan_curries)"
    },
    key_ingredients=["pork chunks with fat", "naturally fermented toddy vinegar / coconut vinegar", "kashmiri dried chillies", "garlic (heavy quantity)", "ginger", "cinnamon", "cloves", "cumin"],
    possible_ingredients=["sugar/jaggery pinch to balance acid"],
    hard_negatives=["GA_CURRY_FISH_GOAN", "RJ_NONVEG_LAAL_MAAS", "JK_NONVEG_ROGAN_JOSH"],
    density_g_cm3=1.06,
    default_serving_weight_g=220.0,
    nutrition_per_100g={"calories": 245.0, "protein_g": 17.5, "carbs_g": 3.5, "fat_g": 18.0, "fiber_g": 1.0, "sodium_mg": 460.0},
    hierarchy=WestIndianHierarchy(
        level3_state_region="Goa",
        level4_cuisine="Goan",
        level5_food_family="Curries/Usal",
        level6_food_type="Meat Curry",
        level7_variant="Pork Vindaloo",
        level8_cooking_method=["vinegar_marinated", "slow_braised"],
        level9_default_portion="1 bowl (220g)",
        nutrition_ref_id="wi_pork_vindaloo"
    )
))

register_west_food(WestIndianFoodClass(
    permanent_id="GA_NONVEG_CHICKEN_CAFREAL",
    canonical_name="Goan Chicken Cafreal",
    alternate_names=["chicken cafreal", "cafreal", "goan green chicken", "galinha cafreal"],
    regional_names={"English": "Pan-Braised Chicken in Fiery Emerald Herb & Rum Masala", "Konkani": "काफ्रियाल", "Portuguese": "Frango Cafreal"},
    vegetarian=False,
    gravy_type="semi_gravy",
    visual_features={
        "color": "deep_vibrant_dark_forest_green",
        "texture": "thick_spiced_herb_paste_clinging_tightly_to_charred_chicken_cuts",
        "meat": "bone_in_chicken_legs_or_breasts_with_crisp_pan_char_marks",
        "sides": ["round_potato_wedges_fried_in_the_same_green_oil"]
    },
    key_ingredients=["bone-in chicken cuts", "fresh coriander leaves (large bunches)", "green chillies", "cinnamon", "cloves", "toddy vinegar / rum", "ginger-garlic", "potatoes"],
    possible_ingredients=["onion garnish"],
    hard_negatives=["PB_CURRY_PALAK_PANEER", "PB_NONVEG_BUTTER_CHICKEN", "GA_CURRY_FISH_GOAN"],
    density_g_cm3=1.02,
    default_serving_weight_g=240.0,
    nutrition_per_100g={"calories": 195.0, "protein_g": 18.0, "carbs_g": 4.5, "fat_g": 11.8, "fiber_g": 1.5, "sodium_mg": 410.0},
    hierarchy=WestIndianHierarchy(
        level3_state_region="Goa",
        level4_cuisine="Goan",
        level5_food_family="Curries/Usal",
        level6_food_type="Chicken Curry",
        level7_variant="Chicken Cafreal",
        level8_cooking_method=["green_masala_marinated", "pan_shallow_braised"],
        level9_default_portion="1 plate (240g)",
        nutrition_ref_id="wi_chicken_cafreal"
    )
))

register_west_food(WestIndianFoodClass(
    permanent_id="KN_BEVERAGE_SOL_KADHI",
    canonical_name="Sol Kadhi (Kokum Kadhi)",
    alternate_names=["sol kadhi", "solkadhi", "kokum curry drink", "konkani digestive"],
    regional_names={"English": "Chilled Pink Coconut Milk & Kokum Infusion", "Marathi": "सोलकढी", "Konkani": "सोलकडी"},
    vegetarian=True,
    gravy_type="thin_gravy",
    visual_features={
        "liquid": "thin_pouring_opaque_creamy_drink",
        "color": "distinctive_pastel_pink_to_rose_mauve_hue",
        "garnishes": ["finely_chopped_coriander", "crushed_garlic_hint", "slit_green_chilli"]
    },
    key_ingredients=["fresh thick coconut milk", "kokum peel extract (amsul/solam - provides signature pink color)", "garlic", "green chillies", "salt", "coriander"],
    possible_ingredients=["cumin powder"],
    hard_negatives=["GJ_BEVERAGE_CHAAS", "PB_CURRY_KADHI_PAKORA", "TN_CURRY_MOR_KUZHAMBU"],
    density_g_cm3=1.01,
    default_serving_weight_g=150.0,
    nutrition_per_100g={"calories": 75.0, "protein_g": 1.2, "carbs_g": 3.8, "fat_g": 6.2, "fiber_g": 0.5, "sodium_mg": 180.0},
    hierarchy=WestIndianHierarchy(
        level3_state_region="Konkan",
        level4_cuisine="Konkani",
        level5_food_family="Beverages",
        level6_food_type="Digestive Drink",
        level7_variant="Sol Kadhi",
        level8_cooking_method=["raw_extracted_chilled"],
        level9_default_portion="1 glass (150g)",
        nutrition_ref_id="wi_sol_kadhi"
    )
))

register_west_food(WestIndianFoodClass(
    permanent_id="GA_THALI_FISH_FEAST",
    canonical_name="Goan Fish Thali",
    alternate_names=["goan fish thali", "fish curry thali", "goan thali"],
    regional_names={"English": "Traditional Coastal Goan Seafood Feast", "Konkani": "नुस्ते जेवण"},
    vegetarian=False,
    gravy_type="coconut_gravy",
    visual_features={
        "presentation": "stainless_steel_thali_with_steamed_rice_mound_at_center",
        "dishes": ["mound_of_goan_boiled_rice", "orange_fish_curry_katori", "rava_coated_crisp_fried_fish_steak", "cabbage_foogath", "kismur_(dry_prawn_salad)", "sol_kadhi_glass", "pickle"]
    },
    key_ingredients=["rice", "kingfish / mackerel", "coconut", "kokum", "rava (semolina)", "cabbage", "dried prawns", "spices"],
    possible_ingredients=["clam sukka (tisreo)"],
    hard_negatives=["GJ_THALI_GUJARATI", "PB_THALI_PUNJABI", "TN_MEAL_BANANA_LEAF_FEAST"],
    density_g_cm3=0.98,
    default_serving_weight_g=580.0,
    nutrition_per_100g={"calories": 170.0, "protein_g": 9.5, "carbs_g": 21.0, "fat_g": 5.8, "fiber_g": 2.2, "sodium_mg": 380.0},
    hierarchy=WestIndianHierarchy(
        level3_state_region="Goa",
        level4_cuisine="Goan",
        level5_food_family="Thali",
        level6_food_type="Seafood Platter",
        level7_variant="Goan Fish Thali",
        level8_cooking_method=["assembled_multi_dish"],
        level9_default_portion="Full Fish Thali (580g)",
        nutrition_ref_id="wi_thali_fish_goan"
    )
))

# =============================================================================
# 6. MAHARASHTRIAN & GUJARATI SWEETS (MODAK, SHRIKHAND, BASUNDI, MOHANTHAL)
# =============================================================================

register_west_food(WestIndianFoodClass(
    permanent_id="MH_SWEET_UKADICHE_MODAK",
    canonical_name="Ukadiche Modak",
    alternate_names=["ukadiche modak", "steamed modak", "ganesh modak"],
    regional_names={"English": "Steamed Rice Dumpling with Fresh Coconut & Jaggery Filling", "Marathi": "उकडीचे मोदक"},
    vegetarian=True,
    gravy_type="dry",
    visual_features={
        "shape": "pleated_fluted_conical_drop_dumpling",
        "skin": "soft_steamed_translucent_white_rice_dough_wrapper",
        "height_cm": 5.5,
        "diameter_cm": 4.5,
        "serving": "drizzle_of_pure_yellow_cow_ghee_over_the_top_tip"
    },
    key_ingredients=["rice flour (steamed ukad dough)", "fresh grated coconut", "jaggery (gul)", "cardamom powder", "nutmeg", "ghee"],
    possible_ingredients=["saffron strands (kesar)"],
    hard_negatives=["MH_SWEET_FRIED_MODAK", "TN_BREAKFAST_IDLI_PLAIN", "CHINESE_DIM_SUM"],
    density_g_cm3=0.92,
    default_serving_weight_g=50.0,
    nutrition_per_100g={"calories": 240.0, "protein_g": 3.2, "carbs_g": 46.0, "fat_g": 5.2, "fiber_g": 3.0, "sugar_g": 24.0, "sodium_mg": 45.0},
    hierarchy=WestIndianHierarchy(
        level3_state_region="Maharashtra",
        level4_cuisine="Maharashtrian",
        level5_food_family="Sweets",
        level6_food_type="Modak",
        level7_variant="Ukadiche Modak",
        level8_cooking_method=["steamed"],
        level9_default_portion="2 pieces (100g)",
        nutrition_ref_id="wi_modak_ukadiche"
    )
))

register_west_food(WestIndianFoodClass(
    permanent_id="WI_SWEET_SHRIKHAND",
    canonical_name="Kesar Pista Shrikhand",
    alternate_names=["shrikhand", "amrakhand", "kesar shrikhand", "chakka sweet"],
    regional_names={"English": "Silky Sweetened Hung Curd Dessert with Saffron & Pistachio", "Marathi": "श्रीखंड", "Gujarati": "શ્રીખંડ"},
    vegetarian=True,
    gravy_type="creamy_gravy",
    visual_features={
        "viscosity": "ultra_thick_luxurious_velvety_cream_paste",
        "color": "pale_warm_saffron_yellow",
        "garnishes": ["slivered_pistachios", "sliced_almonds", "crushed_cardamom", "ruby_saffron_strands"]
    },
    key_ingredients=["hung curd (chakka - strained yogurt)", "powdered sugar", "saffron milk", "cardamom powder", "pistachios", "almonds"],
    possible_ingredients=["mango pulp (for Amrakhand)"],
    hard_negatives=["DL_STREET_DAHI_BHALLA", "WI_SWEET_BASUNDI", "TN_SWEET_PAYASAM"],
    density_g_cm3=1.12,
    default_serving_weight_g=100.0,
    nutrition_per_100g={"calories": 285.0, "protein_g": 7.5, "carbs_g": 36.0, "fat_g": 12.0, "fiber_g": 0.5, "sugar_g": 32.0, "sodium_mg": 65.0},
    hierarchy=WestIndianHierarchy(
        level3_state_region="Maharashtra",
        level4_cuisine="Maharashtrian",
        level5_food_family="Sweets",
        level6_food_type="Yogurt Sweet",
        level7_variant="Kesar Shrikhand",
        level8_cooking_method=["strained_whisked_chilled"],
        level9_default_portion="1 small bowl (100g)",
        nutrition_ref_id="wi_shrikhand"
    )
))

register_west_food(WestIndianFoodClass(
    permanent_id="MH_CURRY_TAMBDA_RASSA",
    canonical_name="Kolhapuri Tambda Rassa",
    alternate_names=["tambda rassa", "tambada rassa", "kolhapuri red broth", "mutton tambda rassa"],
    regional_names={"English": "Fiery Red Mutton Bone Broth with Kolhapuri Masala", "Marathi": "तांबडा रस्सा"},
    vegetarian=False,
    gravy_type="thin_gravy",
    visual_features={
        "viscosity": "ultra_thin_translucent_spiced_soup_broth",
        "color": "vibrant_fiery_crimson_red_with_floating_chilli_oil_droplets",
        "meat": "served_in_a_bowl_often_accompanied_by_mutton_sukka_cuts"
    },
    key_ingredients=["mutton bone stock", "kolhapuri kanda lasun masala", "red chillies (lavangi)", "cinnamon", "cloves", "poppy seeds (khus khus)", "oil"],
    possible_ingredients=["fresh coriander garnish"],
    hard_negatives=["MH_CURRY_PANDHRA_RASSA", "RJ_NONVEG_LAAL_MAAS", "GA_CURRY_PORK_VINDALOO"],
    density_g_cm3=1.01,
    default_serving_weight_g=180.0,
    nutrition_per_100g={"calories": 95.0, "protein_g": 6.5, "carbs_g": 2.5, "fat_g": 6.8, "fiber_g": 0.8, "sodium_mg": 380.0},
    hierarchy=WestIndianHierarchy(
        level3_state_region="Maharashtra",
        level4_cuisine="Maharashtrian",
        level5_food_family="Curries/Usal",
        level6_food_type="Broth",
        level7_variant="Tambda Rassa",
        level8_cooking_method=["slow_simmered_bone_broth"],
        level9_default_portion="1 bowl (180g)",
        nutrition_ref_id="wi_tambda_rassa"
    )
))

register_west_food(WestIndianFoodClass(
    permanent_id="MH_CURRY_PANDHRA_RASSA",
    canonical_name="Kolhapuri Pandhra Rassa",
    alternate_names=["pandhra rassa", "pandhara rassa", "white mutton broth"],
    regional_names={"English": "Rich White Mutton Broth with Coconut Milk & Whole Spices", "Marathi": "पांढरा रस्सा"},
    vegetarian=False,
    gravy_type="coconut_gravy",
    visual_features={
        "viscosity": "milky_opaque_aromatic_thin_soup",
        "color": "silky_pure_ivory_white_with_faint_floating_clarified_ghee_eyes",
        "absence": "zero_turmeric_zero_red_chilli_(distinguishes_from_tambda_rassa)"
    },
    key_ingredients=["mutton bone broth", "fresh coconut milk", "poppy seed paste (khus khus)", "white sesame", "green cardamom", "white pepper", "ginger", "cinnamon"],
    possible_ingredients=["cashew paste"],
    hard_negatives=["MH_CURRY_TAMBDA_RASSA", "KN_BEVERAGE_SOL_KADHI", "JK_CURRY_GUSHTABA"],
    density_g_cm3=1.02,
    default_serving_weight_g=180.0,
    nutrition_per_100g={"calories": 115.0, "protein_g": 7.0, "carbs_g": 3.2, "fat_g": 8.5, "fiber_g": 0.5, "sodium_mg": 320.0},
    hierarchy=WestIndianHierarchy(
        level3_state_region="Maharashtra",
        level4_cuisine="Maharashtrian",
        level5_food_family="Curries/Usal",
        level6_food_type="Broth",
        level7_variant="Pandhra Rassa",
        level8_cooking_method=["coconut_milk_infusion", "simmered"],
        level9_default_portion="1 bowl (180g)",
        nutrition_ref_id="wi_pandhra_rassa"
    )
))

register_west_food(WestIndianFoodClass(
    permanent_id="MH_CONDIMENT_THECHA",
    canonical_name="Kolhapuri Mirchi Thecha",
    alternate_names=["thecha", "mirchi thecha", "hirvi mirchi thecha", "kolhapuri thecha"],
    regional_names={"English": "Coarsely Pounded Fiery Green Chilli, Garlic & Peanut Relish", "Marathi": "मिरचीचा ठेचा"},
    vegetarian=True,
    gravy_type="dry",
    visual_features={
        "texture": "rustic_coarse_mortar_pestle_pounded_mash",
        "color": "mottled_bright_and_dark_green_flecked_with_white_garlic_and_golden_peanuts",
        "sheen": "glistening_with_groundnut_oil"
    },
    key_ingredients=["spicy green chillies (pan-roasted)", "whole garlic cloves", "roasted peanuts", "cumin seeds", "salt", "peanut oil"],
    possible_ingredients=["lemon juice"],
    hard_negatives=["MUM_STREET_CHUTNEY_GREEN", "TN_CHUTNEY_MINT"],
    density_g_cm3=0.92,
    default_serving_weight_g=25.0,
    nutrition_per_100g={"calories": 240.0, "protein_g": 7.5, "carbs_g": 12.0, "fat_g": 18.5, "fiber_g": 4.8, "sodium_mg": 680.0},
    hierarchy=WestIndianHierarchy(
        level3_state_region="Maharashtra",
        level4_cuisine="Maharashtrian",
        level5_food_family="Curries/Usal",
        level6_food_type="Relish",
        level7_variant="Mirchi Thecha",
        level8_cooking_method=["pan_roasted", "mortar_pounded"],
        level9_default_portion="1 spoonful (25g)",
        nutrition_ref_id="wi_thecha"
    )
))

register_west_food(WestIndianFoodClass(
    permanent_id="MH_CURRY_BHARLI_VANGI",
    canonical_name="Bharli Vangi",
    alternate_names=["bharli vangi", "stuffed brinjal maharashtrian", "bharwa baingan maharashtra"],
    regional_names={"English": "Baby Eggplants Stuffed with Peanut, Coconut & Goda Masala", "Marathi": "भरली वांगी"},
    vegetarian=True,
    gravy_type="semi_gravy",
    visual_features={
        "vegetable": "whole_small_purple_brinjals_cross_slit_with_green_stalk_intact",
        "gravy": "thick_grainy_dark_amber_brown_peanut_coconut_gravy",
        "surface": "shimmering_oil_meniscus_with_sesame_and_coriander"
    },
    key_ingredients=["baby brinjals", "roasted peanut powder (danyache kut)", "dry desiccated coconut", "goda masala", "sesame seeds", "tamarind-jaggery", "onions", "oil"],
    possible_ingredients=["garlic"],
    hard_negatives=["GJ_MAIN_UNDHIYU_SURTI", "TS_CURRY_BAGARA_BAINGAN", "PB_CURRY_BAINGAN_BHARTA"],
    density_g_cm3=1.04,
    default_serving_weight_g=200.0,
    nutrition_per_100g={"calories": 160.0, "protein_g": 4.5, "carbs_g": 13.5, "fat_g": 10.2, "fiber_g": 5.0, "sodium_mg": 310.0},
    hierarchy=WestIndianHierarchy(
        level3_state_region="Maharashtra",
        level4_cuisine="Maharashtrian",
        level5_food_family="Curries/Usal",
        level6_food_type="Eggplant Curry",
        level7_variant="Bharli Vangi",
        level8_cooking_method=["stuffed", "slow_braised_pot"],
        level9_default_portion="1 bowl (200g)",
        nutrition_ref_id="wi_bharli_vangi"
    )
))

register_west_food(WestIndianFoodClass(
    permanent_id="KN_SEAFOOD_BOMBIL_FRY",
    canonical_name="Crispy Bombil Fry (Bombay Duck)",
    alternate_names=["bombil fry", "bombay duck fry", "rava bombil fry"],
    regional_names={"English": "Crisp Semolina-Crusted Fresh Bombay Duck Fish", "Marathi": "बोंबील फ्राय", "Konkani": "बोंबिल फ्राय"},
    vegetarian=False,
    gravy_type="dry",
    visual_features={
        "shape": "flattened_elongated_fish_fillet_strips",
        "crust": "golden_crunchy_rava_semolina_and_rice_flour_crust",
        "length_cm": 14.0,
        "interior": "succulent_delicate_melt_in_mouth_white_flesh"
    },
    key_ingredients=["fresh bombil (bombay duck fish)", "malvani masala / red chilli", "turmeric", "lemon / agal (kokum water)", "semolina (rava) & rice flour coating", "oil for shallow frying"],
    possible_ingredients=["garlic paste"],
    hard_negatives=["KN_SEAFOOD_SURMAI_FRY", "TN_SEAFOOD_MEEN_VARUVAL", "GA_CURRY_FISH_GOAN"],
    density_g_cm3=0.88,
    default_serving_weight_g=120.0,
    nutrition_per_100g={"calories": 210.0, "protein_g": 16.5, "carbs_g": 12.0, "fat_g": 11.2, "fiber_g": 0.8, "sodium_mg": 390.0},
    hierarchy=WestIndianHierarchy(
        level3_state_region="Konkan",
        level4_cuisine="Malvani",
        level5_food_family="Seafood",
        level6_food_type="Fish Fry",
        level7_variant="Bombil Fry",
        level8_cooking_method=["rava_coated", "shallow_fried"],
        level9_default_portion="2 pieces (120g)",
        nutrition_ref_id="wi_bombil_fry"
    )
))

register_west_food(WestIndianFoodClass(
    permanent_id="KN_SEAFOOD_SURMAI_FRY",
    canonical_name="Malvani Surmai Fry (Kingfish)",
    alternate_names=["surmai fry", "kingfish fry", "malvani fish fry", "tawa surmai"],
    regional_names={"English": "Spicy Semolina Coated Kingfish Steaks", "Marathi": "सुरमई फ्राय"},
    vegetarian=False,
    gravy_type="dry",
    visual_features={
        "shape": "oval_or_circular_steaks_with_central_round_bone_ring",
        "crust": "golden_orange_spiced_semolina_coating_with_char_freckles",
        "diameter_cm": 11.0,
        "thickness_mm": 18.0
    },
    key_ingredients=["surmai (kingfish steaks)", "malvani fish masala", "kokum agal", "rava (sooji)", "rice flour", "oil"],
    possible_ingredients=["onion slices and lemon garnish"],
    hard_negatives=["KN_SEAFOOD_BOMBIL_FRY", "GA_CURRY_FISH_GOAN", "KL_SEAFOOD_KARIMEEN_POLLICHATHU"],
    density_g_cm3=0.92,
    default_serving_weight_g=150.0,
    nutrition_per_100g={"calories": 230.0, "protein_g": 21.0, "carbs_g": 8.5, "fat_g": 12.5, "fiber_g": 0.5, "sodium_mg": 410.0},
    hierarchy=WestIndianHierarchy(
        level3_state_region="Konkan",
        level4_cuisine="Malvani",
        level5_food_family="Seafood",
        level6_food_type="Fish Fry",
        level7_variant="Surmai Fry",
        level8_cooking_method=["rava_crusted", "pan_fried"],
        level9_default_portion="1 large steak (150g)",
        nutrition_ref_id="wi_surmai_fry"
    )
))

register_west_food(WestIndianFoodClass(
    permanent_id="GA_BREAD_POI",
    canonical_name="Goan Poi (Poee)",
    alternate_names=["goan poi", "poee", "goan bran bread", "pao poi"],
    regional_names={"English": "Traditional Whole Wheat & Wheat Bran Leavened Pocket Bread", "Konkani": "पोई", "Portuguese": "Pão Poi"},
    vegetarian=True,
    gravy_type="dry",
    visual_features={
        "shape": "hollow_circular_inflated_pocket_bread",
        "diameter_cm": 12.0,
        "surface": "dusted_with_coarse_wheat_bran_flakes_(bhusa)",
        "color": "golden_tan_with_rustic_speckles",
        "interior": "hollow_pit_like_pita_pocket"
    },
    key_ingredients=["whole wheat flour", "wheat bran (bhusa)", "toddy or active yeast", "warm water", "salt"],
    possible_ingredients=["pinch of sugar"],
    hard_negatives=["GA_BREAD_PAO", "PB_BREAD_ROTI_TAWA", "UP_BREAD_POORI"],
    density_g_cm3=0.68,
    default_serving_weight_g=65.0,
    nutrition_per_100g={"calories": 245.0, "protein_g": 8.8, "carbs_g": 48.0, "fat_g": 1.5, "fiber_g": 7.5, "sodium_mg": 280.0},
    hierarchy=WestIndianHierarchy(
        level3_state_region="Goa",
        level4_cuisine="Goan",
        level5_food_family="Breads",
        level6_food_type="Bread Bun",
        level7_variant="Goan Poi",
        level8_cooking_method=["wood_fired_clay_oven_baked"],
        level9_default_portion="1 piece (65g)",
        nutrition_ref_id="wi_poi_goan"
    )
))

register_west_food(WestIndianFoodClass(
    permanent_id="GA_BREAD_PAO",
    canonical_name="Goan Pao (Laadi Pav)",
    alternate_names=["goan pao", "pao", "pav bun", "goan bread"],
    regional_names={"English": "Crusty Wood-Fired Leavened Bread Roll", "Konkani": "पाव", "Portuguese": "Pão"},
    vegetarian=True,
    gravy_type="dry",
    visual_features={
        "shape": "quad_sliced_square_pillow_roll",
        "crust": "golden_brown_crisp_crunchy_crust_on_top_soft_sides",
        "crumb": "airy_elastic_fermented_crumb"
    },
    key_ingredients=["refined flour (maida)", "yeast / toddy fermentation", "water", "salt", "oil"],
    possible_ingredients=["butter"],
    hard_negatives=["GA_BREAD_POI", "DL_BREAD_BHATURA", "PB_BREAD_KULCHA_PLAIN"],
    density_g_cm3=0.65,
    default_serving_weight_g=50.0,
    nutrition_per_100g={"calories": 260.0, "protein_g": 8.0, "carbs_g": 52.0, "fat_g": 2.0, "fiber_g": 2.2, "sodium_mg": 340.0},
    hierarchy=WestIndianHierarchy(
        level3_state_region="Goa",
        level4_cuisine="Goan",
        level5_food_family="Breads",
        level6_food_type="Bread Bun",
        level7_variant="Goan Pao",
        level8_cooking_method=["baked"],
        level9_default_portion="1 piece (50g)",
        nutrition_ref_id="wi_pao_goan"
    )
))

register_west_food(WestIndianFoodClass(
    permanent_id="GA_SWEET_BEBINCA",
    canonical_name="Goan Bebinca (Bibik)",
    alternate_names=["bebinca", "bibik", "goan seven layer cake"],
    regional_names={"English": "Traditional Multi-Layered Coconut Milk & Egg Pudding", "Konkani": "बेबिंका", "Portuguese": "Bebinca de Goa"},
    vegetarian=False,
    gravy_type="dry",
    visual_features={
        "shape": "layered_slice_showing_7_to_16_distinct_horizontal_strata",
        "color": "alternating_dark_caramel_brown_and_golden_amber_stripes",
        "texture": "succulent_dense_chewy_pudding_glossy_with_ghee"
    },
    key_ingredients=["thick coconut milk", "egg yolks", "refined flour (maida)", "sugar", "pure desi ghee", "nutmeg", "cardamom"],
    possible_ingredients=["vanilla essence"],
    hard_negatives=["RJ_SWEET_GHEVAR", "WI_SWEET_SHRIKHAND", "TN_SWEET_MYSORE_PAK"],
    density_g_cm3=1.14,
    default_serving_weight_g=100.0,
    nutrition_per_100g={"calories": 385.0, "protein_g": 5.2, "carbs_g": 48.0, "fat_g": 19.5, "fiber_g": 0.8, "sugar_g": 40.0, "sodium_mg": 85.0},
    hierarchy=WestIndianHierarchy(
        level3_state_region="Goa",
        level4_cuisine="Goan",
        level5_food_family="Sweets",
        level6_food_type="Layer Cake",
        level7_variant="Goan Bebinca",
        level8_cooking_method=["broiled_layer_by_layer", "baked"],
        level9_default_portion="1 slice (100g)",
        nutrition_ref_id="wi_bebinca"
    )
))

register_west_food(WestIndianFoodClass(
    permanent_id="GJ_CURRY_KADHI",
    canonical_name="Gujarati Kadhi",
    alternate_names=["gujarati kadhi", "sweet kadhi", "gujju kadhi"],
    regional_names={"English": "Sweet & Sour Thin Yogurt-Besan Broth with Cinnamon", "Gujarati": "ગુજરાતી કઢી"},
    vegetarian=True,
    gravy_type="thin_gravy",
    visual_features={
        "viscosity": "thin_pouring_silky_liquid_broth",
        "color": "pale_canary_ivory_yellow",
        "inclusions": "no_pakoras_smooth_uniform_liquid",
        "surface": "crackled_mustard_seeds_cloves_cinnamon_cinnamon_bark_curry_leaves"
    },
    key_ingredients=["sour curd / buttermilk", "gram flour (besan)", "jaggery or sugar", "ginger-green chilli paste", "cinnamon stick", "cloves", "mustard seeds", "hing", "curry leaves", "coriander"],
    possible_ingredients=["ghee tempering"],
    hard_negatives=["PB_CURRY_KADHI_PAKORA", "RJ_CURRY_KADHI", "TN_CURRY_MOR_KUZHAMBU"],
    density_g_cm3=1.03,
    default_serving_weight_g=180.0,
    nutrition_per_100g={"calories": 85.0, "protein_g": 3.2, "carbs_g": 11.5, "fat_g": 3.0, "fiber_g": 0.8, "sugar_g": 6.5, "sodium_mg": 280.0},
    hierarchy=WestIndianHierarchy(
        level3_state_region="Gujarat",
        level4_cuisine="Gujarati",
        level5_food_family="Curries/Usal",
        level6_food_type="Kadhi",
        level7_variant="Gujarati Kadhi",
        level8_cooking_method=["whisked_simmered", "tempered"],
        level9_default_portion="1 bowl (180g)",
        nutrition_ref_id="wi_kadhi_gujarati"
    )
))

register_west_food(WestIndianFoodClass(
    permanent_id="GJ_CURRY_SEV_TAMETA",
    canonical_name="Sev Tameta Nu Shaak",
    alternate_names=["sev tameta", "sev tamatar", "kathiyawadi sev tameta", "sev tomato curry"],
    regional_names={"English": "Tangy Sweet Tomato Curry Topped with Crisp Sev", "Gujarati": "સેવ ટામેટાનું શાક"},
    vegetarian=True,
    gravy_type="semi_gravy",
    visual_features={
        "gravy": "vibrant_red_simmered_tomato_curry_with_mild_sweetness",
        "topping": "generous_layer_of_thick_crunchy_besan_sev_(ratlami_or_nylon)",
        "surface": "chopped_fresh_coriander"
    },
    key_ingredients=["ripe tomatoes", "thick crunchy sev", "mustard seeds", "hing", "jaggery", "red chilli powder", "ginger", "curry leaves", "oil"],
    possible_ingredients=["garlic (Kathiyawadi style)"],
    hard_negatives=["UP_CURRY_ALOO_SABZI", "MUM_STREET_SEV_PURI", "DL_STREET_CHOLE_BHATURE"],
    density_g_cm3=1.04,
    default_serving_weight_g=200.0,
    nutrition_per_100g={"calories": 165.0, "protein_g": 4.5, "carbs_g": 18.0, "fat_g": 8.5, "fiber_g": 3.2, "sodium_mg": 390.0},
    hierarchy=WestIndianHierarchy(
        level3_state_region="Gujarat",
        level4_cuisine="Gujarati",
        level5_food_family="Curries/Usal",
        level6_food_type="Shaak",
        level7_variant="Sev Tameta",
        level8_cooking_method=["simmered", "sev_garnished"],
        level9_default_portion="1 bowl (200g)",
        nutrition_ref_id="wi_sev_tameta"
    )
))

register_west_food(WestIndianFoodClass(
    permanent_id="GJ_SNACK_HANDVO",
    canonical_name="Gujarati Handvo",
    alternate_names=["handvo", "vegetable handvo", "savory lentil cake"],
    regional_names={"English": "Baked Crisp Savory Lentil & Bottle Gourd Cake with Sesame Crust", "Gujarati": "હાંડવો"},
    vegetarian=True,
    gravy_type="dry",
    visual_features={
        "shape": "thick_triangular_or_square_sliced_cake_wedge",
        "thickness_cm": 3.0,
        "crust": "dark_golden_brown_crunchy_crust_densely_topped_with_sesame_and_mustard_seeds",
        "interior": "soft_spongy_fermented_crumb_with_grated_bottle_gourd"
    },
    key_ingredients=["fermented batter of rice, chana dal, toor dal, urad dal", "grated bottle gourd (dudhi/lauki)", "yogurt", "white sesame seeds", "mustard seeds", "green chillies", "ginger", "oil"],
    possible_ingredients=["green peas", "carrots"],
    hard_negatives=["GJ_FARSAN_DHOKLA_WHITE", "GJ_FARSAN_KHAMAN_NYLON", "MH_SNACK_KOTHIMBIR_VADI"],
    density_g_cm3=0.86,
    default_serving_weight_g=140.0,
    nutrition_per_100g={"calories": 210.0, "protein_g": 7.0, "carbs_g": 29.0, "fat_g": 7.8, "fiber_g": 4.5, "sodium_mg": 280.0},
    hierarchy=WestIndianHierarchy(
        level3_state_region="Gujarat",
        level4_cuisine="Gujarati",
        level5_food_family="Farsan",
        level6_food_type="Baked Cake",
        level7_variant="Handvo",
        level8_cooking_method=["fermented", "baked_or_pan_crisped"],
        level9_default_portion="1 slice (140g)",
        nutrition_ref_id="wi_handvo"
    )
))

register_west_food(WestIndianFoodClass(
    permanent_id="GJ_SNACK_KHICHU",
    canonical_name="Gujarati Khichu (Papdi no Lot)",
    alternate_names=["khichu", "papdi no lot", "steamed rice flour snack"],
    regional_names={"English": "Steamed Seasoned Rice Flour Dough with Raw Peanut Oil & Methi Sambhar", "Gujarati": "ખીચું"},
    vegetarian=True,
    gravy_type="dry",
    visual_features={
        "texture": "pliable_warm_dough_soft_dense_steamed",
        "color": "milky_white_to_pale_cream",
        "serving": "drenched_in_raw_aromatic_groundnut_oil_and_sprinkled_with_red_methia_masala"
    },
    key_ingredients=["rice flour (or wheat/jowar)", "papad khar (alkaline salt)", "cumin seeds", "green chilli paste", "raw groundnut oil", "methi masala (achar pickle powder)"],
    possible_ingredients=["sesame seeds"],
    hard_negatives=["TN_BREAKFAST_IDLI_PLAIN", "MH_BREAKFAST_SABUDANA_KHICHDI", "HP_MAIN_SIDDU"],
    density_g_cm3=0.96,
    default_serving_weight_g=150.0,
    nutrition_per_100g={"calories": 175.0, "protein_g": 3.5, "carbs_g": 31.0, "fat_g": 4.5, "fiber_g": 1.2, "sodium_mg": 310.0},
    hierarchy=WestIndianHierarchy(
        level3_state_region="Gujarat",
        level4_cuisine="Gujarati",
        level5_food_family="Farsan",
        level6_food_type="Steamed Dough",
        level7_variant="Khichu",
        level8_cooking_method=["boiled_stirred_steamed"],
        level9_default_portion="1 plate (150g)",
        nutrition_ref_id="wi_khichu"
    )
))

register_west_food(WestIndianFoodClass(
    permanent_id="GJ_BEVERAGE_CHAAS",
    canonical_name="Gujarati Chaas (Spiced Buttermilk)",
    alternate_names=["chaas", "gujarati chaas", "masala chaas", "buttermilk"],
    regional_names={"English": "Chilled Spiced Buttermilk with Roasted Cumin & Mint", "Gujarati": "છાસ"},
    vegetarian=True,
    gravy_type="thin_gravy",
    visual_features={
        "liquid": "thin_frothy_pale_white_refreshing_curd_drink",
        "garnishes": ["roasted_cumin_powder_dusting", "finely_chopped_fresh_mint", "coriander"]
    },
    key_ingredients=["churned curd (dahi)", "chilled water", "roasted cumin seeds (bhuna jeera)", "black salt (kala namak)", "mint", "coriander"],
    possible_ingredients=["ginger hint"],
    hard_negatives=["KN_BEVERAGE_SOL_KADHI", "WI_SWEET_SHRIKHAND", "TN_CURRY_MOR_KUZHAMBU"],
    density_g_cm3=1.01,
    default_serving_weight_g=200.0,
    nutrition_per_100g={"calories": 30.0, "protein_g": 1.8, "carbs_g": 2.5, "fat_g": 1.2, "fiber_g": 0.2, "sodium_mg": 180.0},
    hierarchy=WestIndianHierarchy(
        level3_state_region="Gujarat",
        level4_cuisine="Gujarati",
        level5_food_family="Beverages",
        level6_food_type="Buttermilk",
        level7_variant="Gujarati Chaas",
        level8_cooking_method=["churned_chilled"],
        level9_default_portion="1 tall glass (200g)",
        nutrition_ref_id="wi_chaas_gujarati"
    )
))

register_west_food(WestIndianFoodClass(
    permanent_id="MUM_STREET_DAHI_PURI",
    canonical_name="Mumbai Dahi Batata Puri",
    alternate_names=["dahi puri", "dahi batata puri", "bombay dahi puri"],
    regional_names={"English": "Crisp Puris Stuffed with Potatoes, Drowned in Chilled Sweet Curd & Chutneys", "Hindi": "दही पूरी", "Marathi": "दही पुरी"},
    vegetarian=True,
    gravy_type="creamy_gravy",
    visual_features={
        "layout": "6_inflated_round_hollow_puris_with_cracked_tops",
        "stuffing": "boiled_potato_cubes_and_black_chickpeas",
        "dominant_feature": "overflowing_with_creamy_whisked_sweetened_curd",
        "toppings": ["red_saunth_tamarind_chutney", "green_mint_chutney", "yellow_sev", "pomegranate_pearls", "chaat_masala"]
    },
    key_ingredients=["crisp hollow puris (gol gappa shells)", "boiled potatoes", "boiled brown chickpeas", "sweetened whisked curd (dahi)", "tamarind chutney", "green chutney", "nylon sev", "chaat masala"],
    possible_ingredients=["pomegranate seeds"],
    hard_negatives=["MUM_STREET_SEV_PURI", "DL_STREET_DAHI_BHALLA", "DL_STREET_GOL_GAPPA"],
    density_g_cm3=1.06,
    default_serving_weight_g=220.0,
    nutrition_per_100g={"calories": 165.0, "protein_g": 4.5, "carbs_g": 24.0, "fat_g": 6.0, "fiber_g": 2.0, "sodium_mg": 310.0},
    hierarchy=WestIndianHierarchy(
        level3_state_region="Mumbai",
        level4_cuisine="Mumbai Street Food",
        level5_food_family="Street Food",
        level6_food_type="Chaat",
        level7_variant="Dahi Puri",
        level8_cooking_method=["assembled"],
        level9_default_portion="6 pieces (220g)",
        nutrition_ref_id="wi_dahi_puri"
    )
))

register_west_food(WestIndianFoodClass(
    permanent_id="MUM_STREET_RAGDA_PATTICE",
    canonical_name="Mumbai Ragda Pattice",
    alternate_names=["ragda pattice", "ragda patties", "bombay ragda pattice"],
    regional_names={"English": "Crisp Potato Patties Submerged in White Dried Pea Ragda Stew", "Hindi": "रगड़ा पैटिस", "Marathi": "रगडा पॅटिस"},
    vegetarian=True,
    gravy_type="semi_gravy",
    visual_features={
        "patties": "2_golden_crisp_pan_fried_potato_patties_(pattice)",
        "gravy": "hot_spiced_yellow_white_pea_stew_(ragda)_ladled_generously_over_patties",
        "garnishes": ["finely_chopped_onions", "tamarind_date_chutney", "spicy_green_chutney", "sev_crunch", "coriander"]
    },
    key_ingredients=["potato patties (boiled potatoes, cornstarch, salt, pan-fried)", "ragda (dried white peas / safed vatana, turmeric, spices)", "tamarind chutney", "mint chutney", "onions", "sev"],
    possible_ingredients=["chaat masala"],
    hard_negatives=["DL_STREET_ALOO_TIKKI_CHAAT", "MUM_STREET_PAV_BHAJI", "MH_CURRY_USAL_MATKI"],
    density_g_cm3=1.04,
    default_serving_weight_g=240.0,
    nutrition_per_100g={"calories": 155.0, "protein_g": 5.8, "carbs_g": 25.0, "fat_g": 4.2, "fiber_g": 4.8, "sodium_mg": 360.0},
    hierarchy=WestIndianHierarchy(
        level3_state_region="Mumbai",
        level4_cuisine="Mumbai Street Food",
        level5_food_family="Street Food",
        level6_food_type="Chaat",
        level7_variant="Ragda Pattice",
        level8_cooking_method=["pan_fried_patties", "boiled_stew", "assembled"],
        level9_default_portion="2 pattice in ragda (240g)",
        nutrition_ref_id="wi_ragda_pattice"
    )
))

# Register canonical ID aliases
CANONICAL_ID_ALIASES = {
    "GJ_FARSAN_KHAMAN": "GJ_FARSAN_KHAMAN_NYLON",
    "MH_SNACK_BATATA_VADA": "MUM_STREET_BATATA_VADA",
    "MH_BREAD_PURAN_POLI": "MH_SWEET_PURAN_POLI",
    "GA_CURRY_FISH_XITT_CODI": "GA_CURRY_FISH_GOAN",
    "GJ_BREAD_ROTLO_BAJRA": "GJ_BREAD_ROTLA_BAJRA",
    "GJ_CURRY_UNDHIYU": "GJ_MAIN_UNDHIYU_SURTI",
    "MH_CURRY_MISAL_KAT": "MH_CURRY_MISAL_KOLHAPURI",
    "MH_SWEET_MODAK_UKADICHE": "MH_SWEET_UKADICHE_MODAK",
    "MH_SWEET_SHRIKHAND": "WI_SWEET_SHRIKHAND",
    "GJ_DAL_GUJARATI": "GJ_MAIN_DAL_DHOKLI",
    "GJ_KADHI_GUJARATI": "GJ_CURRY_KADHI",
    "GJ_RICE_KHICHDI": "GJ_SNACK_KHICHU",
    "MH_BREAD_PAV": "GA_BREAD_PAO",
    "GA_BEVERAGE_SOL_KADHI": "KN_BEVERAGE_SOL_KADHI",
    "GA_SEAFOOD_RAVA_FISH_FRY": "KN_SEAFOOD_SURMAI_FRY",
    "MH_SNACK_SABUDANA_VADA": "MH_BREAKFAST_SABUDANA_VADA",
    "GJ_BREAD_ROTLO_PHULKA": "GJ_BREAD_THEPLA_METHI"
}

for alias_id, target_id in CANONICAL_ID_ALIASES.items():
    if target_id in WEST_INDIAN_TAXONOMY_REGISTRY and alias_id not in WEST_INDIAN_TAXONOMY_REGISTRY:
        WEST_INDIAN_TAXONOMY_REGISTRY[alias_id] = WEST_INDIAN_TAXONOMY_REGISTRY[target_id]

# Additional regional multilingual synonyms
EXTRA_SYNONYMS = {
    "ખમણ ઢોકળા": "GJ_FARSAN_KHAMAN_NYLON",
    "ખમણ": "GJ_FARSAN_KHAMAN_NYLON",
    "નાયલોન ખમણ": "GJ_FARSAN_KHAMAN_NYLON",
    "વડા પાઉં": "MUM_STREET_VADA_PAV",
    "વડા પાવ": "MUM_STREET_VADA_PAV",
    "વડાપાવ": "MUM_STREET_VADA_PAV",
    "वडा पाव": "MUM_STREET_VADA_PAV",
    "पुरणपोळी": "MH_SWEET_PURAN_POLI",
    "पुरण पोळी": "MH_SWEET_PURAN_POLI",
    "પુરણ પોળી": "MH_SWEET_PURAN_POLI",
    "xitt codi": "GA_CURRY_FISH_GOAN",
    "xit kodi": "GA_CURRY_FISH_GOAN",
    "goan fish curry": "GA_CURRY_FISH_GOAN"
}
for s_name, s_id in EXTRA_SYNONYMS.items():
    WEST_INDIAN_SYNONYM_MAP[s_name.lower().strip()] = s_id

# Utility resolvers
def resolve_west_food_by_name(query: str) -> Optional[WestIndianFoodClass]:
    q = query.lower().strip()
    if q in WEST_INDIAN_SYNONYM_MAP:
        perm_id = WEST_INDIAN_SYNONYM_MAP[q]
        return WEST_INDIAN_TAXONOMY_REGISTRY.get(perm_id)
    for alias, perm_id in WEST_INDIAN_SYNONYM_MAP.items():
        if q == alias or q in alias or alias in q:
            return WEST_INDIAN_TAXONOMY_REGISTRY.get(perm_id)
    return None

def get_west_food_class(perm_id: str) -> Optional[WestIndianFoodClass]:
    return WEST_INDIAN_TAXONOMY_REGISTRY.get(perm_id)

def list_all_west_food_ids() -> List[str]:
    return list(WEST_INDIAN_TAXONOMY_REGISTRY.keys())
