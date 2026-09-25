from datetime import date, datetime, timedelta, timezone
from typing import Dict, List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from sqlalchemy.orm import selectinload

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.meal import Meal
from app.models.water_log import WaterLog
from app.schemas.dashboard import (
    DashboardTodayResponse,
    MacroBreakdown,
    MealsByType,
    DashboardSummaryResponse,
    DailySummaryItem
)
from app.schemas.meal import MealOut

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/today", response_model=DashboardTodayResponse)
async def get_dashboard_today(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    today = datetime.now(timezone.utc).date()

    meals_result = await db.execute(
        select(Meal)
        .where(and_(Meal.user_id == current_user.id, Meal.meal_date == today))
        .options(selectinload(Meal.food_items))
        .order_by(Meal.created_at.desc())
    )
    today_meals = meals_result.scalars().all()

    water_result = await db.execute(
        select(func.coalesce(func.sum(WaterLog.amount_ml), 0))
        .where(and_(WaterLog.user_id == current_user.id, WaterLog.date == today))
    )
    water_consumed = int(water_result.scalar() or 0)

    total_calories = sum(m.total_calories for m in today_meals)
    total_protein = sum(m.total_protein for m in today_meals)
    total_carbs = sum(m.total_carbs for m in today_meals)
    total_fat = sum(m.total_fat for m in today_meals)

    cal_target = current_user.daily_calorie_target or 2000.0
    cal_remaining = max(0.0, cal_target - total_calories)
    cal_percentage = min(100.0, round((total_calories / cal_target) * 100, 1)) if cal_target > 0 else 0.0

    p_target = current_user.protein_target or 150.0
    p_remaining = max(0.0, p_target - total_protein)
    p_percentage = min(100.0, round((total_protein / p_target) * 100, 1)) if p_target > 0 else 0.0

    c_target = current_user.carb_target or 250.0
    c_remaining = max(0.0, c_target - total_carbs)
    c_percentage = min(100.0, round((total_carbs / c_target) * 100, 1)) if c_target > 0 else 0.0

    f_target = current_user.fat_target or 65.0
    f_remaining = max(0.0, f_target - total_fat)
    f_percentage = min(100.0, round((total_fat / f_target) * 100, 1)) if f_target > 0 else 0.0

    water_target = current_user.daily_water_target_ml or 2500
    water_percentage = min(100.0, round((water_consumed / water_target) * 100, 1)) if water_target > 0 else 0.0

    standard_types = ["Breakfast", "Lunch", "Snack", "Dinner"]
    meals_by_type_dict: Dict[str, MealsByType] = {}
    for st in standard_types:
        matching = [m for m in today_meals if m.meal_type.lower() == st.lower()]
        meals_by_type_dict[st] = MealsByType(
            calories=round(sum(m.total_calories for m in matching), 1),
            count=len(matching),
            meals=[MealOut.model_validate(m) for m in matching]
        )

    return DashboardTodayResponse(
        date=today,
        calories_consumed=round(total_calories, 1),
        daily_calorie_target=round(cal_target, 1),
        calories_remaining=round(cal_remaining, 1),
        calories_percentage=cal_percentage,
        protein=MacroBreakdown(
            consumed=round(total_protein, 1),
            target=round(p_target, 1),
            remaining=round(p_remaining, 1),
            percentage=p_percentage
        ),
        carbs=MacroBreakdown(
            consumed=round(total_carbs, 1),
            target=round(c_target, 1),
            remaining=round(c_remaining, 1),
            percentage=c_percentage
        ),
        fat=MacroBreakdown(
            consumed=round(total_fat, 1),
            target=round(f_target, 1),
            remaining=round(f_remaining, 1),
            percentage=f_percentage
        ),
        water_consumed_ml=water_consumed,
        water_target_ml=water_target,
        water_percentage=water_percentage,
        meals_by_type=meals_by_type_dict,
        recent_meals=[MealOut.model_validate(m) for m in today_meals[:5]]
    )

@router.get("/summary", response_model=DashboardSummaryResponse)
async def get_dashboard_summary(
    timeframe: str = Query("week", description="today, yesterday, week, month"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    today = datetime.now(timezone.utc).date()
    
    if timeframe == "today":
        start_date = today
        end_date = today
    elif timeframe == "yesterday":
        start_date = today - timedelta(days=1)
        end_date = today - timedelta(days=1)
    elif timeframe == "month":
        start_date = today - timedelta(days=29)
        end_date = today
    else:
        start_date = today - timedelta(days=6)
        end_date = today

    result = await db.execute(
        select(Meal)
        .where(
            and_(
                Meal.user_id == current_user.id,
                Meal.meal_date >= start_date,
                Meal.meal_date <= end_date
            )
        )
        .order_by(Meal.meal_date.asc())
    )
    meals = result.scalars().all()

    days_count = (end_date - start_date).days + 1
    daily_map = {}
    for i in range(days_count):
        d = start_date + timedelta(days=i)
        d_str = d.isoformat()
        daily_map[d_str] = {
            "date": d_str,
            "calories": 0.0,
            "target_calories": current_user.daily_calorie_target,
            "protein_g": 0.0,
            "carbs_g": 0.0,
            "fat_g": 0.0,
            "meal_count": 0
        }

    total_calories = 0.0
    for m in meals:
        d_str = m.meal_date.isoformat()
        if d_str in daily_map:
            daily_map[d_str]["calories"] += m.total_calories
            daily_map[d_str]["protein_g"] += m.total_protein
            daily_map[d_str]["carbs_g"] += m.total_carbs
            daily_map[d_str]["fat_g"] += m.total_fat
            daily_map[d_str]["meal_count"] += 1
            total_calories += m.total_calories

    daily_items = [
        DailySummaryItem(
            date=v["date"],
            calories=round(v["calories"], 1),
            target_calories=round(v["target_calories"], 1),
            protein_g=round(v["protein_g"], 1),
            carbs_g=round(v["carbs_g"], 1),
            fat_g=round(v["fat_g"], 1),
            meal_count=v["meal_count"]
        )
        for v in daily_map.values()
    ]

    avg_cals = round(total_calories / max(1, days_count), 1)

    return DashboardSummaryResponse(
        timeframe=timeframe,
        start_date=start_date.isoformat(),
        end_date=end_date.isoformat(),
        average_daily_calories=avg_cals,
        total_calories=round(total_calories, 1),
        total_meals=len(meals),
        daily_stats=daily_items
    )
