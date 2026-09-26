"""
Hard Negative Mining Pairs & Disambiguation Rules
Defines confusing food pairs that require specialized contrastive loss / hard example mining.
"""

from typing import List, Dict
from pydantic import BaseModel, Field

class ConfusingPair(BaseModel):
    class_a: str
    class_b: str
    visual_distinction: str
    discriminative_features: List[str]

CONFUSING_FOOD_PAIRS: List[ConfusingPair] = [
    ConfusingPair(
        class_a="Idli",
        class_b="Dhokla",
        visual_distinction="Dhokla is bright yellow with mustard-curry leaf tadka and porous sponge texture; Idli is pure white fermented rice-urad steamed cake.",
        discriminative_features=["Color (yellow vs white)", "Tadka seeds on surface", "Coriander garnish"]
    ),
    ConfusingPair(
        class_a="Dosa",
        class_b="Crepe",
        visual_distinction="Dosa has fermentation porous micro-holes, crisp golden roasted rim; crepe is smooth wheat/egg-based pliable pancake.",
        discriminative_features=["Micro-pores", "Golden roasting gradient", "Served with sambar/chutney"]
    ),
    ConfusingPair(
        class_a="Vada",
        class_b="Bonda",
        visual_distinction="Medu Vada is donut-shaped with central hole and crispy crust; Bonda is spherical with gram flour batter coating.",
        discriminative_features=["Central hole geometry", "Crust texture", "Interior urad grain vs spiced potato"]
    ),
    ConfusingPair(
        class_a="Biryani",
        class_b="Chicken Fried Rice",
        visual_distinction="Biryani grains are coated in deep spiced oil/gravy with whole spices and meat chunks; Fried Rice has dry separated grains with visible spring onions and scrambled egg.",
        discriminative_features=["Gravy glaze on rice", "Whole spices (cardamom/clove/bayleaf)", "Spring onion flecks in fried rice"]
    ),
    ConfusingPair(
        class_a="Biryani",
        class_b="Pulao",
        visual_distinction="Pulao is lighter in color, cooked by absorption with whole vegetables or mild spices; Biryani is layered dum cooked with intense masala marinade.",
        discriminative_features=["Color intensity", "Spice marinade density", "Meat caramelization"]
    ),
    ConfusingPair(
        class_a="Biryani",
        class_b="Kuska",
        visual_distinction="Kuska is empty biryani-flavored spiced rice cooked in meat broth without meat pieces; Biryani must have protein pieces.",
        discriminative_features=["Presence of meat/bone pieces"]
    ),
    ConfusingPair(
        class_a="Sambar",
        class_b="Dal Tadka",
        visual_distinction="Sambar is thinner with dark reddish-brown tamarind hue and mixed vegetables (drumstick/shallots); Dal Tadka is golden yellow puree with ghee cumin tadka.",
        discriminative_features=["Tamarind reddish hue", "Visible chunky vegetables", "Coriander-cumin seed powder"]
    ),
    ConfusingPair(
        class_a="Rasam",
        class_b="Thin Gravy / Salna",
        visual_distinction="Rasam has translucent red/pepper broth with floating coriander and crushed garlic; Salna is opaque, emulsified coconut-poppy seed gravy.",
        discriminative_features=["Broth translucency", "Oil sheen layer", "Emulsification"]
    ),
    ConfusingPair(
        class_a="Paneer",
        class_b="Tofu",
        visual_distinction="Paneer has milky white, dense crumbly texture; Tofu has slightly porous, gelatinous/firm curd structure with sharp cut edges.",
        discriminative_features=["Surface moisture", "Porous grain", "Color warmth"]
    ),
    ConfusingPair(
        class_a="Ven Pongal",
        class_b="Rava Upma",
        visual_distinction="Pongal has glossy ghee sheen with visible yellow moong dal, whole black peppercorns and split cashews; Upma has separated semolina granule texture.",
        discriminative_features=["Whole peppercorns", "Moong dal grains", "Semolina granulate vs rice-dal mash"]
    ),
    ConfusingPair(
        class_a="Parotta",
        class_b="Paratha",
        visual_distinction="South Indian Parotta has spiral multi-layered flaky swirls of kneaded maida dough; North Indian Paratha is flat rolled whole wheat flatbread, often stuffed.",
        discriminative_features=["Spiral concentric layers", "Flaky puff vs flat bread", "Wheat color vs maida pale gold"]
    )
]
