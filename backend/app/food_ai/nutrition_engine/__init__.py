"""
Nutrition Engine Package
Exports verified food nutrition database, recipe-level composition calculator,
and calibrated uncertainty model.
"""

from .verified_database import FoodNutritionProfile, VERIFIED_FOOD_NUTRITION_DB
from .recipe_database import RecipeIngredient, RecipeBlueprint, RECIPE_REGISTRY
from .uncertainty_model import CalibratedNutritionEstimate, compute_calibrated_bounds
