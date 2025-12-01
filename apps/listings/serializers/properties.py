from rest_framework import serializers
from apps.listings.models import Property


class PropertySerializer(serializers.ModelSerializer):
    city = serializers.CharField()

    class Meta:
        model = Property
        fields = [
            "id",
            "property_type",
            "city",
            "address",
            "rooms",
            "total_area",
            "living_area",
            "floor",
            "total_floors",
            "year_built",
            "latitude",
            "longitude",
            "is_new_building",
        ]
        read_only_fields = ["id"]
