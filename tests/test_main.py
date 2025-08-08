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
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["title"] == "test task"
    assert data["completed"] is False


def test_get_all_tasks():
    response = client.post(
        "/tasks/",
        json={"title": "test task"},
    )
    assert response.status_code == 201

    response = client.get("/tasks")
    assert response.status_code == 200
    tasks = response.json()
    assert any(
        task["title"] == "test task" and task["completed"] == False for task in tasks
    ), f"Expected to find 'test task' in {tasks}"
