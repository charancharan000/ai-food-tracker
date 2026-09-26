"""
Cooking Method, Food State, Food Form, and Ingredient Presence Metadata
Provides fine-grained state classification especially critical for oil absorption and hydration ratios.
"""

from enum import Enum
from typing import List, Dict, Optional
from pydantic import BaseModel, Field

class CookingMethod(str, Enum):
    RAW = "raw"
    BOILED = "boiled"
    STEAMED = "steamed"
    PRESSURE_COOKED = "pressure_cooked"
    GRILLED = "grilled"
    ROASTED = "roasted"
    BAKED = "baked"
    PAN_FRIED = "pan_fried"
    DEEP_FRIED = "deep_fried"
    AIR_FRIED = "air_fried"
    STIR_FRIED = "stir_fried"
    SAUTEED = "sauteed"
    SMOKED = "smoked"
    FERMENTED = "fermented"

class FoodForm(str, Enum):
    WHOLE = "whole"
    SLICED = "sliced"
    CHOPPED = "chopped"
    DICED = "diced"
    MASHED = "mashed"
    GROUND = "ground"
    SHREDDED = "shredded"
    PUREED = "pureed"
    MIXED = "mixed"
    LIQUID = "liquid"
    SEMI_SOLID = "semi-solid"
    SOLID = "solid"

class IngredientPresence(str, Enum):
    PRESENT = "present"
    ABSENT = "absent"
    UNCERTAIN = "uncertain"

class IngredientAnnotation(BaseModel):
    name: str
    status: IngredientPresence = IngredientPresence.PRESENT
    estimated_grams: Optional[float] = None
    confidence: float = Field(default=0.9, ge=0.0, le=1.0)

# Sample complex dish ingredient blueprints
DISH_INGREDIENT_BLUEPRINTS: Dict[str, List[IngredientAnnotation]] = {
    "Masala Dosa": [
        IngredientAnnotation(name="parboiled rice", status=IngredientPresence.PRESENT),
        IngredientAnnotation(name="urad dal", status=IngredientPresence.PRESENT),
        IngredientAnnotation(name="potato", status=IngredientPresence.PRESENT),
        IngredientAnnotation(name="onion", status=IngredientPresence.PRESENT),
        IngredientAnnotation(name="sesame/vegetable oil or ghee", status=IngredientPresence.PRESENT),
        IngredientAnnotation(name="mustard seeds & curry leaves", status=IngredientPresence.PRESENT),
        IngredientAnnotation(name="cheese", status=IngredientPresence.ABSENT),
    ],
    "Chicken Biryani": [
        IngredientAnnotation(name="basmati or seeraga samba rice", status=IngredientPresence.PRESENT),
        IngredientAnnotation(name="chicken pieces with bone", status=IngredientPresence.PRESENT),
        IngredientAnnotation(name="cooking oil or ghee", status=IngredientPresence.PRESENT),
        IngredientAnnotation(name="sliced onion", status=IngredientPresence.PRESENT),
        IngredientAnnotation(name="curd / yogurt", status=IngredientPresence.PRESENT),
        IngredientAnnotation(name="ginger garlic paste & spices", status=IngredientPresence.PRESENT),
        IngredientAnnotation(name="fresh mint & coriander", status=IngredientPresence.PRESENT),
        IngredientAnnotation(name="pork", status=IngredientPresence.ABSENT),
        IngredientAnnotation(name="beef", status=IngredientPresence.ABSENT),
    ],
    "Kothu Parotta": [
        IngredientAnnotation(name="shredded maida parotta", status=IngredientPresence.PRESENT),
        IngredientAnnotation(name="meat/egg gravy (salna)", status=IngredientPresence.PRESENT),
        IngredientAnnotation(name="chopped onions & chillies", status=IngredientPresence.PRESENT),
        IngredientAnnotation(name="refined vegetable oil", status=IngredientPresence.PRESENT),
    ]
}
