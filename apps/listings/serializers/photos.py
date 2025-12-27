from rest_framework.serializers import ModelSerializer

from apps.listings.models import Photo


class PhotoBaseSerializer(ModelSerializer):
    """
    Base serializer for Photo instances.
    """
    class Meta:
        """
        Customize the serializer's metadata.
        """
        model = Photo 
        fields = "__all__"


class PhotoListSerializer(PhotoBaseSerializer):
    """
    Serializer for listing Photo instances.
    """
    class Meta:
        """
        Customize the serializer's metadata.
        """
        model = Photo
        fields = (
            "id",
            "image",
            "order",
            "is_main",
            "listing",
        )


class PhotoCreateSerializer(PhotoBaseSerializer):
    """
    Serializer for creating Photo instances.
    """
    class Meta:
        """
        Customize the serializer's metadata.
        """
        model = Photo
        fields = (
            "image",
            "order",
            "is_main",
            "listing",
        )