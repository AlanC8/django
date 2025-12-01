from typing import Any

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request as DRFRequest
from rest_framework.response import Response as DRFResponse
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import ViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from apps.auths.models import User
from apps.auths.serializers import (
    AuthErrorsSerializer,
    HTTP405MethodNotAllowedSerializer,
    UserRegisterSerializer,
)


class UserViewSet(ViewSet):
    """
    ViewSet for handling CustomUser-related endpoints.
    """

    @swagger_auto_schema(
        operation_description="Fetch personal account details of the authenticated user.",
        operation_summary="Get current user info",
        tags=["Auth"],
        responses={
            200: openapi.Response(
                description="User information retrieved successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(
                            type=openapi.TYPE_INTEGER, description="User ID"
                        ),
                        "email": openapi.Schema(
                            type=openapi.TYPE_STRING, description="User email"
                        ),
                    },
                ),
            ),
            401: openapi.Response(
                description="Authentication credentials were not provided"
            ),
            405: HTTP405MethodNotAllowedSerializer,
        },
        security=[{"Bearer": []}],
    )
    @action(
        methods=("GET",),
        detail=False,
        url_name="me",
        url_path="me",
        permission_classes=(IsAuthenticated,),
    )
    def get_user_info(
        self, request: DRFRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]
    ) -> DRFResponse:
        """Fetch personal account details of the authenticated user."""
        user: User = request.user

        return DRFResponse(
            data={
                "id": user.id,  # type: ignore
                "email": user.email,
            },
            status=HTTP_200_OK,
        )

    @swagger_auto_schema(
        operation_description="Register a new user and return JWT tokens.",
        operation_summary="Register new user",
        tags=["Auth"],
        request_body=UserRegisterSerializer,
        responses={
            200: openapi.Response(
                description="User registered successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(
                            type=openapi.TYPE_INTEGER, description="User ID"
                        ),
                        "email": openapi.Schema(
                            type=openapi.TYPE_STRING, description="User email"
                        ),
                        "access": openapi.Schema(
                            type=openapi.TYPE_STRING, description="JWT access token"
                        ),
                        "refresh": openapi.Schema(
                            type=openapi.TYPE_STRING, description="JWT refresh token"
                        ),
                    },
                ),
            ),
            400: AuthErrorsSerializer,
            405: HTTP405MethodNotAllowedSerializer,
        },
    )
    @action(
        methods=("POST",),
        detail=False,
        url_name="register",
        url_path="register",
        permission_classes=(AllowAny,),
    )
    def register(
        self, request: DRFRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]
    ) -> DRFResponse:
        """Register a new user and return JWT tokens."""
        serializer: UserRegisterSerializer = UserRegisterSerializer(data=request.data)  # type: ignore
        serializer.is_valid(raise_exception=True)

        user: User = User.objects.create_user(
            email=serializer.validated_data["email"],  # type: ignore
            password=serializer.validated_data["password"],  # type: ignore
        )

        refresh: RefreshToken = RefreshToken.for_user(user)
        access_token: str = str(refresh.access_token)

        return DRFResponse(
            data={
                "id": user.id,  # type: ignore
                "email": user.email,
                "access": access_token,
                "refresh": str(refresh),
            },
            status=HTTP_200_OK,
        )
