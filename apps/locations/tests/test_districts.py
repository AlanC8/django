import pytest
from rest_framework import status
from rest_framework.test import APIClient

from apps.locations.models import District

pytestmark = pytest.mark.django_db


def test_districts_list_filters_by_city(api_client: APIClient, district_factory) -> None:
    district = district_factory(name="Central District", slug="central")
    district_factory(name="Other District", slug="other", city=district.city)
    another_city_district = district_factory(name="Remote", slug="remote")

    response = api_client.get("/api/locations/districts", {"city": district.city_id})

    assert response.status_code == status.HTTP_200_OK
    names = [item["name"] for item in response.data]
    assert "Central District" in names
    assert "Other District" in names
    assert all(item["city"]["id"] == district.city_id for item in response.data)
    assert another_city_district.name not in names


def test_district_create_missing_city_returns_400(api_client: APIClient) -> None:
    response = api_client.post(
        "/api/locations/districts",
        {"name": "No City", "slug": "no-city"},
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "city" in response.data


def test_district_retrieve_nonexistent_returns_404(api_client: APIClient) -> None:
    response = api_client.get("/api/locations/districts/12345")

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_district_partial_update_invalid_city_returns_400(
    api_client: APIClient,
    district_factory,
) -> None:
    district: District = district_factory()

    response = api_client.patch(
        f"/api/locations/districts/{district.id}",
        {"city": 99999},
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "city" in response.data
