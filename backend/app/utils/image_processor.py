import io
from typing import Tuple
from PIL import Image
from fastapi import UploadFile
from app.core.config import settings
from app.core.exceptions import BadRequestException

def validate_and_process_image(
    file_bytes: bytes,
    content_type: str,
    max_dimension: int = 1600,
    jpeg_quality: int = 85
) -> Tuple[bytes, str, int, int]:
    """
    Validates the uploaded image bytes, checks size and format,
    and returns (optimized_bytes, mime_type, width, height).
    """
    # 1. Size check
    max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
    if len(file_bytes) > max_bytes:
        raise BadRequestException(f"Image file exceeds maximum size of {settings.MAX_UPLOAD_SIZE_MB}MB.")

    # 2. Content-type check
    if content_type.lower() not in settings.ALLOWED_IMAGE_TYPES:
        raise BadRequestException(
            f"Invalid image format '{content_type}'. Supported formats: JPEG, PNG, WEBP."
        )

    # 3. Open with PIL and verify integrity
    try:
        image = Image.open(io.BytesIO(file_bytes))
        image.load()
    except Exception as e:
        raise BadRequestException("Unable to decode uploaded image file. Please provide a valid photo.")

    # Convert RGBA / P to RGB if saving to JPEG
    if image.mode in ("RGBA", "LA", "P"):
        rgb_image = Image.new("RGB", image.size, (255, 255, 255))
        if image.mode == "P":
            image = image.convert("RGBA")
        rgb_image.paste(image, mask=image.split()[-1] if image.mode in ("RGBA", "LA") else None)
        image = rgb_image
    elif image.mode != "RGB":
        image = image.convert("RGB")

    orig_width, orig_height = image.size

    # Resize if larger than max_dimension
    if orig_width > max_dimension or orig_height > max_dimension:
        image.thumbnail((max_dimension, max_dimension), Image.Resampling.LANCZOS)

    output_buffer = io.BytesIO()
    image.save(output_buffer, format="JPEG", quality=jpeg_quality, optimize=True)
    optimized_bytes = output_buffer.getvalue()

    return optimized_bytes, "image/jpeg", image.width, image.height
