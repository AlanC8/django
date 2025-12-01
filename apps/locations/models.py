from django.db import models

from apps.abstracts.models import AbstractBaseModel


class City(AbstractBaseModel):
    """
    City (Almaty, Astana, Shymkent and etc.)
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)

    def __str__(self):
        return self.name


class District(AbstractBaseModel):
    """
    District of the city (for example: Bostandyk, Almaly)
    """
    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name="districts"
    )
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=150)

    class Meta:
        unique_together = ("city", "slug")
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} — {self.city.name}"


class Microdistrict(AbstractBaseModel):
    """
    Microdistrict inside the district (Samal-1, Samal-2, Orbit-3, Kokzheyek, Zhetysu 2 and etc.)
    """
    district = models.ForeignKey(
        District,
        on_delete=models.CASCADE,
        related_name="microdistricts",
    )
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=150)

    class Meta:
        unique_together = ("district", "slug")
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} — {self.district.name} ({self.district.city.name})"


class Category(AbstractBaseModel):
    """
    Категории типа недвижимости:
    - квартира
    - дом
    - участок
    - коммерция
    - гараж
    - новостройка
    и т.д.
    """

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)

    # Пример: "Жилая недвижимость", "Коммерческая", "Земельные участки"
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="children",
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    def __str__(self):
        return self.name
