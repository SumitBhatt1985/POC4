"""
URL configuration for SFD backend service.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/sfd/', include('apps.sfd.urls')),
]
