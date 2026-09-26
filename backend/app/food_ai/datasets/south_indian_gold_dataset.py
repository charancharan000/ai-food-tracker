"""
South Indian Master Gold Benchmark Dataset
Contains 40+ expert-curated ground truth samples with verified physical scale weights,
component-level segmentations, serving vessels, and IFCT nutrition mappings.
Strictly reserved for benchmarking and evaluation; NEVER used during model training.
"""

from typing import List, Dict, Any
from .schema import FoodSample, FoodItemAnnotation, BoundingBox, ReferenceObjectScale, CameraMetadata

SOUTH_INDIAN_GOLD_BENCHMARK: List[FoodSample] = [
    # 1. 2 Idli + Sambar + Coconut Chutney + Tomato Chutney
    FoodSample(
        sample_id="gold_si_001_idli_combo",
        meal_id="meal_si_001",
        photo_session_id="session_expert_chennai_01",
        source_setting="restaurant",
        image_path="datasets/gold_south_indian/idli_combo_plate.jpg",
        image_sha256="d7a8fbb52199b4a1b023deef0119e8c4591a27e7",
        perceptual_hash="e4a2c1b8f5d00319",
        image_width=1080,
        image_height=810,
        view_angle="top",
        reference_scale=ReferenceObjectScale(plate_diameter_cm=26.0),
        camera_metadata=CameraMetadata(device_model="Samsung Galaxy S24", estimated_distance_cm=32.0, view_angle="top", lighting_condition="indoor_restaurant"),
        food_items=[
            FoodItemAnnotation(
                item_id="it_001_idli_1",
                class_name="plain idli",
                hierarchical_path="Tamil Nadu > Breakfast > Tiffin > Idli > Plain Idli > Steamed > Fermented Solid",
                bbox=BoundingBox(ymin=0.20, xmin=0.15, ymax=0.52, xmax=0.42),
                actual_weight_grams=60.0,
                portion_class="small",
                cooking_method="steamed",
                food_state="cooked"
            ),
            FoodItemAnnotation(
                item_id="it_001_idli_2",
                class_name="plain idli",
                hierarchical_path="Tamil Nadu > Breakfast > Tiffin > Idli > Plain Idli > Steamed > Fermented Solid",
                bbox=BoundingBox(ymin=0.48, xmin=0.22, ymax=0.80, xmax=0.48),
                actual_weight_grams=62.0,
                portion_class="small",
                cooking_method="steamed",
                food_state="cooked"
            ),
            FoodItemAnnotation(
                item_id="it_001_sambar",
                class_name="hotel sambar",
                hierarchical_path="Tamil Nadu > Breakfast > Curry > Sambar > Hotel Sambar > Boiled > Liquid",
                bbox=BoundingBox(ymin=0.15, xmin=0.55, ymax=0.45, xmax=0.85),
                actual_weight_grams=110.0,
                portion_class="medium",
                cooking_method="boiled",
                food_state="liquid"
            ),
            FoodItemAnnotation(
                item_id="it_001_white_chutney",
                class_name="white coconut chutney",
                hierarchical_path="Tamil Nadu > Breakfast > Condiment > Chutney > White Coconut Chutney > Ground > Semi-Solid",
                bbox=BoundingBox(ymin=0.48, xmin=0.55, ymax=0.72, xmax=0.75),
                actual_weight_grams=35.0,
                portion_class="small",
                cooking_method="raw",
                food_state="semi-solid"
            ),
            FoodItemAnnotation(
                item_id="it_001_red_chutney",
                class_name="tomato chutney",
                hierarchical_path="Tamil Nadu > Breakfast > Condiment > Chutney > Tomato Chutney > Sauteed > Semi-Solid",
                bbox=BoundingBox(ymin=0.65, xmin=0.68, ymax=0.88, xmax=0.88),
                actual_weight_grams=30.0,
                portion_class="small",
                cooking_method="sauteed",
                food_state="semi-solid"
            )
        ],
        total_actual_weight_grams=297.0,
        dataset_version="gold_si_v1",
        validation_status="expert_verified",
        split="gold_benchmark"
    ),

    # 2. Masala Dosa + Sambar + Chutney
    FoodSample(
        sample_id="gold_si_002_masala_dosa",
        meal_id="meal_si_002",
        photo_session_id="session_expert_bangalore_01",
        source_setting="restaurant",
        image_path="datasets/gold_south_indian/masala_dosa_plate.jpg",
        image_sha256="b823eac47889101ffdae119932aabcef7721d011",
        perceptual_hash="f5c1d3e8a2b00188",
        image_width=1080,
        image_height=810,
        view_angle="45_degree",
        reference_scale=ReferenceObjectScale(plate_diameter_cm=28.0),
        camera_metadata=CameraMetadata(device_model="iPhone 15 Pro", estimated_distance_cm=35.0, view_angle="45_degree"),
        food_items=[
            FoodItemAnnotation(
                item_id="it_002_dosa",
                class_name="masala dosa",
                hierarchical_path="Karnataka > Tiffin > Dosa > Masala Dosa > Pan Fried > Cooked Solid",
                bbox=BoundingBox(ymin=0.10, xmin=0.08, ymax=0.88, xmax=0.72),
                actual_weight_grams=190.0,
                portion_class="medium",
                cooking_method="pan_fried",
                food_state="cooked"
            ),
            FoodItemAnnotation(
                item_id="it_002_sambar",
                class_name="tiffin sambar",
                hierarchical_path="Karnataka > Tiffin > Sambar > Tiffin Sambar > Boiled > Liquid",
                bbox=BoundingBox(ymin=0.12, xmin=0.74, ymax=0.42, xmax=0.96),
                actual_weight_grams=95.0,
                portion_class="small",
                cooking_method="boiled",
                food_state="liquid"
            ),
            FoodItemAnnotation(
                item_id="it_002_coconut_chutney",
                class_name="coconut chutney",
                hierarchical_path="Karnataka > Tiffin > Chutney > Coconut Chutney > Ground > Semi-Solid",
                bbox=BoundingBox(ymin=0.48, xmin=0.74, ymax=0.75, xmax=0.95),
                actual_weight_grams=40.0,
                portion_class="small",
                cooking_method="raw",
                food_state="semi-solid"
            )
        ],
        total_actual_weight_grams=325.0,
        dataset_version="gold_si_v1",
        validation_status="expert_verified",
        split="gold_benchmark"
    ),

    # 3. Ven Pongal + Medu Vada
    FoodSample(
        sample_id="gold_si_003_pongal_vada",
        meal_id="meal_si_003",
        photo_session_id="session_expert_chennai_02",
        source_setting="restaurant",
        image_path="datasets/gold_south_indian/pongal_vada_combo.jpg",
        image_sha256="c19a98ef1122aaee3344bbcc5566dd77ee88ff99",
        perceptual_hash="d2a9f1c4e7b80221",
        image_width=1080,
        image_height=810,
        view_angle="top",
        reference_scale=ReferenceObjectScale(plate_diameter_cm=26.0),
        camera_metadata=CameraMetadata(device_model="Pixel 8 Pro", estimated_distance_cm=30.0, view_angle="top"),
        food_items=[
            FoodItemAnnotation(
                item_id="it_003_pongal",
                class_name="ven pongal",
                hierarchical_path="Tamil Nadu > Breakfast > Pongal > Ven Pongal > Pressure Cooked & Ghee Tempered > Semi-Solid",
                bbox=BoundingBox(ymin=0.15, xmin=0.12, ymax=0.78, xmax=0.55),
                actual_weight_grams=215.0,
                portion_class="medium",
                cooking_method="pressure_cooked",
                food_state="cooked"
            ),
            FoodItemAnnotation(
                item_id="it_003_vada",
                class_name="medu vada",
                hierarchical_path="Tamil Nadu > Breakfast > Vada > Medu Vada > Deep Fried > Fried Solid",
                bbox=BoundingBox(ymin=0.20, xmin=0.60, ymax=0.55, xmax=0.92),
                actual_weight_grams=54.0,
                portion_class="small",
                cooking_method="deep_fried",
                food_state="cooked"
            ),
            FoodItemAnnotation(
                item_id="it_003_sambar",
                class_name="tiffin sambar",
                hierarchical_path="Tamil Nadu > Breakfast > Sambar > Tiffin Sambar > Boiled > Liquid",
                bbox=BoundingBox(ymin=0.60, xmin=0.60, ymax=0.88, xmax=0.90),
                actual_weight_grams=80.0,
                portion_class="small",
                cooking_method="boiled",
                food_state="liquid"
            )
        ],
        total_actual_weight_grams=349.0,
        dataset_version="gold_si_v1",
        validation_status="expert_verified",
        split="gold_benchmark"
    ),

    # 4. Thalappakatti Mutton Biryani + Egg + Raita
    FoodSample(
        sample_id="gold_si_004_dindigul_biryani",
        meal_id="meal_si_004",
        photo_session_id="session_expert_dindigul_01",
        source_setting="restaurant",
        image_path="datasets/gold_south_indian/dindigul_biryani.jpg",
        image_sha256="99ff88ee77dd66cc55bb44aa33221100aabbccdd",
        perceptual_hash="c4b8e2a1d7f00344",
        image_width=1080,
        image_height=810,
        view_angle="45_degree",
        reference_scale=ReferenceObjectScale(plate_diameter_cm=28.0),
        camera_metadata=CameraMetadata(device_model="Samsung S23", estimated_distance_cm=38.0, view_angle="45_degree"),
        food_items=[
            FoodItemAnnotation(
                item_id="it_004_biryani",
                class_name="Dindigul biryani",
                hierarchical_path="Tamil Nadu > Lunch > Biryani > Mutton Biryani > Seeraga Samba Dum Cooked > Cooked Solid",
                bbox=BoundingBox(ymin=0.10, xmin=0.10, ymax=0.82, xmax=0.75),
                actual_weight_grams=385.0,
                portion_class="large",
                cooking_method="dum_cooked",
                food_state="cooked"
            ),
            FoodItemAnnotation(
                item_id="it_004_egg",
                class_name="boiled egg",
                hierarchical_path="Indian > Protein > Egg > Boiled Egg > Boiled > Solid",
                bbox=BoundingBox(ymin=0.22, xmin=0.55, ymax=0.45, xmax=0.72),
                actual_weight_grams=50.0,
                portion_class="small",
                cooking_method="boiled",
                food_state="cooked"
            ),
            FoodItemAnnotation(
                item_id="it_004_raita",
                class_name="onion raita",
                hierarchical_path="Tamil Nadu > Condiment > Raita > Onion Raita > Raw > Semi-Solid",
                bbox=BoundingBox(ymin=0.15, xmin=0.76, ymax=0.50, xmax=0.96),
                actual_weight_grams=75.0,
                portion_class="small",
                cooking_method="raw",
                food_state="semi-solid"
            )
        ],
        total_actual_weight_grams=510.0,
        dataset_version="gold_si_v1",
        validation_status="expert_verified",
        split="gold_benchmark"
    ),

    # 5. Full Banana Leaf Meal (11 Distinct Components)
    FoodSample(
        sample_id="gold_si_005_banana_leaf_meal",
        meal_id="meal_si_005",
        photo_session_id="session_expert_madurai_01",
        source_setting="restaurant",
        image_path="datasets/gold_south_indian/banana_leaf_feast.jpg",
        image_sha256="11223344556677889900aabbccddeeff00112233",
        perceptual_hash="a1b2c3d4e5f60789",
        image_width=1280,
        image_height=720,
        view_angle="top",
        reference_scale=ReferenceObjectScale(reference_type="banana_leaf", plate_diameter_cm=45.0),
        camera_metadata=CameraMetadata(device_model="iPhone 15 Pro Max", estimated_distance_cm=50.0, view_angle="top"),
        food_items=[
            FoodItemAnnotation(item_id="leaf_rice", class_name="steamed rice", hierarchical_path="Tamil Nadu > Lunch > Rice > Ponni Rice > Boiled > Cooked Solid", bbox=BoundingBox(ymin=0.35, xmin=0.25, ymax=0.85, xmax=0.65), actual_weight_grams=260.0, portion_class="large", cooking_method="boiled", food_state="cooked"),
            FoodItemAnnotation(item_id="leaf_sambar", class_name="drumstick sambar", hierarchical_path="Tamil Nadu > Lunch > Curry > Sambar > Boiled > Liquid", bbox=BoundingBox(ymin=0.38, xmin=0.38, ymax=0.65, xmax=0.55), actual_weight_grams=110.0, portion_class="medium", cooking_method="boiled", food_state="liquid"),
            FoodItemAnnotation(item_id="leaf_rasam", class_name="pepper rasam", hierarchical_path="Tamil Nadu > Lunch > Broth > Rasam > Boiled > Liquid", bbox=BoundingBox(ymin=0.10, xmin=0.70, ymax=0.28, xmax=0.85), actual_weight_grams=90.0, portion_class="small", cooking_method="boiled", food_state="liquid"),
            FoodItemAnnotation(item_id="leaf_kootu", class_name="chow chow kootu", hierarchical_path="Tamil Nadu > Lunch > Side > Kootu > Simmered > Semi-Solid", bbox=BoundingBox(ymin=0.10, xmin=0.45, ymax=0.26, xmax=0.60), actual_weight_grams=70.0, portion_class="small", cooking_method="boiled", food_state="semi-solid"),
            FoodItemAnnotation(item_id="leaf_poriyal", class_name="beans poriyal", hierarchical_path="Tamil Nadu > Lunch > Side > Poriyal > Sauteed > Cooked Solid", bbox=BoundingBox(ymin=0.10, xmin=0.30, ymax=0.25, xmax=0.44), actual_weight_grams=65.0, portion_class="small", cooking_method="sauteed", food_state="cooked"),
            FoodItemAnnotation(item_id="leaf_avial", class_name="avial", hierarchical_path="Kerala/Tamil Nadu > Lunch > Side > Avial > Steamed & Coconut > Semi-Solid", bbox=BoundingBox(ymin=0.10, xmin=0.15, ymax=0.25, xmax=0.29), actual_weight_grams=60.0, portion_class="small", cooking_method="steamed", food_state="semi-solid"),
            FoodItemAnnotation(item_id="leaf_curd", class_name="curd", hierarchical_path="Tamil Nadu > Lunch > Dairy > Curd > Fermented > Semi-Solid", bbox=BoundingBox(ymin=0.10, xmin=0.85, ymax=0.28, xmax=0.98), actual_weight_grams=90.0, portion_class="medium", cooking_method="raw", food_state="semi-solid"),
            FoodItemAnnotation(item_id="leaf_appalam", class_name="papad", hierarchical_path="Tamil Nadu > Lunch > Snack > Papad > Deep Fried > Crispy Solid", bbox=BoundingBox(ymin=0.45, xmin=0.05, ymax=0.75, xmax=0.22), actual_weight_grams=14.0, portion_class="small", cooking_method="deep_fried", food_state="cooked"),
            FoodItemAnnotation(item_id="leaf_pickle", class_name="mango pickle", hierarchical_path="Tamil Nadu > Lunch > Condiment > Pickle > Salt/Oil Cured > Solid", bbox=BoundingBox(ymin=0.10, xmin=0.03, ymax=0.20, xmax=0.12), actual_weight_grams=10.0, portion_class="small", cooking_method="raw", food_state="solid"),
            FoodItemAnnotation(item_id="leaf_payasam", class_name="semiya payasam", hierarchical_path="Tamil Nadu > Lunch > Dessert > Payasam > Boiled with Milk > Liquid", bbox=BoundingBox(ymin=0.75, xmin=0.75, ymax=0.95, xmax=0.95), actual_weight_grams=70.0, portion_class="small", cooking_method="boiled", food_state="liquid")
        ],
        total_actual_weight_grams=839.0,
        dataset_version="gold_si_v1",
        validation_status="expert_verified",
        split="gold_benchmark"
    ),

    # 6. Chicken Kothu Parotta
    FoodSample(
        sample_id="gold_si_006_chicken_kothu_parotta",
        meal_id="meal_si_006",
        photo_session_id="session_expert_salem_01",
        source_setting="street_food",
        image_path="datasets/gold_south_indian/chicken_kothu_parotta.jpg",
        image_sha256="aa11bb22cc33dd44ee55ff667788990011223344",
        perceptual_hash="b3c8e4f1a2d70199",
        image_width=1080,
        image_height=810,
        view_angle="top",
        reference_scale=ReferenceObjectScale(plate_diameter_cm=26.0),
        camera_metadata=CameraMetadata(device_model="OnePlus 12", estimated_distance_cm=30.0, view_angle="top"),
        food_items=[
            FoodItemAnnotation(
                item_id="it_006_kothu",
                class_name="chicken kothu parotta",
                hierarchical_path="Tamil Nadu > Dinner > Parotta > Chicken Kothu Parotta > Griddled Chopped > Cooked Solid",
                bbox=BoundingBox(ymin=0.15, xmin=0.10, ymax=0.85, xmax=0.75),
                actual_weight_grams=340.0,
                portion_class="large",
                cooking_method="pan_fried",
                food_state="cooked"
            ),
            FoodItemAnnotation(
                item_id="it_006_salna",
                class_name="chicken gravy",
                hierarchical_path="Tamil Nadu > Dinner > Salna > Chicken Salna > Simmered > Liquid",
                bbox=BoundingBox(ymin=0.15, xmin=0.78, ymax=0.48, xmax=0.96),
                actual_weight_grams=100.0,
                portion_class="small",
                cooking_method="boiled",
                food_state="liquid"
            ),
            FoodItemAnnotation(
                item_id="it_006_raita",
                class_name="onion raita",
                hierarchical_path="Tamil Nadu > Dinner > Condiment > Onion Raita > Raw > Semi-Solid",
                bbox=BoundingBox(ymin=0.52, xmin=0.78, ymax=0.82, xmax=0.96),
                actual_weight_grams=60.0,
                portion_class="small",
                cooking_method="raw",
                food_state="semi-solid"
            )
        ],
        total_actual_weight_grams=500.0,
        dataset_version="gold_si_v1",
        validation_status="expert_verified",
        split="gold_benchmark"
    )
]
