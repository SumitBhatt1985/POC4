"""
URL Configuration for users app.

This module defines URL patterns for user authentication endpoints.
"""

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (LoginAPIView, 
                    LogoutAPIView, 
                    UserProfileAPIView, 
                    SignUpAPIView, 
                    HomePageView, 
                    FeedbackAPIView,
                    RoleMasterAPIView,
                    EditRoleAPIView,
                    DeleteRoleAPIView,
                    UserManagementAPIView)

app_name = 'users'

urlpatterns = [
    # Authentication endpoints
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('signup/', SignUpAPIView.as_view(), name='signup'),
    path('profile/', UserProfileAPIView.as_view(), name='profile'),
    path('home/', HomePageView.as_view(), name='home'),
    path('feedback/', FeedbackAPIView.as_view(), name='feedback'),
    path('roles/', RoleMasterAPIView.as_view(), name='role'),
    path('roles/edit/', EditRoleAPIView.as_view(), name='edit-role'),
    path('roles/delete/', DeleteRoleAPIView.as_view(), name='delete-role'),

    # User management endpoints
    path('users/manage/', UserManagementAPIView.as_view(), name='user-management'),

    # JWT token refresh endpoint (provided by SimpleJWT)
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
