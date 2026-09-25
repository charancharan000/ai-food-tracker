from datetime import date, datetime, timezone
from typing import List, Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.water_log import WaterLog
from app.schemas.water import WaterLogCreate, WaterLogOut, WaterTodayResponse
from app.core.exceptions import NotFoundException

router = APIRouter(prefix="/water", tags=["Water Tracking"])

@router.post("", response_model=WaterLogOut, status_code=status.HTTP_201_CREATED)
async def log_water(
    water_in: WaterLogCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    log_date = water_in.date or datetime.now(timezone.utc).date()
    new_log = WaterLog(
        user_id=current_user.id,
        date=log_date,
        amount_ml=water_in.amount_ml
    )
    db.add(new_log)
    await db.commit()
    await db.refresh(new_log)
    return new_log

@router.get("/today", response_model=WaterTodayResponse)
async def get_water_today(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    today = datetime.now(timezone.utc).date()
    result = await db.execute(
        select(WaterLog)
        .where(and_(WaterLog.user_id == current_user.id, WaterLog.date == today))
        .order_by(WaterLog.created_at.desc())
    )
    logs = result.scalars().all()
    
    total_ml = sum(log.amount_ml for log in logs)
    target_ml = current_user.daily_water_target_ml or 2500
    remaining_ml = max(0, target_ml - total_ml)
    percentage = min(100.0, round((total_ml / target_ml) * 100, 1)) if target_ml > 0 else 0.0

    return WaterTodayResponse(
        date=today,
        total_ml=total_ml,
        target_ml=target_ml,
        remaining_ml=remaining_ml,
        percentage=percentage,
        logs=[WaterLogOut.model_validate(l) for l in logs]
    )

@router.delete("/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_water_log(
    log_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(WaterLog).where(and_(WaterLog.id == log_id, WaterLog.user_id == current_user.id))
    )
    log = result.scalar_one_or_none()
    if not log:
        raise NotFoundException(f"Water log entry {log_id} not found.")

    await db.delete(log)
    await db.commit()
    return None
