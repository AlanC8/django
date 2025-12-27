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
from apps.locations.models import Microdistrict
from apps.locations.serializers.microdistricts import (
    MicrodistrictListSerializer,
    MicrodistrictCreateSerializer,
    MicrodistrictUpdateSerializer,
)


class MicrodistrictViewSet(ViewSet):
    """
    ViewSet for handling Microdistrict-related endpoints.
    """
    permission_classes = (AllowAny,)
    serializer_class = MicrodistrictListSerializer
    
    @extend_schema(
        tags=["Locations: Microdistricts"],
        description="List microdistricts with optional filtering by district and search by name.",
        parameters=[
            OpenApiParameter(
                name="district",
                description="Filter by district ID",
                required=False,
                type=int
            ),
            OpenApiParameter(
                name="search",
                description="Search by microdistrict name",
                required=False,
                type=str
            ),
        ],
        responses={200: MicrodistrictListSerializer(many=True)}
    )
    def list(
        self,
        request: DRFRequest,
        *args: tuple[Any, ...],
        **kwargs: dict[str, Any]
    ) -> DRFResponse:
        """
        Handle GET requests to list microdistricts.
        """
        # Оптимизация запросов: тянем район и город района
        queryset: QuerySet[Microdistrict] = Microdistrict.objects.select_related(
            "district",
            "district__city"
        ).all().order_by("name")

        # Manual Filtering by District
        district_id = request.query_params.get("district")
        if district_id:
            queryset = queryset.filter(district_id=district_id)

        # Manual Search by Name
        search_query = request.query_params.get("search")
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)

        serializer: MicrodistrictListSerializer = MicrodistrictListSerializer(
            queryset,
            many=True
        )

        return DRFResponse(
            data=serializer.data,
            status=HTTP_200_OK
        )

    @extend_schema(tags=["Locations: Microdistricts"], request=MicrodistrictCreateSerializer, responses={201: MicrodistrictCreateSerializer})
    def create(self, request: DRFRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        """
        Handle POST requests to create a new microdistrict.
        """
        serializer: MicrodistrictCreateSerializer = MicrodistrictCreateSerializer(
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

    @extend_schema(tags=["Locations: Microdistricts"], responses={200: MicrodistrictListSerializer})
    def retrieve(self, request: DRFRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        """
        Handle GET requests to retrieve a specific microdistrict.
        """
        try:
            instance: Microdistrict = Microdistrict.objects.select_related(
                "district",
                "district__city"
            ).get(id=kwargs["pk"])
        except Microdistrict.DoesNotExist:
            return DRFResponse(
                data={"detail": f"Microdistrict with id={kwargs['pk']} does not exist."},
                status=HTTP_404_NOT_FOUND
            )

        serializer: MicrodistrictListSerializer = MicrodistrictListSerializer(instance)
        
        return DRFResponse(
            data=serializer.data,
            status=HTTP_200_OK
        )

    @extend_schema(tags=["Locations: Microdistricts"], request=MicrodistrictUpdateSerializer)
    def partial_update(self, request: DRFRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        """
        Handle PATCH requests to partially update a microdistrict.
        """
        try:
            instance: Microdistrict = Microdistrict.objects.get(id=kwargs["pk"])
        except Microdistrict.DoesNotExist:
            return DRFResponse(
                data={"detail": f"Microdistrict with id={kwargs['pk']} does not exist."},
                status=HTTP_404_NOT_FOUND
            )

        serializer: MicrodistrictUpdateSerializer = MicrodistrictUpdateSerializer(
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

    @extend_schema(tags=["Locations: Microdistricts"])
    def destroy(self, request: DRFRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        """
        Handle DELETE requests to delete a microdistrict.
        """
        try:
            instance: Microdistrict = Microdistrict.objects.get(id=kwargs["pk"])
        except Microdistrict.DoesNotExist:
            return DRFResponse(
                data={"detail": f"Microdistrict with id={kwargs['pk']} does not exist."},
                status=HTTP_404_NOT_FOUND
            )

        instance.delete()

        return DRFResponse(status=HTTP_204_NO_CONTENT)