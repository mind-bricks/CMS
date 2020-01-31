from django.db import models
from rest_framework import (
    exceptions,
    mixins,
    viewsets,
)
from rest_framework_extensions import (
    mixins as mixins_ext,
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
    ContentGrant,
    ContentGrantUser,
    ContentGrantScope,
)
from .serializers import (
    ContentSerializer,
    ContentGrantSerializer,
    ContentGrantUserSerializer,
    ContentGrantScopeSerializer,
)


class ContentViewSet(viewsets.ModelViewSet):
    filter_class = ContentFilterSet
    lookup_field = 'uuid'
    permission_classes = [AllowReadOnly | UserHasScope]
    queryset = Content.objects.all()
    required_scopes = ['cms']
    serializer_class = ContentSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if not user.is_authenticated:
            return qs.filter(is_public=True)

        uuid = user.uuid
        scopes = user.scopes
        qs_cond = (
            models.Q(created_user=uuid) |
            models.Q(write_grant__users__user=uuid) |
            models.Q(write_grant__scopes__scope__in=scopes)
        )
        if self.action in ['list', 'retrieve']:
            qs_cond |= (
                models.Q(is_public=True) |
                models.Q(read_grant__users__user=uuid) |
                models.Q(read_grant__scopes__scope__in=scopes)
            )
        return qs.filter(qs_cond)

    def perform_create(self, serializer):
        serializer.save(created_user=self.request.user.uuid)


class ContentGrantViewSet(viewsets.ModelViewSet):
    lookup_field = 'name'
    permission_classes = [UserHasScope]
    queryset = ContentGrant.objects.all()
    required_scopes = ['cms']
    serializer_class = ContentGrantSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(created_user=self.request.user.uuid)

    def perform_create(self, serializer):
        serializer.save(created_user=self.request.user.uuid)


class ContentGrantUserViewSet(
    mixins_ext.NestedViewSetMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    lookup_field = 'user'
    permission_classes = [UserHasScope]
    queryset = ContentGrantUser.objects.all()
    required_scopes = ['cms']
    serializer_class = ContentGrantUserSerializer

    def perform_create(self, serializer):
        grant = ContentGrant.objects.filter(
            created_user=self.request.user.uuid,
            name=self.kwargs['parent_lookup_grant__name'],
        ).first()
        if not grant:
            raise exceptions.NotFound('content grant no found')

        serializer.save(grant=grant)


class ContentGrantScopeViewSet(
    mixins_ext.NestedViewSetMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    lookup_field = 'scope'
    lookup_value_regex = '[^/]+'
    permission_classes = [UserHasScope]
    queryset = ContentGrantScope.objects.all()
    required_scopes = ['cms']
    serializer_class = ContentGrantScopeSerializer

    def perform_create(self, serializer):
        grant = ContentGrant.objects.filter(
            created_user=self.request.user.uuid,
            name=self.kwargs['parent_lookup_grant__name'],
        ).first()
        if not grant:
            raise exceptions.NotFound('content grant no found')

        serializer.save(grant=grant)
