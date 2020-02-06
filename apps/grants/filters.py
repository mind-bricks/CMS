from django_filters.rest_framework import (
    filters,
    filterset,
)

from ..filters import (
    UUIDListFilter,
)
from .models import (
    Grant,
)


class GrantFilterSet(filterset.FilterSet):
    uuid__in = UUIDListFilter(
        field_name='uuid',
        lookup_expr='in',
    )
    name__contains = filters.CharFilter(
        field_name='name',
        lookup_expr='contains',
    )

    class Meta:
        model = Grant
        fields = [
            'uuid',
            'uuid__in',
            'name',
            'name__contains',
        ]
