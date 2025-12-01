from decimal import Decimal

import pytest
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.auths.models import User
from apps.listings.models import Listing, Property

pytestmark = pytest.mark.django_db


def _auth_headers(user: User) -> dict[str, str]:
    token = RefreshToken.for_user(user)
    return {"HTTP_AUTHORIZATION": f"Bearer {token.access_token}"}


@pytest.fixture
def user() -> User:
    return User.objects.create_user(email="owner@example.com", password="StrongPass123!")


@pytest.fixture
def other_user() -> User:
    return User.objects.create_user(email="other@example.com", password="StrongPass123!")


@pytest.fixture
def property_obj() -> Property:
    return Property.objects.create(
        title="Test apartment",
        property_type=Property.PropertyType.APARTMENT,
        city="Almaty",
        address="Test street 1",
        rooms=2,
        total_area=Decimal("60.00"),
        living_area=Decimal("45.00"),
        floor=3,
        total_floors=9,
        year_built=2010,
        latitude=Decimal("43.256670"),
        longitude=Decimal("76.928610"),
        is_new_building=False,
    )


@pytest.fixture
def listing(user: User, property_obj: Property) -> Listing:
    return Listing.objects.create(
        property=property_obj,
        owner=user,
        title="My listing",
        description="Nice flat",
        price=Decimal("150000000.00"),
        currency="KZT",
    )


def test_publish_listing_success(api_client: APIClient, listing: Listing, user: User) -> None:
    response = api_client.post(
        f"/api/apartments/listings/{listing.id}/publish/",
        **_auth_headers(user),
    )

    listing.refresh_from_db()
    assert response.status_code == status.HTTP_200_OK
    assert listing.status == Listing.Status.PUBLISHED
    assert listing.published_at is not None


def test_publish_listing_unauthorized(api_client: APIClient, listing: Listing) -> None:
    response = api_client.post(f"/api/apartments/listings/{listing.id}/publish/")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_publish_listing_invalid_token(api_client: APIClient, listing: Listing) -> None:
    headers = {"HTTP_AUTHORIZATION": "Bearer invalid.token"}

    response = api_client.post(
        f"/api/apartments/listings/{listing.id}/publish/",
        **headers,
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_publish_nonexistent_listing_returns_404(api_client: APIClient, user: User) -> None:
    headers = _auth_headers(user)
    response = api_client.post("/api/apartments/listings/999/publish/", **headers)

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_my_listings_returns_only_own(api_client: APIClient, listing: Listing, other_user: User) -> None:
    # Listing for a different user should not leak into the owner's response
    other_property = Property.objects.create(
        title="Other prop",
        property_type=Property.PropertyType.HOUSE,
        city="Astana",
        address="Street 2",
        rooms=4,
        total_area=Decimal("120.00"),
        living_area=Decimal("90.00"),
        year_built=2015,
        latitude=Decimal("51.160523"),
        longitude=Decimal("71.470356"),
        is_new_building=False,
    )
    Listing.objects.create(
        property=other_property,
        owner=other_user,
        title="Other listing",
        description="House",
        price=Decimal("250000000.00"),
        currency="KZT",
    )

    response = api_client.get("/api/apartments/listings/my/", **_auth_headers(listing.owner))

    assert response.status_code == status.HTTP_200_OK
    ids = [item["id"] for item in response.data]
    assert listing.id in ids
    assert all(item["owner"] == listing.owner.id for item in response.data)


def test_my_listings_unauthorized(api_client: APIClient) -> None:
    response = api_client.get("/api/apartments/listings/my/")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_my_listings_empty_for_user_without_listings(api_client: APIClient, user: User) -> None:
    response = api_client.get("/api/apartments/listings/my/", **_auth_headers(user))

    assert response.status_code == status.HTTP_200_OK
    assert response.data == []
