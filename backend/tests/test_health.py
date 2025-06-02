"""Smoke test for /health endpoint.

Can be executed with:
    pytest backend/tests -q
"""

# import pytest # No longer needed for local fixture
from fastapi.testclient import TestClient # Keep for type hinting client from conftest


# Local import inside test to avoid making theCooperator a package yet.
# from app.main import create_app  # No longer needed as client from conftest provides the app

# @pytest.fixture(scope="session") # REMOVE this local client fixture
# def client() -> TestClient:
#     return TestClient(create_app())


def test_health_ok(client: TestClient) -> None:  # client now comes from conftest.py
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
