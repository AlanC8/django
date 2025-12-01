from typing import Any

from rest_framework import viewsets, permissions
from rest_framework.request import Request
from rest_framework.response import Response

from apps.listings.models import Property
from apps.listings.serializers.properties import PropertySerializer


class PropertyViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing property objects (Property).
    Supports:
    - list
    - create
    - retrieve
    - partial_update
    - destroy
    With filtering, searching and sorting.
    """

    # city is a CharField, so no select_related
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = (permissions.IsAuthenticated,)

    filterset_fields = [
        "property_type",
        "city",
        "is_new_building",
        "rooms",
    ]

    search_fields = [
        "title",
        "address",
    ]

    ordering_fields = [
        "total_area",
        "living_area",
        "floor",
        "total_floors",
        "year_built",
    ]
    ordering = ["-year_built"] 

    def perform_create(self, serializer: PropertySerializer) -> None:
        """
        If needed, you can bind owner here,
        if you add the owner field to the Property.
        """
        serializer.save()
