import pytest
from rest_framework import status
from rest_framework.test import APIClient

from apps.locations.models import Category

pytestmark = pytest.mark.django_db


def test_categories_list_filters_by_parent(
    api_client: APIClient,
    category_factory,
) -> None:
    parent = category_factory(name="Residential", slug="residential")
    child = category_factory(name="Apartments", slug="apartments", parent=parent)
    category_factory(name="Commercial", slug="commercial")

    response = api_client.get("/api/locations/categories", {"parent": parent.id})

    assert response.status_code == status.HTTP_200_OK
    names = [item["name"] for item in response.data]
    assert child.name in names
    assert all(item["parent"] == parent.id for item in response.data)
    assert "Commercial" not in names


def test_category_create_missing_name_returns_400(api_client: APIClient) -> None:
    response = api_client.post(
        "/api/locations/categories",
        {"slug": "missing-name"},
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "name" in response.data


def test_category_retrieve_nonexistent_returns_404(api_client: APIClient) -> None:
    response = api_client.get("/api/locations/categories/4321")

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_category_partial_update_invalid_parent_returns_400(
    api_client: APIClient,
    category_factory,
) -> None:
    category: Category = category_factory(name="Land", slug="land")

    response = api_client.patch(
        f"/api/locations/categories/{category.id}",
        {"parent": 99999},
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "parent" in response.data
