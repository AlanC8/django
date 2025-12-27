from django.urls import include, path
from drf_spectacular.utils import OpenApiResponse, extend_schema, inline_serializer
from rest_framework import serializers
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from apps.auths.views import UserViewSet

router: DefaultRouter = DefaultRouter(trailing_slash=False)

router.register(
    prefix="auth",
    viewset=UserViewSet,
    basename="auth",
)


class DecoratedTokenObtainPairView(TokenObtainPairView):
    @extend_schema(
        tags=["Auth"],
        summary="Login",
        description="Authenticate user with email and password to obtain JWT tokens.",
        request=inline_serializer(
            name="TokenObtainPairRequest",
            fields={
                "email": serializers.EmailField(),
                "password": serializers.CharField(),
            },
        ),
        responses={
            200: inline_serializer(
                name="TokenObtainPairResponse",
                fields={
                    "access": serializers.CharField(),
                    "refresh": serializers.CharField(),
                },
            ),
            401: OpenApiResponse(description="Invalid credentials"),
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class DecoratedTokenRefreshView(TokenRefreshView):
    @extend_schema(
        tags=["Auth"],
        summary="Refresh token",
        description="Refresh JWT access token using a valid refresh token.",
        request=inline_serializer(
            name="TokenRefreshRequest",
            fields={
                "refresh": serializers.CharField(),
            },
        ),
        responses={
            200: inline_serializer(
                name="TokenRefreshResponse",
                fields={
                    "access": serializers.CharField(),
                },
            ),
            401: OpenApiResponse(description="Invalid or expired refresh token"),
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class DecoratedTokenVerifyView(TokenVerifyView):
    @extend_schema(
        tags=["Auth"],
        summary="Verify token",
        description="Verify that a JWT token is valid.",
        request=inline_serializer(
            name="TokenVerifyRequest",
            fields={
                "token": serializers.CharField(),
            },
        ),
        responses={
            200: OpenApiResponse(description="Token is valid"),
            401: OpenApiResponse(description="Token is invalid or expired"),
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

urlpatterns = [
    path("auth/login/", DecoratedTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/refresh/", DecoratedTokenRefreshView.as_view(), name="token_refresh"),
    path("auth/verify/", DecoratedTokenVerifyView.as_view(), name="token_verify"),
    path("", include(router.urls)),
]
