from fastapi.testclient import TestClient
from app.api import app, reset_demo_db

reset_demo_db()

client = TestClient(app)


def test_create_and_read_task():
    # create unit and member for assignment
    r = client.post("/units/", json={"name": "201"})
    unit_id = r.json()["id"]
    r = client.post(
        "/members/",
        json={"name": "Carol", "email": "carol@example.com", "unit_id": unit_id},
    )
    member_id = r.json()["id"]

    # create task
    r = client.post("/tasks/", json={"title": "Fix sink", "assignee_id": member_id})
    assert r.status_code == 200
    task_id = r.json()["id"]

    # list tasks
    r = client.get("/tasks/")
    assert r.status_code == 200
    tasks = r.json()
    assert any(t["id"] == task_id for t in tasks)

    # get single task
    r = client.get(f"/tasks/{task_id}")
    assert r.status_code == 200
    assert r.json()["title"] == "Fix sink"

    # update task
    r = client.put(
        f"/tasks/{task_id}",
        json={
            "title": "Fix sink - updated",
            "status": "in_progress",
            "priority": "high",
        },
    )
    assert r.status_code == 200
    assert r.json()["status"] == "in_progress"
    assert r.json()["title"] == "Fix sink - updated"

    # delete task
    r = client.delete(f"/tasks/{task_id}")
    assert r.status_code == 200
    r = client.get(f"/tasks/{task_id}")
    assert r.json() is None
