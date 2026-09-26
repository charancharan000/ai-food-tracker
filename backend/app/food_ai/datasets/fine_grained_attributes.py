"""
Fine-Grained Attribute Annotation Models & Food State System
Implements Sections 5, 7, 9, 11, 13, 16, 18, 20-28 of Part 3.
Guarantees:
- Specific detailed visual attribute models for Idli, Sambar, Chutney, Dosa, Vada, Rice, Biryani, Meat/Fish/Egg
- 30 Vegetable Ingredient Classes with VISIBLE, NOT_VISIBLE, UNCERTAIN status
- 16 discrete cooking methods with multi-label support
- 20 discrete food states
"""

from typing import List, Dict, Any, Optional
from enum import Enum
from pydantic import BaseModel, Field

# =============================================================================
# SECTIONS 25 & 26 — 30 VEGETABLES & TERNARY VISIBILITY STATUS
# =============================================================================

class IngredientVisibilityStatus(str, Enum):
    VISIBLE = "VISIBLE"
    NOT_VISIBLE = "NOT_VISIBLE"
    UNCERTAIN = "UNCERTAIN"

THIRTY_VEGETABLE_CLASSES = [
    "potato", "carrot", "beans", "peas", "beetroot", "cabbage", "cauliflower",
    "brinjal", "okra", "drumstick", "pumpkin", "radish", "onion", "shallot",
    "tomato", "capsicum", "coconut", "green_chilli", "red_chilli", "spinach",
    "moringa_leaves", "banana", "raw_banana", "bottle_gourd", "snake_gourd",
    "chow_chow", "bitter_gourd", "cluster_beans", "ivy_gourd", "curry_leaves"
]

class VegetablePresenceRecord(BaseModel):
    vegetable_name: str
    status: IngredientVisibilityStatus
    confidence: float = 1.0
    bounding_box: Optional[Dict[str, float]] = None

# =============================================================================
# SECTIONS 27 & 28 — 16 COOKING METHODS & 20 FOOD STATES
# =============================================================================

SIXTEEN_COOKING_METHODS = [
    "steamed", "boiled", "pressure_cooked", "deep_fried", "shallow_fried",
    "pan_fried", "tawa_fried", "grilled", "roasted", "baked", "air_fried",
    "sauteed", "stir_fried", "slow_cooked", "fermented", "raw"
]

TWENTY_FOOD_STATES = [
    "raw", "uncooked", "partially_cooked", "cooked", "overcooked", "fried",
    "steamed", "boiled", "grilled", "roasted", "mashed", "pureed", "chopped",
    "sliced", "diced", "shredded", "mixed", "liquid", "semi_solid", "solid"
]

# =============================================================================
# SECTION 5 — IDLI DETAILED VISUAL ATTRIBUTES
# =============================================================================

class IdliSampleAnnotation(BaseModel):
    idli_type: str = Field(..., description="plain, mini, button, rava, kanchipuram, millet, ragi, oats, vegetable, podi, ghee_podi, fried, masala, stuffed")
    piece_count: int = Field(..., ge=1)
    piece_width_cm: float = 7.5
    piece_height_cm: float = 2.8
    shape: str = Field(default="convex_lens_disc")
    surface_texture: str = Field(default="porous_micro_aerated")
    softness_indicator: str = Field(default="high_springy", description="soft, medium, dense")
    color: str = Field(default="snow_white")
    steam_visibility: bool = False
    visible_cracks: bool = False
    plate_type: str = Field(default="steel_plate")
    serving_style: str = Field(default="dry_with_accompaniments_side")
    sambar_present: bool = True
    chutney_present: bool = True
    podi_present: bool = False
    oil_present: bool = False
    ghee_present: bool = False

# =============================================================================
# SECTION 7 — SAMBAR DETAILED VISUAL ATTRIBUTES
# =============================================================================

class SambarSampleAnnotation(BaseModel):
    sambar_class: str = Field(default="tiffin_sambar")
    thickness: str = Field(default="medium_broth", description="thin, medium_broth, thick")
    color: str = Field(default="golden_orange_translucent")
    oil_layer: str = Field(default="thin_sheen", description="none, thin_sheen, heavy_ghee")
    dal_visibility: bool = True
    vegetable_visibility: bool = True
    tamarind_appearance: str = Field(default="mildly_tangy_tint")
    spice_particles: bool = True
    curry_leaves: bool = True
    mustard_seeds: bool = True
    vegetable_types_present: List[str] = Field(default_factory=lambda: ["shallots", "drumstick", "tomato"])
    bowl_type: str = Field(default="katori_steel_cup")
    liquid_level_pct: float = 85.0
    serving_temperature: str = Field(default="steaming_hot")
    portion_g: float = 110.0

# =============================================================================
# SECTION 9 — CHUTNEY DETAILED VISUAL ATTRIBUTES
# =============================================================================

class ChutneySampleAnnotation(BaseModel):
    chutney_class: str = Field(default="white_coconut_chutney")
    color: str = Field(default="ivory_white")
    texture: str = Field(default="fine_grated_crumb")
    smoothness: str = Field(default="medium_coarse")
    thickness: str = Field(default="medium_thick_paste")
    visible_ingredients: List[str] = Field(default_factory=lambda: ["coconut_crumb", "mustard_seeds", "curry_leaves"])
    oil_layer: str = Field(default="light_tempering_droplets")
    tempering_present: bool = True
    container: str = Field(default="plate_dollop")
    portion_g: float = 45.0
    garnishing: Optional[str] = "fried_curry_leaf"

# =============================================================================
# SECTION 11 — DOSA DETAILED VISUAL ATTRIBUTES
# =============================================================================

class DosaSampleAnnotation(BaseModel):
    dosa_class: str = Field(default="masala_dosa")
    diameter_cm: float = 28.0
    thickness_cm: float = 0.20
    fold_count: int = 1
    fold_direction: str = Field(default="half_moon", description="half_moon, triangle, roll, open_flat, cone")
    crispness: str = Field(default="brittle_crisp")
    edge_color: str = Field(default="deep_golden_brown")
    center_color: str = Field(default="golden_amber")
    surface: str = Field(default="spiral_grooved_with_roasted_blisters")
    oil_level: str = Field(default="moderate")
    ghee_level: str = Field(default="high")
    masala_present: bool = True
    toppings: List[str] = Field(default_factory=list)
    filling: Optional[str] = "spiced_potato_onion_mash"
    burn_marks: bool = False
    holes_pattern: str = Field(default="micro_pores", description="micro_pores, open_mesh_net, smooth")
    shape: str = Field(default="folded_cylinder")

# =============================================================================
# SECTION 13 — VADA DETAILED VISUAL ATTRIBUTES
# =============================================================================

class VadaSampleAnnotation(BaseModel):
    vada_class: str = Field(default="medu_vada")
    hole_count: int = 1
    hole_diameter_cm: float = 2.2
    diameter_cm: float = 7.8
    thickness_cm: float = 3.2
    surface: str = Field(default="blistered_fried_crust")
    roughness: str = Field(default="crisp_light")
    fried_color: str = Field(default="deep_golden_amber")
    visible_ingredients: List[str] = Field(default_factory=lambda: ["whole_black_pepper", "curry_leaves", "chilli_bits"])
    onion_visible: bool = False
    chilli_visible: bool = True
    curry_leaves_visible: bool = True
    dal_visibility: str = Field(default="smooth_pureed_aerated", description="smooth_pureed_aerated, whole_chana_dal_pebbles")

# =============================================================================
# SECTION 16 — RICE DETAILED VISUAL ATTRIBUTES
# =============================================================================

class RiceSampleAnnotation(BaseModel):
    rice_class: str = Field(default="curd_rice")
    grain_length_mm: float = 5.2
    grain_width_mm: float = 2.1
    grain_color: str = Field(default="creamy_white")
    grain_shape: str = Field(default="medium_oval_mashed")
    cooked_state: str = Field(default="soft_mashed_emulsion")
    oil_presence: bool = False
    ghee_presence: bool = False
    moisture_level: str = Field(default="creamy_moist")
    visible_ingredients: List[str] = Field(default_factory=lambda: ["curd", "mustard_seeds", "green_chillies", "ginger"])
    spices_present: List[str] = Field(default_factory=lambda: ["mustard", "asafoetida"])
    vegetables_present: List[str] = Field(default_factory=list)
    meat_present: bool = False
    egg_present: bool = False
    sauce_coating: str = Field(default="yogurt_cream")

# =============================================================================
# SECTION 18 & 19 — BIRYANI DETAILED VISUAL ATTRIBUTES
# =============================================================================

class BiryaniSampleAnnotation(BaseModel):
    biryani_class: str = Field(default="dindigul_mutton_biryani")
    regional_style: str = Field(default="Dindigul")
    rice_type: str = Field(default="seeraga_samba", description="seeraga_samba, basmati, jeerakasala")
    rice_color: str = Field(default="uniform_amber_brown")
    grain_length_mm: float = 4.2
    meat_type: str = Field(default="mutton", description="chicken, mutton, egg, fish, prawn, veg")
    meat_piece_count: int = 3
    egg_presence: bool = True
    fried_onion_visible: bool = True
    mint_visible: bool = True
    coriander_visible: bool = True
    whole_spices_visible: List[str] = Field(default_factory=lambda: ["cloves", "cinnamon", "cardamom"])
    oil_ghee_sheen: str = Field(default="rich_gloss")
    masala_coating: str = Field(default="uniformly_absorbed_in_grain")
    layering_visible: bool = False
    container: str = Field(default="ceramic_plate")
    serving_style: str = Field(default="platter_with_raita_and_gravy")
    accompanying_items: List[str] = Field(default_factory=lambda: ["boiled_egg", "onion_raita", "ennai_kathirikai"])

# =============================================================================
# SECTIONS 20-24 — NON-VEGETARIAN & EGG DETAILED ATTRIBUTES
# =============================================================================

class ProteinMeatSampleAnnotation(BaseModel):
    protein_type: str = Field(..., description="chicken, mutton, fish, prawn, crab, squid, egg")
    bone_present: bool = True
    piece_count: int = 4
    piece_size_cm: float = 4.5
    cut_type: str = Field(default="curry_cut", description="steak, fillet, whole, head, tail, curry_cut, lollipop, wing, drumstick")
    skin_present: bool = False
    gravy_coating: str = Field(default="thick_caramelized_masala")
    fried_coating: Optional[str] = "crispy_cornstarch_batter"
    yolk_visible: Optional[bool] = None
    yolk_color: Optional[str] = None
    cooked_state: str = Field(default="well_done_roasted")
