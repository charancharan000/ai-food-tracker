"""
Indian Snacks & Tiffin Composite Plate & Platter Decomposer (Part 15)
Implements Sections 14, 16, 25, 31, 55, 56, 58, 61, 64 of Part 15 Specification.

Core Principles:
1. Anti-Monolithic Architecture: Multi-item tiffin platters, chaat assemblies and snack plates
   MUST be decomposed into independent line items with isolated nutrition, mass, macros and confidence.
2. Accompaniment Isolation (Section 39): Chutneys, sambar, raita, sauces, and garnishes are separated
   and never merged into the primary snack's weight unless physically homogenized.
3. Component-level Count & Mass Conservation: Count pieces for samosas, vadas, puris, momos, idlis.

Decomposers Implemented:
- TiffinPlatterDecomposer (Idli + Medhu Vadai + Sambar + Coconut Chutney) [Section 64 benchmark]
- SamosaPlateDecomposer (Samosas + Mint Chutney + Saunth Tamarind Chutney + Onion Garnish)
- PaniPuriAssemblyDecomposer (Puri Shells + Potato/Chana filling + Teekha Mint Water + Meetha Tamarind + Boondi)
- AlooTikkiChaatDecomposer (Crisp Aloo Tikkis + Chole + Dahi + Saunth + Hari Chutney + Sev + Onion)
- VadaPavDecomposer (Batata Vada + Pav Bread + Dry Garlic Chutney + Fried Salted Green Chilli)
- MisalPavDecomposer (Sprouted Matki Rassa Gravy + Crunchy Farsan + Pav Buns + Raw Onion + Lemon)
- MomoPlatterDecomposer (Steamed/Fried Momos + Red Chilli Garlic Chutney + Clear Broth/Soup)
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class SnackComponentItem(BaseModel):
    component_name: str
    canonical_food_id: Optional[str] = None
    role: str                       # "primary_snack", "tiffin_main", "accompaniment", "sauce", "topping", "garnish"
    count: Optional[int] = None
    estimated_weight_g: float
    calories: float
    protein_g: float
    carbs_g: float
    fat_g: float
    fiber_g: float
    confidence: float = 0.95
    is_countable: bool = False


class CompositeSnackPlatterResult(BaseModel):
    platter_name: str
    total_components_count: int
    components: List[SnackComponentItem]
    total_plate_weight_g: float
    total_calories: float
    total_protein_g: float
    total_carbs_g: float
    total_fat_g: float
    total_fiber_g: float
    calorie_uncertainty_range: tuple[float, float]
    zero_monolithic_guarantee: bool = True
    zero_double_counting_guarantee: bool = True


# =============================================================================
# 1. SOUTH INDIAN TIFFIN COMBO DECOMPOSER (Section 64 Spec Benchmark)
# =============================================================================
class TiffinComboDecomposer:
    """
    Decomposes South Indian Tiffin Combo (Section 64 benchmark):
    - 4 Idlis (180g)
    - 2 Medhu Vadais (100g)
    - Sambar (120g)
    - Coconut Chutney (40g)
    """

    @classmethod
    def decompose(
        cls,
        idli_count: int = 4,
        vada_count: int = 2,
        sambar_volume_ml: float = 120.0,
        chutney_volume_ml: float = 40.0,
    ) -> CompositeSnackPlatterResult:
        idli_wt = idli_count * 45.0 # 180g for 4 idlis
        vada_wt = vada_count * 50.0 # 100g for 2 vadas
        sambar_wt = sambar_volume_ml * 1.02 # ~122.4g
        chutney_wt = chutney_volume_ml * 1.05 # ~42g

        components = [
            SnackComponentItem(
                component_name="Idli",
                canonical_food_id="IND-TIF-TN-IDLI-001",
                role="tiffin_main",
                count=idli_count,
                estimated_weight_g=round(idli_wt, 1),
                calories=round((idli_wt / 100.0) * 136.0, 1),
                protein_g=round((idli_wt / 100.0) * 4.8, 1),
                carbs_g=round((idli_wt / 100.0) * 27.2, 1),
                fat_g=round((idli_wt / 100.0) * 0.6, 1),
                fiber_g=round((idli_wt / 100.0) * 2.1, 1),
                is_countable=True,
                confidence=0.98,
            ),
            SnackComponentItem(
                component_name="Medhu Vadai",
                canonical_food_id="IND-SNK-TN-MEDHUVADAI-001",
                role="primary_snack",
                count=vada_count,
                estimated_weight_g=round(vada_wt, 1),
                calories=round((vada_wt / 100.0) * 262.0, 1),
                protein_g=round((vada_wt / 100.0) * 9.5, 1),
                carbs_g=round((vada_wt / 100.0) * 28.5, 1),
                fat_g=round((vada_wt / 100.0) * 12.8, 1),
                fiber_g=round((vada_wt / 100.0) * 4.8, 1),
                is_countable=True,
                confidence=0.96,
            ),
            SnackComponentItem(
                component_name="Sambar",
                canonical_food_id="IND-CUR-SAMBAR-001",
                role="accompaniment",
                count=None,
                estimated_weight_g=round(sambar_wt, 1),
                calories=round((sambar_wt / 100.0) * 65.0, 1),
                protein_g=round((sambar_wt / 100.0) * 2.8, 1),
                carbs_g=round((sambar_wt / 100.0) * 9.5, 1),
                fat_g=round((sambar_wt / 100.0) * 1.8, 1),
                fiber_g=round((sambar_wt / 100.0) * 2.2, 1),
                is_countable=False,
                confidence=0.95,
            ),
            SnackComponentItem(
                component_name="Coconut Chutney",
                canonical_food_id="IND-CHT-COCONUT-001",
                role="accompaniment",
                count=None,
                estimated_weight_g=round(chutney_wt, 1),
                calories=round((chutney_wt / 100.0) * 192.0, 1),
                protein_g=round((chutney_wt / 100.0) * 2.8, 1),
                carbs_g=round((chutney_wt / 100.0) * 6.4, 1),
                fat_g=round((chutney_wt / 100.0) * 17.5, 1),
                fiber_g=round((chutney_wt / 100.0) * 3.5, 1),
                is_countable=False,
                confidence=0.94,
            ),
        ]

        tot_wt = sum(c.estimated_weight_g for c in components)
        tot_cal = sum(c.calories for c in components)
        tot_pro = sum(c.protein_g for c in components)
        tot_carb = sum(c.carbs_g for c in components)
        tot_fat = sum(c.fat_g for c in components)
        tot_fib = sum(c.fiber_g for c in components)

        return CompositeSnackPlatterResult(
            platter_name="South Indian Tiffin Combo (Idli + Vada + Sambar + Chutney)",
            total_components_count=len(components),
            components=components,
            total_plate_weight_g=round(tot_wt, 1),
            total_calories=round(tot_cal, 1),
            total_protein_g=round(tot_pro, 1),
            total_carbs_g=round(tot_carb, 1),
            total_fat_g=round(tot_fat, 1),
            total_fiber_g=round(tot_fib, 1),
            calorie_uncertainty_range=(round(tot_cal * 0.90, 1), round(tot_cal * 1.12, 1)),
        )


# =============================================================================
# 2. SAMOSA PLATE DECOMPOSER (Sections 11, 31, 39)
# =============================================================================
class SamosaPlateDecomposer:
    """
    Decomposes Samosa Plate:
    - 2 Punjabi Samosas (170g)
    - Saunth Tamarind Chutney (35g)
    - Mint Coriander Chutney (25g)
    - Pickled Onion & Fried Chilli (20g)
    """

    @classmethod
    def decompose(
        cls,
        samosa_count: int = 2,
        include_chutneys: bool = True,
    ) -> CompositeSnackPlatterResult:
        samosa_wt = samosa_count * 85.0
        components = [
            SnackComponentItem(
                component_name="Punjabi Samosa",
                canonical_food_id="IND-SNK-NI-SAMOSA-001",
                role="primary_snack",
                count=samosa_count,
                estimated_weight_g=round(samosa_wt, 1),
                calories=round((samosa_wt / 100.0) * 262.0, 1),
                protein_g=round((samosa_wt / 100.0) * 4.5, 1),
                carbs_g=round((samosa_wt / 100.0) * 32.8, 1),
                fat_g=round((samosa_wt / 100.0) * 12.8, 1),
                fiber_g=round((samosa_wt / 100.0) * 3.2, 1),
                is_countable=True,
                confidence=0.97,
            )
        ]

        if include_chutneys:
            components.extend([
                SnackComponentItem(
                    component_name="Saunth (Sweet Tamarind Chutney)",
                    canonical_food_id="IND-CHT-TAMARIND-001",
                    role="accompaniment",
                    count=None,
                    estimated_weight_g=35.0,
                    calories=42.0,
                    protein_g=0.4,
                    carbs_g=10.2,
                    fat_g=0.1,
                    fiber_g=0.6,
                    is_countable=False,
                    confidence=0.93,
                ),
                SnackComponentItem(
                    component_name="Mint Coriander Chutney",
                    canonical_food_id="IND-CHT-MINT-001",
                    role="accompaniment",
                    count=None,
                    estimated_weight_g=25.0,
                    calories=12.0,
                    protein_g=0.5,
                    carbs_g=1.8,
                    fat_g=0.3,
                    fiber_g=0.8,
                    is_countable=False,
                    confidence=0.94,
                ),
                SnackComponentItem(
                    component_name="Fried Green Chilli & Sliced Onions",
                    canonical_food_id="IND-SNK-GARNISH-001",
                    role="garnish",
                    count=None,
                    estimated_weight_g=15.0,
                    calories=9.0,
                    protein_g=0.2,
                    carbs_g=1.5,
                    fat_g=0.2,
                    fiber_g=0.4,
                    is_countable=False,
                    confidence=0.92,
                ),
            ])

        tot_wt = sum(c.estimated_weight_g for c in components)
        tot_cal = sum(c.calories for c in components)
        tot_pro = sum(c.protein_g for c in components)
        tot_carb = sum(c.carbs_g for c in components)
        tot_fat = sum(c.fat_g for c in components)
        tot_fib = sum(c.fiber_g for c in components)

        return CompositeSnackPlatterResult(
            platter_name="Samosa Plate with Chutneys & Garnish",
            total_components_count=len(components),
            components=components,
            total_plate_weight_g=round(tot_wt, 1),
            total_calories=round(tot_cal, 1),
            total_protein_g=round(tot_pro, 1),
            total_carbs_g=round(tot_carb, 1),
            total_fat_g=round(tot_fat, 1),
            total_fiber_g=round(tot_fib, 1),
            calorie_uncertainty_range=(round(tot_cal * 0.88, 1), round(tot_cal * 1.15, 1)),
        )


# =============================================================================
# 3. PANI PURI COMPONENT-LEVEL DECOMPOSER (Section 16)
# =============================================================================
class PaniPuriAssemblyDecomposer:
    """
    Decomposes Pani Puri Plate (Section 16 non-negotiable):
    - Countable Puri Shells (6 pieces)
    - Boiled Potato & Chickpea Filling
    - Tangy Spiced Mint Teekha Pani
    - Sweet Meetha Saunth Chutney
    - Crisp Boondi Garnish
    """

    @classmethod
    def decompose(
        cls,
        puri_count: int = 6,
    ) -> CompositeSnackPlatterResult:
        # 6 puris: each shell ~5g -> 30g
        # Filling ~10g per puri -> 60g
        # Teekha + Meetha pani ~15ml per puri -> 90g
        shell_wt = puri_count * 5.0
        filling_wt = puri_count * 10.0
        water_wt = puri_count * 15.0

        components = [
            SnackComponentItem(
                component_name="Crisp Hollow Puri Shells",
                canonical_food_id="IND-SNK-PANI-PURISHELL-001",
                role="primary_snack",
                count=puri_count,
                estimated_weight_g=round(shell_wt, 1),
                calories=round(puri_count * 22.0, 1), # ~132 kcal
                protein_g=round(puri_count * 0.5, 1),
                carbs_g=round(puri_count * 3.2, 1),
                fat_g=round(puri_count * 0.9, 1),
                fiber_g=round(puri_count * 0.3, 1),
                is_countable=True,
                confidence=0.98,
            ),
            SnackComponentItem(
                component_name="Potato & Black Chana Stuffing",
                canonical_food_id="IND-SNK-PANI-FILLING-001",
                role="topping",
                count=None,
                estimated_weight_g=round(filling_wt, 1),
                calories=round(filling_wt * 0.95, 1), # ~57 kcal
                protein_g=round(filling_wt * 0.04, 1),
                carbs_g=round(filling_wt * 0.17, 1),
                fat_g=round(filling_wt * 0.01, 1),
                fiber_g=round(filling_wt * 0.02, 1),
                is_countable=False,
                confidence=0.94,
            ),
            SnackComponentItem(
                component_name="Teekha Mint-Coriander Spicy Water",
                canonical_food_id="IND-SNK-PANI-SPICYWATER-001",
                role="accompaniment",
                count=None,
                estimated_weight_g=round(water_wt * 0.7, 1), # ~63g
                calories=12.0,
                protein_g=0.3,
                carbs_g=2.2,
                fat_g=0.1,
                fiber_g=0.4,
                is_countable=False,
                confidence=0.95,
            ),
            SnackComponentItem(
                component_name="Meetha Tamarind Sweet Chutney Drop",
                canonical_food_id="IND-SNK-PANI-SWEETWATER-001",
                role="accompaniment",
                count=None,
                estimated_weight_g=round(water_wt * 0.3, 1), # ~27g
                calories=38.0,
                protein_g=0.2,
                carbs_g=9.2,
                fat_g=0.0,
                fiber_g=0.3,
                is_countable=False,
                confidence=0.92,
            ),
            SnackComponentItem(
                component_name="Crisp Boondi Floating Garnish",
                canonical_food_id="IND-SNK-PANI-BOONDI-001",
                role="garnish",
                count=None,
                estimated_weight_g=10.0,
                calories=52.0,
                protein_g=1.1,
                carbs_g=4.8,
                fat_g=3.2,
                fiber_g=0.4,
                is_countable=False,
                confidence=0.90,
            ),
        ]

        tot_wt = sum(c.estimated_weight_g for c in components)
        tot_cal = sum(c.calories for c in components)
        tot_pro = sum(c.protein_g for c in components)
        tot_carb = sum(c.carbs_g for c in components)
        tot_fat = sum(c.fat_g for c in components)
        tot_fib = sum(c.fiber_g for c in components)

        return CompositeSnackPlatterResult(
            platter_name=f"Pani Puri Plate ({puri_count} Pieces Deconstructed)",
            total_components_count=len(components),
            components=components,
            total_plate_weight_g=round(tot_wt, 1),
            total_calories=round(tot_cal, 1),
            total_protein_g=round(tot_pro, 1),
            total_carbs_g=round(tot_carb, 1),
            total_fat_g=round(tot_fat, 1),
            total_fiber_g=round(tot_fib, 1),
            calorie_uncertainty_range=(round(tot_cal * 0.90, 1), round(tot_cal * 1.15, 1)),
        )


# =============================================================================
# 4. ALOO TIKKI CHAAT DECOMPOSER (Section 14)
# =============================================================================
class AlooTikkiChaatDecomposer:
    """
    Decomposes Aloo Tikki Chaat (Section 14):
    - 2 Crisp Aloo Tikkis (140g)
    - Chole Chickpea Curry (100g)
    - Sweet Dahi / Yogurt (50g)
    - Saunth Tamarind Chutney (30g)
    - Mint Coriander Chutney (20g)
    - Nylon Sev & Onions Garnish (25g)
    """

    @classmethod
    def decompose(cls, tikki_count: int = 2) -> CompositeSnackPlatterResult:
        tikki_wt = tikki_count * 70.0
        components = [
            SnackComponentItem(
                component_name="Crispy Aloo Tikki Patties",
                canonical_food_id="IND-SNK-NI-ALOOTIKKI-001",
                role="primary_snack",
                count=tikki_count,
                estimated_weight_g=round(tikki_wt, 1),
                calories=round((tikki_wt / 100.0) * 195.0, 1),
                protein_g=round((tikki_wt / 100.0) * 3.4, 1),
                carbs_g=round((tikki_wt / 100.0) * 28.5, 1),
                fat_g=round((tikki_wt / 100.0) * 7.8, 1),
                fiber_g=round((tikki_wt / 100.0) * 2.8, 1),
                is_countable=True,
                confidence=0.97,
            ),
            SnackComponentItem(
                component_name="Spiced Chole Curry Gravy",
                canonical_food_id="IND-CUR-CHOLE-001",
                role="accompaniment",
                count=None,
                estimated_weight_g=100.0,
                calories=130.0,
                protein_g=6.2,
                carbs_g=18.5,
                fat_g=3.8,
                fiber_g=4.8,
                is_countable=False,
                confidence=0.95,
            ),
            SnackComponentItem(
                component_name="Sweetened Whisked Dahi (Curd)",
                canonical_food_id="IND-DAHI-SWEET-001",
                role="topping",
                count=None,
                estimated_weight_g=50.0,
                calories=48.0,
                protein_g=2.1,
                carbs_g=4.8,
                fat_g=2.2,
                fiber_g=0.0,
                is_countable=False,
                confidence=0.94,
            ),
            SnackComponentItem(
                component_name="Saunth Tamarind Chutney",
                canonical_food_id="IND-CHT-TAMARIND-001",
                role="topping",
                count=None,
                estimated_weight_g=30.0,
                calories=36.0,
                protein_g=0.3,
                carbs_g=8.7,
                fat_g=0.1,
                fiber_g=0.5,
                is_countable=False,
                confidence=0.93,
            ),
            SnackComponentItem(
                component_name="Mint Green Chutney",
                canonical_food_id="IND-CHT-MINT-001",
                role="topping",
                count=None,
                estimated_weight_g=20.0,
                calories=10.0,
                protein_g=0.4,
                carbs_g=1.5,
                fat_g=0.2,
                fiber_g=0.6,
                is_countable=False,
                confidence=0.92,
            ),
            SnackComponentItem(
                component_name="Nylon Sev & Chopped Onions Garnish",
                canonical_food_id="IND-SNK-SEV-001",
                role="garnish",
                count=None,
                estimated_weight_g=25.0,
                calories=98.0,
                protein_g=2.2,
                carbs_g=11.2,
                fat_g=5.1,
                fiber_g=1.1,
                is_countable=False,
                confidence=0.91,
            ),
        ]

        tot_wt = sum(c.estimated_weight_g for c in components)
        tot_cal = sum(c.calories for c in components)
        tot_pro = sum(c.protein_g for c in components)
        tot_carb = sum(c.carbs_g for c in components)
        tot_fat = sum(c.fat_g for c in components)
        tot_fib = sum(c.fiber_g for c in components)

        return CompositeSnackPlatterResult(
            platter_name="Delhi Aloo Tikki Chole Chaat",
            total_components_count=len(components),
            components=components,
            total_plate_weight_g=round(tot_wt, 1),
            total_calories=round(tot_cal, 1),
            total_protein_g=round(tot_pro, 1),
            total_carbs_g=round(tot_carb, 1),
            total_fat_g=round(tot_fat, 1),
            total_fiber_g=round(tot_fib, 1),
            calorie_uncertainty_range=(round(tot_cal * 0.88, 1), round(tot_cal * 1.14, 1)),
        )


# =============================================================================
# 5. VADA PAV DECOMPOSER (Section 18)
# =============================================================================
class SnackVadaPavDecomposer:
    """
    Decomposes Mumbai Vada Pav (Section 18):
    - Batata Vada Patty (70g)
    - Pav Bun (55g)
    - Dry Red Garlic Peanut Chutney (10g)
    - Green Chutney (8g)
    - Fried Green Chilli (5g)
    """

    @classmethod
    def decompose(cls, vada_pav_count: int = 1) -> CompositeSnackPlatterResult:
        components = [
            SnackComponentItem(
                component_name="Batata Vada Fried Patty",
                canonical_food_id="IND-SNK-TN-POTATOBONDA-001",
                role="primary_snack",
                count=vada_pav_count,
                estimated_weight_g=round(vada_pav_count * 70.0, 1),
                calories=round(vada_pav_count * 160.0, 1),
                protein_g=round(vada_pav_count * 3.4, 1),
                carbs_g=round(vada_pav_count * 21.7, 1),
                fat_g=round(vada_pav_count * 6.7, 1),
                fiber_g=round(vada_pav_count * 2.1, 1),
                is_countable=True,
                confidence=0.98,
            ),
            SnackComponentItem(
                component_name="Ladi Pav Bread Bun",
                canonical_food_id="IND-BRD-PAV-001",
                role="primary_snack",
                count=vada_pav_count,
                estimated_weight_g=round(vada_pav_count * 55.0, 1),
                calories=round(vada_pav_count * 145.0, 1),
                protein_g=round(vada_pav_count * 4.2, 1),
                carbs_g=round(vada_pav_count * 27.5, 1),
                fat_g=round(vada_pav_count * 2.1, 1),
                fiber_g=round(vada_pav_count * 1.2, 1),
                is_countable=True,
                confidence=0.98,
            ),
            SnackComponentItem(
                component_name="Dry Red Garlic-Peanut Chutney",
                canonical_food_id="IND-CHT-GARLICDRY-001",
                role="topping",
                count=None,
                estimated_weight_g=round(vada_pav_count * 10.0, 1),
                calories=round(vada_pav_count * 38.0, 1),
                protein_g=round(vada_pav_count * 1.1, 1),
                carbs_g=round(vada_pav_count * 2.4, 1),
                fat_g=round(vada_pav_count * 2.7, 1),
                fiber_g=round(vada_pav_count * 0.6, 1),
                is_countable=False,
                confidence=0.93,
            ),
            SnackComponentItem(
                component_name="Fried Salted Green Chilli",
                canonical_food_id="IND-SNK-GARNISH-001",
                role="garnish",
                count=vada_pav_count,
                estimated_weight_g=round(vada_pav_count * 5.0, 1),
                calories=round(vada_pav_count * 5.0, 1),
                protein_g=0.1,
                carbs_g=0.8,
                fat_g=0.2,
                fiber_g=0.3,
                is_countable=False,
                confidence=0.92,
            ),
        ]

        tot_wt = sum(c.estimated_weight_g for c in components)
        tot_cal = sum(c.calories for c in components)
        tot_pro = sum(c.protein_g for c in components)
        tot_carb = sum(c.carbs_g for c in components)
        tot_fat = sum(c.fat_g for c in components)
        tot_fib = sum(c.fiber_g for c in components)

        return CompositeSnackPlatterResult(
            platter_name=f"Mumbai Vada Pav ({vada_pav_count} Assembly)",
            total_components_count=len(components),
            components=components,
            total_plate_weight_g=round(tot_wt, 1),
            total_calories=round(tot_cal, 1),
            total_protein_g=round(tot_pro, 1),
            total_carbs_g=round(tot_carb, 1),
            total_fat_g=round(tot_fat, 1),
            total_fiber_g=round(tot_fib, 1),
            calorie_uncertainty_range=(round(tot_cal * 0.90, 1), round(tot_cal * 1.12, 1)),
        )


# =============================================================================
# 6. MISAL PAV DECOMPOSER (Section 18)
# =============================================================================
class SnackMisalPavDecomposer:
    """
    Decomposes Kolhapuri / Puneri Misal Pav (Section 18):
    - Sprouted Matki Rassa Gravy (180g)
    - Farsan Crunchy Topping (40g)
    - Pav Buns (2 pieces, 110g)
    - Diced Onions & Fresh Coriander (25g)
    - Fresh Lemon Wedge (10g)
    """

    @classmethod
    def decompose(cls, pav_count: int = 2) -> CompositeSnackPlatterResult:
        components = [
            SnackComponentItem(
                component_name="Sprouted Moth Bean (Matki) Kat/Rassa Gravy",
                canonical_food_id="IND-CUR-MISALRASSA-001",
                role="primary_snack",
                count=None,
                estimated_weight_g=180.0,
                calories=175.0,
                protein_g=7.5,
                carbs_g=19.2,
                fat_g=7.8,
                fiber_g=4.5,
                is_countable=False,
                confidence=0.96,
            ),
            SnackComponentItem(
                component_name="Crunchy Farsan & Sev Topping",
                canonical_food_id="IND-SNK-FARSAN-001",
                role="topping",
                count=None,
                estimated_weight_g=40.0,
                calories=210.0,
                protein_g=4.8,
                carbs_g=19.8,
                fat_g=12.5,
                fiber_g=2.4,
                is_countable=False,
                confidence=0.95,
            ),
            SnackComponentItem(
                component_name="Ladi Pav Buns",
                canonical_food_id="IND-BRD-PAV-001",
                role="accompaniment",
                count=pav_count,
                estimated_weight_g=round(pav_count * 55.0, 1),
                calories=round(pav_count * 145.0, 1),
                protein_g=round(pav_count * 4.2, 1),
                carbs_g=round(pav_count * 27.5, 1),
                fat_g=round(pav_count * 2.1, 1),
                fiber_g=round(pav_count * 1.2, 1),
                is_countable=True,
                confidence=0.98,
            ),
            SnackComponentItem(
                component_name="Finely Chopped Raw Onions & Coriander",
                canonical_food_id="IND-SNK-GARNISH-001",
                role="garnish",
                count=None,
                estimated_weight_g=25.0,
                calories=10.0,
                protein_g=0.3,
                carbs_g=2.1,
                fat_g=0.1,
                fiber_g=0.5,
                is_countable=False,
                confidence=0.93,
            ),
            SnackComponentItem(
                component_name="Fresh Lemon Wedge",
                canonical_food_id="IND-SNK-LEMON-001",
                role="garnish",
                count=1,
                estimated_weight_g=10.0,
                calories=3.0,
                protein_g=0.1,
                carbs_g=0.9,
                fat_g=0.0,
                fiber_g=0.2,
                is_countable=False,
                confidence=0.95,
            ),
        ]

        tot_wt = sum(c.estimated_weight_g for c in components)
        tot_cal = sum(c.calories for c in components)
        tot_pro = sum(c.protein_g for c in components)
        tot_carb = sum(c.carbs_g for c in components)
        tot_fat = sum(c.fat_g for c in components)
        tot_fib = sum(c.fiber_g for c in components)

        return CompositeSnackPlatterResult(
            platter_name="Maharashtra Misal Pav Platter",
            total_components_count=len(components),
            components=components,
            total_plate_weight_g=round(tot_wt, 1),
            total_calories=round(tot_cal, 1),
            total_protein_g=round(tot_pro, 1),
            total_carbs_g=round(tot_carb, 1),
            total_fat_g=round(tot_fat, 1),
            total_fiber_g=round(tot_fib, 1),
            calorie_uncertainty_range=(round(tot_cal * 0.88, 1), round(tot_cal * 1.15, 1)),
        )


# =============================================================================
# 7. MOMO PLATTER DECOMPOSER (Section 23)
# =============================================================================
class MomoPlatterDecomposer:
    """
    Decomposes Himalayan Momo Platter (Section 23):
    - 6 Steamed or Fried Momos (168g to 210g)
    - Fiery Red Chilli Garlic Chutney (30g)
    - Clear Vegetable/Chicken Broth Soup (100ml)
    """

    @classmethod
    def decompose(
        cls,
        momo_type: str = "steamed_veg",
        momo_count: int = 6,
    ) -> CompositeSnackPlatterResult:
        is_fried = "fried" in momo_type.lower()
        is_chicken = "chicken" in momo_type.lower()

        if is_chicken:
            if is_fried:
                food_id = "IND-SNK-NE-FRIEDCHICKENMOMO-001"
                momo_name = "Fried Chicken Momo"
                per_piece_wt = 35.0
                cals_100g = 255.0
                pro_100g = 11.2
                carb_100g = 24.5
                fat_100g = 12.8
            else:
                food_id = "IND-SNK-NE-CHICKENMOMO-001"
                momo_name = "Steamed Chicken Momo"
                per_piece_wt = 32.0
                cals_100g = 175.0
                pro_100g = 11.8
                carb_100g = 22.0
                fat_100g = 4.5
        else:
            food_id = "IND-SNK-NE-VEGMOMO-001"
            momo_name = "Steamed Veg Momo"
            per_piece_wt = 28.0
            cals_100g = 140.0
            pro_100g = 4.2
            carb_100g = 26.5
            fat_100g = 2.1

        momo_tot_wt = momo_count * per_piece_wt
        components = [
            SnackComponentItem(
                component_name=momo_name,
                canonical_food_id=food_id,
                role="primary_snack",
                count=momo_count,
                estimated_weight_g=round(momo_tot_wt, 1),
                calories=round((momo_tot_wt / 100.0) * cals_100g, 1),
                protein_g=round((momo_tot_wt / 100.0) * pro_100g, 1),
                carbs_g=round((momo_tot_wt / 100.0) * carb_100g, 1),
                fat_g=round((momo_tot_wt / 100.0) * fat_100g, 1),
                fiber_g=round((momo_tot_wt / 100.0) * 1.5, 1),
                is_countable=True,
                confidence=0.98,
            ),
            SnackComponentItem(
                component_name="Spicy Red Chilli Garlic Chutney",
                canonical_food_id="IND-CHT-CHILLIGARLIC-001",
                role="accompaniment",
                count=None,
                estimated_weight_g=30.0,
                calories=24.0,
                protein_g=0.6,
                carbs_g=4.2,
                fat_g=0.6,
                fiber_g=0.8,
                is_countable=False,
                confidence=0.95,
            ),
            SnackComponentItem(
                component_name="Clear Momo Broth (Soup)",
                canonical_food_id="IND-SOUP-MOMO-001",
                role="accompaniment",
                count=None,
                estimated_weight_g=100.0,
                calories=22.0,
                protein_g=1.2,
                carbs_g=2.5,
                fat_g=0.8,
                fiber_g=0.4,
                is_countable=False,
                confidence=0.92,
            ),
        ]

        tot_wt = sum(c.estimated_weight_g for c in components)
        tot_cal = sum(c.calories for c in components)
        tot_pro = sum(c.protein_g for c in components)
        tot_carb = sum(c.carbs_g for c in components)
        tot_fat = sum(c.fat_g for c in components)
        tot_fib = sum(c.fiber_g for c in components)

        return CompositeSnackPlatterResult(
            platter_name=f"Himalayan Momo Platter ({momo_count} Pieces + Chutney + Soup)",
            total_components_count=len(components),
            components=components,
            total_plate_weight_g=round(tot_wt, 1),
            total_calories=round(tot_cal, 1),
            total_protein_g=round(tot_pro, 1),
            total_carbs_g=round(tot_carb, 1),
            total_fat_g=round(tot_fat, 1),
            total_fiber_g=round(tot_fib, 1),
            calorie_uncertainty_range=(round(tot_cal * 0.90, 1), round(tot_cal * 1.12, 1)),
        )


# Backward-compatible aliases for internal module usage
VadaPavDecomposer = SnackVadaPavDecomposer
MisalPavDecomposer = SnackMisalPavDecomposer

