from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.auths.views import UserViewSet

router: DefaultRouter = DefaultRouter(trailing_slash=False)

router.register(
    prefix="auth",
    viewset=UserViewSet,
    basename="auth",
)


urlpatterns = [
    path("", include(router.urls)),
]
