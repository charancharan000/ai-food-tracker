"""
Hard-Negative Mining & Direct Pairwise Discriminator Engine
Implements Sections 6, 8, 10, 12, 14, 15, and 17 of Part 3.
Generates balanced hard-negative training batches and applies visual boundary tests.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class HardNegativeBatchSample(BaseModel):
    sample_id: str
    target_class: str
    confusing_negative_class: str
    discriminative_test_name: str
    negative_image_type: str
    key_visual_contrast: str

# =============================================================================
# SECTION 6, 8, 12, 14, 15, 17 — HARD NEGATIVE TEST BATTERY
# =============================================================================

class HardNegativeEngine:
    @staticmethod
    def get_idli_hard_negatives() -> List[Dict[str, str]]:
        return [
            {"negative": "dhokla", "reason": "Yellow-sugar sponge cubes with mustard seeds; test porosity and sugar sheen vs fermented rice crumb."},
            {"negative": "paniyaram", "reason": "Spherical solid fritter with browned tawa crust; test spherical geometry vs convex lens disc."},
            {"negative": "steamed_modak", "reason": "Fluted tear-drop shape with sweet jaggery-coconut center; test apex fluting and sweetness."},
            {"negative": "steamed_rice_cake", "reason": "Dense East Asian sticky rice block; test elastic gelatinized starch vs aerated urad crumb."},
            {"negative": "appam", "reason": "Bowl-shaped soft fermented spongy center with crispy paper-thin lacy frill border."},
            {"negative": "white_bread_bun", "reason": "Baked yeast wheat crumb with golden-brown crust; test yeast bread aroma and gluten cell walls."},
            {"negative": "mochi", "reason": "Ultra-glutinous smooth chewy rice paste; test surface elasticity vs porous crumb."}
        ]

    @staticmethod
    def get_sambar_hard_negatives() -> List[Dict[str, str]]:
        return [
            {"negative": "dal_tadka", "reason": "Pure yellow toor dal with garlic-cumin ghee tempering; test absence of tamarind and sambar powder."},
            {"negative": "tomato_dal", "reason": "Andhra tomato pappu; thick mashed dal with stewed tomato chunks, no drumstick/shallots."},
            {"negative": "rasam", "reason": "Watery clear herbal broth with pepper foam; test viscosity and opacity (rasam is translucent)."},
            {"negative": "tomato_gravy_salna", "reason": "Coconut-fennel poppy seed meat/veg gravy; test coconut emulsion vs tamarind lentil broth."},
            {"negative": "vegetable_curry", "reason": "Thick dry/semi-dry vegetable masala; test liquid stew level."},
            {"negative": "kuzhambu", "reason": "Tamarind-oil broth without toor dal base (e.g. Vatha Kuzhambu); test lentil suspension density."},
            {"negative": "clear_soup", "reason": "Western strained vegetable or chicken broth; test absence of mustard-curry leaf tempering."}
        ]

    @staticmethod
    def get_dosa_hard_negatives() -> List[Dict[str, str]]:
        return [
            {"negative": "french_crepe", "reason": "Pliable soft wheat/milk crepe; test concentric griddle ridges and brittle roasted blister rim."},
            {"negative": "omelette", "reason": "Whisked egg sheet; test protein coagulate texture, yellow color, and absence of fermented batter spiral."},
            {"negative": "laccha_paratha", "reason": "Wheat dough multi-layer flatbread; test dough thickness and absence of crisp lacy edges."},
            {"negative": "roti_chapati", "reason": "Dry ungreased whole wheat puffed disc; test absence of griddle oil and golden blisters."},
            {"negative": "pancake", "reason": "Thick fluffy baking-powder cake; test thickness (> 8mm vs dosa < 2mm) and syrup sweetness."},
            {"negative": "plain_vs_paper_roast", "reason": "Thickness test: paper roast is ultra-thin (< 0.8mm) brittle glass cone vs standard dosa (1.5-2mm)."},
            {"negative": "plain_vs_ghee_roast", "reason": "Gloss test: high cow ghee surface sheen and uniform mahogany roast vs moderate sesame oil."},
            {"negative": "rava_dosa_vs_plain_dosa", "reason": "Texture test: rava dosa is an open perforated net lattice with cracked peppercorns and onions."},
            {"negative": "neer_dosa_vs_thin_dosa", "reason": "Color test: neer dosa is chalk pure white with zero browning, folded into soft quadrants."},
            {"negative": "set_dosa_vs_small_pancakes", "reason": "Fermentation test: set dosa has thousands of micro spongy pores (poha fermentation) with zero sugar."}
        ]

    @staticmethod
    def get_vada_hard_negatives() -> List[Dict[str, str]]:
        return [
            {"negative": "mysore_bonda", "reason": "Solid spherical globe with no central hole; genus 0 vs genus 1 topology."},
            {"negative": "onion_pakoda", "reason": "Jagged amorphous cluster of besan-coated onion ribbons vs smooth circular disc."},
            {"negative": "sweet_doughnut", "reason": "Yeast/sugar fried wheat dough with glaze; test savory black peppercorns and urad dal crumb."},
            {"negative": "falafel", "reason": "Crushed chickpea ball with parsley/cumin; test green interior and absence of whole urad dal dough."},
            {"negative": "bread_fritter", "reason": "Besan-coated white bread triangle; test internal spongy bread matrix."}
        ]

    @staticmethod
    def get_rice_ten_pairwise_datasets() -> List[Dict[str, Any]]:
        """
        SECTION 17: Ten Direct Pair Datasets for Rice Confusion
        """
        return [
            {
                "pair_id": "pair_01_biryani_vs_fried_rice",
                "class_a": "South Indian Biryani",
                "class_b": "Indo-Chinese Fried Rice",
                "key_discriminator": "Whole spices (cloves, cardamom), bone-in meat, meat juices vs dry wok-tossed grains, diced spring onions, soy sauce."
            },
            {
                "pair_id": "pair_02_biryani_vs_pulao",
                "class_a": "Biryani",
                "class_b": "Pulao",
                "key_discriminator": "Deep spicy yogurt-marinated rice with fried onions vs single-pot pale aromatic whole-spice rice cooked in broth."
            },
            {
                "pair_id": "pair_03_biryani_vs_kuska",
                "class_a": "Meat Biryani",
                "class_b": "Kuska (Empty Biryani Rice)",
                "key_discriminator": "Presence of discrete cooked meat/chicken cuts vs entirely empty spiced biryani grains."
            },
            {
                "pair_id": "pair_04_biryani_vs_ghee_rice",
                "class_a": "Biryani",
                "class_b": "Ghee Rice",
                "key_discriminator": "Reddish-amber masala-absorbed grains vs ivory white grains glistening with cow ghee, cashews, and raisins."
            },
            {
                "pair_id": "pair_05_ghee_rice_vs_kuska",
                "class_a": "Ghee Rice",
                "class_b": "Kuska",
                "key_discriminator": "Ivory white color with fried cashews vs orange-brown spiced tomato-onion rice."
            },
            {
                "pair_id": "pair_06_lemon_rice_vs_tamarind_rice",
                "class_a": "Lemon Rice (Chitranna)",
                "class_b": "Tamarind Rice (Puliyodarai)",
                "key_discriminator": "Bright canary yellow hue (turmeric + lemon) vs deep dark maroon-brown tamarind paste coating."
            },
            {
                "pair_id": "pair_07_lemon_rice_vs_mango_rice",
                "class_a": "Lemon Rice",
                "class_b": "Raw Mango Rice (Manga Sadam)",
                "key_discriminator": "Smooth turmeric-dyed grains with lemon juice vs pale yellowish-white rice studded with grated green raw mango shreds."
            },
            {
                "pair_id": "pair_08_curd_rice_vs_plain_rice",
                "class_a": "Curd Rice (Thayir Sadam)",
                "class_b": "Plain Steamed Rice",
                "key_discriminator": "Creamy mashed emulsion with tempered black mustard seeds, green chillies, ginger vs dry separable white grains."
            },
            {
                "pair_id": "pair_09_sambar_rice_vs_rice_plus_sambar",
                "class_a": "Pre-mixed Sambar Rice (Bisibelebath / Sambar Sadam)",
                "class_b": "Plain Rice with Sambar Poured on Side",
                "key_discriminator": "Homogeneous orange lentil-rice mash cooked together vs separate white rice mound with independent sambar pool."
            },
            {
                "pair_id": "pair_10_tomato_rice_vs_biryani",
                "class_a": "Tomato Rice (Thakkali Sadam)",
                "class_b": "Biryani",
                "key_discriminator": "Bright red-orange tomato-shallot tempered rice without meat, mint, saffron, or whole biryani spices."
            }
        ]

    @staticmethod
    def resolve_chutney_uncertainty(
        color_detected: str,
        coconut_confidence: float,
        peanut_confidence: float
    ) -> Dict[str, Any]:
        """
        SECTION 10: Chutney Uncertainty Protocol
        Never hallucinate ingredients from color alone.
        """
        if color_detected.lower() == "white":
            if coconut_confidence >= 0.88 and peanut_confidence < 0.30:
                return {"classification": "White Coconut Chutney", "uncertain": False, "confidence": coconut_confidence}
            else:
                return {
                    "classification": "White Chutney",
                    "status_text": "white chutney detected — exact type uncertain",
                    "uncertain": True,
                    "possible_types": ["White Coconut Chutney", "Peanut / Groundnut Chutney", "Sesame Chutney"],
                    "confidence": 0.68
                }
        elif color_detected.lower() == "red":
            return {
                "classification": "Red Chutney",
                "status_text": "red chutney detected — exact type uncertain",
                "uncertain": True,
                "possible_types": ["Tomato Kaara Chutney", "Onion Red Chilli Chutney", "Garlic Red Chutney"],
                "confidence": 0.70
            }
        return {"classification": "Chutney", "status_text": "Chutney detected", "uncertain": True, "confidence": 0.60}
