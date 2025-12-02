from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
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
    @swagger_auto_schema(
        operation_description="Authenticate user with email and password to obtain JWT tokens.",
        operation_summary="Login",
        tags=["Auth"],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["email", "password"],
            properties={
                "email": openapi.Schema(
                    type=openapi.TYPE_STRING, description="User email"
                ),
                "password": openapi.Schema(
                    type=openapi.TYPE_STRING, description="User password"
                ),
            },
        ),
        responses={
            200: openapi.Response(
                description="Login successful",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "access": openapi.Schema(
                            type=openapi.TYPE_STRING, description="JWT access token"
                        ),
                        "refresh": openapi.Schema(
                            type=openapi.TYPE_STRING, description="JWT refresh token"
                        ),
                    },
                ),
            ),
            401: openapi.Response(description="Invalid credentials"),
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class DecoratedTokenRefreshView(TokenRefreshView):
    @swagger_auto_schema(
        operation_description="Refresh JWT access token using a valid refresh token.",
        operation_summary="Refresh token",
        tags=["Auth"],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["refresh"],
            properties={
                "refresh": openapi.Schema(
                    type=openapi.TYPE_STRING, description="JWT refresh token"
                ),
            },
        ),
        responses={
            200: openapi.Response(
                description="Token refreshed successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "access": openapi.Schema(
                            type=openapi.TYPE_STRING, description="New JWT access token"
                        ),
                    },
                ),
            ),
            401: openapi.Response(description="Invalid or expired refresh token"),
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class DecoratedTokenVerifyView(TokenVerifyView):
    @swagger_auto_schema(
        operation_description="Verify that a JWT token is valid.",
        operation_summary="Verify token",
        tags=["Auth"],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["token"],
            properties={
                "token": openapi.Schema(
                    type=openapi.TYPE_STRING, description="JWT token to verify"
                ),
            },
        ),
        responses={
            200: openapi.Response(description="Token is valid"),
            401: openapi.Response(description="Token is invalid or expired"),
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
