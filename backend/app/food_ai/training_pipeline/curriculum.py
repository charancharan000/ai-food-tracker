"""
Progressive Training Curriculum Schedule
Orchestrates the 9-stage progressive training from coarse visual concepts to physical weight regression.
"""

from typing import List, Dict, Any
from pydantic import BaseModel, Field

class CurriculumStage(BaseModel):
    stage_number: int
    stage_name: str
    target_tasks: List[str]
    frozen_layers: List[str]
    active_loss_functions: List[str]
    recommended_epochs: int
    learning_rate: float

CURRICULUM_STAGES: List[CurriculumStage] = [
    CurriculumStage(
        stage_number=1,
        stage_name="Food vs Non-Food Binary Pretraining",
        target_tasks=["Binary Food Filter"],
        frozen_layers=[],
        active_loss_functions=["BCEWithLogitsLoss"],
        recommended_epochs=5,
        learning_rate=5e-4
    ),
    CurriculumStage(
        stage_number=2,
        stage_name="Broad Category Learning",
        target_tasks=["Rice", "Tiffin", "Curry", "Dry Fry", "Bread", "Beverage"],
        frozen_layers=[],
        active_loss_functions=["CrossEntropyLoss"],
        recommended_epochs=5,
        learning_rate=3e-4
    ),
    CurriculumStage(
        stage_number=3,
        stage_name="Regional Cuisine Discrimination",
        target_tasks=["Tamil Nadu", "Kerala", "Karnataka", "Andhra", "North Indian", "Continental"],
        frozen_layers=["backbone.stem", "backbone.layer1"],
        active_loss_functions=["CrossEntropyLoss"],
        recommended_epochs=4,
        learning_rate=2e-4
    ),
    CurriculumStage(
        stage_number=4,
        stage_name="Fine-Grained Dish Classification",
        target_tasks=["120+ Tamil & Indian Dish Classes (Idli variants, Dosa variants, Biryanis)"],
        frozen_layers=["backbone.stem"],
        active_loss_functions=["CrossEntropyLoss_LabelSmoothed", "ArcFaceMargin"],
        recommended_epochs=8,
        learning_rate=1e-4
    ),
    CurriculumStage(
        stage_number=5,
        stage_name="Hard Confusing Class Disambiguation",
        target_tasks=["Biryani vs Fried Rice", "Idli vs Dhokla", "Pongal vs Upma"],
        frozen_layers=[],
        active_loss_functions=["TripletMarginLoss", "CrossEntropyLoss"],
        recommended_epochs=5,
        learning_rate=5e-5
    ),
    CurriculumStage(
        stage_number=6,
        stage_name="Multi-Label Ingredient Recognition",
        target_tasks=["Lentils", "Spices", "Oils", "Vegetable pieces", "Proteins"],
        frozen_layers=["backbone.stem", "backbone.layer1"],
        active_loss_functions=["AsymmetricLoss"],
        recommended_epochs=4,
        learning_rate=1e-4
    ),
    CurriculumStage(
        stage_number=7,
        stage_name="Portion Sizing Classification",
        target_tasks=["Small (1 serving)", "Medium (2 servings)", "Large (3+ servings)"],
        frozen_layers=[],
        active_loss_functions=["OrdinalLoss"],
        recommended_epochs=4,
        learning_rate=1e-4
    ),
    CurriculumStage(
        stage_number=8,
        stage_name="Physical Weight Regression in Grams",
        target_tasks=["Scale-Calibrated Continuous Gram Prediction"],
        frozen_layers=["classification_head"],
        active_loss_functions=["SmoothL1Loss", "MAPELoss"],
        recommended_epochs=6,
        learning_rate=8e-5
    ),
    CurriculumStage(
        stage_number=9,
        stage_name="Full End-to-End Joint Fine-Tuning & Calibration",
        target_tasks=["Joint Multitask Inference", "Temperature Scaling"],
        frozen_layers=[],
        active_loss_functions=["JointWeightedMultiLoss"],
        recommended_epochs=4,
        learning_rate=3e-5
    )
]
