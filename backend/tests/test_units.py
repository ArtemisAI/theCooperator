from fastapi.testclient import TestClient

from app.api import app, Base, engine

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

client = TestClient(app)

def test_unit_crud():
    r = client.post("/units/", json={"name": "301"})
    assert r.status_code == 200
    unit_id = r.json()["id"]

    r = client.get(f"/units/{unit_id}")
    assert r.status_code == 200
    assert r.json()["name"] == "301"

    r = client.put(f"/units/{unit_id}", json={"name": "302"})
    assert r.status_code == 200
    assert r.json()["name"] == "302"

    r = client.get("/units/")
    assert any(u["id"] == unit_id for u in r.json())

    r = client.delete(f"/units/{unit_id}")
    assert r.status_code == 200
    r = client.get(f"/units/{unit_id}")
    assert r.json() is None
