"""
South Indian Non-Vegetarian Food Taxonomy
Specialized taxonomy for chicken, mutton, fish, seafood, and egg preparations.
"""

from typing import List, Dict, Any

CHICKEN_CLASSES: List[str] = [
    "Chicken 65",
    "Chicken Fry",
    "Chicken Pepper Fry",
    "Chicken Sukka",
    "Chicken Chukka",
    "Chicken Chettinad",
    "Chicken Curry",
    "Chicken Gravy",
    "Chicken Roast",
    "Chicken Tikka",
    "Chicken Kebab",
    "Chicken Lollipop",
    "Chicken Breast",
    "Chicken Leg",
    "Chicken Wings",
]

MUTTON_CLASSES: List[str] = [
    "Mutton Curry",
    "Mutton Sukka",
    "Mutton Chukka",
    "Mutton Fry",
    "Mutton Kola",
    "Mutton Biryani",
]

FISH_CLASSES: List[str] = [
    "Fish Fry",
    "Fish Curry",
    "Meen Kuzhambu",
    "Meen Varuval",
    "Fish Tawa Fry",
    "Fish Roast",
]

SEAFOOD_CLASSES: List[str] = [
    "Prawn Fry",
    "Prawn Masala",
    "Prawn Curry",
    "Crab Curry",
    "Crab Masala",
    "Squid Fry",
    "Squid Curry",
]

EGG_CLASSES: List[str] = [
    "Boiled Egg",
    "Half Boiled Egg",
    "Fried Egg",
    "Omelette",
    "Masala Omelette",
    "Egg Podimas",
    "Egg Bhurji",
    "Egg Curry",
]

NON_VEG_METADATA: Dict[str, Dict[str, Any]] = {
    "Chicken 65": {
        "visual_signature": "Vibrant deep red/orange crisp boneless or bone-in cubes, fried curry leaves, slit green chillies",
        "cooking_method": "Deep Fried after spiced cornstarch/rice flour marination",
        "calories_per_100g": 240,
        "protein_per_100g": 22.5,
        "fat_per_100g": 14.8
    },
    "Chicken Chettinad": {
        "visual_signature": "Dark, deeply aromatic brown gravy coated with freshly roasted kalpasi (black stone flower), star anise, peppercorns",
        "cooking_method": "Slow simmered braised chicken",
        "calories_per_100g": 185,
        "protein_per_100g": 18.0,
        "fat_per_100g": 11.5
    },
    "Meen Kuzhambu": {
        "visual_signature": "Tangy red-orange tamarind fish stew with shallots and garlic",
        "cooking_method": "Clay pot slow simmered",
        "calories_per_100g": 125,
        "protein_per_100g": 15.5,
        "fat_per_100g": 5.8
    },
    "Masala Omelette": {
        "visual_signature": "Golden round egg patty embedded with minced onions, green chillies, coriander, turmeric",
        "cooking_method": "Pan fried in oil or butter",
        "calories_per_100g": 178,
        "protein_per_100g": 12.0,
        "fat_per_100g": 13.5
    }
}
