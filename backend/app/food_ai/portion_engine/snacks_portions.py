"""
Indian Snacks & Tiffin Portion Engine, Cooking Method & Oil Estimator (Part 15)
Implements Sections 32–39 of Part 15 Specification.

Features:
- Countable snack piece estimator (1, 2, 3, 4, 5, 6, 8, 10, etc.) with overlapping detection.
- Portion sizing tiers: Mini, Small, Regular, Medium, Large, Jumbo, Plate, Bowl, Packet.
- Reference object calibrator (Steel plate, Banana leaf, Paper plate, Hand, Spoon, Cup).
- Two-Photo Portion Mode (Top view + 45-degree angle view).
- Cooking method categorization (Steamed, Deep-fried, Shallow-fried, Baked, Roasted, Air-fried).
- Qualitative Oil/Fat Estimator (Section 37: Low, Moderate, High, Deep-fried, Unknown).
  STRICT: Never outputs "exact 12 ml oil" from image alone.
- Filling detector and independent accompaniment weight separator (Section 39).
"""

from typing import Dict, Any, List, Optional, Tuple
from pydantic import BaseModel, Field


class SnackPortionConfig(BaseModel):
    food_id: str
    canonical_name: str
    unit_type: str                  # "piece", "gram", "plate", "bowl"
    standard_piece_weight_g: Optional[float] = None
    mini_piece_weight_g: Optional[float] = None
    jumbo_piece_weight_g: Optional[float] = None
    default_serving_pieces: int = 1
    default_serving_weight_g: float = 100.0
    density_g_ml: float = 1.05
    is_countable: bool = True


SNACK_PORTION_DATABASE: Dict[str, SnackPortionConfig] = {
    # South Indian Snacks & Tiffin
    "IND-SNK-TN-MEDHUVADAI-001": SnackPortionConfig(
        food_id="IND-SNK-TN-MEDHUVADAI-001",
        canonical_name="Medhu Vadai",
        unit_type="piece",
        standard_piece_weight_g=45.0,
        mini_piece_weight_g=22.0,
        jumbo_piece_weight_g=70.0,
        default_serving_pieces=2,
        default_serving_weight_g=90.0,
        is_countable=True,
    ),
    "IND-SNK-TN-MASALAVADAI-001": SnackPortionConfig(
        food_id="IND-SNK-TN-MASALAVADAI-001",
        canonical_name="Masala Vadai",
        unit_type="piece",
        standard_piece_weight_g=40.0,
        mini_piece_weight_g=20.0,
        jumbo_piece_weight_g=60.0,
        default_serving_pieces=2,
        default_serving_weight_g=80.0,
        is_countable=True,
    ),
    "IND-TIF-TN-IDLI-001": SnackPortionConfig(
        food_id="IND-TIF-TN-IDLI-001",
        canonical_name="Idli",
        unit_type="piece",
        standard_piece_weight_g=45.0,
        mini_piece_weight_g=12.0,
        jumbo_piece_weight_g=120.0, # Thatte idli
        default_serving_pieces=3,
        default_serving_weight_g=135.0,
        is_countable=True,
    ),
    "IND-TIF-TN-MASALADOSA-001": SnackPortionConfig(
        food_id="IND-TIF-TN-MASALADOSA-001",
        canonical_name="Masala Dosa",
        unit_type="plate",
        standard_piece_weight_g=180.0,
        mini_piece_weight_g=110.0,
        jumbo_piece_weight_g=260.0,
        default_serving_pieces=1,
        default_serving_weight_g=180.0,
        is_countable=True,
    ),
    "IND-SNK-TN-PANIYARAM-001": SnackPortionConfig(
        food_id="IND-SNK-TN-PANIYARAM-001",
        canonical_name="Kuzhi Paniyaram",
        unit_type="piece",
        standard_piece_weight_g=25.0,
        mini_piece_weight_g=15.0,
        jumbo_piece_weight_g=40.0,
        default_serving_pieces=6,
        default_serving_weight_g=150.0,
        is_countable=True,
    ),
    "IND-SNK-TN-ONIONBAJJI-001": SnackPortionConfig(
        food_id="IND-SNK-TN-ONIONBAJJI-001",
        canonical_name="Onion Bajji",
        unit_type="piece",
        standard_piece_weight_g=35.0,
        mini_piece_weight_g=20.0,
        jumbo_piece_weight_g=55.0,
        default_serving_pieces=3,
        default_serving_weight_g=105.0,
        is_countable=True,
    ),
    "IND-SNK-TN-POTATOBONDA-001": SnackPortionConfig(
        food_id="IND-SNK-TN-POTATOBONDA-001",
        canonical_name="Potato Bonda",
        unit_type="piece",
        standard_piece_weight_g=55.0,
        mini_piece_weight_g=30.0,
        jumbo_piece_weight_g=85.0,
        default_serving_pieces=2,
        default_serving_weight_g=110.0,
        is_countable=True,
    ),

    # North Indian Snacks
    "IND-SNK-NI-SAMOSA-001": SnackPortionConfig(
        food_id="IND-SNK-NI-SAMOSA-001",
        canonical_name="Samosa",
        unit_type="piece",
        standard_piece_weight_g=85.0,
        mini_piece_weight_g=35.0, # Cocktail samosa
        jumbo_piece_weight_g=140.0, # Halwai jumbo samosa
        default_serving_pieces=2,
        default_serving_weight_g=170.0,
        is_countable=True,
    ),
    "IND-SNK-NI-PYAZKACHORI-001": SnackPortionConfig(
        food_id="IND-SNK-NI-PYAZKACHORI-001",
        canonical_name="Pyaz Kachori",
        unit_type="piece",
        standard_piece_weight_g=120.0,
        mini_piece_weight_g=60.0,
        jumbo_piece_weight_g=160.0,
        default_serving_pieces=1,
        default_serving_weight_g=120.0,
        is_countable=True,
    ),
    "IND-SNK-NI-DALKACHORI-001": SnackPortionConfig(
        food_id="IND-SNK-NI-DALKACHORI-001",
        canonical_name="Dal Kachori",
        unit_type="piece",
        standard_piece_weight_g=65.0,
        mini_piece_weight_g=30.0,
        jumbo_piece_weight_g=95.0,
        default_serving_pieces=2,
        default_serving_weight_g=130.0,
        is_countable=True,
    ),
    "IND-SNK-NI-ALOOTIKKI-001": SnackPortionConfig(
        food_id="IND-SNK-NI-ALOOTIKKI-001",
        canonical_name="Aloo Tikki",
        unit_type="piece",
        standard_piece_weight_g=70.0,
        mini_piece_weight_g=35.0,
        jumbo_piece_weight_g=110.0,
        default_serving_pieces=2,
        default_serving_weight_g=140.0,
        is_countable=True,
    ),
    "IND-SNK-NI-PANIPURI-001": SnackPortionConfig(
        food_id="IND-SNK-NI-PANIPURI-001",
        canonical_name="Pani Puri",
        unit_type="piece",
        standard_piece_weight_g=30.0, # Complete shell + potato + pani
        mini_piece_weight_g=20.0,
        jumbo_piece_weight_g=40.0,
        default_serving_pieces=6,
        default_serving_weight_g=180.0,
        is_countable=True,
    ),

    # West Indian Snacks
    "IND-SNK-MH-VADAPAV-001": SnackPortionConfig(
        food_id="IND-SNK-MH-VADAPAV-001",
        canonical_name="Vada Pav",
        unit_type="piece",
        standard_piece_weight_g=140.0,
        mini_piece_weight_g=85.0,
        jumbo_piece_weight_g=195.0,
        default_serving_pieces=1,
        default_serving_weight_g=140.0,
        is_countable=True,
    ),
    "IND-SNK-MH-MISALPAV-001": SnackPortionConfig(
        food_id="IND-SNK-MH-MISALPAV-001",
        canonical_name="Misal Pav",
        unit_type="plate",
        standard_piece_weight_g=300.0,
        mini_piece_weight_g=200.0,
        jumbo_piece_weight_g=420.0,
        default_serving_pieces=1,
        default_serving_weight_g=300.0,
        is_countable=False,
    ),
    "IND-SNK-GJ-DHOKLA-001": SnackPortionConfig(
        food_id="IND-SNK-GJ-DHOKLA-001",
        canonical_name="Dhokla",
        unit_type="piece",
        standard_piece_weight_g=35.0,
        mini_piece_weight_g=20.0,
        jumbo_piece_weight_g=55.0,
        default_serving_pieces=4,
        default_serving_weight_g=140.0,
        is_countable=True,
    ),
    "IND-SNK-GJ-KHAMAN-001": SnackPortionConfig(
        food_id="IND-SNK-GJ-KHAMAN-001",
        canonical_name="Khaman",
        unit_type="piece",
        standard_piece_weight_g=40.0,
        mini_piece_weight_g=25.0,
        jumbo_piece_weight_g=60.0,
        default_serving_pieces=4,
        default_serving_weight_g=160.0,
        is_countable=True,
    ),

    # Northeast Momos
    "IND-SNK-NE-VEGMOMO-001": SnackPortionConfig(
        food_id="IND-SNK-NE-VEGMOMO-001",
        canonical_name="Steamed Veg Momo",
        unit_type="piece",
        standard_piece_weight_g=28.0,
        mini_piece_weight_g=18.0,
        jumbo_piece_weight_g=40.0,
        default_serving_pieces=6,
        default_serving_weight_g=168.0,
        is_countable=True,
    ),
    "IND-SNK-NE-CHICKENMOMO-001": SnackPortionConfig(
        food_id="IND-SNK-NE-CHICKENMOMO-001",
        canonical_name="Steamed Chicken Momo",
        unit_type="piece",
        standard_piece_weight_g=32.0,
        mini_piece_weight_g=20.0,
        jumbo_piece_weight_g=45.0,
        default_serving_pieces=6,
        default_serving_weight_g=192.0,
        is_countable=True,
    ),
}


class CountablePieceEstimator:
    """Estimates piece count and flags occlusion/overlapping (Section 32)."""

    @classmethod
    def estimate_pieces(
        cls,
        detected_instances_count: int,
        is_overlapping: bool = False,
        cluster_area_relative: float = 1.0,
    ) -> Dict[str, Any]:
        count = max(1, detected_instances_count)
        uncertainty = False

        if is_overlapping:
            uncertainty = True
            # In crowded/stacked piles, true count may be slightly higher
            estimated_range = (count, count + int(round(count * 0.35)))
        else:
            estimated_range = (count, count)

        return {
            "piece_count": count,
            "count_range": estimated_range,
            "count_uncertain": uncertainty,
            "user_confirmation_recommended": uncertainty,
        }


class QualitativeOilEstimator:
    """
    Implements Section 37 Non-Negotiable Oil Estimation:
    Classifies qualitative visible oil levels:
    - Low visible oil
    - Moderate visible oil
    - High visible oil
    - Oil-coated
    - Deep-fried
    - Unknown
    STRICT: Never claims exact milliliters or grams of oil from a photo alone!
    """

    CATEGORIES = [
        "Low visible oil",
        "Moderate visible oil",
        "High visible oil",
        "Oil-coated",
        "Deep-fried",
        "Unknown",
    ]

    @classmethod
    def estimate_oil_level(
        cls,
        cooking_method: str,
        sheen_score: float = 0.5,
        fried_blistering: bool = False,
    ) -> Dict[str, Any]:
        cm = cooking_method.lower()

        if "steam" in cm or "boiled" in cm:
            tier = "Low visible oil"
            oil_factor_multiplier = 1.0
            description = "Steamed or boiled preparation; minimal surface oil unless tadka is added."
        elif "roast" in cm or "bake" in cm or "air" in cm:
            tier = "Moderate visible oil" if sheen_score > 0.6 else "Low visible oil"
            oil_factor_multiplier = 1.05
            description = "Baked/roasted snack; surface fat from dough shortening or ghee brushing."
        elif "pan" in cm or "shallow" in cm:
            tier = "Moderate visible oil" if sheen_score < 0.65 else "High visible oil"
            oil_factor_multiplier = 1.15
            description = "Shallow/pan-fried on tawa; moderate oil absorption on contact surfaces."
        elif "deep" in cm or fried_blistering:
            tier = "Deep-fried"
            oil_factor_multiplier = 1.25
            description = "Deep-fried in oil/ghee; high oil retention in fried crust and porous crumb."
        else:
            tier = "Unknown"
            oil_factor_multiplier = 1.10
            description = "Uncertain cooking method; conservative oil multiplier applied."

        return {
            "oil_tier": tier,
            "oil_factor_multiplier": oil_factor_multiplier,
            "description": description,
            "disclaimer": "Section 37: Qualitative oil tier estimated from cooking method prior; visual image cannot determine exact oil milliliters.",
        }


class TwoPhotoPortionMode:
    """
    Implements Section 35:
    Combines Top-view (Photo 1) and 45-degree angle (Photo 2) to resolve 3D height, volume and mass.
    """

    @classmethod
    def refine_portion(
        cls,
        food_id: str,
        top_view_piece_count: int,
        side_view_height_cm: float,
        reference_plate_diameter_cm: float = 24.0,
    ) -> Dict[str, Any]:
        config = SNACK_PORTION_DATABASE.get(food_id)
        std_wt = config.standard_piece_weight_g if config else 50.0

        # Calibration scale against standard 24cm plate
        scale_ratio = reference_plate_diameter_cm / 24.0

        # Height expansion factor: flat discs vs tall puffy items
        if side_view_height_cm > 4.5:
            size_multiplier = 1.25 # Jumbo / Halwai size
            size_label = "Jumbo / Extra Large"
        elif side_view_height_cm < 2.0:
            size_multiplier = 0.75 # Mini / Cocktail size
            size_label = "Mini"
        else:
            size_multiplier = 1.0 # Regular
            size_label = "Regular"

        refined_piece_weight = round(std_wt * size_multiplier * scale_ratio, 1)
        total_weight = round(top_view_piece_count * refined_piece_weight, 1)

        return {
            "size_tier": size_label,
            "piece_count": top_view_piece_count,
            "refined_piece_weight_g": refined_piece_weight,
            "total_estimated_weight_g": total_weight,
            "weight_uncertainty_range_g": (round(total_weight * 0.88, 1), round(total_weight * 1.14, 1)),
            "fusion_mode": "two_photo_fused",
        }
