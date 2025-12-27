from collections.abc import Callable
from decimal import Decimal

import pytest
from rest_framework_simplejwt.tokens import RefreshToken

from apps.auths.models import User
from apps.listings.models import Listing, Property


@pytest.fixture
def user() -> User:
    return User.objects.create_user(email="owner@example.com", password="StrongPass123!")


@pytest.fixture
def other_user() -> User:
    return User.objects.create_user(email="other@example.com", password="StrongPass123!")


@pytest.fixture
def auth_headers() -> Callable[[User], dict[str, str]]:
    def _build(user: User) -> dict[str, str]:
        token = RefreshToken.for_user(user)
        return {"HTTP_AUTHORIZATION": f"Bearer {token.access_token}"}

    return _build


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
