import os

import pytest
from rest_framework.test import APIClient


os.environ.setdefault("PROJECT_ENV_ID", "local")
os.environ.setdefault("DB_NAME", "test_db")
os.environ.setdefault("DB_USER", "user")
os.environ.setdefault("DB_PASSWORD", "password")
os.environ.setdefault("DB_HOST", "localhost")
os.environ.setdefault("DB_PORT", "5432")


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()
