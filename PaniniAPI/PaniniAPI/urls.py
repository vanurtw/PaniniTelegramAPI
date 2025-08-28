from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from .swagger_urls import urlpatterns_swagger

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('users.urls')),
    path('api/v1/', include('auth_users.urls')),
    path('api/v1/', include('teams.urls')),
]

if settings.DEBUG:
    urlpatterns += urlpatterns_swagger
