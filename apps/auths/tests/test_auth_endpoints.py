import pytest
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.auths.models import User

pytestmark = pytest.mark.django_db


def _auth_headers(user: User) -> dict[str, str]:
    token = RefreshToken.for_user(user)
    return {"HTTP_AUTHORIZATION": f"Bearer {token.access_token}"}


def test_register_success(api_client: APIClient) -> None:
    payload = {"email": "newuser@example.com", "password": "StrongPass123!"}

    response = api_client.post("/api/auth/register", data=payload, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["email"] == payload["email"]
    assert "access" in response.data and "refresh" in response.data
    assert User.objects.filter(email=payload["email"]).exists()


def test_register_missing_email(api_client: APIClient) -> None:
    payload = {"password": "StrongPass123!"}

    response = api_client.post("/api/auth/register", data=payload, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "email" in response.data


def test_register_missing_password(api_client: APIClient) -> None:
    payload = {"email": "user2@example.com"}

    response = api_client.post("/api/auth/register", data=payload, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "password" in response.data


def test_register_duplicate_email(api_client: APIClient) -> None:
    email = "dupe@example.com"
    User.objects.create_user(email=email, password="StrongPass123!")
    payload = {"email": email, "password": "StrongPass123!"}

    response = api_client.post("/api/auth/register", data=payload, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "email" in response.data


def test_login_success(api_client: APIClient) -> None:
    email = "login@example.com"
    password = "StrongPass123!"
    User.objects.create_user(email=email, password=password)
    payload = {"email": email, "password": password}

    response = api_client.post("/api/auth/login/", data=payload, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data and "refresh" in response.data


def test_login_wrong_password(api_client: APIClient) -> None:
    email = "loginfail@example.com"
    User.objects.create_user(email=email, password="CorrectPass123!")
    payload = {"email": email, "password": "WrongPass"}

    response = api_client.post("/api/auth/login/", data=payload, format="json")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "detail" in response.data


def test_login_missing_email(api_client: APIClient) -> None:
    payload = {"password": "StrongPass123!"}

    response = api_client.post("/api/auth/login/", data=payload, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "email" in response.data


def test_login_missing_password(api_client: APIClient) -> None:
    payload = {"email": "someone@example.com"}

    response = api_client.post("/api/auth/login/", data=payload, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "password" in response.data


def test_me_success(api_client: APIClient) -> None:
    user = User.objects.create_user(email="me@example.com", password="StrongPass123!")

    response = api_client.get("/api/auth/me", **_auth_headers(user))

    assert response.status_code == status.HTTP_200_OK
    assert response.data["email"] == user.email


def test_me_without_token(api_client: APIClient) -> None:
    response = api_client.get("/api/auth/me")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_me_with_invalid_token(api_client: APIClient) -> None:
    headers = {"HTTP_AUTHORIZATION": "Bearer invalid.token.value"}

    response = api_client.get("/api/auth/me", **headers)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_me_with_refresh_token(api_client: APIClient) -> None:
    user = User.objects.create_user(email="refresh@example.com", password="StrongPass123!")
    refresh = RefreshToken.for_user(user)
    headers = {"HTTP_AUTHORIZATION": f"Bearer {refresh}"}

    response = api_client.get("/api/auth/me", **headers)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
