from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import UserRegister, UserLogin, TokenResponse, UserOut
from app.core.security import hash_password, verify_password, create_access_token
from app.core.exceptions import BadRequestException, CredentialsException
from app.services.nutrition_calc import calculate_daily_calorie_and_macro_targets
from app.api.deps import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserRegister, db: AsyncSession = Depends(get_db)):
    # Check if user already exists
    existing_result = await db.execute(select(User).where(User.email == user_in.email.lower()))
    if existing_result.scalar_one_or_none():
        raise BadRequestException("An account with this email already exists.")
    
    # Calculate initial targets based on profile
    targets = calculate_daily_calorie_and_macro_targets(
        age=user_in.age,
        gender=user_in.gender,
        height_cm=user_in.height_cm,
        weight_kg=user_in.weight_kg,
        activity_level=user_in.activity_level or "moderate",
        goal=user_in.goal or "maintain"
    )
    
    # Create user
    new_user = User(
        name=user_in.name.strip(),
        email=user_in.email.lower().strip(),
        password_hash=hash_password(user_in.password),
        age=user_in.age,
        gender=user_in.gender,
        height_cm=user_in.height_cm,
        weight_kg=user_in.weight_kg,
        activity_level=user_in.activity_level or "moderate",
        goal=user_in.goal or "maintain",
        daily_calorie_target=targets["daily_calorie_target"],
        protein_target=targets["protein_target"],
        carb_target=targets["carb_target"],
        fat_target=targets["fat_target"],
        daily_water_target_ml=targets["daily_water_target_ml"],
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    token = create_access_token(new_user.id)
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user=UserOut.model_validate(new_user)
    )

@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == credentials.email.lower().strip()))
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(credentials.password, user.password_hash):
        raise CredentialsException("Invalid email or password.")
        
    token = create_access_token(user.id)
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user=UserOut.model_validate(user)
    )

@router.get("/me", response_model=UserOut)
async def get_me(current_user: User = Depends(get_current_user)):
    return UserOut.model_validate(current_user)
