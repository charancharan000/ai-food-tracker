"""
Indian Dal, Curry & Gravy Composite Meal Decomposer (Part 11)
Implements Sections 39, 40, and 67 of Part 11 Master Training Specification.

Guarantees:
- Component-level decomposition for Indian Curry meals:
  * Curry + Rice combinations (Section 39):
    Never treats Steamed Rice + Sambar/Dal/Chicken Curry as a monolithic dish.
    Itemizes rice staple and curries separately with discrete portion mass & calories.
  * Curry + Bread combinations (Section 40):
    Itemizes bread counts (Chapati, Naan, Parotta, Puri) and curry portions separately.
  * Banana Leaf / Full Thali Feast deconstruction (Section 67):
    Itemizes Central Rice, Sambar, Rasam, Kootu, Poriyal, Curd, Papad, Pickle, and optional
    non-veg curry. Strictly prohibits monolithic 900 kcal estimate.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class CurryMealComponent(BaseModel):
    name: str
    item_name: str = ""
    category: str  # "grain_staple", "bread_staple", "curry_gravy", "protein_chunk", "dry_vegetable", "condiment", "accompaniment"
    count: Optional[int] = None
    weight_g: float
    calories: float
    protein_g: float
    carbs_g: float
    fat_g: float
    fiber_g: float
    confidence: float = Field(..., ge=0.0, le=1.0)

    def model_post_init(self, __context: Any) -> None:
        if not self.item_name:
            self.item_name = self.name


class CurryCompositeDecompositionResult(BaseModel):
    composite_meal_name: str
    plate_type: str = ""
    regional_style: str
    components: List[CurryMealComponent]
    total_weight_g: float
    total_calories_range: Dict[str, float]  # "low", "expected", "high"
    total_protein_g: float
    total_carbs_g: float
    total_fat_g: float
    total_fiber_g: float
    overall_confidence: float
    decomposition_notes: str

    def model_post_init(self, __context: Any) -> None:
        if not self.plate_type:
            self.plate_type = self.composite_meal_name


class CurryRiceDecomposer:
    """
    Deconstructs Rice + Curry combinations (Section 39).
    Enforces independent itemization of rice and gravies.
    """
    @classmethod
    def decompose(
        cls,
        rice_type: str = "Steamed Sona Masoori Rice",
        rice_grams: float = 200.0,
        curry_name: str = "Yellow Dal Tadka",
        curry_grams: float = 160.0,
        accompaniments: Optional[List[Dict[str, Any]]] = None
    ) -> CurryCompositeDecompositionResult:
        components: List[CurryMealComponent] = []

        # 1. Rice Staple (typical steamed white rice: ~130 kcal / 100g, 2.7g P, 28g C, 0.3g F, 0.4g Fib)
        rice_cals = round((rice_grams / 100.0) * 130.0, 1)
        rice_p = round((rice_grams / 100.0) * 2.7, 1)
        rice_c = round((rice_grams / 100.0) * 28.2, 1)
        rice_f = round((rice_grams / 100.0) * 0.3, 1)
        rice_fib = round((rice_grams / 100.0) * 0.4, 1)

        components.append(CurryMealComponent(
            name=rice_type,
            category="grain_staple",
            weight_g=rice_grams,
            calories=rice_cals,
            protein_g=rice_p,
            carbs_g=rice_c,
            fat_g=rice_f,
            fiber_g=rice_fib,
            confidence=0.94
        ))

        # 2. Curry / Gravy
        cname = curry_name.lower()
        if "sambar" in cname:
            # Sambar: ~65 kcal / 100g, 2.6g P, 9.8g C, 1.8g F, 2.2g Fib
            c_cals = round((curry_grams / 100.0) * 65.0, 1)
            c_p = round((curry_grams / 100.0) * 2.6, 1)
            c_c = round((curry_grams / 100.0) * 9.8, 1)
            c_f = round((curry_grams / 100.0) * 1.8, 1)
            c_fib = round((curry_grams / 100.0) * 2.2, 1)
        elif "chicken" in cname:
            # Chicken curry: ~145 kcal / 100g, 12.5g P, 4.0g C, 8.5g F, 1.0g Fib
            c_cals = round((curry_grams / 100.0) * 145.0, 1)
            c_p = round((curry_grams / 100.0) * 12.5, 1)
            c_c = round((curry_grams / 100.0) * 4.0, 1)
            c_f = round((curry_grams / 100.0) * 8.5, 1)
            c_fib = round((curry_grams / 100.0) * 1.0, 1)
        elif "fish" in cname:
            # Fish curry: ~115 kcal / 100g, 11.0g P, 3.5g C, 6.2g F, 0.8g Fib
            c_cals = round((curry_grams / 100.0) * 115.0, 1)
            c_p = round((curry_grams / 100.0) * 11.0, 1)
            c_c = round((curry_grams / 100.0) * 3.5, 1)
            c_f = round((curry_grams / 100.0) * 6.2, 1)
            c_fib = round((curry_grams / 100.0) * 0.8, 1)
        elif "rasam" in cname:
            # Rasam: ~35 kcal / 100g, 1.1g P, 4.5g C, 1.4g F, 0.8g Fib
            c_cals = round((curry_grams / 100.0) * 35.0, 1)
            c_p = round((curry_grams / 100.0) * 1.1, 1)
            c_c = round((curry_grams / 100.0) * 4.5, 1)
            c_f = round((curry_grams / 100.0) * 1.4, 1)
            c_fib = round((curry_grams / 100.0) * 0.8, 1)
        else:
            # Yellow Dal Tadka default: ~105 kcal / 100g, 5.2g P, 13.5g C, 3.6g F, 2.8g Fib
            c_cals = round((curry_grams / 100.0) * 105.0, 1)
            c_p = round((curry_grams / 100.0) * 5.2, 1)
            c_c = round((curry_grams / 100.0) * 13.5, 1)
            c_f = round((curry_grams / 100.0) * 3.6, 1)
            c_fib = round((curry_grams / 100.0) * 2.8, 1)

        components.append(CurryMealComponent(
            name=curry_name,
            category="curry_gravy",
            weight_g=curry_grams,
            calories=c_cals,
            protein_g=c_p,
            carbs_g=c_c,
            fat_g=c_f,
            fiber_g=c_fib,
            confidence=0.91
        ))

        # 3. Optional Accompaniments
        if accompaniments:
            for acc in accompaniments:
                components.append(CurryMealComponent(
                    name=acc.get("name", "Accompaniment"),
                    category=acc.get("category", "accompaniment"),
                    weight_g=acc.get("weight_g", 30.0),
                    calories=acc.get("calories", 40.0),
                    protein_g=acc.get("protein_g", 1.0),
                    carbs_g=acc.get("carbs_g", 5.0),
                    fat_g=acc.get("fat_g", 1.5),
                    fiber_g=acc.get("fiber_g", 0.5),
                    confidence=acc.get("confidence", 0.85)
                ))

        total_weight = sum(c.weight_g for c in components)
        total_cals = sum(c.calories for c in components)
        total_p = sum(c.protein_g for c in components)
        total_c = sum(c.carbs_g for c in components)
        total_f = sum(c.fat_g for c in components)
        total_fib = sum(c.fiber_g for c in components)

        return CurryCompositeDecompositionResult(
            composite_meal_name=f"{rice_type} + {curry_name}",
            regional_style="Pan-Indian / South Indian Rice Meal",
            components=components,
            total_weight_g=round(total_weight, 1),
            total_calories_range={
                "low": round(total_cals * 0.88, 1),
                "expected": round(total_cals, 1),
                "high": round(total_cals * 1.15, 1)
            },
            total_protein_g=round(total_p, 1),
            total_carbs_g=round(total_c, 1),
            total_fat_g=round(total_f, 1),
            total_fiber_g=round(total_fib, 1),
            overall_confidence=0.92,
            decomposition_notes="Deconstructed into discrete rice staple and curry sauce components (Section 39)."
        )


class CurryBreadDecomposer:
    """
    Deconstructs Bread + Curry combinations (Section 40).
    Itemizes flatbreads, gravy, and meat/paneer chunks separately.
    """
    @classmethod
    def decompose(
        cls,
        bread_name: str = "Tandoori Roti",
        bread_count: int = 2,
        bread_piece_weight_g: float = 40.0,
        curry_name: str = "Paneer Butter Masala",
        curry_weight_g: float = 200.0,
        paneer_piece_count: Optional[int] = 5
    ) -> CurryCompositeDecompositionResult:
        components: List[CurryMealComponent] = []

        # 1. Bread component
        bname = bread_name.lower()
        if "naan" in bname:
            unit_cals = 260.0
            unit_p, unit_c, unit_f, unit_fib = 7.5, 45.0, 5.5, 2.0
            weight_per_piece = 90.0
        elif "parotta" in bname:
            unit_cals = 290.0
            unit_p, unit_c, unit_f, unit_fib = 5.2, 42.0, 11.5, 1.8
            weight_per_piece = 85.0
        elif "puri" in bname:
            unit_cals = 125.0
            unit_p, unit_c, unit_f, unit_fib = 2.2, 14.5, 6.5, 1.2
            weight_per_piece = 35.0
        elif "bhatura" in bname:
            unit_cals = 280.0
            unit_p, unit_c, unit_f, unit_fib = 6.0, 38.0, 12.0, 1.5
            weight_per_piece = 85.0
        else:
            # Chapati / Roti
            unit_cals = 104.0
            unit_p, unit_c, unit_f, unit_fib = 3.1, 19.5, 1.6, 2.4
            weight_per_piece = bread_piece_weight_g

        total_bread_weight = weight_per_piece * bread_count
        total_bread_cals = unit_cals * bread_count

        components.append(CurryMealComponent(
            name=f"{bread_name} ({bread_count} pcs)",
            category="bread_staple",
            count=bread_count,
            weight_g=round(total_bread_weight, 1),
            calories=round(total_bread_cals, 1),
            protein_g=round(unit_p * bread_count, 1),
            carbs_g=round(unit_c * bread_count, 1),
            fat_g=round(unit_f * bread_count, 1),
            fiber_g=round(unit_fib * bread_count, 1),
            confidence=0.94
        ))

        # 2. Curry component (split into pieces + sauce if paneer/chicken)
        cname = curry_name.lower()
        if "paneer" in cname and paneer_piece_count:
            piece_weight = paneer_piece_count * 18.0
            gravy_weight = max(curry_weight_g - piece_weight, 60.0)
            
            # Paneer pieces (~265 kcal / 100g, 18.3g P, 1.2g C, 20.8g F)
            p_cals = round((piece_weight / 100.0) * 265.0, 1)
            p_p = round((piece_weight / 100.0) * 18.3, 1)
            p_c = round((piece_weight / 100.0) * 1.2, 1)
            p_f = round((piece_weight / 100.0) * 20.8, 1)

            components.append(CurryMealComponent(
                name=f"Paneer Cubes ({paneer_piece_count} pcs)",
                category="protein_chunk",
                count=paneer_piece_count,
                weight_g=round(piece_weight, 1),
                calories=p_cals,
                protein_g=p_p,
                carbs_g=p_c,
                fat_g=p_f,
                fiber_g=0.0,
                confidence=0.91
            ))

            # Makhani Gravy (~140 kcal / 100g, 2.5g P, 8.5g C, 11.0g F, 1.5g Fib)
            g_cals = round((gravy_weight / 100.0) * 140.0, 1)
            g_p = round((gravy_weight / 100.0) * 2.5, 1)
            g_c = round((gravy_weight / 100.0) * 8.5, 1)
            g_f = round((gravy_weight / 100.0) * 11.0, 1)
            g_fib = round((gravy_weight / 100.0) * 1.5, 1)

            components.append(CurryMealComponent(
                name=f"{curry_name} (Gravy Sauce)",
                category="curry_gravy",
                weight_g=round(gravy_weight, 1),
                calories=g_cals,
                protein_g=g_p,
                carbs_g=g_c,
                fat_g=g_f,
                fiber_g=g_fib,
                confidence=0.90
            ))
        else:
            # Homestyle Dal or Gravy (~110 kcal / 100g)
            c_cals = round((curry_weight_g / 100.0) * 110.0, 1)
            c_p = round((curry_weight_g / 100.0) * 5.0, 1)
            c_c = round((curry_weight_g / 100.0) * 12.0, 1)
            c_f = round((curry_weight_g / 100.0) * 4.5, 1)
            c_fib = round((curry_weight_g / 100.0) * 2.5, 1)

            components.append(CurryMealComponent(
                name=curry_name,
                category="curry_gravy",
                weight_g=round(curry_weight_g, 1),
                calories=c_cals,
                protein_g=c_p,
                carbs_g=c_c,
                fat_g=c_f,
                fiber_g=c_fib,
                confidence=0.92
            ))

        total_weight = sum(c.weight_g for c in components)
        total_cals = sum(c.calories for c in components)
        total_p = sum(c.protein_g for c in components)
        total_c = sum(c.carbs_g for c in components)
        total_f = sum(c.fat_g for c in components)
        total_fib = sum(c.fiber_g for c in components)

        return CurryCompositeDecompositionResult(
            composite_meal_name=f"{bread_name} with {curry_name}",
            regional_style="Pan-Indian Bread + Gravy Combo",
            components=components,
            total_weight_g=round(total_weight, 1),
            total_calories_range={
                "low": round(total_cals * 0.89, 1),
                "expected": round(total_cals, 1),
                "high": round(total_cals * 1.14, 1)
            },
            total_protein_g=round(total_p, 1),
            total_carbs_g=round(total_c, 1),
            total_fat_g=round(total_f, 1),
            total_fiber_g=round(total_fib, 1),
            overall_confidence=0.92,
            decomposition_notes="Deconstructed into discrete bread piece counts and curry gravy/protein mass (Section 40)."
        )


class BananaLeafThaliDecomposer:
    """
    Deconstructs South Indian / Indian Banana Leaf Meals (Section 67).
    Decomposes into:
    - Steamed Rice (central mound)
    - Sambar
    - Rasam
    - Kootu
    - Poriyal
    - Curd
    - Appalam / Papad
    - Pickle
    - Optional Chicken Curry / Fish Curry
    Strict Rule: Never outputs a monolithic single calorie number.
    """
    @classmethod
    def decompose(
        cls,
        leaf_style: str = "South Indian Tamil / Kerala Banana Leaf Meal",
        has_non_veg: bool = False,
        non_veg_dish: Optional[str] = None
    ) -> CurryCompositeDecompositionResult:
        components: List[CurryMealComponent] = [
            # 1. Steamed Rice Mound (220g)
            CurryMealComponent(
                name="Steamed Ponni / Sona Masoori Rice",
                category="grain_staple",
                weight_g=220.0,
                calories=286.0,
                protein_g=5.9,
                carbs_g=62.0,
                fat_g=0.7,
                fiber_g=0.9,
                confidence=0.96
            ),
            # 2. Sambar (120g)
            CurryMealComponent(
                name="Drumstick & Shallot Sambar",
                category="curry_gravy",
                weight_g=120.0,
                calories=78.0,
                protein_g=3.1,
                carbs_g=11.8,
                fat_g=2.2,
                fiber_g=2.6,
                confidence=0.93
            ),
            # 3. Rasam (90g)
            CurryMealComponent(
                name="Tomato Pepper Rasam",
                category="curry_gravy",
                weight_g=90.0,
                calories=31.5,
                protein_g=1.0,
                carbs_g=4.1,
                fat_g=1.3,
                fiber_g=0.7,
                confidence=0.91
            ),
            # 4. Kootu (80g)
            CurryMealComponent(
                name="Chow Chow / Cabbage Kootu",
                category="curry_gravy",
                weight_g=80.0,
                calories=72.0,
                protein_g=2.4,
                carbs_g=8.0,
                fat_g=3.4,
                fiber_g=2.8,
                confidence=0.89
            ),
            # 5. Poriyal / Dry Vegetable (70g)
            CurryMealComponent(
                name="Beans / Carrot Poriyal (with grated coconut)",
                category="dry_vegetable",
                weight_g=70.0,
                calories=56.0,
                protein_g=1.8,
                carbs_g=6.3,
                fat_g=2.7,
                fiber_g=2.9,
                confidence=0.90
            ),
            # 6. Plain Curd / Dahi (80g)
            CurryMealComponent(
                name="Fresh Set Curd / Dahi",
                category="accompaniment",
                weight_g=80.0,
                calories=49.0,
                protein_g=2.5,
                carbs_g=3.5,
                fat_g=2.4,
                fiber_g=0.0,
                confidence=0.95
            ),
            # 7. Appalam / Papad (1 piece, ~12g)
            CurryMealComponent(
                name="Fried Appalam / Papad",
                category="accompaniment",
                count=1,
                weight_g=12.0,
                calories=52.0,
                protein_g=1.5,
                carbs_g=5.5,
                fat_g=2.7,
                fiber_g=0.4,
                confidence=0.95
            ),
            # 8. Mango / Lemon Pickle (15g)
            CurryMealComponent(
                name="Spicy Mango / Lime Pickle",
                category="condiment",
                weight_g=15.0,
                calories=24.0,
                protein_g=0.2,
                carbs_g=1.5,
                fat_g=1.9,
                fiber_g=0.3,
                confidence=0.92
            ),
        ]

        if has_non_veg:
            nv_name = non_veg_dish or "Chettinad Chicken Curry"
            components.append(CurryMealComponent(
                name=nv_name,
                category="curry_gravy",
                weight_g=150.0,
                calories=218.0,
                protein_g=18.5,
                carbs_g=6.0,
                fat_g=13.0,
                fiber_g=1.5,
                confidence=0.91
            ))

        total_weight = sum(c.weight_g for c in components)
        total_cals = sum(c.calories for c in components)
        total_p = sum(c.protein_g for c in components)
        total_c = sum(c.carbs_g for c in components)
        total_f = sum(c.fat_g for c in components)
        total_fib = sum(c.fiber_g for c in components)

        return CurryCompositeDecompositionResult(
            composite_meal_name=f"Full Banana Leaf Feast ({'Non-Veg' if has_non_veg else 'Traditional Vegetarian'})",
            regional_style=leaf_style,
            components=components,
            total_weight_g=round(total_weight, 1),
            total_calories_range={
                "low": round(total_cals * 0.90, 1),
                "expected": round(total_cals, 1),
                "high": round(total_cals * 1.12, 1)
            },
            total_protein_g=round(total_p, 1),
            total_carbs_g=round(total_c, 1),
            total_fat_g=round(total_f, 1),
            total_fiber_g=round(total_fib, 1),
            overall_confidence=0.93,
            decomposition_notes="Complete component-level deconstruction of Banana Leaf meal adhering to Section 67 rules (zero monolithic estimation)."
        )
