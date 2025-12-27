# Python modules
from typing import Any

# Django modules
from django.db.models import QuerySet

# Django REST Framework
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import AllowAny
from rest_framework.request import Request as DRFRequest
from rest_framework.response import Response as DRFResponse
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)

# 3rd Party
from drf_spectacular.utils import extend_schema, OpenApiParameter

# Project modules
from apps.locations.models import District
from apps.locations.serializers.districts import (
    DistrictListSerializer,
    DistrictCreateSerializer,
    DistrictUpdateSerializer,
)


class DistrictViewSet(ViewSet):
    """
    ViewSet for handling District-related endpoints.
    """
    permission_classes = (AllowAny,)
    serializer_class = DistrictListSerializer
    
    @extend_schema(
        tags=["Locations: Districts"],
        description="List districts with optional filtering by city and search by name.",
        parameters=[
            OpenApiParameter(
                name="city",
                description="Filter by city ID",
                required=False,
                type=int
            ),
            OpenApiParameter(
                name="search",
                description="Search by district name",
                required=False,
                type=str
            ),
        ],
        responses={200: DistrictListSerializer(many=True)}
    )
    def list(
        self,
        request: DRFRequest,
        *args: tuple[Any, ...],
        **kwargs: dict[str, Any]
    ) -> DRFResponse:
        """
        Handle GET requests to list districts.
        """
        queryset: QuerySet[District] = District.objects.select_related("city").all().order_by("name")

        # Manual Filtering by City
        city_id = request.query_params.get("city")
        if city_id:
            queryset = queryset.filter(city_id=city_id)

        # Manual Search by Name
        search_query = request.query_params.get("search")
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)

        serializer: DistrictListSerializer = DistrictListSerializer(
            queryset,
            many=True
        )

        return DRFResponse(
            data=serializer.data,
            status=HTTP_200_OK
        )

    @extend_schema(tags=["Locations: Districts"], request=DistrictCreateSerializer, responses={201: DistrictCreateSerializer})
    def create(self, request: DRFRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        """
        Handle POST requests to create a new district.
        """
        serializer: DistrictCreateSerializer = DistrictCreateSerializer(
            data=request.data
        )
        
        if not serializer.is_valid():
            return DRFResponse(
                data=serializer.errors,
                status=HTTP_400_BAD_REQUEST
            )
        
        serializer.save()

        return DRFResponse(
            data=serializer.data,
            status=HTTP_201_CREATED
        )

    @extend_schema(tags=["Locations: Districts"], responses={200: DistrictListSerializer})
    def retrieve(self, request: DRFRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        """
        Handle GET requests to retrieve a specific district.
        """
        try:
            instance: District = District.objects.select_related("city").get(id=kwargs["pk"])
        except District.DoesNotExist:
            return DRFResponse(
                data={"detail": f"District with id={kwargs['pk']} does not exist."},
                status=HTTP_404_NOT_FOUND
            )

        serializer: DistrictListSerializer = DistrictListSerializer(instance)
        
        return DRFResponse(
            data=serializer.data,
            status=HTTP_200_OK
        )

    @extend_schema(tags=["Locations: Districts"], request=DistrictUpdateSerializer)
    def partial_update(self, request: DRFRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        """
        Handle PATCH requests to partially update a district.
        """
        try:
            instance: District = District.objects.get(id=kwargs["pk"])
        except District.DoesNotExist:
            return DRFResponse(
                data={"detail": f"District with id={kwargs['pk']} does not exist."},
                status=HTTP_404_NOT_FOUND
            )

        serializer: DistrictUpdateSerializer = DistrictUpdateSerializer(
            instance=instance,
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

    @extend_schema(tags=["Locations: Districts"])
    def destroy(self, request: DRFRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        """
        Handle DELETE requests to delete a district.
        """
        try:
            instance: District = District.objects.get(id=kwargs["pk"])
        except District.DoesNotExist:
            return DRFResponse(
                data={"detail": f"District with id={kwargs['pk']} does not exist."},
                status=HTTP_404_NOT_FOUND
            )

        instance.delete()

        return DRFResponse(status=HTTP_204_NO_CONTENT)