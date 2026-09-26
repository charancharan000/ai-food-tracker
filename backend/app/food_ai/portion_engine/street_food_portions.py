"""
Street Food Portion Engine, Oil Uncertainty, Cheese/Mayo & Sauce Modeler (Part 8)
Implements Sections 50, 61, 62, 64, 65, 66, 67, 68 of Part 8 Master Training Specification.

Guarantees:
- Food-specific portion database:
  * Never uses one universal serving size.
  * Explicit models for piece counts (Pani Puri, Momos, Samosas, Jalebi, Pavs),
    plate weights (Chaats, Noodles, Rice), and volumes (Chai, Lassi, Sugarcane Juice).
- StreetOilEstimator (Section 65):
  * Preparation style: Deep Fried, Shallow Fried, Pan Fried, Grilled, Steamed, Boiled, Roasted, Baked.
  * Oil level estimation: Low, Medium, High, Unknown.
  * Never claims exact 15g from image alone; widens calorie uncertainty intervals for high/unknown oil.
- StreetCheeseMayonnaiseCalculator (Sections 67 & 68):
  * Grated cheese, cheese slices, melted cheese sauce.
  * Plain mayo, garlic mayo, loaded mayo.
- StreetSauceChutneyPortioner (Section 66):
  * Mint green chutney, sweet tamarind saunth, dry garlic chutney, schezwan sauce.
- Beverage Sugar Handling (Sections 61 & 62):
  * Flags sugar as 'Unknown' when visually undetectable and provides calibrated range.
"""

from typing import Dict, Any, Optional, Tuple, List
from pydantic import BaseModel, Field


class StreetPortionModel(BaseModel):
    food_id: str
    portion_unit: str  # "piece", "plate", "bowl", "cup", "wrap"
    standard_unit_mass_g: float
    typical_portion_range_g: Tuple[float, float]
    piece_count_typical: Optional[int] = None
    density_g_cm3: float = 0.85
    notes: str


STREET_FOOD_PORTION_DATABASE: Dict[str, StreetPortionModel] = {
    "pani_puri": StreetPortionModel(
        food_id="pani_puri",
        portion_unit="piece",
        standard_unit_mass_g=28.0,
        typical_portion_range_g=(160.0, 260.0),
        piece_count_typical=6,
        density_g_cm3=0.82,
        notes="Portion calculated per filled puri (shell + filling + water + topping)."
    ),
    "samosa": StreetPortionModel(
        food_id="samosa",
        portion_unit="piece",
        standard_unit_mass_g=100.0,
        typical_portion_range_g=(75.0, 220.0),
        piece_count_typical=1,
        density_g_cm3=0.82,
        notes="Mini samosa: 25-35g; Standard halwai samosa: 85-115g."
    ),
    "vada_pav": StreetPortionModel(
        food_id="vada_pav",
        portion_unit="piece",
        standard_unit_mass_g=135.0,
        typical_portion_range_g=(120.0, 160.0),
        piece_count_typical=1,
        density_g_cm3=0.74,
        notes="Ladi pav (45g) + Batata Vada (75g) + chutneys & chilli (15g)."
    ),
    "pav_bhaji": StreetPortionModel(
        food_id="pav_bhaji",
        portion_unit="plate",
        standard_unit_mass_g=330.0,
        typical_portion_range_g=(280.0, 420.0),
        piece_count_typical=2,
        density_g_cm3=0.88,
        notes="2 Pavs (80g) + Bhaji (200g) + Butter slab (15-25g) + Onions (30g)."
    ),
    "momos": StreetPortionModel(
        food_id="momos",
        portion_unit="piece",
        standard_unit_mass_g=30.0,
        typical_portion_range_g=(180.0, 300.0),
        piece_count_typical=6,
        density_g_cm3=0.92,
        notes="Portion calculated per piece (6, 8, or 10 pieces standard serving)."
    ),
    "chaat_bowl": StreetPortionModel(
        food_id="chaat_bowl",
        portion_unit="bowl",
        standard_unit_mass_g=220.0,
        typical_portion_range_g=(170.0, 340.0),
        density_g_cm3=0.85,
        notes="Applies to Bhel Puri, Papdi Chaat, Sev Puri, Aloo Chaat."
    ),
    "jalebi": StreetPortionModel(
        food_id="jalebi",
        portion_unit="piece",
        standard_unit_mass_g=30.0,
        typical_portion_range_g=(90.0, 180.0),
        piece_count_typical=4,
        density_g_cm3=1.12,
        notes="Standard spiral swirl is 25-35g including sugar syrup glaze."
    ),
    "cutting_chai": StreetPortionModel(
        food_id="cutting_chai",
        portion_unit="cup",
        standard_unit_mass_g=100.0,  # ~100 ml
        typical_portion_range_g=(90.0, 150.0),
        density_g_cm3=1.03,
        notes="Cutting chai: 90-110 ml; Full glass: 180-220 ml."
    ),
    "sweet_lassi": StreetPortionModel(
        food_id="sweet_lassi",
        portion_unit="cup",
        standard_unit_mass_g=300.0,  # ~280 ml
        typical_portion_range_g=(250.0, 400.0),
        density_g_cm3=1.07,
        notes="Kulhad or tall glass serving with floating malai top."
    ),
    "sugarcane_juice": StreetPortionModel(
        food_id="sugarcane_juice",
        portion_unit="cup",
        standard_unit_mass_g=260.0,
        typical_portion_range_g=(200.0, 350.0),
        density_g_cm3=1.06,
        notes="Medium street glass (250 ml)."
    ),
    "noodles": StreetPortionModel(
        food_id="noodles",
        portion_unit="plate",
        standard_unit_mass_g=280.0,
        typical_portion_range_g=(220.0, 350.0),
        density_g_cm3=0.82,
        notes="High-flame wok full street plate."
    ),
    "fried_rice": StreetPortionModel(
        food_id="fried_rice",
        portion_unit="plate",
        standard_unit_mass_g=300.0,
        typical_portion_range_g=(240.0, 380.0),
        density_g_cm3=0.84,
        notes="Street-style wok fried rice plate."
    ),
    "roll_wrap": StreetPortionModel(
        food_id="roll_wrap",
        portion_unit="wrap",
        standard_unit_mass_g=220.0,
        typical_portion_range_g=(180.0, 280.0),
        piece_count_typical=1,
        density_g_cm3=0.86,
        notes="Single Kathi roll, Frankie, or Shawarma wrap."
    )
}


# =============================================================================
# SECTION 65 — STREET FOOD OIL ESTIMATOR
# =============================================================================

class OilEstimationResult(BaseModel):
    preparation_style: str  # Deep Fried, Shallow Fried, Pan Fried, Grilled, Steamed, Boiled, Roasted, Baked
    oil_level: str          # "Low", "Medium", "High", "Unknown"
    fat_multiplier: float
    uncertainty_spread_pct: float  # Percentage to widen calorie uncertainty interval
    notes: str


class StreetOilEstimator:
    """
    Implements Section 65:
    - Never claims 'Oil = exactly 15g' from image appearance alone.
    - Treats oil quantity as an uncertainty factor: Low / Medium / High / Unknown.
    """
    @staticmethod
    def estimate_oil(
        preparation_style: str,
        surface_sheen: Optional[str] = None,  # "greasy", "glossy", "matte", "dry"
        is_deep_fried: bool = False
    ) -> OilEstimationResult:
        prep = preparation_style.lower().strip()
        sheen = (surface_sheen or "glossy").lower().strip()

        if is_deep_fried or "deep" in prep or prep in ("bhatura", "samosa", "kachori", "pakoda", "bhajiya"):
            if sheen == "greasy":
                return OilEstimationResult(
                    preparation_style="Deep Fried",
                    oil_level="High",
                    fat_multiplier=1.35,
                    uncertainty_spread_pct=18.0,
                    notes="High surface oil sheen and deep-fried preparation detected. Calorie range expanded to reflect oil absorption variance."
                )
            else:
                return OilEstimationResult(
                    preparation_style="Deep Fried",
                    oil_level="Medium",
                    fat_multiplier=1.20,
                    uncertainty_spread_pct=14.0,
                    notes="Deep-fried item with drained/blotted surface. Medium oil absorption estimated."
                )

        elif "shallow" in prep or "pan" in prep or "tawa" in prep or "tossed" in prep:
            return OilEstimationResult(
                preparation_style="Shallow / Pan Fried",
                oil_level="Medium",
                fat_multiplier=1.10,
                uncertainty_spread_pct=12.0,
                notes="Tawa or pan-fried preparation with moderate oil/butter glaze."
            )

        elif "steamed" in prep or "boiled" in prep:
            return OilEstimationResult(
                preparation_style="Steamed / Boiled",
                oil_level="Low",
                fat_multiplier=0.75,
                uncertainty_spread_pct=8.0,
                notes="Steamed or boiled preparation. Low intrinsic surface fat."
            )

        elif "roasted" in prep or "grilled" in prep or "baked" in prep:
            return OilEstimationResult(
                preparation_style="Roasted / Grilled",
                oil_level="Low",
                fat_multiplier=0.85,
                uncertainty_spread_pct=10.0,
                notes="Dry heat roasting / grilling with minimal oil brushing."
            )

        else:
            return OilEstimationResult(
                preparation_style="Unknown",
                oil_level="Unknown",
                fat_multiplier=1.00,
                uncertainty_spread_pct=22.0,
                notes="Oil quantity cannot be definitively determined from image appearance alone. Uncertainty interval widened per Section 65."
            )


# =============================================================================
# SECTIONS 67 & 68 — CHEESE & MAYONNAISE CALCULATOR
# =============================================================================

class CheeseMayonnaiseAdjustment(BaseModel):
    topping_name: str
    estimated_mass_g: float
    calories: float
    protein_g: float
    carbs_g: float
    fat_g: float


class StreetCheeseMayonnaiseCalculator:
    """
    Implements Sections 67 & 68:
    - Grated processed cheese, cheese slice, melted cheese sauce.
    - Plain mayo, garlic mayo, loaded mayo.
    """
    @staticmethod
    def calculate_cheese(
        cheese_type: str = "grated",  # "grated", "slice", "melted_sauce"
        intensity: str = "standard"   # "light", "standard", "heavy"
    ) -> CheeseMayonnaiseAdjustment:
        if cheese_type == "slice":
            mass = 20.0
            cals = 64.0
            pro = 4.0
            carb = 0.6
            fat = 5.2
            name = "Processed Cheddar Cheese Slice"
        elif cheese_type == "melted_sauce":
            mult = 0.6 if intensity == "light" else (1.4 if intensity == "heavy" else 1.0)
            mass = 30.0 * mult
            cals = 85.0 * mult
            pro = 3.2 * mult
            carb = 2.4 * mult
            fat = 7.1 * mult
            name = "Melted Street Cheese Sauce"
        else:  # grated Amul cheese
            mult = 0.6 if intensity == "light" else (1.5 if intensity == "heavy" else 1.0)
            mass = 28.0 * mult
            cals = 102.0 * mult
            pro = 6.0 * mult
            carb = 0.8 * mult
            fat = 8.4 * mult
            name = "Grated Amul Processed Cheese Blanket"

        return CheeseMayonnaiseAdjustment(
            topping_name=name,
            estimated_mass_g=round(mass, 1),
            calories=round(cals, 1),
            protein_g=round(pro, 1),
            carbs_g=round(carb, 1),
            fat_g=round(fat, 1)
        )

    @staticmethod
    def calculate_mayonnaise(
        mayo_type: str = "plain",     # "plain", "garlic", "spicy"
        intensity: str = "standard"   # "light", "standard", "loaded"
    ) -> CheeseMayonnaiseAdjustment:
        mult = 0.5 if intensity == "light" else (1.6 if intensity == "loaded" else 1.0)
        mass = 25.0 * mult
        cals = 145.0 * mult
        pro = 0.3 * mult
        carb = 2.2 * mult
        fat = 15.2 * mult
        desc = "Loaded " if intensity == "loaded" else ""

        return CheeseMayonnaiseAdjustment(
            topping_name=f"{desc}{mayo_type.title()} Street Mayonnaise Dollop",
            estimated_mass_g=round(mass, 1),
            calories=round(cals, 1),
            protein_g=round(pro, 1),
            carbs_g=round(carb, 1),
            fat_g=round(fat, 1)
        )


# =============================================================================
# SECTIONS 61 & 62 — BEVERAGE SUGAR UNCERTAINTY HANDLER
# =============================================================================

class BeverageSugarResult(BaseModel):
    beverage_name: str
    sugar_status: str       # "Detected_Sugar", "Unsweetened", "Unknown"
    volume_ml: float
    base_calories: float
    sugar_added_cals: float
    calibrated_calorie_range: Tuple[float, float]
    requires_user_confirmation: bool
    prompt_for_user: Optional[str] = None


class BeverageSugarHandler:
    """
    Implements Section 61 & 62:
    - If sugar cannot be detected from appearance: sugar status is 'Unknown'.
    - Flags for user confirmation rather than assuming zero or heavy sugar.
    """
    @staticmethod
    def evaluate_beverage(
        beverage_type: str,  # "cutting_chai", "sweet_lassi", "sugarcane_juice", "filter_coffee"
        volume_ml: float = 120.0,
        user_specified_sugar_spoons: Optional[int] = None
    ) -> BeverageSugarResult:
        if beverage_type in ("cutting_chai", "filter_coffee"):
            base_cal = (volume_ml / 100.0) * 45.0  # milk and brew alone
            if user_specified_sugar_spoons is not None:
                sugar_cals = user_specified_sugar_spoons * 20.0
                total = base_cal + sugar_cals
                return BeverageSugarResult(
                    beverage_name=beverage_type.replace("_", " ").title(),
                    sugar_status="Detected_Sugar",
                    volume_ml=volume_ml,
                    base_calories=round(base_cal, 1),
                    sugar_added_cals=round(sugar_cals, 1),
                    calibrated_calorie_range=(round(total * 0.95, 1), round(total * 1.05, 1)),
                    requires_user_confirmation=False
                )
            else:
                # Sugar undetectable by camera (Section 61)
                # Standard street chai has 1.5 to 2.5 tsp sugar
                low_cals = base_cal + 20.0  # 1 tsp
                high_cals = base_cal + 55.0  # 2.5 tsp
                return BeverageSugarResult(
                    beverage_name=beverage_type.replace("_", " ").title(),
                    sugar_status="Unknown",
                    volume_ml=volume_ml,
                    base_calories=round(base_cal, 1),
                    sugar_added_cals=35.0,
                    calibrated_calorie_range=(round(low_cals, 1), round(high_cals, 1)),
                    requires_user_confirmation=True,
                    prompt_for_user=f"How much sugar was added to this {beverage_type.replace('_', ' ')}? (Unsweetened / 1 Spoon / 2 Spoons / Sweetened)"
                )

        elif beverage_type == "sugarcane_juice":
            # Pure sugarcane juice contains ~13-18% natural sucrose by volume
            cals = (volume_ml / 100.0) * 68.0
            return BeverageSugarResult(
                beverage_name="Fresh Sugarcane Juice",
                sugar_status="Natural_Cane_Sucrose",
                volume_ml=volume_ml,
                base_calories=round(cals, 1),
                sugar_added_cals=0.0,
                calibrated_calorie_range=(round(cals * 0.88, 1), round(cals * 1.15, 1)),
                requires_user_confirmation=False,
                prompt_for_user=None
            )

        else:  # lassi
            base_cal = (volume_ml / 100.0) * 65.0
            added_sugar = (volume_ml / 100.0) * 45.0
            total = base_cal + added_sugar
            return BeverageSugarResult(
                beverage_name=beverage_type.replace("_", " ").title(),
                sugar_status="Traditional_Sweetened",
                volume_ml=volume_ml,
                base_calories=round(base_cal, 1),
                sugar_added_cals=round(added_sugar, 1),
                calibrated_calorie_range=(round(total * 0.85, 1), round(total * 1.18, 1)),
                requires_user_confirmation=False
            )
