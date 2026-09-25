from datetime import date, timedelta
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_meal_crud_flow(client: AsyncClient, auth_headers: dict):
    meal_payload = {
        "meal_type": "Lunch",
        "notes": "Healthy balanced lunch after workout",
        "food_items": [
            {
                "name": "Chicken Biryani",
                "estimated_weight_g": 350.0,
                "servings": 1.0,
                "calories": 620.0,
                "protein_g": 32.0,
                "carbs_g": 72.0,
                "fat_g": 21.0,
                "fiber_g": 4.0,
                "sugar_g": 5.0,
                "sodium_mg": 850.0,
                "confidence": 0.85
            },
            {
                "name": "Cucumber Raita",
                "estimated_weight_g": 100.0,
                "servings": 1.0,
                "calories": 65.0,
                "protein_g": 3.5,
                "carbs_g": 6.0,
                "fat_g": 3.0,
                "fiber_g": 0.8,
                "sugar_g": 4.0,
                "sodium_mg": 180.0,
                "confidence": 0.80
            }
        ]
    }
    create_res = await client.post("/api/v1/meals", headers=auth_headers, json=meal_payload)
    assert create_res.status_code == 201
    meal_data = create_res.json()
    meal_id = meal_data["id"]
    assert meal_data["total_calories"] == 685.0
    assert len(meal_data["food_items"]) == 2

    today_res = await client.get("/api/v1/meals/today", headers=auth_headers)
    assert today_res.status_code == 200
    today_meals = today_res.json()
    assert any(m["id"] == meal_id for m in today_meals)

    get_res = await client.get(f"/api/v1/meals/{meal_id}", headers=auth_headers)
    assert get_res.status_code == 200
    assert get_res.json()["id"] == meal_id

    update_payload = {
        "meal_type": "Dinner",
        "notes": "Updated to dinner",
        "food_items": [
            {
                "name": "Chicken Biryani",
                "estimated_weight_g": 450.0,
                "servings": 1.0,
                "calories": 797.1,
                "protein_g": 41.1,
                "carbs_g": 92.6,
                "fat_g": 27.0,
                "fiber_g": 5.1,
                "sugar_g": 6.4,
                "sodium_mg": 1092.9,
                "confidence": 0.85
            }
        ]
    }
    put_res = await client.put(f"/api/v1/meals/{meal_id}", headers=auth_headers, json=update_payload)
    assert put_res.status_code == 200
    updated_data = put_res.json()
    assert updated_data["meal_type"] == "Dinner"
    assert len(updated_data["food_items"]) == 1
    assert updated_data["total_calories"] == 797.1

    del_res = await client.delete(f"/api/v1/meals/{meal_id}", headers=auth_headers)
    assert del_res.status_code == 204

    check_res = await client.get(f"/api/v1/meals/{meal_id}", headers=auth_headers)
    assert check_res.status_code == 404
