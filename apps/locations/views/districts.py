from rest_framework import viewsets, permissions
from apps.locations.models import District
from apps.locations.serializers.districts import DistrictSerializer


class DistrictViewSet(viewsets.ModelViewSet):
    queryset = District.objects.all().select_related("city")
    serializer_class = DistrictSerializer
    permission_classes = (permissions.AllowAny,)

    filterset_fields = ["city"]
    search_fields = ["name"]
    ordering_fields = ["name"]
