from functools import reduce

from django.db import models
from rest_framework import (
    viewsets,
)

from ..permissions import (
    UserHasScope,
    AllowReadOnly,
)
from .filters import (
    ContentFilterSet,
)
from .models import (
    Content,
)
from .serializers import (
    ContentSerializer,
)


class ContentViewSet(viewsets.ModelViewSet):
    filter_class = ContentFilterSet
    lookup_field = 'uuid'
    permission_classes = [AllowReadOnly | UserHasScope]
    queryset = Content.objects.select_related(
        'read_grant',
        'write_grant',
    ).all()
    required_scopes = ['cms.users']
    serializer_class = ContentSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        uuid = getattr(user, 'uuid', None)
        scopes = getattr(user, 'scopes', None)
        qs_cond = dict(
            created_user=uuid,
            write_grant__users__user=uuid,
            write_grant__scopes__scope__in=scopes,
        )
        if self.action in ['list', 'retrieve']:
            qs_cond.update(
                is_public=True,
                read_grant__users__user=uuid,
                read_grant__scopes__scope__in=scopes,
            )
        qs_cond = [
            models.Q(**{k: v})
            for k, v in qs_cond.items() if v is not None
        ]
        return qs.filter(reduce(lambda x, y: x | y, qs_cond))

    def perform_create(self, serializer):
        serializer.save(created_user=self.request.user.id)
