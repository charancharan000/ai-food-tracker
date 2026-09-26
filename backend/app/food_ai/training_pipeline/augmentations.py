"""
Identity-Preserving Food Augmentation Pipeline
Applies realistic mobile phone perspective shifts, lighting changes, slight steam blur,
and dish rotation while strictly avoiding identity-altering color inversions.
"""

from typing import Dict, Any

class FoodAugmentationPlan:
    """
    Specifies Albumentations / Torchvision transforms configured specifically for food photography.
    """
    TRAIN_PIPELINE = [
        {"name": "RandomResizedCrop", "size": (384, 384), "scale": (0.8, 1.0)},
        {"name": "HorizontalFlip", "p": 0.5},
        {"name": "ShiftScaleRotate", "shift_limit": 0.05, "scale_limit": 0.1, "rotate_limit": 25, "p": 0.6},
        {"name": "Perspective", "scale": (0.02, 0.08), "p": 0.4}, # Simulates camera tilt
        {"name": "ColorJitter", "brightness": 0.15, "contrast": 0.15, "saturation": 0.10, "hue": 0.03, "p": 0.5},
        {"name": "GaussianBlur", "blur_limit": (3, 5), "p": 0.2}, # Simulates soft focus / kitchen steam
        {"name": "CoarseDropout", "max_holes": 4, "max_height": 32, "max_width": 32, "p": 0.3}, # Simulates partial occlusion
        {"name": "Normalize", "mean": [0.485, 0.456, 0.406], "std": [0.229, 0.224, 0.225]}
    ]

    VAL_PIPELINE = [
        {"name": "Resize", "size": (384, 384)},
        {"name": "Normalize", "mean": [0.485, 0.456, 0.406], "std": [0.229, 0.224, 0.225]}
    ]
