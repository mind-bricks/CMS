from django_filters.rest_framework import (
    filters,
    filterset,
)

from .models import (
    Content,
)


class ContentFilterSet(filterset.FilterSet):
    label__contains = filters.CharFilter(
        field_name='label',
        lookup_expr='contains',
    )

    class Meta:
        model = Content
        fields = [
            'label',
            'label__contains',
        ]
