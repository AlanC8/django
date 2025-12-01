from typing import Any

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db.models import BooleanField, CharField, EmailField

from apps.abstracts.models import AbstractBaseModel


class UserManager(BaseUserManager):
    """Custom User Manager to make database requests."""

    def __check_user_instance(
        self,
        email: str,
        password: str,
        **kwargs: Any,
    ) -> "User":
        """Get user instance."""
        if not email:
            raise ValidationError(message="Email field is required", code="email_empty")

        new_user: "User" = self.model(
            email=self.normalize_email(email),
            password=password,
            **kwargs,
        )

        return new_user

    def create_user(
        self,
        email: str,
        password: str,
        **kwargs: Any,
    ) -> "User":
        """Create and save a User with the given email and password."""
        user = self.__check_user_instance(
            email=email,
            password=password,
            **kwargs,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email: str,
        password: str,
        **kwargs: Any,
    ) -> "User":
        """Create and save a SuperUser with the given email and password."""
        user = self.__check_user_instance(
            email=email,
            password=password,
            is_staff=True,
            is_superuser=True,
            **kwargs,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin, AbstractBaseModel):  # type: ignore
    """
    Custom user model extending AbstractBaseModel.
    """

    EMAIL_MAX_LENGTH = 150
    FULL_NAME_MAX_LENGTH = 150
    PASSWORD_MAX_LENGTH = 254

    email = EmailField(
        max_length=EMAIL_MAX_LENGTH,
        unique=True,
        db_index=True,
        verbose_name="Email address",
        help_text="User's email address",
    )

    password = CharField(
        max_length=PASSWORD_MAX_LENGTH,
        validators=[validate_password],
        verbose_name="Password",
        help_text="User's hash representation of the password",
    )
    is_staff = BooleanField(
        default=False,  # type: ignore
        verbose_name="Staff status",
        help_text="True if the user is an admin and has an access to the admin panel",
    )
    is_active = BooleanField(
        default=True,  # type: ignore
        verbose_name="Active status",
        help_text="True if the user is active and has an access to request data",
    )

    USERNAME_FIELD = "email"
    objects = UserManager()
