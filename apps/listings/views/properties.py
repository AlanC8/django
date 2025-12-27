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
from drf_spectacular.utils import extend_schema

# Project modules
from apps.listings.models import Property
from apps.listings.serializers.properties import (
    PropertyBaseSerializer,
    PropertyListSerializer,
    PropertyCreateSerializer,
    PropertyUpdateSerializer,
)


class PropertyViewSet(ViewSet):
    """
    ViewSet for handling Property-related endpoints.
    """
    permission_classes = (AllowAny,)
    serializer_class = PropertyListSerializer
    
    @extend_schema(tags=["Properties"], responses={200: PropertyListSerializer(many=True)})
    def list(
        self,
        request: DRFRequest,
        *args: tuple[Any, ...],
        **kwargs: dict[str, Any]
    ) -> DRFResponse:
        """
        Handle GET requests to list properties.
        """
        queryset: QuerySet[Property] = Property.objects.all().order_by("-year_built")
        
        serializer: PropertyListSerializer = PropertyListSerializer(
            queryset,
            many=True
        )

        return DRFResponse(
            data=serializer.data,
            status=HTTP_200_OK
        )

    @extend_schema(tags=["Properties"], request=PropertyCreateSerializer, responses={201: PropertyCreateSerializer})
    def create(self, request: DRFRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        """
        Handle POST requests to create a new property.
        """
        serializer: PropertyCreateSerializer = PropertyCreateSerializer(
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

    @extend_schema(tags=["Properties"], responses={200: PropertyListSerializer})
    def retrieve(self, request: DRFRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        """
        Handle GET requests to retrieve a specific property.
        """
        try:
            instance: Property = Property.objects.get(id=kwargs["pk"])
        except Property.DoesNotExist:
            return DRFResponse(
                data={"detail": f"Property with id={kwargs['pk']} does not exist."},
                status=HTTP_404_NOT_FOUND
            )

        serializer: PropertyListSerializer = PropertyListSerializer(instance)
        
        return DRFResponse(
            data=serializer.data,
            status=HTTP_200_OK
        )

    @extend_schema(tags=["Properties"], request=PropertyUpdateSerializer)
    def partial_update(self, request: DRFRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        """
        Handle PATCH requests to partially update a property.
        """
        try:
            instance: Property = Property.objects.get(id=kwargs["pk"])
        except Property.DoesNotExist:
            return DRFResponse(
                data={"detail": f"Property with id={kwargs['pk']} does not exist."},
                status=HTTP_404_NOT_FOUND
            )

        serializer: PropertyUpdateSerializer = PropertyUpdateSerializer(
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

    @extend_schema(tags=["Properties"])
    def destroy(self, request: DRFRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        """
        Handle DELETE requests to delete a property.
        """
        try:
            instance: Property = Property.objects.get(id=kwargs["pk"])
        except Property.DoesNotExist:
            return DRFResponse(
                data={"detail": f"Property with id={kwargs['pk']} does not exist."},
                status=HTTP_404_NOT_FOUND
            )

        instance.delete()

        return DRFResponse(status=HTTP_204_NO_CONTENT)