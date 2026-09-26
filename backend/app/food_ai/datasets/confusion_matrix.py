"""
Visual Confusion Matrix & Pairwise Disambiguation Engine
Implements Section 30 of Part 2.
Contains explicit discriminative feature extractors for all 26 confusing pairs.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class ConfusionPairSpec(BaseModel):
    pair_id: str
    class_a: str
    class_b: str
    risk_level: str = Field(default="high", description="high, critical, moderate")
    discriminative_features: List[str]
    disambiguation_test: str
    primary_differentiator_a: str
    primary_differentiator_b: str

# 26 Explicit Pairwise Visual Confusion Resolvers
CONFUSION_MATRIX_REGISTRY: Dict[str, ConfusionPairSpec] = {
    "idli_vs_rava_idli_vs_dhokla": ConfusionPairSpec(
        pair_id="idli_vs_rava_idli_vs_dhokla",
        class_a="Plain Idli",
        class_b="Rava Idli / Dhokla",
        risk_level="critical",
        discriminative_features=[
            "color_chroma: snow white vs golden buff yellow vs vibrant lemon yellow",
            "surface_texture: micro-porous sponge vs coarse semolina grains vs aerated sponge cubes",
            "inclusions: pristine no specks vs split cashew + mustard + carrot vs black mustard + green chilli + sesame"
        ],
        disambiguation_test="Evaluate central inclusion (cashew = rava idli), cube cutting and sugar syrup sheen (dhokla), or pristine white lens shape (plain idli).",
        primary_differentiator_a="Pure snow white color, lens disc shape, zero mustard/carrot specks.",
        primary_differentiator_b="Granular crumb with split cashew and grated carrot (Rava Idli) or cubic yellow sponge (Dhokla)."
    ),
    "dosa_vs_crepe": ConfusionPairSpec(
        pair_id="dosa_vs_crepe",
        class_a="South Indian Dosa",
        class_b="French Crepe",
        risk_level="high",
        discriminative_features=[
            "griddle_spiral: concentric circular batter trails from flat ladle vs smooth spun batter",
            "edge_texture: brittle lacy fried crust vs soft pliable pale rim",
            "accompaniment: chutney and sambar vs sweet spreads, fruits, or cheese"
        ],
        disambiguation_test="Check for concentric spiral spreading patterns and brittle golden blisters.",
        primary_differentiator_a="Concentric circular ridges, brittle golden crust, oil/ghee aroma.",
        primary_differentiator_b="Smooth uniform pale skin, pliable velvety fold without brittle crispness."
    ),
    "medu_vada_vs_bonda": ConfusionPairSpec(
        pair_id="medu_vada_vs_bonda",
        class_a="Medu Vada",
        class_b="Mysore Bonda / Aloo Bonda",
        risk_level="critical",
        discriminative_features=[
            "topology: toroidal ring with central open hole vs solid spherical globe",
            "exterior: blistered crispy lentil shell vs smooth golden batter coat"
        ],
        disambiguation_test="Detect topological genus 1 (closed central aperture) vs solid sphere genus 0.",
        primary_differentiator_a="Central aperture hole with crispy toroidal donut boundary.",
        primary_differentiator_b="Solid spherical globe with no hole; smooth or yellow besan crust."
    ),
    "paruppu_vada_vs_pakoda": ConfusionPairSpec(
        pair_id="paruppu_vada_vs_pakoda",
        class_a="Paruppu Vada (Masala Vada)",
        class_b="Onion Pakoda",
        risk_level="high",
        discriminative_features=[
            "shape: cohesive flattened circular disc vs amorphous clustered tangled fritter",
            "texture: densely packed whole and split yellow chana dal vs besan-coated onion ribbons"
        ],
        disambiguation_test="Verify flattened disc geometry and visible whole uncrushed chana dal grains.",
        primary_differentiator_a="Flattened circular disc with visible yellow chana dal pebbles and fennel.",
        primary_differentiator_b="Irregular jagged cluster of extruded onion strands in fried chickpea batter."
    ),
    "pongal_vs_upma": ConfusionPairSpec(
        pair_id="pongal_vs_upma",
        class_a="Ven Pongal",
        class_b="Rava Upma",
        risk_level="critical",
        discriminative_features=[
            "inclusions: whole black peppercorns and split golden cashews vs mustard seeds and brown urad dal gems",
            "texture: soft burst rice-moong dal mash vs individual granular semolina grains",
            "sheen: high liquid ghee sheen vs matte semi-dry crumb"
        ],
        disambiguation_test="Extract black spherical inclusions. Whole peppercorns (4-5mm) identify Ven Pongal. Tiny black mustard seeds (< 1.5mm) identify Rava Upma.",
        primary_differentiator_a="Large whole black peppercorns, cumin, split cashews, glossy creamy rice mash.",
        primary_differentiator_b="Fine semolina grains, micro mustard seeds, browned urad dal, green chillies."
    ),
    "pongal_vs_kichdi": ConfusionPairSpec(
        pair_id="pongal_vs_kichdi",
        class_a="Ven Pongal",
        class_b="North Indian Khichdi",
        risk_level="high",
        discriminative_features=[
            "spice_coloring: pale golden yellow without red chilli/turmeric overload vs deep turmeric yellow with vegetables",
            "fat_sheen: heavy pure ghee emulsion vs light ghee/oil with hing tempering"
        ],
        disambiguation_test="Confirm black peppercorns + cashew signature and pure South Indian breakfast context.",
        primary_differentiator_a="Heavy ghee sheen, whole peppercorns, cashews, served with sambar & chutney.",
        primary_differentiator_b="Mixed with diced potatoes, peas, turmeric, served with papad, curd, pickle."
    ),
    "sambar_vs_dal": ConfusionPairSpec(
        pair_id="sambar_vs_dal",
        class_a="South Indian Sambar",
        class_b="North Indian Dal Tadka / Dal Fry",
        risk_level="high",
        discriminative_features=[
            "acidity_and_color: tamarind-infused reddish orange broth vs turmeric-cumin yellow stew",
            "vegetables: whole shallots, drumsticks, brinjal vs purely mashed lentils with garlic tadka",
            "curry_leaves: abundant fried green curry leaves and mustard seeds"
        ],
        disambiguation_test="Detect tamarind translucency, drumstick cuts, and shallot inclusions.",
        primary_differentiator_a="Tangy tamarind broth, shallots, drumstick, sambar powder, curry leaves.",
        primary_differentiator_b="Thick yellow toor/moong mash, ghee garlic cumin tempering, dried red whole chilli."
    ),
    "sambar_vs_rasam": ConfusionPairSpec(
        pair_id="sambar_vs_rasam",
        class_a="Sambar",
        class_b="Rasam",
        risk_level="critical",
        discriminative_features=[
            "viscosity: medium-thick lentil suspension vs ultra-thin water-like herbal broth",
            "opacity: semi-opaque to opaque vs translucent clear broth with floating herbs"
        ],
        disambiguation_test="Measure opacity and surface froth; Rasam is watery with floating coriander and pepper foam.",
        primary_differentiator_a="Lentil-thickened body, diced vegetables, cooked shallots.",
        primary_differentiator_b="Watery spiced broth, heavy crushed black pepper, crushed garlic cloves, fresh coriander froth."
    ),
    "rasam_vs_soup": ConfusionPairSpec(
        pair_id="rasam_vs_soup",
        class_a="South Indian Rasam",
        class_b="Clear Tomato / Vegetable Soup",
        risk_level="high",
        discriminative_features=[
            "tempering: crackled black mustard seeds and curry leaves vs smooth strained broth",
            "aromatics: asafoetida, cumin, crushed garlic and black pepper vs herbs (parsley, thyme, croutons)"
        ],
        disambiguation_test="Check for floating mustard seeds, curry leaves, and crushed garlic flakes.",
        primary_differentiator_a="Mustard seed tempering, curry leaves, crushed pepper, garlic skins.",
        primary_differentiator_b="Smooth homogenous broth or cream base with western croutons or parsley."
    ),
    "poriyal_vs_stir_fry": ConfusionPairSpec(
        pair_id="poriyal_vs_stir_fry",
        class_a="South Indian Poriyal",
        class_b="Asian / Western Stir Fry",
        risk_level="moderate",
        discriminative_features=[
            "coconut: generous grated fresh white coconut shreds over dry vegetable vs cornstarch/soy sauce glaze",
            "tempering: black mustard seeds and split urad dal vs soy sauce or garlic-ginger stir fry"
        ],
        disambiguation_test="Confirm grated white coconut snow and absence of dark soy sauce.",
        primary_differentiator_a="Grated fresh coconut topping, mustard seeds, browned urad dal, dry texture.",
        primary_differentiator_b="Glossy soy or cornstarch glaze, wok char, sesame oil, bell pepper strips."
    ),
    "kootu_vs_dal": ConfusionPairSpec(
        pair_id="kootu_vs_dal",
        class_a="South Indian Kootu",
        class_b="Plain Dal",
        risk_level="moderate",
        discriminative_features=[
            "vegetable_ratio: equal or greater vegetable chunks (chow chow, pumpkin, cabbage) cooked in ground coconut-cumin paste vs lentil puree",
            "paste: visible coconut-cumin ground paste base"
        ],
        disambiguation_test="Detect large soft vegetable chunks bound with chana/moong dal and ground coconut paste.",
        primary_differentiator_a="Soft gourd/pumpkin pieces bound in coconut-cumin-chana dal gravy.",
        primary_differentiator_b="Homogenous cooked lentil broth without large gourd chunks or coconut paste."
    ),
    "biryani_vs_fried_rice": ConfusionPairSpec(
        pair_id="biryani_vs_fried_rice",
        class_a="South Indian Biryani",
        class_b="Indo-Chinese Fried Rice",
        risk_level="critical",
        discriminative_features=[
            "coloring: warm amber/brown/saffron steeped in meat marinade vs pale white rice with scattered soy/sauce specks",
            "grain_aroma_and_fat: ghee and rendered meat juices vs dry wok-tossed vegetable oil",
            "vegetable_cut: whole fried onions (birista) and whole spices vs machine-diced carrots, cabbage, and spring onions"
        ],
        disambiguation_test="Inspect for whole spices (cinnamon, cloves, star anise, cardamom) and bone-in meat cuts.",
        primary_differentiator_a="Spiced marinated rice, bone-in meat cuts, whole spices, fried onions.",
        primary_differentiator_b="Diced spring onions, cubed carrots, dry individual wok-tossed grains, no whole Indian spices."
    ),
    "biryani_vs_pulao": ConfusionPairSpec(
        pair_id="biryani_vs_pulao",
        class_a="Biryani",
        class_b="Pulao",
        risk_level="high",
        discriminative_features=[
            "masala_intensity: heavily spiced layered rice with yogurt marinade vs lightly aromatic whole-spice cooked rice",
            "layering: distinct meat gravy layer or deep spiced grain absorption vs single-pot uniform mild rice"
        ],
        disambiguation_test="Analyze spice color density and presence of rich masala coating around meat.",
        primary_differentiator_a="Deep reddish-brown or variegated saffron rice coated in rich spiced meat masala.",
        primary_differentiator_b="Pale white/yellow rice cooked in broth, whole cumin, mild cardamom, minimal gravy."
    ),
    "biryani_vs_kuska": ConfusionPairSpec(
        pair_id="biryani_vs_kuska",
        class_a="Meat Biryani",
        class_b="Kuska (Plain Biryani Rice)",
        risk_level="high",
        discriminative_features=[
            "meat_presence: physical bone-in chicken or mutton pieces present vs entirely plain spiced rice without meat cuts"
        ],
        disambiguation_test="Segment plate looking for chicken/mutton meat chunks; if absent, classify as Kuska.",
        primary_differentiator_a="Distinct bone-in or boneless cooked meat chunks embedded in rice.",
        primary_differentiator_b="Empty spiced biryani rice with zero meat pieces, cooked in meat stock or ghee."
    ),
    "ghee_rice_vs_kuska": ConfusionPairSpec(
        pair_id="ghee_rice_vs_kuska",
        class_a="Ghee Rice (Nei Sadam)",
        class_b="Kuska",
        risk_level="high",
        discriminative_features=[
            "color: ivory white or pale buttery cream vs reddish-amber spiced rice",
            "garnishes: golden fried cashews, raisins, and caramel onions vs biryani spice masala"
        ],
        disambiguation_test="Color thresholding: Ghee rice is ivory/white with cashews; Kuska is orange/brown spiced.",
        primary_differentiator_a="Ivory white grains glistening with ghee, fried cashews, golden raisins.",
        primary_differentiator_b="Orange-amber spiced rice cooked with tomato, onion, and biryani masala."
    ),
    "curd_rice_vs_plain_rice_plus_curd": ConfusionPairSpec(
        pair_id="curd_rice_vs_plain_rice_plus_curd",
        class_a="Tempered Curd Rice (Thayir Sadam)",
        class_b="Plain Rice with Curd on Side",
        risk_level="moderate",
        discriminative_features=[
            "homogeneity: soft mashed rice thoroughly emulsified with curd and milk vs separate white rice mound with liquid yogurt pool",
            "tempering: crackled black mustard seeds, chopped green chillies, ginger slivers, and curry leaves evenly distributed"
        ],
        disambiguation_test="Check for uniform mash and embedded mustard seed / ginger / chilli tempering.",
        primary_differentiator_a="Soft mashed creamy emulsion, tempered mustard seeds, ginger, green chillies.",
        primary_differentiator_b="Intact un-mashed rice grains with separate unmixed plain curd pool."
    ),
    "lemon_rice_vs_tamarind_rice": ConfusionPairSpec(
        pair_id="lemon_rice_vs_tamarind_rice",
        class_a="Lemon Rice (Chitranna)",
        class_b="Tamarind Rice (Puliyodarai)",
        risk_level="high",
        discriminative_features=[
            "color_chroma: bright vibrant canary yellow (turmeric + lemon) vs deep dark reddish brown / maroon (tamarind paste)",
            "nuts: roasted crunchy yellow peanuts in both, but background color is starkly distinct"
        ],
        disambiguation_test="Evaluate median hue: Bright Yellow (HSV hue ~45-60) = Lemon Rice; Dark Brownish-Red (HSV hue ~10-25) = Tamarind Rice.",
        primary_differentiator_a="Vibrant bright canary yellow rice with roasted peanuts, curry leaves, green chillies.",
        primary_differentiator_b="Deep reddish-brown tamarind paste coating, roasted sesame, fenugreek, dried red chillies."
    ),
    "coconut_chutney_vs_white_chutney": ConfusionPairSpec(
        pair_id="coconut_chutney_vs_white_chutney",
        class_a="White Coconut Chutney",
        class_b="Peanut / Sesame Chutney (White style)",
        risk_level="critical",
        discriminative_features=[
            "texture_and_gloss: visible grated coconut fiber crumb vs ultra-smooth ground peanut emulsion",
            "fat_droplets: coconut oil sheen vs peanut oil viscosity"
        ],
        disambiguation_test="Apply Section 34 Ambiguity Preserver: if grated coconut shreds are unconfirmed, return 'White Chutney — exact type uncertain.'",
        primary_differentiator_a="Grated fresh coconut flecks, fine crumb texture, mustard tempering.",
        primary_differentiator_b="Smooth homogenous nut-butter texture, denser viscosity."
    ),
    "tomato_chutney_vs_red_gravy": ConfusionPairSpec(
        pair_id="tomato_chutney_vs_red_gravy",
        class_a="Tomato Kaara Chutney",
        class_b="Red Curry / Gravy (Salna / Kuzhambu)",
        risk_level="high",
        discriminative_features=[
            "viscosity: thick condiment paste served in small dollop (30-50g) vs liquid flowing gravy served in bowls/cups (100-200g)",
            "plating: dolloped at edge of plate vs poured in center or in deep katori"
        ],
        disambiguation_test="Portion size and containment: small edge dollop = Chutney; liquid pool in bowl = Gravy.",
        primary_differentiator_a="Thick paste texture, small edge dollop, mustard tempering, no large vegetable pieces.",
        primary_differentiator_b="Liquid flowing consistency, large bowl portion, cooked vegetable or meat chunks."
    ),
    "mint_chutney_vs_coriander_chutney": ConfusionPairSpec(
        pair_id="mint_chutney_vs_coriander_chutney",
        class_a="Mint Chutney (Pudina)",
        class_b="Coriander Chutney (Kothamalli)",
        risk_level="moderate",
        discriminative_features=[
            "green_shade: deep mossy olive-green vs bright emerald vivid green",
            "texture: slightly darker leaf oxidation vs bright fresh herb texture"
        ],
        disambiguation_test="If indistinguishable, classify under parent 'Green Herb Chutney' with alternative suggestions.",
        primary_differentiator_a="Darker olive-moss green, ground roasted gram base.",
        primary_differentiator_b="Vibrant grass-emerald green, fine leafy shreds, ginger."
    ),
    "parotta_vs_paratha": ConfusionPairSpec(
        pair_id="parotta_vs_paratha",
        class_a="South Indian Parotta",
        class_b="North Indian Paratha",
        risk_level="critical",
        discriminative_features=[
            "layer_mechanism: concentric spiral rings crushed to reveal paper-thin multi-layer ribbons vs rolled folded flat wheat dough",
            "flour_type: all-purpose white maida (pale with golden blisters) vs whole wheat atta (brownish-tan earthy color)"
        ],
        disambiguation_test="Examine dough color (white maida vs brown atta) and presence of concentric coiled spiral sheets.",
        primary_differentiator_a="White flour (maida), concentric spiral rings, ultra-flaky crushed edges.",
        primary_differentiator_b="Brown whole wheat flour (atta), flat rolled sheet, stuffing (aloo/paneer/gobi) or square/triangle fold."
    ),
    "poori_vs_bhatura": ConfusionPairSpec(
        pair_id="poori_vs_bhatura",
        class_a="South Indian Poori",
        class_b="North Indian Bhatura",
        risk_level="high",
        discriminative_features=[
            "diameter: small to medium (10-14 cm) vs giant oval balloon (22-30 cm)",
            "flour: whole wheat flour (golden-tan) vs fermented maida (pale white/golden blistered elastic)"
        ],
        disambiguation_test="Measure physical diameter using plate scale calibrator: diameter < 16cm = Poori; diameter > 20cm = Bhatura.",
        primary_differentiator_a="Diameter 10-14 cm, whole wheat golden-brown surface, thin crispy blistered shell.",
        primary_differentiator_b="Diameter 22-30 cm, giant oval balloon, pale fermented maida dough, chewy texture."
    ),
    "kothu_parotta_vs_fried_rice": ConfusionPairSpec(
        pair_id="kothu_parotta_vs_fried_rice",
        class_a="Kothu Parotta",
        class_b="Egg / Chicken Fried Rice",
        risk_level="critical",
        discriminative_features=[
            "element_shape: flat shredded dough ribbons and caramelized ragged flakes vs individual slender oval rice grains",
            "texture: chewy soft dough pieces soaked in salna gravy vs dry separated individual grains tossed in wok"
        ],
        disambiguation_test="Morphological aspect ratio of pieces: elongated dough flakes (width > 5mm, irregular ribbons) = Kothu Parotta; rice grains (< 2mm width, oval) = Fried Rice.",
        primary_differentiator_a="Caramelized shredded wheat parotta flakes, scrambled egg, rich salna gravy coating.",
        primary_differentiator_b="Individual dry wok-tossed rice grains, diced spring onions, no dough flakes."
    ),
    "chicken_vs_mutton": ConfusionPairSpec(
        pair_id="chicken_vs_mutton",
        class_a="South Indian Chicken Dish",
        class_b="South Indian Mutton Dish",
        risk_level="high",
        discriminative_features=[
            "meat_color: pale pinkish-white cooked meat fiber vs dark reddish-brown to maroon dense muscle meat",
            "bone_structure: slender tubular hollow bones / cartilage vs dense thick marrow bones and chop ribs"
        ],
        disambiguation_test="Inspect meat fiber color and bone cross-section: dark fiber + thick marrow bone = Mutton; pale fiber = Chicken.",
        primary_differentiator_a="Pale fibrous meat, wing/leg drumstick bone, lighter gravy absorption.",
        primary_differentiator_b="Dark red-brown dense meat, marrow bone cuts, richer dark caramelized gravy."
    ),
    "fish_vs_chicken": ConfusionPairSpec(
        pair_id="fish_vs_chicken",
        class_a="Fish Fry / Fish Curry",
        class_b="Chicken Fry / Chicken Curry",
        risk_level="high",
        discriminative_features=[
            "flaking: distinct transverse myotome flakes (layered fish steaks) vs longitudinal stringy chicken fibers",
            "skin_and_bone: visible silvery/black fish skin, central spine bone, or ring steak cut"
        ],
        disambiguation_test="Check for transverse fish flakes, tail fin / steak geometry, or spine bones.",
        primary_differentiator_a="Transverse delicate flakes, oval cross-section fish steak, center spine.",
        primary_differentiator_b="Longitudinal fibrous muscle strands, drumstick or wing bones, irregular diced cubes."
    ),
    "prawn_vs_small_chicken_pieces": ConfusionPairSpec(
        pair_id="prawn_vs_small_chicken_pieces",
        class_a="Prawn Fry / Curry (Eraal)",
        class_b="Small Diced Boneless Chicken",
        risk_level="high",
        discriminative_features=[
            "morphology: curled C-shape or comma-shape segmented crustacean body with tail fan vs irregular angular cubed chicken chunks",
            "color: translucent pearly white with orange-pink curled ridges"
        ],
        disambiguation_test="Inspect curvature and segmentation: curled comma-shaped segmented arc = Prawn; random angular cube = Chicken.",
        primary_differentiator_a="Curled C-shaped comma body, segmented tail ridges, orange-pink edges.",
        primary_differentiator_b="Angular irregular cubes with linear poultry muscle grain."
    )
}

def get_confusion_pair(pair_id: str) -> Optional[ConfusionPairSpec]:
    return CONFUSION_MATRIX_REGISTRY.get(pair_id)

def get_all_confusion_pairs() -> List[ConfusionPairSpec]:
    return list(CONFUSION_MATRIX_REGISTRY.values())

def disambiguate_pair(pred_class_a: str, pred_class_b: str, visual_cues: Dict[str, Any]) -> Dict[str, Any]:
    """
    Applies the specific pairwise rule to disambiguate confusing foods.
    """
    for pair in CONFUSION_MATRIX_REGISTRY.values():
        if (pred_class_a.lower() in pair.class_a.lower() or pred_class_a.lower() in pair.class_b.lower()) and \
           (pred_class_b.lower() in pair.class_a.lower() or pred_class_b.lower() in pair.class_b.lower()):
            return {
                "pair_matched": pair.pair_id,
                "risk_level": pair.risk_level,
                "disambiguation_test": pair.disambiguation_test,
                "discriminative_cues": pair.discriminative_features,
                "applied_cues": visual_cues
            }
    return {
        "pair_matched": "generic_comparison",
        "risk_level": "moderate",
        "disambiguation_test": "Evaluate fine-grained texture, ingredients, and color profiles.",
        "discriminative_cues": [],
        "applied_cues": visual_cues
    }
