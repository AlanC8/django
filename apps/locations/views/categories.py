from rest_framework import viewsets, permissions
from apps.locations.models import Category
from apps.locations.serializers.categories import CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().select_related("parent")
    serializer_class = CategorySerializer
    permission_classes = (permissions.AllowAny,)

    filterset_fields = ["parent"]
    search_fields = ["name"]
    ordering_fields = ["name"]
