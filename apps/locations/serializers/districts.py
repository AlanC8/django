from rest_framework import serializers
from apps.locations.models import District
from apps.locations.serializers.cities import CitySerializer


class DistrictSerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)
    city_id = serializers.PrimaryKeyRelatedField(
        queryset=District._meta.get_field("city").remote_field.model.objects.all(),
        write_only=True,
        source="city",
    )

    class Meta:
        model = District
        fields = ["id", "name", "slug", "city", "city_id"]
        read_only_fields = ["id", "slug"]
