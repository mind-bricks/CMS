# from django.contrib import admin
from django.urls import (
    include,
    path,
)
from rest_framework_swagger import (
    views as swagger_views
)

# admin.site.site_header = 'CMS'
# admin.site.site_title = 'CMS Admin'
# admin.site.index_title = 'Content Management System Admin Site'

urlpatterns = [
    path('', include('apps.contents.urls')),
    # path('admin/', admin.site.urls),
    path('swagger/', swagger_views.get_swagger_view(title='CMS APIs')),
]
