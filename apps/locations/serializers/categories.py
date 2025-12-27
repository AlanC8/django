# Python modules
from typing import Any

# Django REST Framework modules
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
)

# Project modules
from apps.locations.models import Category


class CategoryBaseSerializer(ModelSerializer):
    """
    Base serializer for Category instances.
    """
    class Meta:
        """
        Customize the serializer's metadata.
        """
        model = Category
        fields = "__all__"


class CategoryListSerializer(CategoryBaseSerializer):
    """
    Serializer for listing Category instances.
    """
    parent_name = SerializerMethodField()

    class Meta:
        """
        Customize the serializer's metadata.
        """
        model = Category
        fields = (
            "id",
            "name",
            "slug",
            "parent",
            "parent_name",
        )

    def get_parent_name(self, obj: Category) -> str:
        """
        Get the name of the parent category.
        """
        return obj.parent.name if obj.parent else ""


class CategoryCreateSerializer(CategoryBaseSerializer):
    """
    Serializer for creating Category instances.
    """
    class Meta:
        """
        Customize the serializer's metadata.
        """
        model = Category
        fields = (
            "name",
            "slug",
            "parent",
        )


class CategoryUpdateSerializer(CategoryBaseSerializer):
    """
    Serializer for updating Category instances.
    """
    class Meta:
        """
        Customize the serializer's metadata.
        """
        model = Category
        fields = (
            "name",
            "slug",
            "parent",
        )