from datetime import datetime, date, timezone
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import Integer, String, Float, Date, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.food_item import FoodItem

class Meal(Base):
    __tablename__ = "meals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    meal_type: Mapped[str] = mapped_column(String(50), nullable=False)  # Breakfast, Lunch, Snack, Dinner
    meal_date: Mapped[date] = mapped_column(Date, default=lambda: datetime.now(timezone.utc).date(), index=True)
    
    total_calories: Mapped[float] = mapped_column(Float, default=0.0)
    total_protein: Mapped[float] = mapped_column(Float, default=0.0)
    total_carbs: Mapped[float] = mapped_column(Float, default=0.0)
    total_fat: Mapped[float] = mapped_column(Float, default=0.0)
    total_fiber: Mapped[float] = mapped_column(Float, default=0.0)
    total_sugar: Mapped[float] = mapped_column(Float, default=0.0)
    total_sodium: Mapped[float] = mapped_column(Float, default=0.0)
    
    image_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="meals")
    food_items: Mapped[List["FoodItem"]] = relationship("FoodItem", back_populates="meal", cascade="all, delete-orphan", lazy="selectin")
