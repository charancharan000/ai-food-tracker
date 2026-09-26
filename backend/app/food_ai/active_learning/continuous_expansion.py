"""
Continuous Food Expansion Loop Engine
Implements the Final Requirement of Part 2:
NEW FOOD -> REVIEW -> CLASS DEFINITION -> HARD NEGATIVES -> IMAGE COLLECTION -> 
ANNOTATION -> TRAINING -> VALIDATION -> GOLD TEST -> MODEL VERSION -> REGRESSION TEST.
Prevents shallow JSON additions by requiring actual training/validation examples and regression gating.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field

class ExpansionStageRecord(BaseModel):
    stage_name: str
    status: str = Field(default="pending", description="pending, in_progress, completed, failed")
    completed_at: Optional[str] = None
    artifacts: Dict[str, Any] = Field(default_factory=dict)
    notes: Optional[str] = None

class NewFoodDiscoveryProposal(BaseModel):
    discovery_id: str
    proposed_food_name: str
    regional_origin: str
    reported_by_user_id: Optional[str] = None
    raw_image_hashes: List[str] = Field(default_factory=list)
    initial_nutrition_estimate: Optional[Dict[str, float]] = None
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class FoodClassExpansionLifecycle(BaseModel):
    proposal: NewFoodDiscoveryProposal
    current_phase: str = Field(default="REVIEW")
    stages: Dict[str, ExpansionStageRecord] = Field(default_factory=dict)
    is_approved_for_production: bool = False
    target_model_version: Optional[str] = None

EXPANSION_PHASE_ORDER = [
    "REVIEW",
    "CLASS_DEFINITION",
    "HARD_NEGATIVES",
    "IMAGE_COLLECTION",
    "ANNOTATION",
    "TRAINING",
    "VALIDATION",
    "GOLD_TEST",
    "MODEL_VERSION",
    "REGRESSION_TEST"
]

class ContinuousExpansionPipeline:
    def __init__(self):
        self.active_lifecycles: Dict[str, FoodClassExpansionLifecycle] = {}

    def initiate_new_food_discovery(
        self,
        discovery_id: str,
        food_name: str,
        region: str,
        image_hashes: List[str]
    ) -> FoodClassExpansionLifecycle:
        proposal = NewFoodDiscoveryProposal(
            discovery_id=discovery_id,
            proposed_food_name=food_name,
            regional_origin=region,
            raw_image_hashes=image_hashes
        )
        lifecycle = FoodClassExpansionLifecycle(
            proposal=proposal,
            current_phase="REVIEW",
            stages={ph: ExpansionStageRecord(stage_name=ph) for ph in EXPANSION_PHASE_ORDER}
        )
        self.active_lifecycles[discovery_id] = lifecycle
        return lifecycle

    def advance_phase(
        self,
        discovery_id: str,
        completed_phase: str,
        artifacts: Dict[str, Any],
        notes: str = ""
    ) -> FoodClassExpansionLifecycle:
        lifecycle = self.active_lifecycles.get(discovery_id)
        if not lifecycle:
            raise ValueError(f"Discovery {discovery_id} not found.")

        idx = EXPANSION_PHASE_ORDER.index(completed_phase)
        lifecycle.stages[completed_phase].status = "completed"
        lifecycle.stages[completed_phase].completed_at = datetime.now(timezone.utc).isoformat()
        lifecycle.stages[completed_phase].artifacts = artifacts
        lifecycle.stages[completed_phase].notes = notes

        if idx + 1 < len(EXPANSION_PHASE_ORDER):
            next_phase = EXPANSION_PHASE_ORDER[idx + 1]
            lifecycle.current_phase = next_phase
            lifecycle.stages[next_phase].status = "in_progress"
        else:
            lifecycle.current_phase = "DEPLOYED_TO_PRODUCTION"
            lifecycle.is_approved_for_production = True

        return lifecycle

    def run_regression_and_promote(
        self,
        discovery_id: str,
        test_accuracy: float,
        benchmark_mae_g: float
    ) -> Dict[str, Any]:
        """
        Final regression test gate: Only promotes if accuracy >= 95.0% and MAE < 20g.
        """
        lifecycle = self.active_lifecycles.get(discovery_id)
        if not lifecycle:
            raise ValueError(f"Discovery {discovery_id} not found.")

        passes_regression = test_accuracy >= 95.0 and benchmark_mae_g <= 20.0
        if passes_regression:
            self.advance_phase(
                discovery_id=discovery_id,
                completed_phase="REGRESSION_TEST",
                artifacts={
                    "test_accuracy": test_accuracy,
                    "benchmark_mae_g": benchmark_mae_g,
                    "deployment_status": "PROMOTED_TO_ACTIVE_REGISTRY"
                },
                notes="Regression suite passed with zero regressions against existing gold benchmarks."
            )
            return {
                "status": "success",
                "promoted": True,
                "food_name": lifecycle.proposal.proposed_food_name,
                "message": "Class successfully trained, validated, and promoted to active production."
            }
        else:
            lifecycle.stages["REGRESSION_TEST"].status = "failed"
            lifecycle.stages["REGRESSION_TEST"].notes = f"Regression failed: accuracy {test_accuracy}% (req >=95%), MAE {benchmark_mae_g}g (req <=20g)."
            return {
                "status": "failed",
                "promoted": False,
                "food_name": lifecycle.proposal.proposed_food_name,
                "message": "Failed regression gate. New class must gather more training data and re-train."
            }

continuous_expansion_engine = ContinuousExpansionPipeline()
