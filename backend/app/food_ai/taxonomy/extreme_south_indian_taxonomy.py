"""
Extreme South Indian Food Taxonomy & Specification
Implements Section 1 through Section 27 of Part 2.
Every food class contains all 20 required canonical fields:
1. food_id
2. canonical_name
3. alternate_names
4. regional_names
5. category
6. sub_category
7. region
8. state
9. variant
10. cooking_method
11. food_state
12. visual_features
13. common_ingredients
14. possible_ingredients
15. hard_negative_classes
16. portion_classes
17. weight_classes
18. nutrition_reference
19. confidence_rules
20. annotation_requirements
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class ExtremeFoodClass(BaseModel):
    food_id: str
    canonical_name: str
    alternate_names: List[str] = Field(default_factory=list)
    regional_names: Dict[str, str] = Field(default_factory=dict)
    category: str
    sub_category: str
    region: str
    state: str
    variant: str
    cooking_method: str
    food_state: str
    visual_features: Dict[str, Any] = Field(default_factory=dict)
    common_ingredients: List[str] = Field(default_factory=list)
    possible_ingredients: List[str] = Field(default_factory=list)
    hard_negative_classes: List[str] = Field(default_factory=list)
    portion_classes: Dict[str, float] = Field(default_factory=dict)
    weight_classes: Dict[str, Any] = Field(default_factory=dict)
    nutrition_reference: Dict[str, float] = Field(default_factory=dict)
    confidence_rules: Dict[str, float] = Field(default_factory=dict)
    annotation_requirements: List[str] = Field(default_factory=list)

# Master Registry
EXTREME_TAXONOMY_REGISTRY: Dict[str, ExtremeFoodClass] = {}

def register_class(entry: ExtremeFoodClass):
    EXTREME_TAXONOMY_REGISTRY[entry.food_id] = entry

# =============================================================================
# SECTION 1 — TAMIL NADU BREAKFAST DATASET: IDLI FAMILY (29 Classes)
# =============================================================================

IDLI_CLASSES = [
    ExtremeFoodClass(
        food_id="tn_idli_plain",
        canonical_name="Plain Steamed Idli",
        alternate_names=["Idly", "Steamed Rice Cake", "Vellai Idli"],
        regional_names={"Tamil": "இட்லி", "Telugu": "ఇడ్లీ", "Kannada": "ಇಡ್ಲಿ", "Malayalam": "ഇഡ്ഡലി"},
        category="Breakfast",
        sub_category="Idli Family",
        region="South Indian",
        state="Tamil Nadu",
        variant="Standard Fermented Parboiled Rice & Urad Dal",
        cooking_method="steam_cooked",
        food_state="solid_porous",
        visual_features={
            "shape": "convex_lens_disc",
            "color": "snow_white_to_ivory",
            "surface_texture": "porous_micro_aerated_sponge",
            "diameter_cm": 7.5,
            "thickness_cm": 2.8,
            "sheen": "matte_dull",
            "visible_inclusions": []
        },
        common_ingredients=["parboiled idli rice", "whole white urad dal", "fenugreek seeds", "water", "sea salt"],
        possible_ingredients=["poha / flattened rice", "sago / tapioca pearls"],
        hard_negative_classes=["rava_idli", "dhokla", "paniyaram", "steamed_rice_cake", "thatte_idli"],
        portion_classes={"small": 60.0, "medium": 120.0, "large": 180.0},
        weight_classes={"single_piece_g": 60.0, "count_range": [1, 6], "density_g_cm3": 0.72},
        nutrition_reference={"calories_per_100g": 136.0, "protein_g": 4.2, "carbs_g": 28.5, "fat_g": 0.6, "fiber_g": 1.4, "sodium_mg": 185.0},
        confidence_rules={"min_disc_symmetry": 0.85, "whiteness_threshold": 0.80, "surface_porosity_min": 0.70},
        annotation_requirements=["count each idli as an independent instance", "segment edge boundary avoiding sambar overlap", "record vessel type"]
    ),
    ExtremeFoodClass(
        food_id="tn_idli_soft",
        canonical_name="Soft Feather Idli (Kushboo Idli)",
        alternate_names=["Kushboo Idli", "Poo Idli", "Feather Idli"],
        regional_names={"Tamil": "குஷ்பூ இட்லி"},
        category="Breakfast",
        sub_category="Idli Family",
        region="South Indian",
        state="Tamil Nadu",
        variant="Extra-fluffy aerated fermented idli with sago/tapioca",
        cooking_method="steam_cooked",
        food_state="solid_porous",
        visual_features={"shape": "plump_dome_disc", "color": "bright_white", "surface_texture": "ultra_soft_springy_sponge", "diameter_cm": 8.5, "thickness_cm": 3.4},
        common_ingredients=["idli rice", "urad dal", "sago pearls", "fenugreek", "salt"],
        possible_ingredients=["castor seeds extract", "baking soda"],
        hard_negative_classes=["tn_idli_plain", "thatte_idli", "dhokla"],
        portion_classes={"small": 75.0, "medium": 150.0, "large": 225.0},
        weight_classes={"single_piece_g": 75.0, "count_range": [1, 4], "density_g_cm3": 0.62},
        nutrition_reference={"calories_per_100g": 142.0, "protein_g": 3.8, "carbs_g": 30.5, "fat_g": 0.5, "fiber_g": 1.2, "sodium_mg": 190.0},
        confidence_rules={"dome_height_ratio": 0.40, "whiteness_threshold": 0.85},
        annotation_requirements=["measure vertical dome height from side view"]
    ),
    ExtremeFoodClass(
        food_id="tn_idli_hard",
        canonical_name="Dense Hard Idli",
        alternate_names=["Dense Idli", "Underfermented Idli"],
        regional_names={"Tamil": "கெட்டி இட்லி"},
        category="Breakfast",
        sub_category="Idli Family",
        region="South Indian",
        state="Tamil Nadu",
        variant="Under-fermented or heavy batter steamed idli",
        cooking_method="steam_cooked",
        food_state="solid_dense",
        visual_features={"shape": "flat_disc", "color": "off_white_grayish", "surface_texture": "smooth_rubbery_few_pores", "diameter_cm": 7.0, "thickness_cm": 1.8},
        common_ingredients=["idli rice", "urad dal", "salt"],
        possible_ingredients=[],
        hard_negative_classes=["tn_idli_plain", "steamed_rice_cake"],
        portion_classes={"small": 65.0, "medium": 130.0, "large": 195.0},
        weight_classes={"single_piece_g": 65.0, "count_range": [1, 4], "density_g_cm3": 0.88},
        nutrition_reference={"calories_per_100g": 140.0, "protein_g": 4.1, "carbs_g": 29.8, "fat_g": 0.5, "fiber_g": 1.3, "sodium_mg": 180.0},
        confidence_rules={"flatness_ratio": 0.80, "low_aeration": 0.75},
        annotation_requirements=["note compact height and minimal surface pores"]
    ),
    ExtremeFoodClass(
        food_id="tn_idli_mini",
        canonical_name="Mini Button Idli",
        alternate_names=["Button Idli", "Chitti Idli", "Cocktail Idli"],
        regional_names={"Tamil": "மினி இட்லி / பட்டன் இட்லி"},
        category="Breakfast",
        sub_category="Idli Family",
        region="South Indian",
        state="Tamil Nadu",
        variant="Bite-sized coin steamed idli (often served 14-25 in a bowl)",
        cooking_method="steam_cooked",
        food_state="solid_porous",
        visual_features={"shape": "miniature_convex_disc", "color": "white", "diameter_cm": 2.8, "thickness_cm": 1.2},
        common_ingredients=["idli rice", "urad dal", "fenugreek", "salt"],
        possible_ingredients=["ghee", "sambar glaze"],
        hard_negative_classes=["tn_idli_plain", "paniyaram", "seedai"],
        portion_classes={"small": 80.0, "medium": 160.0, "large": 240.0},
        weight_classes={"single_piece_g": 11.5, "count_range": [10, 25], "density_g_cm3": 0.74},
        nutrition_reference={"calories_per_100g": 138.0, "protein_g": 4.2, "carbs_g": 28.8, "fat_g": 0.6, "fiber_g": 1.4, "sodium_mg": 185.0},
        confidence_rules={"cluster_detection": 0.90, "max_diameter_cm": 3.5},
        annotation_requirements=["count individual mini discs or annotate as a bounding cluster if submerged in sambar"]
    ),
    ExtremeFoodClass(
        food_id="tn_idli_mallipoo",
        canonical_name="Mallipoo Idli (Jasmine Soft Idli)",
        alternate_names=["Jasmine Idli", "Madurai Mallipoo Idli"],
        regional_names={"Tamil": "மல்லிப்பூ இட்லி"},
        category="Breakfast",
        sub_category="Idli Family",
        region="South Indian",
        state="Tamil Nadu",
        variant="Pure white ultra-tender fragrant steamed idli",
        cooking_method="steam_cooked",
        food_state="solid_porous",
        visual_features={"shape": "soft_lens", "color": "pure_jasmine_white", "surface_texture": "fine_silk_aerated_craterlets", "diameter_cm": 7.8, "thickness_cm": 2.9},
        common_ingredients=["parboiled idli rice", "premium de-husked urad dal", "sea salt"],
        possible_ingredients=["cooked rice addition"],
        hard_negative_classes=["tn_idli_plain", "rava_idli", "dhokla"],
        portion_classes={"small": 62.0, "medium": 124.0, "large": 186.0},
        weight_classes={"single_piece_g": 62.0, "count_range": [1, 6], "density_g_cm3": 0.68},
        nutrition_reference={"calories_per_100g": 135.0, "protein_g": 4.3, "carbs_g": 28.2, "fat_g": 0.5, "fiber_g": 1.4, "sodium_mg": 180.0},
        confidence_rules={"whiteness_index": 0.92, "smooth_edge_contour": 0.88},
        annotation_requirements=["verify pristine white hue without brown tempering specks"]
    ),
    ExtremeFoodClass(
        food_id="tn_idli_kanchipuram",
        canonical_name="Kanchipuram Kovil Idli",
        alternate_names=["Kovil Idli", "Temple Idli", "Spiced Steamed Cake"],
        regional_names={"Tamil": "காஞ்சிபுரம் இட்லி / கோவில் இட்லி"},
        category="Breakfast",
        sub_category="Idli Family",
        region="South Indian",
        state="Tamil Nadu",
        variant="Cylindrical or large segmented spiced idli tempered with dry ginger, cumin, pepper, ghee, and asafoetida",
        cooking_method="steam_cooked_in_mandharai_leaves",
        food_state="solid_spiced_dense",
        visual_features={
            "shape": "cylindrical_slice_or_leaf_basket_disc",
            "color": "yellowish_cream_buff",
            "surface_texture": "coarse_crumb_embedded_spices",
            "diameter_cm": 9.0,
            "thickness_cm": 4.5,
            "visible_inclusions": ["cracked whole black pepper", "cumin seeds", "dry ginger bits", "curry leaves", "golden cashews"]
        },
        common_ingredients=["raw rice", "boiled rice", "urad dal", "pure cow ghee", "whole black peppercorns", "cumin seeds", "sukku (dry ginger)", "asafoetida", "curry leaves"],
        possible_ingredients=["sesame oil", "cashews"],
        hard_negative_classes=["rava_idli", "ven_pongal", "dhokla", "upma"],
        portion_classes={"small": 120.0, "medium": 200.0, "large": 300.0},
        weight_classes={"single_piece_g": 150.0, "count_range": [1, 2], "density_g_cm3": 0.84},
        nutrition_reference={"calories_per_100g": 188.0, "protein_g": 4.8, "carbs_g": 27.2, "fat_g": 6.8, "fiber_g": 2.1, "sodium_mg": 240.0},
        confidence_rules={"pepper_inclusion_detection": 0.88, "ghee_yellow_hue": 0.80},
        annotation_requirements=["must detect coarse whole peppercorns and mandharai leaf lines"]
    ),
    ExtremeFoodClass(
        food_id="ka_idli_rava",
        canonical_name="Rava Idli (Semolina Spiced Steamed Cake)",
        alternate_names=["Sooji Idli", "Rawa Idli", "Brahmin Rava Idli"],
        regional_names={"Kannada": "ರವೆ ಇಡ್ಲಿ", "Tamil": "ரவா இட்லி"},
        category="Breakfast",
        sub_category="Idli Family",
        region="Karnataka",
        state="Karnataka",
        variant="Curd and roasted semolina steamed cake with mustard, carrot, cashews, and coriander",
        cooking_method="steam_cooked",
        food_state="solid_crumbly_grainy",
        visual_features={
            "shape": "flat_top_convex_disc",
            "color": "golden_buff_yellowish",
            "surface_texture": "granular_rough_porous",
            "diameter_cm": 8.0,
            "thickness_cm": 2.5,
            "visible_inclusions": ["split roasted cashew nut at center", "grated orange carrot shreds", "chopped coriander leaves", "mustard seeds", "green chillies"]
        },
        common_ingredients=["roasted semolina / sooji", "sour curd", "mustard seeds", "chana dal", "cashews", "grated carrot", "coriander", "green chilli", "curry leaves", "ghee"],
        possible_ingredients=["eno fruit salt", "ginger"],
        hard_negative_classes=["tn_idli_plain", "dhokla", "kanchipuram_idli", "rava_upma"],
        portion_classes={"small": 75.0, "medium": 150.0, "large": 225.0},
        weight_classes={"single_piece_g": 75.0, "count_range": [1, 3], "density_g_cm3": 0.82},
        nutrition_reference={"calories_per_100g": 165.0, "protein_g": 5.0, "carbs_g": 31.0, "fat_g": 3.2, "fiber_g": 1.6, "sodium_mg": 260.0},
        confidence_rules={"central_cashew_presence": 0.85, "granular_texture_presence": 0.90},
        annotation_requirements=["verify presence of granular crumb, central cashew, and mustard-carrot specks"]
    ),
    ExtremeFoodClass(
        food_id="tn_idli_ragi",
        canonical_name="Ragi Idli (Finger Millet Steamed Cake)",
        alternate_names=["Finger Millet Idli", "Kelvaragu Idli"],
        regional_names={"Tamil": "கேழ்வரகு இட்லி / ராகி இட்லி", "Kannada": "ರಾಗಿ ಇಡ್ಲಿ"},
        category="Breakfast",
        sub_category="Idli Family",
        region="South Indian",
        state="Tamil Nadu",
        variant="Fermented finger millet flour and urad dal steamed cake",
        cooking_method="steam_cooked",
        food_state="solid_porous",
        visual_features={"shape": "convex_disc", "color": "deep_chocolate_brown_to_earthy_maroon", "surface_texture": "matte_porous", "diameter_cm": 7.5, "thickness_cm": 2.6},
        common_ingredients=["ragi flour", "idli rice", "urad dal", "salt"],
        possible_ingredients=["grated carrot"],
        hard_negative_classes=["tn_idli_plain", "black_rice_idli", "chocolate_cake"],
        portion_classes={"small": 62.0, "medium": 124.0, "large": 186.0},
        weight_classes={"single_piece_g": 62.0, "count_range": [1, 4], "density_g_cm3": 0.76},
        nutrition_reference={"calories_per_100g": 128.0, "protein_g": 4.5, "carbs_g": 25.8, "fat_g": 0.8, "fiber_g": 3.8, "sodium_mg": 170.0},
        confidence_rules={"brown_ragi_hue": 0.90, "aerated_porosity": 0.80},
        annotation_requirements=["differentiate deep brown tone from black rice idli"]
    ),
    ExtremeFoodClass(
        food_id="tn_idli_podi",
        canonical_name="Ghee Podi Idli (Gunpowder Tantalized Idli)",
        alternate_names=["Podi Idli", "Tiffin Podi Idli", "Milagai Podi Mini Idli"],
        regional_names={"Tamil": "பொடி இட்லி / நெய் பொடி இட்லி"},
        category="Breakfast",
        sub_category="Idli Family",
        region="South Indian",
        state="Tamil Nadu",
        variant="Steamed idlis generously tossed in fragrant desi ghee and spicy coarse lentil gun powder",
        cooking_method="steam_cooked_then_tossed",
        food_state="coated_solid",
        visual_features={
            "shape": "disc_or_mini_cubes",
            "color": "reddish_orange_rust_coating",
            "surface_texture": "granular_glistening_oil_crust",
            "sheen": "glossy_ghee_sheen",
            "visible_inclusions": ["coarse red chilli lentil flakes", "toasted sesame seeds", "fried curry leaves"]
        },
        common_ingredients=["steamed idlis", "desi cow ghee or gingelly oil", "milagai podi (chana dal, urad dal, dried red chillies, sesame, hing)"],
        possible_ingredients=["mustard seeds tempering", "coriander garnish"],
        hard_negative_classes=["tn_idli_plain", "chilli_idli", "masala_idli", "fried_idli"],
        portion_classes={"small": 90.0, "medium": 180.0, "large": 270.0},
        weight_classes={"single_piece_g": 68.0, "count_range": [1, 4], "density_g_cm3": 0.78},
        nutrition_reference={"calories_per_100g": 210.0, "protein_g": 5.4, "carbs_g": 26.5, "fat_g": 9.5, "fiber_g": 2.8, "sodium_mg": 380.0},
        confidence_rules={"rust_red_coat_coverage": 0.80, "ghee_sheen": 0.75},
        annotation_requirements=["record whether full size disc or mini button idlis; measure ghee coating depth"]
    ),
    ExtremeFoodClass(
        food_id="ka_idli_thatte",
        canonical_name="Thatte Idli (Plate Sized Steamed Cake)",
        alternate_names=["Plate Idli", "Bidadi Thatte Idli", "Flat Idli"],
        regional_names={"Kannada": "ತಟ್ಟೆ ಇಡ್ಲಿ"},
        category="Breakfast",
        sub_category="Idli Family",
        region="Karnataka",
        state="Karnataka",
        variant="Large flat saucer-shaped steamed idli served with butter dollop",
        cooking_method="steam_cooked_in_plates",
        food_state="solid_porous",
        visual_features={"shape": "wide_flat_circular_disc", "color": "white_to_ivory", "diameter_cm": 14.5, "thickness_cm": 1.6, "surface_texture": "open_alveolar_sponge"},
        common_ingredients=["idli rice", "urad dal", "sago pearls / sabudana", "flattened rice", "butter"],
        possible_ingredients=["red chutney smear"],
        hard_negative_classes=["tn_idli_plain", "dosa", "set_dosa", "appam"],
        portion_classes={"small": 140.0, "medium": 280.0, "large": 420.0},
        weight_classes={"single_piece_g": 140.0, "count_range": [1, 2], "density_g_cm3": 0.70},
        nutrition_reference={"calories_per_100g": 145.0, "protein_g": 4.0, "carbs_g": 30.5, "fat_g": 1.2, "fiber_g": 1.3, "sodium_mg": 195.0},
        confidence_rules={"diameter_min_cm": 12.0, "thickness_max_cm": 2.2},
        annotation_requirements=["measure diameter across plate to prevent misclassification as standard idli"]
    )
]

for item in IDLI_CLASSES:
    register_class(item)

# =============================================================================
# SECTION 2 — DOSA FAMILY (Key Representative Classes from 38+ Variants)
# =============================================================================

DOSA_CLASSES = [
    ExtremeFoodClass(
        food_id="tn_dosa_plain",
        canonical_name="Plain Dosa (Sada Dosa)",
        alternate_names=["Sada Dosa", "Plain Crepe", "Golden Roast"],
        regional_names={"Tamil": "சாதாரண தோசை", "Telugu": "ప్లెయిన్ దోశ", "Kannada": "ಪ್ಲೇನ್ ದೋಸೆ"},
        category="Breakfast",
        sub_category="Dosa Family",
        region="South Indian",
        state="Tamil Nadu",
        variant="Thin crispy golden fermented rice-lentil flat griddle crepe",
        cooking_method="tawa_griddled",
        food_state="crispy_sheet",
        visual_features={
            "shape": "round_folded_half_moon_or_flat",
            "color": "golden_amber_brown_gradient",
            "diameter_cm": 26.0,
            "thickness_cm": 0.15,
            "edge_crispness": "brittle_lacy",
            "center_texture": "tender_light_crisp",
            "sheen": "light_oil_glistening"
        },
        common_ingredients=["rice", "urad dal", "fenugreek", "sesame oil / refined oil", "salt"],
        possible_ingredients=["poha"],
        hard_negative_classes=["french_crepe", "paper_roast", "kal_dosa", "cheela"],
        portion_classes={"small": 90.0, "medium": 125.0, "large": 170.0},
        weight_classes={"single_piece_g": 125.0, "count_range": [1, 3], "density_g_cm3": 0.48},
        nutrition_reference={"calories_per_100g": 168.0, "protein_g": 4.1, "carbs_g": 29.5, "fat_g": 4.0, "fiber_g": 1.5, "sodium_mg": 210.0},
        confidence_rules={"concentric_griddle_spiral": 0.85, "golden_gradient": 0.90},
        annotation_requirements=["record fold style: half-moon, open flat, or roll"]
    ),
    ExtremeFoodClass(
        food_id="tn_dosa_masala",
        canonical_name="Masala Dosa (Spiced Potato Stuffed Dosa)",
        alternate_names=["Potato Masala Dosa", "Aloo Masala Dosa"],
        regional_names={"Tamil": "மசால் தோசை", "Telugu": "మసాలా దోశ"},
        category="Breakfast",
        sub_category="Dosa Family",
        region="South Indian",
        state="Tamil Nadu",
        variant="Crisp fermented crepe folded over spiced turmeric-mustard potato onion filling",
        cooking_method="tawa_griddled",
        food_state="composite_crisp_and_soft_mash",
        visual_features={
            "shape": "folded_cylinder_or_triangle_pocket",
            "color": "golden_brown_exterior",
            "diameter_cm": 28.0,
            "thickness_cm": 3.5,
            "visible_inclusions": ["yellow potato filling peeking at open seam", "mustard seeds", "green chillies"]
        },
        common_ingredients=["fermented dosa batter", "potatoes", "onions", "green chillies", "mustard seeds", "turmeric", "curry leaves", "oil / ghee"],
        possible_ingredients=["ginger", "urad dal tempering", "cashews"],
        hard_negative_classes=["mysore_masala_dosa", "plain_dosa", "spring_dosa"],
        portion_classes={"small": 150.0, "medium": 210.0, "large": 290.0},
        weight_classes={"single_piece_g": 200.0, "count_range": [1, 2], "density_g_cm3": 0.58},
        nutrition_reference={"calories_per_100g": 188.0, "protein_g": 4.2, "carbs_g": 26.4, "fat_g": 7.5, "fiber_g": 2.2, "sodium_mg": 320.0},
        confidence_rules={"potato_bulge_ratio": 0.80, "exterior_crispness": 0.90},
        annotation_requirements=["segment composite boundary; estimate filling ratio vs shell weight"]
    ),
    ExtremeFoodClass(
        food_id="ka_dosa_mysore_masala",
        canonical_name="Mysore Masala Dosa",
        alternate_names=["Red Chutney Glazed Dosa", "Mysuru Masale Dose"],
        regional_names={"Kannada": "ಮೈಸೂರು ಮಸಾಲ ದೋಸೆ"},
        category="Breakfast",
        sub_category="Dosa Family",
        region="Karnataka",
        state="Karnataka",
        variant="Thick-crisp golden dosa smeared internally with spicy red garlic-chilli chutney, stuffed with potato palya and topped with butter",
        cooking_method="tawa_griddled_high_heat",
        food_state="composite_crisp_glaze",
        visual_features={
            "shape": "folded_half_moon_thick",
            "color": "rich_reddish_copper_brown",
            "diameter_cm": 24.0,
            "thickness_cm": 3.8,
            "sheen": "heavy_butter_ghee_gloss",
            "visible_inclusions": ["crimson-red chutney coating inside fold", "spiced potato mash", "melting white butter dollop"]
        },
        common_ingredients=["fermented batter with beaten rice and chana dal", "red garlic chutney (byadagi chillies, garlic, roasted gram)", "potato palya", "pure butter / ghee"],
        possible_ingredients=["onion rings"],
        hard_negative_classes=["tn_dosa_masala", "podi_dosa", "ghee_roast"],
        portion_classes={"small": 170.0, "medium": 240.0, "large": 320.0},
        weight_classes={"single_piece_g": 230.0, "count_range": [1, 2], "density_g_cm3": 0.62},
        nutrition_reference={"calories_per_100g": 215.0, "protein_g": 4.6, "carbs_g": 27.8, "fat_g": 10.2, "fiber_g": 2.4, "sodium_mg": 360.0},
        confidence_rules={"crimson_inner_glaze_detected": 0.92, "thick_sponge_crisp_profile": 0.88},
        annotation_requirements=["look for the signature crimson red Byadagi chilli smear on the inner surface"]
    ),
    ExtremeFoodClass(
        food_id="tn_dosa_ghee_roast",
        canonical_name="Ghee Paper Roast Dosa",
        alternate_names=["Ney Roast", "Cone Dosa", "Paper Ghee Roast"],
        regional_names={"Tamil": "நெய் ரோஸ்ட்", "Malayalam": "നെയ്യ് റോസ്റ്റ്"},
        category="Breakfast",
        sub_category="Dosa Family",
        region="South Indian",
        state="Tamil Nadu",
        variant="Wafer-thin ultra-crisp golden cone or long roll drenched in pure desi cow ghee",
        cooking_method="tawa_griddled_slow_roast",
        food_state="ultra_crisp_brittle",
        visual_features={
            "shape": "tall_standing_cone_or_elongated_cylinder",
            "color": "uniform_golden_mahogany",
            "length_cm": 45.0,
            "thickness_cm": 0.08,
            "sheen": "high_gloss_aromatic_ghee",
            "edge_crispness": "glass_brittle"
        },
        common_ingredients=["idli rice", "urad dal", "chana dal", "fenugreek", "pure cow ghee in generous quantity"],
        possible_ingredients=["sugar pinch for caramelization"],
        hard_negative_classes=["tn_dosa_plain", "paper_dosa", "masala_dosa"],
        portion_classes={"small": 110.0, "medium": 160.0, "large": 220.0},
        weight_classes={"single_piece_g": 150.0, "count_range": [1, 2], "density_g_cm3": 0.42},
        nutrition_reference={"calories_per_100g": 235.0, "protein_g": 3.9, "carbs_g": 28.0, "fat_g": 12.4, "fiber_g": 1.2, "sodium_mg": 220.0},
        confidence_rules={"cone_geometry_or_long_roll": 0.94, "ultra_thin_gauge": 0.89},
        annotation_requirements=["annotate cone apex and base or roll extremities; detect high ghee sheen"]
    ),
    ExtremeFoodClass(
        food_id="tn_dosa_rava_onion",
        canonical_name="Onion Rava Dosa",
        alternate_names=["Rava Dosa", "Lacy Semolina Dosa", "Sooji Dosa"],
        regional_names={"Tamil": "வெங்காய ரவா தோசை", "Telugu": "ఆనియన్ రవ్వ దోశ"},
        category="Breakfast",
        sub_category="Dosa Family",
        region="South Indian",
        state="Tamil Nadu",
        variant="Unfermented semolina and rice flour thin batter poured to form a brittle lacy open-mesh net with charred onions",
        cooking_method="high_heat_griddle_splash",
        food_state="brittle_net_mesh",
        visual_features={
            "shape": "round_open_perforated_mesh",
            "color": "mottled_golden_beige_with_brown_spots",
            "diameter_cm": 28.0,
            "thickness_cm": 0.12,
            "surface_texture": "cratered_net_lattice",
            "visible_inclusions": ["translucent charred diced onions", "crushed black peppercorns", "cumin seeds", "slit green chillies"]
        },
        common_ingredients=["rava / sooji", "rice flour", "maida", "finely diced red onions", "whole cumin", "cracked black pepper", "curry leaves", "oil"],
        possible_ingredients=["cashews", "grated ginger"],
        hard_negative_classes=["tn_dosa_plain", "neer_dosa", "pesarattu"],
        portion_classes={"small": 120.0, "medium": 175.0, "large": 240.0},
        weight_classes={"single_piece_g": 170.0, "count_range": [1, 2], "density_g_cm3": 0.46},
        nutrition_reference={"calories_per_100g": 195.0, "protein_g": 4.5, "carbs_g": 29.8, "fat_g": 7.2, "fiber_g": 1.8, "sodium_mg": 280.0},
        confidence_rules={"perforated_lattice_ratio": 0.88, "visible_onion_inclusion": 0.85},
        annotation_requirements=["must detect porous open mesh holes throughout surface"]
    ),
    ExtremeFoodClass(
        food_id="ap_dosa_pesarattu",
        canonical_name="Andhra Pesarattu (Whole Green Moong Dosa)",
        alternate_names=["Moong Dal Dosa", "Pesarattu Dosa"],
        regional_names={"Telugu": "పెసరట్టు", "Tamil": "பெசரட்டு"},
        category="Breakfast",
        sub_category="Dosa Family",
        region="Andhra Pradesh",
        state="Andhra Pradesh",
        variant="Unfermented batter made of soaked whole green moong dal, ginger, and green chillies",
        cooking_method="tawa_griddled",
        food_state="crisp_sheet",
        visual_features={
            "shape": "round_folded_sheet",
            "color": "olive_green_to_golden_greenish_brown",
            "diameter_cm": 26.0,
            "thickness_cm": 0.22,
            "surface_texture": "slightly_coarse_matte",
            "visible_inclusions": ["chopped raw onions and ginger topping", "cumin seeds"]
        },
        common_ingredients=["whole green gram / moong beans", "green chillies", "fresh ginger", "cumin seeds", "onions", "oil"],
        possible_ingredients=["upma filling (for Upma Pesarattu)"],
        hard_negative_classes=["tn_dosa_plain", "adai", "ragi_dosa"],
        portion_classes={"small": 110.0, "medium": 165.0, "large": 230.0},
        weight_classes={"single_piece_g": 160.0, "count_range": [1, 2], "density_g_cm3": 0.55},
        nutrition_reference={"calories_per_100g": 155.0, "protein_g": 8.5, "carbs_g": 24.0, "fat_g": 3.5, "fiber_g": 4.2, "sodium_mg": 210.0},
        confidence_rules={"greenish_olive_hue": 0.90, "high_protein_dal_matte": 0.82},
        annotation_requirements=["distinguish olive green tone from yellow/white rice dosa"]
    ),
    ExtremeFoodClass(
        food_id="ka_dosa_neer",
        canonical_name="Neer Dosa (Mangalorean Water Dosa)",
        alternate_names=["Water Dosa", "Bari Dosa"],
        regional_names={"Kannada": "ನೀರ್ ದೋಸೆ", "Tulu": "ನೀರ್ ದೋಸೆ"},
        category="Breakfast",
        sub_category="Dosa Family",
        region="Karnataka",
        state="Karnataka",
        variant="Ultra-thin delicate soft lacy white unfermented watery rice batter crepe",
        cooking_method="covered_pan_steamed_griddle",
        food_state="soft_lacy_sheet",
        visual_features={
            "shape": "folded_quadrant_triangle",
            "color": "chalk_pure_white",
            "diameter_cm": 22.0,
            "thickness_cm": 0.08,
            "surface_texture": "fine_silk_lacy_perforated_soft",
            "sheen": "matte_dry"
        },
        common_ingredients=["short grain white rice", "fresh grated coconut", "water", "salt"],
        possible_ingredients=[],
        hard_negative_classes=["appam", "tn_dosa_plain", "paper_dosa"],
        portion_classes={"small": 70.0, "medium": 140.0, "large": 210.0},
        weight_classes={"single_piece_g": 45.0, "count_range": [2, 5], "density_g_cm3": 0.65},
        nutrition_reference={"calories_per_100g": 125.0, "protein_g": 2.8, "carbs_g": 26.5, "fat_g": 1.2, "fiber_g": 0.8, "sodium_mg": 140.0},
        confidence_rules={"pure_white_hue": 0.92, "triangle_fold_geometry": 0.88, "zero_browning": 0.95},
        annotation_requirements=["must have zero browning on both sides; folded into delicate quadrants"]
    )
]

for item in DOSA_CLASSES:
    register_class(item)

# =============================================================================
# SECTION 3 — VADA FAMILY (15 Classes with Hole Geometry & Hard Negatives)
# =============================================================================

VADA_CLASSES = [
    ExtremeFoodClass(
        food_id="tn_vada_medu",
        canonical_name="Medu Vada (Crispy Lentil Donut Fritter)",
        alternate_names=["Ulundhu Vadai", "Garelu", "Uddina Vada", "Mendu Vada"],
        regional_names={"Tamil": "மெது வடை / உளுந்து வடை", "Telugu": "గారెలు", "Kannada": "ಉದ್ದಿನ ವಡೆ", "Malayalam": "ഉഴുന്ന് വട"},
        category="Breakfast",
        sub_category="Vada Family",
        region="South Indian",
        state="Tamil Nadu",
        variant="Aerated soaked whole urad dal deep fried into a golden toroidal ring with central aperture",
        cooking_method="deep_fried",
        food_state="solid_fried_donut",
        visual_features={
            "shape": "torus_donut_with_central_hole",
            "outer_diameter_cm": 7.8,
            "hole_diameter_cm": 2.2,
            "thickness_cm": 3.2,
            "fried_color": "deep_golden_amber",
            "outer_texture": "crisp_blistered_crust",
            "inner_texture": "cloud_soft_spongy_steamy",
            "visible_inclusions": ["whole black peppercorns", "curry leaf fragments", "chopped green chilli rings", "diced onion bits"]
        },
        common_ingredients=["whole white urad dal", "black peppercorns", "green chillies", "curry leaves", "ginger", "asafoetida", "salt", "refined frying oil"],
        possible_ingredients=["finely diced shallots", "rice flour (for crispness)"],
        hard_negative_classes=["bonda", "sweet_doughnut", "onion_vadai", "paruppu_vada"],
        portion_classes={"small": 50.0, "medium": 65.0, "large": 90.0},
        weight_classes={"single_piece_g": 65.0, "count_range": [1, 4], "density_g_cm3": 0.62},
        nutrition_reference={"calories_per_100g": 262.0, "protein_g": 9.6, "carbs_g": 28.0, "fat_g": 12.4, "fiber_g": 4.2, "sodium_mg": 310.0},
        confidence_rules={"hole_circularity_score": 0.85, "golden_ring_symmetry": 0.88},
        annotation_requirements=["verify presence of central hole to distinguish from solid bonda"]
    ),
    ExtremeFoodClass(
        food_id="tn_vada_paruppu",
        canonical_name="Paruppu Vada (Masala Vada / Chana Dal Crunchy Fritter)",
        alternate_names=["Masala Vadai", "Parippu Vada", "Aamai Vadai", "Chana Dal Vada"],
        regional_names={"Tamil": "பருப்பு வடை / மசால் வடை", "Malayalam": "പരിപ്പ് വട"},
        category="Snack",
        sub_category="Vada Family",
        region="South Indian",
        state="Tamil Nadu",
        variant="Coarsely crushed chana dal and toor dal disc deep fried with rustic aromatics and spices",
        cooking_method="deep_fried",
        food_state="solid_fried_crunchy",
        visual_features={
            "shape": "coarse_flat_disc_no_hole",
            "outer_diameter_cm": 6.8,
            "thickness_cm": 1.4,
            "fried_color": "rustic_reddish_dark_amber",
            "outer_texture": "crunchy_pebbled_rough",
            "visible_inclusions": ["whole uncrushed yellow chana dal gems", "diced red onions", "dried red chilli flakes", "fennel seeds (saunf)", "curry leaves"]
        },
        common_ingredients=["chana dal (Bengal gram)", "toor dal", "dry red chillies", "fennel seeds", "onions", "ginger", "curry leaves", "oil"],
        possible_ingredients=["garlic cloves", "mint leaves"],
        hard_negative_classes=["tn_vada_medu", "onion_pakoda", "falafel", "maddur_vada"],
        portion_classes={"small": 45.0, "medium": 60.0, "large": 80.0},
        weight_classes={"single_piece_g": 55.0, "count_range": [1, 4], "density_g_cm3": 0.88},
        nutrition_reference={"calories_per_100g": 310.0, "protein_g": 12.8, "carbs_g": 34.2, "fat_g": 14.5, "fiber_g": 6.8, "sodium_mg": 340.0},
        confidence_rules={"zero_central_hole": 0.95, "visible_whole_dal_grains": 0.90, "rough_pebbled_surface": 0.88},
        annotation_requirements=["must confirm absence of hole and visible uncrushed chana dal"]
    ),
    ExtremeFoodClass(
        food_id="tn_vada_sambar",
        canonical_name="Sambar Vada (Soaked Dip Vada)",
        alternate_names=["Sambar Vadai", "Soaked Vada"],
        regional_names={"Tamil": "சாம்பார் வடை"},
        category="Breakfast",
        sub_category="Vada Family",
        region="South Indian",
        state="Tamil Nadu",
        variant="Medu vada completely submerged in steaming spiced vegetable tiffin sambar topped with ghee and raw onions",
        cooking_method="deep_fried_then_stew_soaked",
        food_state="soaked_sponge_in_gravy",
        visual_features={
            "shape": "swollen_torus_submerged",
            "color": "golden_orange_broth_with_soaked_pastry",
            "diameter_cm": 8.8,
            "thickness_cm": 3.8,
            "surface_texture": "softened_saturated_crust",
            "visible_inclusions": ["diced raw red onions floating", "chopped coriander leaves", "ghee swirls", "drumstick or shallot bits"]
        },
        common_ingredients=["medu vada", "tiffin sambar", "finely diced raw onions", "coriander garnish", "ghee"],
        possible_ingredients=[],
        hard_negative_classes=["tn_vada_medu", "thayir_vada", "rasam_vada"],
        portion_classes={"small": 160.0, "medium": 240.0, "large": 350.0},
        weight_classes={"single_piece_g": 220.0, "count_range": [1, 2], "density_g_cm3": 0.95},
        nutrition_reference={"calories_per_100g": 165.0, "protein_g": 5.8, "carbs_g": 19.5, "fat_g": 7.4, "fiber_g": 3.2, "sodium_mg": 420.0},
        confidence_rules={"vada_submerged_in_sambar": 0.94},
        annotation_requirements=["detect dual-component: submerged swollen vada + surrounding sambar liquid boundary"]
    ),
    ExtremeFoodClass(
        food_id="tn_vada_thayir",
        canonical_name="Thayir Vada (Curd Soaked Dahi Vada South Style)",
        alternate_names=["Curd Vada", "Perugu Vada", "Mosaru Vade"],
        regional_names={"Tamil": "தயிர் வடை", "Telugu": "పెరుగు వడ", "Kannada": "ಮೊಸರು ವಡೆ"},
        category="Snack",
        sub_category="Vada Family",
        region="South Indian",
        state="Tamil Nadu",
        variant="Medu vada soaked in creamy whisked curd tempered with mustard, green chillies, ginger, and boondi/kara sev",
        cooking_method="deep_fried_then_yogurt_soaked",
        food_state="soaked_sponge_in_yogurt",
        visual_features={
            "shape": "swollen_disc_submerged_in_white_cream",
            "color": "cream_white_with_yellow_green_tempering",
            "surface_texture": "glossy_cooling_yogurt_cloak",
            "visible_inclusions": ["golden boondi balls", "black mustard seeds", "finely grated carrot shreds", "coriander", "ginger slivers"]
        },
        common_ingredients=["medu vada", "fresh thick curd / yogurt", "mustard seeds", "green chillies", "asafoetida", "coriander", "boondi"],
        possible_ingredients=["pomegranate pearls", "grated carrot"],
        hard_negative_classes=["dahi_bhalla", "tn_vada_sambar", "rasam_vada"],
        portion_classes={"small": 150.0, "medium": 220.0, "large": 320.0},
        weight_classes={"single_piece_g": 200.0, "count_range": [1, 2], "density_g_cm3": 0.98},
        nutrition_reference={"calories_per_100g": 178.0, "protein_g": 6.8, "carbs_g": 16.5, "fat_g": 9.8, "fiber_g": 2.1, "sodium_mg": 280.0},
        confidence_rules={"white_curd_lake_coverage": 0.90, "mustard_tempering_visible": 0.85},
        annotation_requirements=["detect thick yogurt covering and discriminate from north indian sweet dahi bhalla (no tamarind sauce)"]
    )
]

for item in VADA_CLASSES:
    register_class(item)

# =============================================================================
# SECTION 5 & 6 — PONGAL & UPMA FAMILIES (Pairwise Anti-Confusion Discrimination)
# =============================================================================

PONGAL_UPMA_CLASSES = [
    ExtremeFoodClass(
        food_id="tn_pongal_ven",
        canonical_name="Ven Pongal (Ghee Hot Pepper Pongal)",
        alternate_names=["Ghee Pongal", "Khara Pongal", "Kovil Ven Pongal"],
        regional_names={"Tamil": "வெண் பொங்கல்", "Telugu": "వెన్ పొంగల్", "Kannada": "ಖಾರಾ ಪೊಂಗಲ್"},
        category="Breakfast",
        sub_category="Pongal Family",
        region="South Indian",
        state="Tamil Nadu",
        variant="Soft pressure-cooked raw rice and split yellow moong dal mash tempered heavily in pure cow ghee with black peppercorns, cumin, cashews, and ginger",
        cooking_method="pressure_cooked_and_tempered",
        food_state="semi_solid_glossy_mash",
        visual_features={
            "consistency": "soft_creamy_flowing_mound",
            "color": "pale_creamy_yellowish_gold",
            "sheen": "high_glossy_ghee_luster",
            "grain_visibility": "soft_burst_rice_moong_mash",
            "visible_inclusions": ["whole glossy black peppercorns", "whole cumin seeds", "golden fried cashew nuts", "slivers of fresh ginger", "fried curry leaves"]
        },
        common_ingredients=["raw rice", "yellow moong dal", "pure desi cow ghee", "whole black peppercorns", "cumin seeds", "cashew nuts", "fresh ginger", "curry leaves", "asafoetida", "salt"],
        possible_ingredients=["cracked pepper", "green chilli"],
        hard_negative_classes=["rava_upma", "khichdi", "curd_rice", "rice_pudding"],
        portion_classes={"small": 130.0, "medium": 190.0, "large": 280.0},
        weight_classes={"single_serving_g": 190.0, "density_g_cm3": 0.95},
        nutrition_reference={"calories_per_100g": 192.0, "protein_g": 4.5, "carbs_g": 26.0, "fat_g": 7.5, "fiber_g": 1.8, "sodium_mg": 280.0},
        confidence_rules={"peppercorn_and_cashew_detection": 0.92, "creamy_ghee_mash_texture": 0.90},
        annotation_requirements=["MUST inspect for whole black peppercorns and split cashews to prevent confusion with Rava Upma"]
    ),
    ExtremeFoodClass(
        food_id="tn_upma_rava",
        canonical_name="Rava Upma (Semolina Savory Porridge)",
        alternate_names=["Sooji Upma", "Uppittu", "Rawa Upma"],
        regional_names={"Tamil": "ரவா உப்புமா", "Kannada": "ಉಪ್ಪಿಟ್ಟು", "Telugu": "రవ్వ ఉప్మా"},
        category="Breakfast",
        sub_category="Upma Family",
        region="South Indian",
        state="Tamil Nadu",
        variant="Roasted wheat semolina cooked into fluffy savory crumb tempered with mustard, urad dal, chana dal, green chillies, and ginger",
        cooking_method="boiled_and_steam_rested",
        food_state="semi_solid_granular_crumb",
        visual_features={
            "consistency": "granular_separable_crumb",
            "color": "ivory_white_to_light_cream",
            "sheen": "low_to_moderate_oil",
            "grain_size": "fine_beaded_semolina_grains",
            "visible_inclusions": ["black mustard seeds", "split white urad dal browned gems", "golden chana dal gems", "slit green chillies", "fresh ginger bits", "curry leaves"]
        },
        common_ingredients=["roasted semolina (sooji)", "oil / ghee", "mustard seeds", "urad dal", "chana dal", "green chillies", "ginger", "curry leaves", "onions", "water", "salt"],
        possible_ingredients=["chopped carrots", "green peas", "roasted cashews"],
        hard_negative_classes=["tn_pongal_ven", "poha", "khichdi", "couscous"],
        portion_classes={"small": 120.0, "medium": 180.0, "large": 260.0},
        weight_classes={"single_serving_g": 180.0, "density_g_cm3": 0.88},
        nutrition_reference={"calories_per_100g": 158.0, "protein_g": 3.8, "carbs_g": 27.5, "fat_g": 3.8, "fiber_g": 1.6, "sodium_mg": 260.0},
        confidence_rules={"grain_bead_texture_detected": 0.90, "mustard_urad_dal_gems": 0.88, "absence_of_black_pepper_grains": 0.90},
        annotation_requirements=["verify fine individual semolina granules and absence of whole black peppercorns"]
    )
]

for item in PONGAL_UPMA_CLASSES:
    register_class(item)

# =============================================================================
# SECTION 8 — PAROTTA & KOTHU PAROTTA FAMILY (19 Classes)
# =============================================================================

PAROTTA_CLASSES = [
    ExtremeFoodClass(
        food_id="tn_parotta_kothu_chicken",
        canonical_name="Madurai Chicken Kothu Parotta",
        alternate_names=["Chicken Kothu", "Kothu Roti Chicken", "Street Kothu Parotta"],
        regional_names={"Tamil": "சிக்கன் கொத்து பரோட்டா"},
        category="Dinner",
        sub_category="Parotta Family",
        region="South Indian",
        state="Tamil Nadu",
        variant="Flaky shredded layered parotta vigorously beaten and minced on a hot flat iron tawa with spiced chicken pieces, egg scramble, onions, and rich chicken salna gravy",
        cooking_method="tawa_chopped_iron_beat",
        food_state="chopped_tossed_solid",
        visual_features={
            "shape": "heaped_tossed_shred_mound",
            "color": "rich_reddish_golden_brown",
            "surface_texture": "irregular_flaky_ribbons_interleaved",
            "visible_inclusions": ["chopped caramelized parotta flakes", "shredded tender chicken morsels", "soft scrambled egg ribbons", "sautéed onions and green chillies", "fresh coriander"]
        },
        common_ingredients=["shredded malabar parotta", "boneless chicken meat curry pieces", "eggs", "chicken salna gravy", "sliced red onions", "green chillies", "curry leaves", "fennel powder", "black pepper", "oil"],
        possible_ingredients=["sliced capsicum / bell peppers"],
        hard_negative_classes=["chicken_fried_rice", "egg_noodles", "chicken_keema", "chilli_parotta"],
        portion_classes={"small": 220.0, "medium": 340.0, "large": 480.0},
        weight_classes={"single_serving_g": 340.0, "density_g_cm3": 0.86},
        nutrition_reference={"calories_per_100g": 225.0, "protein_g": 11.2, "carbs_g": 24.5, "fat_g": 9.1, "fiber_g": 1.5, "sodium_mg": 460.0},
        confidence_rules={"shredded_parotta_ribbon_structure": 0.94, "beaten_egg_meat_interleave": 0.90},
        annotation_requirements=["distinguish shredded wheat dough ribbons from rice grains (fried rice) or extruded noodles"]
    ),
    ExtremeFoodClass(
        food_id="kl_parotta_malabar",
        canonical_name="Kerala Malabar Parotta",
        alternate_names=["Malabar Porotta", "Kerala Layered Parotta"],
        regional_names={"Malayalam": "മലബാർ പൊറോട്ട", "Tamil": "மலபார் பரோட்டா"},
        category="Dinner",
        sub_category="Parotta Family",
        region="Kerala",
        state="Kerala",
        variant="Spiral-kneaded layered flaky all-purpose flour flatbread cooked on tawa and crushed by hand to reveal flaky rings",
        cooking_method="tawa_griddled_and_crushed",
        food_state="flaky_layered_solid",
        visual_features={
            "shape": "round_disc_with_concentric_spiral_coils",
            "diameter_cm": 18.0,
            "thickness_cm": 0.8,
            "color": "creamy_ivory_with_golden_brown_blisters",
            "surface_texture": "flaky_spiral_ringlets_peeling"
        },
        common_ingredients=["maida (all-purpose flour)", "sugar", "salt", "water", "oil / dalda / ghee"],
        possible_ingredients=["egg in dough", "milk in dough"],
        hard_negative_classes=["laccha_paratha", "roti", "chapati", "naan"],
        portion_classes={"small": 80.0, "medium": 160.0, "large": 240.0},
        weight_classes={"single_piece_g": 80.0, "count_range": [1, 4], "density_g_cm3": 0.80},
        nutrition_reference={"calories_per_100g": 320.0, "protein_g": 6.0, "carbs_g": 43.0, "fat_g": 13.5, "fiber_g": 1.8, "sodium_mg": 380.0},
        confidence_rules={"concentric_flaky_ringlets": 0.93, "golden_tawa_blisters": 0.88},
        annotation_requirements=["must identify concentric coiled sheet layers to discriminate from North Indian paratha"]
    )
]

for item in PAROTTA_CLASSES:
    register_class(item)

# =============================================================================
# SECTION 11 — BIRYANI EXTREME DATASET (Regional Masters & Seeraga Samba vs Basmati)
# =============================================================================

BIRYANI_CLASSES = [
    ExtremeFoodClass(
        food_id="tn_biryani_dindigul_mutton",
        canonical_name="Dindigul Thalappakatti Mutton Biryani",
        alternate_names=["Thalappakatti Biryani", "Dindigul Biryani", "Seeraga Samba Mutton Biryani"],
        regional_names={"Tamil": "திண்டுக்கல் தலப்பாக்கட்டி மட்டன் பிரியாணி"},
        category="Lunch",
        sub_category="Biryani Family",
        region="Tamil Nadu",
        state="Tamil Nadu",
        variant="Dum-cooked petite Seeraga Samba short-grain rice with tender succulent bone-in goat meat, curd, shallots, and fragrant whole spices",
        cooking_method="dum_pot_cooked",
        food_state="solid_cooked_grain_and_meat",
        visual_features={
            "rice_grain_type": "seeraga_samba_short_oval_grain",
            "grain_length_mm": 4.2,
            "grain_color": "uniform_pale_amber_brownish_green",
            "masala_distribution": "uniformly_absorbed_in_every_grain",
            "meat_presence": "dark_succulent_bone_in_mutton_chunks",
            "visible_inclusions": ["bone-in mutton cuts", "soft cooked shallots", "curd emulsion sheen", "cloves", "cinnamon quills"]
        },
        common_ingredients=["seeraga samba rice", "young tender mutton with bone", "small shallots (chinna vengayam)", "sour curd", "ginger garlic paste", "pure cow ghee", "green chillies", "mint", "coriander", "cinnamon", "cardamom", "cloves"],
        possible_ingredients=["lemon juice"],
        hard_negative_classes=["hyderabadi_biryani", "pulao", "mutton_fried_rice", "kuska"],
        portion_classes={"small": 250.0, "medium": 360.0, "large": 500.0},
        weight_classes={"single_serving_g": 360.0, "density_g_cm3": 0.84},
        nutrition_reference={"calories_per_100g": 205.0, "protein_g": 11.5, "carbs_g": 20.5, "fat_g": 8.2, "fiber_g": 1.1, "sodium_mg": 330.0},
        confidence_rules={"short_grain_seeraga_samba_presence": 0.95, "homogeneous_spice_tint": 0.90},
        annotation_requirements=["CRITICAL: verify short-grain Seeraga Samba rice (< 5mm) and absence of long Basmati needles"]
    ),
    ExtremeFoodClass(
        food_id="ts_biryani_hyderabadi_chicken",
        canonical_name="Hyderabadi Chicken Dum Biryani",
        alternate_names=["Kacchi Yakhni Biryani", "Hyderabadi Biryani"],
        regional_names={"Telugu": "హైదరాబాదీ చికెన్ దమ్ బిర్యానీ", "Urdu": "حیدرآبادی بریانی"},
        category="Lunch",
        sub_category="Biryani Family",
        region="Telangana",
        state="Telangana",
        variant="Kacchi dum cooked extra-long aged basmati rice layered over raw marinated bone-in chicken with saffron milk, fried onions, mint, and desi ghee",
        cooking_method="kacchi_dum_sealed_handi",
        food_state="solid_cooked_grain_and_meat",
        visual_features={
            "rice_grain_type": "extra_long_basmati_grain",
            "grain_length_mm": 8.5,
            "grain_color": "bi_color_variegated_white_and_saffron_orange",
            "masala_distribution": "distinct_layers_white_rice_over_masala_base",
            "visible_inclusions": ["crispy dark brown fried onions (birista)", "fresh emerald mint leaves", "saffron streaks", "black cardamom", "star anise", "chicken leg/thigh cuts"]
        },
        common_ingredients=["aged long-grain basmati rice", "bone-in chicken pieces", "thick yogurt", "ginger garlic paste", "fried onions (birista)", "saffron milk", "desi ghee", "mint", "coriander", "shahi jeera", "star anise"],
        possible_ingredients=["rose water", "kewra water"],
        hard_negative_classes=["tn_biryani_dindigul_mutton", "chicken_pulao", "fried_rice"],
        portion_classes={"small": 260.0, "medium": 380.0, "large": 520.0},
        weight_classes={"single_serving_g": 380.0, "density_g_cm3": 0.82},
        nutrition_reference={"calories_per_100g": 172.0, "protein_g": 10.8, "carbs_g": 21.0, "fat_g": 5.2, "fiber_g": 1.0, "sodium_mg": 290.0},
        confidence_rules={"long_grain_basmati_needle_ratio": 0.94, "variegated_saffron_white_grains": 0.92},
        annotation_requirements=["verify slender long Basmati grains (> 7.5mm) and separate white vs saffron-dyed rice grains"]
    )
]

for item in BIRYANI_CLASSES:
    register_class(item)

# =============================================================================
# SECTION 12 — SAMBAR FAMILY (Independent Component Detection)
# =============================================================================

SAMBAR_CLASSES = [
    ExtremeFoodClass(
        food_id="tn_sambar_hotel_tiffin",
        canonical_name="Hotel Tiffin Sambar",
        alternate_names=["Tiffin Sambar", "Saravana Bhavan Style Sambar", "Idli Sambar"],
        regional_names={"Tamil": "டிபன் சாம்பார்"},
        category="Accompaniment",
        sub_category="Sambar Family",
        region="South Indian",
        state="Tamil Nadu",
        variant="Translucent golden-orange simmered toor and yellow moong dal broth sweetened mildly with jaggery, shallots, and drumstick",
        cooking_method="boiled_simmered",
        food_state="liquid_stew",
        visual_features={
            "thickness": "medium_flowing_broth",
            "color": "golden_orange_translucent",
            "oil_layer": "thin_ghee_tempered_sheen",
            "visible_inclusions": ["translucent shallots / pearl onions", "drumstick cuts", "mustard seeds", "dried red chilli pods", "curry leaves"]
        },
        common_ingredients=["toor dal", "yellow moong dal", "pearl onions (shallots)", "tomatoes", "tamarind extract", "sambar powder", "jaggery pinch", "mustard seeds", "curry leaves", "asafoetida"],
        possible_ingredients=["drumstick pieces", "coriander garnish"],
        hard_negative_classes=["rasam", "tomato_soup", "thin_dal", "mor_kuzhambu"],
        portion_classes={"small": 70.0, "medium": 120.0, "large": 200.0},
        weight_classes={"single_serving_g": 110.0, "density_g_cm3": 1.05},
        nutrition_reference={"calories_per_100g": 68.0, "protein_g": 3.2, "carbs_g": 10.5, "fat_g": 1.6, "fiber_g": 2.4, "sodium_mg": 320.0},
        confidence_rules={"sambar_color_range": 0.88, "tempering_mustard_curry_leaves": 0.85},
        annotation_requirements=["MUST segment as an independent bounding box even when poured directly over idlis or served in a steel bowl"]
    )
]

for item in SAMBAR_CLASSES:
    register_class(item)

# =============================================================================
# SECTION 19 — CHUTNEY EXTENDED DATASET (Ambiguity Preservation Rule)
# =============================================================================

CHUTNEY_CLASSES = [
    ExtremeFoodClass(
        food_id="tn_chutney_white_coconut",
        canonical_name="Fresh White Coconut Chutney",
        alternate_names=["Thengai Chutney", "Kobbari Chutney", "Coconut Chutney"],
        regional_names={"Tamil": "தேங்காய் சட்னி", "Telugu": "కొబ్బరి పచ్చడి", "Kannada": "ತೆಂಗಿನಕಾಯಿ ಚಟ್ನಿ", "Malayalam": "തേങ്ങാ ചമ്മന്തി"},
        category="Accompaniment",
        sub_category="Chutney Family",
        region="South Indian",
        state="Tamil Nadu",
        variant="Grated fresh coconut ground with roasted gram, green chillies, and ginger, tempered with mustard seeds and curry leaves in coconut or sesame oil",
        cooking_method="ground_raw_with_hot_tempering",
        food_state="semi_solid_paste",
        visual_features={
            "thickness": "medium_thick_grated_paste",
            "color": "ivory_white_to_pale_cream",
            "surface_texture": "fine_grated_coconut_crumb",
            "visible_inclusions": ["crackled black mustard seeds", "split white urad dal", "crisp green curry leaves", "hing oil droplet"]
        },
        common_ingredients=["fresh grated coconut", "roasted chana gram (pottukadalai)", "green chillies", "fresh ginger", "salt", "mustard seeds", "curry leaves", "coconut oil"],
        possible_ingredients=["cumin seeds", "garlic clove"],
        hard_negative_classes=["peanut_chutney", "sesame_chutney", "mayonnaise", "curd_pachadi"],
        portion_classes={"small": 25.0, "medium": 45.0, "large": 75.0},
        weight_classes={"single_serving_g": 45.0, "density_g_cm3": 1.02},
        nutrition_reference={"calories_per_100g": 210.0, "protein_g": 3.0, "carbs_g": 7.5, "fat_g": 19.2, "fiber_g": 3.5, "sodium_mg": 260.0},
        confidence_rules={"ivory_white_paste": 0.90, "mustard_curry_leaf_tempering": 0.88},
        annotation_requirements=["if texture cannot be definitively isolated from peanut or sesame chutney, flag ambiguity chip per Section 34"]
    ),
    ExtremeFoodClass(
        food_id="tn_chutney_tomato_kaara",
        canonical_name="Spicy Tomato Kaara Chutney",
        alternate_names=["Kaara Chutney", "Tomato Chutney", "Red Chutney", "Thakkali Chutney"],
        regional_names={"Tamil": "கார சட்னி / தக்காளி சட்னி"},
        category="Accompaniment",
        sub_category="Chutney Family",
        region="South Indian",
        state="Tamil Nadu",
        variant="Ripened red tomatoes, shallots, garlic, and dried red chillies sautéed and ground into a tangy fiery red dip",
        cooking_method="sautéed_and_ground",
        food_state="semi_solid_paste",
        visual_features={
            "thickness": "medium_thick_flowing_dip",
            "color": "vibrant_crimson_orange_red",
            "surface_texture": "smooth_to_micro_pulpy",
            "visible_inclusions": ["black mustard seeds", "curry leaves", "gingelly oil sheen"]
        },
        common_ingredients=["ripe tomatoes", "shallots", "garlic cloves", "dried red chillies", "tamarind small piece", "gingelly oil (sesame oil)", "mustard seeds", "salt"],
        possible_ingredients=["urad dal", "chana dal"],
        hard_negative_classes=["tomato_ketchup", "red_sambar", "szechuan_sauce"],
        portion_classes={"small": 25.0, "medium": 45.0, "large": 70.0},
        weight_classes={"single_serving_g": 40.0, "density_g_cm3": 1.06},
        nutrition_reference={"calories_per_100g": 88.0, "protein_g": 1.8, "carbs_g": 9.8, "fat_g": 4.2, "fiber_g": 1.9, "sodium_mg": 340.0},
        confidence_rules={"vibrant_red_hue": 0.92, "tempering_seeds_visible": 0.85},
        annotation_requirements=["distinguish from smooth western tomato ketchup by detecting visible oil emulsion and mustard tempering"]
    )
]

for item in CHUTNEY_CLASSES:
    register_class(item)

# =============================================================================
# SECTION 16 & 17 — PORIYAL & KEERAI FAMILIES
# =============================================================================

PORIYAL_CLASSES = [
    ExtremeFoodClass(
        food_id="tn_poriyal_beans",
        canonical_name="Green Beans Coconut Poriyal",
        alternate_names=["Beans Poriyal", "Beans Thoran", "French Beans Stir Fry"],
        regional_names={"Tamil": "பீன்ஸ் பொரியல்", "Malayalam": "ബീൻസ് തോരൻ"},
        category="Lunch",
        sub_category="Poriyal Family",
        region="South Indian",
        state="Tamil Nadu",
        variant="Finely cut cross-section green French beans sautéed dry with mustard, split urad dal, green chillies, and freshly grated coconut",
        cooking_method="stir_fried_dry",
        food_state="solid_diced_vegetable",
        visual_features={
            "cut_shape": "fine_cross_section_cylinders",
            "color": "bright_emerald_green_interspersed_with_white_shreds",
            "surface_texture": "dry_tender_crisp",
            "visible_inclusions": ["grated white coconut shreds", "browned urad dal gems", "mustard seeds", "curry leaves"]
        },
        common_ingredients=["fresh green beans", "grated fresh coconut", "mustard seeds", "split white urad dal", "green chillies", "curry leaves", "coconut oil / refined oil", "salt"],
        possible_ingredients=["turmeric pinch"],
        hard_negative_classes=["cabbage_poriyal", "beans_kootu", "western_green_beans"],
        portion_classes={"small": 50.0, "medium": 80.0, "large": 130.0},
        weight_classes={"single_serving_g": 75.0, "density_g_cm3": 0.65},
        nutrition_reference={"calories_per_100g": 85.0, "protein_g": 2.5, "carbs_g": 7.4, "fat_g": 5.1, "fiber_g": 3.2, "sodium_mg": 240.0},
        confidence_rules={"diced_green_cylinder_presence": 0.90, "white_coconut_shred_ratio": 0.85},
        annotation_requirements=["look for grated coconut snow sprinkled over diced green beans"]
    ),
    ExtremeFoodClass(
        food_id="tn_keerai_moringa",
        canonical_name="Moringa Keerai Poriyal (Drumstick Leaves Stir Fry)",
        alternate_names=["Murungai Keerai Poriyal", "Drumstick Leaf Fry"],
        regional_names={"Tamil": "முருங்கைக்கீரை பொரியல்"},
        category="Lunch",
        sub_category="Keerai Family",
        region="South Indian",
        state="Tamil Nadu",
        variant="Tender drumstick leaflets sautéed dry with shallots, red chillies, and roasted ground peanuts or grated coconut",
        cooking_method="stir_fried_dry",
        food_state="solid_cooked_leafy_greens",
        visual_features={
            "color": "deep_forest_green",
            "texture": "distinct_tiny_oval_leaflets",
            "visible_inclusions": ["individual small oval leaflets", "dried red chilli broken pieces", "shallot slices", "crushed peanuts or coconut flakes"]
        },
        common_ingredients=["fresh moringa (murungai) leaves", "shallots", "dry red chillies", "mustard seeds", "oil", "salt"],
        possible_ingredients=["crushed roasted peanuts", "grated coconut"],
        hard_negative_classes=["spinach_keerai", "methi_leaves", "keerai_masiyal"],
        portion_classes={"small": 40.0, "medium": 70.0, "large": 110.0},
        weight_classes={"single_serving_g": 65.0, "density_g_cm3": 0.58},
        nutrition_reference={"calories_per_100g": 95.0, "protein_g": 6.8, "carbs_g": 8.2, "fat_g": 3.8, "fiber_g": 4.5, "sodium_mg": 190.0},
        confidence_rules={"tiny_oval_leaflets_detected": 0.92, "rule_never_classify_as_spinach": 1.0},
        annotation_requirements=["NEVER classify as generic spinach; confirm small individual moringa leaflets"]
    )
]

for item in PORIYAL_CLASSES:
    register_class(item)

# =============================================================================
# SECTION 21 — SOUTH INDIAN NON-VEG (Chicken 65 & Chettinad)
# =============================================================================

NON_VEG_CLASSES = [
    ExtremeFoodClass(
        food_id="tn_chicken_65",
        canonical_name="South Indian Chicken 65",
        alternate_names=["Chennai Chicken 65", "Chicken 65 Fry"],
        regional_names={"Tamil": "சிக்கன் 65", "Telugu": "చికెన్ 65"},
        category="Starter",
        sub_category="Non-Veg Chicken",
        region="South Indian",
        state="Tamil Nadu",
        variant="Bite-sized chicken chunks marinated in curd, Kashmiri chilli, ginger, garlic, and cornstarch, deep fried and tossed with crackled curry leaves and green chillies",
        cooking_method="deep_fried_and_tossed",
        food_state="solid_crispy_meat",
        visual_features={
            "shape": "bite_sized_irregular_nuggets",
            "color": "deep_crimson_ruby_red",
            "surface_texture": "blistered_crisp_crust",
            "visible_inclusions": ["deep-fried translucent green curry leaves", "slit green chillies", "lemon wedges", "thin sliced onion rings"]
        },
        common_ingredients=["boneless chicken chunks", "curd / yogurt", "kashmiri red chilli powder", "ginger garlic paste", "cornstarch", "rice flour", "curry leaves", "green chillies", "oil"],
        possible_ingredients=["black pepper", "lemon juice"],
        hard_negative_classes=["gobi_65", "paneer_65", "chicken_tikka", "buffalo_wings"],
        portion_classes={"small": 120.0, "medium": 180.0, "large": 260.0},
        weight_classes={"single_serving_g": 180.0, "density_g_cm3": 0.78},
        nutrition_reference={"calories_per_100g": 245.0, "protein_g": 22.5, "carbs_g": 9.2, "fat_g": 13.1, "fiber_g": 0.8, "sodium_mg": 520.0},
        confidence_rules={"crimson_red_crust": 0.92, "fried_curry_leaf_adornment": 0.89},
        annotation_requirements=["verify chicken meat fiber structure to differentiate from cauliflower Gobi 65 or Paneer 65"]
    )
]

for item in NON_VEG_CLASSES:
    register_class(item)

# =============================================================================
# TAXONOMY ACCESS & SEARCH INTERFACE
# =============================================================================

def get_food_class(food_id: str) -> Optional[ExtremeFoodClass]:
    return EXTREME_TAXONOMY_REGISTRY.get(food_id)

def get_all_food_classes() -> List[ExtremeFoodClass]:
    return list(EXTREME_TAXONOMY_REGISTRY.values())

def find_classes_by_name(query: str) -> List[ExtremeFoodClass]:
    q = query.lower().strip()
    results = []
    for item in EXTREME_TAXONOMY_REGISTRY.values():
        if (q in item.canonical_name.lower() or 
            any(q in alt.lower() for alt in item.alternate_names) or
            any(q in reg.lower() for reg in item.regional_names.values())):
            results.append(item)
    return results

def get_classes_by_subcategory(sub_category: str) -> List[ExtremeFoodClass]:
    return [item for item in EXTREME_TAXONOMY_REGISTRY.values() if item.sub_category == sub_category]
