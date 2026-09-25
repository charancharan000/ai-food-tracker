from datetime import datetime, date
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict

class FoodItemBase(BaseModel):
    name: str
    estimated_weight_g: float
    servings: float = 1.0
    calories: float
    protein_g: float
    carbs_g: float
    fat_g: float
    fiber_g: float = 0.0
    sugar_g: float = 0.0
    sodium_mg: float = 0.0
    confidence: float = 0.8

class FoodItemCreate(FoodItemBase):
    pass

class FoodItemOut(FoodItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    meal_id: int

class MealCreate(BaseModel):
    meal_type: str = Field(..., description="Breakfast, Lunch, Snack, Dinner")
    meal_date: Optional[date] = None
    notes: Optional[str] = None
    image_url: Optional[str] = None
    food_items: List[FoodItemCreate] = Field(..., min_length=1)

class MealUpdate(BaseModel):
    meal_type: Optional[str] = None
    meal_date: Optional[date] = None
    notes: Optional[str] = None
    food_items: Optional[List[FoodItemCreate]] = None

class MealOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    meal_type: str
    meal_date: date
    total_calories: float
    total_protein: float
    total_carbs: float
    total_fat: float
    total_fiber: float
    total_sugar: float
    total_sodium: float
    image_url: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime
    food_items: List[FoodItemOut] = []
