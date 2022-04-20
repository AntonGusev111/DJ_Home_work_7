from django_filters import rest_framework as filters, DateFromToRangeFilter

from advertisements.models import Advertisement


class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""
    creator = filters.CharFilter(field_name='creator_id', lookup_expr='in')
    created_at = DateFromToRangeFilter(field_name='created_at', lookup_expr='in')
    status = filters.CharFilter(field_name='status')

    class Meta:
        model = Advertisement
        fields = ['creator', 'created_at', 'status']
