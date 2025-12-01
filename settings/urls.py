from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/apartments/", include("apps.listings.urls")),
    path("api/locations/", include("apps.locations.urls")),
]
