import pytest
from rest_framework import status
from rest_framework.test import APIClient

from apps.locations.models import Microdistrict

pytestmark = pytest.mark.django_db


def test_microdistricts_list_filters_by_district(
    api_client: APIClient,
    microdistrict_factory,
) -> None:
    microdistrict = microdistrict_factory(name="Samal-1", slug="samal-1")
    microdistrict_factory(name="Orbit-2", slug="orbit-2", district=microdistrict.district)
    other_district_micro = microdistrict_factory(name="Remote", slug="remote")

    response = api_client.get("/api/locations/microdistricts", {"district": microdistrict.district_id})

    assert response.status_code == status.HTTP_200_OK
    names = [item["name"] for item in response.data]
    assert microdistrict.name in names
    assert "Orbit-2" in names
    assert other_district_micro.name not in names


def test_microdistrict_create_missing_district_returns_400(api_client: APIClient) -> None:
    response = api_client.post(
        "/api/locations/microdistricts",
        {"name": "No District", "slug": "no-district"},
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "district" in response.data


def test_microdistrict_retrieve_nonexistent_returns_404(api_client: APIClient) -> None:
    response = api_client.get("/api/locations/microdistricts/77777")

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_microdistrict_destroy_nonexistent_returns_404(api_client: APIClient) -> None:
    response = api_client.delete("/api/locations/microdistricts/55555")

    assert response.status_code == status.HTTP_404_NOT_FOUND
