import pytest
from fastapi.testclient import TestClient

from app.main import app, create_tasks_table

client = TestClient(app)


@pytest.fixture(autouse=True)
def use_in_memory_db():
    create_tasks_table(db=":memory:")
    yield


def create_task(title: str = "Default task"):
    response = client.post("/tasks/", json={"title": title})
    return response


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_post_task():
    response = create_task()
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["title"] == "Default task"
    assert data["completed"] is False

    response = client.post(
        "/tasks/",
    )
    assert response.status_code == 422


def test_get_all_tasks():
    response = create_task()
    assert response.status_code == 201

    response = client.get("/tasks")
    assert response.status_code == 200
    tasks = response.json()
    assert any(
        task["title"] == "Default task" and task["completed"] == False for task in tasks
    ), f"Expected to find 'Default task' in {tasks}"


def test_get_task_by_id():
    created = create_task("Test get")
    assert created.status_code == 201
    created_id = created.json()["id"]

    response = client.get(f"/tasks/{created_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created_id
    assert data["title"] == "Test get"

    response = client.get("/tasks/9999999")
    assert response.status_code == 404
