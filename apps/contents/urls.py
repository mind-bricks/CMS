from django.urls import (
    include,
    path,
)
from rest_framework import routers

from .views import (
    ContentViewSet,
)

router = routers.DefaultRouter()
router.register(
    'contents',
    ContentViewSet,
    basename='contents'
)

app_name = 'contents'

urlpatterns = [
    path(r'', include(router.urls)),
]
