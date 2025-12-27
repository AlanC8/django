import pytest

from apps.auths.models import User


@pytest.fixture
def create_user(db):
    def _create_user(email: str = "user@example.com", password: str = "strongpass123") -> User:
        return User.objects.create_user(email=email, password=password)

    return _create_user
