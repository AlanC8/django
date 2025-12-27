from django.db import models

from apps.abstracts.models import AbstractBaseModel


class City(AbstractBaseModel):
    """
    City (Almaty, Astana, Shymkent and etc.)
    """

    NAME_MAX_LEN = 100
    SLUG_MAX_LEN = 120

    name = models.CharField(max_length=NAME_MAX_LEN, unique=True)
    slug = models.SlugField(max_length=SLUG_MAX_LEN, unique=True)

    def __str__(self):
        return self.name


class District(AbstractBaseModel):
    """
    District of the city (for example: Bostandyk, Almaly)
    """

    NAME_MAX_LEN = 120
    SLUG_MAX_LEN = 150

    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="districts")
    name = models.CharField(max_length=NAME_MAX_LEN)
    slug = models.SlugField(max_length=SLUG_MAX_LEN)

    class Meta:
        unique_together = ("city", "slug")
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} — {self.city.name}"


class Microdistrict(AbstractBaseModel):
    """
    Microdistrict inside the district (Samal-1, Samal-2, Orbit-3, Kokzheyek, Zhetysu 2 and etc.)
    """

    NAME_MAX_LEN = 120
    SLUG_MAX_LEN = 150

    district = models.ForeignKey(
        District,
        on_delete=models.CASCADE,
        related_name="microdistricts",
    )
    name = models.CharField(max_length=NAME_MAX_LEN)
    slug = models.SlugField(max_length=SLUG_MAX_LEN)

    class Meta:
        unique_together = ("district", "slug")
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} — {self.district.name} ({self.district.city.name})"


class Category(AbstractBaseModel):
    """
    Category of the property.
    """

    NAME_MAX_LEN = 100
    SLUG_MAX_LEN = 120

    name = models.CharField(max_length=NAME_MAX_LEN, unique=True)
    slug = models.SlugField(max_length=SLUG_MAX_LEN, unique=True)

    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, related_name="children", null=True, blank=True
    )

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name
