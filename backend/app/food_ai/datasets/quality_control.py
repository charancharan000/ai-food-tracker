"""
Data Quality Control & Duplicate Prevention Pipeline
Validates resolution, blurriness, perceptual duplicates, and physical weight sanity bounds.
"""

import math
from typing import Tuple, List, Dict, Any, Optional

def compute_dhash(image_grayscale_pixels: List[List[int]], hash_size: int = 8) -> str:
    """
    Computes difference hash (dHash) from 2D pixel array.
    Outputs a hexadecimal hash string.
    """
    if not image_grayscale_pixels or len(image_grayscale_pixels) < hash_size:
        return "0" * (hash_size * hash_size // 4)
    
    diff_bits = []
    for row in range(min(hash_size, len(image_grayscale_pixels))):
        for col in range(min(hash_size, len(image_grayscale_pixels[row]) - 1)):
            diff_bits.append(1 if image_grayscale_pixels[row][col] > image_grayscale_pixels[row][col + 1] else 0)
    
    hex_str = "".join(str(b) for b in diff_bits)
    return hex(int(hex_str, 2))[2:].zfill(hash_size * hash_size // 4) if hex_str else "0000"

def hamming_distance(hash1: str, hash2: str) -> int:
    """Calculates hamming distance between two hex hash strings."""
    try:
        val1 = int(hash1, 16)
        val2 = int(hash2, 16)
        return bin(val1 ^ val2).count("1")
    except Exception:
        return 999

class QualityControlGate:
    MIN_WIDTH = 224
    MIN_HEIGHT = 224
    DUPLICATE_HAMMING_THRESHOLD = 5 # 0-5 difference indicates duplicate/near-duplicate

    @staticmethod
    def validate_sample(
        width: int,
        height: int,
        laplacian_variance: float,
        weight_grams: float,
        food_class: str,
        existing_hashes: Optional[List[str]] = None,
        candidate_hash: Optional[str] = None
    ) -> Tuple[bool, List[str]]:
        rejection_reasons = []

        # 1. Resolution Check
        if width < QualityControlGate.MIN_WIDTH or height < QualityControlGate.MIN_HEIGHT:
            rejection_reasons.append(f"Low resolution: {width}x{height} (minimum {QualityControlGate.MIN_WIDTH}x{QualityControlGate.MIN_HEIGHT})")

        # 2. Blur Check (variance of Laplacian)
        if laplacian_variance < 80.0:
            rejection_reasons.append(f"Image is too blurry: Laplacian score {laplacian_variance:.1f} < 80.0")

        # 3. Weight Range Sanity Check
        if weight_grams <= 0 or weight_grams > 3000.0:
            rejection_reasons.append(f"Implausible physical meal weight: {weight_grams}g (must be between 5g and 3000g)")

        # 4. Duplicate / Near-Duplicate Detection
        if candidate_hash and existing_hashes:
            for ex_hash in existing_hashes:
                dist = hamming_distance(candidate_hash, ex_hash)
                if dist <= QualityControlGate.DUPLICATE_HAMMING_THRESHOLD:
                    rejection_reasons.append(f"Near-duplicate image detected (Hamming distance {dist} <= {QualityControlGate.DUPLICATE_HAMMING_THRESHOLD})")
                    break

        return (len(rejection_reasons) == 0, rejection_reasons)
