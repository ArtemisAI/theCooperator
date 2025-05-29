"""Tests for Unit CRUD endpoints."""

from __future__ import annotations

from fastapi.testclient import TestClient


def test_create_and_list_units(client: TestClient) -> None:  # noqa: D103
    res_create = client.post("/api/v1/units/", json={"label": "Unit 1A"})
    assert res_create.status_code == 201
    data_create = res_create.json()
    assert data_create["label"] == "Unit 1A"

    res_list = client.get("/api/v1/units/")
    assert res_list.status_code == 200
    data_list = res_list.json()
    assert any(u["label"] == "Unit 1A" for u in data_list)
