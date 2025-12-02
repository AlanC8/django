import django_filters
from apps.listings.models import Listing


class ListingFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    city = django_filters.CharFilter(field_name="property__city__slug")
    district = django_filters.CharFilter(field_name="property__district__slug")

    class Meta:
        model = Listing
        fields = ["status", "is_top"]
