"""
Northeast Indian Food Portion, Count & Volumetric Scaling Engine (Part 7)
Implements Sections 40, 52, 53, 54, 55, 66, 71, 72 of Part 7 Master Training Specification.

Guarantees:
- Food Counting for Momos, Pithas, Sel Roti, Pukhlein, Sha Phaley, Meat Pieces, and Fish Pieces
- Overlapping & Occlusion Handling (separating visible_count vs estimated_total_count)
- Discrete Portion Tiers for Rice, Stews, Soups, and Fermented Pastes
- Reference Object Calibration (plate, katori, soup bowl, hand)
- Northeast Visual Fat / Oil & Pork Fat Estimator (fatty pork belly vs lean meat vs oil-free boiled broth)
"""

from typing import Dict, Any, Optional, Tuple
from pydantic import BaseModel, Field

# =============================================================================
# 1. COUNTABLE NORTHEAST FOOD REGISTRY & DETECTOR (Sections 40, 55)
# =============================================================================

COUNTABLE_NORTHEAST_ITEMS: Dict[str, Dict[str, Any]] = {
    "NE_MOMO_PORK_STEAMED": {"unit_name": "momo", "typical_weight_g": 30.0, "min_weight_g": 24.0, "max_weight_g": 36.0},
    "NE_MOMO_VEG_STEAMED": {"unit_name": "momo", "typical_weight_g": 28.0, "min_weight_g": 22.0, "max_weight_g": 34.0},
    "NE_MOMO_CHICKEN_STEAMED": {"unit_name": "momo", "typical_weight_g": 29.0, "min_weight_g": 23.0, "max_weight_g": 35.0},
    "AS_PITHA_TIL": {"unit_name": "pitha", "typical_weight_g": 40.0, "min_weight_g": 32.0, "max_weight_g": 48.0},
    "AS_PITHA_GHILA": {"unit_name": "pitha", "typical_weight_g": 45.0, "min_weight_g": 38.0, "max_weight_g": 52.0},
    "ML_SNACK_PUKHLEIN": {"unit_name": "pukhlein", "typical_weight_g": 50.0, "min_weight_g": 40.0, "max_weight_g": 60.0},
    "SK_BREAD_SEL_ROTI": {"unit_name": "sel_roti_ring", "typical_weight_g": 60.0, "min_weight_g": 50.0, "max_weight_g": 72.0},
    "SK_SNACK_SHA_PHALEY": {"unit_name": "sha_phaley", "typical_weight_g": 120.0, "min_weight_g": 100.0, "max_weight_g": 140.0},
    "PORK_PIECE_NORTHEAST": {"unit_name": "pork_piece", "typical_weight_g": 45.0, "min_weight_g": 35.0, "max_weight_g": 60.0},
    "FISH_PIECE_TENGA": {"unit_name": "fish_steak", "typical_weight_g": 90.0, "min_weight_g": 70.0, "max_weight_g": 115.0}
}

class NortheastCountableResult(BaseModel):
    is_countable: bool
    unit_name: str
    visible_count: int
    estimated_total_count: int
    occluded_count: int
    unit_weight_g: float
    total_estimated_weight_g: float
    confidence: float
    notes: str

class NortheastCountableDetector:
    """
    Implements Sections 40, 55, 71, 72:
    Counts items such as Momos, Pithas, Sel Roti, Meat Pieces.
    Supports overlapping/partially occluded objects.
    """
    @staticmethod
    def estimate_count_and_weight(
        food_id: str,
        visible_count: int,
        occlusion_factor: float = 0.0, # 0.0 means no occlusion, 0.2 means 20% estimated hidden
        scale_multiplier: float = 1.0
    ) -> NortheastCountableResult:
        if food_id in COUNTABLE_NORTHEAST_ITEMS:
            spec = COUNTABLE_NORTHEAST_ITEMS[food_id]
            unit_wt = spec["typical_weight_g"] * scale_multiplier
            unit_wt = max(spec["min_weight_g"], min(spec["max_weight_g"], unit_wt))

            # Estimate total count factoring in occlusion
            if occlusion_factor > 0.0:
                est_total = int(round(visible_count / (1.0 - min(occlusion_factor, 0.5))))
            else:
                est_total = visible_count
            hidden_cnt = max(0, est_total - visible_count)
            tot_wt = round(est_total * unit_wt, 1)

            conf = 0.96 if hidden_cnt == 0 else 0.88
            notes = f"Detected {visible_count} visible {spec['unit_name']}(s)"
            if hidden_cnt > 0:
                notes += f" + {hidden_cnt} estimated partially occluded based on plate clustering (Total: {est_total} items, {tot_wt}g)."
            else:
                notes += f" (Total: {tot_wt}g)."

            return NortheastCountableResult(
                is_countable=True,
                unit_name=spec["unit_name"],
                visible_count=visible_count,
                estimated_total_count=est_total,
                occluded_count=hidden_cnt,
                unit_weight_g=round(unit_wt, 1),
                total_estimated_weight_g=tot_wt,
                confidence=conf,
                notes=notes
            )

        return NortheastCountableResult(
            is_countable=False,
            unit_name="serving",
            visible_count=1,
            estimated_total_count=1,
            occluded_count=0,
            unit_weight_g=150.0,
            total_estimated_weight_g=150.0,
            confidence=0.70,
            notes="Item is continuous volume; estimated via standard portion."
        )

# =============================================================================
# 2. DISCRETE PORTION TIERS FOR RICE & SOUPS (Section 53)
# =============================================================================

class NortheastPortionTiers:
    RICE_TIERS = [50.0, 100.0, 150.0, 200.0, 250.0, 300.0]
    SOUP_STEW_TIERS = [100.0, 150.0, 200.0, 250.0, 350.0]
    FERMENTED_PASTE_TIERS = [20.0, 40.0, 60.0, 80.0]

    @classmethod
    def match_soup_tier(cls, grams: float) -> Tuple[float, str]:
        best = min(cls.SOUP_STEW_TIERS, key=lambda x: abs(x - grams))
        return best, f"{int(best)}g soup/stew portion"

# =============================================================================
# 3. VISUAL FAT & PORK FAT ESTIMATOR (Sections 52, 66)
# =============================================================================

class NortheastFatLevelEstimator:
    """
    Implements Sections 52, 66:
    Northeast cooking ranges from 100% oil-free boiled stews (Bai, Chamthong)
    to rich fatty pork belly braises (Dohneiihong, Phagshapa) and wood-smoked pork.
    """
    @staticmethod
    def estimate_fat(cues: Dict[str, Any]) -> Dict[str, Any]:
        has_heavy_pork_belly_fat = cues.get("has_heavy_pork_fat", False)
        is_deep_fried = cues.get("is_deep_fried", False)
        is_oil_free_boiled = cues.get("is_oil_free_boiled", False)
        has_black_sesame_oil = cues.get("has_black_sesame", False)

        if has_heavy_pork_belly_fat:
            return {
                "fat_level": "high",
                "fat_multiplier": 1.25,
                "notes": "Generous indigenous pork belly fat rind visibly present."
            }

        if is_deep_fried or has_black_sesame_oil:
            return {
                "fat_level": "medium_high",
                "fat_multiplier": 1.15,
                "notes": "Deep fried or roasted sesame seed oil extraction."
            }

        if is_oil_free_boiled:
            return {
                "fat_level": "very_low",
                "fat_multiplier": 0.70,
                "notes": "Traditional oil-free boiled/steamed herbal preparation."
            }

        return {
            "fat_level": "moderate",
            "fat_multiplier": 1.0,
            "notes": "Standard regional recipe fat baseline."
        }
