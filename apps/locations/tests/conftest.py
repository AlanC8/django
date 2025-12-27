from typing import Callable

import pytest

from apps.locations.models import Category, City, District, Microdistrict


@pytest.fixture
def city_factory() -> Callable[..., City]:
    def _create(**overrides: object) -> City:
        idx = City.objects.count() + 1
        defaults = {"name": f"City {idx}", "slug": f"city-{idx}"}
        defaults.update(overrides)
        return City.objects.create(**defaults)

    return _create


@pytest.fixture
def district_factory(city_factory: Callable[..., City]) -> Callable[..., District]:
    def _create(**overrides: object) -> District:
        idx = District.objects.count() + 1
        city = overrides.pop("city", city_factory())
        defaults = {"name": f"District {idx}", "slug": f"district-{idx}", "city": city}
        defaults.update(overrides)
        return District.objects.create(**defaults)

    return _create


@pytest.fixture
def microdistrict_factory(district_factory: Callable[..., District]) -> Callable[..., Microdistrict]:
    def _create(**overrides: object) -> Microdistrict:
        idx = Microdistrict.objects.count() + 1
        district = overrides.pop("district", district_factory())
        defaults = {"name": f"Microdistrict {idx}", "slug": f"microdistrict-{idx}", "district": district}
        defaults.update(overrides)
        return Microdistrict.objects.create(**defaults)

    return _create


@pytest.fixture
def category_factory() -> Callable[..., Category]:
    def _create(**overrides: object) -> Category:
        idx = Category.objects.count() + 1
        defaults = {"name": f"Category {idx}", "slug": f"category-{idx}", "parent": None}
        defaults.update(overrides)
        return Category.objects.create(**defaults)

    return _create
