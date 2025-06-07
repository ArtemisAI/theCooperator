from fastapi.testclient import TestClient

from app.api import app, Base, engine

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

client = TestClient(app)

def test_create_and_read_member():
    # create unit
    r = client.post("/units/", json={"name": "101"})
    assert r.status_code == 200
    unit_id = r.json()["id"]

    # create member
    r = client.post("/members/", json={"name": "Alice", "email": "alice@example.com", "unit_id": unit_id})
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
    assert data["email"] == "alice@example.com"

    # update member
    r = client.put(f"/members/{member_id}", json={"name": "Alice B", "email": "alice.b@example.com", "unit_id": unit_id})
    assert r.status_code == 200
    assert r.json()["name"] == "Alice B"

    # delete member
    r = client.delete(f"/members/{member_id}")
    assert r.status_code == 200
    r = client.get(f"/members/{member_id}")
    assert r.json() is None
