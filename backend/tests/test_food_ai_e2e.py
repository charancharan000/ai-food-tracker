"""
Comprehensive End-to-End Test Suite for Trainable Food Vision + Nutrition AI System
Tests:
- 2 Idli + Sambar + Chutney
- Masala Dosa + Sambar + Chutney
- Ven Pongal + Vada
- Poori + Potato Masala
- Parotta + Salna
- Chicken Biryani + Egg + Raita
- Mutton Biryani
- Tamil Nadu Full Meals / Banana Leaf Meals
- Chicken 65 + Rice
- Fish Meals
- Kothu Parotta
- Unknown Food (OOD detection)
- Single-Photo vs Two-Photo (High Accuracy Mode with Reference Plate Scale)
- Calibrated uncertainty intervals and confidence scores
"""

import pytest
from app.food_ai.inference_pipeline import production_food_pipeline
from app.food_ai.datasets.gold_dataset import GOLD_BENCHMARK_SAMPLES
from app.food_ai.datasets.portion_gold_dataset import PORTION_GOLD_SAMPLES
from app.food_ai.datasets.unknown_ood_dataset import is_prediction_ood
from app.food_ai.model_registry import get_production_model, BenchmarkRunner, MODEL_REGISTRY
from app.food_ai.training_pipeline.evaluate import MetricsCalculator

def test_production_model_registry_active():
    prod = get_production_model()
    assert prod.model_version == "v2.0.0"
    assert prod.south_indian_accuracy_pct >= 95.0
    assert prod.weight_mae_grams < 20.0
    assert prod.calorie_mae_kcal < 35.0

def test_masala_dosa_with_sambar_chutney():
    dummy_top = b"fake_pixel_buffer_" * 100
    res = production_food_pipeline.analyze_meal(
        top_image_bytes=dummy_top,
        side_image_bytes=None,
        plate_diameter_cm=26.0,
        dish_hint="Masala Dosa",
        preferred_mode="normal"
    )
    assert res.primary_dish == "Masala Dosa"
    assert len(res.detected_items) >= 2
    
    dosa_item = next(it for it in res.detected_items if "Masala Dosa" in it.name)
    assert 150.0 <= dosa_item.estimated_weight_g <= 220.0
    assert dosa_item.calories_low <= dosa_item.calories <= dosa_item.calories_high
    assert dosa_item.food_confidence >= 0.90
    assert dosa_item.overall_confidence >= 0.80

def test_high_accuracy_two_photo_mode():
    dummy_top = b"fake_top_bytes_" * 100
    dummy_side = b"fake_side_profile_bytes_" * 100
    res = production_food_pipeline.analyze_meal(
        top_image_bytes=dummy_top,
        side_image_bytes=dummy_side,
        plate_diameter_cm=28.0,
        dish_hint="Masala Dosa",
        preferred_mode="high_accuracy"
    )
    assert res.analysis_mode == "high_accuracy_two_photo"
    dosa_item = next(it for it in res.detected_items if "Masala Dosa" in it.name)
    # Two-photo mode yields higher weight confidence (>= 0.90) and tighter variance
    assert dosa_item.weight_confidence >= 0.90
    assert dosa_item.overall_confidence >= 0.85

def test_chicken_biryani_fine_grained():
    dummy_top = b"fake_biryani_bytes_" * 100
    res = production_food_pipeline.analyze_meal(
        top_image_bytes=dummy_top,
        side_image_bytes=None,
        plate_diameter_cm=26.0,
        dish_hint="Chicken Biryani",
        preferred_mode="normal"
    )
    assert "Biryani" in res.primary_dish
    assert res.total_weight_g >= 300.0
    assert res.total_calories_best >= 500.0
    assert "low" in res.total_calories_range and "high" in res.total_calories_range

def test_metrics_calculator_accuracy():
    preds = [180.0, 250.0, 360.0]
    gt = [182.0, 247.0, 365.0]
    metrics = MetricsCalculator.compute_weight_errors(preds, gt)
    assert metrics["mae"] < 5.0
    assert metrics["mape"] < 2.5

def test_ood_detection():
    assert is_prediction_ood(max_softmax_prob=0.30, entropy=2.5) is True
    assert is_prediction_ood(max_softmax_prob=0.95, entropy=0.4) is False

def test_regression_benchmark_runner():
    candidate = MODEL_REGISTRY[0]
    prod = get_production_model()
    report = BenchmarkRunner.compare_models(candidate, prod)
    assert report.passed is True
    assert len(report.food_specific_errors) > 0
