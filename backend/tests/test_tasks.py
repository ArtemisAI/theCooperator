"""Tests for Task CRUD endpoints (placeholder)."""

import pytest
from fastapi.testclient import TestClient

from app.main import create_app

@pytest.fixture(scope="session")
def client() -> TestClient:
    return TestClient(create_app())

def test_tasks_crud(client: TestClient) -> None:
    # Create a new task
    payload = {"title": "Test Task", "description": "Task description"}
    response = client.post("/api/v1/tasks/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    task_id = data["id"]
    assert data["title"] == payload["title"]
    # List tasks should include the new one
    list_resp = client.get("/api/v1/tasks/")
    assert list_resp.status_code == 200
    tasks = list_resp.json()
    assert any(t["id"] == task_id for t in tasks)
    # Get the task by ID
    get_resp = client.get(f"/api/v1/tasks/{task_id}")
    assert get_resp.status_code == 200
    get_data = get_resp.json()
    assert get_data["id"] == task_id
    # Update the task
    update_payload = {"title": "Updated Task", "status": "in_progress"}
    upd_resp = client.put(f"/api/v1/tasks/{task_id}", json=update_payload)
    assert upd_resp.status_code == 200
    upd_data = upd_resp.json()
    assert upd_data["title"] == "Updated Task"
    assert upd_data["status"] == "in_progress"
    # Delete the task
    del_resp = client.delete(f"/api/v1/tasks/{task_id}")
    assert del_resp.status_code == 204
    # Subsequent get should 404
    missing_resp = client.get(f"/api/v1/tasks/{task_id}")
    assert missing_resp.status_code == 404