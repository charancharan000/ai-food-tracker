"""
Human Expert Annotation Service
Backend for admin annotation tools: handles bounding boxes, segmentation polygons,
physical scale weights, regional tags, ingredients, and gold dataset promotion.
"""

import time
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from ..datasets.schema import FoodSample, FoodItemAnnotation, BoundingBox, ReferenceObjectScale

class AdminAnnotationPayload(BaseModel):
    queue_id: Optional[str] = None
    image_path: str
    image_width: int
    image_height: int
    meal_id: str
    
    # Food item annotations
    items: List[Dict[str, Any]] # class_name, bbox [ymin, xmin, ymax, xmax], segmentation_polygon, actual_weight_grams
    reference_scale_diameter_cm: float = 26.0
    cuisine_region: str = "South Indian"
    cooking_method: str = "cooked"
    food_state: str = "solid"
    ingredients: List[str] = Field(default_factory=list)
    approve_for_gold_benchmark: bool = False

class AnnotationService:
    @staticmethod
    def process_admin_annotation(payload: AdminAnnotationPayload) -> FoodSample:
        """
        Converts human admin annotation into canonical FoodSample and adds to training/benchmark pool.
        """
        food_items: List[FoodItemAnnotation] = []
        total_w = 0.0

        for idx, it in enumerate(payload.items):
            box_raw = it.get("bbox", [0.1, 0.1, 0.9, 0.9])
            actual_w = float(it.get("actual_weight_grams", 150.0))
            total_w += actual_w

            food_items.append(FoodItemAnnotation(
                item_id=f"ann_item_{int(time.time())}_{idx}",
                class_name=it.get("class_name", "Food Item"),
                hierarchical_path=f"Food > {payload.cuisine_region} > {it.get('class_name', 'Dish')} > Cooked",
                bbox=BoundingBox(ymin=box_raw[0], xmin=box_raw[1], ymax=box_raw[2], xmax=box_raw[3]),
                segmentation_polygon=it.get("segmentation_polygon", None),
                actual_weight_grams=actual_w,
                portion_class=it.get("portion_class", "medium"),
                cooking_method=payload.cooking_method,
                food_state=payload.food_state,
                visible_ingredients=payload.ingredients,
                confidence_annotated=1.0
            ))

        sample = FoodSample(
            sample_id=f"sample_{int(time.time() * 1000)}",
            meal_id=payload.meal_id,
            photo_session_id=f"session_admin_{int(time.time())}",
            source_setting="restaurant",
            image_path=payload.image_path,
            image_sha256="validated_human_sample",
            image_width=payload.image_width,
            image_height=payload.image_height,
            reference_scale=ReferenceObjectScale(plate_diameter_cm=payload.reference_scale_diameter_cm),
            food_items=food_items,
            total_actual_weight_grams=round(total_w, 1),
            dataset_version="dataset_v2",
            validation_status="expert_verified",
            split="gold_benchmark" if payload.approve_for_gold_benchmark else "train"
        )

        return sample
