"""
Hard Example Mining Module
Automatically flags and filters difficult samples (high loss, misclassified pairs,
severe weight/calorie errors, or low confidence) into hard_examples_vX for targeted retraining.
"""

from typing import List, Dict, Any
from pydantic import BaseModel, Field

class HardSampleRecord(BaseModel):
    sample_id: str
    ground_truth_dish: str
    predicted_dish: str
    ground_truth_weight_g: float
    predicted_weight_g: float
    weight_error_pct: float
    ground_truth_calories: float
    predicted_calories: float
    calorie_error_pct: float
    confidence_score: float
    mining_reason: str # "frequent_confusion", "large_weight_error", "low_confidence", "misclassification"

class HardExampleMiner:
    CONFIDENCE_THRESHOLD = 0.65
    WEIGHT_ERROR_PCT_THRESHOLD = 20.0
    CALORIE_ERROR_PCT_THRESHOLD = 25.0

    @staticmethod
    def identify_hard_examples(evaluation_logs: List[Dict[str, Any]]) -> List[HardSampleRecord]:
        hard_samples: List[HardSampleRecord] = []

        for log in evaluation_logs:
            reasons = []
            gt_dish = log.get("ground_truth_dish", "")
            pred_dish = log.get("predicted_dish", "")
            gt_w = float(log.get("ground_truth_weight_g", 1.0))
            pred_w = float(log.get("predicted_weight_g", 0.0))
            gt_cals = float(log.get("ground_truth_calories", 1.0))
            pred_cals = float(log.get("predicted_calories", 0.0))
            conf = float(log.get("confidence", 1.0))

            w_err = abs(pred_w - gt_w) / max(gt_w, 1.0) * 100.0
            cal_err = abs(pred_cals - gt_cals) / max(gt_cals, 1.0) * 100.0

            if gt_dish != pred_dish:
                reasons.append(f"Misclassified: {gt_dish} -> {pred_dish}")
            if conf < HardExampleMiner.CONFIDENCE_THRESHOLD:
                reasons.append(f"Low confidence ({conf:.2f} < {HardExampleMiner.CONFIDENCE_THRESHOLD})")
            if w_err > HardExampleMiner.WEIGHT_ERROR_PCT_THRESHOLD:
                reasons.append(f"Weight error ({w_err:.1f}% > {HardExampleMiner.WEIGHT_ERROR_PCT_THRESHOLD}%)")
            if cal_err > HardExampleMiner.CALORIE_ERROR_PCT_THRESHOLD:
                reasons.append(f"Calorie error ({cal_err:.1f}% > {HardExampleMiner.CALORIE_ERROR_PCT_THRESHOLD}%)")

            if reasons:
                hard_samples.append(HardSampleRecord(
                    sample_id=log.get("sample_id", "unknown"),
                    ground_truth_dish=gt_dish,
                    predicted_dish=pred_dish,
                    ground_truth_weight_g=gt_w,
                    predicted_weight_g=pred_w,
                    weight_error_pct=round(w_err, 1),
                    ground_truth_calories=gt_cals,
                    predicted_calories=pred_cals,
                    calorie_error_pct=round(cal_err, 1),
                    confidence_score=round(conf, 3),
                    mining_reason="; ".join(reasons)
                ))

        return hard_samples
