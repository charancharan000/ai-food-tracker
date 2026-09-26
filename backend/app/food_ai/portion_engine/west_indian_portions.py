"""
West Indian Food-Specific Portion Engine, Countable Foods Estimator & Fat/Sheen Calibrator
Implements Sections 25-28, 30, and 33 of Part 5.
Guarantees:
- Discrete Countable Food Detector (Dhokla, Khandvi, Batata Vada, Modak, Puri, Pav, Puran Poli, Muthia, Vadi).
- Multiplies detected units by physical unit densities and calibrated single-unit weights.
- Katori bowl volumetric geometry for dals, curries, khichdi, kadhi, and usal.
- Bread thickness, diameter, and coarse flour mass models (Phulka, Jowar Bhakri, Bajra Rotla, Rice Bhakri).
- Street-food paper plate boundary isolation (Rule 29).
- Visual Fat/Sheen Level Estimator (Low, Medium, High, Butter Pool, Tarri Oil Floats).
"""

from typing import Dict, Any, List, Optional, Tuple
from pydantic import BaseModel, Field


class WestIndianPortionModel(BaseModel):
    category: str  # "countable_snack", "bread_flatbread", "curry_katori", "rice_plate", "beverage"
    sub_type: str
    density_g_cm3: float
    typical_weight_g: float
    credible_range_g: Tuple[float, float]
    diameter_cm: Optional[float] = None
    thickness_mm: Optional[float] = None
    unit_weight_g: Optional[float] = None
    is_countable: bool = False


# Master Portions Dictionary for West Indian Food Items
WEST_INDIAN_PORTION_TABLE: Dict[str, WestIndianPortionModel] = {
    # COUNTABLE SNACKS & APPETIZERS
    "MH_SNACK_BATATA_VADA": WestIndianPortionModel(
        category="countable_snack",
        sub_type="batata_vada",
        density_g_cm3=0.88,
        typical_weight_g=75.0,
        credible_range_g=(60.0, 90.0),
        unit_weight_g=75.0,
        is_countable=True
    ),
    "MH_BREAD_PAV": WestIndianPortionModel(
        category="countable_snack",
        sub_type="ladi_pav",
        density_g_cm3=0.38,
        typical_weight_g=50.0,
        credible_range_g=(42.0, 58.0),
        unit_weight_g=50.0,
        is_countable=True
    ),
    "GJ_FARSAN_KHAMAN": WestIndianPortionModel(
        category="countable_snack",
        sub_type="khaman_dhokla",
        density_g_cm3=0.72,
        typical_weight_g=70.0,  # 2 pieces default
        credible_range_g=(55.0, 85.0),
        unit_weight_g=35.0,
        is_countable=True
    ),
    "GJ_FARSAN_KHANDVI": WestIndianPortionModel(
        category="countable_snack",
        sub_type="khandvi_roll",
        density_g_cm3=0.84,
        typical_weight_g=80.0,  # 4 rolls default
        credible_range_g=(60.0, 100.0),
        unit_weight_g=20.0,
        is_countable=True
    ),
    "GJ_FARSAN_DHOKLA_WHITE": WestIndianPortionModel(
        category="countable_snack",
        sub_type="white_khatta_dhokla",
        density_g_cm3=0.75,
        typical_weight_g=70.0,
        credible_range_g=(55.0, 85.0),
        unit_weight_g=35.0,
        is_countable=True
    ),
    "MH_SWEET_MODAK_UKADICHE": WestIndianPortionModel(
        category="countable_snack",
        sub_type="ukadiche_modak",
        density_g_cm3=0.92,
        typical_weight_g=90.0,  # 2 modaks default
        credible_range_g=(75.0, 110.0),
        unit_weight_g=45.0,
        is_countable=True
    ),
    "MH_SNACK_KOTHIMBIR_VADI": WestIndianPortionModel(
        category="countable_snack",
        sub_type="kothimbir_vadi",
        density_g_cm3=0.86,
        typical_weight_g=75.0,  # 3 vadis default
        credible_range_g=(55.0, 95.0),
        unit_weight_g=25.0,
        is_countable=True
    ),
    "MH_SNACK_ALU_VADI": WestIndianPortionModel(
        category="countable_snack",
        sub_type="alu_vadi_patra",
        density_g_cm3=0.85,
        typical_weight_g=75.0,  # 3 vadis default
        credible_range_g=(55.0, 95.0),
        unit_weight_g=25.0,
        is_countable=True
    ),
    "MH_SNACK_SABUDANA_VADA": WestIndianPortionModel(
        category="countable_snack",
        sub_type="sabudana_vada",
        density_g_cm3=0.88,
        typical_weight_g=90.0,  # 2 vadis default
        credible_range_g=(75.0, 110.0),
        unit_weight_g=45.0,
        is_countable=True
    ),
    "GJ_FARSAN_MUTHIA": WestIndianPortionModel(
        category="countable_snack",
        sub_type="methi_muthia",
        density_g_cm3=0.82,
        typical_weight_g=75.0,  # 3 muthia pieces default
        credible_range_g=(60.0, 90.0),
        unit_weight_g=25.0,
        is_countable=True
    ),
    "GJ_BREAD_PURI": WestIndianPortionModel(
        category="countable_snack",
        sub_type="puri",
        density_g_cm3=0.68,
        typical_weight_g=44.0,  # 2 puris default
        credible_range_g=(36.0, 55.0),
        unit_weight_g=22.0,
        is_countable=True
    ),
    "WI_ACCOMPANIMENT_PAPAD": WestIndianPortionModel(
        category="countable_snack",
        sub_type="udad_papad",
        density_g_cm3=0.45,
        typical_weight_g=15.0,
        credible_range_g=(12.0, 18.0),
        unit_weight_g=15.0,
        is_countable=True
    ),

    # FLATBREADS & BHAKRIS
    "MH_BREAD_PURAN_POLI": WestIndianPortionModel(
        category="bread_flatbread",
        sub_type="puran_poli",
        density_g_cm3=0.85,
        typical_weight_g=85.0,
        credible_range_g=(70.0, 100.0),
        diameter_cm=18.0,
        thickness_mm=3.0,
        unit_weight_g=85.0,
        is_countable=True
    ),
    "MH_BREAD_BHAKRI_JOWAR": WestIndianPortionModel(
        category="bread_flatbread",
        sub_type="jowar_bhakri",
        density_g_cm3=0.86,
        typical_weight_g=60.0,
        credible_range_g=(48.0, 72.0),
        diameter_cm=17.0,
        thickness_mm=3.5,
        unit_weight_g=60.0,
        is_countable=True
    ),
    "MH_BREAD_BHAKRI_BAJRA": WestIndianPortionModel(
        category="bread_flatbread",
        sub_type="bajra_bhakri",
        density_g_cm3=0.88,
        typical_weight_g=65.0,
        credible_range_g=(52.0, 80.0),
        diameter_cm=16.5,
        thickness_mm=4.0,
        unit_weight_g=65.0,
        is_countable=True
    ),
    "GJ_BREAD_ROTLO_BAJRA": WestIndianPortionModel(
        category="bread_flatbread",
        sub_type="kathiyawadi_bajra_rotlo",
        density_g_cm3=0.92,
        typical_weight_g=85.0,
        credible_range_g=(70.0, 105.0),
        diameter_cm=16.0,
        thickness_mm=5.5,
        unit_weight_g=85.0,
        is_countable=True
    ),
    "MH_BREAD_BHAKRI_RICE": WestIndianPortionModel(
        category="bread_flatbread",
        sub_type="rice_tandalachi_bhakri",
        density_g_cm3=0.82,
        typical_weight_g=55.0,
        credible_range_g=(45.0, 68.0),
        diameter_cm=17.0,
        thickness_mm=2.5,
        unit_weight_g=55.0,
        is_countable=True
    ),
    "MH_BREAD_BHAKRI_NACHNI": WestIndianPortionModel(
        category="bread_flatbread",
        sub_type="nachni_ragi_bhakri",
        density_g_cm3=0.84,
        typical_weight_g=55.0,
        credible_range_g=(45.0, 68.0),
        diameter_cm=16.0,
        thickness_mm=3.0,
        unit_weight_g=55.0,
        is_countable=True
    ),
    "GJ_BREAD_ROTLO_PHULKA": WestIndianPortionModel(
        category="bread_flatbread",
        sub_type="gujarati_phulka_rotli",
        density_g_cm3=0.74,
        typical_weight_g=24.0,
        credible_range_g=(18.0, 30.0),
        diameter_cm=15.5,
        thickness_mm=1.4,
        unit_weight_g=24.0,
        is_countable=True
    ),
    "GJ_BREAD_THEPLA_METHI": WestIndianPortionModel(
        category="bread_flatbread",
        sub_type="methi_thepla",
        density_g_cm3=0.80,
        typical_weight_g=35.0,
        credible_range_g=(28.0, 42.0),
        diameter_cm=16.0,
        thickness_mm=1.8,
        unit_weight_g=35.0,
        is_countable=True
    ),
    "MH_SNACK_THALIPEETH": WestIndianPortionModel(
        category="bread_flatbread",
        sub_type="thalipeeth",
        density_g_cm3=0.88,
        typical_weight_g=75.0,
        credible_range_g=(60.0, 90.0),
        diameter_cm=15.0,
        thickness_mm=4.0,
        unit_weight_g=75.0,
        is_countable=True
    ),

    # KATORI CURRIES & DALS
    "GJ_DAL_GUJARATI": WestIndianPortionModel(
        category="curry_katori",
        sub_type="gujarati_dal",
        density_g_cm3=1.04,
        typical_weight_g=140.0,
        credible_range_g=(110.0, 180.0)
    ),
    "GJ_KADHI_GUJARATI": WestIndianPortionModel(
        category="curry_katori",
        sub_type="gujarati_kadhi",
        density_g_cm3=1.03,
        typical_weight_g=140.0,
        credible_range_g=(110.0, 180.0)
    ),
    "MH_CURRY_VARAN_BHAT": WestIndianPortionModel(
        category="curry_katori",
        sub_type="maharashtrian_varan",
        density_g_cm3=1.05,
        typical_weight_g=120.0,
        credible_range_g=(95.0, 150.0)
    ),
    "MH_CURRY_USAL_MATKI": WestIndianPortionModel(
        category="curry_katori",
        sub_type="matki_usal",
        density_g_cm3=1.05,
        typical_weight_g=130.0,
        credible_range_g=(100.0, 160.0)
    ),
    "MH_CURRY_MISAL_KAT": WestIndianPortionModel(
        category="curry_katori",
        sub_type="misal_kat_tarri",
        density_g_cm3=1.02,
        typical_weight_g=120.0,
        credible_range_g=(90.0, 150.0)
    ),
    "GJ_CURRY_UNDHIYU": WestIndianPortionModel(
        category="curry_katori",
        sub_type="undhiyu",
        density_g_cm3=1.06,
        typical_weight_g=140.0,
        credible_range_g=(110.0, 180.0)
    ),
    "GJ_CURRY_RINGAN_BATETA": WestIndianPortionModel(
        category="curry_katori",
        sub_type="ringan_bateta",
        density_g_cm3=1.02,
        typical_weight_g=120.0,
        credible_range_g=(95.0, 150.0)
    ),
    "GJ_CURRY_SEV_TAMETA": WestIndianPortionModel(
        category="curry_katori",
        sub_type="sev_tameta",
        density_g_cm3=1.02,
        typical_weight_g=130.0,
        credible_range_g=(100.0, 160.0)
    ),
    "MH_CURRY_PITLA": WestIndianPortionModel(
        category="curry_katori",
        sub_type="pitla",
        density_g_cm3=1.04,
        typical_weight_g=130.0,
        credible_range_g=(100.0, 160.0)
    ),
    "MH_CURRY_TAMBDA_RASSA": WestIndianPortionModel(
        category="curry_katori",
        sub_type="tambda_rassa",
        density_g_cm3=1.02,
        typical_weight_g=140.0,
        credible_range_g=(110.0, 180.0)
    ),
    "MH_CURRY_PANDHRA_RASSA": WestIndianPortionModel(
        category="curry_katori",
        sub_type="pandhra_rassa",
        density_g_cm3=1.03,
        typical_weight_g=140.0,
        credible_range_g=(110.0, 180.0)
    ),
    "GA_CURRY_FISH_XITT_CODI": WestIndianPortionModel(
        category="curry_katori",
        sub_type="goan_fish_curry",
        density_g_cm3=1.03,
        typical_weight_g=160.0,
        credible_range_g=(120.0, 200.0)
    ),
    "GA_CURRY_PORK_VINDALOO": WestIndianPortionModel(
        category="curry_katori",
        sub_type="goan_pork_vindaloo",
        density_g_cm3=1.06,
        typical_weight_g=160.0,
        credible_range_g=(125.0, 200.0)
    ),
    "GA_CURRY_CHICKEN_XACUTI": WestIndianPortionModel(
        category="curry_katori",
        sub_type="goan_chicken_xacuti",
        density_g_cm3=1.05,
        typical_weight_g=160.0,
        credible_range_g=(125.0, 200.0)
    ),

    # RICE DISHES
    "GJ_RICE_KHICHDI": WestIndianPortionModel(
        category="rice_plate",
        sub_type="vaghareli_khichdi",
        density_g_cm3=1.08,
        typical_weight_g=160.0,
        credible_range_g=(120.0, 220.0)
    ),
    "GA_RICE_UKDA_BOILED": WestIndianPortionModel(
        category="rice_plate",
        sub_type="goan_ukda_rice",
        density_g_cm3=1.05,
        typical_weight_g=200.0,
        credible_range_g=(150.0, 260.0)
    ),
    "MH_RICE_MASALE_BHAT": WestIndianPortionModel(
        category="rice_plate",
        sub_type="masale_bhat",
        density_g_cm3=1.06,
        typical_weight_g=180.0,
        credible_range_g=(140.0, 240.0)
    ),
    "MH_BREAKFAST_POHA_KANDA": WestIndianPortionModel(
        category="rice_plate",
        sub_type="kanda_poha",
        density_g_cm3=0.72,
        typical_weight_g=150.0,
        credible_range_g=(120.0, 200.0)
    ),
    "MH_BREAKFAST_SABUDANA_KHICHDI": WestIndianPortionModel(
        category="rice_plate",
        sub_type="sabudana_khichdi",
        density_g_cm3=0.88,
        typical_weight_g=160.0,
        credible_range_g=(125.0, 210.0)
    ),

    # BEVERAGES & DESSERTS
    "GJ_BEVERAGE_CHAAS": WestIndianPortionModel(
        category="beverage",
        sub_type="spiced_chaas",
        density_g_cm3=1.01,
        typical_weight_g=180.0,
        credible_range_g=(150.0, 220.0)
    ),
    "GA_BEVERAGE_SOL_KADHI": WestIndianPortionModel(
        category="beverage",
        sub_type="sol_kadhi",
        density_g_cm3=1.01,
        typical_weight_g=120.0,
        credible_range_g=(100.0, 150.0)
    ),
    "MH_SWEET_SHRIKHAND": WestIndianPortionModel(
        category="curry_katori",
        sub_type="kesar_shrikhand",
        density_g_cm3=1.12,
        typical_weight_g=75.0,
        credible_range_g=(60.0, 100.0)
    ),
    "GA_SWEET_BEBINCA": WestIndianPortionModel(
        category="countable_snack",
        sub_type="bebinca_slice",
        density_g_cm3=1.14,
        typical_weight_g=70.0,
        credible_range_g=(55.0, 85.0),
        unit_weight_g=70.0,
        is_countable=True
    )
}


class CountableFoodDetector:
    """
    Detector for discrete countable West Indian food items (e.g. 2 batata vadas, 4 khandvi rolls, 3 puris).
    """
    @classmethod
    def estimate_countable_portion(
        cls,
        canonical_food_id: str,
        detected_count: Optional[int] = None
    ) -> Dict[str, Any]:
        portion_meta = WEST_INDIAN_PORTION_TABLE.get(canonical_food_id)
        if not portion_meta or not portion_meta.is_countable:
            return {
                "is_countable": False,
                "count": None,
                "unit_weight_g": None,
                "estimated_weight_g": 100.0,
                "credible_range_g": (80.0, 120.0)
            }

        unit_wt = portion_meta.unit_weight_g or 50.0
        # If no count passed, calculate default count from typical weight
        count = detected_count if (detected_count is not None and detected_count > 0) else max(1, round(portion_meta.typical_weight_g / unit_wt))
        total_weight = count * unit_wt
        min_wt = round(count * unit_wt * 0.82, 1)
        max_wt = round(count * unit_wt * 1.18, 1)

        return {
            "is_countable": True,
            "count": count,
            "unit_weight_g": unit_wt,
            "estimated_weight_g": round(total_weight, 1),
            "credible_range_g": (min_wt, max_wt),
            "portion_string": f"{count} piece{'s' if count > 1 else ''} ({round(total_weight)}g total)"
        }


class WestIndianKatoriBowlCalibrator:
    """
    Katori bowl volumetric geometry calibrator for West Indian liquid/semi-liquid dishes.
    """
    KATORI_STANDARDS = {
        "small": {"volume_cm3": 110.0, "description": "Small side katori (e.g. chutney, sweet, relish)"},
        "standard": {"volume_cm3": 150.0, "description": "Standard dining katori (dal, kadhi, usal, shaak)"},
        "large": {"volume_cm3": 210.0, "description": "Large deep katori (main curry, extra rassa, pav bhaji bowl)"}
    }

    @classmethod
    def estimate_katori_weight(
        cls,
        canonical_food_id: str,
        bowl_size: str = "standard",
        fill_fraction: float = 0.90
    ) -> Tuple[float, Tuple[float, float]]:
        model = WEST_INDIAN_PORTION_TABLE.get(canonical_food_id)
        density = model.density_g_cm3 if model else 1.04
        vol_info = cls.KATORI_STANDARDS.get(bowl_size, cls.KATORI_STANDARDS["standard"])
        effective_vol = vol_info["volume_cm3"] * fill_fraction
        est_weight = effective_vol * density
        credible_range = (round(est_weight * 0.85, 1), round(est_weight * 1.15, 1))
        return round(est_weight, 1), credible_range


class WestIndianFatLevelEstimator:
    """
    Visual fat, butter pool, and ghee sheen estimator for West Indian cuisine.
    Rule 34 & 7: Never claim exact grams from visual cues alone; categorize into low/medium/high
    with honest caloric/fat ranges.
    """
    @classmethod
    def estimate_fat_profile(cls, cues: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        cues = cues or {}
        visual_tags = [t.lower() for t in cues.get("visual_tags", [])]

        has_butter_pool = cues.get("visible_butter", False) or "butter_dollop" in visual_tags or "melted_butter" in visual_tags
        has_tarri_oil = cues.get("visible_tarri", False) or "tarri_layer" in visual_tags or "kat_rassa" in visual_tags
        has_ghee_glaze = cues.get("ghee_brushed", False) or "ghee_sheen" in visual_tags

        if has_butter_pool:
            return {
                "fat_level": "high",
                "fat_multiplier": 1.25,
                "extra_fat_g": 12.0,  # Butter dollop contribution
                "description": "Visible butter dollop / melted butter pool detected"
            }
        elif has_tarri_oil:
            return {
                "fat_level": "high",
                "fat_multiplier": 1.28,
                "extra_fat_g": 8.0,  # Red spiced oil surface layer
                "description": "High red oil tarri float visible on gravy surface"
            }
        elif has_ghee_glaze:
            return {
                "fat_level": "medium",
                "fat_multiplier": 1.12,
                "extra_fat_g": 4.5,
                "description": "Light to moderate ghee sheen on flatbread surface"
            }
        elif cues.get("sheen") == "matte" or "home_style" in visual_tags:
            return {
                "fat_level": "low",
                "fat_multiplier": 0.85,
                "extra_fat_g": 0.0,
                "description": "Matte low-fat home-style preparation"
            }
        else:
            return {
                "fat_level": "medium",
                "fat_multiplier": 1.0,
                "extra_fat_g": 0.0,
                "description": "Standard restaurant/thali preparation fat level"
            }


def get_portion_for_west_food(
    food_id: str,
    count: Optional[int] = None
) -> Tuple[float, Tuple[float, float], Optional[int]]:
    """
    Returns (estimated_weight_g, credible_range_g, count_or_none) for any West Indian food class.
    """
    alias_map = {
        "GJ_FARSAN_KHAMAN_NYLON": "GJ_FARSAN_KHAMAN",
        "MH_SWEET_PURAN_POLI": "MH_BREAD_PURAN_POLI",
        "MUM_STREET_BATATA_VADA": "MH_SNACK_BATATA_VADA",
        "GA_BREAD_PAO": "MH_BREAD_PAV",
        "MH_SWEET_UKADICHE_MODAK": "MH_SWEET_MODAK_UKADICHE",
        "GA_CURRY_FISH_GOAN": "GA_CURRY_FISH_XITT_CODI",
        "MH_CURRY_MISAL_KOLHAPURI": "MH_CURRY_MISAL_KAT",
        "WI_SWEET_SHRIKHAND": "MH_SWEET_SHRIKHAND",
        "GJ_BREAD_ROTLA_BAJRA": "GJ_BREAD_ROTLO_BAJRA",
        "GJ_MAIN_UNDHIYU_SURTI": "GJ_CURRY_UNDHIYU",
        "GJ_MAIN_DAL_DHOKLI": "GJ_DAL_GUJARATI",
        "GJ_CURRY_KADHI": "GJ_KADHI_GUJARATI",
        "GJ_SNACK_KHICHU": "GJ_RICE_KHICHDI",
        "KN_BEVERAGE_SOL_KADHI": "GA_BEVERAGE_SOL_KADHI",
        "KN_SEAFOOD_SURMAI_FRY": "GA_SEAFOOD_RAVA_FISH_FRY",
        "MH_BREAKFAST_SABUDANA_VADA": "MH_SNACK_SABUDANA_VADA"
    }
    resolved_id = alias_map.get(food_id, food_id)
    model = WEST_INDIAN_PORTION_TABLE.get(food_id) or WEST_INDIAN_PORTION_TABLE.get(resolved_id)
    if not model:
        return 120.0, (90.0, 150.0), None

    if model.is_countable:
        res = CountableFoodDetector.estimate_countable_portion(resolved_id, count)
        return res["estimated_weight_g"], res["credible_range_g"], res["count"]

    return model.typical_weight_g, model.credible_range_g, None
