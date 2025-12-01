from typing import Any

from rest_framework import viewsets, permissions
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from apps.listings.models import Photo
from apps.listings.serializers.photos import PhotoSerializer


class PhotoViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing photo objects (Photo).
    Through urls you use:
    - list  (GET /photos/)
    - create (POST /photos/)
    - destroy (DELETE /photos/{id}/)

    retrieve / update is an action in ViewSet,
    but you don't map them in urls, so they are not exposed externally.
    """

    queryset = Photo.objects.all().select_related("listing")
    serializer_class = PhotoSerializer
    permission_classes = (permissions.AllowAny,)

    filterset_fields = [
        "listing",
        "is_main",
    ]
    ordering_fields = [
        "order",
        "id",
    ]
    ordering = ["order", "id"]

    def perform_create(self, serializer: PhotoSerializer) -> None:
        """
        You can add logic:
        - if is_main = True, reset other is_main for this listing.
        For now, just save.
        """
        serializer.save()
