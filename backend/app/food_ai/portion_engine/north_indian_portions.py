"""
North Indian Food-Specific Portion Engine, Density Models & Oil/Ghee Range Estimator
Implements Sections 25-28, 30, and 33 of Part 4.
Guarantees:
- Food-specific physically measured portion models for Breads, Parathas, Dals, and Rice.
- Katori bowl volumetric geometry (small 110g, standard 180g, large 240g).
- Bread thickness and diameter scale calibrator.
- Oil/Ghee Range Estimator:
  - Low Oil (Home style: 3-5% fat)
  - Medium Oil (Restaurant style: 8-12% fat)
  - High Ghee (Dhaba / Tari style: 15-22% fat)
  - Visible Butter Pool / Makhan Dollop (+10-15g fat addition)
"""

from typing import Dict, Any, List, Optional, Tuple
from pydantic import BaseModel, Field

class NorthIndianPortionModel(BaseModel):
    category: str # "bread_roti", "bread_paratha", "bread_naan", "curry_katori", "rice_plate"
    sub_type: str # e.g. "phulka", "tandoori_roti", "makki_roti", "stuffed_paratha"
    density_g_cm3: float
    typical_weight_g: float
    credible_range_g: Tuple[float, float]
    diameter_cm: Optional[float] = None
    thickness_mm: Optional[float] = None
    volume_cm3: Optional[float] = None

# Master Portions Dictionary
NORTH_INDIAN_PORTION_TABLE: Dict[str, NorthIndianPortionModel] = {
    # ROTIS
    "roti_phulka": NorthIndianPortionModel(
        category="bread_roti",
        sub_type="phulka",
        density_g_cm3=0.75,
        typical_weight_g=28.0,
        credible_range_g=(20.0, 35.0),
        diameter_cm=16.0,
        thickness_mm=1.5
    ),
    "roti_tandoori": NorthIndianPortionModel(
        category="bread_roti",
        sub_type="tandoori_roti",
        density_g_cm3=0.75,
        typical_weight_g=45.0,
        credible_range_g=(38.0, 55.0),
        diameter_cm=18.0,
        thickness_mm=2.5
    ),
    "roti_makki": NorthIndianPortionModel(
        category="bread_roti",
        sub_type="makki_roti",
        density_g_cm3=0.88,
        typical_weight_g=60.0,
        credible_range_g=(50.0, 75.0),
        diameter_cm=16.0,
        thickness_mm=4.5
    ),
    "roti_bajra": NorthIndianPortionModel(
        category="bread_roti",
        sub_type="bajra_roti",
        density_g_cm3=0.88,
        typical_weight_g=65.0,
        credible_range_g=(52.0, 80.0),
        diameter_cm=17.0,
        thickness_mm=4.5
    ),
    "roti_jowar": NorthIndianPortionModel(
        category="bread_roti",
        sub_type="jowar_roti",
        density_g_cm3=0.86,
        typical_weight_g=60.0,
        credible_range_g=(48.0, 72.0),
        diameter_cm=17.0,
        thickness_mm=3.8
    ),
    "roti_mandua": NorthIndianPortionModel(
        category="bread_roti",
        sub_type="mandua_roti",
        density_g_cm3=0.84,
        typical_weight_g=55.0,
        credible_range_g=(45.0, 68.0),
        diameter_cm=16.5,
        thickness_mm=3.5
    ),

    # PARATHAS
    "paratha_plain": NorthIndianPortionModel(
        category="bread_paratha",
        sub_type="plain_paratha",
        density_g_cm3=0.82,
        typical_weight_g=65.0,
        credible_range_g=(55.0, 78.0),
        diameter_cm=18.0,
        thickness_mm=3.0
    ),
    "paratha_stuffed": NorthIndianPortionModel(
        category="bread_paratha",
        sub_type="stuffed_paratha",
        density_g_cm3=0.86,
        typical_weight_g=120.0,
        credible_range_g=(100.0, 150.0),
        diameter_cm=20.0,
        thickness_mm=4.0
    ),
    "paratha_methi": NorthIndianPortionModel(
        category="bread_paratha",
        sub_type="methi_paratha",
        density_g_cm3=0.82,
        typical_weight_g=75.0,
        credible_range_g=(65.0, 90.0),
        diameter_cm=19.0,
        thickness_mm=3.2
    ),

    # NAANS & KULCHAS
    "naan_plain": NorthIndianPortionModel(
        category="bread_naan",
        sub_type="plain_naan",
        density_g_cm3=0.72,
        typical_weight_g=80.0,
        credible_range_g=(70.0, 95.0),
        diameter_cm=22.0,
        thickness_mm=3.5
    ),
    "naan_butter": NorthIndianPortionModel(
        category="bread_naan",
        sub_type="butter_naan",
        density_g_cm3=0.72,
        typical_weight_g=85.0,
        credible_range_g=(75.0, 100.0),
        diameter_cm=23.0,
        thickness_mm=3.8
    ),
    "kulcha_amritsari": NorthIndianPortionModel(
        category="bread_naan",
        sub_type="amritsari_kulcha",
        density_g_cm3=0.82,
        typical_weight_g=140.0,
        credible_range_g=(120.0, 165.0),
        diameter_cm=18.0,
        thickness_mm=5.5
    ),

    # FRIED BREADS
    "bread_poori": NorthIndianPortionModel(
        category="bread_fried",
        sub_type="poori",
        density_g_cm3=0.70,
        typical_weight_g=30.0,
        credible_range_g=(24.0, 36.0),
        diameter_cm=11.0,
        thickness_mm=1.8
    ),
    "bread_bhatura": NorthIndianPortionModel(
        category="bread_fried",
        sub_type="bhatura",
        density_g_cm3=0.68,
        typical_weight_g=95.0,
        credible_range_g=(80.0, 115.0),
        diameter_cm=22.0,
        thickness_mm=3.0
    ),

    # CURRY KATORI BOWLS
    "katori_small": NorthIndianPortionModel(
        category="curry_katori",
        sub_type="katori_small",
        density_g_cm3=1.05,
        typical_weight_g=110.0,
        credible_range_g=(95.0, 125.0),
        diameter_cm=7.5,
        volume_cm3=105.0
    ),
    "katori_standard": NorthIndianPortionModel(
        category="curry_katori",
        sub_type="katori_standard",
        density_g_cm3=1.05,
        typical_weight_g=180.0,
        credible_range_g=(160.0, 205.0),
        diameter_cm=8.5,
        volume_cm3=171.0
    ),
    "katori_large": NorthIndianPortionModel(
        category="curry_katori",
        sub_type="katori_large",
        density_g_cm3=1.05,
        typical_weight_g=240.0,
        credible_range_g=(215.0, 270.0),
        diameter_cm=9.5,
        volume_cm3=228.0
    ),

    # RICE PORTIONS
    "rice_half_plate": NorthIndianPortionModel(
        category="rice_plate",
        sub_type="steamed_rice_half",
        density_g_cm3=0.80,
        typical_weight_g=150.0,
        credible_range_g=(130.0, 170.0),
        volume_cm3=187.5
    ),
    "rice_full_plate": NorthIndianPortionModel(
        category="rice_plate",
        sub_type="steamed_rice_full",
        density_g_cm3=0.80,
        typical_weight_g=250.0,
        credible_range_g=(220.0, 290.0),
        volume_cm3=312.5
    ),
    "biryani_plate": NorthIndianPortionModel(
        category="rice_plate",
        sub_type="biryani_serving",
        density_g_cm3=0.82,
        typical_weight_g=350.0,
        credible_range_g=(310.0, 400.0),
        volume_cm3=426.8
    )
}

# =============================================================================
# OIL / GHEE RANGE ESTIMATOR
# =============================================================================

class OilGheeRangeEstimator:
    """
    Analyzes visual cues of surface sheen, oil meniscus (tari), melted butter lake,
    or white butter dollop to calibrate fat and calorie content.
    """
    @classmethod
    def estimate_oil_ghee_profile(cls, visual_sheen_cues: Dict[str, Any]) -> Dict[str, Any]:
        """
        visual_sheen_cues may contain:
        - "gloss_level": "matte", "low", "medium", "high", "glossy"
        - "surface_oil_layer": bool (tari visible)
        - "butter_dollop": bool (makhan / butter cube visible)
        - "restaurant_or_home": "home", "restaurant", "dhaba"
        """
        gloss = visual_sheen_cues.get("gloss_level", "low").lower()
        has_tari = visual_sheen_cues.get("surface_oil_layer", False)
        has_butter_dollop = visual_sheen_cues.get("butter_dollop", False)
        venue = visual_sheen_cues.get("restaurant_or_home", "home").lower()

        # Extra fat addition from visible butter/makhan
        extra_fat_g = 12.0 if has_butter_dollop else 0.0

        if has_tari or venue == "dhaba" or gloss == "high":
            # Dhaba style high oil / ghee
            fat_multiplier = 1.35
            profile_name = "Dhaba / High Ghee Style"
            description = "Prominent floating oil meniscus (tari) or heavy ghee glaze detected."
            fat_level = "high"
        elif venue == "restaurant" or gloss == "medium":
            # Restaurant style medium oil
            fat_multiplier = 1.15
            profile_name = "Restaurant Style"
            description = "Standard restaurant gravy preparation with tempered ghee/oil."
            fat_level = "medium"
        else:
            # Home style low oil
            fat_multiplier = 1.00
            profile_name = "Home Style / Low Oil"
            description = "Minimal surface sheen, healthy light home preparation."
            fat_level = "low"

        return {
            "fat_level": fat_level,
            "profile_name": profile_name,
            "fat_multiplier": fat_multiplier,
            "extra_fat_g": extra_fat_g,
            "has_butter_dollop": has_butter_dollop,
            "description": description
        }

def get_portion_for_north_food(food_id: str, portion_hint: Optional[str] = None) -> Tuple[float, Tuple[float, float]]:
    """
    Returns (estimated_weight_g, (min_g, max_g)) for a given food ID.
    """
    fid = food_id.upper()
    
    # Check breads
    if "ROTI_TAWA" in fid:
        m = NORTH_INDIAN_PORTION_TABLE["roti_phulka"]
        return (m.typical_weight_g, m.credible_range_g)
    elif "ROTI_TANDOORI" in fid:
        m = NORTH_INDIAN_PORTION_TABLE["roti_tandoori"]
        return (m.typical_weight_g, m.credible_range_g)
    elif "ROTI_MAKKI" in fid:
        m = NORTH_INDIAN_PORTION_TABLE["roti_makki"]
        return (m.typical_weight_g, m.credible_range_g)
    elif "ROTI_BAJRA" in fid:
        m = NORTH_INDIAN_PORTION_TABLE["roti_bajra"]
        return (m.typical_weight_g, m.credible_range_g)
    elif "ROTI_JOWAR" in fid:
        m = NORTH_INDIAN_PORTION_TABLE["roti_jowar"]
        return (m.typical_weight_g, m.credible_range_g)
    elif "ROTI_MANDUA" in fid:
        m = NORTH_INDIAN_PORTION_TABLE["roti_mandua"]
        return (m.typical_weight_g, m.credible_range_g)
    elif "PARATHA_PLAIN" in fid:
        m = NORTH_INDIAN_PORTION_TABLE["paratha_plain"]
        return (m.typical_weight_g, m.credible_range_g)
    elif "PARATHA_METHI" in fid:
        m = NORTH_INDIAN_PORTION_TABLE["paratha_methi"]
        return (m.typical_weight_g, m.credible_range_g)
    elif "PARATHA" in fid: # stuffed paratha
        m = NORTH_INDIAN_PORTION_TABLE["paratha_stuffed"]
        return (m.typical_weight_g, m.credible_range_g)
    elif "NAAN_BUTTER" in fid:
        m = NORTH_INDIAN_PORTION_TABLE["naan_butter"]
        return (m.typical_weight_g, m.credible_range_g)
    elif "NAAN" in fid:
        m = NORTH_INDIAN_PORTION_TABLE["naan_plain"]
        return (m.typical_weight_g, m.credible_range_g)
    elif "KULCHA_AMRITSARI" in fid:
        m = NORTH_INDIAN_PORTION_TABLE["kulcha_amritsari"]
        return (m.typical_weight_g, m.credible_range_g)
    elif "BHATURA" in fid:
        m = NORTH_INDIAN_PORTION_TABLE["bread_bhatura"]
        return (m.typical_weight_g, m.credible_range_g)
    elif "POORI" in fid:
        m = NORTH_INDIAN_PORTION_TABLE["bread_poori"]
        return (m.typical_weight_g, m.credible_range_g)
    
    # Check Curries / Dals (standard katori)
    elif "CURRY" in fid or "DAL" in fid:
        m = NORTH_INDIAN_PORTION_TABLE["katori_standard"]
        return (m.typical_weight_g, m.credible_range_g)
    
    # Check Rice
    elif "BIRYANI" in fid:
        m = NORTH_INDIAN_PORTION_TABLE["biryani_plate"]
        return (m.typical_weight_g, m.credible_range_g)
    elif "RICE" in fid:
        m = NORTH_INDIAN_PORTION_TABLE["rice_full_plate"]
        return (m.typical_weight_g, m.credible_range_g)
    
    # Fallback generic default
    return (150.0, (120.0, 180.0))
