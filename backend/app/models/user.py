from datetime import datetime, timezone
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import Integer, String, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

if TYPE_CHECKING:
    from app.models.meal import Meal
    from app.models.water_log import WaterLog

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    
    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    gender: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    height_cm: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    weight_kg: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    activity_level: Mapped[str] = mapped_column(String(50), default="moderate")
    goal: Mapped[str] = mapped_column(String(50), default="maintain")
    
    daily_calorie_target: Mapped[float] = mapped_column(Float, default=2000.0)
    protein_target: Mapped[float] = mapped_column(Float, default=150.0)
    carb_target: Mapped[float] = mapped_column(Float, default=250.0)
    fat_target: Mapped[float] = mapped_column(Float, default=65.0)
    daily_water_target_ml: Mapped[int] = mapped_column(Integer, default=2500)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=lambda: datetime.now(timezone.utc), 
        onupdate=lambda: datetime.now(timezone.utc)
    )

    meals: Mapped[List["Meal"]] = relationship("Meal", back_populates="user", cascade="all, delete-orphan")
    water_logs: Mapped[List["WaterLog"]] = relationship("WaterLog", back_populates="user", cascade="all, delete-orphan")
