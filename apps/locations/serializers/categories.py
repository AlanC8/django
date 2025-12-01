from rest_framework import serializers
from apps.locations.models import Category


class CategorySerializer(serializers.ModelSerializer):
    parent_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        write_only=True,
        source="parent",
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "slug",
            "parent",
            "parent_id",
        ]
        read_only_fields = ["id", "slug"]
