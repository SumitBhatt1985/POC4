from django.urls import path
from . import views, health

urlpatterns = [
    path('health/', health.health_check, name='health'),
]
