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

    # Title must be valid
    response = client_with_db.post("/tasks/", json={"title": ""})
    assert response.status_code == 422

    # Title must be < 100 char
    response = client_with_db.post("/tasks/", json={"title": "A" * 150})
    assert response.status_code == 422

    # Post requires data
    response = client_with_db.post(
        "/tasks/",
    )
    assert response.status_code == 422

    # Post requires data
    response = client_with_db.post("/tasks/", json={})
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

    # Check response for get nonexistant id
    response = client_with_db.get("/tasks/9999999")
    assert response.status_code == 404


def test_delete_task(client_with_db):
    created = create_task(client_with_db)
    assert created.status_code == 201
    created_id = created.json()["id"]

    response = client_with_db.delete(f"/tasks/{created_id}")
    assert response.status_code == 204

    # Check that task was properly deleted
    response = client_with_db.get(f"/tasks/{created_id}")
    assert response.status_code == 404

    # Check response for deleting nonexistant id
    response = client_with_db.delete("/tasks/99999")
    assert response.status_code == 404


def test_put_task(client_with_db):
    created = create_task(client_with_db)
    assert created.status_code == 201
    created_id = created.json()["id"]

    response = client_with_db.put(
        f"/tasks/{created_id}", json={"title": "Updated Title", "completed": True}
    )
    data = response.json()
    assert response.status_code == 200
    assert data["id"] == created_id
    assert data["title"] == "Updated Title"
    assert data["completed"] is True

    # Check response for invalid id
    response = client_with_db.put(
        f"/tasks/{2}", json={"title": "Updated Title", "completed": True}
    )
    assert response.status_code == 404

    # Put doesn't accept id
    response = client_with_db.put(
        f"/tasks/{created_id}",
        json={"id": 3, "title": "Updated Title", "completed": True},
    )
    assert response.status_code == 422

    # Put requires title and completed
    response = client_with_db.put(
        f"/tasks/{created_id}", json={"title": "Updated Title"}
    )
    assert response.status_code == 422

    # Title must be string
    response = client_with_db.put(
        f"/tasks/{created_id}", json={"title": True, "completed": True}
    )
    assert response.status_code == 422

    # Completed must be boolean
    response = client_with_db.put(
        f"/tasks/{created_id}", json={"title": "Updated Title", "completed": "yes"}
    )
    assert response.status_code == 422

    # Put requires json argument
    response = client_with_db.put(f"/tasks/{created_id}", json={})
    assert response.status_code == 422


def test_patch_task(client_with_db):
    created = create_task(client_with_db)
    assert created.status_code == 201
    created_id = created.json()["id"]

    response = client_with_db.patch(
        f"/tasks/{created_id}", json={"title": "Updated Title"}
    )
    data = response.json()
    assert response.status_code == 200
    assert data["id"] == created_id
    assert data["title"] == "Updated Title"
    assert data["completed"] is False

    # Check that patch updates title and completed
    response = client_with_db.patch(
        f"/tasks/{created_id}", json={"title": "Updated Title 2", "completed": True}
    )
    data = response.json()
    assert response.status_code == 200
    assert data["id"] == created_id
    assert data["title"] == "Updated Title 2"
    assert data["completed"] is True

    # Check that empty data is handled properly
    response = client_with_db.patch(f"/tasks/{created_id}", json={})
    data = response.json()
    assert response.status_code == 200
    assert data["id"] == created_id
    assert data["title"] == "Updated Title 2"
    assert data["completed"] is True

    # Title must be string
    response = client_with_db.put(
        f"/tasks/{created_id}", json={"title": True, "completed": True}
    )
    assert response.status_code == 422

    # Completed must be boolean
    response = client_with_db.put(
        f"/tasks/{created_id}", json={"title": "Updated Title", "completed": "yes"}
    )
    assert response.status_code == 422

    # Put requires json argument
    response = client_with_db.put(f"/tasks/{created_id}", json={})
    assert response.status_code == 422
