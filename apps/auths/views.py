from typing import Any

from drf_spectacular.utils import (OpenApiResponse, extend_schema,
                                   inline_serializer)
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request as DRFRequest
from rest_framework.response import Response as DRFResponse
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import ViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from apps.auths.models import User
from apps.auths.serializers import (AuthErrorsSerializer,
                                    HTTP405MethodNotAllowedSerializer,
                                    UserRegisterSerializer)


class UserViewSet(ViewSet):
    """
    ViewSet for handling CustomUser-related endpoints.
    """

    @extend_schema(
        tags=["Auth"],
        summary="Get current user info",
        description="Fetch personal account details of the authenticated user.",
        responses={
            200: inline_serializer(
                name="UserInfoResponse",
                fields={
                    "id": serializers.IntegerField(),
                    "email": serializers.EmailField(),
                },
            ),
            401: OpenApiResponse(
                description="Authentication credentials were not provided"
            ),
            405: HTTP405MethodNotAllowedSerializer,
        },
        auth=[{"Bearer": []}],  # type: ignore
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

    @extend_schema(
        tags=["Auth"],
        summary="Register new user",
        description="Register a new user and return JWT tokens.",
        request=UserRegisterSerializer,
        responses={
            200: inline_serializer(
                name="UserRegisterResponse",
                fields={
                    "id": serializers.IntegerField(),
                    "email": serializers.EmailField(),
                    "access": serializers.CharField(),
                    "refresh": serializers.CharField(),
                },
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
        )
        user.set_password(serializer.validated_data["password"])  # type: ignore
        user.save()

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
