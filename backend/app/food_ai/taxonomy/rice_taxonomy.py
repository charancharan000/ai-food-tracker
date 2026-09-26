"""
Tamil Rice Dataset Taxonomy
Covers traditional plain, variety, and tempered rice dishes.
"""

from typing import List, Dict, Any

TAMIL_RICE_CLASSES: List[str] = [
    "White Rice",
    "Brown Rice",
    "Red Rice",
    "Hand-Pounded Rice",
    "Seeraga Samba Rice",
    "Ghee Rice",
    "Kuska",
    "Pulao",
    "Vegetable Pulao",
    "Lemon Rice",
    "Tomato Rice",
    "Coconut Rice",
    "Curd Rice",
    "Thayir Sadam",
    "Tamarind Rice",
    "Puliyodarai",
    "Mango Rice",
    "Mint Rice",
    "Coriander Rice",
    "Sesame Rice",
    "Sambar Rice",
]

RICE_VARIETIES_METADATA: Dict[str, Dict[str, Any]] = {
    "White Rice": {
        "glycemic_index": "High (70-75)",
        "calories_per_100g_cooked": 130,
        "standard_serving_g": 200,
        "texture": "Fluffy, separated grains or softly mashed for rasam/curd"
    },
    "Seeraga Samba Rice": {
        "glycemic_index": "Medium (60-65)",
        "calories_per_100g_cooked": 140,
        "standard_serving_g": 220,
        "aroma": "Fragrant small-grain traditional Tamil rice used in Dindigul biryani"
    },
    "Curd Rice": {
        "glycemic_index": "Medium (55-60)",
        "calories_per_100g_cooked": 142,
        "protein_per_100g": 3.8,
        "fat_per_100g": 4.5,
        "standard_serving_g": 220,
        "tempering": "Mustard seeds, green chillies, curry leaves, ginger, pomegranate/grapes"
    },
    "Puliyodarai": {
        "glycemic_index": "Medium-High",
        "calories_per_100g_cooked": 185,
        "standard_serving_g": 200,
        "characteristics": "Tamarind paste cooked with sesame oil, roasted peanuts, chana dal, fenugreek powder"
    }
}
