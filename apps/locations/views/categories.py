# Python modules
from typing import Any

# Django modules
from django.db.models import QuerySet, Q

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
from apps.locations.models import Category
from apps.locations.serializers.categories import (
    CategoryListSerializer,
    CategoryCreateSerializer,
    CategoryUpdateSerializer,
)


class CategoryViewSet(ViewSet):
    """
    ViewSet for handling Category-related endpoints.
    """
    permission_classes = (AllowAny,)
    serializer_class = CategoryListSerializer
    
    @extend_schema(
        tags=["Locations: Categories"],
        description="List categories with optional search by name and filtering by parent.",
        parameters=[
            OpenApiParameter(name="search", description="Search by category name", required=False, type=str),
            OpenApiParameter(name="parent", description="Filter by parent category ID", required=False, type=int),
        ],
        responses={200: CategoryListSerializer(many=True)}
    )
    def list(
        self,
        request: DRFRequest,
        *args: tuple[Any, ...],
        **kwargs: dict[str, Any]
    ) -> DRFResponse:
        """
        Handle GET requests to list categories.
        """
        queryset: QuerySet[Category] = Category.objects.select_related("parent").all().order_by("name")

        # Manual Filtering
        search_query = request.query_params.get("search")
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)

        parent_id = request.query_params.get("parent")
        if parent_id:
            queryset = queryset.filter(parent_id=parent_id)
        
        serializer: CategoryListSerializer = CategoryListSerializer(
            queryset,
            many=True
        )

        return DRFResponse(
            data=serializer.data,
            status=HTTP_200_OK
        )

    @extend_schema(tags=["Locations: Categories"], request=CategoryCreateSerializer, responses={201: CategoryCreateSerializer})
    def create(self, request: DRFRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        """
        Handle POST requests to create a new category.
        """
        serializer: CategoryCreateSerializer = CategoryCreateSerializer(
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

    @extend_schema(tags=["Locations: Categories"], responses={200: CategoryListSerializer})
    def retrieve(self, request: DRFRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        """
        Handle GET requests to retrieve a specific category.
        """
        try:
            instance: Category = Category.objects.select_related("parent").get(id=kwargs["pk"])
        except Category.DoesNotExist:
            return DRFResponse(
                data={"detail": f"Category with id={kwargs['pk']} does not exist."},
                status=HTTP_404_NOT_FOUND
            )

        serializer: CategoryListSerializer = CategoryListSerializer(instance)
        
        return DRFResponse(
            data=serializer.data,
            status=HTTP_200_OK
        )

    @extend_schema(tags=["Locations: Categories"], request=CategoryUpdateSerializer)
    def partial_update(self, request: DRFRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        """
        Handle PATCH requests to partially update a category.
        """
        try:
            instance: Category = Category.objects.get(id=kwargs["pk"])
        except Category.DoesNotExist:
            return DRFResponse(
                data={"detail": f"Category with id={kwargs['pk']} does not exist."},
                status=HTTP_404_NOT_FOUND
            )

        serializer: CategoryUpdateSerializer = CategoryUpdateSerializer(
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

    @extend_schema(tags=["Locations: Categories"])
    def destroy(self, request: DRFRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        """
        Handle DELETE requests to delete a category.
        """
        try:
            instance: Category = Category.objects.get(id=kwargs["pk"])
        except Category.DoesNotExist:
            return DRFResponse(
                data={"detail": f"Category with id={kwargs['pk']} does not exist."},
                status=HTTP_404_NOT_FOUND
            )

        instance.delete()

        return DRFResponse(status=HTTP_204_NO_CONTENT)