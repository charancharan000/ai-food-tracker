import asyncio
import io
import pytest
import pytest_asyncio
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from PIL import Image

import app.models  # ensure models loaded
from app.main import app as fastapi_app
from app.db.session import get_db
from app.models.base import Base
from app.core.config import settings

# Test database: SQLite in-memory
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    future=True
)

TestSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(autouse=True)
async def prepare_database():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    async with TestSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

fastapi_app.dependency_overrides[get_db] = override_get_db

@pytest_asyncio.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=fastapi_app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

@pytest_asyncio.fixture
async def auth_headers(client: AsyncClient) -> dict:
    # Register and login a default test user
    reg_payload = {
        "name": "Alex Nutritionist",
        "email": "alex.test@example.com",
        "password": "Password123!",
        "age": 28,
        "gender": "male",
        "height_cm": 178.0,
        "weight_kg": 75.0,
        "activity_level": "moderate",
        "goal": "maintain"
    }
    res = await client.post("/api/v1/auth/register", json=reg_payload)
    data = res.json()
    token = data["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def sample_food_image_bytes() -> bytes:
    img = Image.new("RGB", (200, 200), color=(220, 100, 50))
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG")
    return buffer.getvalue()
