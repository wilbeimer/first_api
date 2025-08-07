import pytest
from fastapi.testclient import TestClient

from app.main import app, create_tasks_table

client = TestClient(app)


@pytest.fixture(autouse=True)
def use_in_memory_db():
    create_tasks_table(db=":memory:")
    yield


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_post_task():
    response = client.post(
        "/tasks/",
        json={"title": "test task"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["title"] == "test task"
    assert data["completed"] is False
