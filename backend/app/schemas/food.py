from typing import List, Optional
from pydantic import BaseModel, Field

class FoodItemDetection(BaseModel):
    name: str = Field(..., description="Identified food item name")
    estimated_weight_g: float = Field(..., ge=0, description="Estimated weight in grams")
    servings: float = Field(default=1.0, ge=0.1, description="Servings multiplier")
    calories: float = Field(..., ge=0, description="Calories in kcal")
    protein_g: float = Field(..., ge=0, description="Protein in grams")
    carbs_g: float = Field(..., ge=0, description="Carbohydrates in grams")
    fat_g: float = Field(..., ge=0, description="Fat in grams")
    fiber_g: float = Field(default=0.0, ge=0, description="Fiber in grams")
    sugar_g: float = Field(default=0.0, ge=0, description="Sugar in grams")
    sodium_mg: float = Field(default=0.0, ge=0, description="Sodium in milligrams")
    confidence: float = Field(default=0.8, ge=0.0, le=1.0, description="AI confidence score 0.0 to 1.0")

class NutritionTotal(BaseModel):
    calories: float = Field(..., ge=0)
    protein_g: float = Field(..., ge=0)
    carbs_g: float = Field(..., ge=0)
    fat_g: float = Field(..., ge=0)
    fiber_g: float = Field(default=0.0, ge=0)
    sugar_g: float = Field(default=0.0, ge=0)
    sodium_mg: float = Field(default=0.0, ge=0)

class FoodAnalysisResponse(BaseModel):
    food_items: List[FoodItemDetection]
    total: NutritionTotal
    notes: Optional[str] = "Nutrition is estimated from the image and portion size."
    image_preview_url: Optional[str] = None
