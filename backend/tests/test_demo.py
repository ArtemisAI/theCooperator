from fastapi.testclient import TestClient

from app.api import app, reset_demo_db

# Ensure a clean DB for the test
reset_demo_db()
client = TestClient(app)


def test_demo_reset_endpoint():
    # Modify DB
    client.post("/units/", json={"name": "999"})
    # Reset using demo endpoint
    r = client.post("/demo/reset")
    assert r.status_code == 200

    r = client.get("/units/")
    names = [u["name"] for u in r.json()]
    assert names == ["101", "102"]

    r = client.get("/tasks/")
    titles = [t["title"] for t in r.json()]
    assert "Paint hallway" in titles and "Fix sink" in titles
