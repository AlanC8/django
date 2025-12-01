from django.urls import path

from .views.cities import CityViewSet
from .views.districts import DistrictViewSet
from .views.microdistricts import MicrodistrictViewSet
from .views.categories import CategoryViewSet


city_list = CityViewSet.as_view(
    {
        "get": "list",
        "post": "create"
    }
)
city_detail = CityViewSet.as_view(

    {
        "get": "retrieve",
        "patch": "partial_update",
        "delete": "destroy",
    }
)

district_list = DistrictViewSet.as_view({"get": "list", "post": "create"})

district_detail = DistrictViewSet.as_view(
    {
        "get": "retrieve",
        "patch": "partial_update",
        "delete": "destroy",
    },
)

microdistrict_list = MicrodistrictViewSet.as_view(
    {
        "get": "list",
        "post": "create",
    }
)
microdistrict_detail = MicrodistrictViewSet.as_view(
    {
        "get": "retrieve",
        "patch": "partial_update",
        "delete": "destroy",
    }
)

category_list = CategoryViewSet.as_view({"get": "list", "post": "create"})

category_detail = CategoryViewSet.as_view(
    {
        "get": "retrieve",
        "patch": "partial_update",
        "delete": "destroy",
    }
)

urlpatterns = [
    path("cities/", city_list),
    path("cities/<int:pk>/", city_detail),

    path("districts/", district_list),
    path("districts/<int:pk>/", district_detail),

    path("microdistricts/", microdistrict_list),
    path("microdistricts/<int:pk>/", microdistrict_detail),

    path("categories/", category_list),
    path("categories/<int:pk>/", category_detail),
]
