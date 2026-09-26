"""
Hierarchical Curriculum Learning & Training Priority Scheduler
Implements Section 38 and Section 39 of Part 2.
Controls the 12-stage progressive training sequence and priority gates.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class CurriculumStageSpec(BaseModel):
    stage_number: int
    stage_name: str
    target_objective: str
    loss_function: str
    active_heads: List[str]
    convergence_metric: str
    target_threshold: float
    description: str

class TrainingPriorityGroup(BaseModel):
    priority_level: int
    group_name: str
    classes: List[str]
    min_required_samples_per_class: int
    hard_negative_pairs: List[str]

# =============================================================================
# SECTION 38 — TRAINING PRIORITY SCHEDULE
# =============================================================================

TRAINING_PRIORITY_SCHEDULE: Dict[int, TrainingPriorityGroup] = {
    1: TrainingPriorityGroup(
        priority_level=1,
        group_name="Core Breakfast & Staples",
        classes=["idli", "sambar", "chutney", "dosa", "vada", "rice"],
        min_required_samples_per_class=500,
        hard_negative_pairs=["idli_vs_dhokla", "dosa_vs_crepe", "medu_vada_vs_bonda", "coconut_vs_peanut_chutney"]
    ),
    2: TrainingPriorityGroup(
        priority_level=2,
        group_name="Secondary Breakfast & Biryanis",
        classes=["pongal", "upma", "poori", "parotta", "kothu_parotta", "biryani", "rasam"],
        min_required_samples_per_class=350,
        hard_negative_pairs=["pongal_vs_upma", "poori_vs_bhatura", "biryani_vs_fried_rice", "kothu_vs_noodles"]
    ),
    3: TrainingPriorityGroup(
        priority_level=3,
        group_name="Vegetables, Sides & Gravies",
        classes=["poriyal", "kootu", "avial", "keerai", "kuzhambu"],
        min_required_samples_per_class=250,
        hard_negative_pairs=["poriyal_vs_stir_fry", "kootu_vs_dal", "sambar_vs_rasam"]
    ),
    4: TrainingPriorityGroup(
        priority_level=4,
        group_name="Non-Vegetarian Proteins",
        classes=["chicken", "mutton", "fish", "egg", "prawn", "crab"],
        min_required_samples_per_class=200,
        hard_negative_pairs=["chicken_vs_mutton", "fish_vs_chicken", "prawn_vs_diced_chicken"]
    ),
    5: TrainingPriorityGroup(
        priority_level=5,
        group_name="Savory Snacks, Sweets & Hyper-Regional",
        classes=["bajji", "pakoda", "murukku", "kesari", "payasam", "halwa", "mysore_pak", "regional_specialties"],
        min_required_samples_per_class=150,
        hard_negative_pairs=["paruppu_vada_vs_pakoda", "sweet_pongal_vs_rice_pudding"]
    )
}

# =============================================================================
# SECTION 39 — 12-STAGE HIERARCHICAL CURRICULUM PIPELINE
# =============================================================================

TWELVE_STAGE_CURRICULUM: List[CurriculumStageSpec] = [
    CurriculumStageSpec(
        stage_number=1,
        stage_name="food_vs_non_food",
        target_objective="Binary food existence filtering",
        loss_function="BinaryCrossEntropy",
        active_heads=["binary_food_head"],
        convergence_metric="f1_score",
        target_threshold=0.99,
        description="Filters out empty plates, utensils, hands, tables, and non-edible objects before running food AI."
    ),
    CurriculumStageSpec(
        stage_number=2,
        stage_name="single_vs_multiple_foods",
        target_objective="Detect single item vs multi-food composite plate",
        loss_function="BinaryCrossEntropy",
        active_heads=["composition_head"],
        convergence_metric="accuracy",
        target_threshold=0.97,
        description="Branches input into single-crop analyzer or initiates multi-box instance decomposition."
    ),
    CurriculumStageSpec(
        stage_number=3,
        stage_name="food_category",
        target_objective="High-level category classification (Breakfast, Rice, Stew, Snack, Sweet, Non-Veg)",
        loss_function="CrossEntropyLoss",
        active_heads=["category_head"],
        convergence_metric="top1_accuracy",
        target_threshold=0.96,
        description="Coarse hierarchical partition into primary meal categories."
    ),
    CurriculumStageSpec(
        stage_number=4,
        stage_name="regional_classification",
        target_objective="Cuisine / Regional origin (Tamil Nadu, Kerala, Karnataka, Andhra/Telangana)",
        loss_function="CrossEntropyLoss",
        active_heads=["regional_head"],
        convergence_metric="top1_accuracy",
        target_threshold=0.94,
        description="Regional context prior to prime fine-grained variant branches."
    ),
    CurriculumStageSpec(
        stage_number=5,
        stage_name="fine_grained_classification",
        target_objective="Discriminate 450+ exact dish variants (e.g. Dindigul Biryani vs Ambur Biryani)",
        loss_function="FocalLoss(gamma=2.0)",
        active_heads=["fine_grained_head"],
        convergence_metric="top1_accuracy",
        target_threshold=0.93,
        description="Fine-grained visual representation learning with hard negative penalty."
    ),
    CurriculumStageSpec(
        stage_number=6,
        stage_name="hard_negative_classification",
        target_objective="Pairwise hard-negative mining (Section 30 confusion matrix)",
        loss_function="TripletMarginLoss + ContrastiveLoss",
        active_heads=["fine_grained_head", "contrastive_embedding_head"],
        convergence_metric="hard_pair_accuracy",
        target_threshold=0.95,
        description="Forces feature space separation between easily confused dishes (Pongal vs Upma, Medu Vada vs Bonda)."
    ),
    CurriculumStageSpec(
        stage_number=7,
        stage_name="instance_segmentation",
        target_objective="Precise polygonal boundary isolation per component",
        loss_function="MaskLoss (Dice + BCE)",
        active_heads=["mask_head", "bbox_head"],
        convergence_metric="mask_mAP_50_95",
        target_threshold=0.88,
        description="Separates overlapping items like Sambar poured onto Idlis or multiple Chutney cups."
    ),
    CurriculumStageSpec(
        stage_number=8,
        stage_name="ingredient_recognition",
        target_objective="Detect visible aromatics, temperings, and inclusions",
        loss_function="MultiLabelAsymmetricLoss",
        active_heads=["ingredient_head"],
        convergence_metric="mean_f1",
        target_threshold=0.90,
        description="Identifies peppercorns, cashews, mustard seeds, curry leaves, shallots, and whole spices."
    ),
    CurriculumStageSpec(
        stage_number=9,
        stage_name="portion_estimation",
        target_objective="Categorical portion sizing (small, medium, large, piece counts)",
        loss_function="OrdinalCrossEntropyLoss",
        active_heads=["portion_head", "count_head"],
        convergence_metric="count_mae",
        target_threshold=0.94,
        description="Counts individual discrete pieces (e.g. 1 to 6 idlis) or classifies serving size."
    ),
    CurriculumStageSpec(
        stage_number=10,
        stage_name="weight_estimation",
        target_objective="Continuous gram weight estimation from calibrated volume and density",
        loss_function="HuberLoss(delta=10.0)",
        active_heads=["weight_regression_head"],
        convergence_metric="mape_pct",
        target_threshold=12.0,
        description="Computes physical grams using plate calibrator and food-specific density tables."
    ),
    CurriculumStageSpec(
        stage_number=11,
        stage_name="nutrition_estimation",
        target_objective="Compute recipe-aware calories and macronutrients",
        loss_function="L1Loss + RangeConstraintPenalty",
        active_heads=["nutrition_head"],
        convergence_metric="calorie_mae_kcal",
        target_threshold=28.0,
        description="Calculates exact calories and macros via raw-to-cooked conversion tables."
    ),
    CurriculumStageSpec(
        stage_number=12,
        stage_name="uncertainty_calibration",
        target_objective="Temperature scaling & Bayesian interval calibration",
        loss_function="NegativeLogLikelihood + ECE",
        active_heads=["uncertainty_head"],
        convergence_metric="expected_calibration_error",
        target_threshold=0.035,
        description="Calibrates confidence scores so predicted 90% confidence matches 90% empirical precision; enforces Section 34 Ambiguity Preserver."
    )
]

class HierarchicalCurriculumManager:
    @staticmethod
    def get_stage(stage_number: int) -> Optional[CurriculumStageSpec]:
        for st in TWELVE_STAGE_CURRICULUM:
            if st.stage_number == stage_number:
                return st
        return None

    @staticmethod
    def get_priority_classes(priority_level: int) -> List[str]:
        group = TRAINING_PRIORITY_SCHEDULE.get(priority_level)
        return group.classes if group else []

    @staticmethod
    def check_stage_gate_passed(stage_number: int, current_metric_val: float) -> bool:
        st = HierarchicalCurriculumManager.get_stage(stage_number)
        if not st:
            return False
        if "error" in st.convergence_metric or "mae" in st.convergence_metric or "mape" in st.convergence_metric:
            return current_metric_val <= st.target_threshold
        return current_metric_val >= st.target_threshold
