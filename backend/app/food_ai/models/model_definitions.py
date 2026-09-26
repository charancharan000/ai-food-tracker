"""
Model Architecture Definitions for the 13 Specialized Food AI Models
Each task is isolated in a modular component to avoid destructive gradient interference.
"""

from typing import Dict, List, Any, Optional, Tuple
from pydantic import BaseModel, Field

class QualityAssessmentResult(BaseModel):
    is_acceptable: bool
    blur_score: float
    brightness_score: float
    framing_score: float
    feedback: str

class DetectionResult(BaseModel):
    box_normalized: List[float] # [ymin, xmin, ymax, xmax]
    class_label: str
    confidence: float
    polygon_points: Optional[List[List[float]]] = None

class IngredientPrediction(BaseModel):
    ingredient_name: str
    probability: float
    status: str # "present", "absent", "uncertain"

class WeightPrediction(BaseModel):
    estimated_grams: float
    min_grams: float
    max_grams: float
    confidence: float
    estimation_method: str # "reference_scaled_volume", "multi_view_density", "single_view_prior"

class CalibratedResult(BaseModel):
    raw_confidence: float
    calibrated_confidence: float
    temperature: float = 1.25

# Abstract base & implementation specs for the 13 models
class ModelArchitectureSpecs:
    """Specifications for neural network backbones across all 13 specialized components."""
    
    # Model 1: Image Quality Classifier
    MODEL_1_QUALITY = {
        "model_id": "model_1_quality_assessor",
        "backbone": "mobilenet_v3_small",
        "input_resolution": (224, 224),
        "outputs": ["blur_metric", "exposure_metric", "food_centered_metric"],
        "loss": "MSELoss + BCEWithLogitsLoss"
    }

    # Model 2: Food / Non-Food Binary Classifier
    MODEL_2_FOOD_NONFOOD = {
        "model_id": "model_2_food_nonfood",
        "backbone": "efficientnet_b0",
        "input_resolution": (224, 224),
        "classes": ["Non-Food", "Food"],
        "loss": "BCEWithLogitsLoss"
    }

    # Model 3: Food Object Detector
    MODEL_3_DETECTOR = {
        "model_id": "model_3_food_detector",
        "architecture": "YOLOv8-Small / Faster R-CNN",
        "anchor_scales": [32, 64, 128, 256],
        "target": "Localizes bounding boxes of all distinct meal items on plate"
    }

    # Model 4: Food Instance Segmentation Model
    MODEL_4_SEGMENTER = {
        "model_id": "model_4_instance_segmenter",
        "architecture": "Mask R-CNN / SegFormer-B2",
        "mask_resolution": (28, 28),
        "target": "Accurate pixel boundaries separating rice, gravies, curries, and breads"
    }

    # Model 5: Fine-Grained Food Classifier (with Dedicated South Indian Branch)
    MODEL_5_FINE_GRAINED = {
        "model_id": "model_5_fine_grained_classifier",
        "backbone": "convnext_small / swin_transformer_v2",
        "input_resolution": (384, 384),
        "branches": {
            "global_food": 120,
            "south_indian_specialized": 95,
            "biryani_fine_grained": 15
        },
        "loss": "CrossEntropyLoss with label smoothing (0.1) + ArcFace margin"
    }

    # Model 6: Cuisine / Region Classifier
    MODEL_6_CUISINE = {
        "model_id": "model_6_cuisine_region",
        "backbone": "efficientnet_b2",
        "classes": ["Tamil Nadu", "Kerala", "Karnataka", "Andhra/Telangana", "North Indian", "Continental", "East Asian"],
        "loss": "CrossEntropyLoss"
    }

    # Model 7: Ingredient Recognition Multi-Label Model
    MODEL_7_INGREDIENTS = {
        "model_id": "model_7_ingredient_multilabel",
        "backbone": "resnet50_multi_label",
        "loss": "AsymmetricLoss (ASL) for extreme multi-label positive/negative imbalance"
    }

    # Model 8: Cooking Method Classifier
    MODEL_8_COOKING_METHOD = {
        "model_id": "model_8_cooking_method",
        "classes": ["steamed", "pan_fried", "deep_fried", "boiled", "pressure_cooked", "roasted", "raw"],
        "loss": "CrossEntropyLoss"
    }

    # Model 9: Raw / Cooked State Classifier
    MODEL_9_RAW_COOKED = {
        "model_id": "model_9_raw_cooked_state",
        "classes": ["raw", "cooked", "fermented", "processed"],
        "loss": "CrossEntropyLoss"
    }

    # Model 10: Portion Category Estimator
    MODEL_10_PORTION = {
        "model_id": "model_10_portion_estimator",
        "classes": ["small", "medium", "large"],
        "loss": "OrdinalRegressionLoss"
    }

    # Model 11: Scale-Calibrated Weight Estimation Model
    MODEL_11_WEIGHT = {
        "model_id": "model_11_physical_weight_regressor",
        "inputs": ["segmentation_mask_area_pixels", "plate_reference_diameter_pixels", "estimated_depth_map", "food_density_prior_g_cm3"],
        "loss": "SmoothL1Loss + MAPELoss",
        "target": "Direct physical weight in grams with standard error"
    }

    # Model 12: Nutrition Retrieval & Recipe Matching Model
    MODEL_12_NUTRITION_RETRIEVAL = {
        "model_id": "model_12_nutrition_recipe_matcher",
        "database": "IFCT_2017 + USDA + Verified Recipe Templates",
        "matching_strategy": "Embedding cosine similarity + Recipe variation interpolation"
    }

    # Model 13: Uncertainty & Confidence Calibration Model
    MODEL_13_CALIBRATION = {
        "model_id": "model_13_confidence_calibrator",
        "method": "Temperature Scaling on validation logits",
        "target": "Ensures an 85% reported confidence actually corresponds to 85% empirical accuracy"
    }
