from rest_framework import serializers

from apps.listings.models import Photo


class PhotoSerializer(serializers.ModelSerializer):
    """Serializer for Listing Photo model."""

    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Photo
        fields = [
            "id",
            "image_url",
            "is_main",
            "order",
        ]
        read_only_fields = ["id", "image_url"]

    def get_image_url(self, obj) -> str:
        request = self.context.get("request")
        url = obj.image.url if obj.image else None
        return request.build_absolute_uri(url) if request and url else url
