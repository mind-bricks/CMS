from django_filters.rest_framework import (
    filters,
    filterset,
)

from .models import (
    Layout,
)


class LayoutFilterSet(filterset.FilterSet):
    parent = filters.CharFilter(
        field_name='parent__name',
    )
    parent__isnull = filters.BooleanFilter(
        field_name='parent',
        lookup_expr='isnull',
    )
    name__contains = filters.CharFilter(
        field_name='name',
        lookup_expr='contains',
    )

    class Meta:
        model = Layout
        fields = [
            'name',
            'name__contains',
            'parent',
            'parent__isnull',
        ]
