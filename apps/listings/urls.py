from django.urls import path

from .views.listings import ListingViewSet
from .views.properties import PropertyViewSet
from .views.photos import PhotoViewSet


listing_list = ListingViewSet.as_view({
    "get": "list",
    "post": "create",
})

listing_detail = ListingViewSet.as_view({
    "get": "retrieve",
    "patch": "partial_update",
    "delete": "destroy",
})

listing_my = ListingViewSet.as_view({
    "get": "my_listings",
})

listing_publish = ListingViewSet.as_view({
    "post": "publish",
})


property_list = PropertyViewSet.as_view({
    "get": "list",
    "post": "create",
})

property_detail = PropertyViewSet.as_view({
    "get": "retrieve",
    "patch": "partial_update",
    "delete": "destroy",
})


photo_list = PhotoViewSet.as_view({
    "get": "list",
    "post": "create",
})

photo_detail = PhotoViewSet.as_view({
    "delete": "destroy",
})


urlpatterns = [
    # Listings
    path("listings/", listing_list),
    path("listings/<int:pk>/", listing_detail),
    path("listings/my/", listing_my),
    path("listings/<int:pk>/publish/", listing_publish),

    # Properties
    path("properties/", property_list),
    path("properties/<int:pk>/", property_detail),

    # Photos
    path("photos/", photo_list),
    path("photos/<int:pk>/", photo_detail),
]
