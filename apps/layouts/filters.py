from django_filters.rest_framework import (
    filters,
    filterset,
)

from .models import (
    Layout,
    LayoutElement,
)


class LayoutFilterSet(filterset.FilterSet):
    parent = filters.UUIDFilter(
        field_name='parent__uuid',
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


class LayoutElementFilterSet(filterset.FilterSet):
    name__contains = filters.CharFilter(
        field_name='name',
        lookup_expr='contains',
    )

    class Meta:
        model = LayoutElement
        fields = [
            'name',
            'name__contains',
        ]
