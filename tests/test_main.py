# tests/test_main.py
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models import Task

client = TestClient(app)


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


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
