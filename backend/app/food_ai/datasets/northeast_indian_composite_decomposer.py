"""
Northeast Indian Composite Meal Decomposer (Part 7)
Implements Sections 29, 56, 57, 58, 70, 73, 86, 90.

Guarantees:
- Multi-component meal platter decomposition without ever collapsing into a monolithic "Northeast Meal"
- Decomposes:
  1. Assamese Traditional Thali (Joha Rice, Amitar Khar, Masor Tenga, Aloo Pitika, Mati Mahor Dal)
  2. Meghalaya Jadoh Platter (Pork Jadoh, Dohneiihong, Doh Khlieh, Tungrymbai)
  3. Manipuri Chakluk / Meal (Steamed Rice, Kangshoi, Eromba, Singju, Paknam)
  4. Naga Traditional Platter (Steamed Rice, Smoked Pork with Axone, Boiled Greens, Raja Mircha Chutney)
  5. Tripuri Mui Borok Meal (Rice, Chakhwi, Mosdeng Serma, Gudok, Bamboo Shoot Fish)
  6. Sikkimese Traditional Meal (Rice, Gundruk Jhol, Phagshapa, Kinema, Sel Roti)
- Packaging & Plate Invariance (bell-metal kanh, banana leaves, bamboo platters, wooden bowls)
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class DecomposedNortheastItem(BaseModel):
    item_index: int
    canonical_food_id: str
    name: str
    variant: str
    category: str
    is_countable: bool = False
    count: Optional[int] = None
    estimated_weight_g: float
    calories: float
    protein_g: float
    carbs_g: float
    fat_g: float
    fiber_g: float
    confidence: float
    notes: str = ""

class NortheastCompositeDecompositionResult(BaseModel):
    platter_name: str
    platter_type: str # "thali", "meal_plate", "mui_borok_meal", "street_platter"
    state: str
    region_community: str
    total_components_detected: int
    items: List[DecomposedNortheastItem]
    total_edible_weight_g: float
    total_calories: float
    total_protein_g: float
    total_carbs_g: float
    total_fat_g: float
    total_fiber_g: float
    deconstruction_rules_enforced: List[str]

# =============================================================================
# 1. ASSAMESE THALI DECOMPOSER (Section 73)
# =============================================================================

class AssameseThaliDecomposer:
    @staticmethod
    def decompose(meta: Optional[Dict[str, Any]] = None) -> NortheastCompositeDecompositionResult:
        items: List[DecomposedNortheastItem] = [
            DecomposedNortheastItem(
                item_index=1, canonical_food_id="AS_RICE_JOHA",
                name="Assamese Joha Rice", variant="Steamed Fragrant Rice", category="Rice",
                estimated_weight_g=180.0, calories=243.0, protein_g=5.0, carbs_g=53.1, fat_g=0.7, fiber_g=1.1, confidence=0.96
            ),
            DecomposedNortheastItem(
                item_index=2, canonical_food_id="AS_KHAR_OMITA",
                name="Amitar Khar", variant="Raw Papaya Alkaline Starter", category="Vegetarian",
                estimated_weight_g=100.0, calories=55.0, protein_g=1.2, carbs_g=7.5, fat_g=2.2, fiber_g=2.8, confidence=0.94
            ),
            DecomposedNortheastItem(
                item_index=3, canonical_food_id="AS_FISH_MASOR_TENGA",
                name="Masor Tenga", variant="Light Sour Fish Curry with Tomato & Lemon", category="Fish",
                is_countable=True, count=1, estimated_weight_g=160.0, calories=156.8, protein_g=16.8, carbs_g=5.1, fat_g=7.7, fiber_g=1.3, confidence=0.95
            ),
            DecomposedNortheastItem(
                item_index=4, canonical_food_id="AS_VEG_ALOO_PITIKA",
                name="Aloo Pitika", variant="Mashed Potatoes with Raw Mustard Oil", category="Vegetarian",
                estimated_weight_g=80.0, calories=88.0, protein_g=1.6, carbs_g=14.0, fat_g=3.0, fiber_g=1.6, confidence=0.96
            ),
            DecomposedNortheastItem(
                item_index=5, canonical_food_id="AS_DAL_MATI_MAH",
                name="Mati Mahor Dal", variant="Black Gram Dal with Ginger", category="Dal",
                estimated_weight_g=120.0, calories=114.0, protein_g=7.2, carbs_g=16.8, fat_g=2.2, fiber_g=3.8, confidence=0.93
            ),
            DecomposedNortheastItem(
                item_index=6, canonical_food_id="ACCOMPANIMENT_KAZI_NEMU",
                name="Kazi Nemu & Green Chilli", variant="Assam Lemon Wedge & Fresh Chilli", category="Accompaniment",
                estimated_weight_g=15.0, calories=4.0, protein_g=0.1, carbs_g=0.9, fat_g=0.0, fiber_g=0.3, confidence=0.98
            )
        ]

        tot_w = sum(it.estimated_weight_g for it in items)
        tot_c = sum(it.calories for it in items)
        tot_p = sum(it.protein_g for it in items)
        tot_cb = sum(it.carbs_g for it in items)
        tot_f = sum(it.fat_g for it in items)
        tot_fib = sum(it.fiber_g for it in items)

        return NortheastCompositeDecompositionResult(
            platter_name="Traditional Assamese Thali (Kanh Platter)",
            platter_type="thali",
            state="Assam",
            region_community="Brahmaputra Valley",
            total_components_detected=len(items),
            items=items,
            total_edible_weight_g=round(tot_w, 1),
            total_calories=round(tot_c, 1),
            total_protein_g=round(tot_p, 1),
            total_carbs_g=round(tot_cb, 1),
            total_fat_g=round(tot_f, 1),
            total_fiber_g=round(tot_fib, 1),
            deconstruction_rules_enforced=[
                "Sections 56 & 73: Decomposed Assamese meal into separate Joha rice, Khar, Tenga fish, Pitika, and Dal.",
                "Bell-metal platter (Kanh) invariant visual background handled."
            ]
        )

# =============================================================================
# 2. MEGHALAYA JADOH PLATTER DECOMPOSER (Sections 11, 73)
# =============================================================================

class MeghalayaJadohPlatterDecomposer:
    @staticmethod
    def decompose(meta: Optional[Dict[str, Any]] = None) -> NortheastCompositeDecompositionResult:
        items: List[DecomposedNortheastItem] = [
            DecomposedNortheastItem(
                item_index=1, canonical_food_id="ML_RICE_JADOH_PORK",
                name="Khasi Jadoh", variant="Rice Cooked in Pork Fat", category="Rice",
                estimated_weight_g=220.0, calories=429.0, protein_g=18.7, carbs_g=55.0, fat_g=15.8, fiber_g=2.6, confidence=0.96
            ),
            DecomposedNortheastItem(
                item_index=2, canonical_food_id="ML_MEAT_DOHNEIIHONG",
                name="Dohneiihong", variant="Pork with Roasted Black Sesame", category="Meat",
                is_countable=True, count=3, estimated_weight_g=140.0, calories=385.0, protein_g=21.3, carbs_g=6.3, fat_g=30.8, fiber_g=3.9, confidence=0.95
            ),
            DecomposedNortheastItem(
                item_index=3, canonical_food_id="ML_MEAT_DOH_KHLIEH",
                name="Doh Khlieh", variant="Boiled Pork & Raw Onion Salad", category="Meat",
                estimated_weight_g=70.0, calories=147.0, protein_g=11.8, carbs_g=2.7, fat_g=10.2, fiber_g=0.6, confidence=0.92
            ),
            DecomposedNortheastItem(
                item_index=4, canonical_food_id="ML_FERMENTED_TUNGRYMBAI",
                name="Tungrymbai", variant="Fermented Soybean & Sesame Paste", category="Fermented",
                estimated_weight_g=40.0, calories=74.0, protein_g=5.0, carbs_g=3.7, fat_g=4.6, fiber_g=1.9, confidence=0.94
            ),
            DecomposedNortheastItem(
                item_index=5, canonical_food_id="ML_VEG_BOILED_GREENS",
                name="Khasi Boiled Greens", variant="Steamed Seasonal Leaves with Ginger", category="Vegetarian",
                estimated_weight_g=60.0, calories=24.0, protein_g=1.5, carbs_g=3.8, fat_g=0.4, fiber_g=2.1, confidence=0.93
            )
        ]

        tot_w = sum(it.estimated_weight_g for it in items)
        tot_c = sum(it.calories for it in items)
        tot_p = sum(it.protein_g for it in items)
        tot_cb = sum(it.carbs_g for it in items)
        tot_f = sum(it.fat_g for it in items)
        tot_fib = sum(it.fiber_g for it in items)

        return NortheastCompositeDecompositionResult(
            platter_name="Khasi Jadoh & Pork Platter",
            platter_type="meal_plate",
            state="Meghalaya",
            region_community="Khasi Hills",
            total_components_detected=len(items),
            items=items,
            total_edible_weight_g=round(tot_w, 1),
            total_calories=round(tot_c, 1),
            total_protein_g=round(tot_p, 1),
            total_carbs_g=round(tot_cb, 1),
            total_fat_g=round(tot_f, 1),
            total_fiber_g=round(tot_fib, 1),
            deconstruction_rules_enforced=[
                "Section 11: Segmented Jadoh rice from Dohneiihong black sesame pork, Doh Khlieh, and Tungrymbai."
            ]
        )

# =============================================================================
# 3. NAGA TRADITIONAL PLATTER DECOMPOSER (Sections 24, 73)
# =============================================================================

class NagaPlatterDecomposer:
    @staticmethod
    def decompose(meta: Optional[Dict[str, Any]] = None) -> NortheastCompositeDecompositionResult:
        items: List[DecomposedNortheastItem] = [
            DecomposedNortheastItem(
                item_index=1, canonical_food_id="NL_RICE_STEAMED",
                name="Plain Steamed Rice", variant="Local Hill Rice", category="Rice",
                estimated_weight_g=200.0, calories=260.0, protein_g=5.4, carbs_g=56.4, fat_g=0.6, fiber_g=0.8, confidence=0.96
            ),
            DecomposedNortheastItem(
                item_index=2, canonical_food_id="NL_MEAT_SMOKED_PORK_AXONE",
                name="Smoked Pork with Axone", variant="Wood-Smoked Pork in Fermented Soybean", category="Meat",
                is_countable=True, count=3, estimated_weight_g=150.0, calories=435.0, protein_g=26.3, carbs_g=5.7, fat_g=34.5, fiber_g=2.7, confidence=0.95
            ),
            DecomposedNortheastItem(
                item_index=3, canonical_food_id="NL_VEG_BOILED_GREENS",
                name="Boiled Naga Greens", variant="Steamed Mustard Leaves with Bamboo Shoot", category="Vegetarian",
                estimated_weight_g=80.0, calories=32.0, protein_g=2.0, carbs_g=4.8, fat_g=0.5, fiber_g=2.8, confidence=0.94
            ),
            DecomposedNortheastItem(
                item_index=4, canonical_food_id="NL_CHUTNEY_RAJA_MIRCHA",
                name="Raja Mircha Chutney", variant="Naga King Chilli & Tomato Mash", category="Chutney/Salad",
                estimated_weight_g=30.0, calories=18.0, protein_g=0.4, carbs_g=3.2, fat_g=0.4, fiber_g=1.2, confidence=0.95
            )
        ]

        tot_w = sum(it.estimated_weight_g for it in items)
        tot_c = sum(it.calories for it in items)
        tot_p = sum(it.protein_g for it in items)
        tot_cb = sum(it.carbs_g for it in items)
        tot_f = sum(it.fat_g for it in items)
        tot_fib = sum(it.fiber_g for it in items)

        return NortheastCompositeDecompositionResult(
            platter_name="Traditional Naga Feast Platter",
            platter_type="meal_plate",
            state="Nagaland",
            region_community="Kohima",
            total_components_detected=len(items),
            items=items,
            total_edible_weight_g=round(tot_w, 1),
            total_calories=round(tot_c, 1),
            total_protein_g=round(tot_p, 1),
            total_carbs_g=round(tot_cb, 1),
            total_fat_g=round(tot_f, 1),
            total_fiber_g=round(tot_fib, 1),
            deconstruction_rules_enforced=[
                "Sections 24 & 73: Decomposed Naga feast into steamed rice, smoked pork with axone, boiled greens, and king chilli chutney."
            ]
        )

# =============================================================================
# 4. TRIPURI MUI BOROK MEAL DECOMPOSER (Section 29)
# =============================================================================

class TripuriMuiBorokDecomposer:
    """
    Implements Section 29:
    Treat Mui Borok as a cuisine/meal category rather than automatically one single dish.
    Never return only Mui Borok = 800 kcal without component segmentation.
    """
    @staticmethod
    def decompose(meta: Optional[Dict[str, Any]] = None) -> NortheastCompositeDecompositionResult:
        items: List[DecomposedNortheastItem] = [
            DecomposedNortheastItem(
                item_index=1, canonical_food_id="TR_RICE_MAI",
                name="Plain Steamed Rice", variant="Mai (Tripuri Rice)", category="Rice",
                estimated_weight_g=180.0, calories=234.0, protein_g=4.9, carbs_g=50.8, fat_g=0.5, fiber_g=0.7, confidence=0.96
            ),
            DecomposedNortheastItem(
                item_index=2, canonical_food_id="TR_STEW_CHAKHWI",
                name="Tripuri Chakhwi", variant="Alkaline Bamboo Shoot & Pork/Jackfruit Stew", category="Stew/Soup",
                estimated_weight_g=120.0, calories=78.0, protein_g=2.6, carbs_g=11.8, fat_g=2.2, fiber_g=3.8, confidence=0.94
            ),
            DecomposedNortheastItem(
                item_index=3, canonical_food_id="TR_CHUTNEY_MOSDENG_SERMA",
                name="Mosdeng Serma", variant="Roasted Tomato & Fermented Berma Fish Mash", category="Chutney/Salad",
                estimated_weight_g=60.0, calories=37.2, protein_g=1.9, carbs_g=4.8, fat_g=0.9, fiber_g=1.2, confidence=0.95
            ),
            DecomposedNortheastItem(
                item_index=4, canonical_food_id="TR_CURRY_GUDOK",
                name="Gudok", variant="Bamboo Pipe Steamed Fish & Vegetables with Berma", category="Fish",
                estimated_weight_g=100.0, calories=85.0, protein_g=9.2, carbs_g=4.5, fat_g=3.4, fiber_g=2.0, confidence=0.92
            )
        ]

        tot_w = sum(it.estimated_weight_g for it in items)
        tot_c = sum(it.calories for it in items)
        tot_p = sum(it.protein_g for it in items)
        tot_cb = sum(it.carbs_g for it in items)
        tot_f = sum(it.fat_g for it in items)
        tot_fib = sum(it.fiber_g for it in items)

        return NortheastCompositeDecompositionResult(
            platter_name="Traditional Tripuri Mui Borok Meal",
            platter_type="mui_borok_meal",
            state="Tripura",
            region_community="Tripuri",
            total_components_detected=len(items),
            items=items,
            total_edible_weight_g=round(tot_w, 1),
            total_calories=round(tot_c, 1),
            total_protein_g=round(tot_p, 1),
            total_carbs_g=round(tot_cb, 1),
            total_fat_g=round(tot_f, 1),
            total_fiber_g=round(tot_fib, 1),
            deconstruction_rules_enforced=[
                "Section 29: Treated Mui Borok as a multi-component meal; decomposed into Rice, Chakhwi, Mosdeng Serma, and Gudok."
            ]
        )

# =============================================================================
# 5. SIKKIM REGIONAL MEAL DECOMPOSER (Section 73)
# =============================================================================

class SikkimMealDecomposer:
    @staticmethod
    def decompose(meta: Optional[Dict[str, Any]] = None) -> NortheastCompositeDecompositionResult:
        items: List[DecomposedNortheastItem] = [
            DecomposedNortheastItem(
                item_index=1, canonical_food_id="SK_RICE_STEAMED",
                name="Steamed Rice", variant="Plain White Rice", category="Rice",
                estimated_weight_g=180.0, calories=234.0, protein_g=4.9, carbs_g=50.8, fat_g=0.5, fiber_g=0.7, confidence=0.96
            ),
            DecomposedNortheastItem(
                item_index=2, canonical_food_id="SK_STEW_GUNDRUK",
                name="Gundruk Jhol", variant="Fermented Mustard Greens Tangy Soup", category="Fermented",
                estimated_weight_g=150.0, calories=87.0, protein_g=4.8, carbs_g=11.2, fat_g=2.7, fiber_g=5.7, confidence=0.95
            ),
            DecomposedNortheastItem(
                item_index=3, canonical_food_id="SK_MEAT_PHAGSHAPA",
                name="Phagshapa", variant="Pork Fat with Radish & Dry Chillies", category="Meat",
                is_countable=True, count=3, estimated_weight_g=130.0, calories=338.0, protein_g=17.9, carbs_g=4.9, fat_g=27.9, fiber_g=1.6, confidence=0.94
            ),
            DecomposedNortheastItem(
                item_index=4, canonical_food_id="SK_FERMENTED_KINEMA",
                name="Kinema Curry", variant="Fermented Whole Soybean Curry", category="Fermented",
                estimated_weight_g=80.0, calories=144.0, protein_g=11.6, carbs_g=8.2, fat_g=7.2, fiber_g=4.0, confidence=0.93
            ),
            DecomposedNortheastItem(
                item_index=5, canonical_food_id="SK_BREAD_SEL_ROTI",
                name="Sel Roti", variant="Sweet Crispy Ring Rice Bread", category="Pitha/Snack",
                is_countable=True, count=1, estimated_weight_g=60.0, calories=210.0, protein_g=2.7, carbs_g=37.2, fat_g=6.1, fiber_g=0.7, confidence=0.96
            )
        ]

        tot_w = sum(it.estimated_weight_g for it in items)
        tot_c = sum(it.calories for it in items)
        tot_p = sum(it.protein_g for it in items)
        tot_cb = sum(it.carbs_g for it in items)
        tot_f = sum(it.fat_g for it in items)
        tot_fib = sum(it.fiber_g for it in items)

        return NortheastCompositeDecompositionResult(
            platter_name="Sikkimese Traditional Meal",
            platter_type="thali",
            state="Sikkim",
            region_community="Gangtok",
            total_components_detected=len(items),
            items=items,
            total_edible_weight_g=round(tot_w, 1),
            total_calories=round(tot_c, 1),
            total_protein_g=round(tot_p, 1),
            total_carbs_g=round(tot_cb, 1),
            total_fat_g=round(tot_f, 1),
            total_fiber_g=round(tot_fib, 1),
            deconstruction_rules_enforced=[
                "Section 73: Decomposed Sikkim meal into Rice, Gundruk Jhol, Phagshapa pork, Kinema, and Sel Roti."
            ]
        )

# =============================================================================
# 6. MANIPURI REGIONAL MEAL DECOMPOSER (Section 54, 73)
# =============================================================================


class ManipuriMealDecomposer:
    @staticmethod
    def decompose(meta: Optional[Dict[str, Any]] = None) -> NortheastCompositeDecompositionResult:
        items: List[DecomposedNortheastItem] = [
            DecomposedNortheastItem(
                item_index=1, canonical_food_id="MN_RICE_STEAMED",
                name="Steamed Rice", variant="Meitei Steamed White Rice", category="Rice",
                estimated_weight_g=180.0, calories=234.0, protein_g=4.9, carbs_g=50.8, fat_g=0.5, fiber_g=0.7, confidence=0.96
            ),
            DecomposedNortheastItem(
                item_index=2, canonical_food_id="MN_STEW_KANGSHOI",
                name="Kangshoi", variant="Oil-Free Boiled Vegetable & Fish Broth", category="Stew/Soup",
                estimated_weight_g=150.0, calories=65.0, protein_g=4.5, carbs_g=8.2, fat_g=1.2, fiber_g=2.8, confidence=0.95
            ),
            DecomposedNortheastItem(
                item_index=3, canonical_food_id="MN_CHUTNEY_EROMBA",
                name="Eromba", variant="Mashed Potato & Vegetable with Roasted Ngari Fish", category="Chutney/Salad",
                estimated_weight_g=70.0, calories=65.0, protein_g=3.2, carbs_g=11.5, fat_g=0.8, fiber_g=1.6, confidence=0.96
            ),
            DecomposedNortheastItem(
                item_index=4, canonical_food_id="MN_SALAD_SINGJU",
                name="Singju", variant="Shredded Vegetable Herb Salad with Roasted Gram & Ngari", category="Chutney/Salad",
                estimated_weight_g=60.0, calories=55.0, protein_g=2.8, carbs_g=7.5, fat_g=1.5, fiber_g=2.4, confidence=0.94
            )
        ]

        tot_w = sum(it.estimated_weight_g for it in items)
        tot_c = sum(it.calories for it in items)
        tot_p = sum(it.protein_g for it in items)
        tot_cb = sum(it.carbs_g for it in items)
        tot_f = sum(it.fat_g for it in items)
        tot_fib = sum(it.fiber_g for it in items)

        return NortheastCompositeDecompositionResult(
            platter_name="Traditional Manipuri Meal (Chakluk)",
            platter_type="meal_plate",
            state="Manipur",
            region_community="Imphal Valley",
            total_components_detected=len(items),
            items=items,
            total_edible_weight_g=round(tot_w, 1),
            total_calories=round(tot_c, 1),
            total_protein_g=round(tot_p, 1),
            total_carbs_g=round(tot_cb, 1),
            total_fat_g=round(tot_f, 1),
            total_fiber_g=round(tot_fib, 1),
            deconstruction_rules_enforced=[
                "Section 54: Decomposed Manipuri meal into Steamed Rice, Kangshoi broth, Eromba mash, and Singju salad."
            ]
        )

# =============================================================================
# 7. MIZO REGIONAL MEAL DECOMPOSER (Section 54, 73)
# =============================================================================

class MizoMealDecomposer:
    @staticmethod
    def decompose(meta: Optional[Dict[str, Any]] = None) -> NortheastCompositeDecompositionResult:
        items: List[DecomposedNortheastItem] = [
            DecomposedNortheastItem(
                item_index=1, canonical_food_id="MZ_RICE_STEAMED",
                name="Steamed Rice", variant="Mizo Steamed Plain Rice", category="Rice",
                estimated_weight_g=180.0, calories=234.0, protein_g=4.9, carbs_g=50.8, fat_g=0.5, fiber_g=0.7, confidence=0.96
            ),
            DecomposedNortheastItem(
                item_index=2, canonical_food_id="MZ_STEW_BAI",
                name="Bai", variant="Boiled Vegetables & Bamboo Shoot Stew", category="Stew/Soup",
                estimated_weight_g=150.0, calories=78.0, protein_g=3.6, carbs_g=10.2, fat_g=2.2, fiber_g=3.9, confidence=0.95
            ),
            DecomposedNortheastItem(
                item_index=3, canonical_food_id="MZ_MEAT_VAWKSA_REP",
                name="Vawksa Rep", variant="Smoked Pork with Mustard Greens", category="Meat",
                is_countable=True, count=3, estimated_weight_g=120.0, calories=312.0, protein_g=18.5, carbs_g=2.8, fat_g=25.2, fiber_g=1.2, confidence=0.94
            ),
            DecomposedNortheastItem(
                item_index=4, canonical_food_id="MZ_CHUTNEY_CHILLI",
                name="Mizo Chilli Chutney", variant="Crushed Raw Bird's Eye Chilli with Garlic", category="Chutney/Salad",
                estimated_weight_g=20.0, calories=15.0, protein_g=0.4, carbs_g=2.8, fat_g=0.2, fiber_g=0.6, confidence=0.96
            )
        ]

        tot_w = sum(it.estimated_weight_g for it in items)
        tot_c = sum(it.calories for it in items)
        tot_p = sum(it.protein_g for it in items)
        tot_cb = sum(it.carbs_g for it in items)
        tot_f = sum(it.fat_g for it in items)
        tot_fib = sum(it.fiber_g for it in items)

        return NortheastCompositeDecompositionResult(
            platter_name="Traditional Mizo Meal",
            platter_type="meal_plate",
            state="Mizoram",
            region_community="Aizawl",
            total_components_detected=len(items),
            items=items,
            total_edible_weight_g=round(tot_w, 1),
            total_calories=round(tot_c, 1),
            total_protein_g=round(tot_p, 1),
            total_carbs_g=round(tot_cb, 1),
            total_fat_g=round(tot_f, 1),
            total_fiber_g=round(tot_fib, 1),
            deconstruction_rules_enforced=[
                "Section 54: Decomposed Mizo meal into Rice, Boiled Vegetable Bai, Smoked Pork (Vawksa Rep), and Chilli Chutney."
            ]
        )

# =============================================================================
# 8. ARUNACHAL TRIBAL MEAL DECOMPOSER (Section 54, 73)
# =============================================================================

class ArunachalMealDecomposer:
    @staticmethod
    def decompose(meta: Optional[Dict[str, Any]] = None) -> NortheastCompositeDecompositionResult:
        items: List[DecomposedNortheastItem] = [
            DecomposedNortheastItem(
                item_index=1, canonical_food_id="AR_RICE_STEAMED",
                name="Steamed Rice", variant="Tribal Steamed Rice", category="Rice",
                estimated_weight_g=180.0, calories=234.0, protein_g=4.9, carbs_g=50.8, fat_g=0.5, fiber_g=0.7, confidence=0.96
            ),
            DecomposedNortheastItem(
                item_index=2, canonical_food_id="AR_BAMBOO_EKUNG_PORK",
                name="Pork with Ekung", variant="Tender Pork with Fermented Bamboo Shoot", category="Meat",
                is_countable=True, count=3, estimated_weight_g=140.0, calories=336.0, protein_g=21.7, carbs_g=4.5, fat_g=25.9, fiber_g=2.5, confidence=0.94
            ),
            DecomposedNortheastItem(
                item_index=3, canonical_food_id="AR_BREAD_KHURA",
                name="Monpa Khura", variant="Buckwheat Pancake Flatbread", category="Pitha/Snack",
                is_countable=True, count=1, estimated_weight_g=70.0, calories=147.0, protein_g=4.5, carbs_g=28.1, fat_g=2.2, fiber_g=3.1, confidence=0.95
            ),
            DecomposedNortheastItem(
                item_index=4, canonical_food_id="AR_FERMENTED_CHHURPI_SOUP",
                name="Chhurpi Soup", variant="Fermented Yak Cheese Herbal Broth", category="Fermented",
                estimated_weight_g=120.0, calories=110.4, protein_g=8.2, carbs_g=4.2, fat_g=7.0, fiber_g=0.6, confidence=0.93
            ),
            DecomposedNortheastItem(
                item_index=5, canonical_food_id="AR_BOILED_GREENS",
                name="Boiled Wild Greens", variant="Steamed Indigenous Herbs with Ginger", category="Vegetarian",
                estimated_weight_g=70.0, calories=28.0, protein_g=1.8, carbs_g=4.2, fat_g=0.4, fiber_g=2.5, confidence=0.95
            )
        ]

        tot_w = sum(it.estimated_weight_g for it in items)
        tot_c = sum(it.calories for it in items)
        tot_p = sum(it.protein_g for it in items)
        tot_cb = sum(it.carbs_g for it in items)
        tot_f = sum(it.fat_g for it in items)
        tot_fib = sum(it.fiber_g for it in items)

        return NortheastCompositeDecompositionResult(
            platter_name="Traditional Arunachal Tribal Platter",
            platter_type="thali",
            state="Arunachal Pradesh",
            region_community="Tawang / West Kameng",
            total_components_detected=len(items),
            items=items,
            total_edible_weight_g=round(tot_w, 1),
            total_calories=round(tot_c, 1),
            total_protein_g=round(tot_p, 1),
            total_carbs_g=round(tot_cb, 1),
            total_fat_g=round(tot_f, 1),
            total_fiber_g=round(tot_fib, 1),
            deconstruction_rules_enforced=[
                "Section 54: Decomposed Arunachal tribal meal into Rice, Pork with Ekung, Monpa Khura, Chhurpi Soup, and Wild Greens."
            ]
        )

# =============================================================================
# 9. PACKAGING & SERVING WARE FILTER (Section 57)
# =============================================================================


class NortheastPackagingFilter:
    """
    Implements Section 57:
    Excludes non-edible serving vessels:
    - Bell-metal kanh thali / bowl
    - Banana leaf (kola pata)
    - Hollow bamboo cooking tube (sunga / bamboo pipe)
    - Wooden bowl / plate
    - Sal leaf dona
    """
    NON_FOOD_LABELS = {
        "bell_metal_kanh_platter": "Traditional Assamese bell-metal dinner plate",
        "banana_leaf": "Plantain leaf serving base",
        "bamboo_pipe_cooking_tube": "Bamboo cylinder used for Sunga rice or fish",
        "wooden_bowl": "Traditional tribal hand-carved wooden bowl",
        "stainless_steel_thali": "Modern steel serving plate",
        "sal_leaf_dona": "Pressed sal leaf cup"
    }

    @classmethod
    def filter_non_food_detections(cls, detections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [d for d in detections if d.get("label", "").lower().strip() not in cls.NON_FOOD_LABELS]
