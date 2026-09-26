"""
Extreme Annotation Schema & Physical Calibrators
Implements Section 31, 32, 33, 34, 35, 36, and 37 of Part 2.
"""

from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

# =============================================================================
# SECTION 36 — FORMAL 24-FIELD ANNOTATION SCHEMA
# =============================================================================

class BoundingBox(BaseModel):
    ymin: float = Field(..., ge=0.0, le=1.0)
    xmin: float = Field(..., ge=0.0, le=1.0)
    ymax: float = Field(..., ge=0.0, le=1.0)
    xmax: float = Field(..., ge=0.0, le=1.0)

class FoodItemDetailedAnnotation(BaseModel):
    image_id: str
    meal_id: str = Field(..., description="Groups multi-view/multi-shot images of the same physical meal")
    source_id: str
    session_id: str
    food_id: str
    canonical_name: str
    variant: str
    region: str
    state: str
    category: str
    bbox: BoundingBox
    segmentation: List[List[float]] = Field(default_factory=list, description="[[x1, y1], [x2, y2], ...]")
    occlusion_level: float = Field(default=0.0, ge=0.0, le=1.0, description="0.0 = fully visible, 1.0 = completely occluded")
    visibility: float = Field(default=1.0, ge=0.0, le=1.0)
    portion_size: str = Field(default="medium", description="small, medium, or large")
    actual_weight_grams: float = Field(..., description="Ground-truth digital scale weight in grams")
    plate_diameter: Optional[float] = Field(default=26.0, description="Measured reference plate diameter in cm")
    bowl_diameter: Optional[float] = Field(default=None, description="Measured reference bowl diameter in cm")
    cooking_method: str = Field(default="cooked")
    food_state: str = Field(default="solid")
    ingredients: List[str] = Field(default_factory=list)
    confidence: float = Field(default=1.0)
    annotator: str = Field(default="expert_chef_nutritionist")
    annotation_status: str = Field(default="verified", description="verified, pending_review, gold_standard")
    nutrition_reference_id: str

# =============================================================================
# SECTION 37 — EXPLICIT UNKNOWN / UNCERTAIN OOD LABELS
# =============================================================================

EXPLICIT_UNKNOWN_LABELS = {
    "unknown_food": "Non-food or unrecognizable item; no calorie prediction forced.",
    "unknown_south_indian_food": "Clear South Indian culinary features, but exact variant cannot be verified visually.",
    "unknown_chutney": "Chutney detected — exact type uncertain (e.g. coconut vs peanut vs sesame).",
    "unknown_rice": "Rice preparation detected — exact grain or variety unconfirmed without aroma/taste.",
    "unknown_curry": "South Indian gravy / curry detected — exact protein or vegetable type uncertain.",
    "unknown_snack": "Deep-fried South Indian savory snack detected — exact dough/filling uncertain.",
    "unknown_nonveg": "Meat/poultry/seafood preparation detected — exact species/cut unconfirmed.",
    "mixed_food": "Heavily mixed food (e.g., rice and curry mashed together prior to eating).",
    "partially_visible": "Item cut off at image boundary (> 50% outside frame).",
    "heavily_occluded": "Item hidden behind taller dishes, glass, or cutlery (> 70% occluded).",
    "blurred_food": "Motion blur or out-of-focus blur prevents fine-grained classification.",
    "low_light_food": "Severe underexposure; color chroma and texture unresolvable."
}

# =============================================================================
# SECTION 31 — IMAGE COLLECTION ENVIRONMENT METADATA
# =============================================================================

class ImageCollectionProtocol(BaseModel):
    source_setting: str = Field(..., description="home, restaurant, hotel, college_mess, street_food, canteen, takeaway, delivery, traditional_serving, modern_serving")
    view_angle: str = Field(..., description="top_view, 45_degree, side_view, close_up, far_view, partial_crop")
    lighting_condition: str = Field(..., description="bright_lighting, dark_lighting, yellow_lighting, natural_lighting, flash, shadows, backlight, blur, motion_blur")
    serving_vessel: str = Field(..., description="banana_leaf, steel_plate, stainless_thali, ceramic_plate, plastic_container, clay_pot, paper_box, leaf_cup")
    background_type: str = Field(..., description="wooden_table, granite_table, steel_table, floor_mat, plastic_table, tablecloth")

# =============================================================================
# SECTION 32 & 33 — PORTION DISTRIBUTIONS & REFERENCE CALIBRATION
# =============================================================================

# Calibrated physical density table for volume-to-mass conversion (g/cm^3)
CALIBRATED_DENSITY_TABLE: Dict[str, float] = {
    "plain_idli": 0.72,
    "soft_idli": 0.62,
    "dense_idli": 0.88,
    "rava_idli": 0.82,
    "thatte_idli": 0.70,
    "plain_dosa": 0.48,
    "masala_dosa": 0.58,
    "mysore_masala_dosa": 0.62,
    "ghee_roast_dosa": 0.42,
    "neer_dosa": 0.65,
    "medu_vada": 0.62,
    "paruppu_vada": 0.88,
    "sambar_vada": 0.95,
    "thayir_vada": 0.98,
    "ven_pongal": 0.95,
    "rava_upma": 0.88,
    "poori": 0.45,
    "malabar_parotta": 0.80,
    "chicken_kothu_parotta": 0.86,
    "seeraga_samba_biryani": 0.84,
    "basmati_chicken_biryani": 0.82,
    "steamed_ponni_rice": 0.85,
    "curd_rice": 0.98,
    "hotel_sambar": 1.05,
    "tomato_rasam": 1.02,
    "white_coconut_chutney": 1.02,
    "tomato_kaara_chutney": 1.06,
    "beans_poriyal": 0.65,
    "chicken_65": 0.78
}

class ReferenceScaleCalibrator:
    @staticmethod
    def calculate_scale_ratio(measured_plate_pixels: float, standard_plate_diameter_cm: float = 26.0) -> float:
        """
        Calculates pixels-per-centimeter ratio.
        """
        if measured_plate_pixels <= 0:
            return 1.0
        return measured_plate_pixels / standard_plate_diameter_cm

    @staticmethod
    def estimate_physical_weight(
        area_pixels: float,
        pixels_per_cm: float,
        thickness_cm: float,
        food_id: str,
        shape_form_factor: float = 0.80
    ) -> float:
        """
        Converts 2D segmented area + estimated thickness into physical mass (grams)
        using calibrated density tables. Never assumes volume = weight.
        """
        if pixels_per_cm <= 0:
            pixels_per_cm = 15.0 # fallback default
            
        area_cm2 = area_pixels / (pixels_per_cm ** 2)
        volume_cm3 = area_cm2 * thickness_cm * shape_form_factor
        
        density = CALIBRATED_DENSITY_TABLE.get(food_id.lower(), 0.80)
        estimated_weight_g = volume_cm3 * density
        return round(max(5.0, estimated_weight_g), 1)

# =============================================================================
# SECTION 34 & 35 — INVARIANCE & HARD NEGATIVE SPECIFICATIONS
# =============================================================================

INVARIANCE_RULES = [
    "Plate and table invariance: Food identity must not change whether served on banana leaf, steel plate, or ceramic.",
    "Lighting invariance: Sambar must be identified under warm yellow tungsten, daylight, or smartphone LED flash.",
    "Garnish invariance: Dosa remains Dosa whether topped with chopped coriander, podi sprinkle, or served plain.",
    "Background invariance: Food detection must remain robust across restaurant, college mess, home, and street stalls."
]

HARD_NEGATIVE_TRIPLETS = [
    {"anchor": "ven_pongal", "positive": "ghee_pongal", "negative": "rava_upma", "reason": "Both yellow mash; distinguish via whole peppercorns vs mustard seeds."},
    {"anchor": "medu_vada", "positive": "ulundhu_vada", "negative": "aloo_bonda", "reason": "Both golden fried; distinguish via central hole aperture."},
    {"anchor": "dindigul_biryani", "positive": "thalappakatti_biryani", "negative": "hyderabadi_biryani", "reason": "Both biryanis; distinguish via Seeraga Samba short grain vs Basmati needles."},
    {"anchor": "paruppu_vada", "positive": "masala_vada", "negative": "onion_pakoda", "reason": "Both crunchy dal snacks; distinguish via flat round disc vs jagged cluster."}
]
