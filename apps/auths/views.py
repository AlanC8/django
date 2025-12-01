from typing import Any

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request as DRFRequest
from rest_framework.response import Response as DRFResponse
from rest_framework.status import HTTP_200_OK
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for managing User instances."""

    @action(
        methods=("POST",),
        detail=False,
        url_path="login",
        url_name="login",
        permission_classes=(AllowAny,),
    )
    def login(self, request: DRFRequest, *args: Any, **kwargs: Any) -> DRFResponse:
        """
        Handle user login.

        Parameters:
            request: DRFRequest
                The request object.
            *args: tuple
                Additional positional arguments.
            **kwargs: dict
                Additional keyword arguments.

        Returns:
            DRFResponse
                Response containing user data or error message.
        """

        serializer: UserSerializer = UserSerializer(data=request.data)  # type: ignore

        serializer.is_valid(raise_exception=True)

        user: User = serializer.validated_data.pop("user")  # type: ignore

        refresh: RefreshToken = RefreshToken.for_user(user)
        access_token: str = str(refresh.access_token)

        return DRFResponse(
            data={
                "access": access_token,
                "refresh": str(refresh),
            },
            status=HTTP_200_OK,
        )
