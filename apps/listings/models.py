from django.conf import settings
from django.db import models

from apps.abstracts.models import AbstractBaseModel


class Property(AbstractBaseModel):
    """
    Physical property object (apartment, house, commercial and etc.).
    Can have multiple listings (Listing).
    """

    TITLE_MAX_LEN = 100
    PROPERTY_TYPE_MAX_LEN = 20
    ADDRESS_MAX_LEN = 100
    TOTAL_MAX_DIGITS = 7
    TOTAL_DECIMAL_PLACES = 2
    MAP_MAX_DIGITS = 9
    MAX_DECIMAL_PLACES = 6

    class PropertyType(models.TextChoices):
        APARTMENT = "apartment", "Apartment"
        HOUSE = "house", "House"
        COMMERCIAL = "commercial", "Commercial"
        LAND = "land", "Land"

    title = models.CharField(
        max_length=TITLE_MAX_LEN,
        help_text="Short name of the property, for example: '2-bedroom apartment, Samal'",
    )
    property_type = models.CharField(
        max_length=20,
        choices=PropertyType.choices,
        default=PropertyType.APARTMENT,
    )

    city = models.CharField(max_length=TITLE_MAX_LEN)
    address = models.CharField(max_length=ADDRESS_MAX_LEN)

    rooms = models.PositiveSmallIntegerField(
        help_text="Number of rooms",
    )
    total_area = models.DecimalField(
        max_digits=TOTAL_MAX_DIGITS,
        decimal_places=TOTAL_DECIMAL_PLACES,
        help_text="Total area, m²",
    )
    living_area = models.DecimalField(
        max_digits=TOTAL_MAX_DIGITS,
        decimal_places=TOTAL_DECIMAL_PLACES,
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
        max_digits=MAP_MAX_DIGITS,
        decimal_places=MAX_DECIMAL_PLACES,
        null=True,
        blank=True,
    )
    longitude = models.DecimalField(
        max_digits=MAP_MAX_DIGITS,
        decimal_places=MAX_DECIMAL_PLACES,
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

    TITLE_MAX_LEN = 100
    PRICE_MAX_DIGITS = 12
    PRICE_DECIMAL_PLACES = 2
    CURRENCY_MAX_LEN = 3
    STATUS_MAX_LEN = 20

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

    title = models.CharField(max_length=TITLE_MAX_LEN)
    description = models.TextField(blank=True)

    price = models.DecimalField(
        max_digits=PRICE_MAX_DIGITS,
        decimal_places=PRICE_DECIMAL_PLACES,
    )
    currency = models.CharField(
        max_length=CURRENCY_MAX_LEN,
        default="KZT",  
    )

    status = models.CharField(
        max_length=STATUS_MAX_LEN,
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

    ORDER_DEFAULT = 0

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
        default=ORDER_DEFAULT,
        help_text="Order of sorting",
    )

    def __str__(self) -> str:
        return f"Photo #{self.pk} for listing {self.listing_id}"
