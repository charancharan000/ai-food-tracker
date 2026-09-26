"""
Recipe-Level Nutrition Engine with Household & Restaurant Variations
Calculates accurate macronutrients by summing raw ingredients, accounting for cooking yield,
moisture evaporation, and oil absorption.
"""

from typing import List, Dict, Optional
from pydantic import BaseModel, Field

class RecipeIngredient(BaseModel):
    name: str
    raw_weight_g: float
    calories: float
    protein_g: float
    carbs_g: float
    fat_g: float
    fiber_g: float = 0.0
    sodium_mg: float = 0.0

class RecipeBlueprint(BaseModel):
    dish_id: str
    dish_name: str
    variant: str = "Standard Home Recipe" # e.g. "Home Style", "Hotel Restaurant Style", "Healthy Low Oil"
    ingredients: List[RecipeIngredient]
    cooked_weight_yield_g: float
    cooking_notes: str

    def compute_nutrition_per_100g(self) -> Dict[str, float]:
        total_raw_weight = sum(i.raw_weight_g for i in self.ingredients)
        total_calories = sum(i.calories for i in self.ingredients)
        total_protein = sum(i.protein_g for i in self.ingredients)
        total_carbs = sum(i.carbs_g for i in self.ingredients)
        total_fat = sum(i.fat_g for i in self.ingredients)
        total_fiber = sum(i.fiber_g for i in self.ingredients)
        total_sodium = sum(i.sodium_mg for i in self.ingredients)

        final_weight = self.cooked_weight_yield_g or total_raw_weight
        scale = 100.0 / final_weight

        return {
            "calories_per_100g": round(total_calories * scale, 1),
            "protein_g_per_100g": round(total_protein * scale, 2),
            "carbs_g_per_100g": round(total_carbs * scale, 2),
            "fat_g_per_100g": round(total_fat * scale, 2),
            "fiber_g_per_100g": round(total_fiber * scale, 2),
            "sodium_mg_per_100g": round(total_sodium * scale, 1),
            "total_recipe_calories": round(total_calories, 1),
            "total_recipe_weight_g": round(final_weight, 1),
        }

RECIPE_REGISTRY: Dict[str, List[RecipeBlueprint]] = {
    "Masala Dosa": [
        RecipeBlueprint(
            dish_id="masala_dosa_home",
            dish_name="Masala Dosa",
            variant="Traditional Home Style (Moderate Oil)",
            ingredients=[
                RecipeIngredient(name="Dosa Batter (Rice+Urad)", raw_weight_g=100.0, calories=150.0, protein_g=3.5, carbs_g=30.0, fat_g=0.5),
                RecipeIngredient(name="Potato Filling", raw_weight_g=80.0, calories=75.0, protein_g=1.8, carbs_g=14.0, fat_g=1.2),
                RecipeIngredient(name="Ghee / Oil", raw_weight_g=8.0, calories=72.0, protein_g=0.0, carbs_g=0.0, fat_g=8.0),
            ],
            cooked_weight_yield_g=180.0,
            cooking_notes="Crisped on iron tawa with 1 tsp ghee, steam loss approx 8g."
        ),
        RecipeBlueprint(
            dish_id="masala_dosa_restaurant",
            dish_name="Masala Dosa",
            variant="Hotel Restaurant Style (Ghee Roast)",
            ingredients=[
                RecipeIngredient(name="Dosa Batter", raw_weight_g=110.0, calories=165.0, protein_g=3.8, carbs_g=33.0, fat_g=0.6),
                RecipeIngredient(name="Potato Masala", raw_weight_g=100.0, calories=95.0, protein_g=2.2, carbs_g=18.0, fat_g=1.5),
                RecipeIngredient(name="Desi Ghee (Liberal application)", raw_weight_g=18.0, calories=160.0, protein_g=0.0, carbs_g=0.0, fat_g=18.0),
            ],
            cooked_weight_yield_g=210.0,
            cooking_notes="Golden crisp restaurant roast with rich butter/ghee glaze."
        )
    ],
    "Chicken Biryani": [
        RecipeBlueprint(
            dish_id="chicken_biryani_dindigul",
            dish_name="Chicken Biryani",
            variant="Dindigul Thalappakatti Seeraga Samba Style",
            ingredients=[
                RecipeIngredient(name="Seeraga Samba Rice", raw_weight_g=250.0, calories=890.0, protein_g=17.0, carbs_g=195.0, fat_g=1.2),
                RecipeIngredient(name="Chicken with bone", raw_weight_g=300.0, calories=450.0, protein_g=58.0, carbs_g=0.0, fat_g=24.0),
                RecipeIngredient(name="Curd & Marinade", raw_weight_g=80.0, calories=50.0, protein_g=2.8, carbs_g=3.8, fat_g=2.6),
                RecipeIngredient(name="Ghee & Groundnut Oil", raw_weight_g=40.0, calories=360.0, protein_g=0.0, carbs_g=0.0, fat_g=40.0),
                RecipeIngredient(name="Fried Shallots & Aromatics", raw_weight_g=60.0, calories=65.0, protein_g=1.5, carbs_g=10.0, fat_g=1.8),
            ],
            cooked_weight_yield_g=680.0,
            cooking_notes="Woodfire dum absorption; 2 generous servings yield."
        ),
        RecipeBlueprint(
            dish_id="chicken_biryani_hyderabadi",
            dish_name="Chicken Biryani",
            variant="Hyderabadi Basmati Dum Style",
            ingredients=[
                RecipeIngredient(name="Basmati Rice", raw_weight_g=250.0, calories=875.0, protein_g=16.5, carbs_g=190.0, fat_g=1.0),
                RecipeIngredient(name="Marinated Chicken", raw_weight_g=300.0, calories=480.0, protein_g=60.0, carbs_g=1.0, fat_g=26.0),
                RecipeIngredient(name="Fried Onions (Birista)", raw_weight_g=50.0, calories=180.0, protein_g=2.0, carbs_g=15.0, fat_g=12.0),
                RecipeIngredient(name="Saffron Milk & Ghee", raw_weight_g=45.0, calories=340.0, protein_g=1.0, carbs_g=2.5, fat_g=36.0),
            ],
            cooked_weight_yield_g=700.0,
            cooking_notes="Sealed dum pot with layered basmati and spiced chicken."
        )
    ],
    "Idli": [
        RecipeBlueprint(
            dish_id="idli_standard",
            dish_name="Steamed Idli (2 pieces)",
            variant="Standard 4:1 Rice-to-Dal Fermented Recipe",
            ingredients=[
                RecipeIngredient(name="Parboiled Idli Rice", raw_weight_g=60.0, calories=213.0, protein_g=4.1, carbs_g=47.0, fat_g=0.3),
                RecipeIngredient(name="Whole Urad Dal", raw_weight_g=15.0, calories=51.0, protein_g=3.6, carbs_g=8.8, fat_g=0.2),
                RecipeIngredient(name="Water (absorbed)", raw_weight_g=45.0, calories=0.0, protein_g=0.0, carbs_g=0.0, fat_g=0.0),
            ],
            cooked_weight_yield_g=120.0,
            cooking_notes="Steamed in wet cotton cloth / oiled molds for 10 minutes."
        )
    ],
    "Ven Pongal": [
        RecipeBlueprint(
            dish_id="ven_pongal_ghee",
            dish_name="Ven Pongal",
            variant="Classic Ghee Ven Pongal with Cashews",
            ingredients=[
                RecipeIngredient(name="Raw Rice", raw_weight_g=100.0, calories=356.0, protein_g=6.8, carbs_g=78.2, fat_g=0.5),
                RecipeIngredient(name="Yellow Moong Dal", raw_weight_g=50.0, calories=173.0, protein_g=12.0, carbs_g=29.5, fat_g=0.6),
                RecipeIngredient(name="Desi Ghee", raw_weight_g=20.0, calories=180.0, protein_g=0.0, carbs_g=0.0, fat_g=20.0),
                RecipeIngredient(name="Cashews & Pepper Tempering", raw_weight_g=15.0, calories=85.0, protein_g=2.2, carbs_g=4.2, fat_g=7.5),
            ],
            cooked_weight_yield_g=420.0,
            cooking_notes="Pressure cooked soft with 4x water, finished with crackling pepper-cumin ghee."
        )
    ],
    "Medu Vada": [
        RecipeBlueprint(
            dish_id="medu_vada_classic",
            dish_name="Medu Vada (1 piece)",
            variant="Deep Fried Urad Dal Fritter",
            ingredients=[
                RecipeIngredient(name="Soaked Urad Dal", raw_weight_g=45.0, calories=150.0, protein_g=10.5, carbs_g=26.0, fat_g=0.6),
                RecipeIngredient(name="Absorbed Frying Oil", raw_weight_g=7.0, calories=63.0, protein_g=0.0, carbs_g=0.0, fat_g=7.0),
                RecipeIngredient(name="Onion, Ginger, Pepper", raw_weight_g=6.0, calories=5.0, protein_g=0.2, carbs_g=1.0, fat_g=0.0),
            ],
            cooked_weight_yield_g=55.0,
            cooking_notes="Fluffy aerated batter shaped with hole, deep fried at 180°C."
        )
    ],
    "Chicken Kothu Parotta": [
        RecipeBlueprint(
            dish_id="kothu_parotta_chicken",
            dish_name="Chicken Kothu Parotta",
            variant="Street Style with Egg & Chicken Salna",
            ingredients=[
                RecipeIngredient(name="Shredded Maida Parotta", raw_weight_g=180.0, calories=570.0, protein_g=11.5, carbs_g=85.0, fat_g=21.0),
                RecipeIngredient(name="Chicken Meat Pieces", raw_weight_g=70.0, calories=105.0, protein_g=18.0, carbs_g=0.0, fat_g=3.5),
                RecipeIngredient(name="Egg (1 whole)", raw_weight_g=50.0, calories=72.0, protein_g=6.3, carbs_g=0.4, fat_g=4.8),
                RecipeIngredient(name="Salna / Spiced Gravy", raw_weight_g=60.0, calories=55.0, protein_g=1.8, carbs_g=4.0, fat_g=3.8),
            ],
            cooked_weight_yield_g=340.0,
            cooking_notes="Chop-griddled with metal blades on heavy flat-top cast iron."
        )
    ],
    "Curd Rice": [
        RecipeBlueprint(
            dish_id="curd_rice_tempered",
            dish_name="Curd Rice (Thayir Sadam)",
            variant="Traditional Home Style Tempered",
            ingredients=[
                RecipeIngredient(name="Cooked Soft White Rice", raw_weight_g=140.0, calories=182.0, protein_g=3.8, carbs_g=39.0, fat_g=0.4),
                RecipeIngredient(name="Fresh Thick Curd & Milk", raw_weight_g=100.0, calories=68.0, protein_g=3.5, carbs_g=4.8, fat_g=3.8),
                RecipeIngredient(name="Ghee Tempering with Mustard, Green Chillies, Curry Leaves", raw_weight_g=6.0, calories=54.0, protein_g=0.0, carbs_g=0.0, fat_g=6.0),
            ],
            cooked_weight_yield_g=240.0,
            cooking_notes="Softly mashed rice folded with fresh curd, tempered in hot ghee."
        )
    ],
    "Chicken 65": [
        RecipeBlueprint(
            dish_id="chicken_65_crispy",
            dish_name="Chicken 65",
            variant="South Indian Restaurant Crispy Deep Fried",
            ingredients=[
                RecipeIngredient(name="Boneless Chicken Cubes", raw_weight_g=120.0, calories=144.0, protein_g=27.0, carbs_g=0.0, fat_g=3.1),
                RecipeIngredient(name="Cornflour/Rice Flour Batter & Spices", raw_weight_g=18.0, calories=65.0, protein_g=1.0, carbs_g=15.0, fat_g=0.2),
                RecipeIngredient(name="Absorbed Frying Oil", raw_weight_g=18.0, calories=162.0, protein_g=0.0, carbs_g=0.0, fat_g=18.0),
            ],
            cooked_weight_yield_g=150.0,
            cooking_notes="Deep fried with curry leaves and green chillies."
        )
    ]
}
