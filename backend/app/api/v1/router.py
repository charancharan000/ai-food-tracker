from fastapi import APIRouter
from app.api.v1.auth import router as auth_router
from app.api.v1.food import router as food_router
from app.api.v1.meals import router as meals_router
from app.api.v1.dashboard import router as dashboard_router
from app.api.v1.profile import router as profile_router
from app.api.v1.water import router as water_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(food_router)
api_router.include_router(meals_router)
api_router.include_router(dashboard_router)
api_router.include_router(profile_router)
api_router.include_router(water_router)
