"""
Food AI Taxonomies Module
Exports all hierarchical, regional, South Indian, Pan-Indian, and International taxonomies.
"""

from .hierarchical_taxonomy import HierarchicalLabel, HIERARCHICAL_EXAMPLES
from .tamil_nadu_taxonomy import TAMIL_NADU_TIFFIN_TAXONOMY, ALL_TAMIL_TIFFIN_CLASSES, TIFFIN_METADATA
from .rice_taxonomy import TAMIL_RICE_CLASSES, RICE_VARIETIES_METADATA
from .biryani_taxonomy import BIRYANI_PROTEIN_CLASSES, BIRYANI_REGIONAL_STYLES, BIRYANI_HARD_NEGATIVES, BIRYANI_DISTINCTIONS
from .sambar_rasam_kuzhambu_taxonomy import SAMBAR_CLASSES, RASAM_CLASSES, KUZHAMBU_CLASSES, LIQUID_STEW_METADATA
from .vegetables_taxonomy import VEGETABLE_PREPARATION_TYPES, SPECIFIC_PORIYAL_CLASSES, SPECIFIC_KOOTU_CLASSES, VEGETABLE_METADATA
from .chutney_taxonomy import CHUTNEY_CLASSES, CHUTNEY_DATASET_ANNOTATIONS, ChutneyVisualAttributes
from .non_veg_taxonomy import CHICKEN_CLASSES, MUTTON_CLASSES, FISH_CLASSES, SEAFOOD_CLASSES, EGG_CLASSES, NON_VEG_METADATA
from .meal_composition_taxonomy import BananaLeafMealComposition, BANANA_LEAF_STANDARD_TEMPLATE, MealComponentAnnotation
from .pan_indian_taxonomy import PAN_INDIAN_REGIONAL_TAXONOMY
from .international_taxonomy import INTERNATIONAL_CLASSES, INTERNATIONAL_BENCHMARKS
from .cooking_state_form import CookingMethod, FoodForm, IngredientPresence, IngredientAnnotation, DISH_INGREDIENT_BLUEPRINTS
