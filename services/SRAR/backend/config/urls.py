"""
URL configuration for SRAR backend service.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/srar/', include('apps.srar.urls')),
]
