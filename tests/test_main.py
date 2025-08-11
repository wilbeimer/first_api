import sqlite3

import pytest
from fastapi.testclient import TestClient

from app.main import app, create_tasks_table
from app.models import Task


@pytest.fixture()
def client_with_db():
    Task._connection = sqlite3.connect(":memory:", check_same_thread=False)
    create_tasks_table()
    client = TestClient(app)
    yield client
    Task._connection.close()
    Task._connection = None


def create_task(client, title: str = "Default task"):
    response = client.post("/tasks/", json={"title": title})
    return response


def test_root(client_with_db):
    response = client_with_db.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_post_task(client_with_db):
    response = create_task(client_with_db)
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert isinstance(data["id"], int)
    assert data["title"] == "Default task"
    assert data["completed"] is False

    # Post requires data
    response = client_with_db.post(
        "/tasks/",
    )
    assert response.status_code == 422


def test_get_all_tasks(client_with_db):
    response = create_task(client_with_db)
    assert response.status_code == 201

    response = client_with_db.get("/tasks")
    assert response.status_code == 200
    tasks = response.json()
    assert isinstance(tasks, list)
    assert all(
        task["title"] == "Default task" and task["completed"] == False for task in tasks
    ), f"Expected to find 'Default task' in {tasks}"


def test_get_task_by_id(client_with_db):
    created = create_task(client_with_db, "Test get")
    assert created.status_code == 201
    created_id = created.json()["id"]
    created_title = created.json()["title"]

    response = client_with_db.get(f"/tasks/{created_id}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["completed"], bool)
    assert data["id"] == created_id
    assert data["title"] == created_title

    response = client_with_db.get("/tasks/9999999")
    assert response.status_code == 404


def test_delete_task(client_with_db):
    created = create_task(client_with_db)
    assert created.status_code == 201
    created_id = created.json()["id"]

    response = client_with_db.delete(f"/tasks/{created_id}")
    assert response.status_code == 204

    # Check that task was deleted
    response = client_with_db.get(f"/tasks/{created_id}")
    assert response.status_code == 404

    response = client_with_db.delete("/tasks/99999")
    assert response.status_code == 404


def test_put_task(client_with_db):
    created = create_task(client_with_db)
    assert created.status_code == 201
    created_id = created.json()["id"]

    response = client_with_db.put(
        f"/tasks/{created_id}", json={"title": "Updated Title", "completed": True}
    )
    assert response.status_code == 200

    response = client_with_db.put(
        f"/tasks/{2}", json={"title": "Updated Title", "completed": True}
    )
    assert response.status_code == 404

    response = client_with_db.put(
        f"/tasks/{created_id}", json={"title": "Updated Title"}
    )
    assert response.status_code == 422


    response = client_with_db.put(
        f"/tasks/{created_id}", json={"title": True, "completed": "yes"}
    )
    assert response.status_code == 422

    response = client_with_db.put(f"/tasks/{created_id}", json={})
    assert response.status_code == 422
