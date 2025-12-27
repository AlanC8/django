from decimal import Decimal

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from apps.auths.models import User
from apps.listings.models import Listing, Property

pytestmark = pytest.mark.django_db


def test_my_listings_returns_only_own(
    api_client: APIClient,
    listing: Listing,
    other_user: User,
    auth_headers,
) -> None:
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

    response = api_client.get("/api/apartments/listings/my", **auth_headers(listing.owner))

    assert response.status_code == status.HTTP_200_OK
    ids = [item["id"] for item in response.data]
    assert listing.id in ids
    assert all(item["owner"] == listing.owner.id for item in response.data)


def test_my_listings_unauthorized(api_client: APIClient) -> None:
    response = api_client.get("/api/apartments/listings/my")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_my_listings_empty_for_user_without_listings(
    api_client: APIClient,
    user: User,
    auth_headers,
) -> None:
    response = api_client.get("/api/apartments/listings/my", **auth_headers(user))

    assert response.status_code == status.HTTP_200_OK
    assert response.data == []
