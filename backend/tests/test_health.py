"""Smoke test for /health endpoint.

Can be executed with:
    pytest backend/tests -q
"""

import pytest
from fastapi.testclient import TestClient


# Local import inside test to avoid making theCooperator a package yet.
from app.main import create_app  # type: ignore  # noqa: E402


@pytest.fixture(scope="session")
def client() -> TestClient:  # noqa: D401 – test fixture.
    return TestClient(create_app())


def test_health_ok(client: TestClient) -> None:  # noqa: D103
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
