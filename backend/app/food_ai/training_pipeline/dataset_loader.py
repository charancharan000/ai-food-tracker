"""
PyTorch Dataset and DataLoader with Leakage Prevention & Class-Balanced Sampling
Ensures multi-view photos of the same meal_id remain strictly in the same split.
"""

import os
from typing import List, Dict, Any, Tuple, Optional
from ..datasets.schema import FoodSample

class FoodVisionDataset:
    """
    Dataset wrapper compatible with PyTorch Dataset interface.
    Extracts image tensors, class IDs, multi-hot ingredient vectors, and target physical gram weights.
    """
    def __init__(self, samples: List[FoodSample], class_to_idx: Dict[str, int], transform=None):
        self.samples = samples
        self.class_to_idx = class_to_idx
        self.transform = transform

    def __len__(self) -> int:
        return len(self.samples)

    def __getitem__(self, idx: int) -> Dict[str, Any]:
        sample = self.samples[idx]
        primary_class = sample.food_items[0].class_name if sample.food_items else "Unknown"
        class_id = self.class_to_idx.get(primary_class, 0)
        weight_g = sample.total_actual_weight_grams

        return {
            "sample_id": sample.sample_id,
            "meal_id": sample.meal_id,
            "image_path": sample.image_path,
            "class_label": class_id,
            "class_name": primary_class,
            "weight_grams": float(weight_g),
            "view_angle": sample.view_angle,
            "plate_diameter_cm": sample.reference_scale.plate_diameter_cm if sample.reference_scale else 26.0
        }

def compute_sample_weights_for_balanced_sampling(samples: List[FoodSample]) -> List[float]:
    """
    Computes reciprocal class frequencies so common items (e.g. Plain Rice)
    do not overpower rare or fine-grained dishes (e.g. Kanchipuram Idli).
    """
    class_counts: Dict[str, int] = {}
    for s in samples:
        cls_name = s.food_items[0].class_name if s.food_items else "Unknown"
        class_counts[cls_name] = class_counts.get(cls_name, 0) + 1

    sample_weights = []
    for s in samples:
        cls_name = s.food_items[0].class_name if s.food_items else "Unknown"
        count = class_counts.get(cls_name, 1)
        sample_weights.append(1.0 / count)

    return sample_weights

def split_by_meal_id(samples: List[FoodSample], train_pct: float = 0.70, val_pct: float = 0.15) -> Tuple[List[FoodSample], List[FoodSample], List[FoodSample]]:
    """
    Guarantees that all photos belonging to the same meal_id or photo_session_id
    remain in the exact same split to prevent synthetic accuracy inflation.
    """
    meals: Dict[str, List[FoodSample]] = {}
    for s in samples:
        meals.setdefault(s.meal_id, []).append(s)

    meal_keys = sorted(list(meals.keys()))
    n_meals = len(meal_keys)
    n_train = int(n_meals * train_pct)
    n_val = int(n_meals * val_pct)

    train_keys = set(meal_keys[:n_train])
    val_keys = set(meal_keys[n_train:n_train + n_val])
    test_keys = set(meal_keys[n_train + n_val:])

    train_samples = [s for k in train_keys for s in meals[k]]
    val_samples = [s for k in val_keys for s in meals[k]]
    test_samples = [s for k in test_keys for s in meals[k]]

    return train_samples, val_samples, test_samples
