"""
Food AI Datasets Module
Exports canonical dataset schema, quality control gate, gold benchmark datasets,
hard negative mining pairs, out-of-distribution benchmark, and format exporter.
"""

from .schema import FoodSample, FoodItemAnnotation, BoundingBox, ReferenceObjectScale, CameraMetadata
from .quality_control import QualityControlGate, compute_dhash, hamming_distance
from .gold_dataset import GOLD_BENCHMARK_SAMPLES
from .portion_gold_dataset import PORTION_GOLD_SAMPLES, MultiViewMealSample
from .hard_negatives import CONFUSING_FOOD_PAIRS, ConfusingPair
from .unknown_ood_dataset import OOD_DATASET_BENCHMARK, is_prediction_ood
from .exporter import DatasetExporter
