"""Tests for Metrics endpoints (placeholder)."""

import pytest
from fastapi.testclient import TestClient

from app.main import create_app

@pytest.fixture(scope="session")
def client() -> TestClient:
    return TestClient(create_app())

@pytest.mark.skip(reason="TODO: implement tests for Metrics endpoints")
def test_metrics_endpoints(client: TestClient) -> None:
    pass