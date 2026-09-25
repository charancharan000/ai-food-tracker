from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.profile import ProfileUpdate, GoalsUpdate, ProfileOut
from app.services.nutrition_calc import calculate_daily_calorie_and_macro_targets

router = APIRouter(prefix="/profile", tags=["Profile & Goals"])

@router.get("", response_model=ProfileOut)
async def get_profile(current_user: User = Depends(get_current_user)):
    return ProfileOut.model_validate(current_user)

@router.put("", response_model=ProfileOut)
async def update_profile(
    profile_in: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if profile_in.name is not None:
        current_user.name = profile_in.name.strip()
    if profile_in.age is not None:
        current_user.age = profile_in.age
    if profile_in.gender is not None:
        current_user.gender = profile_in.gender
    if profile_in.height_cm is not None:
        current_user.height_cm = profile_in.height_cm
    if profile_in.weight_kg is not None:
        current_user.weight_kg = profile_in.weight_kg
    if profile_in.activity_level is not None:
        current_user.activity_level = profile_in.activity_level
    if profile_in.goal is not None:
        current_user.goal = profile_in.goal

    # Recalculate targets based on updated profile
    targets = calculate_daily_calorie_and_macro_targets(
        age=current_user.age,
        gender=current_user.gender,
        height_cm=current_user.height_cm,
        weight_kg=current_user.weight_kg,
        activity_level=current_user.activity_level,
        goal=current_user.goal
    )
    current_user.daily_calorie_target = targets["daily_calorie_target"]
    current_user.protein_target = targets["protein_target"]
    current_user.carb_target = targets["carb_target"]
    current_user.fat_target = targets["fat_target"]
    current_user.daily_water_target_ml = targets["daily_water_target_ml"]

    await db.commit()
    await db.refresh(current_user)
    return ProfileOut.model_validate(current_user)

@router.put("/goals", response_model=ProfileOut)
async def update_goals(
    goals_in: GoalsUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if goals_in.daily_calorie_target is not None:
        current_user.daily_calorie_target = goals_in.daily_calorie_target
    if goals_in.protein_target is not None:
        current_user.protein_target = goals_in.protein_target
    if goals_in.carb_target is not None:
        current_user.carb_target = goals_in.carb_target
    if goals_in.fat_target is not None:
        current_user.fat_target = goals_in.fat_target
    if goals_in.daily_water_target_ml is not None:
        current_user.daily_water_target_ml = goals_in.daily_water_target_ml

    await db.commit()
    await db.refresh(current_user)
    return ProfileOut.model_validate(current_user)
