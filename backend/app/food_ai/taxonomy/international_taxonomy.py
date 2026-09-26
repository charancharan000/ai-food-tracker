"""
International Food Coverage Taxonomy
Global food categories with standard portion benchmarks and macro densities.
"""

from typing import List, Dict, Any

INTERNATIONAL_CLASSES: List[str] = [
    "Pizza",
    "Burger",
    "Pasta",
    "Spaghetti",
    "Lasagna",
    "Sushi",
    "Ramen",
    "Tacos",
    "Burrito",
    "Steak",
    "Salad",
    "Sandwich",
    "Hot Dog",
    "Fried Chicken",
    "Fish and Chips",
    "Pancakes",
    "Waffles",
    "Cereal",
    "Oatmeal",
    "French Fries",
    "Nachos",
    "Wraps"
]

INTERNATIONAL_BENCHMARKS: Dict[str, Dict[str, Any]] = {
    "Pizza": {
        "calories_per_100g": 266,
        "protein_per_100g": 11.4,
        "carbs_per_100g": 33.3,
        "fat_per_100g": 9.8,
        "typical_slice_weight_g": 107
    },
    "Burger": {
        "calories_per_100g": 254,
        "protein_per_100g": 13.0,
        "carbs_per_100g": 24.0,
        "fat_per_100g": 12.0,
        "typical_burger_weight_g": 220
    },
    "Sushi": {
        "calories_per_100g": 143,
        "protein_per_100g": 5.8,
        "carbs_per_100g": 24.5,
        "fat_per_100g": 2.1,
        "typical_roll_weight_g": 180
    },
    "Steak": {
        "calories_per_100g": 271,
        "protein_per_100g": 25.0,
        "carbs_per_100g": 0.0,
        "fat_per_100g": 19.0,
        "typical_steak_weight_g": 225
    }
}
