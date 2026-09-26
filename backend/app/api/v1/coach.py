"""
FastAPI Router for FITBRO AI Fitness & Nutrition Coach
Implements /coach/chat and /coach/analyze-food-image endpoints with user profile & daily progress integration.
"""

from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from sqlalchemy.orm import selectinload

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.meal import Meal
from app.models.food_item import FoodItem
from app.models.water_log import WaterLog
from app.schemas.meal import MealOut
from app.services.fitness_coach_engine import (
    FitnessCoachIntelligence,
    UserProfileContext,
    CoachResponse,
    ParsedFoodLoggingItem,
)
from app.services.ai_vision_service import get_ai_vision_service
from app.food_ai.inference_pipeline import production_food_pipeline

router = APIRouter(prefix="/coach", tags=["AI Coach"])


class ChatMessagePayload(BaseModel):
    role: str # "user" or "coach"
    content: str


class CoachChatRequest(BaseModel):
    message: str
    conversation_history: Optional[List[ChatMessagePayload]] = Field(default_factory=list)
    auto_log_food: bool = True


class CoachChatResponse(BaseModel):
    reply: str
    intent_detected: str
    is_tamil_tanglish: bool = False
    logged_meal: Optional[MealOut] = None
    detected_foods: Optional[List[Dict[str, Any]]] = None
    daily_context: Dict[str, Any]


@router.post("/chat", response_model=CoachChatResponse)
async def chat_with_coach(
    payload: CoachChatRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    today = datetime.now(timezone.utc).date()

    # 1. Fetch today's meals for the authenticated user
    meals_result = await db.execute(
        select(Meal)
        .where(and_(Meal.user_id == current_user.id, Meal.meal_date == today))
        .options(selectinload(Meal.food_items))
    )
    today_meals = meals_result.scalars().all()

    # 2. Fetch today's water logs
    water_result = await db.execute(
        select(func.coalesce(func.sum(WaterLog.amount_ml), 0))
        .where(and_(WaterLog.user_id == current_user.id, WaterLog.date == today))
    )
    water_consumed = int(water_result.scalar() or 0)

    # 3. Aggregate today's macros
    cals_today = sum(m.total_calories for m in today_meals)
    protein_today = sum(m.total_protein for m in today_meals)
    carbs_today = sum(m.total_carbs for m in today_meals)
    fat_today = sum(m.total_fat for m in today_meals)

    # 4. Construct user profile context
    user_ctx = UserProfileContext(
        name=current_user.name,
        age=current_user.age or 25,
        gender=current_user.gender or "male",
        height_cm=current_user.height_cm or 175.0,
        weight_kg=current_user.weight_kg or 70.0,
        activity_level=current_user.activity_level or "moderate",
        goal=current_user.goal or "maintain",
        daily_calorie_target=current_user.daily_calorie_target or 2000.0,
        protein_target=current_user.protein_target or 140.0,
        carb_target=current_user.carb_target or 250.0,
        fat_target=current_user.fat_target or 65.0,
        daily_water_target_ml=current_user.daily_water_target_ml or 2500,
        calories_consumed_today=round(cals_today, 1),
        protein_consumed_today=round(protein_today, 1),
        carbs_consumed_today=round(carbs_today, 1),
        fat_consumed_today=round(fat_today, 1),
        water_consumed_today=water_consumed,
    )

    # Format conversation history
    history_dicts = [{"role": m.role, "content": m.content} for m in (payload.conversation_history or [])]

    # 5. Generate coach intelligence answer
    coach_result = FitnessCoachIntelligence.generate_coach_answer(
        user_message=payload.message,
        user_profile=user_ctx,
        conversation_history=history_dicts,
    )

    logged_meal_out: Optional[MealOut] = None

    # 6. Auto-log food to user's database if logging intent detected and requested
    if coach_result.logged_food_items and payload.auto_log_food:
        tot_cals = sum(it.calories for it in coach_result.logged_food_items)
        tot_pro = sum(it.protein_g for it in coach_result.logged_food_items)
        tot_carb = sum(it.carbs_g for it in coach_result.logged_food_items)
        tot_fat = sum(it.fat_g for it in coach_result.logged_food_items)
        tot_fib = sum(it.fiber_g for it in coach_result.logged_food_items)

        new_meal = Meal(
            user_id=current_user.id,
            meal_type="Snack" if "snack" in payload.message.lower() else "Meal",
            meal_date=today,
            total_calories=round(tot_cals, 1),
            total_protein=round(tot_pro, 1),
            total_carbs=round(tot_carb, 1),
            total_fat=round(tot_fat, 1),
            total_fiber=round(tot_fib, 1),
            total_sugar=0.0,
            total_sodium=0.0,
            notes=f"Logged via FitBro AI Coach: '{payload.message}'",
        )
        db.add(new_meal)
        await db.flush()

        for it in coach_result.logged_food_items:
            fi = FoodItem(
                meal_id=new_meal.id,
                name=it.name,
                estimated_weight_g=it.estimated_weight_g,
                servings=it.quantity,
                calories=it.calories,
                protein_g=it.protein_g,
                carbs_g=it.carbs_g,
                fat_g=it.fat_g,
                fiber_g=it.fiber_g,
                sugar_g=0.0,
                sodium_mg=0.0,
                confidence=0.92,
            )
            db.add(fi)

        await db.commit()

        # Reload with food items
        reloaded = await db.execute(
            select(Meal).where(Meal.id == new_meal.id).options(selectinload(Meal.food_items))
        )
        saved_meal = reloaded.scalar_one()
        logged_meal_out = MealOut.model_validate(saved_meal)

    detected_foods_list = (
        [it.model_dump() for it in coach_result.logged_food_items] if coach_result.logged_food_items else None
    )

    daily_summary = {
        "calories_consumed_today": user_ctx.calories_consumed_today,
        "daily_calorie_target": user_ctx.daily_calorie_target,
        "remaining_calories": coach_result.remaining_calories,
        "protein_consumed_today": user_ctx.protein_consumed_today,
        "protein_target": user_ctx.protein_target,
        "remaining_protein": coach_result.remaining_protein,
    }

    return CoachChatResponse(
        reply=coach_result.reply_text,
        intent_detected=coach_result.intent_detected,
        is_tamil_tanglish=coach_result.is_tamil_tanglish,
        logged_meal=logged_meal_out,
        detected_foods=detected_foods_list,
        daily_context=daily_summary,
    )


@router.post("/analyze-food-image")
async def coach_analyze_food_image(
    file: UploadFile = File(..., description="Food photo from coach chat"),
    plate_diameter_cm: float = Form(26.0),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Connects AI Coach to existing FITBRO food vision pipeline (Food Image Support).
    Identifies foods, portions, calories, macros, and returns coaching guidance.
    """
    try:
        image_bytes = await file.read()
        analysis = production_food_pipeline.analyze_meal(
            top_image_bytes=image_bytes,
            plate_diameter_cm=plate_diameter_cm,
            dish_hint=None,
            preferred_mode="normal",
        )

        detected_summary = "\n".join(
            [f"• **{item.food_name}** ({item.estimated_weight_grams}g): ~{item.calories} kcal | {item.protein_grams}g Protein | {item.carbs_grams}g Carbs | {item.fat_grams}g Fat"
             for item in analysis.detected_items]
        )

        coach_advice = (
            f"📸 **Food Image Analyzed!**\n\n"
            f"{detected_summary}\n\n"
            f"**Total Estimated Nutrition:**\n"
            f"• Calories: **{analysis.total_calories} kcal**\n"
            f"• Protein: **{analysis.total_protein_g}g**\n"
            f"• Carbs: **{analysis.total_carbs_g}g**\n"
            f"• Fat: **{analysis.total_fat_g}g**\n\n"
            f"💡 *Coach Analysis:* "
        )

        if analysis.total_protein_g >= 25.0:
            coach_advice += "Excellent high-protein meal! This fits great with your muscle recovery goals."
        elif analysis.total_calories > 600:
            coach_advice += "Calorie-dense meal. If you are cutting or in a deficit, be mindful of remaining portions for the rest of the day."
        else:
            coach_advice += "Balanced meal. Consider adding a side of boiled eggs or curd if you need more protein."

        return {
            "coach_reply": coach_advice,
            "detected_items": [item.model_dump() for item in analysis.detected_items],
            "total_calories": analysis.total_calories,
            "total_protein_g": analysis.total_protein_g,
            "total_carbs_g": analysis.total_carbs_g,
            "total_fat_g": analysis.total_fat_g,
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Image analysis failed: {str(e)}",
        )
