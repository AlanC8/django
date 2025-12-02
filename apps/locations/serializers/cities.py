from rest_framework import serializers

from apps.locations.models import City


class CitySerializer(serializers.ModelSerializer):
    """Serializer for City model."""

    class Meta:
        model = City
        fields = [
            "id",
            "name",
            "slug",
        ]
        read_only_fields = ["id", "slug"]
