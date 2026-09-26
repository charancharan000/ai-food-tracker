"""
Rice & Biryani Portion Engine, Rice-to-Meat Ratio & Ghee Modeler (Part 9)
Implements Sections 46, 47, 48, 49, 50, 51 of Part 9 Master Training Specification.

Guarantees:
- Food-specific portion database:
  * Distinct calibrated portion ranges for Small, Medium, Large, and Extra Large.
  * Different baselines for Biryani, Plain Rice, Fried Rice, Pulao, and Curd Rice (Section 50).
- Rice-to-Meat Ratio Modeling (Section 46):
  * Deconstructs biryani into separate rice mass and meat mass rather than opaque monolithic weight.
- Ghee & Oil Estimator (Section 47):
  * Categories: Low, Medium, High, Unknown.
  * Never claims exact ghee grams from image alone; widens calorie uncertainty intervals for high/unknown fat.
- Fried Onion (Birista) & Dry Fruit Detection (Sections 48 & 49):
  * Explicit caloric density adjustments for birista, cashews, and raisins.
"""

from typing import Dict, Any, Optional, Tuple, List
from pydantic import BaseModel, Field


class RicePortionSize(BaseModel):
    category: str  # "Small", "Medium", "Large", "Extra Large"
    typical_grams: float
    gram_range: Tuple[float, float]


class RiceFoodPortionConfig(BaseModel):
    dish_family: str  # "biryani", "plain_rice", "pulao", "fried_rice", "curd_rice", "khichdi", "pongal"
    small: RicePortionSize
    medium: RicePortionSize
    large: RicePortionSize
    extra_large: RicePortionSize
    density_g_cm3: float = 0.85
    notes: str


RICE_PORTION_DATABASE: Dict[str, RiceFoodPortionConfig] = {
    "biryani": RiceFoodPortionConfig(
        dish_family="biryani",
        small=RicePortionSize(category="Small", typical_grams=250.0, gram_range=(200.0, 290.0)),
        medium=RicePortionSize(category="Medium", typical_grams=380.0, gram_range=(320.0, 440.0)),
        large=RicePortionSize(category="Large", typical_grams=520.0, gram_range=(450.0, 590.0)),
        extra_large=RicePortionSize(category="Extra Large", typical_grams=700.0, gram_range=(600.0, 850.0)),
        density_g_cm3=0.83,
        notes="Standard restaurant biryani serving is 380-450g including meat and rice."
    ),
    "plain_rice": RiceFoodPortionConfig(
        dish_family="plain_rice",
        small=RicePortionSize(category="Small", typical_grams=150.0, gram_range=(120.0, 180.0)),
        medium=RicePortionSize(category="Medium", typical_grams=240.0, gram_range=(190.0, 290.0)),
        large=RicePortionSize(category="Large", typical_grams=350.0, gram_range=(300.0, 420.0)),
        extra_large=RicePortionSize(category="Extra Large", typical_grams=480.0, gram_range=(430.0, 580.0)),
        density_g_cm3=0.81,
        notes="Steamed plain rice cup/katori or heap."
    ),
    "pulao": RiceFoodPortionConfig(
        dish_family="pulao",
        small=RicePortionSize(category="Small", typical_grams=180.0, gram_range=(150.0, 220.0)),
        medium=RicePortionSize(category="Medium", typical_grams=300.0, gram_range=(240.0, 360.0)),
        large=RicePortionSize(category="Large", typical_grams=420.0, gram_range=(370.0, 480.0)),
        extra_large=RicePortionSize(category="Extra Large", typical_grams=550.0, gram_range=(490.0, 650.0)),
        density_g_cm3=0.82,
        notes="Veg, peas, or meat pulao."
    ),
    "fried_rice": RiceFoodPortionConfig(
        dish_family="fried_rice",
        small=RicePortionSize(category="Small", typical_grams=200.0, gram_range=(160.0, 240.0)),
        medium=RicePortionSize(category="Medium", typical_grams=320.0, gram_range=(260.0, 380.0)),
        large=RicePortionSize(category="Large", typical_grams=440.0, gram_range=(390.0, 500.0)),
        extra_large=RicePortionSize(category="Extra Large", typical_grams=580.0, gram_range=(510.0, 700.0)),
        density_g_cm3=0.84,
        notes="Wok stir-fried rice."
    ),
    "curd_rice": RiceFoodPortionConfig(
        dish_family="curd_rice",
        small=RicePortionSize(category="Small", typical_grams=180.0, gram_range=(140.0, 220.0)),
        medium=RicePortionSize(category="Medium", typical_grams=280.0, gram_range=(230.0, 340.0)),
        large=RicePortionSize(category="Large", typical_grams=390.0, gram_range=(350.0, 450.0)),
        extra_large=RicePortionSize(category="Extra Large", typical_grams=520.0, gram_range=(460.0, 620.0)),
        density_g_cm3=0.92,
        notes="Dense tempered curd rice bowl."
    ),
    "pongal": RiceFoodPortionConfig(
        dish_family="pongal",
        small=RicePortionSize(category="Small", typical_grams=180.0, gram_range=(150.0, 220.0)),
        medium=RicePortionSize(category="Medium", typical_grams=280.0, gram_range=(240.0, 340.0)),
        large=RicePortionSize(category="Large", typical_grams=400.0, gram_range=(350.0, 460.0)),
        extra_large=RicePortionSize(category="Extra Large", typical_grams=540.0, gram_range=(470.0, 650.0)),
        density_g_cm3=0.96,
        notes="Mashed ghee ven pongal or sweet pongal."
    )
}


# =============================================================================
# SECTION 46 — RICE-TO-MEAT RATIO ESTIMATOR
# =============================================================================

class RiceToMeatSplitResult(BaseModel):
    total_biryani_mass_g: float
    rice_mass_g: float
    meat_mass_g: float
    rice_percentage: float
    meat_percentage: float
    protein_type: str
    meat_pieces_count: int


class RiceToMeatRatioEstimator:
    """
    Implements Section 46:
    Estimates explicit rice-to-meat ratio (e.g. Rice: 350g, Chicken: 120g)
    rather than treating biryani as a monolithic 470g block.
    """
    @staticmethod
    def estimate_split(
        total_mass_g: float,
        protein_type: str = "chicken",
        visible_meat_pieces: Optional[int] = None
    ) -> RiceToMeatSplitResult:
        if "veg" in protein_type.lower() or "plain" in protein_type.lower():
            return RiceToMeatSplitResult(
                total_biryani_mass_g=total_mass_g,
                rice_mass_g=total_mass_g,
                meat_mass_g=0.0,
                rice_percentage=100.0,
                meat_percentage=0.0,
                protein_type="vegetarian",
                meat_pieces_count=0
            )

        # Standard piece mass
        unit_piece_mass = 55.0 if "chicken" in protein_type.lower() else (45.0 if "mutton" in protein_type.lower() else 18.0)

        if visible_meat_pieces is not None and visible_meat_pieces > 0:
            pieces = visible_meat_pieces
            meat_g = min(total_mass_g * 0.50, pieces * unit_piece_mass)
            rice_g = total_mass_g - meat_g
        else:
            # Typical ratio: 72% rice, 28% meat
            meat_g = total_mass_g * 0.28
            rice_g = total_mass_g - meat_g
            pieces = max(1, int(round(meat_g / unit_piece_mass)))

        meat_pct = round((meat_g / total_mass_g) * 100.0, 1)
        rice_pct = round(100.0 - meat_pct, 1)

        return RiceToMeatSplitResult(
            total_biryani_mass_g=round(total_mass_g, 1),
            rice_mass_g=round(rice_g, 1),
            meat_mass_g=round(meat_g, 1),
            rice_percentage=rice_pct,
            meat_percentage=meat_pct,
            protein_type=protein_type,
            meat_pieces_count=pieces
        )


# =============================================================================
# SECTION 47 — RICE OIL & GHEE ESTIMATOR
# =============================================================================

class RiceFatEstimationResult(BaseModel):
    fat_level: str  # "Low", "Medium", "High", "Unknown"
    fat_multiplier: float
    uncertainty_spread_pct: float
    notes: str


class RiceOilGheeEstimator:
    """
    Implements Section 47:
    - Never claims exact ghee or oil grams from image alone.
    - Categorizes into Low, Medium, High, or Unknown.
    """
    @staticmethod
    def estimate_fat(
        dish_family: str,
        surface_sheen: Optional[str] = None,  # "heavy_ghee_glaze", "moderate_sheen", "matte_dry"
        has_birista: bool = False
    ) -> RiceFatEstimationResult:
        sheen = (surface_sheen or "moderate_sheen").lower()

        if "pongal" in dish_family.lower() or sheen == "heavy_ghee_glaze":
            return RiceFatEstimationResult(
                fat_level="High",
                fat_multiplier=1.30,
                uncertainty_spread_pct=16.0,
                notes="Intense desi ghee glaze and surface sheen observed. Expanded calorie interval applied."
            )

        elif "biryani" in dish_family.lower() or has_birista:
            if sheen == "heavy_ghee_glaze":
                return RiceFatEstimationResult(
                    fat_level="High",
                    fat_multiplier=1.25,
                    uncertainty_spread_pct=15.0,
                    notes="High oil/ghee marbling with heavy fried onion coating."
                )
            else:
                return RiceFatEstimationResult(
                    fat_level="Medium",
                    fat_multiplier=1.10,
                    uncertainty_spread_pct=12.0,
                    notes="Standard restaurant/dum biryani fat glaze."
                )

        elif "plain" in dish_family.lower() or sheen == "matte_dry":
            return RiceFatEstimationResult(
                fat_level="Low",
                fat_multiplier=0.85,
                uncertainty_spread_pct=7.0,
                notes="Dry steamed grains with negligible added fat."
            )

        else:
            return RiceFatEstimationResult(
                fat_level="Unknown",
                fat_multiplier=1.00,
                uncertainty_spread_pct=20.0,
                notes="Oil/ghee quantity cannot be definitively determined from image appearance alone per Section 47."
            )


# =============================================================================
# SECTIONS 48 & 49 — FRIED ONIONS & DRIED FRUIT GARNISH
# =============================================================================

class RiceGarnishAddition(BaseModel):
    garnish_name: str
    mass_g: float
    calories: float
    protein_g: float
    carbs_g: float
    fat_g: float


class RiceGarnishCalculator:
    """
    Implements Sections 48 & 49:
    Accounts for fried onion (birista) and nuts/raisin additions.
    """
    @staticmethod
    def calculate_birista(intensity: str = "standard") -> RiceGarnishAddition:
        mult = 0.5 if intensity == "light" else (1.6 if intensity == "heavy" else 1.0)
        mass = 15.0 * mult
        cals = 58.0 * mult
        fat = 4.2 * mult
        return RiceGarnishAddition(
            garnish_name="Caramelized Fried Onions (Birista)",
            mass_g=round(mass, 1),
            calories=round(cals, 1),
            protein_g=round(0.6 * mult, 1),
            carbs_g=round(4.8 * mult, 1),
            fat_g=round(fat, 1)
        )

    @staticmethod
    def calculate_nuts_and_raisins(intensity: str = "standard") -> RiceGarnishAddition:
        mult = 0.5 if intensity == "light" else (1.5 if intensity == "heavy" else 1.0)
        mass = 20.0 * mult
        cals = 110.0 * mult
        fat = 7.5 * mult
        return RiceGarnishAddition(
            garnish_name="Golden Fried Cashews & Sultana Raisins",
            mass_g=round(mass, 1),
            calories=round(cals, 1),
            protein_g=round(2.6 * mult, 1),
            carbs_g=round(9.2 * mult, 1),
            fat_g=round(fat, 1)
        )
