# Django modules
from django.urls import include, path

# Django Rest Framework modules
from rest_framework.routers import DefaultRouter

# Project modules
from apps.locations.views.cities import CityViewSet
from apps.locations.views.districts import DistrictViewSet
from apps.locations.views.microdistricts import MicrodistrictViewSet
from apps.locations.views.categories import CategoryViewSet


router: DefaultRouter = DefaultRouter(
    trailing_slash=False
)

router.register(
    prefix="cities",
    viewset=CityViewSet,
    basename="cities",
)

router.register(
    prefix="districts",
    viewset=DistrictViewSet,
    basename="districts",
)

router.register(
    prefix="microdistricts",
    viewset=MicrodistrictViewSet,
    basename="microdistricts",
)

router.register(
    prefix="categories",
    viewset=CategoryViewSet,
    basename="categories",
)

urlpatterns = [
    path("", include(router.urls)),
]