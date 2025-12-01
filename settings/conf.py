from decouple import config

# --------------------------------------------
# Env
# --------------------------------------------
ENV_POSSIBLE_OPTIONS = [
    "prod",
    "local",
]

ENV_ID = config(
    "PROJECT_ENV_ID",
    cast=str,
)

# --------------------------------------------
# Database
#
DB_NAME = config(
    "DB_NAME",
    cast=str,
)

DB_USER = config(
    "DB_USER",
    cast=str,
)

DB_PASSWORD = config(
    "DB_PASSWORD",
    cast=str,
)

DB_HOST = config(
    "DB_HOST",
    cast=str,
)

DB_PORT = config(
    "DB_PORT",
    cast=str,
)

# --------------------------------------------
# Django Rest Framework
# 
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.AllowAny"],
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}



# --------------------------------------------
# Secret Key
#
SECRET_KEY = "django-insecure-bqt7^m_m908t-xnc6!gh(bn&indw#)9sr!@3m&(#yn*_-sz03c"
