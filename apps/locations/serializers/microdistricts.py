from rest_framework import serializers
from apps.locations.models import Microdistrict
from apps.locations.serializers.districts import DistrictSerializer


class MicrodistrictSerializer(serializers.ModelSerializer):
    district = DistrictSerializer(read_only=True)
    district_id = serializers.PrimaryKeyRelatedField(
        queryset=Microdistrict._meta.get_field("district").remote_field.model.objects.all(),
        write_only=True,
        source="district",
    )

    class Meta:
        model = Microdistrict
        fields = ["id", "name", "slug", "district", "district_id"]
        read_only_fields = ["id", "slug"]
