from datetime import date, datetime, timezone
from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.meal import Meal
from app.models.food_item import FoodItem
from app.schemas.meal import MealCreate, MealUpdate, MealOut
from app.services.nutrition_calc import calculate_meal_totals
from app.core.exceptions import NotFoundException, BadRequestException

router = APIRouter(prefix="/meals", tags=["Meals"])

@router.post("", response_model=MealOut, status_code=status.HTTP_201_CREATED)
async def create_meal(
    meal_in: MealCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if not meal_in.food_items:
        raise BadRequestException("Meal must contain at least one food item.")

    totals = calculate_meal_totals(meal_in.food_items)
    meal_date = meal_in.meal_date or datetime.now(timezone.utc).date()

    new_meal = Meal(
        user_id=current_user.id,
        meal_type=meal_in.meal_type,
        meal_date=meal_date,
        total_calories=totals["calories"],
        total_protein=totals["protein_g"],
        total_carbs=totals["carbs_g"],
        total_fat=totals["fat_g"],
        total_fiber=totals["fiber_g"],
        total_sugar=totals["sugar_g"],
        total_sodium=totals["sodium_mg"],
        image_url=meal_in.image_url,
        notes=meal_in.notes,
    )
    db.add(new_meal)
    await db.flush()  # to get new_meal.id

    for item_data in meal_in.food_items:
        food_item = FoodItem(
            meal_id=new_meal.id,
            name=item_data.name,
            estimated_weight_g=item_data.estimated_weight_g,
            servings=item_data.servings,
            calories=item_data.calories,
            protein_g=item_data.protein_g,
            carbs_g=item_data.carbs_g,
            fat_g=item_data.fat_g,
            fiber_g=item_data.fiber_g,
            sugar_g=item_data.sugar_g,
            sodium_mg=item_data.sodium_mg,
            confidence=item_data.confidence,
        )
        db.add(food_item)

    await db.commit()
    
    # Reload with food items
    result = await db.execute(
        select(Meal).where(Meal.id == new_meal.id).options(selectinload(Meal.food_items))
    )
    meal = result.scalar_one()
    return meal

@router.get("/today", response_model=List[MealOut])
async def get_today_meals(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    today = datetime.now(timezone.utc).date()
    result = await db.execute(
        select(Meal)
        .where(and_(Meal.user_id == current_user.id, Meal.meal_date == today))
        .options(selectinload(Meal.food_items))
        .order_by(Meal.created_at.desc())
    )
    return result.scalars().all()

@router.get("", response_model=List[MealOut])
async def get_meals(
    meal_date: Optional[date] = Query(None, alias="date"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    query = select(Meal).where(Meal.user_id == current_user.id).options(selectinload(Meal.food_items))
    if meal_date:
        query = query.where(Meal.meal_date == meal_date)
    query = query.order_by(Meal.meal_date.desc(), Meal.created_at.desc())
    result = await db.execute(query)
    return result.scalars().all()

@router.get("/{meal_id}", response_model=MealOut)
async def get_meal(
    meal_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Meal)
        .where(and_(Meal.id == meal_id, Meal.user_id == current_user.id))
        .options(selectinload(Meal.food_items))
    )
    meal = result.scalar_one_or_none()
    if not meal:
        raise NotFoundException(f"Meal with ID {meal_id} not found.")
    return meal

@router.put("/{meal_id}", response_model=MealOut)
async def update_meal(
    meal_id: int,
    meal_update: MealUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Meal)
        .where(and_(Meal.id == meal_id, Meal.user_id == current_user.id))
        .options(selectinload(Meal.food_items))
    )
    meal = result.scalar_one_or_none()
    if not meal:
        raise NotFoundException(f"Meal with ID {meal_id} not found.")

    if meal_update.meal_type is not None:
        meal.meal_type = meal_update.meal_type
    if meal_update.meal_date is not None:
        meal.meal_date = meal_update.meal_date
    if meal_update.notes is not None:
        meal.notes = meal_update.notes

    # If food items provided, replace existing items
    if meal_update.food_items is not None:
        totals = calculate_meal_totals(meal_update.food_items)
        meal.total_calories = totals["calories"]
        meal.total_protein = totals["protein_g"]
        meal.total_carbs = totals["carbs_g"]
        meal.total_fat = totals["fat_g"]
        meal.total_fiber = totals["fiber_g"]
        meal.total_sugar = totals["sugar_g"]
        meal.total_sodium = totals["sodium_mg"]

        meal.food_items = [
            FoodItem(
                meal_id=meal.id,
                name=item_data.name,
                estimated_weight_g=item_data.estimated_weight_g,
                servings=item_data.servings,
                calories=item_data.calories,
                protein_g=item_data.protein_g,
                carbs_g=item_data.carbs_g,
                fat_g=item_data.fat_g,
                fiber_g=item_data.fiber_g,
                sugar_g=item_data.sugar_g,
                sodium_mg=item_data.sodium_mg,
                confidence=item_data.confidence,
            )
            for item_data in meal_update.food_items
        ]

    await db.commit()
    
    # Reload updated meal
    reloaded = await db.execute(
        select(Meal).where(Meal.id == meal_id).options(selectinload(Meal.food_items))
    )
    return reloaded.scalar_one()

@router.delete("/{meal_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_meal(
    meal_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Meal).where(and_(Meal.id == meal_id, Meal.user_id == current_user.id))
    )
    meal = result.scalar_one_or_none()
    if not meal:
        raise NotFoundException(f"Meal with ID {meal_id} not found.")

    await db.delete(meal)
    await db.commit()
    return None
