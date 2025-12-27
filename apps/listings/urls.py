# Django modules
from django.urls import include, path

# Django Rest Framework modules
from rest_framework.routers import DefaultRouter

# Project modules
from apps.listings.views.listings import ListingViewSet
from apps.listings.views.properties import PropertyViewSet
from apps.listings.views.photos import PhotoViewSet

router: DefaultRouter = DefaultRouter(
    trailing_slash=False
)

router.register(
    prefix="listings",
    viewset=ListingViewSet,
    basename="listings",
)

router.register(
    prefix="properties",
    viewset=PropertyViewSet,
    basename="properties",
)

router.register(
    prefix="photos",
    viewset=PhotoViewSet,
    basename="photos",
)

urlpatterns = [
    # Преподаватель использовал префикс v1, можно добавить сюда или в главном urls.py
    path("", include(router.urls)), 
]