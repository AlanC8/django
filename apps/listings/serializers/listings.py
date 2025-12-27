# Python modules
from typing import Any

# Django REST Framework modules
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
)

# Project modules
from apps.listings.models import Listing
from apps.listings.serializers.properties import PropertyListSerializer
# from apps.auths.serializers import CustomUserForeignSerializer # Подставьте свой сериализатор юзера


class ListingBaseSerializer(ModelSerializer):
    """
    Base serializer for Listing instances.
    """
    class Meta:
        """
        Customize the serializer's metadata.
        """
        model = Listing
        fields = "__all__"


class ListingListSerializer(ListingBaseSerializer):
    """
    Serializer for listing Listing instances.
    """
    status_display = SerializerMethodField()
    property = PropertyListSerializer(read_only=True)
    # owner = CustomUserForeignSerializer(read_only=True) # Раскомментируйте, если есть сериализатор

    class Meta:
        """
        Customize the serializer's metadata.
        """
        model = Listing
        fields = (
            "id",
            "title",
            "description",
            "price",
            "status",
            "status_display",
            "published_at",
            "owner",
            "property",
        )

    def get_status_display(self, obj: Listing) -> str:
        """
        Get the human-readable status label.
        """
        return obj.get_status_display()


class ListingCreateSerializer(ListingBaseSerializer):
    """
    Serializer for creating Listing instances.
    """
    class Meta:
        """
        Customize the serializer's metadata.
        """
        model = Listing
        fields = (
            "id",
            "title",
            "description",
            "price",
            "property",
        )


class ListingUpdateSerializer(ListingBaseSerializer):
    """
    Serializer for updating Listing instances.
    """
    class Meta:
        """
        Customize the serializer's metadata.
        """
        model = Listing
        fields = (
            "title",
            "description",
            "price",
        )