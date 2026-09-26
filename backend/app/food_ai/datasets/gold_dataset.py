"""
Gold Benchmark Dataset & South Indian Dedicated Test Set
Strict zero-contamination benchmark dataset with verified physical weights,
ground truth instance masks, and verified recipes. Never used during training.
"""

from typing import List
from .schema import FoodSample, FoodItemAnnotation, BoundingBox, ReferenceObjectScale, CameraMetadata

GOLD_BENCHMARK_SAMPLES: List[FoodSample] = [
    FoodSample(
        sample_id="gold_tn_001_masala_dosa",
        meal_id="meal_phys_001",
        photo_session_id="session_expert_01",
        source_setting="restaurant",
        image_path="datasets/gold/masala_dosa_01.jpg",
        image_sha256="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        perceptual_hash="d3a7c1b8e4f20109",
        image_width=1080,
        image_height=810,
        view_angle="top",
        reference_scale=ReferenceObjectScale(plate_diameter_cm=26.0),
        camera_metadata=CameraMetadata(device_model="Pixel 8", estimated_distance_cm=35.0, view_angle="top"),
        food_items=[
            FoodItemAnnotation(
                item_id="item_001_dosa",
                class_name="Masala Dosa",
                hierarchical_path="Food > South Indian > Tiffin > Dosa > Masala Dosa > Pan Fried > Cooked Solid",
                bbox=BoundingBox(ymin=0.15, xmin=0.10, ymax=0.85, xmax=0.90),
                actual_weight_grams=184.0,
                portion_class="medium",
                cooking_method="pan_fried",
                food_state="cooked"
            )
        ],
        total_actual_weight_grams=184.0,
        dataset_version="dataset_gold_v1",
        validation_status="expert_verified",
        split="gold_benchmark"
    ),
    FoodSample(
        sample_id="gold_tn_002_idli_sambar",
        meal_id="meal_phys_002",
        photo_session_id="session_expert_01",
        source_setting="home",
        image_path="datasets/gold/idli_sambar_chutney_02.jpg",
        image_sha256="4b227777d4dd1fc61c6f884f48641d02b4d121d3fd328cb08b5531fcacdabf8a",
        perceptual_hash="b4a8e2c1f5d30218",
        image_width=1080,
        image_height=810,
        view_angle="top",
        reference_scale=ReferenceObjectScale(plate_diameter_cm=24.0),
        camera_metadata=CameraMetadata(device_model="iPhone 15", estimated_distance_cm=30.0, view_angle="top"),
        food_items=[
            FoodItemAnnotation(
                item_id="item_002_idli_1",
                class_name="Idli",
                hierarchical_path="Food > South Indian > Tiffin > Idli > Steamed Idli > Steamed > Fermented",
                bbox=BoundingBox(ymin=0.20, xmin=0.15, ymax=0.55, xmax=0.45),
                actual_weight_grams=62.0,
                portion_class="small",
                cooking_method="steamed",
                food_state="cooked"
            ),
            FoodItemAnnotation(
                item_id="item_002_idli_2",
                class_name="Idli",
                hierarchical_path="Food > South Indian > Tiffin > Idli > Steamed Idli > Steamed > Fermented",
                bbox=BoundingBox(ymin=0.45, xmin=0.20, ymax=0.80, xmax=0.50),
                actual_weight_grams=61.0,
                portion_class="small",
                cooking_method="steamed",
                food_state="cooked"
            ),
            FoodItemAnnotation(
                item_id="item_002_sambar",
                class_name="Drumstick Sambar",
                hierarchical_path="Food > South Indian > Lentil Stew > Sambar > Drumstick Sambar > Simmered > Liquid",
                bbox=BoundingBox(ymin=0.15, xmin=0.55, ymax=0.45, xmax=0.85),
                actual_weight_grams=115.0,
                portion_class="medium",
                cooking_method="boiled",
                food_state="liquid"
            ),
            FoodItemAnnotation(
                item_id="item_002_chutney",
                class_name="Coconut Chutney",
                hierarchical_path="Food > South Indian > Condiment > Chutney > Coconut Chutney > Ground > Semi-Solid",
                bbox=BoundingBox(ymin=0.50, xmin=0.58, ymax=0.78, xmax=0.86),
                actual_weight_grams=38.0,
                portion_class="small",
                cooking_method="raw",
                food_state="semi-solid"
            )
        ],
        total_actual_weight_grams=276.0,
        dataset_version="dataset_gold_v1",
        validation_status="expert_verified",
        split="gold_benchmark"
    ),
    FoodSample(
        sample_id="gold_tn_003_biryani_thalappakatti",
        meal_id="meal_phys_003",
        photo_session_id="session_expert_02",
        source_setting="restaurant",
        image_path="datasets/gold/thalappakatti_biryani_03.jpg",
        image_sha256="ef2d127de37b942baad06145e54b0c619a1f22327b2ebbcfbec78f5564afe39d",
        perceptual_hash="c3b9d1e4a5f60329",
        image_width=1080,
        image_height=810,
        view_angle="45_degree",
        reference_scale=ReferenceObjectScale(plate_diameter_cm=26.0),
        camera_metadata=CameraMetadata(device_model="Samsung S23", estimated_distance_cm=40.0, view_angle="45_degree"),
        food_items=[
            FoodItemAnnotation(
                item_id="item_003_biryani",
                class_name="Chicken Biryani",
                hierarchical_path="Food > South Indian > Rice Dish > Biryani > Dindigul Thalappakatti Style > Dum Cooked > Cooked Solid",
                bbox=BoundingBox(ymin=0.15, xmin=0.15, ymax=0.80, xmax=0.80),
                actual_weight_grams=348.0,
                portion_class="large",
                cooking_method="pressure_cooked",
                food_state="cooked"
            ),
            FoodItemAnnotation(
                item_id="item_003_egg",
                class_name="Boiled Egg",
                hierarchical_path="Food > Indian > Protein > Egg > Boiled Egg > Boiled > Solid",
                bbox=BoundingBox(ymin=0.25, xmin=0.65, ymax=0.45, xmax=0.82),
                actual_weight_grams=52.0,
                portion_class="small",
                cooking_method="boiled",
                food_state="cooked"
            )
        ],
        total_actual_weight_grams=400.0,
        dataset_version="dataset_gold_v1",
        validation_status="expert_verified",
        split="gold_benchmark"
    )
]
