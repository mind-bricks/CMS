from django.urls import (
    include,
    path,
)
from rest_framework_extensions import routers

from .views import (
    GrantViewSet,
    GrantUserViewSet,
    GrantScopeViewSet,
)

router = routers.ExtendedDefaultRouter()
router_grant = router.register(
    'grants',
    GrantViewSet,
    basename='grants',
)
router_grant.register(
    'users',
    GrantUserViewSet,
    basename='grant-users',
    parents_query_lookups=['grant__uuid'],
)

router_grant.register(
    'scopes',
    GrantScopeViewSet,
    basename='grant-scopes',
    parents_query_lookups=['grant__uuid'],
)

app_name = 'grants'

urlpatterns = [
    path(r'', include(router.urls)),
]
