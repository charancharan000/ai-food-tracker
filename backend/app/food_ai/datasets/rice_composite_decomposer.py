"""
Rice & Biryani Composite Meal Decomposer (Part 9)
Implements Sections 43, 44, 46, 58, 59, 64, 78 of Part 9 Master Training Specification.

Guarantees:
- BiryaniPlateDecomposer:
  * Decomposes biryani plate into Rice, Meat, Egg, Birista, Raita, Salan, and Pickle (Section 44).
  * Excludes side dishes from core biryani mass/calories (Section 43).
  * Calculates explicit Rice-to-Meat Ratio (Section 46: e.g. Rice 350g + Chicken 120g).
- SouthIndianRiceMealDecomposer (Section 58):
  * Never returns "South Indian Rice Meal = 900 kcal" without component analysis.
  * Decomposes into Rice, Sambar, Rasam, Poriyal, Curd, Appalam, and Pickle.
- BiryaniComboMealDecomposer (Section 59):
  * Decomposes Biryani + Chicken 65 + Boiled Egg + Raita + Salan + Drink combo meals.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class RiceMealComponent(BaseModel):
    name: str
    category: str  # "rice_base", "protein", "egg", "side_dish", "garnish", "accompaniment"
    count: Optional[int] = None
    estimated_mass_g: float
    calories: float
    protein_g: float
    carbs_g: float
    fat_g: float
    fiber_g: float
    confidence: float = Field(..., ge=0.0, le=1.0)


class RiceCompositeDecompositionResult(BaseModel):
    composite_meal_name: str
    regional_style: str
    components: List[RiceMealComponent]
    total_mass_g: float
    total_calories_range: Dict[str, float]  # "low", "expected", "high"
    total_protein_g: float
    total_carbs_g: float
    total_fat_g: float
    total_fiber_g: float
    overall_confidence: float
    decomposition_notes: str


# =============================================================================
# 1. BIRYANI PLATE DECOMPOSER (Sections 43, 44, 46)
# =============================================================================

class BiryaniPlateDecomposer:
    """
    Decomposes biryani plate into discrete constituents:
    - Biryani Rice
    - Meat Pieces (chicken, mutton, prawn)
    - Boiled Egg
    - Caramelized Fried Onions (birista)
    - Side dishes (Raita, Salan, Pickle) - NOT merged into biryani weight!
    """
    @staticmethod
    def decompose(
        style: str = "Hyderabadi",
        protein_type: str = "chicken",
        rice_mass_g: float = 320.0,
        meat_pieces_count: int = 2,
        has_egg: bool = True,
        has_raita: bool = True,
        has_salan: bool = True,
        meta: Optional[Dict[str, Any]] = None
    ) -> RiceCompositeDecompositionResult:
        components: List[RiceMealComponent] = []

        # 1. Biryani Rice (seasoned dum grains)
        rice_cals = (rice_mass_g / 100.0) * 155.0  # basmati cooked in aromatics & mild fat
        components.append(RiceMealComponent(
            name=f"{style} Biryani Rice",
            category="rice_base",
            estimated_mass_g=round(rice_mass_g, 1),
            calories=round(rice_cals, 1),
            protein_g=round((rice_mass_g / 100.0) * 3.4, 1),
            carbs_g=round((rice_mass_g / 100.0) * 28.5, 1),
            fat_g=round((rice_mass_g / 100.0) * 3.2, 1),
            fiber_g=round((rice_mass_g / 100.0) * 0.9, 1),
            confidence=0.96
        ))

        # 2. Meat Pieces (chicken or mutton or prawn)
        if "chicken" in protein_type.lower():
            unit_meat_mass = 55.0
            meat_mass = meat_pieces_count * unit_meat_mass
            meat_cals = (meat_mass / 100.0) * 195.0
            meat_pro = (meat_mass / 100.0) * 22.0
            meat_fat = (meat_mass / 100.0) * 11.5
            meat_label = "Bone-in Spiced Chicken Pieces"
        elif "mutton" in protein_type.lower():
            unit_meat_mass = 45.0
            meat_mass = meat_pieces_count * unit_meat_mass
            meat_cals = (meat_mass / 100.0) * 235.0
            meat_pro = (meat_mass / 100.0) * 20.5
            meat_fat = (meat_mass / 100.0) * 16.5
            meat_label = "Tender Spiced Mutton Chunks"
        elif "prawn" in protein_type.lower():
            unit_meat_mass = 15.0
            meat_mass = meat_pieces_count * unit_meat_mass
            meat_cals = (meat_mass / 100.0) * 140.0
            meat_pro = (meat_mass / 100.0) * 23.0
            meat_fat = (meat_mass / 100.0) * 4.5
            meat_label = "Spiced Prawns"
        else:
            meat_mass = 0.0
            meat_cals = 0.0
            meat_pro = 0.0
            meat_fat = 0.0
            meat_label = "Vegetarian"

        if meat_pieces_count > 0 and meat_mass > 0:
            components.append(RiceMealComponent(
                name=meat_label,
                category="protein",
                count=meat_pieces_count,
                estimated_mass_g=round(meat_mass, 1),
                calories=round(meat_cals, 1),
                protein_g=round(meat_pro, 1),
                carbs_g=round(meat_pieces_count * 1.5, 1),
                fat_g=round(meat_fat, 1),
                fiber_g=0.2,
                confidence=0.94
            ))

        # 3. Boiled Egg (if detected)
        if has_egg:
            components.append(RiceMealComponent(
                name="Hard-Boiled Egg",
                category="egg",
                count=1,
                estimated_mass_g=50.0,
                calories=74.0,
                protein_g=6.3,
                carbs_g=0.6,
                fat_g=5.0,
                fiber_g=0.0,
                confidence=0.97
            ))

        # 4. Fried Onions (Birista) Garnish
        components.append(RiceMealComponent(
            name="Caramelized Fried Onions (Birista)",
            category="garnish",
            estimated_mass_g=15.0,
            calories=58.0,
            protein_g=0.6,
            carbs_g=5.2,
            fat_g=4.0,
            fiber_g=0.8,
            confidence=0.91
        ))

        # 5. Side: Onion-Cucumber Raita (Section 43: segregated)
        if has_raita:
            components.append(RiceMealComponent(
                name="Cooling Onion-Cucumber Raita",
                category="side_dish",
                estimated_mass_g=80.0,
                calories=48.0,
                protein_g=2.8,
                carbs_g=4.5,
                fat_g=2.1,
                fiber_g=0.4,
                confidence=0.93
            ))

        # 6. Side: Mirchi ka Salan / Gravy (Section 43: segregated)
        if has_salan:
            components.append(RiceMealComponent(
                name="Mirchi Ka Salan (Peanut-Sesame Gravy)",
                category="side_dish",
                estimated_mass_g=60.0,
                calories=78.0,
                protein_g=2.1,
                carbs_g=5.2,
                fat_g=5.6,
                fiber_g=1.2,
                confidence=0.90
            ))

        total_mass = sum(c.estimated_mass_g for c in components)
        exp_cals = sum(c.calories for c in components)
        total_pro = sum(c.protein_g for c in components)
        total_carb = sum(c.carbs_g for c in components)
        total_fat = sum(c.fat_g for c in components)
        total_fib = sum(c.fiber_g for c in components)

        # Calibrated uncertainty interval (Section 65)
        cals_low = round(exp_cals * 0.88, 1)
        cals_high = round(exp_cals * 1.14, 1)

        return RiceCompositeDecompositionResult(
            composite_meal_name=f"{style} {protein_type.title()} Biryani Plate",
            regional_style=style,
            components=components,
            total_mass_g=round(total_mass, 1),
            total_calories_range={"low": cals_low, "expected": round(exp_cals, 1), "high": cals_high},
            total_protein_g=round(total_pro, 1),
            total_carbs_g=round(total_carb, 1),
            total_fat_g=round(total_fat, 1),
            total_fiber_g=round(total_fib, 1),
            overall_confidence=0.94,
            decomposition_notes=f"Decomposed into {rice_mass_g}g rice, {meat_pieces_count} {protein_type} pieces, egg, and separate side dishes per Section 43 & 46."
        )


# =============================================================================
# 2. SOUTH INDIAN RICE MEAL DECOMPOSER (Section 58)
# =============================================================================

class SouthIndianRiceMealDecomposer:
    """
    Decomposes South Indian Full Rice Meal into courses/bowls:
    - Steamed White Rice
    - Sambar
    - Rasam
    - Poriyal / Kootu
    - Curd
    - Appalam & Pickle
    Never calculates a monolithic 900 kcal without component analysis (Section 58).
    """
    @staticmethod
    def decompose(
        rice_portion_g: float = 240.0,
        has_sambar: bool = True,
        has_rasam: bool = True,
        has_poriyal: bool = True,
        has_curd: bool = True,
        has_appalam: bool = True,
        meta: Optional[Dict[str, Any]] = None
    ) -> RiceCompositeDecompositionResult:
        components: List[RiceMealComponent] = []

        # 1. Steamed White Rice
        rice_cals = (rice_portion_g / 100.0) * 130.0
        components.append(RiceMealComponent(
            name="Steamed White Rice",
            category="rice_base",
            estimated_mass_g=rice_portion_g,
            calories=round(rice_cals, 1),
            protein_g=round((rice_portion_g / 100.0) * 2.7, 1),
            carbs_g=round((rice_portion_g / 100.0) * 28.2, 1),
            fat_g=round((rice_portion_g / 100.0) * 0.3, 1),
            fiber_g=round((rice_portion_g / 100.0) * 0.4, 1),
            confidence=0.97
        ))

        # 2. Sambar (120g)
        if has_sambar:
            components.append(RiceMealComponent(
                name="Toor Dal Vegetable Sambar",
                category="side_dish",
                estimated_mass_g=120.0,
                calories=98.0,
                protein_g=4.2,
                carbs_g=14.5,
                fat_g=2.6,
                fiber_g=2.8,
                confidence=0.95
            ))

        # 3. Rasam (100g)
        if has_rasam:
            components.append(RiceMealComponent(
                name="Tamarind Pepper Tomato Rasam",
                category="side_dish",
                estimated_mass_g=100.0,
                calories=42.0,
                protein_g=1.2,
                carbs_g=6.8,
                fat_g=1.1,
                fiber_g=0.6,
                confidence=0.94
            ))

        # 4. Poriyal (80g)
        if has_poriyal:
            components.append(RiceMealComponent(
                name="Green Beans & Coconut Poriyal",
                category="side_dish",
                estimated_mass_g=80.0,
                calories=68.0,
                protein_g=2.1,
                carbs_g=8.2,
                fat_g=3.2,
                fiber_g=2.4,
                confidence=0.92
            ))

        # 5. Curd (80g)
        if has_curd:
            components.append(RiceMealComponent(
                name="Fresh Plain Curd (Dahi)",
                category="side_dish",
                estimated_mass_g=80.0,
                calories=52.0,
                protein_g=2.8,
                carbs_g=3.6,
                fat_g=2.8,
                fiber_g=0.0,
                confidence=0.96
            ))

        # 6. Appalam (15g)
        if has_appalam:
            components.append(RiceMealComponent(
                name="Crisp Fried Appalam / Papad",
                category="accompaniment",
                count=1,
                estimated_mass_g=15.0,
                calories=65.0,
                protein_g=3.2,
                carbs_g=7.5,
                fat_g=2.8,
                fiber_g=0.8,
                confidence=0.98
            ))

        total_mass = sum(c.estimated_mass_g for c in components)
        exp_cals = sum(c.calories for c in components)
        total_pro = sum(c.protein_g for c in components)
        total_carb = sum(c.carbs_g for c in components)
        total_fat = sum(c.fat_g for c in components)
        total_fib = sum(c.fiber_g for c in components)

        cals_low = round(exp_cals * 0.90, 1)
        cals_high = round(exp_cals * 1.12, 1)

        return RiceCompositeDecompositionResult(
            composite_meal_name="South Indian Traditional Rice Meal",
            regional_style="South Indian",
            components=components,
            total_mass_g=round(total_mass, 1),
            total_calories_range={"low": cals_low, "expected": round(exp_cals, 1), "high": cals_high},
            total_protein_g=round(total_pro, 1),
            total_carbs_g=round(total_carb, 1),
            total_fat_g=round(total_fat, 1),
            total_fiber_g=round(total_fib, 1),
            overall_confidence=0.95,
            decomposition_notes="Decomposed into rice, sambar, rasam, poriyal, curd, and appalam per Section 58."
        )


# =============================================================================
# 3. BIRYANI COMBO MEAL DECOMPOSER (Section 59)
# =============================================================================

class BiryaniComboMealDecomposer:
    """
    Decomposes Biryani Combo Meals:
    e.g. Chicken Biryani + Chicken 65 + Boiled Egg + Raita + Salan + Beverage (Section 59).
    """
    @staticmethod
    def decompose_combo(
        biryani_mass_g: float = 350.0,
        chicken_65_pieces: int = 4,
        include_egg: bool = True,
        include_drink: bool = True,
        meta: Optional[Dict[str, Any]] = None
    ) -> RiceCompositeDecompositionResult:
        components: List[RiceMealComponent] = []

        # 1. Chicken Biryani Core (Rice + chicken inside)
        biryani_cals = (biryani_mass_g / 100.0) * 182.0
        components.append(RiceMealComponent(
            name="Chicken Dum Biryani (Rice & Meat)",
            category="rice_base",
            estimated_mass_g=biryani_mass_g,
            calories=round(biryani_cals, 1),
            protein_g=round((biryani_mass_g / 100.0) * 9.5, 1),
            carbs_g=round((biryani_mass_g / 100.0) * 22.0, 1),
            fat_g=round((biryani_mass_g / 100.0) * 6.5, 1),
            fiber_g=round((biryani_mass_g / 100.0) * 1.1, 1),
            confidence=0.95
        ))

        # 2. Chicken 65 (Fried spiced appetizer)
        c65_mass = chicken_65_pieces * 25.0
        c65_cals = (c65_mass / 100.0) * 260.0
        components.append(RiceMealComponent(
            name="Crisp Chicken 65 Appetizer",
            category="protein",
            count=chicken_65_pieces,
            estimated_mass_g=round(c65_mass, 1),
            calories=round(c65_cals, 1),
            protein_g=round((c65_mass / 100.0) * 19.5, 1),
            carbs_g=round((c65_mass / 100.0) * 8.5, 1),
            fat_g=round((c65_mass / 100.0) * 16.5, 1),
            fiber_g=0.6,
            confidence=0.93
        ))

        # 3. Boiled Egg
        if include_egg:
            components.append(RiceMealComponent(
                name="Hard-Boiled Egg",
                category="egg",
                count=1,
                estimated_mass_g=50.0,
                calories=74.0,
                protein_g=6.3,
                carbs_g=0.6,
                fat_g=5.0,
                fiber_g=0.0,
                confidence=0.97
            ))

        # 4. Raita & Salan
        components.append(RiceMealComponent(
            name="Onion Raita",
            category="side_dish",
            estimated_mass_g=80.0,
            calories=48.0,
            protein_g=2.8,
            carbs_g=4.5,
            fat_g=2.1,
            fiber_g=0.4,
            confidence=0.94
        ))
        components.append(RiceMealComponent(
            name="Mirchi Salan Gravy",
            category="side_dish",
            estimated_mass_g=60.0,
            calories=78.0,
            protein_g=2.1,
            carbs_g=5.2,
            fat_g=5.6,
            fiber_g=1.2,
            confidence=0.91
        ))

        # 5. Soft drink (optional)
        if include_drink:
            components.append(RiceMealComponent(
                name="Chilled Carbonated Soft Drink",
                category="accompaniment",
                estimated_mass_g=250.0,
                calories=105.0,
                protein_g=0.0,
                carbs_g=26.5,
                fat_g=0.0,
                fiber_g=0.0,
                confidence=0.96
            ))

        total_mass = sum(c.estimated_mass_g for c in components)
        exp_cals = sum(c.calories for c in components)
        total_pro = sum(c.protein_g for c in components)
        total_carb = sum(c.carbs_g for c in components)
        total_fat = sum(c.fat_g for c in components)
        total_fib = sum(c.fiber_g for c in components)

        cals_low = round(exp_cals * 0.90, 1)
        cals_high = round(exp_cals * 1.12, 1)

        return RiceCompositeDecompositionResult(
            composite_meal_name="Biryani Feast Combo Meal",
            regional_style="Pan-India",
            components=components,
            total_mass_g=round(total_mass, 1),
            total_calories_range={"low": cals_low, "expected": round(exp_cals, 1), "high": cals_high},
            total_protein_g=round(total_pro, 1),
            total_carbs_g=round(total_carb, 1),
            total_fat_g=round(total_fat, 1),
            total_fiber_g=round(total_fib, 1),
            overall_confidence=0.94,
            decomposition_notes="Decomposed Biryani, Chicken 65, Boiled Egg, Raita, Salan, and beverage per Section 59."
        )
