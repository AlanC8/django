from typing import Any, Optional

from rest_framework.exceptions import ValidationError
from rest_framework.serializers import (
    CharField,
    EmailField,
    IntegerField,
    ListField,
    Serializer,
)

from .models import User


class UserLoginResponseSerializer(Serializer):
    """Serializer for user login response."""

    id = IntegerField()
    email = EmailField()
    access_token = CharField()
    refresh_token = CharField()

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "access_token",
            "refresh_token",
        ]


class UserLoginErrorsSerializer(Serializer):
    """
    Serializer for user login errors.
    """

    email = ListField(
        child=CharField(),
        required=False,
    )
    password = ListField(
        child=CharField(),
        required=False,
    )

    class Meta:
        """Customization of the Serializer metadata."""

        fields = (
            "email",
            "password",
        )


class HTTP405MethodNotAllowedSerializer(Serializer):
    """
    Serializer for HTTP 405 Method Not Allowed response.
    """

    detail = CharField()

    class Meta:
        """Customization of the Serializer metadata."""

        fields = ("detail",)


class UserLoginSerializer(Serializer):
    """
    Serializer for user login.
    """

    email = EmailField(
        required=True,
        max_length=User.EMAIL_MAX_LENGTH,
    )
    password = CharField(
        required=True,
        max_length=User.PASSWORD_MAX_LENGTH,
    )

    class Meta:
        """Customization of the Serializer metadata."""

        fields = (
            "email",
            "password",
        )

    def validate_email(self, value: str) -> str:
        """Validates the email field."""
        return value.lower()

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        """Validates the input data."""
        email: str = attrs["email"]
        password: str = attrs["password"]

        user: Optional[User] = User.objects.filter(email=email).first()

        if not user:
            raise ValidationError(
                detail={"email": [f"User with email '{email}' does not exist."]}
            )

        if not user.check_password(raw_password=password):
            raise ValidationError(detail={"password": ["Incorrect password."]})

        attrs["user"] = user

        return super().validate(attrs)
