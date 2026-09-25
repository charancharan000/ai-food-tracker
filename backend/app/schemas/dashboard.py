from datetime import date
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from app.schemas.meal import MealOut

class MacroBreakdown(BaseModel):
    consumed: float
    target: float
    remaining: float
    percentage: float

class MealsByType(BaseModel):
    calories: float
    count: int
    meals: List[MealOut]

class DashboardTodayResponse(BaseModel):
    date: date
    calories_consumed: float
    daily_calorie_target: float
    calories_remaining: float
    calories_percentage: float
    protein: MacroBreakdown
    carbs: MacroBreakdown
    fat: MacroBreakdown
    water_consumed_ml: int
    water_target_ml: int
    water_percentage: float
    meals_by_type: Dict[str, MealsByType]
    recent_meals: List[MealOut]

class DailySummaryItem(BaseModel):
    date: str
    calories: float
    target_calories: float
    protein_g: float
    carbs_g: float
    fat_g: float
    meal_count: int

class DashboardSummaryResponse(BaseModel):
    timeframe: str
    start_date: str
    end_date: str
    average_daily_calories: float
    total_calories: float
    total_meals: int
    daily_stats: List[DailySummaryItem]
