from typing import Any

from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from apps.listings.models import Listing
from apps.listings.serializers.listings import ListingSerializer
from apps.listings.filters.listings import ListingFilter


class ListingViewSet(viewsets.ModelViewSet):
    """CRUD + Filter + Sort + Pagination for Listing model."""

    queryset = Listing.objects.all().select_related("property", "owner")
    serializer_class = ListingSerializer
    filterset_class = ListingFilter
    # Auth required by default; publish list is explicitly opened below.
    permission_classes = [permissions.IsAuthenticated]

    ordering_fields = ["price", "published_at"]
    search_fields = ["title", "description"]

    def get_queryset(self):
        qs = super().get_queryset()
        if self.action == "my_listings":
            return qs.filter(owner=self.request.user)
        if self.action in ("published_listings", "list"):
            return qs.filter(status=Listing.Status.PUBLISHED)
        return qs

    def get_permissions(self):
        """Allow public access for published list; auth required otherwise."""
        if self.action in ("published_listings",):
            return [permissions.AllowAny()]
        return super().get_permissions()

    def perform_create(self, serializer: ListingSerializer) -> None:
        """Bind owner to current user on create."""
        serializer.save(owner=self.request.user)

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
        methods=["GET"],
        detail=False,
        url_path="published",
        permission_classes=[permissions.AllowAny],
    )
    def published_listings(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """List of published listings."""
        qs = self.get_queryset().filter(status=Listing.Status.PUBLISHED)
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
