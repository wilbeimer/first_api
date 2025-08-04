# tests/test_main.py
import pytest
from httpx import AsyncClient

from app.main import app
from app.models import Task


@pytest.fixture(scope="function", autouse=True)
def use_in_memory_db():
    Task.set_db_name(":memory:")

    with Task.get_db() as cursor:
        cursor.execute(
            """
                CREATE TABLE tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                completed BOOLEAN
            )
        """
        )
    yield


@pytest.mark.asyncio
async def test_root():
    async with AsyncClient(app=app, base_url="http://test") as test_client:
        response = await test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

