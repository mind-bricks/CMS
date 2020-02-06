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
)

from .filters import (
    GrantFilterSet,
)
from .models import (
    Grant,
    GrantUser,
    GrantScope,
)
from .serializers import (
    GrantSerializer,
    GrantUserSerializer,
    GrantScopeSerializer,
)


class GrantViewSet(viewsets.ModelViewSet):
    filter_class = GrantFilterSet
    lookup_field = 'uuid'
    permission_classes = [UserHasScope]
    queryset = Grant.objects.all()
    required_scopes = ['cms']
    serializer_class = GrantSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(created_user=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save(created_user=self.request.user.id)


class GrantUserViewSet(
    mixins_ext.NestedViewSetMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    lookup_field = 'user'
    permission_classes = [UserHasScope]
    queryset = GrantUser.objects.all()
    required_scopes = ['cms']
    serializer_class = GrantUserSerializer

    def perform_create(self, serializer):
        grant = Grant.objects.filter(
            created_user=self.request.user.id,
            uuid=self.kwargs['parent_lookup_grant__uuid'],
        ).first()
        if not grant:
            raise exceptions.PermissionDenied(
                'can not write to content grant'
            )

        serializer.save(grant=grant)


class GrantScopeViewSet(
    mixins_ext.NestedViewSetMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    lookup_field = 'scope'
    lookup_value_regex = '[^/]+'
    permission_classes = [UserHasScope]
    queryset = GrantScope.objects.all()
    required_scopes = ['cms']
    serializer_class = GrantScopeSerializer

    def perform_create(self, serializer):
        grant = Grant.objects.filter(
            created_user=self.request.user.id,
            uuid=self.kwargs['parent_lookup_grant__uuid'],
        ).first()
        if not grant:
            raise exceptions.PermissionDenied(
                'can not write to content grant'
            )

        serializer.save(grant=grant)
