"""
Tamil Nadu Food Taxonomy
Fine-grained label taxonomy covering traditional breakfast, tiffin, and street food.
"""

from typing import Dict, List, Any

TAMIL_NADU_TIFFIN_TAXONOMY: Dict[str, List[str]] = {
    "Idli": [
        "Idli",
        "Mini Idli",
        "Kanchipuram Idli",
        "Ragi Idli",
        "Millet Idli",
    ],
    "Dosa": [
        "Plain Dosa",
        "Masala Dosa",
        "Ghee Dosa",
        "Mysore Masala Dosa",
        "Onion Dosa",
        "Tomato Dosa",
        "Podi Dosa",
        "Ghee Podi Dosa",
        "Rava Dosa",
        "Onion Rava Dosa",
        "Paper Roast",
        "Set Dosa",
        "Kal Dosa",
        "Neer Dosa",
        "Egg Dosa",
        "Cheese Dosa",
        "Paneer Dosa",
        "Chicken Dosa",
    ],
    "Vada": [
        "Medu Vada",
        "Ulundhu Vada",
        "Masala Vada",
        "Paruppu Vada",
        "Keerai Vada",
        "Rasa Vada",
        "Thayir Vada",
    ],
    "Pongal": [
        "Ven Pongal",
        "Ghee Pongal",
        "Sweet Pongal",
    ],
    "Upma": [
        "Rava Upma",
        "Vegetable Upma",
        "Semiya Upma",
        "Aval Upma",
        "Millet Upma",
    ],
    "Other Tiffin": [
        "Kuzhi Paniyaram",
        "Masala Paniyaram",
        "Sweet Paniyaram",
        "Adai",
        "Ragi Adai",
        "Puttu",
        "Appam",
        "Idiyappam",
        "Poori",
        "Poori Masala",
        "Parotta",
        "Bun Parotta",
        "Kothu Parotta",
        "Egg Kothu Parotta",
        "Chicken Kothu Parotta",
        "Mutton Kothu Parotta",
    ],
}

ALL_TAMIL_TIFFIN_CLASSES: List[str] = [
    item for sublist in TAMIL_NADU_TIFFIN_TAXONOMY.values() for item in sublist
]

TIFFIN_METADATA: Dict[str, Dict[str, Any]] = {
    "Masala Dosa": {
        "primary_grain": "Fermented Rice & Urad Dal",
        "filling": "Spiced Potato Masala with Mustard & Curry Leaves",
        "typical_weight_range_g": (140, 240),
        "standard_weight_g": 180,
        "cooking_method": "Pan Fried with Ghee/Oil",
        "accompaniments": ["Sambar", "Coconut Chutney", "Tomato Chutney"]
    },
    "Ven Pongal": {
        "primary_grain": "Raw Rice & Moong Dal",
        "tempering": "Ghee, Black Pepper, Cumin, Ginger, Cashews, Curry Leaves",
        "typical_weight_range_g": (150, 280),
        "standard_weight_g": 200,
        "cooking_method": "Pressure Cooked & Ghee Tempered",
        "accompaniments": ["Sambar", "Coconut Chutney", "Medu Vada"]
    },
    "Medu Vada": {
        "primary_grain": "Whole Urad Dal Batter",
        "spices": "Whole Black Peppercorns, Green Chillies, Ginger, Curry Leaves",
        "typical_weight_range_g": (40, 75),
        "standard_weight_g": 55,
        "cooking_method": "Deep Fried Donut-Shaped Fritter",
        "accompaniments": ["Sambar", "Coconut Chutney"]
    },
    "Kothu Parotta": {
        "primary_grain": "Shredded Maida Parotta",
        "protein_options": ["Egg", "Chicken", "Mutton", "Vegetable"],
        "typical_weight_range_g": (250, 420),
        "standard_weight_g": 320,
        "cooking_method": "Griddled, Chopped with Metal Blades on Flat Top with Salna",
        "accompaniments": ["Chicken Salna", "Onion Raita"]
    }
}
