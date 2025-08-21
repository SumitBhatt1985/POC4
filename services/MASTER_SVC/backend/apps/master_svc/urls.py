from django.urls import path

from . import views, health

urlpatterns = [
    path('health/', health.health_check, name='health'),
    # path('create/', views.GenericCreateView.as_view(), name='generic-create'),
    # path('view/', views.GenericListView.as_view(), name='generic-list'),
    # path('update/<int:pk>/', views.GenericUpdateView.as_view(), name='generic-update'),
    # path('delete/<int:pk>/', views.GenericDeleteView.as_view(), name='generic-delete'),
    # path('wrapper/', views.WrapperAPIView.as_view(), name='wrapper-api'),
    # path('flexible-wrapper/', views.FlexibleWrapperAPIView.as_view(), name='flexible-wrapper-api'),
    path('wrapper/', views.FlexibleWrapperAPIView.as_view(), name='wrapper-api'),
]
