# Python modules
from typing import Any

# Django REST Framework modules
from rest_framework.serializers import ModelSerializer

# Project modules
from apps.locations.models import District
from apps.locations.serializers.cities import CityListSerializer


class DistrictBaseSerializer(ModelSerializer):
    """
    Base serializer for District instances.
    """
    class Meta:
        """
        Customize the serializer's metadata.
        """
        model = District
        fields = "__all__"


class DistrictListSerializer(DistrictBaseSerializer):
    """
    Serializer for listing District instances.
    """
    # Используем вложенный сериализатор для отображения данных города
    city = CityListSerializer(read_only=True)

    class Meta:
        """
        Customize the serializer's metadata.
        """
        model = District
        fields = (
            "id",
            "name",
            "slug",
            "city",
        )


class DistrictCreateSerializer(DistrictBaseSerializer):
    """
    Serializer for creating District instances.
    """
    # Поле 'city' здесь ожидает ID города (стандартное поведение ModelSerializer)
    class Meta:
        """
        Customize the serializer's metadata.
        """
        model = District
        fields = (
            "name",
            "slug",
            "city",
        )


class DistrictUpdateSerializer(DistrictBaseSerializer):
    """
    Serializer for updating District instances.
    """
    class Meta:
        """
        Customize the serializer's metadata.
        """
        model = District
        fields = (
            "name",
            "slug",
            "city",
        )