# Python modules
from typing import Any

# Django REST Framework modules
from rest_framework.serializers import ModelSerializer

# Project modules
from apps.locations.models import City


class CityBaseSerializer(ModelSerializer):
    """
    Base serializer for City instances.
    """
    class Meta:
        """
        Customize the serializer's metadata.
        """
        model = City
        fields = "__all__"


class CityListSerializer(CityBaseSerializer):
    """
    Serializer for listing City instances.
    """
    class Meta:
        """
        Customize the serializer's metadata.
        """
        model = City
        fields = (
            "id",
            "name",
            "slug",
        )


class CityCreateSerializer(CityBaseSerializer):
    """
    Serializer for creating City instances.
    """
    class Meta:
        """
        Customize the serializer's metadata.
        """
        model = City
        fields = (
            "name",
            "slug",
        )


class CityUpdateSerializer(CityBaseSerializer):
    """
    Serializer for updating City instances.
    """
    class Meta:
        """
        Customize the serializer's metadata.
        """
        model = City
        fields = (
            "name",
            "slug",
        )