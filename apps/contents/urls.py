from django.urls import (
    include,
    path,
)
from rest_framework_extensions import routers

from .views import (
    ContentViewSet,
    ContentGrantViewSet,
    ContentGrantUserViewSet,
    ContentGrantScopeViewSet,
)

router = routers.ExtendedDefaultRouter()
router_grant = router.register(
    'contents/grants',
    ContentGrantViewSet,
    basename='content-grants',
)
router_grant.register(
    'users',
    ContentGrantUserViewSet,
    basename='content-grant-users',
    parents_query_lookups=['grant__name'],
)

router_grant.register(
    'scopes',
    ContentGrantScopeViewSet,
    basename='content-grant-scopes',
    parents_query_lookups=['grant__name'],
)
router.register(
    'contents',
    ContentViewSet,
    basename='contents'
)

app_name = 'contents'

urlpatterns = [
    path(r'', include(router.urls)),
]
