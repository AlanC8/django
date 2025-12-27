import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.auths.models import User


@pytest.mark.django_db
def test_register_success(api_client: APIClient) -> None:
    response = api_client.post(
        "/api/auth/register",
        {"email": "new@example.com", "password": "strongpass123"},
        format="json",
    )

    assert response.status_code == 200
    body = response.json()
    assert body["email"] == "new@example.com"
    assert "access" in body and "refresh" in body
    assert User.objects.filter(email="new@example.com").exists()


@pytest.mark.django_db
def test_register_short_password_fails(api_client: APIClient) -> None:
    response = api_client.post(
        "/api/auth/register",
        {"email": "new@example.com", "password": "short"},
        format="json",
    )

    assert response.status_code == 400
    assert "password" in response.json()


@pytest.mark.django_db
def test_register_duplicate_email_fails(api_client: APIClient, create_user) -> None:
    create_user(email="dupe@example.com")

    response = api_client.post(
        "/api/auth/register",
        {"email": "dupe@example.com", "password": "anotherpass123"},
        format="json",
    )

    assert response.status_code == 400
    assert "email" in response.json()


@pytest.mark.django_db
def test_register_authenticated_user_forbidden(api_client: APIClient, create_user) -> None:
    user = create_user()
    access = RefreshToken.for_user(user).access_token
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

    response = api_client.post(
        "/api/auth/register",
        {"email": "other@example.com", "password": "strongpass123"},
        format="json",
    )

    assert response.status_code == 403
