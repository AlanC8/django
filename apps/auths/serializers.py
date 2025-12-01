from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model."""

    email = serializers.EmailField(required=True, max_length=User.EMAIL_MAX_LENGTH)
    password = serializers.CharField(
        write_only=True,
        required=True,
        max_length=User.PASSWORD_MAX_LENGTH,
        min_length=8,
    )

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "password",
        ]
        read_only_fields = ["id", "email"]
