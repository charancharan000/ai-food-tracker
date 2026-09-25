import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_food_analysis_endpoint(
    client: AsyncClient, 
    auth_headers: dict, 
    sample_food_image_bytes: bytes
):
    files = {
        "file": ("meal_photo.jpg", sample_food_image_bytes, "image/jpeg")
    }
    response = await client.post(
        "/api/v1/food/analyze",
        headers=auth_headers,
        files=files
    )
    assert response.status_code == 200
    data = response.json()
    assert "food_items" in data
    assert len(data["food_items"]) >= 1
    
    first_item = data["food_items"][0]
    assert "name" in first_item
    assert "estimated_weight_g" in first_item
    assert "calories" in first_item
    assert "protein_g" in first_item
    assert "carbs_g" in first_item
    assert "fat_g" in first_item
    assert "confidence" in first_item
    
    assert "total" in data
    assert data["total"]["calories"] > 0
    assert "notes" in data

@pytest.mark.asyncio
async def test_food_analysis_invalid_file_type(client: AsyncClient, auth_headers: dict):
    files = {
        "file": ("document.txt", b"plain text content not an image", "text/plain")
    }
    response = await client.post(
        "/api/v1/food/analyze",
        headers=auth_headers,
        files=files
    )
    assert response.status_code == 400
    assert "invalid image format" in response.json()["detail"].lower()

@pytest.mark.asyncio
async def test_food_analysis_unauthorized(client: AsyncClient, sample_food_image_bytes: bytes):
    files = {
        "file": ("meal.jpg", sample_food_image_bytes, "image/jpeg")
    }
    response = await client.post(
        "/api/v1/food/analyze",
        files=files
    )
    assert response.status_code == 401
