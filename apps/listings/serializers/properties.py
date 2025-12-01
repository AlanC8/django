from rest_framework import serializers
from apps.listings.models import Property
from apps.locations.serializers.cities import CitySerializer


class PropertySerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)

    class Meta:
        model = Property
        fields = [
            "id",
            "title",
            "property_type",
            "city",
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
