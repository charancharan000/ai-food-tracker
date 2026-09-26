"""
Training Configuration & Hyperparameters
Specifies learning rates, curriculum stages, loss weights, and checkpoint directories.
"""

from typing import Dict, Any, List
from pydantic import BaseModel, Field

class TrainingConfig(BaseModel):
    experiment_name: str = "nutriscan_south_indian_finetune_v2"
    device: str = "cuda" # falls back to "cpu" if unavailable
    random_seed: int = 42

    # Backbone & Image Specs
    image_size: int = 384
    batch_size: int = 16
    num_workers: int = 4
    pin_memory: bool = True

    # Optimization
    learning_rate: float = 3e-4
    weight_decay: float = 1e-4
    warmup_epochs: int = 3
    total_epochs: int = 35
    gradient_accumulation_steps: int = 2
    max_grad_norm: float = 1.0

    # Loss Weights
    loss_weight_classification: float = 1.0
    loss_weight_cuisine: float = 0.5
    loss_weight_ingredients: float = 0.7
    loss_weight_weight_grams: float = 1.2 # Prioritize physical weight accuracy!
    loss_weight_hard_negatives: float = 1.5

    # Checkpointing & Early Stopping
    early_stopping_patience: int = 6
    checkpoint_dir: str = "checkpoints/v2"
    save_best_metric: str = "val_weight_mae_grams" # Best model minimizes weight error

    # Class Imbalance
    use_class_balanced_sampling: bool = True
    label_smoothing: float = 0.1

DEFAULT_TRAINING_CONFIG = TrainingConfig()
