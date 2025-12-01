from typing import Any

from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED

from apps.listings.models import Listing
from apps.listings.serializers.listings import ListingSerializer
from apps.listings.filters.listings import ListingFilter


class ListingViewSet(viewsets.ModelViewSet):
    """CRUD + Filter + Sort + Pagination for Listing model."""

    queryset = Listing.objects.all().select_related("property", "owner")
    serializer_class = ListingSerializer
    filterset_class = ListingFilter
    permission_classes = [permissions.AllowAny]

    ordering_fields = ["price", "published_at"]
    search_fields = ["title", "description"]

    @action(
        methods=["GET"],
        detail=False,
        url_path="my",
        permission_classes=[permissions.IsAuthenticated],
    )
    def my_listings(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """List of listings for the current user."""
        qs = self.get_queryset().filter(owner=request.user)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    @action(
        methods=["POST"],
        detail=True,
        url_path="publish",
        permission_classes=[permissions.IsAuthenticated],
    )
    def publish(self, request: Request, pk=None) -> Response:
        """Publication of the listing."""
        listing = self.get_object()
        listing.status = Listing.Status.PUBLISHED
        listing.published_at = listing.updated_at
        listing.save()
        return Response({"message": "Listing published"}, status=HTTP_200_OK)
