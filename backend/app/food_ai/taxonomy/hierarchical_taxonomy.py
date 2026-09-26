"""
Hierarchical Food Taxonomy
Enforces 7-level structured categorization for fine-grained classification.
"""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field

class HierarchicalLabel(BaseModel):
    level1_food_or_nonfood: str = Field(..., description="Food or Non-Food")
    level2_cuisine_region: str = Field(..., description="e.g. South Indian, North Indian, Western, East Asian")
    level3_category: str = Field(..., description="e.g. Tiffin, Rice Dish, Curry/Gravy, Dry Fry, Bread, Dessert")
    level4_dish: str = Field(..., description="e.g. Dosa, Biryani, Sambar, Kuzhambu, Poriyal")
    level5_variant: str = Field(..., description="e.g. Masala Dosa, Ambur Chicken Biryani, Drumstick Sambar")
    level6_cooking_method: str = Field(..., description="e.g. Pan Fried, Dum/Steam, Slow Simmered, Deep Fried")
    level7_state_and_form: str = Field(..., description="e.g. Cooked Solid, Cooked Semi-Solid, Fermented")

    def to_path(self) -> str:
        return f"{self.level1_food_or_nonfood} > {self.level2_cuisine_region} > {self.level3_category} > {self.level4_dish} > {self.level5_variant} > {self.level6_cooking_method} > {self.level7_state_and_form}"

HIERARCHICAL_EXAMPLES = [
    HierarchicalLabel(
        level1_food_or_nonfood="Food",
        level2_cuisine_region="South Indian",
        level3_category="Tiffin",
        level4_dish="Dosa",
        level5_variant="Masala Dosa",
        level6_cooking_method="Pan Fried",
        level7_state_and_form="Cooked Solid / Folded Crepe"
    ),
    HierarchicalLabel(
        level1_food_or_nonfood="Food",
        level2_cuisine_region="South Indian",
        level3_category="Rice Dish",
        level4_dish="Biryani",
        level5_variant="Dindigul Thalappakatti Mutton Biryani",
        level6_cooking_method="Dum Cooked / Braised",
        level7_state_and_form="Cooked Solid Grains"
    ),
    HierarchicalLabel(
        level1_food_or_nonfood="Food",
        level2_cuisine_region="South Indian",
        level3_category="Tiffin",
        level4_dish="Idli",
        level5_variant="Kanchipuram Idli",
        level6_cooking_method="Steamed",
        level7_state_and_form="Fermented Steamed Cake"
    ),
    HierarchicalLabel(
        level1_food_or_nonfood="Food",
        level2_cuisine_region="South Indian",
        level3_category="Lentil Curry",
        level4_dish="Sambar",
        level5_variant="Drumstick Sambar",
        level6_cooking_method="Boiled / Tempered",
        level7_state_and_form="Cooked Liquid / Semi-Solid"
    )
]
