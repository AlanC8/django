# Python modules
from typing import Optional

# Django modules
from django.db.models import (
    CharField,
    SlugField,
    ForeignKey,
    CASCADE,
    UniqueConstraint,
)

# Project modules
from apps.abstracts.models import AbstractBaseModel


class City(AbstractBaseModel):
    """
    City database model (Almaty, Astana, etc.).
    """

    NAME_MAX_LEN = 100
    SLUG_MAX_LEN = 120

    name = CharField(
        max_length=NAME_MAX_LEN,
        unique=True,
    )
    slug = SlugField(
        max_length=SLUG_MAX_LEN,
        unique=True,
    )

    def __repr__(self) -> str:
        return f"City(id={self.id}, name={self.name})"

    def __str__(self) -> str:
        return self.name


class District(AbstractBaseModel):
    """
    District of the city (Bostandyk, Almaly).
    """

    NAME_MAX_LEN = 120
    SLUG_MAX_LEN = 150

    city = ForeignKey(
        to=City,
        on_delete=CASCADE,
        related_name="districts",
    )
    name = CharField(
        max_length=NAME_MAX_LEN,
    )
    slug = SlugField(
        max_length=SLUG_MAX_LEN,
    )

    class Meta:
        ordering = ["name"]
        unique_together = ("city", "slug")

    def __repr__(self) -> str:
        return f"District(id={self.id}, name={self.name}, city_id={self.city_id})"

    def __str__(self) -> str:
        return f"{self.name} — {self.city.name}"


class Microdistrict(AbstractBaseModel):
    """
    Microdistrict inside the district (Samal-1, Orbit-3).
    """

    NAME_MAX_LEN = 120
    SLUG_MAX_LEN = 150

    district = ForeignKey(
        to=District,
        on_delete=CASCADE,
        related_name="microdistricts",
    )
    name = CharField(
        max_length=NAME_MAX_LEN,
    )
    slug = SlugField(
        max_length=SLUG_MAX_LEN,
    )

    class Meta:
        ordering = ["name"]
        unique_together = ("district", "slug")

    def __repr__(self) -> str:
        return f"Microdistrict(id={self.id}, name={self.name}, district_id={self.district_id})"

    def __str__(self) -> str:
        return f"{self.name} — {self.district.name}"


class Category(AbstractBaseModel):
    """
    Category of the property (Residential, Commercial, etc.).
    """

    NAME_MAX_LEN = 100
    SLUG_MAX_LEN = 120

    name = CharField(
        max_length=NAME_MAX_LEN,
        unique=True,
    )
    slug = SlugField(
        max_length=SLUG_MAX_LEN,
        unique=True,
    )
    parent = ForeignKey(
        to="self",
        on_delete=CASCADE,
        related_name="children",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __repr__(self) -> str:
        return f"Category(id={self.id}, name={self.name})"

    def __str__(self) -> str:
        return self.name