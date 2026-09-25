import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_water_logging_flow(client: AsyncClient, auth_headers: dict):
    log1 = await client.post("/api/v1/water", headers=auth_headers, json={"amount_ml": 250})
    assert log1.status_code == 201
    log1_id = log1.json()["id"]

    log2 = await client.post("/api/v1/water", headers=auth_headers, json={"amount_ml": 500})
    assert log2.status_code == 201

    today_res = await client.get("/api/v1/water/today", headers=auth_headers)
    assert today_res.status_code == 200
    today_data = today_res.json()
    assert today_data["total_ml"] >= 750
    assert len(today_data["logs"]) >= 2

    del_res = await client.delete(f"/api/v1/water/{log1_id}", headers=auth_headers)
    assert del_res.status_code == 204

    after_res = await client.get("/api/v1/water/today", headers=auth_headers)
    assert after_res.status_code == 200
    assert after_res.json()["total_ml"] == today_data["total_ml"] - 250
