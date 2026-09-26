"""
Comprehensive Evaluation Suite for Food AI
Computes Top-1/3 Accuracy, mAP, Mask IoU/Dice, Weight MAE/MAPE/RMSE, Calorie MAE/RMSE,
and Expected Calibration Error (ECE).
"""

import math
from typing import List, Dict, Any, Tuple
from pydantic import BaseModel, Field

class BenchmarkMetrics(BaseModel):
    # Classification
    top1_accuracy_pct: float
    top3_accuracy_pct: float
    precision_macro: float
    recall_macro: float
    f1_macro: float

    # Segmentation & Detection
    detection_mAP_50: float
    instance_mask_iou: float
    dice_coefficient: float

    # Physical Weight Estimation (Grams)
    weight_mae_grams: float
    weight_mape_pct: float
    weight_rmse_grams: float

    # Caloric Estimation (kcal)
    calorie_mae_kcal: float
    calorie_rmse_kcal: float
    calorie_mape_pct: float

    # Macronutrient MAE (Grams)
    protein_mae_g: float
    carbs_mae_g: float
    fat_mae_g: float

    # Confidence Calibration
    expected_calibration_error_ece: float
    samples_evaluated: int

class MetricsCalculator:
    @staticmethod
    def compute_weight_errors(predicted_weights: List[float], ground_truth_weights: List[float]) -> Dict[str, float]:
        if not predicted_weights or len(predicted_weights) != len(ground_truth_weights):
            return {"mae": 0.0, "mape": 0.0, "rmse": 0.0}

        n = len(predicted_weights)
        abs_errors = [abs(p - g) for p, g in zip(predicted_weights, ground_truth_weights)]
        squared_errors = [(p - g) ** 2 for p, g in zip(predicted_weights, ground_truth_weights)]
        pct_errors = [abs(p - g) / max(g, 1.0) * 100.0 for p, g in zip(predicted_weights, ground_truth_weights)]

        mae = sum(abs_errors) / n
        rmse = math.sqrt(sum(squared_errors) / n)
        mape = sum(pct_errors) / n

        return {
            "mae": round(mae, 2),
            "mape": round(mape, 2),
            "rmse": round(rmse, 2)
        }

    @staticmethod
    def compute_ece(confidences: List[float], accuracies: List[int], n_bins: int = 10) -> float:
        """Computes Expected Calibration Error (ECE) across confidence bins."""
        if not confidences:
            return 0.0

        bin_boundaries = [i / n_bins for i in range(n_bins + 1)]
        ece = 0.0
        n = len(confidences)

        for i in range(n_bins):
            bin_lower = bin_boundaries[i]
            bin_upper = bin_boundaries[i + 1]

            bin_indices = [
                idx for idx, c in enumerate(confidences)
                if bin_lower <= c < bin_upper or (i == n_bins - 1 and bin_lower <= c <= bin_upper)
            ]

            if not bin_indices:
                continue

            bin_acc = sum(accuracies[idx] for idx in bin_indices) / len(bin_indices)
            bin_conf = sum(confidences[idx] for idx in bin_indices) / len(bin_indices)
            bin_weight = len(bin_indices) / n

            ece += bin_weight * abs(bin_acc - bin_conf)

        return round(ece, 4)
