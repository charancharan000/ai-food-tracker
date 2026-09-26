"""
Portion Gold Dataset with Verified Measured Physical Weights & Multi-View Linkage
Each food is captured from top, 45-degree, and side angles with verified physical scale weight.
"""

from typing import List, Dict, Any
from pydantic import BaseModel, Field

class MultiViewMealSample(BaseModel):
    meal_id: str
    dish_name: str
    actual_measured_weight_grams: float
    portion_class: str
    top_view_image: str
    angle_45_image: str
    side_view_image: str
    plate_diameter_cm: float = 26.0

PORTION_GOLD_SAMPLES: List[MultiViewMealSample] = [
    MultiViewMealSample(
        meal_id="mv_phys_001",
        dish_name="Masala Dosa",
        actual_measured_weight_grams=182.0,
        portion_class="medium",
        top_view_image="datasets/portion_gold/mv_001_top.jpg",
        angle_45_image="datasets/portion_gold/mv_001_45.jpg",
        side_view_image="datasets/portion_gold/mv_001_side.jpg",
        plate_diameter_cm=26.0
    ),
    MultiViewMealSample(
        meal_id="mv_phys_002",
        dish_name="Steamed White Rice",
        actual_measured_weight_grams=247.0,
        portion_class="large",
        top_view_image="datasets/portion_gold/mv_002_top.jpg",
        angle_45_image="datasets/portion_gold/mv_002_45.jpg",
        side_view_image="datasets/portion_gold/mv_002_side.jpg",
        plate_diameter_cm=24.0
    ),
    MultiViewMealSample(
        meal_id="mv_phys_003",
        dish_name="Chicken 65",
        actual_measured_weight_grams=156.0,
        portion_class="medium",
        top_view_image="datasets/portion_gold/mv_003_top.jpg",
        angle_45_image="datasets/portion_gold/mv_003_45.jpg",
        side_view_image="datasets/portion_gold/mv_003_side.jpg",
        plate_diameter_cm=22.0
    ),
    MultiViewMealSample(
        meal_id="mv_phys_004",
        dish_name="Ven Pongal",
        actual_measured_weight_grams=215.0,
        portion_class="medium",
        top_view_image="datasets/portion_gold/mv_004_top.jpg",
        angle_45_image="datasets/portion_gold/mv_004_45.jpg",
        side_view_image="datasets/portion_gold/mv_004_side.jpg",
        plate_diameter_cm=24.0
    ),
    MultiViewMealSample(
        meal_id="mv_phys_005",
        dish_name="Chicken Biryani",
        actual_measured_weight_grams=365.0,
        portion_class="large",
        top_view_image="datasets/portion_gold/mv_005_top.jpg",
        angle_45_image="datasets/portion_gold/mv_005_45.jpg",
        side_view_image="datasets/portion_gold/mv_005_side.jpg",
        plate_diameter_cm=28.0
    )
]
