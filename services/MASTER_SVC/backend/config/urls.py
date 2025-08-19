"""
URL configuration for MASTER_SVC backend service.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/master/', include('apps.master_svc.urls')),
]
