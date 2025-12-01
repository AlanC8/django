from rest_framework import serializers

from apps.listings.models import Listing, Photo
from apps.listings.serializers.photos import PhotoSerializer


class ListingSerializer(serializers.ModelSerializer):
    photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Listing
        fields = [
            "id",
            "title",
            "description",
            "price",
            "currency",
            "status",
            "published_at",
            "is_top",
            "property",
            "owner",
            "photos",
        ]
        read_only_fields = ["id", "owner", "published_at"]
