import logging
from fastapi import APIRouter, Depends, UploadFile, File, status
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.food import FoodAnalysisResponse
from app.utils.image_processor import validate_and_process_image
from app.services.ai_vision_service import get_ai_vision_service
from app.core.exceptions import BadRequestException, AIServiceException

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/food", tags=["Food Analysis"])

@router.post("/analyze", response_model=FoodAnalysisResponse)
async def analyze_food(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """
    Receives food photo via multipart/form-data.
    Validates, compresses, and sends to the multimodal Vision AI service.
    Returns structured nutritional estimates and detected food items.
    """
    if not file.filename:
        raise BadRequestException("No image file provided.")

    # Read image contents
    file_bytes = await file.read()
    if not file_bytes:
        raise BadRequestException("Empty file uploaded.")

    content_type = file.content_type or "image/jpeg"

    # Validate and optimize image
    optimized_bytes, mime_type, width, height = validate_and_process_image(
        file_bytes=file_bytes,
        content_type=content_type
    )

    logger.info(f"Processing food analysis for user {current_user.id}: {file.filename} ({len(optimized_bytes)} bytes)")

    # Send to AI Vision Service
    vision_service = get_ai_vision_service()
    try:
        analysis_result = await vision_service.analyze_food_image(
            image_bytes=optimized_bytes,
            mime_type=mime_type
        )
        return analysis_result
    except AIServiceException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in food analysis: {e}")
        raise AIServiceException("Unable to analyze this image. Please try another clear food photo.")
