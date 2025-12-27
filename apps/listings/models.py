# Python modules
from typing import Dict, Union

# Django modules
from django.conf import settings
from django.db.models import (
    CharField,
    DecimalField,
    PositiveSmallIntegerField,
    PositiveIntegerField,
    BooleanField,
    TextField,
    ForeignKey,
    DateTimeField,
    ImageField,
    CASCADE,
)

# Project modules
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

    # Style: Constants for choices instead of TextChoices
    TYPE_APARTMENT = "apartment"
    TYPE_HOUSE = "house"
    TYPE_COMMERCIAL = "commercial"
    TYPE_LAND = "land"
    
    PROPERTY_TYPE_CHOICES = {
        TYPE_APARTMENT: "Apartment",
        TYPE_HOUSE: "House",
        TYPE_COMMERCIAL: "Commercial",
        TYPE_LAND: "Land",
    }

    title = CharField(
        max_length=TITLE_MAX_LEN,
        help_text="Short name of the property, for example: '2-bedroom apartment, Samal'",
    )
    property_type = CharField(
        max_length=PROPERTY_TYPE_MAX_LEN,
        choices=PROPERTY_TYPE_CHOICES,
        default=TYPE_APARTMENT,
    )
    city = CharField(
        max_length=TITLE_MAX_LEN,
    )
    address = CharField(
        max_length=ADDRESS_MAX_LEN,
    )
    rooms = PositiveSmallIntegerField(
        help_text="Number of rooms",
    )
    total_area = DecimalField(
        max_digits=TOTAL_MAX_DIGITS,
        decimal_places=TOTAL_DECIMAL_PLACES,
        help_text="Total area, m²",
    )
    living_area = DecimalField(
        max_digits=TOTAL_MAX_DIGITS,
        decimal_places=TOTAL_DECIMAL_PLACES,
        null=True,
        blank=True,
        help_text="Living area, m²",
    )
    floor = PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text="Floor",
    )
    total_floors = PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text="Total floors in the house",
    )
    year_built = PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text="Year of construction",
    )
    latitude = DecimalField(
        max_digits=MAP_MAX_DIGITS,
        decimal_places=MAX_DECIMAL_PLACES,
        null=True,
        blank=True,
    )
    longitude = DecimalField(
        max_digits=MAP_MAX_DIGITS,
        decimal_places=MAX_DECIMAL_PLACES,
        null=True,
        blank=True,
    )
    is_new_building = BooleanField(
        default=False,
    )

    def __repr__(self) -> str:
        """Returns the official string representation of the object."""
        return f"Property(id={self.id}, title={self.title}, city={self.city})"

    def __str__(self) -> str:
        """Returns the string representation of the object."""
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

    STATUS_DRAFT = "draft"
    STATUS_PUBLISHED = "published"
    STATUS_ARCHIVED = "archived"

    STATUS_CHOICES = {
        STATUS_DRAFT: "Draft",
        STATUS_PUBLISHED: "Published",
        STATUS_ARCHIVED: "Archived",
    }

    property = ForeignKey(
        to=Property,
        on_delete=CASCADE,
        related_name="listings",
    )
    owner = ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=CASCADE,
        related_name="listings",
    )
    title = CharField(
        max_length=TITLE_MAX_LEN,
    )
    description = TextField(
        blank=True,
    )
    price = DecimalField(
        max_digits=PRICE_MAX_DIGITS,
        decimal_places=PRICE_DECIMAL_PLACES,
    )
    currency = CharField(
        max_length=CURRENCY_MAX_LEN,
        default="KZT",  
    )
    status = CharField(
        max_length=STATUS_MAX_LEN,
        choices=STATUS_CHOICES,
        default=STATUS_DRAFT,
    )
    is_top = BooleanField(
        default=False,
        help_text="Top/raised listing",
    )
    published_at = DateTimeField(
        null=True,
        blank=True,
    )

    def get_status_display(self) -> str:
        """
        Get the human-readable status label.
        Manual implementation since we use dict for choices (optional but safer).
        """
        return self.STATUS_CHOICES.get(self.status, str(self.status))

    def __repr__(self) -> str:
        """Returns the official string representation of the object."""
        return f"Listing(id={self.id}, title={self.title}, status={self.status})"

    def __str__(self) -> str:
        """Returns the string representation of the object."""
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

    listing = ForeignKey(
        to=Listing,
        on_delete=CASCADE,
        related_name="photos",
    )
    image = ImageField(
        upload_to=listing_photo_upload_to,
    )
    is_main = BooleanField(
        default=False,
        help_text="Main photo",
    )
    order = PositiveIntegerField(
        default=ORDER_DEFAULT,
        help_text="Order of sorting",
    )

    def __repr__(self) -> str:
        """Returns the official string representation of the object."""
        return f"Photo(id={self.id}, listing_id={self.listing_id})"

    def __str__(self) -> str:
        """Returns the string representation of the object."""
        return f"Photo #{self.pk} for listing {self.listing_id}"