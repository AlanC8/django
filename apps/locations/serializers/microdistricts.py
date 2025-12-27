# Python modules
from typing import Any

# Django REST Framework modules
from rest_framework.serializers import ModelSerializer

# Project modules
from apps.locations.models import Microdistrict
from apps.locations.serializers.districts import DistrictListSerializer


class MicrodistrictBaseSerializer(ModelSerializer):
    """
    Base serializer for Microdistrict instances.
    """
    class Meta:
        """
        Customize the serializer's metadata.
        """
        model = Microdistrict
        fields = "__all__"


class MicrodistrictListSerializer(MicrodistrictBaseSerializer):
    """
    Serializer for listing Microdistrict instances.
    """
    # Вложенный сериализатор для отображения данных района
    district = DistrictListSerializer(read_only=True)

    class Meta:
        """
        Customize the serializer's metadata.
        """
        model = Microdistrict
        fields = (
            "id",
            "name",
            "slug",
            "district",
        )


class MicrodistrictCreateSerializer(MicrodistrictBaseSerializer):
    """
    Serializer for creating Microdistrict instances.
    """
    # district принимает ID
    class Meta:
        """
        Customize the serializer's metadata.
        """
        model = Microdistrict
        fields = (
            "name",
            "slug",
            "district",
        )


class MicrodistrictUpdateSerializer(MicrodistrictBaseSerializer):
    """
    Serializer for updating Microdistrict instances.
    """
    class Meta:
        """
        Customize the serializer's metadata.
        """
        model = Microdistrict
        fields = (
            "name",
            "slug",
            "district",
        )