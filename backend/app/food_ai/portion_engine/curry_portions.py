"""
Indian Dal, Curry & Gravy Portion Engine (Part 11)
Implements Sections 34, 35, 36, 37, 38, 43, 44, 45, 46, 47, 48, 68 of Part 11.

Guarantees:
- Food-specific portion database for Dal, Sambar, Rasam, Paneer Gravy, Chicken Curry,
  Mutton Curry, Fish Curry, Vegetable Curry, Kadhi, and Kurma.
- Standard Katori & Bowl volumetric calibrations:
  * Small Katori: 100 ml (~100-110 g)
  * Medium Katori: 150 ml (~155-170 g)
  * Large Bowl: 240 ml (~250-275 g)
  * Extra Large Handi: 350 ml (~370-420 g)
- Density matrix by consistency:
  * Very thin (Rasam): 1.01 g/ml
  * Thin (Tiffin sambar, light jhol): 1.04 g/ml
  * Medium (Dal tadka, homestyle chicken curry): 1.08 g/ml
  * Thick (Dal makhani, butter chicken, kurma): 1.14 g/ml
  * Semi-solid / Semi-dry (Sukka, kadai): 1.18 g/ml
  * Dry (Poriyal, dry sabzi): 0.95 g/ml
- Curry Floating Oil (Roghan/Tari) Estimator:
  * Low (0-3g added oil), Medium (4-8g added oil), High (10-18g added oil), Extreme (18-28g added oil)
- Protein-to-Gravy Mass Splitter:
  * Deconstructs curries with protein chunks (chicken, paneer, mutton, fish, egg) into
    discrete piece mass and sauce mass to prevent double-counting.
"""

from typing import Dict, Any, Optional, Tuple, List
from pydantic import BaseModel, Field


class CurryPortionSize(BaseModel):
    category: str  # "Small", "Medium", "Large", "Extra Large"
    typical_volume_ml: float
    typical_grams: float
    gram_range: Tuple[float, float]


class CurryPortionConfig(BaseModel):
    curry_family: str  # "dal", "sambar", "rasam", "paneer_curry", "chicken_curry", "mutton_curry", etc.
    small: CurryPortionSize
    medium: CurryPortionSize
    large: CurryPortionSize
    extra_large: CurryPortionSize
    density_g_ml: float
    notes: str


# Consistency to density table in g/ml
CONSISTENCY_DENSITY_MAP: Dict[str, float] = {
    "Very thin": 1.01,
    "Thin": 1.04,
    "Medium": 1.08,
    "Thick": 1.14,
    "Very thick": 1.16,
    "Semi-solid": 1.18,
    "Dry": 0.95,
}

# Standard Vessel Volumetric Map
VESSEL_VOLUME_MAP: Dict[str, float] = {
    "small_katori": 100.0,
    "medium_katori": 150.0,
    "large_katori": 200.0,
    "standard_bowl": 240.0,
    "serving_handi": 350.0,
    "banana_leaf_spot": 80.0,
    "plate_curry_pool": 120.0,
}


CURRY_PORTION_DATABASE: Dict[str, CurryPortionConfig] = {
    "dal": CurryPortionConfig(
        curry_family="dal",
        small=CurryPortionSize(category="Small", typical_volume_ml=100.0, typical_grams=108.0, gram_range=(95.0, 120.0)),
        medium=CurryPortionSize(category="Medium", typical_volume_ml=150.0, typical_grams=162.0, gram_range=(140.0, 185.0)),
        large=CurryPortionSize(category="Large", typical_volume_ml=240.0, typical_grams=260.0, gram_range=(225.0, 300.0)),
        extra_large=CurryPortionSize(category="Extra Large", typical_volume_ml=350.0, typical_grams=380.0, gram_range=(330.0, 440.0)),
        density_g_ml=1.08,
        notes="Standard yellow dal tadka / dal fry in stainless steel katori."
    ),
    "dal_makhani": CurryPortionConfig(
        curry_family="dal_makhani",
        small=CurryPortionSize(category="Small", typical_volume_ml=100.0, typical_grams=114.0, gram_range=(100.0, 130.0)),
        medium=CurryPortionSize(category="Medium", typical_volume_ml=150.0, typical_grams=171.0, gram_range=(150.0, 195.0)),
        large=CurryPortionSize(category="Large", typical_volume_ml=240.0, typical_grams=274.0, gram_range=(240.0, 315.0)),
        extra_large=CurryPortionSize(category="Extra Large", typical_volume_ml=350.0, typical_grams=400.0, gram_range=(350.0, 460.0)),
        density_g_ml=1.14,
        notes="Heavy black urad dal enriched with butter and cream."
    ),
    "sambar": CurryPortionConfig(
        curry_family="sambar",
        small=CurryPortionSize(category="Small", typical_volume_ml=100.0, typical_grams=105.0, gram_range=(90.0, 115.0)),
        medium=CurryPortionSize(category="Medium", typical_volume_ml=150.0, typical_grams=158.0, gram_range=(135.0, 180.0)),
        large=CurryPortionSize(category="Large", typical_volume_ml=240.0, typical_grams=252.0, gram_range=(220.0, 290.0)),
        extra_large=CurryPortionSize(category="Extra Large", typical_volume_ml=350.0, typical_grams=368.0, gram_range=(320.0, 420.0)),
        density_g_ml=1.05,
        notes="South Indian vegetable sambar with toor dal, vegetables, and tamarind."
    ),
    "rasam": CurryPortionConfig(
        curry_family="rasam",
        small=CurryPortionSize(category="Small", typical_volume_ml=80.0, typical_grams=81.0, gram_range=(70.0, 95.0)),
        medium=CurryPortionSize(category="Medium", typical_volume_ml=120.0, typical_grams=121.0, gram_range=(100.0, 140.0)),
        large=CurryPortionSize(category="Large", typical_volume_ml=180.0, typical_grams=182.0, gram_range=(155.0, 210.0)),
        extra_large=CurryPortionSize(category="Extra Large", typical_volume_ml=250.0, typical_grams=253.0, gram_range=(220.0, 290.0)),
        density_g_ml=1.01,
        notes="Very thin, aromatic pepper-tamarind broth."
    ),
    "kuzhambu": CurryPortionConfig(
        curry_family="kuzhambu",
        small=CurryPortionSize(category="Small", typical_volume_ml=90.0, typical_grams=96.0, gram_range=(80.0, 110.0)),
        medium=CurryPortionSize(category="Medium", typical_volume_ml=140.0, typical_grams=150.0, gram_range=(125.0, 175.0)),
        large=CurryPortionSize(category="Large", typical_volume_ml=220.0, typical_grams=235.0, gram_range=(200.0, 270.0)),
        extra_large=CurryPortionSize(category="Extra Large", typical_volume_ml=320.0, typical_grams=342.0, gram_range=(295.0, 390.0)),
        density_g_ml=1.07,
        notes="Puli or Kara kuzhambu with tamarind, gingelly oil glaze, and vegetables."
    ),
    "kootu": CurryPortionConfig(
        curry_family="kootu",
        small=CurryPortionSize(category="Small", typical_volume_ml=90.0, typical_grams=100.0, gram_range=(85.0, 115.0)),
        medium=CurryPortionSize(category="Medium", typical_volume_ml=140.0, typical_grams=155.0, gram_range=(130.0, 180.0)),
        large=CurryPortionSize(category="Large", typical_volume_ml=220.0, typical_grams=245.0, gram_range=(210.0, 280.0)),
        extra_large=CurryPortionSize(category="Extra Large", typical_volume_ml=320.0, typical_grams=355.0, gram_range=(310.0, 400.0)),
        density_g_ml=1.12,
        notes="Thick vegetable, moong dal, and ground coconut stew."
    ),
    "kadhi": CurryPortionConfig(
        curry_family="kadhi",
        small=CurryPortionSize(category="Small", typical_volume_ml=100.0, typical_grams=106.0, gram_range=(90.0, 120.0)),
        medium=CurryPortionSize(category="Medium", typical_volume_ml=160.0, typical_grams=170.0, gram_range=(145.0, 195.0)),
        large=CurryPortionSize(category="Large", typical_volume_ml=250.0, typical_grams=265.0, gram_range=(230.0, 305.0)),
        extra_large=CurryPortionSize(category="Extra Large", typical_volume_ml=360.0, typical_grams=382.0, gram_range=(330.0, 440.0)),
        density_g_ml=1.06,
        notes="Yogurt and gram flour simmered gravy with tempering."
    ),
    "paneer_curry": CurryPortionConfig(
        curry_family="paneer_curry",
        small=CurryPortionSize(category="Small", typical_volume_ml=120.0, typical_grams=135.0, gram_range=(115.0, 155.0)),
        medium=CurryPortionSize(category="Medium", typical_volume_ml=180.0, typical_grams=205.0, gram_range=(175.0, 235.0)),
        large=CurryPortionSize(category="Large", typical_volume_ml=260.0, typical_grams=295.0, gram_range=(255.0, 340.0)),
        extra_large=CurryPortionSize(category="Extra Large", typical_volume_ml=380.0, typical_grams=430.0, gram_range=(375.0, 495.0)),
        density_g_ml=1.14,
        notes="Paneer cubes in creamy makhani or rich onion-tomato gravy."
    ),
    "chicken_curry": CurryPortionConfig(
        curry_family="chicken_curry",
        small=CurryPortionSize(category="Small", typical_volume_ml=140.0, typical_grams=150.0, gram_range=(130.0, 175.0)),
        medium=CurryPortionSize(category="Medium", typical_volume_ml=200.0, typical_grams=220.0, gram_range=(190.0, 255.0)),
        large=CurryPortionSize(category="Large", typical_volume_ml=300.0, typical_grams=330.0, gram_range=(290.0, 380.0)),
        extra_large=CurryPortionSize(category="Extra Large", typical_volume_ml=420.0, typical_grams=460.0, gram_range=(400.0, 530.0)),
        density_g_ml=1.10,
        notes="Chicken pieces simmered in spiced gravy."
    ),
    "mutton_curry": CurryPortionConfig(
        curry_family="mutton_curry",
        small=CurryPortionSize(category="Small", typical_volume_ml=140.0, typical_grams=155.0, gram_range=(135.0, 180.0)),
        medium=CurryPortionSize(category="Medium", typical_volume_ml=210.0, typical_grams=235.0, gram_range=(200.0, 270.0)),
        large=CurryPortionSize(category="Large", typical_volume_ml=310.0, typical_grams=345.0, gram_range=(300.0, 395.0)),
        extra_large=CurryPortionSize(category="Extra Large", typical_volume_ml=430.0, typical_grams=480.0, gram_range=(420.0, 550.0)),
        density_g_ml=1.12,
        notes="Mutton chunks in rich aromatic gravy with roghan."
    ),
    "fish_curry": CurryPortionConfig(
        curry_family="fish_curry",
        small=CurryPortionSize(category="Small", typical_volume_ml=130.0, typical_grams=140.0, gram_range=(120.0, 165.0)),
        medium=CurryPortionSize(category="Medium", typical_volume_ml=190.0, typical_grams=205.0, gram_range=(175.0, 240.0)),
        large=CurryPortionSize(category="Large", typical_volume_ml=280.0, typical_grams=300.0, gram_range=(260.0, 350.0)),
        extra_large=CurryPortionSize(category="Extra Large", typical_volume_ml=400.0, typical_grams=430.0, gram_range=(380.0, 490.0)),
        density_g_ml=1.08,
        notes="Fish steaks/fillets in coconut or tamarind-tomato gravy."
    ),
    "kurma": CurryPortionConfig(
        curry_family="kurma",
        small=CurryPortionSize(category="Small", typical_volume_ml=110.0, typical_grams=125.0, gram_range=(105.0, 145.0)),
        medium=CurryPortionSize(category="Medium", typical_volume_ml=170.0, typical_grams=190.0, gram_range=(160.0, 220.0)),
        large=CurryPortionSize(category="Large", typical_volume_ml=250.0, typical_grams=280.0, gram_range=(240.0, 320.0)),
        extra_large=CurryPortionSize(category="Extra Large", typical_volume_ml=360.0, typical_grams=405.0, gram_range=(355.0, 465.0)),
        density_g_ml=1.13,
        notes="Coconut, cashew, poppy-seed rich kurma or salna."
    ),
    "poriyal": CurryPortionConfig(
        curry_family="poriyal",
        small=CurryPortionSize(category="Small", typical_volume_ml=80.0, typical_grams=75.0, gram_range=(65.0, 90.0)),
        medium=CurryPortionSize(category="Medium", typical_volume_ml=130.0, typical_grams=120.0, gram_range=(100.0, 145.0)),
        large=CurryPortionSize(category="Large", typical_volume_ml=200.0, typical_grams=190.0, gram_range=(165.0, 225.0)),
        extra_large=CurryPortionSize(category="Extra Large", typical_volume_ml=290.0, typical_grams=275.0, gram_range=(240.0, 320.0)),
        density_g_ml=0.95,
        notes="Stir-fried dry vegetable with mustard seeds and grated coconut."
    ),
}


class CurryFloatingOilEstimator:
    """
    Estimates added floating oil/fat layer (Tari/Roghan) on the curry surface.
    Section 38 & 47.
    """
    TIERS = {
        "low": {"name": "Low Sheen", "added_oil_grams": 2.0, "gram_range": (0.0, 3.0), "calorie_bump": 18.0},
        "medium": {"name": "Medium Sheen", "added_oil_grams": 6.0, "gram_range": (4.0, 8.0), "calorie_bump": 54.0},
        "high": {"name": "High Sheen / Roghan", "added_oil_grams": 14.0, "gram_range": (10.0, 18.0), "calorie_bump": 126.0},
        "extreme": {"name": "Extreme Sheen", "added_oil_grams": 23.0, "gram_range": (18.0, 28.0), "calorie_bump": 207.0},
    }

    @classmethod
    def estimate_floating_oil(cls, visual_features: Dict[str, Any]) -> Dict[str, Any]:
        sheen_level = visual_features.get("oil_sheen", "medium").lower()
        if "extreme" in sheen_level or "heavy_tari" in sheen_level:
            selected = cls.TIERS["extreme"]
            uncertainty_pct = 0.35
        elif "high" in sheen_level or "roghan" in sheen_level:
            selected = cls.TIERS["high"]
            uncertainty_pct = 0.25
        elif "low" in sheen_level or "homestyle" in sheen_level or "no_visible_oil" in sheen_level:
            selected = cls.TIERS["low"]
            uncertainty_pct = 0.15
        else:
            selected = cls.TIERS["medium"]
            uncertainty_pct = 0.20

        return {
            "tier_name": selected["name"],
            "added_oil_grams": selected["added_oil_grams"],
            "added_oil_gram_range": selected["gram_range"],
            "calorie_bump": selected["calorie_bump"],
            "uncertainty_pct": uncertainty_pct,
            "rationale": f"Estimated based on surface oil sheen: {selected['name']} ({selected['added_oil_grams']}g fat)."
        }


class ProteinGravySplitResult(BaseModel):
    total_weight_g: float
    protein_type: str
    piece_count: int
    piece_weight_total_g: float
    gravy_weight_g: float
    bone_weight_g: float
    edible_meat_weight_g: float
    is_bone_in: bool
    mass_conservation_check: bool = True


class CurryProteinGravySplitter:
    """
    Deconstructs protein-based curries into discrete piece mass and gravy mass.
    Implements Sections 17, 23, 44, and 68.
    Zero double counting: total_weight = piece_weight + gravy_weight.
    """
    TYPICAL_PIECE_WEIGHTS: Dict[str, float] = {
        "chicken_bone_in": 45.0,     # Standard curry cut piece with bone (~45g, of which ~12g bone)
        "chicken_boneless": 32.0,    # Tikka/curry cube
        "mutton_bone_in": 50.0,      # Curry cut with bone (~50g, of which ~15g bone)
        "mutton_boneless": 35.0,
        "paneer_cube": 18.0,         # Standard commercial/home cube
        "fish_steak": 75.0,          # Cross-section steak piece
        "fish_fillet": 55.0,         # Boneless cut
        "egg_whole": 50.0,           # Whole boiled egg in curry
        "egg_half": 25.0,            # Half boiled egg
        "prawn": 15.0,               # Medium prawn
    }

    @classmethod
    def split_portion(
        cls,
        protein_type: str,
        total_dish_weight_g: float,
        piece_count: int,
        is_bone_in: bool = False
    ) -> ProteinGravySplitResult:
        ptype = protein_type.lower()
        if "chicken" in ptype:
            key = "chicken_bone_in" if is_bone_in else "chicken_boneless"
            bone_ratio = 0.28 if is_bone_in else 0.0
        elif "mutton" in ptype:
            key = "mutton_bone_in" if is_bone_in else "mutton_boneless"
            bone_ratio = 0.32 if is_bone_in else 0.0
        elif "paneer" in ptype:
            key = "paneer_cube"
            bone_ratio = 0.0
        elif "fish" in ptype:
            key = "fish_steak" if is_bone_in else "fish_fillet"
            bone_ratio = 0.15 if is_bone_in else 0.0
        elif "egg" in ptype:
            key = "egg_whole"
            bone_ratio = 0.0
        elif "prawn" in ptype:
            key = "prawn"
            bone_ratio = 0.0
        else:
            key = "chicken_bone_in"
            bone_ratio = 0.28

        typical_unit = cls.TYPICAL_PIECE_WEIGHTS.get(key, 35.0)
        estimated_piece_weight = min(float(piece_count) * typical_unit, total_dish_weight_g * 0.70)
        gravy_weight = max(total_dish_weight_g - estimated_piece_weight, total_dish_weight_g * 0.30)
        # Recalibrate piece weight to strictly satisfy total = piece + gravy
        actual_piece_weight = round(total_dish_weight_g - gravy_weight, 1)

        bone_weight = round(actual_piece_weight * bone_ratio, 1)
        edible_meat_weight = round(actual_piece_weight - bone_weight, 1)

        return ProteinGravySplitResult(
            total_weight_g=round(total_dish_weight_g, 1),
            protein_type=protein_type,
            piece_count=piece_count,
            piece_weight_total_g=actual_piece_weight,
            gravy_weight_g=round(gravy_weight, 1),
            bone_weight_g=bone_weight,
            edible_meat_weight_g=edible_meat_weight,
            is_bone_in=is_bone_in,
            mass_conservation_check=(round(actual_piece_weight + gravy_weight, 1) == round(total_dish_weight_g, 1))
        )


class CurryPortionEngine:
    """
    Main curry portion inference engine.
    Calculates estimated portion grams, volumes, density, and oil bumps.
    """
    @staticmethod
    def get_portion_config(curry_family: str) -> CurryPortionConfig:
        fam = curry_family.lower()
        for key, cfg in CURRY_PORTION_DATABASE.items():
            if key in fam or fam in key:
                return cfg
        return CURRY_PORTION_DATABASE["dal"]

    @classmethod
    def estimate_curry_portion(
        cls,
        curry_family: str,
        portion_category: str = "Medium",
        vessel_type: Optional[str] = None,
        consistency: str = "Medium",
        visual_features: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        cfg = cls.get_portion_config(curry_family)
        cat = portion_category.capitalize()
        if cat == "Small":
            size_data = cfg.small
        elif cat == "Large":
            size_data = cfg.large
        elif cat == "Extra Large" or cat == "Extra_large" or cat == "Xl":
            size_data = cfg.extra_large
        else:
            size_data = cfg.medium

        # Density based on consistency
        density = CONSISTENCY_DENSITY_MAP.get(consistency, cfg.density_g_ml)

        # Container volume adjustment if recognized
        if vessel_type and vessel_type in VESSEL_VOLUME_MAP:
            volume_ml = VESSEL_VOLUME_MAP[vessel_type]
            grams = round(volume_ml * density, 1)
            gram_range = (round(grams * 0.88, 1), round(grams * 1.15, 1))
        else:
            volume_ml = size_data.typical_volume_ml
            grams = size_data.typical_grams
            gram_range = size_data.gram_range

        # Floating oil
        features = visual_features or {}
        oil_data = CurryFloatingOilEstimator.estimate_floating_oil(features)

        return {
            "curry_family": cfg.curry_family,
            "portion_category": cat,
            "volume_ml": volume_ml,
            "weight_grams": grams,
            "gram_range": gram_range,
            "density_g_ml": density,
            "consistency": consistency,
            "oil_sheen_data": oil_data,
            "notes": cfg.notes
        }
