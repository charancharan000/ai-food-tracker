"""
South Indian Vegetables Taxonomy
Covers dry sauteed vegetables (poriyal/thoran), lentil-vegetable stews (kootu), and mixed vegetable preparations (avial).
"""

from typing import List, Dict, Any

VEGETABLE_PREPARATION_TYPES: List[str] = [
    "Poriyal",
    "Kootu",
    "Avial",
    "Thoran",
    "Keerai Masiyal",
    "Keerai Kootu",
]

SPECIFIC_PORIYAL_CLASSES: List[str] = [
    "Beans Poriyal",
    "Carrot Poriyal",
    "Beetroot Poriyal",
    "Cabbage Poriyal",
    "Potato Poriyal",
    "Brinjal Poriyal",
    "Ladies Finger Poriyal",
    "Cauliflower Poriyal",
    "Drumstick Poriyal",
]

SPECIFIC_KOOTU_CLASSES: List[str] = [
    "Chow Chow Kootu",
    "Pumpkin Kootu",
    "Snake Gourd Kootu",
]

VEGETABLE_METADATA: Dict[str, Dict[str, Any]] = {
    "Avial": {
        "vegetables": ["Raw Banana", "Elephant Yam", "Carrot", "Beans", "Drumstick", "Pumpkin"],
        "base": "Coarsely ground fresh coconut, green chillies, cumin seeds, sour curd, finished with raw coconut oil and curry leaves",
        "calories_per_100g": 115,
        "fat_per_100g": 7.2,
        "fiber_per_100g": 3.8
    },
    "Beans Poriyal": {
        "vegetables": ["Finely chopped French Green Beans"],
        "tempering": "Mustard, urad dal, dried red chillies, fresh grated coconut",
        "calories_per_100g": 68,
        "fiber_per_100g": 3.2
    },
    "Chow Chow Kootu": {
        "vegetables": ["Chayote squash (Chow Chow)", "Split moong dal or chana dal"],
        "tempering": "Coconut-cumin paste with mustard tempering",
        "calories_per_100g": 78,
        "protein_per_100g": 3.5
    }
}
