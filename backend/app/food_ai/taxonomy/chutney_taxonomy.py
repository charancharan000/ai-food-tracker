"""
Chutney Fine-Grained Taxonomy with Visual Attribute Annotations
Explicit attributes: color, texture, visible ingredients, and thickness.
"""

from typing import List, Dict, Any
from pydantic import BaseModel, Field

class ChutneyVisualAttributes(BaseModel):
    chutney_name: str
    dominant_color: str = Field(..., description="e.g. Ivory White, Bright Red, Emerald Green, Golden Orange")
    texture: str = Field(..., description="e.g. Coarse grainy, Smooth paste, Frothy emulsion")
    visible_ingredients: List[str] = Field(default_factory=list, description="e.g. Mustard seeds, curry leaves, red chilli flecks")
    thickness_level: str = Field(..., description="e.g. Runny dipping, Medium pourable, Thick spreadable")
    typical_serving_g: float = 30.0
    calories_per_100g: float
    fat_per_100g: float
    protein_per_100g: float

CHUTNEY_CLASSES: List[str] = [
    "Coconut Chutney",
    "Tomato Chutney",
    "Onion Chutney",
    "Peanut Chutney",
    "Mint Chutney",
    "Coriander Chutney",
    "Ginger Chutney",
    "Garlic Chutney",
    "Red Chutney",
    "Coconut Mint Chutney",
]

CHUTNEY_DATASET_ANNOTATIONS: Dict[str, ChutneyVisualAttributes] = {
    "Coconut Chutney": ChutneyVisualAttributes(
        chutney_name="Coconut Chutney",
        dominant_color="Ivory White to Off-White",
        texture="Slightly grainy shredded coconut emulsion",
        visible_ingredients=["Mustard seeds", "Split urad dal", "Curry leaves", "Green chilli seeds"],
        thickness_level="Medium pourable",
        typical_serving_g=35.0,
        calories_per_100g=195.0,
        fat_per_100g=17.5,
        protein_per_100g=3.2
    ),
    "Tomato Chutney": ChutneyVisualAttributes(
        chutney_name="Tomato Chutney",
        dominant_color="Deep Crimson Red to Orange-Red",
        texture="Smooth-glossy reduction with softened tomato pulp",
        visible_ingredients=["Mustard seeds", "Dried red chillies", "Asafoetida"],
        thickness_level="Medium thick",
        typical_serving_g=30.0,
        calories_per_100g=88.0,
        fat_per_100g=4.2,
        protein_per_100g=1.8
    ),
    "Onion Chutney": ChutneyVisualAttributes(
        chutney_name="Onion Chutney",
        dominant_color="Rustic Maroon / Brownish-Red",
        texture="Caramelized onion paste with tamarind tang",
        visible_ingredients=["Mustard seeds", "Fenugreek seeds", "Red chilli flakes"],
        thickness_level="Thick spreadable",
        typical_serving_g=30.0,
        calories_per_100g=110.0,
        fat_per_100g=5.5,
        protein_per_100g=2.1
    ),
    "Peanut Chutney": ChutneyVisualAttributes(
        chutney_name="Peanut Chutney",
        dominant_color="Creamy Beige / Pale Khaki",
        texture="Rich, dense nutty paste",
        visible_ingredients=["Tempered mustard seeds", "Roasted cumin"],
        thickness_level="Thick spreadable",
        typical_serving_g=35.0,
        calories_per_100g=245.0,
        fat_per_100g=21.0,
        protein_per_100g=9.5
    ),
    "Mint Chutney": ChutneyVisualAttributes(
        chutney_name="Mint Chutney",
        dominant_color="Vibrant Forest Green",
        texture="Fine herb puree with lemon juice",
        visible_ingredients=["Minced mint leaves", "Green chilli fibers"],
        thickness_level="Thin pourable",
        typical_serving_g=25.0,
        calories_per_100g=42.0,
        fat_per_100g=0.8,
        protein_per_100g=2.2
    ),
    "Coriander Chutney": ChutneyVisualAttributes(
        chutney_name="Coriander Chutney",
        dominant_color="Emerald Green with yellowish undertones",
        texture="Silky fresh herb blend",
        visible_ingredients=["Coriander stems", "Roasted chana dal bits"],
        thickness_level="Medium pourable",
        typical_serving_g=30.0,
        calories_per_100g=65.0,
        fat_per_100g=2.5,
        protein_per_100g=2.8
    ),
    "Red Chutney": ChutneyVisualAttributes(
        chutney_name="Red Chutney",
        dominant_color="Bright Spicy Fiery Red",
        texture="Smooth fiery garlic and Byadgi chilli paste",
        visible_ingredients=["Byadgi chilli flakes", "Garlic cloves"],
        thickness_level="Thick spreadable (used inside Mysore Masala Dosa)",
        typical_serving_g=20.0,
        calories_per_100g=135.0,
        fat_per_100g=7.0,
        protein_per_100g=3.0
    ),
    "Coconut Mint Chutney": ChutneyVisualAttributes(
        chutney_name="Coconut Mint Chutney",
        dominant_color="Pale Mint Green",
        texture="Grainy coconut with herbaceous mint aroma",
        visible_ingredients=["Grated coconut shreds", "Green herb flecks", "Mustard seeds"],
        thickness_level="Medium pourable",
        typical_serving_g=35.0,
        calories_per_100g=160.0,
        fat_per_100g=14.0,
        protein_per_100g=2.9
    )
}
