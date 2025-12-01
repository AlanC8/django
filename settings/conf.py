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
