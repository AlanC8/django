from django.conf import settings
from django.db import models

from apps.abstracts.models import AbstractBaseModel


class Property(AbstractBaseModel):
    """
    Physical property object (apartment, house, commercial and etc.).
    Can have multiple listings (Listing).
    """

    class PropertyType(models.TextChoices):
        APARTMENT = "apartment", "Apartment"
        HOUSE = "house", "House"
        COMMERCIAL = "commercial", "Commercial"
        LAND = "land", "Land"

    title = models.CharField(
        max_length=255,
        help_text="Short name of the property, for example: '2-bedroom apartment, Samal'",
    )
    property_type = models.CharField(
        max_length=20,
        choices=PropertyType.choices,
        default=PropertyType.APARTMENT,
    )
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=255)

    rooms = models.PositiveSmallIntegerField(
        help_text="Number of rooms",
    )
    total_area = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        help_text="Total area, m²",
    )
    living_area = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Living area, m²",
    )

    floor = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text="Floor",
    )
    total_floors = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text="Total floors in the house",
    )
    year_built = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text="Year of construction",
    )

    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
    )

    is_new_building = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.title} ({self.city})"


class Listing(AbstractBaseModel):
    """
    Listing on the website (like on krisha.kz).
    Linked to Property and user.
    """

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"
        ARCHIVED = "archived", "Archived"

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="listings",
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="listings",
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )
    currency = models.CharField(
        max_length=3,
        default="KZT",  # можешь поменять на choices
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
    )
    is_top = models.BooleanField(
        default=False,
        help_text="Top/raised listing",
    )
    published_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return f"{self.title} — {self.price} {self.currency}"


def listing_photo_upload_to(instance: "Photo", filename: str) -> str:
    """
    Path to upload photos:
    listings/<listing_id>/<filename>
    """
    return f"listings/{instance.listing_id}/{filename}"


class Photo(AbstractBaseModel):
    """
    Photo, linked to the listing.
    """

    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name="photos",
    )
    image = models.ImageField(
        upload_to=listing_photo_upload_to,
    )
    is_main = models.BooleanField(
        default=False,
        help_text="Main photo",
    )
    order = models.PositiveIntegerField(
        default=0,
        help_text="Order of sorting",
    )

    def __str__(self) -> str:
        return f"Photo #{self.pk} for listing {self.listing_id}"
