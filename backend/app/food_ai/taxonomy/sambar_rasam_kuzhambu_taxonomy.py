"""
Sambar, Rasam, and Kuzhambu Taxonomy
Covers South Indian lentil stews, digestive broths, and tamarind-based gravies.
"""

from typing import List, Dict, Any

SAMBAR_CLASSES: List[str] = [
    "Sambar",
    "Hotel Sambar",
    "Drumstick Sambar",
    "Onion Sambar",
    "Arachuvitta Sambar",
]

RASAM_CLASSES: List[str] = [
    "Tomato Rasam",
    "Pepper Rasam",
    "Jeera Rasam",
    "Garlic Rasam",
    "Lemon Rasam",
    "Pineapple Rasam",
]

KUZHAMBU_CLASSES: List[str] = [
    "Vatha Kuzhambu",
    "Puli Kuzhambu",
    "Kara Kuzhambu",
    "Mor Kuzhambu",
    "Ennai Kathirikai Kuzhambu",
    "Vendakkai Kuzhambu",
    "Fish Kuzhambu",
    "Chicken Kuzhambu",
]

LIQUID_STEW_METADATA: Dict[str, Dict[str, Any]] = {
    "Hotel Sambar": {
        "consistency": "Semi-thick, lightly sweet with jaggery and freshly ground spices",
        "lentil_base": "Toor dal + yellow moong dal",
        "calories_per_100g": 72,
        "protein_per_100g": 3.4
    },
    "Tomato Rasam": {
        "consistency": "Thin, translucent spiced broth with tempered mustard, cumin, crushed pepper, garlic",
        "calories_per_100g": 30,
        "protein_per_100g": 1.1
    },
    "Vatha Kuzhambu": {
        "consistency": "Thick, dark-brown tangy tamarind reduction with sundakkai / manathakkali vathal and sesame oil",
        "calories_per_100g": 120,
        "fat_per_100g": 6.8
    },
    "Mor Kuzhambu": {
        "consistency": "Creamy yellowish buttermilk and coconut gravy with ash gourd or okra",
        "calories_per_100g": 65,
        "protein_per_100g": 2.8
    }
}
