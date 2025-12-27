import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.mark.django_db
def test_get_user_info_success(api_client: APIClient, create_user) -> None:
    user = create_user(email="me@example.com", password="validpass123")
    access = RefreshToken.for_user(user).access_token
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

    response = api_client.get("/api/auth/me")

    assert response.status_code == 200
    body = response.json()
    assert body["email"] == "me@example.com"
    assert body["id"] == user.id


@pytest.mark.django_db
def test_get_user_info_without_token_unauthorized(api_client: APIClient) -> None:
    response = api_client.get("/api/auth/me")

    assert response.status_code == 401


@pytest.mark.django_db
def test_get_user_info_with_invalid_token_unauthorized(api_client: APIClient) -> None:
    api_client.credentials(HTTP_AUTHORIZATION="Bearer invalidtoken")

    response = api_client.get("/api/auth/me")

    assert response.status_code == 401


@pytest.mark.django_db
def test_get_user_info_with_refresh_token_unauthorized(api_client: APIClient, create_user) -> None:
    user = create_user(email="me@example.com", password="validpass123")
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh}")

    response = api_client.get("/api/auth/me")

    assert response.status_code == 401
