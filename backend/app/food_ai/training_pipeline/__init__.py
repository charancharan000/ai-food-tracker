"""
Training Pipeline Package
Exports training configuration, dataset loaders, identity-preserving augmentations,
training curriculum, evaluation suite, and hard example miner.
"""

from .config import TrainingConfig, DEFAULT_TRAINING_CONFIG
from .dataset_loader import FoodVisionDataset, compute_sample_weights_for_balanced_sampling, split_by_meal_id
from .augmentations import FoodAugmentationPlan
from .curriculum import CURRICULUM_STAGES, CurriculumStage
from .train import run_training_pipeline
from .evaluate import BenchmarkMetrics, MetricsCalculator
from .hard_mining import HardExampleMiner, HardSampleRecord
