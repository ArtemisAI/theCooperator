from fastapi.testclient import TestClient

from app.api import app, reset_demo_db

reset_demo_db()

client = TestClient(app)

def test_create_and_read_member():
    # create unit
    r = client.post("/units/", json={"name": "999"})
    assert r.status_code == 200
    unit_id = r.json()["id"]

    # create member
    r = client.post("/members/", json={"name": "Charlie", "email": "charlie@example.com", "unit_id": unit_id})
    assert r.status_code == 200
    member_id = r.json()["id"]

    # list members
    r = client.get("/members/")
    assert r.status_code == 200
    members = r.json()
    assert any(m["id"] == member_id for m in members)

    # get single member
    r = client.get(f"/members/{member_id}")
    assert r.status_code == 200
    data = r.json()
    assert data["email"] == "charlie@example.com"

    # update member
    r = client.put(f"/members/{member_id}", json={"name": "Charlie B", "email": "charlie.b@example.com", "unit_id": unit_id})
    assert r.status_code == 200
    assert r.json()["name"] == "Charlie B"

    # delete member
    r = client.delete(f"/members/{member_id}")
    assert r.status_code == 200
    r = client.get(f"/members/{member_id}")
    assert r.json() is None
