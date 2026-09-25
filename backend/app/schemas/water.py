from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict

class WaterLogCreate(BaseModel):
    amount_ml: int = Field(..., ge=1, le=5000, description="Amount of water drunk in milliliters")
    date: Optional[date] = None

class WaterLogOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    date: date
    amount_ml: int
    created_at: datetime

class WaterTodayResponse(BaseModel):
    date: date
    total_ml: int
    target_ml: int
    remaining_ml: int
    percentage: float
    logs: List[WaterLogOut]
