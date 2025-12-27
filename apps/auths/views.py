from typing import Any

from drf_spectacular.utils import OpenApiResponse, extend_schema
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
    UserInfoSerializer,
    UserLoginSerializer,
    UserRegisterSerializer,
    UserSuccessAuthSerializer,
)


class UserViewSet(ViewSet):
    """
    ViewSet for handling CustomUser-related endpoints.
    """

    @extend_schema(
        tags=["Auth"],
        summary="Get current user info",
        description="Fetch personal account details of the authenticated user.",
        responses={
            200: UserInfoSerializer,
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
            200: UserSuccessAuthSerializer,
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

    @extend_schema(
        tags=["Auth"],
        summary="User login",
        description="Authenticate user and return JWT tokens.",
        request=UserLoginSerializer,
        responses={
            200: UserSuccessAuthSerializer,
            401: AuthErrorsSerializer,
            405: HTTP405MethodNotAllowedSerializer,
        },
    )
    @action(
        methods=("POST",),
        detail=False,
        url_name="login",
        url_path="login",
        permission_classes=(AllowAny,),
    )
    def login(
        self, request: DRFRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]
    ) -> DRFResponse:
        """Login endpoint is handled by DecoratedTokenObtainPairView.

        Parameters:
            request: DRFRequest
                The request object.
            *args: tuple
                Additional positional arguments.
            **kwargs: dict
                Additional keyword arguments.

        Returns:
            DRFResponse
                Response containing user data or error message
        """

        serializer: UserLoginSerializer = UserLoginSerializer(data=request.data)  # type: ignore
        serializer.is_valid(raise_exception=True)

        user: User = serializer.validated_data.pop("user")  # type: ignore

        refresh_token: RefreshToken = RefreshToken.for_user(user)
        access_token: str = str(refresh_token.access_token)

        return DRFResponse(
            data={
                "id": user.id,  # type: ignore
                "email": user.email,
                "access": access_token,
                "refresh": str(refresh_token),
            },
            status=HTTP_200_OK,
        )
