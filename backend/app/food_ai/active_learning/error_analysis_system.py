"""
Error Analysis System, Active Learning Review Queue, & User Feedback Loop
Implements Sections 49, 51, 52, and 53 of Part 3.
Guarantees:
- 9 discrete error types categorized and tracked
- Dedicated Hard Example Mining Dataset
- Automated active learning review queue
- Validated user feedback loops (never blindly retrained)
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from enum import Enum
from pydantic import BaseModel, Field

# =============================================================================
# SECTION 51 — 9 ERROR TYPES & STRUCTURED ERROR ANALYSIS RECORD
# =============================================================================

class FoodAIErrorType(str, Enum):
    VISUAL_SIMILARITY = "visual_similarity"
    INSUFFICIENT_TRAINING_DATA = "insufficient_training_data"
    POOR_IMAGE_QUALITY = "poor_image_quality"
    OCCLUSION = "occlusion"
    WRONG_LABEL = "wrong_label"
    CLASS_OVERLAP = "class_overlap"
    RECIPE_VARIATION = "recipe_variation"
    PORTION_ERROR = "portion_error"
    UNKNOWN_FOOD = "unknown_food"

class ErrorAnalysisRecord(BaseModel):
    error_id: str
    image_id: str
    actual_class: str
    predicted_class: str
    confidence: float
    model_version: str
    error_type: FoodAIErrorType
    lighting_condition: str
    view_angle: str
    occlusion_level_pct: float
    portion_error_grams: Optional[float] = None
    background_type: str
    root_cause_explanation: str
    logged_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

# =============================================================================
# SECTION 49 — HARD-EXAMPLE MINING DATASET
# =============================================================================

class HardExampleRecord(BaseModel):
    hard_example_id: str
    image_hash: str
    true_food_id: str
    confused_with_food_id: str
    observed_loss: float
    error_cluster: str # idli_errors, sambar_errors, chutney_errors, dosa_errors, rice_errors, biryani_errors, nonveg_errors
    priority_retrain_weight: float = Field(default=2.5, description="Loss multiplier during retraining")

# =============================================================================
# SECTION 52 & 53 — ACTIVE LEARNING & USER CORRECTION PIPELINE
# =============================================================================

class UserCorrectionFeedback(BaseModel):
    correction_id: str
    image_id: str
    model_version: str
    original_prediction: str
    corrected_prediction: str
    corrected_variant: Optional[str] = None
    corrected_portion_count: Optional[int] = None
    corrected_weight_grams: Optional[float] = None
    feedback_reason: str = Field(default="Wrong food", description="Change food, Change variant, Change quantity, Change weight, Change ingredients, Wrong food")
    validation_status: str = Field(default="pending_review", description="pending_review, approved_by_expert, rejected_spam")
    submitted_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class ActiveLearningReviewQueue:
    def __init__(self):
        self.review_queue: List[Dict[str, Any]] = []
        self.error_records: List[ErrorAnalysisRecord] = []
        self.hard_example_dataset: List[HardExampleRecord] = []
        self.user_corrections: List[UserCorrectionFeedback] = []

    def evaluate_for_active_learning(
        self,
        image_id: str,
        image_hash: str,
        predicted_class: str,
        confidence: float,
        is_unknown: bool,
        high_confusion_pair: Optional[str] = None
    ) -> bool:
        """
        SECTION 52: Automatically enqueues low-confidence, high-confusion, or unknown dishes.
        """
        reasons: List[str] = []
        if confidence < 0.80:
            reasons.append("low_confidence (<0.80)")
        if is_unknown:
            reasons.append("unknown_food_discovered")
        if high_confusion_pair:
            reasons.append(f"high_confusion_pair ({high_confusion_pair})")

        if reasons:
            self.review_queue.append({
                "queue_id": f"q_{len(self.review_queue) + 1:04d}",
                "image_id": image_id,
                "image_hash": image_hash,
                "predicted_class": predicted_class,
                "confidence": confidence,
                "reasons": reasons,
                "enqueued_at": datetime.now(timezone.utc).isoformat()
            })
            return True
        return False

    def log_error(
        self,
        image_id: str,
        actual: str,
        predicted: str,
        confidence: float,
        model_version: str,
        error_type: FoodAIErrorType,
        explanation: str
    ) -> ErrorAnalysisRecord:
        record = ErrorAnalysisRecord(
            error_id=f"err_{len(self.error_records) + 1:04d}",
            image_id=image_id,
            actual_class=actual,
            predicted_class=predicted,
            confidence=confidence,
            model_version=model_version,
            error_type=error_type,
            lighting_condition="standard_ambient",
            view_angle="top_45_deg",
            occlusion_level_pct=0.0,
            background_type="restaurant_table",
            root_cause_explanation=explanation
        )
        self.error_records.append(record)
        return record

    def record_user_correction(
        self,
        image_id: str,
        original_prediction: str,
        corrected_prediction: str,
        model_version: str,
        feedback_reason: str = "Change food"
    ) -> UserCorrectionFeedback:
        """
        SECTION 53: Validated feedback loops.
        Never retrains immediately; stores for expert validation first.
        """
        feedback = UserCorrectionFeedback(
            correction_id=f"corr_{len(self.user_corrections) + 1:04d}",
            image_id=image_id,
            model_version=model_version,
            original_prediction=original_prediction,
            corrected_prediction=corrected_prediction,
            feedback_reason=feedback_reason,
            validation_status="pending_review"
        )
        self.user_corrections.append(feedback)
        return feedback

error_analysis_hub = ActiveLearningReviewQueue()
