"""
FastAPI Router for Trainable Food Vision + Nutrition AI Subsystem
Endpoints for inference, multi-view high-accuracy mode, model registry,
benchmarking dashboard, active learning queue, and admin annotations.
"""

from typing import Optional, List, Dict, Any
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Query, status
from pydantic import BaseModel

from app.food_ai.inference_pipeline import production_food_pipeline, ProductionInferenceResponse
from app.food_ai.taxonomy import (
    TAMIL_NADU_TIFFIN_TAXONOMY,
    TAMIL_RICE_CLASSES,
    BIRYANI_PROTEIN_CLASSES,
    BIRYANI_REGIONAL_STYLES,
    SAMBAR_CLASSES,
    RASAM_CLASSES,
    KUZHAMBU_CLASSES,
    SPECIFIC_PORIYAL_CLASSES,
    CHUTNEY_CLASSES,
    CHICKEN_CLASSES,
    MUTTON_CLASSES,
    FISH_CLASSES,
    BANANA_LEAF_STANDARD_TEMPLATE,
)
from app.food_ai.model_registry import MODEL_REGISTRY, get_production_model, BenchmarkRunner
from app.food_ai.active_learning import ActiveLearningQueue, AnnotationService, AdminAnnotationPayload

router = APIRouter(prefix="/food-ai", tags=["Trainable Food AI"])

@router.post("/analyze", response_model=ProductionInferenceResponse)
async def analyze_food_ai(
    file: UploadFile = File(..., description="Top-down meal photo"),
    side_file: Optional[UploadFile] = File(None, description="Optional side or 45-degree angle photo for High Accuracy Mode"),
    plate_diameter_cm: float = Form(26.0, description="Reference plate/bowl diameter in cm"),
    hint: Optional[str] = Form(None, description="Optional dish tag/hint for guided fine-grained identification"),
    mode: Optional[str] = Form("normal", description="normal or high_accuracy")
):
    try:
        top_bytes = await file.read()
        side_bytes = await side_file.read() if side_file else None

        result = production_food_pipeline.analyze_meal(
            top_image_bytes=top_bytes,
            side_image_bytes=side_bytes,
            plate_diameter_cm=plate_diameter_cm,
            dish_hint=hint,
            preferred_mode=mode or "normal"
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Food AI analysis error: {str(e)}"
        )

@router.get("/taxonomy/south-indian")
def get_south_indian_taxonomy():
    return {
        "region": "Tamil Nadu & South India",
        "tiffin": TAMIL_NADU_TIFFIN_TAXONOMY,
        "rice_varieties": TAMIL_RICE_CLASSES,
        "biryani": {
            "protein_classes": BIRYANI_PROTEIN_CLASSES,
            "regional_styles": BIRYANI_REGIONAL_STYLES
        },
        "curries_and_stews": {
            "sambar": SAMBAR_CLASSES,
            "rasam": RASAM_CLASSES,
            "kuzhambu": KUZHAMBU_CLASSES
        },
        "vegetables": {
            "poriyal": SPECIFIC_PORIYAL_CLASSES
        },
        "chutneys": CHUTNEY_CLASSES,
        "non_veg": {
            "chicken": CHICKEN_CLASSES,
            "mutton": MUTTON_CLASSES,
            "fish": FISH_CLASSES
        },
        "banana_leaf_meal_composition": BANANA_LEAF_STANDARD_TEMPLATE.model_dump()
    }

@router.get("/model-registry")
def list_registered_models():
    return {
        "active_production_model": get_production_model().model_dump(),
        "registry": [m.model_dump() for m in MODEL_REGISTRY]
    }

@router.get("/benchmark")
def run_benchmark_regression_check():
    prod = get_production_model()
    # Candidate comparison check
    candidate = MODEL_REGISTRY[0]
    report = BenchmarkRunner.compare_models(candidate, prod)
    return report.model_dump()

class UserCorrectionRequest(BaseModel):
    image_uri: str
    predicted_dish: str
    user_suggested_dish: str
    estimated_weight_g: float
    user_confirmed_weight_g: Optional[float] = None
    confidence_score: float = 0.8
    notes: Optional[str] = None

@router.post("/active-learning/correction")
def submit_user_correction(payload: UserCorrectionRequest):
    item = ActiveLearningQueue.add_to_queue(
        image_uri=payload.image_uri,
        predicted_class=payload.predicted_dish,
        predicted_weight_g=payload.estimated_weight_g,
        model_version=get_production_model().model_version,
        confidence=payload.confidence_score,
        triage_reason="user_correction",
        user_suggested_dish=payload.user_suggested_dish,
        user_confirmed_weight_g=payload.user_confirmed_weight_g
    )
    return {
        "status": "received",
        "message": "User correction routed to active learning review queue for expert validation before retraining.",
        "queue_item": item.model_dump()
    }

@router.get("/active-learning/queue")
def get_active_learning_queue():
    items = ActiveLearningQueue.get_pending_items()
    return {
        "total_pending": len(items),
        "queue": [it.model_dump() for it in items]
    }

@router.post("/admin/annotate")
def submit_admin_annotation(payload: AdminAnnotationPayload):
    sample = AnnotationService.process_admin_annotation(payload)
    return {
        "status": "success",
        "message": f"Sample {sample.sample_id} verified and added to {sample.split} dataset.",
        "sample": sample.model_dump()
    }
