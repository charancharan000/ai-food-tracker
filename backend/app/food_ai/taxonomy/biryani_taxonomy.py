"""
Biryani Fine-Grained Dataset Taxonomy
Specialized taxonomy to prevent common confusion between biryani styles, pulao, and fried rice.
"""

from typing import List, Dict, Any

BIRYANI_PROTEIN_CLASSES: List[str] = [
    "Chicken Biryani",
    "Mutton Biryani",
    "Egg Biryani",
    "Fish Biryani",
    "Prawn Biryani",
    "Vegetable Biryani",
]

BIRYANI_REGIONAL_STYLES: List[str] = [
    "Ambur Biryani",
    "Vaniyambadi Biryani",
    "Dindigul Biryani",
    "Thalappakatti-style Biryani",
    "Chettinad Biryani",
    "Hyderabadi Biryani",
    "Malabar Biryani",
]

BIRYANI_HARD_NEGATIVES: List[str] = [
    "Chicken Fried Rice",
    "Mutton Fried Rice",
    "Pulao",
    "Kuska",
    "Ghee Rice",
    "Jeera Rice",
]

BIRYANI_DISTINCTIONS: Dict[str, Dict[str, Any]] = {
    "Ambur Biryani": {
        "rice_type": "Seeraga Samba (small grain)",
        "meat_marination": "Curd, tomato, red chilli paste, mint, coriander",
        "dum_style": "Woodfire dum cooking without whole garam masala dominating",
        "accompaniment": "Ennai Kathirikai (brinjal gravy / dalcha) + Onion Raita"
    },
    "Dindigul Thalappakatti": {
        "rice_type": "Seeraga Samba (Parakkum Sithira)",
        "key_notes": "Tangy curd marinade, tender bone-in mutton, distinct pepper and green chilli heat",
        "color_profile": "Dark golden brown to olive-brown"
    },
    "Hyderabadi Biryani": {
        "rice_type": "Long-grain Aged Basmati",
        "dum_style": "Kacchi Dum (raw meat layered with half-cooked basmati)",
        "color_profile": "Layered white, saffron yellow, and spiced orange-brown",
        "accompaniment": "Mirchi ka Salan + Burani Raita"
    },
    "Chicken Fried Rice (Hard Negative)": {
        "rice_type": "Long grain or medium grain wok-tossed",
        "distinguishing_visuals": "Diced spring onions, shredded carrots, scrambled egg bits, lack of deep spiced gravy coating on rice"
    }
}
