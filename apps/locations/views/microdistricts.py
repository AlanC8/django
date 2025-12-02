from rest_framework import viewsets, permissions
from apps.locations.models import Microdistrict
from apps.locations.serializers.microdistricts import MicrodistrictSerializer


class MicrodistrictViewSet(viewsets.ModelViewSet):
    queryset = Microdistrict.objects.all().select_related("district", "district__city")
    serializer_class = MicrodistrictSerializer
    permission_classes = (permissions.AllowAny,)

    filterset_fields = ["district"]
    search_fields = ["name"]
    ordering_fields = ["name"]
