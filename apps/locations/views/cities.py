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
from apps.locations.models import City
from apps.locations.serializers.cities import (
    CityListSerializer,
    CityCreateSerializer,
    CityUpdateSerializer,
)


class CityViewSet(ViewSet):
    """
    ViewSet for handling City-related endpoints.
    """
    permission_classes = (AllowAny,)
    serializer_class = CityListSerializer
    
    @extend_schema(
        tags=["Locations: Cities"],
        description="List cities with optional search.",
        parameters=[
            OpenApiParameter(
                name="search",
                description="Search by city name",
                required=False,
                type=str
            ),
        ],
        responses={200: CityListSerializer(many=True)}
    )
    def list(
        self,
        request: DRFRequest,
        *args: tuple[Any, ...],
        **kwargs: dict[str, Any]
    ) -> DRFResponse:
        """
        Handle GET requests to list cities.
        """
        queryset: QuerySet[City] = City.objects.all().order_by("name")

        # Manual search implementation
        search_query = request.query_params.get("search")
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)

        serializer: CityListSerializer = CityListSerializer(
            queryset,
            many=True
        )

        return DRFResponse(
            data=serializer.data,
            status=HTTP_200_OK
        )

    @extend_schema(tags=["Locations: Cities"], request=CityCreateSerializer, responses={201: CityCreateSerializer})
    def create(self, request: DRFRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        """
        Handle POST requests to create a new city.
        """
        serializer: CityCreateSerializer = CityCreateSerializer(
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

    @extend_schema(tags=["Locations: Cities"], responses={200: CityListSerializer})
    def retrieve(self, request: DRFRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        """
        Handle GET requests to retrieve a specific city.
        """
        try:
            instance: City = City.objects.get(id=kwargs["pk"])
        except City.DoesNotExist:
            return DRFResponse(
                data={"detail": f"City with id={kwargs['pk']} does not exist."},
                status=HTTP_404_NOT_FOUND
            )

        serializer: CityListSerializer = CityListSerializer(instance)
        
        return DRFResponse(
            data=serializer.data,
            status=HTTP_200_OK
        )

    @extend_schema(tags=["Locations: Cities"], request=CityUpdateSerializer)
    def partial_update(self, request: DRFRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        """
        Handle PATCH requests to partially update a city.
        """
        try:
            instance: City = City.objects.get(id=kwargs["pk"])
        except City.DoesNotExist:
            return DRFResponse(
                data={"detail": f"City with id={kwargs['pk']} does not exist."},
                status=HTTP_404_NOT_FOUND
            )

        serializer: CityUpdateSerializer = CityUpdateSerializer(
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

    @extend_schema(tags=["Locations: Cities"])
    def destroy(self, request: DRFRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        """
        Handle DELETE requests to delete a city.
        """
        try:
            instance: City = City.objects.get(id=kwargs["pk"])
        except City.DoesNotExist:
            return DRFResponse(
                data={"detail": f"City with id={kwargs['pk']} does not exist."},
                status=HTTP_404_NOT_FOUND
            )

        instance.delete()

        return DRFResponse(status=HTTP_204_NO_CONTENT)