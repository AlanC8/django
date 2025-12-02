from rest_framework import viewsets, permissions
from apps.locations.models import City
from apps.locations.serializers.cities import CitySerializer


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = (permissions.AllowAny,)

    search_fields = ["name"]
    ordering_fields = ["name"]
