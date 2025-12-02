from typing import Any, Optional

from rest_framework.exceptions import ValidationError
from rest_framework.serializers import (CharField, EmailField, ListField,
                                        Serializer)

from .models import User


class AuthErrorsSerializer(Serializer):
    """
    Serializer for user registration errors.
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


class UserRegisterSerializer(Serializer):
    """
    Serializer for user registration.
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
        email: str = value.lower()

        if User.objects.filter(email=email).exists():
            raise ValidationError(
                detail={"email": [f"User with email '{email}' already exists."]}
            )

        return email
