from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class ProfileUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    age: Optional[int] = Field(None, ge=10, le=120)
    gender: Optional[str] = None  # male, female, other
    height_cm: Optional[float] = Field(None, ge=50, le=280)
    weight_kg: Optional[float] = Field(None, ge=20, le=350)
    activity_level: Optional[str] = None  # sedentary, light, moderate, active, very_active
    goal: Optional[str] = None  # lose, maintain, gain

class GoalsUpdate(BaseModel):
    daily_calorie_target: Optional[float] = Field(None, ge=500, le=10000)
    protein_target: Optional[float] = Field(None, ge=10, le=500)
    carb_target: Optional[float] = Field(None, ge=10, le=1000)
    fat_target: Optional[float] = Field(None, ge=5, le=300)
    daily_water_target_ml: Optional[int] = Field(None, ge=500, le=10000)

class ProfileOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    age: Optional[int]
    gender: Optional[str]
    height_cm: Optional[float]
    weight_kg: Optional[float]
    activity_level: str
    goal: str
    daily_calorie_target: float
    protein_target: float
    carb_target: float
    fat_target: float
    daily_water_target_ml: int
