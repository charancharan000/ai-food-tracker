"""
Canonical Food Dataset Sample Schema
Enforces strict metadata requirements: physical scale weights, multi-view linkage,
instance segmentations, camera metadata, and split leakage protection.
"""

from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

class BoundingBox(BaseModel):
    ymin: float = Field(..., ge=0.0, le=1.0)
    xmin: float = Field(..., ge=0.0, le=1.0)
    ymax: float = Field(..., ge=0.0, le=1.0)
    xmax: float = Field(..., ge=0.0, le=1.0)

class FoodItemAnnotation(BaseModel):
    item_id: str
    class_name: str
    hierarchical_path: str
    bbox: BoundingBox
    segmentation_polygon: Optional[List[List[float]]] = None # [[x1, y1], [x2, y2], ...]
    
    # Ground Truth Physical Measurements
    actual_weight_grams: float = Field(..., description="Verified scale measurement in grams")
    portion_class: str = Field(default="medium", description="small, medium, or large")
    
    cooking_method: str = "cooked"
    food_state: str = "solid"
    visible_ingredients: List[str] = Field(default_factory=list)
    confidence_annotated: float = 1.0

class ReferenceObjectScale(BaseModel):
    reference_type: str = "plate" # "plate", "bowl", "cup", "card", "coin"
    plate_diameter_cm: Optional[float] = 26.0
    bowl_diameter_cm: Optional[float] = None
    known_width_cm: Optional[float] = None

class CameraMetadata(BaseModel):
    device_model: Optional[str] = None
    focal_length_mm: Optional[float] = None
    estimated_distance_cm: Optional[float] = 35.0
    view_angle: str = Field(default="top", description="top, 45_degree, or side")
    lighting_condition: str = Field(default="ambient", description="daylight, warm_indoor, low_light, flash")

class FoodSample(BaseModel):
    sample_id: str
    meal_id: str = Field(..., description="Crucial: groups multi-view images of the same physical meal to prevent train/val leakage")
    photo_session_id: str
    source_setting: str = Field(default="restaurant", description="home, restaurant, college_mess, hotel, street_food")
    
    image_path: str
    image_sha256: str
    perceptual_hash: Optional[str] = None # pHash string for near-duplicate prevention
    image_width: int
    image_height: int

    view_angle: str = "top" # "top", "45_degree", "side"
    reference_scale: Optional[ReferenceObjectScale] = None
    camera_metadata: Optional[CameraMetadata] = None

    food_items: List[FoodItemAnnotation] = Field(default_factory=list)
    total_actual_weight_grams: float

    dataset_version: str = "dataset_v1"
    validation_status: str = Field(default="expert_verified", description="expert_verified, community_validated, raw")
    split: str = Field(default="train", description="train, val, test, gold_benchmark")
