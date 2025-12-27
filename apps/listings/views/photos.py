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
from apps.listings.models import Photo
from apps.listings.serializers.photos import (
    PhotoBaseSerializer,
    PhotoListSerializer,
    PhotoCreateSerializer,
)


class PhotoViewSet(ViewSet):
    """
    ViewSet for handling Photo-related endpoints.
    """
    permission_classes = (AllowAny,)
    serializer_class = PhotoListSerializer
    
    @extend_schema(tags=["Photos"], responses={200: PhotoListSerializer(many=True)})
    def list(
        self,
        request: DRFRequest,
        *args: tuple[Any, ...],
        **kwargs: dict[str, Any]
    ) -> DRFResponse:
        """
        Handle GET requests to list photos.
        """
        queryset: QuerySet[Photo] = Photo.objects.select_related("listing").all()
        
        serializer: PhotoListSerializer = PhotoListSerializer(
            queryset,
            many=True
        )

        return DRFResponse(
            data=serializer.data,
            status=HTTP_200_OK
        )

    @extend_schema(tags=["Photos"], request=PhotoCreateSerializer, responses={201: PhotoCreateSerializer})
    def create(self, request: DRFRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        """
        Handle POST requests to upload a photo.
        """
        serializer: PhotoCreateSerializer = PhotoCreateSerializer(
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

    @extend_schema(tags=["Photos"])
    def destroy(self, request: DRFRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        """
        Handle DELETE requests to delete a photo.
        """
        try:
            instance: Photo = Photo.objects.get(id=kwargs["pk"])
        except Photo.DoesNotExist:
            return DRFResponse(
                data={"detail": f"Photo with id={kwargs['pk']} does not exist."},
                status=HTTP_404_NOT_FOUND
            )

        instance.delete()

        return DRFResponse(status=HTTP_204_NO_CONTENT)