"""Tests for Task CRUD endpoints (placeholder)."""

import pytest
from fastapi.testclient import TestClient

from app.main import create_app

@pytest.fixture(scope="session")
def client() -> TestClient:
    return TestClient(create_app())

@pytest.mark.skip(reason="TODO: implement tests for Task endpoints")
def test_tasks_crud(client: TestClient) -> None:
    pass