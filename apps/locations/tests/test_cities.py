import pytest
from rest_framework import status
from rest_framework.test import APIClient

from apps.locations.models import City

pytestmark = pytest.mark.django_db


def test_cities_list_filters_by_search(api_client: APIClient, city_factory) -> None:
    almaty = city_factory(name="Almaty", slug="almaty")
    city_factory(name="Astana", slug="astana")

    response = api_client.get("/api/locations/cities", {"search": "alm"})

    assert response.status_code == status.HTTP_200_OK
    names = [city["name"] for city in response.data]
    assert names == [almaty.name]


def test_city_create_missing_slug_returns_400(api_client: APIClient) -> None:
    response = api_client.post(
        "/api/locations/cities",
        {"name": "New City"},
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "slug" in response.data


def test_city_retrieve_nonexistent_returns_404(api_client: APIClient) -> None:
    response = api_client.get("/api/locations/cities/999")

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_city_partial_update_empty_name_returns_400(api_client: APIClient, city_factory) -> None:
    city: City = city_factory(name="Initial", slug="initial")

    response = api_client.patch(
        f"/api/locations/cities/{city.id}",
        {"name": ""},
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "name" in response.data
