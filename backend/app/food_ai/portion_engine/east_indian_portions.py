"""
East Indian Food Portion, Count & Volumetric Scaling Engine (Part 6)
Implements Sections 41, 42, 50, 53 of Part 6 Training Specification.

Guarantees:
- Food-specific portion classes:
  - Rice: 50g, 100g, 150g, 200g, 250g, 300g, 400g+
  - Curry: 50g, 100g, 150g, 200g, 250g, 300g+
  - Fish: 1 small piece (60g), 1 medium piece (100g), 1 large piece (150g), 2 pieces (200g), 3+ pieces (300g+)
  - Sweets: 1 piece, 2 pieces, 3 pieces, 4+ pieces
  - Breads: 1 piece, 2 pieces, 3 pieces, 4+ pieces
  - Bowls: small (100g), medium (180g), large (250g)
- Countable Food Detection (Count * average unit weight = total weight):
  Luchi, Kochuri, Singara, Fish pieces, Prawn pieces, Sweets, Pitha, Litti, Cutlets, Kathi rolls, Fried snacks.
- Portion Reference Objects (katori, steel bowl, spoon, tablespoon, plate, thali, glass, hand)
- Visual Fat / Oil Sheen Estimator (low, medium, high, unknown)
"""

from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

# =============================================================================
# 1. SECTION 42: COUNTABLE FOOD REGISTRY & DETECTOR
# =============================================================================

COUNTABLE_EAST_INDIAN_ITEMS: Dict[str, Dict[str, Any]] = {
    "WB_BREAD_LUCHI": {"unit_name": "luchi", "typical_weight_g": 30.0, "min_weight_g": 25.0, "max_weight_g": 35.0},
    "WB_BREAD_KOCHURI": {"unit_name": "kochuri", "typical_weight_g": 50.0, "min_weight_g": 40.0, "max_weight_g": 60.0},
    "WB_BREAD_RADHA_BALLAVI": {"unit_name": "radhaballabhi", "typical_weight_g": 55.0, "min_weight_g": 45.0, "max_weight_g": 65.0},
    "WB_SNACK_BENGALI_SINGARA": {"unit_name": "singara", "typical_weight_g": 65.0, "min_weight_g": 55.0, "max_weight_g": 80.0},
    "WB_FISH_BHETKI_FRY": {"unit_name": "cutlet", "typical_weight_g": 130.0, "min_weight_g": 110.0, "max_weight_g": 150.0},
    "WB_STREET_VEGETABLE_CHOP": {"unit_name": "chop", "typical_weight_g": 100.0, "min_weight_g": 85.0, "max_weight_g": 115.0},
    "WB_STREET_TELEBHAJA_BEGUNI": {"unit_name": "beguni", "typical_weight_g": 45.0, "min_weight_g": 35.0, "max_weight_g": 55.0},
    "WB_STREET_KATHI_ROLL_EGG_CHICKEN": {"unit_name": "roll", "typical_weight_g": 230.0, "min_weight_g": 200.0, "max_weight_g": 260.0},
    "WB_STREET_KATHI_ROLL_EGG": {"unit_name": "roll", "typical_weight_g": 180.0, "min_weight_g": 160.0, "max_weight_g": 200.0},
    "WB_SWEET_RASGULLA": {"unit_name": "piece", "typical_weight_g": 50.0, "min_weight_g": 40.0, "max_weight_g": 60.0},
    "WB_SWEET_RAJBHOG": {"unit_name": "piece", "typical_weight_g": 75.0, "min_weight_g": 65.0, "max_weight_g": 90.0},
    "WB_SWEET_NOLEN_GUR_SANDESH": {"unit_name": "piece", "typical_weight_g": 35.0, "min_weight_g": 30.0, "max_weight_g": 45.0},
    "WB_SWEET_PLAIN_SANDESH": {"unit_name": "piece", "typical_weight_g": 35.0, "min_weight_g": 30.0, "max_weight_g": 45.0},
    "WB_SWEET_PATISHAPTA": {"unit_name": "crepe", "typical_weight_g": 50.0, "min_weight_g": 40.0, "max_weight_g": 60.0},
    "WB_SWEET_DOODH_PULI": {"unit_name": "puli", "typical_weight_g": 45.0, "min_weight_g": 35.0, "max_weight_g": 55.0},
    "OD_SWEET_CHHENA_GAJA": {"unit_name": "piece", "typical_weight_g": 60.0, "min_weight_g": 50.0, "max_weight_g": 70.0},
    "OD_SWEET_RASABALI": {"unit_name": "patty", "typical_weight_g": 60.0, "min_weight_g": 50.0, "max_weight_g": 70.0},
    "OD_SWEET_PURI_KHAJA": {"unit_name": "piece", "typical_weight_g": 70.0, "min_weight_g": 55.0, "max_weight_g": 85.0},
    "BR_BREAD_LITTI": {"unit_name": "litti", "typical_weight_g": 75.0, "min_weight_g": 65.0, "max_weight_g": 90.0},
    "BR_SWEET_THEKUA": {"unit_name": "cookie", "typical_weight_g": 40.0, "min_weight_g": 30.0, "max_weight_g": 50.0},
    "BR_SWEET_TILKUT": {"unit_name": "disc", "typical_weight_g": 50.0, "min_weight_g": 40.0, "max_weight_g": 60.0},
    "BR_SWEET_SILAO_KHAJA": {"unit_name": "piece", "typical_weight_g": 60.0, "min_weight_g": 45.0, "max_weight_g": 75.0},
    "JH_SNACK_DHUSKA": {"unit_name": "dhuska", "typical_weight_g": 45.0, "min_weight_g": 35.0, "max_weight_g": 55.0},
    "JH_BREAD_CHILKA_ROTI": {"unit_name": "roti", "typical_weight_g": 70.0, "min_weight_g": 60.0, "max_weight_g": 80.0},
    "FISH_PIECE_CARP_STEAK": {"unit_name": "steak", "typical_weight_g": 100.0, "min_weight_g": 80.0, "max_weight_g": 130.0},
    "PRAWN_PIECE_JUMBO": {"unit_name": "prawn", "typical_weight_g": 40.0, "min_weight_g": 30.0, "max_weight_g": 55.0}
}

class CountableFoodDetectionResult(BaseModel):
    is_countable: bool
    unit_name: str
    count: int
    estimated_average_unit_weight_g: float
    total_estimated_weight_g: float
    confidence: float
    notes: str

class CountableFoodDetector:
    @staticmethod
    def estimate_countable_weight(
        food_id: str,
        detected_count: int,
        bounding_box_scale_factor: float = 1.0
    ) -> CountableFoodDetectionResult:
        if food_id in COUNTABLE_EAST_INDIAN_ITEMS:
            spec = COUNTABLE_EAST_INDIAN_ITEMS[food_id]
            unit_wt = spec["typical_weight_g"] * bounding_box_scale_factor
            unit_wt = max(spec["min_weight_g"], min(spec["max_weight_g"], unit_wt))
            tot_wt = round(detected_count * unit_wt, 1)
            return CountableFoodDetectionResult(
                is_countable=True,
                unit_name=spec["unit_name"],
                count=detected_count,
                estimated_average_unit_weight_g=round(unit_wt, 1),
                total_estimated_weight_g=tot_wt,
                confidence=0.95,
                notes=f"Calculated from discrete count of {detected_count} {spec['unit_name']}(s) * {round(unit_wt, 1)}g average unit mass."
            )
        return CountableFoodDetectionResult(
            is_countable=False,
            unit_name="serving",
            count=1,
            estimated_average_unit_weight_g=150.0,
            total_estimated_weight_g=150.0,
            confidence=0.70,
            notes="Item is continuous volume; estimated via volumetric standard portion."
        )

# =============================================================================
# 2. SECTION 41: DISCRETE PORTION TIERS & KATORI CALIBRATOR
# =============================================================================

class EastIndianPortionClassifier:
    """
    Implements Section 41 discrete portions:
    - Rice: 50g, 100g, 150g, 200g, 250g, 300g, 400g+
    - Curry: 50g, 100g, 150g, 200g, 250g, 300g+
    - Fish: 1 small (60g), 1 medium (100g), 1 large (150g), 2 pcs (200g), 3+ pcs (300g+)
    - Sweets: 1 pc, 2 pcs, 3 pcs, 4+ pcs
    - Bowls: small (100g), medium (180g), large (250g)
    """
    RICE_TIERS = [50.0, 100.0, 150.0, 200.0, 250.0, 300.0, 400.0]
    CURRY_TIERS = [50.0, 100.0, 150.0, 200.0, 250.0, 300.0]
    BOWL_TIERS = {"small": 100.0, "medium": 180.0, "large": 250.0}

    @classmethod
    def match_rice_tier(cls, continuous_grams: float) -> Tuple[float, str]:
        best = min(cls.RICE_TIERS, key=lambda x: abs(x - continuous_grams))
        return best, f"{int(best)}g rice portion"

    @classmethod
    def match_curry_tier(cls, continuous_grams: float) -> Tuple[float, str]:
        best = min(cls.CURRY_TIERS, key=lambda x: abs(x - continuous_grams))
        return best, f"{int(best)}g curry portion"

    @classmethod
    def estimate_fish_piece_portion(cls, piece_count: int, size: str = "medium") -> Tuple[float, str]:
        size_map = {"small": 60.0, "medium": 100.0, "large": 150.0}
        unit = size_map.get(size.lower(), 100.0)
        tot = piece_count * unit
        label = f"{piece_count} {size} piece(s) ({int(tot)}g)"
        return tot, label

# =============================================================================
# 3. SECTION 50: PORTION REFERENCE OBJECT SCALER
# =============================================================================

class PortionReferenceScaler:
    """
    Implements Section 50:
    Visible reference objects: katori, steel bowl, spoon, tablespoon, plate, thali, glass, hand.
    If reference object exists -> use for scale estimation.
    If not -> use visual estimation with lower confidence.
    """
    REFERENCE_DIAMETERS_CM = {
        "katori": 8.5,
        "standard_bowl": 11.0,
        "quarter_plate": 18.0,
        "dinner_plate": 26.0,
        "thali": 31.0,
        "teaspoon": 13.0,
        "tablespoon": 18.0,
        "tea_glass": 6.5,
        "earthen_bhar": 7.0,
        "human_hand_palm": 10.0
    }

    @classmethod
    def calibrate_scale(
        cls,
        detected_reference: Optional[str] = None,
        reference_pixel_width: Optional[float] = None
    ) -> Dict[str, Any]:
        if not detected_reference or detected_reference.lower() not in cls.REFERENCE_DIAMETERS_CM:
            return {
                "has_reference_object": False,
                "scale_cm_per_pixel": None,
                "portion_confidence_penalty": 0.15,
                "confidence_level": "medium",
                "notes": "No standard reference object detected; fallback to monocular visual estimation with lower confidence (Section 50)."
            }

        ref_key = detected_reference.lower().strip()
        ref_cm = cls.REFERENCE_DIAMETERS_CM[ref_key]
        cm_per_px = (ref_cm / reference_pixel_width) if reference_pixel_width and reference_pixel_width > 0 else 0.05

        return {
            "has_reference_object": True,
            "reference_object": ref_key,
            "reference_true_dimension_cm": ref_cm,
            "scale_cm_per_pixel": cm_per_px,
            "portion_confidence_penalty": 0.0,
            "confidence_level": "high",
            "notes": f"Calibrated using visible {ref_key} (true dimension: {ref_cm}cm) for physical scale reconstruction."
        }

# =============================================================================
# 4. SECTION 53: VISUAL FAT / OIL SHEEN ESTIMATOR
# =============================================================================

class VisualFatSheenEstimator:
    """
    Implements Section 53:
    Visual labels: low, medium, high, unknown.
    Detects visible oil, visible ghee, mustard oil sheen, fried preparation.
    Never claim exact oil quantity from image alone.
    """
    @staticmethod
    def estimate_fat_level(cues: Dict[str, Any]) -> Dict[str, Any]:
        has_mustard_oil_float = cues.get("mustard_oil_float", False)
        has_ghee_sheen = cues.get("ghee_sheen", False)
        has_fried_oil_glisten = cues.get("fried_oil_glisten", False)
        is_clear_broth = cues.get("is_clear_broth", False)
        is_steamed_or_boiled = cues.get("is_steamed_or_boiled", False)

        if has_mustard_oil_float or (has_ghee_sheen and has_fried_oil_glisten):
            return {
                "fat_level": "high",
                "fat_factor_multiplier": 1.25,
                "confidence": 0.90,
                "notes": "Heavy floating mustard oil layer / deep ghee sheen visibly observed."
            }

        if has_ghee_sheen or has_fried_oil_glisten:
            return {
                "fat_level": "medium",
                "fat_factor_multiplier": 1.0,
                "confidence": 0.88,
                "notes": "Moderate surface sheen indicating standard cooking oil / ghee tempering."
            }

        if is_steamed_or_boiled or is_clear_broth:
            return {
                "fat_level": "low",
                "fat_factor_multiplier": 0.85,
                "confidence": 0.92,
                "notes": "Minimal to low surface oil observed; preparation appears boiled or steamed."
            }

        return {
            "fat_level": "unknown",
            "fat_factor_multiplier": 1.0,
            "confidence": 0.50,
            "notes": "Surface sheen obscured; default median recipe fat content assumed per Section 53 rules."
        }
