# Python modules
from typing import Any

# Django modules
from django.db.models import QuerySet

# Django REST Framework
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request as DRFRequest
from rest_framework.response import Response as DRFResponse
from rest_framework.decorators import action
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
)

# 3rd Party
from drf_spectacular.utils import extend_schema, OpenApiParameter

# Project modules
from apps.listings.models import Listing
from apps.listings.serializers.listings import (
    ListingBaseSerializer,
    ListingListSerializer,
    ListingCreateSerializer,
    ListingUpdateSerializer,
)


class ListingViewSet(ViewSet):
    """
    ViewSet for handling Listing-related endpoints.
    """
    permission_classes = (AllowAny,)
    serializer_class = ListingListSerializer
    
    @extend_schema(
        tags=["Listings"],
        parameters=[OpenApiParameter(
            name="status", description="Filter by status (e.g. 'published')", required=False, type=str)],
        responses={200: ListingListSerializer(many=True)}
    )
    def list(
        self,
        request: DRFRequest,
        *args: tuple[Any, ...],
        **kwargs: dict[str, Any]
    ) -> DRFResponse:
        """
        Handle GET requests to list listings.
        """
        queryset: QuerySet[Listing] = Listing.objects.select_related(
            "property", "owner").order_by("-published_at")

        status_param = request.query_params.get("status")
        if status_param == Listing.Status.PUBLISHED:
            queryset = queryset.filter(status=Listing.Status.PUBLISHED)

        serializer: ListingListSerializer = ListingListSerializer(
            queryset,
            many=True
        )

        return DRFResponse(
            data=serializer.data,
            status=HTTP_200_OK
        )

    @extend_schema(tags=["Listings"], request=ListingCreateSerializer, responses={201: ListingCreateSerializer})
    def create(self, request: DRFRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        """
        Handle POST requests to create a new listing.
        """
        if not request.user.is_authenticated:
            return DRFResponse(status=HTTP_403_FORBIDDEN)

        serializer: ListingCreateSerializer = ListingCreateSerializer(
            data=request.data
        )

        if not serializer.is_valid():
            return DRFResponse(
                data=serializer.errors,
                status=HTTP_400_BAD_REQUEST
            )

        # Manually assigning the owner
        serializer.save(owner=request.user)

        return DRFResponse(
            data=serializer.data,
            status=HTTP_201_CREATED
        )

    @extend_schema(tags=["Listings"], responses={200: ListingListSerializer})
    def retrieve(self, request: DRFRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        """
        Handle GET requests to retrieve a specific listing.
        """
        try:
            listing: Listing = Listing.objects.select_related(
                "property", "owner").get(id=kwargs["pk"])
        except Listing.DoesNotExist:
            return DRFResponse(
                data={
                    "detail": f"Listing with id={kwargs['pk']} does not exist."},
                status=HTTP_404_NOT_FOUND
            )

        serializer: ListingListSerializer = ListingListSerializer(listing)

        return DRFResponse(
            data=serializer.data,
            status=HTTP_200_OK
        )

    @extend_schema(tags=["Listings"], request=ListingUpdateSerializer)
    def partial_update(self, request: DRFRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        """
        Handle PATCH requests to partially update a listing.
        """
        try:
            listing: Listing = Listing.objects.get(id=kwargs["pk"])
        except Listing.DoesNotExist:
            return DRFResponse(
                data={
                    "detail": f"Listing with id={kwargs['pk']} does not exist."},
                status=HTTP_404_NOT_FOUND
            )

        if listing.owner != request.user:
            return DRFResponse(status=HTTP_403_FORBIDDEN)

        serializer: ListingUpdateSerializer = ListingUpdateSerializer(
            instance=listing,
            data=request.data,
            partial=True
        )

        if not serializer.is_valid():
            return DRFResponse(
                data=serializer.errors,
                status=HTTP_400_BAD_REQUEST
            )

        serializer.save()

        return DRFResponse(
            data=serializer.data,
            status=HTTP_200_OK
        )

    @extend_schema(tags=["Listings"])
    def destroy(self, request: DRFRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        """
        Handle DELETE requests to delete a listing.
        """
        try:
            listing: Listing = Listing.objects.get(id=kwargs["pk"])
        except Listing.DoesNotExist:
            return DRFResponse(
                data={
                    "detail": f"Listing with id={kwargs['pk']} does not exist."},
                status=HTTP_404_NOT_FOUND
            )

        if listing.owner != request.user:
            return DRFResponse(status=HTTP_403_FORBIDDEN)

        listing.delete()

        return DRFResponse(status=HTTP_204_NO_CONTENT)

    # --- Actions ---

    @extend_schema(tags=["Listings"], summary="Get my listings")
    @action(
        methods=("GET",),
        detail=False,
        url_path="my",
        permission_classes=(IsAuthenticated,)
    )
    def my_listings(self, request: DRFRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        """
        Handle GET requests to retrieve listings of current user.
        """
        listings: QuerySet[Listing] = Listing.objects.filter(
            owner=request.user).select_related("property", "owner")
        serializer: ListingListSerializer = ListingListSerializer(
            listings, many=True)

        return DRFResponse(
            data=serializer.data,
            status=HTTP_200_OK
        )

    @extend_schema(tags=["Listings"], summary="Publish listing")
    @action(
        methods=("POST",),
        detail=True,
        url_path="publish",
        permission_classes=(IsAuthenticated,)
    )
    def publish(self, request: DRFRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        """
        Handle POST requests to publish a listing.
        """
        try:
            listing: Listing = Listing.objects.get(id=kwargs["pk"])
        except Listing.DoesNotExist:
            return DRFResponse(
                data={
                    "detail": f"Listing with id={kwargs['pk']} does not exist."},
                status=HTTP_404_NOT_FOUND
            )

        if listing.owner != request.user:
            return DRFResponse(status=HTTP_403_FORBIDDEN)

        listing.status = Listing.Status.PUBLISHED
        listing.published_at = listing.updated_at
        listing.save()

        return DRFResponse(
            data={"message": "Listing published"},
            status=HTTP_200_OK
        )
