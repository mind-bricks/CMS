from functools import reduce

from django.db import models
from rest_framework import (
    exceptions,
    permissions,
    viewsets,
)
from rest_framework_extensions import (
    mixins as mixins_ext
)

from ..permissions import (
    UserHasScope,
    AllowReadOnly,
)
from .filters import (
    LayoutFilterSet,
    LayoutElementFilterSet,
)
from .models import (
    Layout,
    LayoutElement,
)
from .serializers import (
    LayoutSerializer,
    LayoutElementSerializer,
)


class LayoutViewSet(viewsets.ModelViewSet):
    filter_class = LayoutFilterSet
    lookup_field = 'uuid'
    permission_classes = [AllowReadOnly | UserHasScope]
    queryset = Layout.objects.select_related(
        'parent',
        'read_grant',
        'write_grant',
    ).all()
    required_scopes = ['cms.users']
    serializer_class = LayoutSerializer

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

    def perform_destroy(self, instance):
        try:
            instance.delete()
        except models.ProtectedError:
            raise exceptions.NotAcceptable(
                'layout children have to be deleted first')


class LayoutElementViewSet(
    mixins_ext.NestedViewSetMixin,
    viewsets.ModelViewSet,
):
    filter_class = LayoutElementFilterSet
    lookup_field = 'uuid'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = LayoutElement.objects.all()
    required_scopes = ['cms.users']
    serializer_class = LayoutElementSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        uuid = getattr(user, 'uuid', None)
        scopes = getattr(user, 'scopes', None)
        qs_cond = dict(
            layout__created_user=uuid,
            layout__write_grant__users__user=uuid,
            layout__write_grant__scopes__scope__in=scopes,
        )
        if self.action in ['list', 'retrieve']:
            qs_cond.update(
                layout__is_public=True,
                layout__read_grant__users__user=uuid,
                layout__read_grant__scopes__scope__in=scopes,
            )
        qs_cond = [
            models.Q(**{k: v})
            for k, v in qs_cond.items() if v is not None
        ]
        return qs.filter(reduce(lambda x, y: x | y, qs_cond))

    def perform_create(self, serializer):
        user = self.request.user
        uuid = user.uuid
        scopes = user.scopes
        qs_cond = dict(
            created_user=uuid,
            write_grant__users__user=uuid,
            write_grant__scopes__scope__in=scopes,
        )
        layout = Layout.objects.filter(
            reduce(lambda x, y: x | y, qs_cond) &
            models.Q(uuid=self.kwargs['parent_lookup_layout__uuid'])
        ).first()
        if not layout:
            raise exceptions.PermissionDenied(
                'can not write to layout')

        serializer.save(layout=layout, created_user=uuid)
