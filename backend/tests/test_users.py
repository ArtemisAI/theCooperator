"""Tests for User CRUD + login."""

from __future__ import annotations

from fastapi.testclient import TestClient


def _create_user(client: TestClient, email: str = "alice@example.com") -> dict:  # noqa: D401
    payload = {"email": email, "password": "secret", "full_name": "Alice"}
    resp = client.post("/api/v1/users/", json=payload)
    assert resp.status_code == 201, resp.text
    return resp.json()


def test_create_and_list_users(client: TestClient) -> None:  # noqa: D103
    user_obj = _create_user(client)

    resp_list = client.get("/api/v1/users/")
    assert resp_list.status_code == 200
    assert any(u["id"] == user_obj["id"] for u in resp_list.json())


def test_login_endpoint(client: TestClient) -> None:  # noqa: D103
    _create_user(client, email="bob@example.com")

    resp_login = client.post(
        "/api/v1/auth/login",
        json={"email": "bob@example.com", "password": "secret"},
    )
    assert resp_login.status_code == 200, resp_login.text
    token = resp_login.json()
    assert token["access_token"].startswith("ey"), token
