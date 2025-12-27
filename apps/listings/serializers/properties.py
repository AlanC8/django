# Python modules
from typing import Any

# Django REST Framework modules
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
)

# Project modules
from apps.listings.models import Property


class PropertyBaseSerializer(ModelSerializer):
    """
    Base serializer for Property instances.
    """
    class Meta:
        """
        Customize the serializer's metadata.
        """
        model = Property
        fields = "__all__"


class PropertyListSerializer(PropertyBaseSerializer):
    """
    Serializer for listing Property instances.
    """
    city_name = SerializerMethodField()

    class Meta:
        """
        Customize the serializer's metadata.
        """
        model = Property
        fields = (
            "id",
            "title",
            "address",
            "city_name",
            "rooms",
            "floor",
            "total_floors",
            "year_built",
            "total_area",
            "living_area",
            "property_type",
        )

    def get_city_name(self, obj: Property) -> str:
        """
        Get the string representation of the city.
        """
        return str(obj.city) if obj.city else ""


class PropertyCreateSerializer(PropertyBaseSerializer):
    """
    Serializer for creating Property instances.
    """
    class Meta:
        """
        Customize the serializer's metadata.
        """
        model = Property
        fields = "__all__"


class PropertyUpdateSerializer(PropertyBaseSerializer):
    """
    Serializer for updating Property instances.
    """
    class Meta:
        """
        Customize the serializer's metadata.
        """
        model = Property
        fields = (
            "title",
            "address",
            "rooms",
        )