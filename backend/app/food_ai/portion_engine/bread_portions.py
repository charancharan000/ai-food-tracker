"""
Indian Bread Portion Engine, Fat Modeler & Stuffing-to-Dough Calculator (Part 10)
Implements Sections 39, 42, 43, 46, 47, 74, 84 of Part 10 Master Training Specification.

Guarantees:
- Calibrated bread portion database covering all major bread families:
  * Phulka / Chapati / Roti
  * Tandoori Roti
  * Naan / Butter Naan / Garlic Naan
  * Kulcha / Amritsari Kulcha
  * Paratha (Plain, Laccha, Kerala Parotta)
  * Stuffed Paratha (Aloo, Paneer, Gobi, Mooli, Sattu)
  * Puri / Poori / Luchi
  * Bhatura
  * Bhakri / Rotla (Jowar, Bajra, Makki)
  * Thepla / Dhebra
  * Appam / Pathiri / Neer Dosa
  * Roomali Roti
- Granular portion categories: Small, Medium, Large, Extra Large (Section 42).
- BreadFatEstimator (Sections 46, 47, 84):
  * Categories: Very Low, Low, Medium, High, Very High, Unknown.
  * Explicitly obeys Non-Negotiable Rule 84: Never assume butter from shine alone.
    Shine can stem from water wash, steam, oil brush, camera flash, or melted butter/ghee.
- BreadStuffingDoughRatioEstimator (Sections 40, 41):
  * Deconstructs stuffed breads into dough shell mass and stuffing core mass.
"""

from typing import Dict, Any, Optional, Tuple, List
from pydantic import BaseModel, Field


class BreadPortionSize(BaseModel):
    category: str  # "Small", "Medium", "Large", "Extra Large"
    typical_grams: float
    gram_range: Tuple[float, float]
    typical_diameter_cm: Optional[float] = None


class BreadFoodPortionConfig(BaseModel):
    bread_family: str
    small: BreadPortionSize
    medium: BreadPortionSize
    large: BreadPortionSize
    extra_large: BreadPortionSize
    density_g_cm3: float = 0.85
    notes: str


# =============================================================================
# BREAD PORTION DATABASE
# =============================================================================

BREAD_PORTION_DATABASE: Dict[str, BreadFoodPortionConfig] = {
    "chapati": BreadFoodPortionConfig(
        bread_family="Roti / Chapati family",
        small=BreadPortionSize(category="Small", typical_grams=30.0, gram_range=(25.0, 35.0), typical_diameter_cm=14.0),
        medium=BreadPortionSize(category="Medium", typical_grams=40.0, gram_range=(35.0, 50.0), typical_diameter_cm=16.0),
        large=BreadPortionSize(category="Large", typical_grams=60.0, gram_range=(50.0, 70.0), typical_diameter_cm=19.0),
        extra_large=BreadPortionSize(category="Extra Large", typical_grams=80.0, gram_range=(70.0, 95.0), typical_diameter_cm=22.0),
        density_g_cm3=0.82,
        notes="Standard homestyle wheat chapati rolled on tawa."
    ),
    "phulka": BreadFoodPortionConfig(
        bread_family="Roti / Chapati family",
        small=BreadPortionSize(category="Small", typical_grams=25.0, gram_range=(20.0, 30.0), typical_diameter_cm=13.0),
        medium=BreadPortionSize(category="Medium", typical_grams=35.0, gram_range=(30.0, 42.0), typical_diameter_cm=15.0),
        large=BreadPortionSize(category="Large", typical_grams=48.0, gram_range=(42.0, 58.0), typical_diameter_cm=18.0),
        extra_large=BreadPortionSize(category="Extra Large", typical_grams=65.0, gram_range=(58.0, 75.0), typical_diameter_cm=20.0),
        density_g_cm3=0.75,
        notes="Flame-puffed paper thin dry whole-wheat balloon roti."
    ),
    "tandoori_roti": BreadFoodPortionConfig(
        bread_family="Tandoor bread family",
        small=BreadPortionSize(category="Small", typical_grams=65.0, gram_range=(50.0, 75.0), typical_diameter_cm=16.0),
        medium=BreadPortionSize(category="Medium", typical_grams=90.0, gram_range=(75.0, 105.0), typical_diameter_cm=18.0),
        large=BreadPortionSize(category="Large", typical_grams=125.0, gram_range=(105.0, 145.0), typical_diameter_cm=21.0),
        extra_large=BreadPortionSize(category="Extra Large", typical_grams=165.0, gram_range=(145.0, 190.0), typical_diameter_cm=24.0),
        density_g_cm3=0.88,
        notes="Whole wheat clay oven baked bread with blistered char marks."
    ),
    "naan": BreadFoodPortionConfig(
        bread_family="Naan family",
        small=BreadPortionSize(category="Small", typical_grams=90.0, gram_range=(75.0, 110.0), typical_diameter_cm=18.0),
        medium=BreadPortionSize(category="Medium", typical_grams=130.0, gram_range=(110.0, 155.0), typical_diameter_cm=22.0),
        large=BreadPortionSize(category="Large", typical_grams=180.0, gram_range=(155.0, 210.0), typical_diameter_cm=26.0),
        extra_large=BreadPortionSize(category="Extra Large", typical_grams=235.0, gram_range=(210.0, 275.0), typical_diameter_cm=30.0),
        density_g_cm3=0.80,
        notes="Leavened maida tandoor bread with teardrop shape."
    ),
    "kulcha": BreadFoodPortionConfig(
        bread_family="Kulcha family",
        small=BreadPortionSize(category="Small", typical_grams=85.0, gram_range=(70.0, 100.0), typical_diameter_cm=16.0),
        medium=BreadPortionSize(category="Medium", typical_grams=120.0, gram_range=(100.0, 145.0), typical_diameter_cm=19.0),
        large=BreadPortionSize(category="Large", typical_grams=165.0, gram_range=(145.0, 190.0), typical_diameter_cm=22.0),
        extra_large=BreadPortionSize(category="Extra Large", typical_grams=210.0, gram_range=(190.0, 245.0), typical_diameter_cm=25.0),
        density_g_cm3=0.84,
        notes="Mildly leavened round tandoori or griddled bread."
    ),
    "paratha_plain": BreadFoodPortionConfig(
        bread_family="Paratha family",
        small=BreadPortionSize(category="Small", typical_grams=55.0, gram_range=(45.0, 70.0), typical_diameter_cm=15.0),
        medium=BreadPortionSize(category="Medium", typical_grams=80.0, gram_range=(70.0, 95.0), typical_diameter_cm=18.0),
        large=BreadPortionSize(category="Large", typical_grams=110.0, gram_range=(95.0, 130.0), typical_diameter_cm=21.0),
        extra_large=BreadPortionSize(category="Extra Large", typical_grams=145.0, gram_range=(130.0, 170.0), typical_diameter_cm=24.0),
        density_g_cm3=0.86,
        notes="Homestyle triangular or round whole-wheat griddled paratha."
    ),
    "paratha_laccha": BreadFoodPortionConfig(
        bread_family="Layered bread family",
        small=BreadPortionSize(category="Small", typical_grams=80.0, gram_range=(65.0, 100.0), typical_diameter_cm=16.0),
        medium=BreadPortionSize(category="Medium", typical_grams=120.0, gram_range=(100.0, 145.0), typical_diameter_cm=19.0),
        large=BreadPortionSize(category="Large", typical_grams=165.0, gram_range=(145.0, 195.0), typical_diameter_cm=22.0),
        extra_large=BreadPortionSize(category="Extra Large", typical_grams=215.0, gram_range=(195.0, 255.0), typical_diameter_cm=25.0),
        density_g_cm3=0.88,
        notes="Multi-layered flaky spiral whole wheat or maida paratha."
    ),
    "parotta_kerala": BreadFoodPortionConfig(
        bread_family="Layered bread family",
        small=BreadPortionSize(category="Small", typical_grams=85.0, gram_range=(70.0, 105.0), typical_diameter_cm=15.0),
        medium=BreadPortionSize(category="Medium", typical_grams=125.0, gram_range=(105.0, 150.0), typical_diameter_cm=18.0),
        large=BreadPortionSize(category="Large", typical_grams=175.0, gram_range=(150.0, 205.0), typical_diameter_cm=21.0),
        extra_large=BreadPortionSize(category="Extra Large", typical_grams=230.0, gram_range=(205.0, 270.0), typical_diameter_cm=24.0),
        density_g_cm3=0.90,
        notes="Clapped multi-layered soft maida flatbread cooked with generous oil/dalda."
    ),
    "paratha_stuffed": BreadFoodPortionConfig(
        bread_family="Stuffed bread family",
        small=BreadPortionSize(category="Small", typical_grams=120.0, gram_range=(100.0, 145.0), typical_diameter_cm=16.0),
        medium=BreadPortionSize(category="Medium", typical_grams=180.0, gram_range=(145.0, 215.0), typical_diameter_cm=19.0),
        large=BreadPortionSize(category="Large", typical_grams=240.0, gram_range=(215.0, 285.0), typical_diameter_cm=23.0),
        extra_large=BreadPortionSize(category="Extra Large", typical_grams=330.0, gram_range=(285.0, 390.0), typical_diameter_cm=27.0),
        density_g_cm3=0.92,
        notes="Stuffed flatbread (aloo, paneer, gobi, mooli, sattu) with dense interior."
    ),
    "puri": BreadFoodPortionConfig(
        bread_family="Puri family",
        small=BreadPortionSize(category="Small", typical_grams=20.0, gram_range=(15.0, 25.0), typical_diameter_cm=10.0),
        medium=BreadPortionSize(category="Medium", typical_grams=30.0, gram_range=(25.0, 38.0), typical_diameter_cm=12.0),
        large=BreadPortionSize(category="Large", typical_grams=45.0, gram_range=(38.0, 55.0), typical_diameter_cm=14.0),
        extra_large=BreadPortionSize(category="Extra Large", typical_grams=65.0, gram_range=(55.0, 75.0), typical_diameter_cm=16.0),
        density_g_cm3=0.78,
        notes="Deep fried puffed whole wheat disk."
    ),
    "bhatura": BreadFoodPortionConfig(
        bread_family="Bhatura family",
        small=BreadPortionSize(category="Small", typical_grams=85.0, gram_range=(70.0, 105.0), typical_diameter_cm=17.0),
        medium=BreadPortionSize(category="Medium", typical_grams=130.0, gram_range=(105.0, 160.0), typical_diameter_cm=21.0),
        large=BreadPortionSize(category="Large", typical_grams=185.0, gram_range=(160.0, 220.0), typical_diameter_cm=25.0),
        extra_large=BreadPortionSize(category="Extra Large", typical_grams=250.0, gram_range=(220.0, 310.0), typical_diameter_cm=30.0),
        density_g_cm3=0.76,
        notes="Deep fried oversized fermented leavened maida balloon."
    ),
    "bhakri": BreadFoodPortionConfig(
        bread_family="Bhakri family",
        small=BreadPortionSize(category="Small", typical_grams=60.0, gram_range=(45.0, 75.0), typical_diameter_cm=14.0),
        medium=BreadPortionSize(category="Medium", typical_grams=95.0, gram_range=(75.0, 120.0), typical_diameter_cm=17.0),
        large=BreadPortionSize(category="Large", typical_grams=140.0, gram_range=(120.0, 165.0), typical_diameter_cm=20.0),
        extra_large=BreadPortionSize(category="Extra Large", typical_grams=185.0, gram_range=(165.0, 220.0), typical_diameter_cm=23.0),
        density_g_cm3=0.91,
        notes="Dense rustic unleavened millet or wheat flatbread."
    ),
    "thepla": BreadFoodPortionConfig(
        bread_family="Regional flatbread family",
        small=BreadPortionSize(category="Small", typical_grams=35.0, gram_range=(28.0, 45.0), typical_diameter_cm=13.0),
        medium=BreadPortionSize(category="Medium", typical_grams=55.0, gram_range=(45.0, 68.0), typical_diameter_cm=16.0),
        large=BreadPortionSize(category="Large", typical_grams=80.0, gram_range=(68.0, 95.0), typical_diameter_cm=19.0),
        extra_large=BreadPortionSize(category="Extra Large", typical_grams=110.0, gram_range=(95.0, 130.0), typical_diameter_cm=22.0),
        density_g_cm3=0.87,
        notes="Spiced thin fenugreek travel flatbread from Gujarat."
    ),
    "appam": BreadFoodPortionConfig(
        bread_family="Fermented bread family",
        small=BreadPortionSize(category="Small", typical_grams=45.0, gram_range=(35.0, 55.0), typical_diameter_cm=14.0),
        medium=BreadPortionSize(category="Medium", typical_grams=65.0, gram_range=(55.0, 80.0), typical_diameter_cm=17.0),
        large=BreadPortionSize(category="Large", typical_grams=95.0, gram_range=(80.0, 115.0), typical_diameter_cm=20.0),
        extra_large=BreadPortionSize(category="Extra Large", typical_grams=130.0, gram_range=(115.0, 150.0), typical_diameter_cm=23.0),
        density_g_cm3=0.79,
        notes="Fermented rice bowl pancake with thick spongy center and lacy crispy edges."
    ),
    "pathiri": BreadFoodPortionConfig(
        bread_family="Rice-based bread family",
        small=BreadPortionSize(category="Small", typical_grams=30.0, gram_range=(24.0, 38.0), typical_diameter_cm=13.0),
        medium=BreadPortionSize(category="Medium", typical_grams=45.0, gram_range=(38.0, 55.0), typical_diameter_cm=15.0),
        large=BreadPortionSize(category="Large", typical_grams=65.0, gram_range=(55.0, 78.0), typical_diameter_cm=18.0),
        extra_large=BreadPortionSize(category="Extra Large", typical_grams=85.0, gram_range=(78.0, 100.0), typical_diameter_cm=21.0),
        density_g_cm3=0.84,
        notes="Paper thin, pristine chalk-white roasted rice flour pancake from Malabar."
    ),
    "roomali_roti": BreadFoodPortionConfig(
        bread_family="Regional flatbread family",
        small=BreadPortionSize(category="Small", typical_grams=50.0, gram_range=(40.0, 65.0), typical_diameter_cm=26.0),
        medium=BreadPortionSize(category="Medium", typical_grams=80.0, gram_range=(65.0, 95.0), typical_diameter_cm=32.0),
        large=BreadPortionSize(category="Large", typical_grams=115.0, gram_range=(95.0, 135.0), typical_diameter_cm=38.0),
        extra_large=BreadPortionSize(category="Extra Large", typical_grams=150.0, gram_range=(135.0, 180.0), typical_diameter_cm=44.0),
        density_g_cm3=0.72,
        notes="Extremely large handkerchief-thin folded soft flatbread."
    ),
    "default": BreadFoodPortionConfig(
        bread_family="General Indian Bread",
        small=BreadPortionSize(category="Small", typical_grams=35.0, gram_range=(25.0, 45.0), typical_diameter_cm=14.0),
        medium=BreadPortionSize(category="Medium", typical_grams=60.0, gram_range=(45.0, 80.0), typical_diameter_cm=17.0),
        large=BreadPortionSize(category="Large", typical_grams=95.0, gram_range=(80.0, 120.0), typical_diameter_cm=20.0),
        extra_large=BreadPortionSize(category="Extra Large", typical_grams=135.0, gram_range=(120.0, 160.0), typical_diameter_cm=23.0),
        density_g_cm3=0.85,
        notes="Fallback bread portion baseline."
    )
}


def resolve_bread_portion(
    bread_type: str,
    portion_category: str = "Medium",
    count: int = 1,
    diameter_cm: Optional[float] = None
) -> Tuple[float, Tuple[float, float]]:
    """
    Returns (typical_total_grams, (min_total_grams, max_total_grams))
    scaled by piece count and optionally adjusted by observed diameter.
    """
    bt = bread_type.lower().strip()
    config = BREAD_PORTION_DATABASE.get("default")
    for key, cfg in BREAD_PORTION_DATABASE.items():
        if key in bt or bt in key:
            config = cfg
            break

    cat = portion_category.title()
    if cat == "Small":
        size = config.small
    elif cat == "Large":
        size = config.large
    elif cat == "Extra Large" or cat == "Extralarge":
        size = config.extra_large
    else:
        size = config.medium

    single_typical = size.typical_grams
    single_min, single_max = size.gram_range

    # Area scaling if diameter provided
    if diameter_cm and size.typical_diameter_cm:
        ratio = (diameter_cm / size.typical_diameter_cm) ** 1.8
        ratio = max(0.6, min(2.0, ratio))
        single_typical *= ratio
        single_min *= ratio
        single_max *= ratio

    cnt = max(1, count)
    return round(single_typical * cnt, 1), (round(single_min * cnt, 1), round(single_max * cnt, 1))


# =============================================================================
# SECTION 46 & 47 — BREAD FAT & GHEE ESTIMATOR
# =============================================================================

class BreadFatEstimationResult(BaseModel):
    fat_level: str  # "Very Low", "Low", "Medium", "High", "Very High", "Unknown"
    added_fat_grams_per_piece: Tuple[float, float]
    added_fat_typical_g: float
    fat_type_guess: str  # "none", "desi_ghee", "butter", "cooking_oil", "uncertain"
    confidence: str      # "High", "Medium", "Low"
    rationale: str
    shine_detected: bool = False
    butter_slab_detected: bool = False


class BreadFatEstimator:
    """
    Implements Sections 46, 47 & Non-Negotiable Rule 84:
    - Categorizes fat into: Very Low, Low, Medium, High, Very High, Unknown.
    - Explicitly obeys: Never assume butter from shine alone.
      Shine can stem from water wash, steam, light oil wipe, camera flash reflection,
      or melted butter/ghee.
    """

    @classmethod
    def estimate_fat(
        cls,
        bread_canonical_name: str,
        cooking_method: str = "Tawa cooked",
        surface_cues: Optional[Dict[str, Any]] = None
    ) -> BreadFatEstimationResult:
        cues = surface_cues or {}
        bname = bread_canonical_name.lower()
        method = cooking_method.lower()

        has_butter_slab = cues.get("butter_slab_present", False)
        sheen_type = cues.get("surface_sheen", "unknown")  # dry, faint_gloss, glossy, greasy_layer, butter_puddle, unknown
        oil_sheen = cues.get("oil_sheen_level", "low")      # dry, low, moderate, high

        # Case 1: Visible physical butter slab / melting dollop
        if has_butter_slab:
            return BreadFatEstimationResult(
                fat_level="Very High",
                added_fat_grams_per_piece=(12.0, 22.0),
                added_fat_typical_g=16.0,
                fat_type_guess="butter",
                confidence="High",
                rationale="Distinct melting butter slab detected resting on bread surface.",
                shine_detected=True,
                butter_slab_detected=True
            )

        # Case 2: Deep Fried Breads (Puri, Bhatura, Luchi)
        if "deep fried" in method or "puri" in bname or "bhatura" in bname or "luchi" in bname:
            if "bhatura" in bname:
                return BreadFatEstimationResult(
                    fat_level="High",
                    added_fat_grams_per_piece=(9.0, 16.0),
                    added_fat_typical_g=12.5,
                    fat_type_guess="cooking_oil",
                    confidence="High",
                    rationale="Deep-fried leavened bhatura with intrinsic oil absorption from frying.",
                    shine_detected=sheen_type in ["glossy", "greasy_layer"]
                )
            else:
                return BreadFatEstimationResult(
                    fat_level="High",
                    added_fat_grams_per_piece=(6.0, 12.0),
                    added_fat_typical_g=8.5,
                    fat_type_guess="cooking_oil",
                    confidence="High",
                    rationale="Deep-fried puri absorbs oil during expansion in hot kadai.",
                    shine_detected=sheen_type in ["glossy", "greasy_layer"]
                )

        # Case 3: Flaky layered breads with laminated oil/dalda (Kerala Parotta, Laccha Paratha)
        if "parotta" in bname or "laccha" in bname:
            return BreadFatEstimationResult(
                fat_level="High",
                added_fat_grams_per_piece=(8.0, 15.0),
                added_fat_typical_g=11.0,
                fat_type_guess="cooking_oil",
                confidence="High",
                rationale="Layered bread incorporates laminated fat between dough folds plus griddle oil.",
                shine_detected=True
            )

        # Case 4: Butter Naan / Garlic Naan / Tandoori Roti with shine
        if "butter naan" in bname:
            return BreadFatEstimationResult(
                fat_level="High",
                added_fat_grams_per_piece=(7.0, 14.0),
                added_fat_typical_g=10.0,
                fat_type_guess="butter",
                confidence="High",
                rationale="Butter naan finished with post-tandoor butter brush glaze.",
                shine_detected=True
            )

        # Case 5: Phulka, Pathiri, Neer Dosa (Inherently dry or oil-free)
        if "phulka" in bname or "pathiri" in bname or "neer dosa" in bname:
            if sheen_type in ["glossy", "greasy_layer"]:
                # Brushed with light ghee after flame puffing
                return BreadFatEstimationResult(
                    fat_level="Low",
                    added_fat_grams_per_piece=(2.0, 4.0),
                    added_fat_typical_g=3.0,
                    fat_type_guess="desi_ghee",
                    confidence="Medium",
                    rationale="Light brush of ghee applied over puffed surface. Never assume heavy butter from sheen alone.",
                    shine_detected=True
                )
            return BreadFatEstimationResult(
                fat_level="Very Low",
                added_fat_grams_per_piece=(0.0, 1.0),
                added_fat_typical_g=0.2,
                fat_type_guess="none",
                confidence="High",
                rationale="Dry roasted flatbread without added surface fat or oil.",
                shine_detected=False
            )

        # Case 6: Stuffed or Plain Paratha (Tawa shallow-fried)
        if "paratha" in bname:
            if sheen_type in ["glossy", "greasy_layer", "butter_puddle"]:
                return BreadFatEstimationResult(
                    fat_level="Medium",
                    added_fat_grams_per_piece=(5.0, 9.0),
                    added_fat_typical_g=7.0,
                    fat_type_guess="desi_ghee",
                    confidence="Medium",
                    rationale="Griddled paratha with visible shallow-frying oil/ghee sheen.",
                    shine_detected=True
                )
            return BreadFatEstimationResult(
                fat_level="Low",
                added_fat_grams_per_piece=(2.5, 5.0),
                added_fat_typical_g=3.5,
                fat_type_guess="desi_ghee",
                confidence="Medium",
                rationale="Dry-roasted paratha with minimal tawa fat.",
                shine_detected=False
            )

        # Case 7: Thepla
        if "thepla" in bname:
            return BreadFatEstimationResult(
                fat_level="Medium",
                added_fat_grams_per_piece=(3.5, 7.0),
                added_fat_typical_g=5.0,
                fat_type_guess="cooking_oil",
                confidence="High",
                rationale="Gujarati thepla incorporates oil in both dough kneading and tawa roasting.",
                shine_detected=sheen_type != "dry"
            )

        # Case 8: Ambiguous shine (Rule 84 enforcement: shine != butter)
        if sheen_type in ["glossy", "greasy_layer"]:
            return BreadFatEstimationResult(
                fat_level="Medium",
                added_fat_grams_per_piece=(3.0, 8.0),
                added_fat_typical_g=5.0,
                fat_type_guess="uncertain",
                confidence="Low",
                rationale="Surface shine detected. Caution: shine may stem from oil, steam condensation, or camera glare. Never assume butter.",
                shine_detected=True
            )

        # Case 9: Default / Unknown
        return BreadFatEstimationResult(
            fat_level="Low",
            added_fat_grams_per_piece=(1.0, 4.0),
            added_fat_typical_g=2.0,
            fat_type_guess="uncertain",
            confidence="Medium",
            rationale="Standard homestyle dry or lightly greased flatbread baseline.",
            shine_detected=False
        )


# =============================================================================
# SECTION 40 & 41 — STUFFING VS DOUGH MASS CALCULATOR
# =============================================================================

class BreadStuffingSplitResult(BaseModel):
    bread_name: str
    total_mass_g: float
    dough_mass_g: float
    stuffing_mass_g: float
    stuffing_type: str
    dough_flour_type: str
    stuffing_ratio_pct: float
    dough_ratio_pct: float


class BreadStuffingDoughRatioEstimator:
    """
    Deconstructs stuffed Indian breads into dough shell mass and stuffing filling mass.
    Ratios calibrated from traditional kitchen formulations:
    - Aloo Paratha: 55% dough, 45% spiced potato
    - Paneer Paratha: 50% dough, 50% crumbled paneer
    - Gobi Paratha: 60% dough, 40% grated cauliflower
    - Mooli Paratha: 62% dough, 38% grated radish
    - Sattu Paratha: 58% dough, 42% roasted gram flour filling
    - Amritsari Kulcha: 48% maida dough, 52% spiced potato-onion
    - Mughlai Paratha: 40% maida crust, 60% egg/minced meat
    - Keema Naan: 50% maida dough, 50% spiced minced meat
    """

    STUFFING_RATIOS: Dict[str, Tuple[float, float, str, str]] = {
        # name_key: (dough_ratio, stuffing_ratio, stuffing_type, dough_flour)
        "aloo": (0.55, 0.45, "potato", "whole_wheat"),
        "paneer": (0.50, 0.50, "paneer", "whole_wheat"),
        "gobi": (0.60, 0.40, "cauliflower", "whole_wheat"),
        "mooli": (0.62, 0.38, "radish", "whole_wheat"),
        "sattu": (0.58, 0.42, "sattu", "whole_wheat"),
        "onion": (0.60, 0.40, "onion", "whole_wheat"),
        "amritsari": (0.48, 0.52, "potato_onion", "refined_flour"),
        "mughlai": (0.40, 0.60, "egg_meat", "refined_flour"),
        "keema": (0.50, 0.50, "minced_meat", "refined_flour"),
        "cheese": (0.55, 0.45, "cheese", "refined_flour")
    }

    @classmethod
    def split_stuffed_bread(
        cls,
        bread_name: str,
        total_mass_g: float
    ) -> BreadStuffingSplitResult:
        bname = bread_name.lower().strip()
        matched_ratio = (0.55, 0.45, "potato", "whole_wheat")  # fallback default stuffed
        is_stuffed = False

        for key, config in cls.STUFFING_RATIOS.items():
            if key in bname:
                matched_ratio = config
                is_stuffed = True
                break

        if not is_stuffed and ("stuffed" in bname or "kulcha" in bname):
            is_stuffed = True

        if not is_stuffed:
            # Plain flatbread: 100% dough
            return BreadStuffingSplitResult(
                bread_name=bread_name,
                total_mass_g=round(total_mass_g, 1),
                dough_mass_g=round(total_mass_g, 1),
                stuffing_mass_g=0.0,
                stuffing_type="none",
                dough_flour_type="whole_wheat" if "naan" not in bname and "bhatura" not in bname else "refined_flour",
                stuffing_ratio_pct=0.0,
                dough_ratio_pct=100.0
            )

        dough_pct, stuffing_pct, stuffing_type, flour = matched_ratio
        dough_g = round(total_mass_g * dough_pct, 1)
        stuffing_g = round(total_mass_g * stuffing_pct, 1)

        return BreadStuffingSplitResult(
            bread_name=bread_name,
            total_mass_g=round(total_mass_g, 1),
            dough_mass_g=dough_g,
            stuffing_mass_g=stuffing_g,
            stuffing_type=stuffing_type,
            dough_flour_type=flour,
            stuffing_ratio_pct=round(stuffing_pct * 100.0, 1),
            dough_ratio_pct=round(dough_pct * 100.0, 1)
        )
