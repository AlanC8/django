import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.mark.django_db
def test_login_success(api_client: APIClient, create_user) -> None:
    create_user(email="login@example.com", password="validpass123")

    response = api_client.post(
        "/api/auth/login",
        {"email": "login@example.com", "password": "validpass123"},
        format="json",
    )

    assert response.status_code == 200
    body = response.json()
    assert body["email"] == "login@example.com"
    assert "access" in body and "refresh" in body


@pytest.mark.django_db
def test_login_wrong_password_fails(api_client: APIClient, create_user) -> None:
    create_user(email="login@example.com", password="validpass123")

    response = api_client.post(
        "/api/auth/login",
        {"email": "login@example.com", "password": "wrongpass"},
        format="json",
    )

    assert response.status_code == 400
    assert "password" in response.json()


@pytest.mark.django_db
def test_login_missing_email_fails(api_client: APIClient) -> None:
    response = api_client.post(
        "/api/auth/login",
        {"password": "validpass123"},
        format="json",
    )

    assert response.status_code == 400
    assert "email" in response.json()


@pytest.mark.django_db
def test_login_wrong_password(api_client: APIClient, create_user) -> None:
    user = create_user(email="login@example.com", password="validpass123")

    response = api_client.post(
        "/api/auth/login",
        {"email": "login@example.com", "password": "wrongpass"},
        format="json",
    )

    assert response.status_code == 400
    assert "password" in response.json()


@pytest.mark.django_db
def test_login_missing_email_fails(api_client: APIClient) -> None:
    response = api_client.post(
        "/api/auth/login",
        {"password": "validpass123"},
        format="json",
    )

    assert response.status_code == 400
    assert "email" in response.json()

