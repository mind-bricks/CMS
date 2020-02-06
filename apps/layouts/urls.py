from django.urls import (
    include,
    path,
)
from rest_framework_extensions import (
    routers,
)

from .views import (
    LayoutViewSet,
    LayoutElementViewSet,
)

router = routers.ExtendedDefaultRouter()
router_layout = router.register(
    'layouts',
    LayoutViewSet,
    basename='layouts',
)
router_layout.register(
    'elements',
    LayoutElementViewSet,
    basename='layout-elements',
    parents_query_lookups=['layout__uuid'],
)

app_name = 'layouts'

urlpatterns = [
    path(r'', include(router.urls)),
]
