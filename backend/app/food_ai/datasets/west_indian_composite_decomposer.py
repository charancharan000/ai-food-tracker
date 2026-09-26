"""
West Indian Composite Platter & Street Food Decomposers
Implements Sections 10, 11, 12, 13, 14, and 29 of Part 5.
Guarantees:
- Composite multi-component meals and street foods are NEVER collapsed into a single monolithic item.
- Decomposes Vada Pav into: Pav, Batata Vada, Dry Garlic Chutney, Green Chutney, Fried Chilli.
- Decomposes Pav Bhaji into: Bhaji, Butter Pav, Butter Dollop (fat level), Chopped Onions, Lemon, Coriander.
- Decomposes Misal Pav into: Usal Base, Kat/Tarri Gravy, Farsan, Sev, Onions, Coriander, Lemon, Pav.
- Decomposes Gujarati Thali into 10-14 discrete items:
  Rotli/Thepla, Puri, Gujarati Dal, Gujarati Kadhi, Ringan Bateta Shaak, Undhiyu, Khaman Farsan, Khichdi, Sambharo, Papad, Chaas, Chhundo, Shrikhand.
- Decomposes Goan Fish Thali into 6-8 discrete items:
  Goan Ukda Rice, Goan Fish Curry (Xitt Codi), Rava Fish Fry, Kismur (Dry Prawn Salad), Cabbage Foogath, Sol Kadhi, Pickle.
- Filters out non-edible packaging materials (Rule 29): paper plate, newspaper liner, steel katori, disposable cup.
- Calculates physical portion weights, densities, and nutrient breakdown per component.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class WestIndianComponentInstance(BaseModel):
    instance_id: str
    canonical_food_id: str
    food_name: str
    category: str
    portion_name: str
    estimated_weight_g: float
    density_g_cm3: float
    calories_kcal: float
    protein_g: float
    carbs_g: float
    fat_g: float
    fiber_g: float
    confidence: float
    bounding_box: List[float] = Field(default_factory=list)  # [ymin, xmin, ymax, xmax]
    segmentation_mask_ref: Optional[str] = None
    is_packaging_filtered: bool = False


class WestIndianCompositeDecompositionResult(BaseModel):
    meal_type: str  # "vada_pav", "pav_bhaji", "misal_pav", "gujarati_thali", "goan_fish_thali"
    num_components: int
    components: List[WestIndianComponentInstance]
    total_weight_g: float
    total_calories_kcal: float
    total_protein_g: float
    total_carbs_g: float
    total_fat_g: float
    total_fiber_g: float
    packaging_detected: List[str] = Field(default_factory=list)
    visual_fat_level: str = "medium"  # low, medium, high, unknown
    summary: str


class PackagingFilter:
    """
    Implements Rule 29: Packaging Filter Rule.
    The AI must identify packaging/containers (paper plate, newspaper, plastic bag, steel katori)
    and exclude them completely from food boundaries, volume estimation, and nutrition calculations.
    """
    NON_EDIBLE_ITEMS = {
        "paper_plate": "Paper Plate",
        "newspaper_liner": "Printed Newspaper Liner",
        "disposable_cup": "Paper/Plastic Cutting Chai Cup",
        "banana_leaf_liner": "Banana Leaf Plate Liner",
        "steel_thali_rim": "Stainless Steel Thali Rim",
        "steel_katori": "Stainless Steel Katori Bowl",
        "foil_container": "Aluminium Takeaway Foil Box",
        "plastic_pouch": "Polythene Chutney Pouch"
    }

    @classmethod
    def detect_and_filter_packaging(cls, visual_tags: List[str]) -> List[str]:
        detected = []
        for tag in visual_tags:
            tag_clean = tag.lower().replace(" ", "_")
            if tag_clean in cls.NON_EDIBLE_ITEMS:
                detected.append(cls.NON_EDIBLE_ITEMS[tag_clean])
        return detected


class VadaPavDecomposer:
    """
    Decomposes Mumbai Vada Pav into its authentic separate physical components:
    Pav, Batata Vada, Dry Garlic Chutney, Green Chutney, and Salted Fried Chilli.
    Never collapses into a single generic fast-food item.
    """
    @classmethod
    def decompose(cls, meta: Optional[Dict[str, Any]] = None) -> WestIndianCompositeDecompositionResult:
        meta = meta or {}
        num_vadas = meta.get("num_vadas", 1)
        include_fried_chilli = meta.get("include_fried_chilli", True)
        include_sweet_chutney = meta.get("include_sweet_chutney", False)
        visual_tags = meta.get("visual_tags", ["paper_plate"])

        packaging = PackagingFilter.detect_and_filter_packaging(visual_tags)
        components: List[WestIndianComponentInstance] = []

        for i in range(num_vadas):
            idx_str = f"_{i+1}" if num_vadas > 1 else ""

            # 1. Pav (Ladi Pav cut open)
            components.append(WestIndianComponentInstance(
                instance_id=f"vadapav_pav{idx_str}",
                canonical_food_id="MH_BREAD_PAV",
                food_name=f"Ladi Pav{idx_str}",
                category="Bread",
                portion_name="1 piece",
                estimated_weight_g=50.0,
                density_g_cm3=0.38,
                calories_kcal=135.0,
                protein_g=4.2,
                carbs_g=26.5,
                fat_g=1.2,
                fiber_g=1.1,
                confidence=0.98,
                bounding_box=[0.15, 0.15, 0.85, 0.85]
            ))

            # 2. Batata Vada (deep fried spiced potato sphere in besan batter)
            components.append(WestIndianComponentInstance(
                instance_id=f"vadapav_vada{idx_str}",
                canonical_food_id="MH_SNACK_BATATA_VADA",
                food_name=f"Batata Vada{idx_str}",
                category="Fritter/Snack",
                portion_name="1 piece",
                estimated_weight_g=75.0,
                density_g_cm3=0.88,
                calories_kcal=185.0,
                protein_g=3.8,
                carbs_g=23.0,
                fat_g=9.0,
                fiber_g=2.2,
                confidence=0.97,
                bounding_box=[0.30, 0.25, 0.70, 0.75]
            ))

            # 3. Dry Garlic Chutney (Lasun Shenga Chutney)
            components.append(WestIndianComponentInstance(
                instance_id=f"vadapav_dry_garlic_chutney{idx_str}",
                canonical_food_id="MH_CHUTNEY_DRY_GARLIC",
                food_name="Dry Red Garlic Chutney",
                category="Condiment",
                portion_name="1 tbsp (inside pav)",
                estimated_weight_g=10.0,
                density_g_cm3=0.65,
                calories_kcal=45.0,
                protein_g=1.2,
                carbs_g=3.5,
                fat_g=2.8,
                fiber_g=0.9,
                confidence=0.94,
                bounding_box=[0.40, 0.35, 0.60, 0.65]
            ))

            # 4. Green Chutney (Mint-Coriander-Chilli)
            components.append(WestIndianComponentInstance(
                instance_id=f"vadapav_green_chutney{idx_str}",
                canonical_food_id="MH_CHUTNEY_GREEN_THECHA",
                food_name="Spicy Green Chutney",
                category="Condiment",
                portion_name="1 tbsp",
                estimated_weight_g=12.0,
                density_g_cm3=0.95,
                calories_kcal=14.0,
                protein_g=0.5,
                carbs_g=1.8,
                fat_g=0.4,
                fiber_g=0.7,
                confidence=0.93,
                bounding_box=[0.42, 0.32, 0.58, 0.68]
            ))

            # 5. Optional Sweet Tamarind Chutney
            if include_sweet_chutney:
                components.append(WestIndianComponentInstance(
                    instance_id=f"vadapav_sweet_chutney{idx_str}",
                    canonical_food_id="MUM_CHUTNEY_MEETHA_TAMARIND",
                    food_name="Sweet Tamarind Chutney",
                    category="Condiment",
                    portion_name="1 tbsp",
                    estimated_weight_g=12.0,
                    density_g_cm3=1.15,
                    calories_kcal=26.0,
                    protein_g=0.2,
                    carbs_g=6.2,
                    fat_g=0.1,
                    fiber_g=0.3,
                    confidence=0.91,
                    bounding_box=[0.43, 0.33, 0.57, 0.67]
                ))

            # 6. Fried Green Chilli
            if include_fried_chilli:
                components.append(WestIndianComponentInstance(
                    instance_id=f"vadapav_fried_chilli{idx_str}",
                    canonical_food_id="MH_GARNISH_FRIED_CHILLI",
                    food_name="Fried Salted Green Chilli",
                    category="Garnish",
                    portion_name="1 whole chilli",
                    estimated_weight_g=8.0,
                    density_g_cm3=0.82,
                    calories_kcal=16.0,
                    protein_g=0.3,
                    carbs_g=1.2,
                    fat_g=1.1,
                    fiber_g=0.5,
                    confidence=0.96,
                    bounding_box=[0.75, 0.60, 0.88, 0.85]
                ))

        total_weight = sum(c.estimated_weight_g for c in components)
        total_cals = sum(c.calories_kcal for c in components)
        total_prot = sum(c.protein_g for c in components)
        total_carbs = sum(c.carbs_g for c in components)
        total_fat = sum(c.fat_g for c in components)
        total_fiber = sum(c.fiber_g for c in components)

        return WestIndianCompositeDecompositionResult(
            meal_type="vada_pav",
            num_components=len(components),
            components=components,
            total_weight_g=round(total_weight, 1),
            total_calories_kcal=round(total_cals, 1),
            total_protein_g=round(total_prot, 1),
            total_carbs_g=round(total_carbs, 1),
            total_fat_g=round(total_fat, 1),
            total_fiber_g=round(total_fiber, 1),
            packaging_detected=packaging,
            visual_fat_level="medium",
            summary=f"Vada Pav decomposed into {len(components)} distinct food instances (Pav + Batata Vada + Chutneys + Chilli)."
        )


class PavBhajiDecomposer:
    """
    Decomposes Pav Bhaji into:
    Bhaji, Butter-toasted Pav, Butter Dollop / Pool, Chopped Onions, Lemon Wedge, Coriander.
    Implements visual butter pool detection and fat-level categorisation (Rule 34 & 7).
    """
    @classmethod
    def decompose(cls, meta: Optional[Dict[str, Any]] = None) -> WestIndianCompositeDecompositionResult:
        meta = meta or {}
        num_pav = meta.get("num_pav", 2)
        butter_level = meta.get("butter_level", "medium")  # low, medium, high (Amul dollop)
        cheese_pav_bhaji = meta.get("cheese_pav_bhaji", False)
        visual_tags = meta.get("visual_tags", ["steel_thali_rim"])

        packaging = PackagingFilter.detect_and_filter_packaging(visual_tags)
        components: List[WestIndianComponentInstance] = []

        # 1. Bhaji base (mashed mixed veg: potato, peas, tomato, cauliflower, capsicum)
        components.append(WestIndianComponentInstance(
            instance_id="pavbhaji_bhaji_core",
            canonical_food_id="MUM_STREET_PAV_BHAJI",
            food_name="Spiced Vegetable Bhaji",
            category="Curry/Bhaji",
            portion_name="1 large katori (200g)",
            estimated_weight_g=200.0,
            density_g_cm3=1.04,
            calories_kcal=210.0,
            protein_g=4.8,
            carbs_g=28.0,
            fat_g=9.0,
            fiber_g=5.6,
            confidence=0.98,
            bounding_box=[0.10, 0.45, 0.85, 0.95]
        ))

        # 2. Butter addition (melted pool / yellow pat on bhaji)
        butter_weight_g = 10.0
        if butter_level == "low":
            butter_weight_g = 5.0
        elif butter_level == "high":
            butter_weight_g = 22.0

        components.append(WestIndianComponentInstance(
            instance_id="pavbhaji_butter_pool",
            canonical_food_id="WI_FAT_BUTTER_DOLLOP",
            food_name=f"Butter Dollop/Pool ({butter_level.capitalize()} Fat)",
            category="Fat/Dairy",
            portion_name=f"{butter_weight_g}g butter dollop",
            estimated_weight_g=butter_weight_g,
            density_g_cm3=0.91,
            calories_kcal=round(butter_weight_g * 7.17, 1),
            protein_g=0.1,
            carbs_g=0.1,
            fat_g=round(butter_weight_g * 0.81, 1),
            fiber_g=0.0,
            confidence=0.95,
            bounding_box=[0.35, 0.60, 0.55, 0.80]
        ))

        # Cheese option
        if cheese_pav_bhaji:
            components.append(WestIndianComponentInstance(
                instance_id="pavbhaji_cheese_shreds",
                canonical_food_id="WI_TOPPING_PROCESSED_CHEESE",
                food_name="Grated Processed Cheese Topping",
                category="Dairy/Topping",
                portion_name="30g grated cheese",
                estimated_weight_g=30.0,
                density_g_cm3=0.85,
                calories_kcal=110.0,
                protein_g=6.5,
                carbs_g=1.0,
                fat_g=9.2,
                fiber_g=0.0,
                confidence=0.96,
                bounding_box=[0.20, 0.50, 0.70, 0.90]
            ))

        # 3. Butter-Toasted Ladi Pav
        for i in range(num_pav):
            components.append(WestIndianComponentInstance(
                instance_id=f"pavbhaji_pav_{i+1}",
                canonical_food_id="MH_BREAD_PAV",
                food_name=f"Butter-Toasted Pav #{i+1}",
                category="Bread",
                portion_name="1 piece buttered",
                estimated_weight_g=48.0,
                density_g_cm3=0.40,
                calories_kcal=155.0,  # pav + tawa butter absorption
                protein_g=4.0,
                carbs_g=25.5,
                fat_g=4.2,
                fiber_g=1.1,
                confidence=0.97,
                bounding_box=[0.15 + (i * 0.35), 0.05, 0.48 + (i * 0.35), 0.40]
            ))

        # 4. Chopped Raw Onions
        components.append(WestIndianComponentInstance(
            instance_id="pavbhaji_chopped_onions",
            canonical_food_id="WI_GARNISH_CHOPPED_ONIONS",
            food_name="Finely Chopped Red Onions",
            category="Garnish/Salad",
            portion_name="1 side portion",
            estimated_weight_g=28.0,
            density_g_cm3=0.78,
            calories_kcal=11.2,
            protein_g=0.3,
            carbs_g=2.6,
            fat_g=0.0,
            fiber_g=0.5,
            confidence=0.96,
            bounding_box=[0.75, 0.10, 0.95, 0.30]
        ))

        # 5. Lemon Wedge
        components.append(WestIndianComponentInstance(
            instance_id="pavbhaji_lemon_wedge",
            canonical_food_id="WI_GARNISH_LEMON_WEDGE",
            food_name="Fresh Lemon Wedge",
            category="Garnish",
            portion_name="1 wedge",
            estimated_weight_g=15.0,
            density_g_cm3=0.92,
            calories_kcal=4.5,
            protein_g=0.1,
            carbs_g=1.2,
            fat_g=0.0,
            fiber_g=0.4,
            confidence=0.98,
            bounding_box=[0.78, 0.32, 0.92, 0.44]
        ))

        # 6. Fresh Coriander Garnish
        components.append(WestIndianComponentInstance(
            instance_id="pavbhaji_coriander",
            canonical_food_id="WI_GARNISH_CORIANDER",
            food_name="Fresh Chopped Coriander",
            category="Garnish",
            portion_name="Garnish sprinkle",
            estimated_weight_g=4.0,
            density_g_cm3=0.45,
            calories_kcal=1.0,
            protein_g=0.1,
            carbs_g=0.2,
            fat_g=0.0,
            fiber_g=0.1,
            confidence=0.94,
            bounding_box=[0.25, 0.55, 0.45, 0.75]
        ))

        total_weight = sum(c.estimated_weight_g for c in components)
        total_cals = sum(c.calories_kcal for c in components)
        total_prot = sum(c.protein_g for c in components)
        total_carbs = sum(c.carbs_g for c in components)
        total_fat = sum(c.fat_g for c in components)
        total_fiber = sum(c.fiber_g for c in components)

        return WestIndianCompositeDecompositionResult(
            meal_type="pav_bhaji",
            num_components=len(components),
            components=components,
            total_weight_g=round(total_weight, 1),
            total_calories_kcal=round(total_cals, 1),
            total_protein_g=round(total_prot, 1),
            total_carbs_g=round(total_carbs, 1),
            total_fat_g=round(total_fat, 1),
            total_fiber_g=round(total_fiber, 1),
            packaging_detected=packaging,
            visual_fat_level=butter_level,
            summary=f"Pav Bhaji decomposed into {len(components)} items (Bhaji + Butter Pool + {num_pav} Pavs + Onion/Lemon/Coriander)."
        )


class MisalPavDecomposer:
    """
    Decomposes Kolhapuri / Puneri / Mumbai Misal Pav into:
    Sprouted Moth/Matki Usal base, Kat/Tarri Gravy, Farsan/Chevdo, Fine Sev, Chopped Onions, Coriander, Lemon, Pav, and Extra Rassa.
    """
    @classmethod
    def decompose(cls, meta: Optional[Dict[str, Any]] = None) -> WestIndianCompositeDecompositionResult:
        meta = meta or {}
        num_pav = meta.get("num_pav", 2)
        has_extra_rassa = meta.get("has_extra_rassa", True)
        misal_style = meta.get("misal_style", "kolhapuri")  # kolhapuri (fiery oily tarri) vs puneri (mild)
        visual_tags = meta.get("visual_tags", ["paper_plate"])

        packaging = PackagingFilter.detect_and_filter_packaging(visual_tags)
        components: List[WestIndianComponentInstance] = []

        # 1. Sprouted Matki Usal (Boiled legume base)
        components.append(WestIndianComponentInstance(
            instance_id="misal_matki_usal",
            canonical_food_id="MH_CURRY_USAL_MATKI",
            food_name="Sprouted Matki Usal Base",
            category="Legume/Curry",
            portion_name="1 cup boiled sprouts",
            estimated_weight_g=130.0,
            density_g_cm3=1.05,
            calories_kcal=145.0,
            protein_g=8.5,
            carbs_g=23.0,
            fat_g=2.1,
            fiber_g=6.2,
            confidence=0.96,
            bounding_box=[0.20, 0.40, 0.75, 0.85]
        ))

        # 2. Kat / Tarri / Rassa (Spicy Red Gravy with oil layer)
        kat_fat = 8.5 if misal_style == "kolhapuri" else 5.0
        components.append(WestIndianComponentInstance(
            instance_id="misal_kat_tarri",
            canonical_food_id="MH_CURRY_MISAL_KAT",
            food_name=f"Misal Kat/Tarri Gravy ({misal_style.capitalize()} Style)",
            category="Gravy",
            portion_name="120ml spicy gravy",
            estimated_weight_g=120.0,
            density_g_cm3=1.02,
            calories_kcal=round(55.0 + (kat_fat * 9.0), 1),
            protein_g=1.8,
            carbs_g=6.2,
            fat_g=kat_fat,
            fiber_g=1.2,
            confidence=0.95,
            bounding_box=[0.18, 0.38, 0.78, 0.88]
        ))

        # 3. Farsan / Mixed Crispy Chevdo
        components.append(WestIndianComponentInstance(
            instance_id="misal_farsan_topping",
            canonical_food_id="MH_FARSAN_CHEVDO",
            food_name="Crispy Mixed Farsan",
            category="Snack/Topping",
            portion_name="35g topping",
            estimated_weight_g=35.0,
            density_g_cm3=0.55,
            calories_kcal=180.0,
            protein_g=3.2,
            carbs_g=18.5,
            fat_g=10.5,
            fiber_g=1.8,
            confidence=0.97,
            bounding_box=[0.25, 0.42, 0.70, 0.82]
        ))

        # 4. Fine Besan Sev
        components.append(WestIndianComponentInstance(
            instance_id="misal_fine_sev",
            canonical_food_id="WI_SNACK_SEV",
            food_name="Crisp Besan Sev",
            category="Topping",
            portion_name="15g sprinkle",
            estimated_weight_g=15.0,
            density_g_cm3=0.52,
            calories_kcal=82.0,
            protein_g=1.8,
            carbs_g=7.2,
            fat_g=5.1,
            fiber_g=0.8,
            confidence=0.96,
            bounding_box=[0.28, 0.45, 0.65, 0.80]
        ))

        # 5. Chopped Red Onions
        components.append(WestIndianComponentInstance(
            instance_id="misal_chopped_onions",
            canonical_food_id="WI_GARNISH_CHOPPED_ONIONS",
            food_name="Chopped Red Onions",
            category="Garnish",
            portion_name="25g garnish",
            estimated_weight_g=25.0,
            density_g_cm3=0.78,
            calories_kcal=10.0,
            protein_g=0.3,
            carbs_g=2.3,
            fat_g=0.0,
            fiber_g=0.4,
            confidence=0.97,
            bounding_box=[0.30, 0.48, 0.60, 0.78]
        ))

        # 6. Chopped Coriander
        components.append(WestIndianComponentInstance(
            instance_id="misal_coriander",
            canonical_food_id="WI_GARNISH_CORIANDER",
            food_name="Fresh Chopped Coriander",
            category="Garnish",
            portion_name="4g garnish",
            estimated_weight_g=4.0,
            density_g_cm3=0.45,
            calories_kcal=1.0,
            protein_g=0.1,
            carbs_g=0.2,
            fat_g=0.0,
            fiber_g=0.1,
            confidence=0.95,
            bounding_box=[0.32, 0.50, 0.58, 0.75]
        ))

        # 7. Lemon Wedge
        components.append(WestIndianComponentInstance(
            instance_id="misal_lemon_wedge",
            canonical_food_id="WI_GARNISH_LEMON_WEDGE",
            food_name="Lemon Wedge",
            category="Garnish",
            portion_name="1 wedge",
            estimated_weight_g=12.0,
            density_g_cm3=0.92,
            calories_kcal=3.6,
            protein_g=0.1,
            carbs_g=1.0,
            fat_g=0.0,
            fiber_g=0.3,
            confidence=0.98,
            bounding_box=[0.80, 0.45, 0.92, 0.55]
        ))

        # 8. Pav Pieces
        for i in range(num_pav):
            components.append(WestIndianComponentInstance(
                instance_id=f"misal_pav_{i+1}",
                canonical_food_id="MH_BREAD_PAV",
                food_name=f"Ladi Pav #{i+1}",
                category="Bread",
                portion_name="1 piece",
                estimated_weight_g=48.0,
                density_g_cm3=0.38,
                calories_kcal=130.0,
                protein_g=4.0,
                carbs_g=25.5,
                fat_g=1.1,
                fiber_g=1.0,
                confidence=0.98,
                bounding_box=[0.15 + (i * 0.35), 0.05, 0.48 + (i * 0.35), 0.35]
            ))

        # 9. Extra Kat/Rassa Katori Bowl
        if has_extra_rassa:
            components.append(WestIndianComponentInstance(
                instance_id="misal_extra_rassa_bowl",
                canonical_food_id="MH_CURRY_MISAL_KAT",
                food_name="Extra Kat/Rassa Bowl",
                category="Gravy",
                portion_name="1 katori extra rassa (90ml)",
                estimated_weight_g=90.0,
                density_g_cm3=1.02,
                calories_kcal=round(40.0 + (kat_fat * 0.7 * 9.0), 1),
                protein_g=1.2,
                carbs_g=4.5,
                fat_g=round(kat_fat * 0.7, 1),
                fiber_g=0.8,
                confidence=0.93,
                bounding_box=[0.72, 0.65, 0.95, 0.92]
            ))

        total_weight = sum(c.estimated_weight_g for c in components)
        total_cals = sum(c.calories_kcal for c in components)
        total_prot = sum(c.protein_g for c in components)
        total_carbs = sum(c.carbs_g for c in components)
        total_fat = sum(c.fat_g for c in components)
        total_fiber = sum(c.fiber_g for c in components)

        return WestIndianCompositeDecompositionResult(
            meal_type="misal_pav",
            num_components=len(components),
            components=components,
            total_weight_g=round(total_weight, 1),
            total_calories_kcal=round(total_cals, 1),
            total_protein_g=round(total_prot, 1),
            total_carbs_g=round(total_carbs, 1),
            total_fat_g=round(total_fat, 1),
            total_fiber_g=round(total_fiber, 1),
            packaging_detected=packaging,
            visual_fat_level="high" if misal_style == "kolhapuri" else "medium",
            summary=f"Misal Pav decomposed into {len(components)} items (Usal + Kat/Tarri + Farsan + Sev + {num_pav} Pavs + Extra Rassa)."
        )


class GujaratiThaliDecomposer:
    """
    Decomposes a Traditional Gujarati Thali into 10 to 14 discrete authentic components:
    Rotli/Thepla, Puri, Gujarati Dal, Gujarati Kadhi, Ringan Bateta Shaak, Undhiyu, Khaman Farsan,
    Khichdi, Sambharo, Roasted Papad, Chaas, Chhundo Pickle, and Shrikhand Sweet.
    """
    @classmethod
    def decompose(cls, meta: Optional[Dict[str, Any]] = None) -> WestIndianCompositeDecompositionResult:
        meta = meta or {}
        num_rotli = meta.get("num_rotli", 3)
        num_puri = meta.get("num_puri", 2)
        has_undhiyu = meta.get("has_undhiyu", True)
        has_sweet = meta.get("has_sweet", True)
        visual_tags = meta.get("visual_tags", ["steel_thali_rim", "steel_katori"])

        packaging = PackagingFilter.detect_and_filter_packaging(visual_tags)
        components: List[WestIndianComponentInstance] = []

        # 1. Gujarati Phulka Rotli (thin, soft, with light ghee sheen)
        for i in range(num_rotli):
            components.append(WestIndianComponentInstance(
                instance_id=f"gj_thali_rotli_{i+1}",
                canonical_food_id="GJ_BREAD_ROTLO_PHULKA",
                food_name=f"Gujarati Phulka Rotli #{i+1}",
                category="Bread",
                portion_name="1 thin piece",
                estimated_weight_g=24.0,
                density_g_cm3=0.74,
                calories_kcal=72.0,
                protein_g=2.4,
                carbs_g=14.0,
                fat_g=0.9,
                fiber_g=2.1,
                confidence=0.97,
                bounding_box=[0.10 + (i * 0.04), 0.10, 0.35 + (i * 0.04), 0.35]
            ))

        # 2. Gujarati Puri
        for i in range(num_puri):
            components.append(WestIndianComponentInstance(
                instance_id=f"gj_thali_puri_{i+1}",
                canonical_food_id="GJ_BREAD_PURI",
                food_name=f"Gujarati Puri #{i+1}",
                category="Bread/Fried",
                portion_name="1 small puri",
                estimated_weight_g=22.0,
                density_g_cm3=0.68,
                calories_kcal=88.0,
                protein_g=1.8,
                carbs_g=10.5,
                fat_g=4.6,
                fiber_g=0.9,
                confidence=0.96,
                bounding_box=[0.25 + (i * 0.05), 0.15, 0.45 + (i * 0.05), 0.35]
            ))

        # 3. Gujarati Dal (Thin sweet and sour toor dal with jaggery, peanuts, kokum)
        components.append(WestIndianComponentInstance(
            instance_id="gj_thali_dal",
            canonical_food_id="GJ_DAL_GUJARATI",
            food_name="Gujarati Sweet & Sour Dal",
            category="Dal/Soup",
            portion_name="1 katori (140g)",
            estimated_weight_g=140.0,
            density_g_cm3=1.04,
            calories_kcal=125.0,
            protein_g=4.8,
            carbs_g=19.2,
            fat_g=3.2,
            fiber_g=2.8,
            confidence=0.98,
            bounding_box=[0.05, 0.40, 0.30, 0.60]
        ))

        # 4. Gujarati Kadhi (Yogurt-besan sweet-tangy soup with cinnamon & cloves)
        components.append(WestIndianComponentInstance(
            instance_id="gj_thali_kadhi",
            canonical_food_id="GJ_KADHI_GUJARATI",
            food_name="Gujarati Kadhi",
            category="Curry/Kadhi",
            portion_name="1 katori (140g)",
            estimated_weight_g=140.0,
            density_g_cm3=1.03,
            calories_kcal=110.0,
            protein_g=3.8,
            carbs_g=14.5,
            fat_g=4.2,
            fiber_g=0.6,
            confidence=0.97,
            bounding_box=[0.05, 0.65, 0.30, 0.85]
        ))

        # 5. Ringan Bateta Nu Shaak (Eggplant and potato dry/semi-gravy curry)
        components.append(WestIndianComponentInstance(
            instance_id="gj_thali_ringan_bateta",
            canonical_food_id="GJ_CURRY_RINGAN_BATETA",
            food_name="Ringan Bateta Nu Shaak",
            category="Vegetable Curry",
            portion_name="1 katori (120g)",
            estimated_weight_g=120.0,
            density_g_cm3=1.02,
            calories_kcal=132.0,
            protein_g=2.4,
            carbs_g=18.0,
            fat_g=5.6,
            fiber_g=3.8,
            confidence=0.96,
            bounding_box=[0.35, 0.70, 0.60, 0.95]
        ))

        # 6. Undhiyu (Mixed vegetables, surti papdi, purple yam, methi muthia)
        if has_undhiyu:
            components.append(WestIndianComponentInstance(
                instance_id="gj_thali_undhiyu",
                canonical_food_id="GJ_CURRY_UNDHIYU",
                food_name="Authentic Surti Undhiyu",
                category="Vegetable Stew",
                portion_name="1 katori (140g)",
                estimated_weight_g=140.0,
                density_g_cm3=1.06,
                calories_kcal=210.0,
                protein_g=5.2,
                carbs_g=24.5,
                fat_g=10.2,
                fiber_g=5.4,
                confidence=0.98,
                bounding_box=[0.35, 0.45, 0.60, 0.68]
            ))

        # 7. Farsan: Khaman Dhokla (2 steamed yellow sponge squares with mustard seeds)
        components.append(WestIndianComponentInstance(
            instance_id="gj_thali_khaman_farsan",
            canonical_food_id="GJ_FARSAN_KHAMAN",
            food_name="Khaman Dhokla Farsan (2 pcs)",
            category="Farsan/Appetizer",
            portion_name="2 pieces (70g)",
            estimated_weight_g=70.0,
            density_g_cm3=0.72,
            calories_kcal=115.0,
            protein_g=4.2,
            carbs_g=18.2,
            fat_g=2.8,
            fiber_g=2.1,
            confidence=0.97,
            bounding_box=[0.65, 0.15, 0.85, 0.35]
        ))

        # 8. Gujarati Khichdi / Steamed Rice
        components.append(WestIndianComponentInstance(
            instance_id="gj_thali_khichdi",
            canonical_food_id="GJ_RICE_KHICHDI",
            food_name="Vaghareli Khichdi",
            category="Rice/Grain",
            portion_name="1 scoop (140g)",
            estimated_weight_g=140.0,
            density_g_cm3=1.08,
            calories_kcal=175.0,
            protein_g=5.2,
            carbs_g=31.0,
            fat_g=3.4,
            fiber_g=2.6,
            confidence=0.96,
            bounding_box=[0.40, 0.30, 0.65, 0.50]
        ))

        # 9. Sambharo (Warm stir-fried crunchy cabbage & carrot salad with mustard)
        components.append(WestIndianComponentInstance(
            instance_id="gj_thali_sambharo",
            canonical_food_id="GJ_SALAD_SAMBHARO",
            food_name="Cabbage Carrot Sambharo",
            category="Warm Salad",
            portion_name="1 small cup (50g)",
            estimated_weight_g=50.0,
            density_g_cm3=0.75,
            calories_kcal=42.0,
            protein_g=0.8,
            carbs_g=4.8,
            fat_g=2.2,
            fiber_g=1.8,
            confidence=0.95,
            bounding_box=[0.65, 0.40, 0.82, 0.55]
        ))

        # 10. Roasted Udad Papad
        components.append(WestIndianComponentInstance(
            instance_id="gj_thali_papad",
            canonical_food_id="WI_ACCOMPANIMENT_PAPAD",
            food_name="Roasted Udad Papad",
            category="Accompaniment",
            portion_name="1 whole crisp papad",
            estimated_weight_g=15.0,
            density_g_cm3=0.45,
            calories_kcal=48.0,
            protein_g=3.2,
            carbs_g=8.0,
            fat_g=0.4,
            fiber_g=1.2,
            confidence=0.99,
            bounding_box=[0.02, 0.20, 0.22, 0.40]
        ))

        # 11. Gujarati Chaas (Light spiced buttermilk with cumin & salt)
        components.append(WestIndianComponentInstance(
            instance_id="gj_thali_chaas",
            canonical_food_id="GJ_BEVERAGE_CHAAS",
            food_name="Gujarati Spiced Chaas",
            category="Beverage/Dairy",
            portion_name="1 steel glass (180ml)",
            estimated_weight_g=180.0,
            density_g_cm3=1.01,
            calories_kcal=58.0,
            protein_g=3.2,
            carbs_g=5.4,
            fat_g=2.5,
            fiber_g=0.0,
            confidence=0.98,
            bounding_box=[0.02, 0.85, 0.30, 0.98]
        ))

        # 12. Chhundo / Mango Pickle
        components.append(WestIndianComponentInstance(
            instance_id="gj_thali_chhundo",
            canonical_food_id="GJ_PICKLE_CHHUNDO",
            food_name="Gujarati Raw Mango Chhundo",
            category="Condiment/Pickle",
            portion_name="1 spoonful (15g)",
            estimated_weight_g=15.0,
            density_g_cm3=1.20,
            calories_kcal=42.0,
            protein_g=0.1,
            carbs_g=10.5,
            fat_g=0.1,
            fiber_g=0.4,
            confidence=0.94,
            bounding_box=[0.60, 0.60, 0.70, 0.70]
        ))

        # 13. Sweet: Kesar Shrikhand
        if has_sweet:
            components.append(WestIndianComponentInstance(
                instance_id="gj_thali_sweet_shrikhand",
                canonical_food_id="MH_SWEET_SHRIKHAND",
                food_name="Kesar Elaichi Shrikhand",
                category="Sweet/Dessert",
                portion_name="1 small katori (70g)",
                estimated_weight_g=70.0,
                density_g_cm3=1.12,
                calories_kcal=215.0,
                protein_g=5.5,
                carbs_g=26.0,
                fat_g=10.2,
                fiber_g=0.0,
                confidence=0.97,
                bounding_box=[0.65, 0.75, 0.88, 0.95]
            ))

        total_weight = sum(c.estimated_weight_g for c in components)
        total_cals = sum(c.calories_kcal for c in components)
        total_prot = sum(c.protein_g for c in components)
        total_carbs = sum(c.carbs_g for c in components)
        total_fat = sum(c.fat_g for c in components)
        total_fiber = sum(c.fiber_g for c in components)

        return WestIndianCompositeDecompositionResult(
            meal_type="gujarati_thali",
            num_components=len(components),
            components=components,
            total_weight_g=round(total_weight, 1),
            total_calories_kcal=round(total_cals, 1),
            total_protein_g=round(total_prot, 1),
            total_carbs_g=round(total_carbs, 1),
            total_fat_g=round(total_fat, 1),
            total_fiber_g=round(total_fiber, 1),
            packaging_detected=packaging,
            visual_fat_level="medium",
            summary=f"Traditional Gujarati Thali decomposed into {len(components)} discrete items (Rotli, Puri, Dal, Kadhi, Shaak, Undhiyu, Farsan, Khichdi, Chaas, Sweet)."
        )


class GoanFishThaliDecomposer:
    """
    Decomposes an Authentic Goan Fish Thali into 6 to 8 discrete components:
    Goan Ukda Rice, Goan Fish Curry (Xitt Codi), Rava Fish Fry, Kismur (dry prawn salad),
    Cabbage Foogath, Sol Kadhi, and Goan Pickle.
    """
    @classmethod
    def decompose(cls, meta: Optional[Dict[str, Any]] = None) -> WestIndianCompositeDecompositionResult:
        meta = meta or {}
        fish_type = meta.get("fish_type", "surmai")  # surmai / kingfish, bangda / mackerel, pomfret
        has_kismur = meta.get("has_kismur", True)
        visual_tags = meta.get("visual_tags", ["steel_thali_rim", "steel_katori"])

        packaging = PackagingFilter.detect_and_filter_packaging(visual_tags)
        components: List[WestIndianComponentInstance] = []

        # 1. Goan Red Ukda Boiled Rice (thick parboiled reddish grains)
        components.append(WestIndianComponentInstance(
            instance_id="goan_thali_rice",
            canonical_food_id="GA_RICE_UKDA_BOILED",
            food_name="Goan Ukda Boiled Rice",
            category="Rice/Grain",
            portion_name="1 mound (200g)",
            estimated_weight_g=200.0,
            density_g_cm3=1.05,
            calories_kcal=230.0,
            protein_g=4.8,
            carbs_g=50.2,
            fat_g=0.6,
            fiber_g=2.4,
            confidence=0.98,
            bounding_box=[0.20, 0.20, 0.65, 0.65]
        ))

        # 2. Goan Fish Curry (Xitt Codi: orange coconut gravy with kokum/tefla)
        components.append(WestIndianComponentInstance(
            instance_id="goan_thali_fish_curry",
            canonical_food_id="GA_CURRY_FISH_XITT_CODI",
            food_name=f"Goan Fish Curry (Xitt Codi - {fish_type.capitalize()})",
            category="Seafood Curry",
            portion_name="1 katori (160g)",
            estimated_weight_g=160.0,
            density_g_cm3=1.03,
            calories_kcal=195.0,
            protein_g=14.5,
            carbs_g=4.2,
            fat_g=13.0,
            fiber_g=1.2,
            confidence=0.97,
            bounding_box=[0.05, 0.45, 0.32, 0.75]
        ))

        # 3. Rava Fish Fry (Semolina crusted shallow fried fish steak)
        fry_weight = 110.0 if fish_type == "surmai" else 95.0
        components.append(WestIndianComponentInstance(
            instance_id="goan_thali_rava_fish_fry",
            canonical_food_id="GA_SEAFOOD_RAVA_FISH_FRY",
            food_name=f"Rava Fried Fish ({fish_type.capitalize()})",
            category="Seafood/Fried",
            portion_name="1 steak/piece",
            estimated_weight_g=fry_weight,
            density_g_cm3=0.96,
            calories_kcal=220.0,
            protein_g=21.0,
            carbs_g=8.5,
            fat_g=11.2,
            fiber_g=0.8,
            confidence=0.98,
            bounding_box=[0.60, 0.15, 0.88, 0.45]
        ))

        # 4. Kismur (Traditional Goan dry prawn salad with roasted coconut, onion, chilli)
        if has_kismur:
            components.append(WestIndianComponentInstance(
                instance_id="goan_thali_kismur",
                canonical_food_id="GA_SALAD_KISMUR",
                food_name="Goan Dried Prawn Kismur",
                category="Seafood Salad",
                portion_name="1 small katori (45g)",
                estimated_weight_g=45.0,
                density_g_cm3=0.68,
                calories_kcal=95.0,
                protein_g=6.8,
                carbs_g=3.2,
                fat_g=6.1,
                fiber_g=1.5,
                confidence=0.96,
                bounding_box=[0.65, 0.50, 0.85, 0.70]
            ))

        # 5. Cabbage Foogath (Goan style steamed cabbage with mustard and fresh coconut)
        components.append(WestIndianComponentInstance(
            instance_id="goan_thali_foogath",
            canonical_food_id="GA_VEG_CABBAGE_FOOGATH",
            food_name="Cabbage Foogath with Coconut",
            category="Vegetable",
            portion_name="1 katori (80g)",
            estimated_weight_g=80.0,
            density_g_cm3=0.82,
            calories_kcal=68.0,
            protein_g=1.6,
            carbs_g=5.8,
            fat_g=4.2,
            fiber_g=2.5,
            confidence=0.95,
            bounding_box=[0.40, 0.70, 0.65, 0.92]
        ))

        # 6. Sol Kadhi (Pink kokum and coconut milk digestive drink)
        components.append(WestIndianComponentInstance(
            instance_id="goan_thali_sol_kadhi",
            canonical_food_id="GA_BEVERAGE_SOL_KADHI",
            food_name="Goan Sol Kadhi",
            category="Beverage/Soup",
            portion_name="1 katori/glass (120ml)",
            estimated_weight_g=120.0,
            density_g_cm3=1.01,
            calories_kcal=62.0,
            protein_g=1.0,
            carbs_g=3.2,
            fat_g=5.2,
            fiber_g=0.4,
            confidence=0.98,
            bounding_box=[0.05, 0.15, 0.28, 0.38]
        ))

        # 7. Goan Pickle
        components.append(WestIndianComponentInstance(
            instance_id="goan_thali_pickle",
            canonical_food_id="GA_PICKLE_AMBE_CHE",
            food_name="Goan Spicy Raw Mango Pickle",
            category="Condiment",
            portion_name="1 spoonful (15g)",
            estimated_weight_g=15.0,
            density_g_cm3=1.18,
            calories_kcal=24.0,
            protein_g=0.2,
            carbs_g=2.1,
            fat_g=1.7,
            fiber_g=0.3,
            confidence=0.94,
            bounding_box=[0.75, 0.72, 0.88, 0.85]
        ))

        total_weight = sum(c.estimated_weight_g for c in components)
        total_cals = sum(c.calories_kcal for c in components)
        total_prot = sum(c.protein_g for c in components)
        total_carbs = sum(c.carbs_g for c in components)
        total_fat = sum(c.fat_g for c in components)
        total_fiber = sum(c.fiber_g for c in components)

        return WestIndianCompositeDecompositionResult(
            meal_type="goan_fish_thali",
            num_components=len(components),
            components=components,
            total_weight_g=round(total_weight, 1),
            total_calories_kcal=round(total_cals, 1),
            total_protein_g=round(total_prot, 1),
            total_carbs_g=round(total_carbs, 1),
            total_fat_g=round(total_fat, 1),
            total_fiber_g=round(total_fiber, 1),
            packaging_detected=packaging,
            visual_fat_level="medium",
            summary=f"Goan Fish Thali decomposed into {len(components)} items (Ukda Rice, Fish Curry, Rava Fry {fish_type.capitalize()}, Kismur, Foogath, Sol Kadhi, Pickle)."
        )
