from django.apps import AppConfig


class AbstractsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"  #  type: ignore
    name = "apps.abstracts"
