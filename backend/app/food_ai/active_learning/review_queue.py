"""
Active Learning Review Queue & User Correction Triage
Collects uncertain predictions, out-of-distribution detections, and user corrections.
Quarantines unverified corrections until human expert validation before dataset ingestion.
"""

import time
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

class ReviewQueueItem(BaseModel):
    queue_id: str
    image_uri: str
    predicted_class: str
    predicted_weight_g: float
    model_version: str
    confidence: float
    
    # User feedback / correction if submitted
    user_suggested_dish: Optional[str] = None
    user_confirmed_weight_g: Optional[float] = None
    
    triage_reason: str # "low_confidence", "ood_unknown_food", "user_correction", "high_weight_discrepancy"
    status: str = "pending_review" # "pending_review", "approved_for_training", "rejected_bad_quality"
    reviewer_notes: Optional[str] = None
    created_at: str = Field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))

class ActiveLearningQueue:
    _queue: List[ReviewQueueItem] = []

    @classmethod
    def add_to_queue(
        cls,
        image_uri: str,
        predicted_class: str,
        predicted_weight_g: float,
        model_version: str,
        confidence: float,
        triage_reason: str,
        user_suggested_dish: Optional[str] = None,
        user_confirmed_weight_g: Optional[float] = None
    ) -> ReviewQueueItem:
        item = ReviewQueueItem(
            queue_id=f"rev_{int(time.time() * 1000)}",
            image_uri=image_uri,
            predicted_class=predicted_class,
            predicted_weight_g=predicted_weight_g,
            model_version=model_version,
            confidence=confidence,
            triage_reason=triage_reason,
            user_suggested_dish=user_suggested_dish,
            user_confirmed_weight_g=user_confirmed_weight_g
        )
        cls._queue.append(item)
        return item

    @classmethod
    def get_pending_items(cls) -> List[ReviewQueueItem]:
        return [it for it in cls._queue if it.status == "pending_review"]

    @classmethod
    def review_item(cls, queue_id: str, approve: bool, verified_dish: Optional[str] = None, verified_weight_g: Optional[float] = None, notes: str = "") -> Optional[ReviewQueueItem]:
        for it in cls._queue:
            if it.queue_id == queue_id:
                it.status = "approved_for_training" if approve else "rejected_bad_quality"
                it.reviewer_notes = notes
                if verified_dish:
                    it.user_suggested_dish = verified_dish
                if verified_weight_g:
                    it.user_confirmed_weight_g = verified_weight_g
                return it
        return None
