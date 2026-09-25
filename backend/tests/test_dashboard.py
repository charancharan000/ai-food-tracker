import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_dashboard_today_calculation(client: AsyncClient, auth_headers: dict):
    meal_payload = {
        "meal_type": "Breakfast",
        "food_items": [
            {
                "name": "Oatmeal with Blueberries",
                "estimated_weight_g": 250.0,
                "calories": 320.0,
                "protein_g": 12.0,
                "carbs_g": 54.0,
                "fat_g": 6.0,
                "confidence": 0.90
            }
        ]
    }
    await client.post("/api/v1/meals", headers=auth_headers, json=meal_payload)

    await client.post("/api/v1/water", headers=auth_headers, json={"amount_ml": 500})

    response = await client.get("/api/v1/dashboard/today", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()

    assert data["calories_consumed"] == 320.0
    assert data["daily_calorie_target"] > 0
    assert data["calories_remaining"] == data["daily_calorie_target"] - 320.0
    assert data["protein"]["consumed"] == 12.0
    assert data["carbs"]["consumed"] == 54.0
    assert data["fat"]["consumed"] == 6.0
    assert data["water_consumed_ml"] == 500
    assert "Breakfast" in data["meals_by_type"]
    assert data["meals_by_type"]["Breakfast"]["calories"] == 320.0

@pytest.mark.asyncio
async def test_dashboard_summary(client: AsyncClient, auth_headers: dict):
    response = await client.get("/api/v1/dashboard/summary?timeframe=week", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["timeframe"] == "week"
    assert "daily_stats" in data
    assert len(data["daily_stats"]) == 7
