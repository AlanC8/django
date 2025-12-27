import pytest
from rest_framework import status
from rest_framework.test import APIClient

from apps.auths.models import User
from apps.listings.models import Listing

pytestmark = pytest.mark.django_db


def test_publish_listing_success(api_client: APIClient, listing: Listing, auth_headers) -> None:
    response = api_client.post(
        f"/api/apartments/listings/{listing.id}/publish",
        **auth_headers(listing.owner),
    )

    listing.refresh_from_db()
    assert response.status_code == status.HTTP_200_OK
    assert listing.status == Listing.Status.PUBLISHED
    assert listing.published_at is not None


def test_publish_listing_unauthorized(api_client: APIClient, listing: Listing) -> None:
    response = api_client.post(f"/api/apartments/listings/{listing.id}/publish")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_publish_listing_invalid_token(api_client: APIClient, listing: Listing) -> None:
    response = api_client.post(
        f"/api/apartments/listings/{listing.id}/publish",
        HTTP_AUTHORIZATION="Bearer invalid.token",
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_publish_nonexistent_listing_returns_404(api_client: APIClient, user: User, auth_headers) -> None:
    response = api_client.post(
        "/api/apartments/listings/999/publish",
        **auth_headers(user),
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_publish_listing_by_non_owner_forbidden(
    api_client: APIClient,
    listing: Listing,
    other_user: User,
    auth_headers,
) -> None:
    response = api_client.post(
        f"/api/apartments/listings/{listing.id}/publish",
        **auth_headers(other_user),
    )

    listing.refresh_from_db()
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert listing.status == Listing.Status.DRAFT
