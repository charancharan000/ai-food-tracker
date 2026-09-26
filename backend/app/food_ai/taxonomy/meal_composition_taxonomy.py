"""
South Indian Full Meal & Banana Leaf Meal Composition Taxonomy
Defines component items for composite meals so that each distinct food item
is segmented, classified, and weighed individually.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class MealComponentAnnotation(BaseModel):
    component_name: str
    bounding_box_normalized: Optional[List[float]] = None # [ymin, xmin, ymax, xmax]
    segmentation_polygon: Optional[List[List[float]]] = None
    default_serving_weight_g: float
    actual_measured_weight_g: Optional[float] = None
    calories_per_100g: float
    protein_per_100g: float
    carbs_per_100g: float
    fat_per_100g: float

class BananaLeafMealComposition(BaseModel):
    meal_type: str = "Tamil Nadu Banana Leaf Sappadu"
    components: List[MealComponentAnnotation] = Field(default_factory=list)

BANANA_LEAF_STANDARD_TEMPLATE = BananaLeafMealComposition(
    components=[
        MealComponentAnnotation(
            component_name="Steamed White Rice (Center)",
            default_serving_weight_g=250.0,
            calories_per_100g=130.0,
            protein_per_100g=2.7,
            carbs_per_100g=28.2,
            fat_per_100g=0.3
        ),
        MealComponentAnnotation(
            component_name="Drumstick Sambar",
            default_serving_weight_g=120.0,
            calories_per_100g=75.0,
            protein_per_100g=3.5,
            carbs_per_100g=11.2,
            fat_per_100g=1.8
        ),
        MealComponentAnnotation(
            component_name="Tomato Pepper Rasam",
            default_serving_weight_g=90.0,
            calories_per_100g=32.0,
            protein_per_100g=1.2,
            carbs_per_100g=5.5,
            fat_per_100g=0.6
        ),
        MealComponentAnnotation(
            component_name="Chow Chow Kootu",
            default_serving_weight_g=80.0,
            calories_per_100g=82.0,
            protein_per_100g=3.8,
            carbs_per_100g=10.5,
            fat_per_100g=2.8
        ),
        MealComponentAnnotation(
            component_name="Beans Carrot Poriyal",
            default_serving_weight_g=75.0,
            calories_per_100g=70.0,
            protein_per_100g=2.1,
            carbs_per_100g=8.4,
            fat_per_100g=3.2
        ),
        MealComponentAnnotation(
            component_name="Avial",
            default_serving_weight_g=70.0,
            calories_per_100g=118.0,
            protein_per_100g=2.6,
            carbs_per_100g=11.8,
            fat_per_100g=6.8
        ),
        MealComponentAnnotation(
            component_name="Homemade Curd (Thayir)",
            default_serving_weight_g=100.0,
            calories_per_100g=61.0,
            protein_per_100g=3.5,
            carbs_per_100g=4.7,
            fat_per_100g=3.3
        ),
        MealComponentAnnotation(
            component_name="Crispy Appalam / Papad",
            default_serving_weight_g=15.0,
            calories_per_100g=375.0,
            protein_per_100g=20.0,
            carbs_per_100g=50.0,
            fat_per_100g=10.0
        ),
        MealComponentAnnotation(
            component_name="Mango Pickle (Oorugai)",
            default_serving_weight_g=10.0,
            calories_per_100g=170.0,
            protein_per_100g=1.5,
            carbs_per_100g=8.0,
            fat_per_100g=14.5
        ),
        MealComponentAnnotation(
            component_name="Semiya Payasam (Dessert)",
            default_serving_weight_g=60.0,
            calories_per_100g=195.0,
            protein_per_100g=3.8,
            carbs_per_100g=32.0,
            fat_per_100g=6.2
        )
    ]
)
