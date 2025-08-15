"""
Serializers for user authentication and management.

This module contains serializers for handling user login using Django's built-in User model.
Optimized for Angular 18+ frontend consumption with clean JSON responses.
"""

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
import logging

logger = logging.getLogger(__name__)


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login with username and password.
    
    This serializer validates user credentials against Django's User model using PostgreSQL
    and returns JWT tokens upon successful authentication.
    
    Frontend Usage (Angular 18+):
    ```typescript
    // POST to /api/v1/auth/login/
    const loginData = {
      username: '[username]',
      password: '[password]'
    };
    
    this.http.post<LoginResponse>('/api/v1/auth/login/', loginData)
      .subscribe(response => {
        if (response.success) {
          // Store tokens in localStorage or sessionStorage
          localStorage.setItem('access_token', response.data.tokens.access);
          localStorage.setItem('refresh_token', response.data.tokens.refresh);
        }
      });
    ```
    """
    
    username = serializers.CharField(
        required=True,
        max_length=150,  # Django User model username max_length
        error_messages={
            'required': 'Username is required.',
            'blank': 'Username cannot be blank.',
            'max_length': 'Username must be 150 characters or fewer.'
        }
    )
    
    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'},
        error_messages={
            'required': 'Password is required.',
            'blank': 'Password cannot be blank.'
        }
    )
    
    def validate(self, attrs):
        """
        Validate user credentials against Django User model using PostgreSQL.
        
        Args:
            attrs (dict): Dictionary containing username and password
            
        Returns:
            dict: Validated data with authenticated user instance
            
        Raises:
            serializers.ValidationError: If credentials are invalid
        """
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            # Authenticate user using Django's built-in authentication
            # This performs a PostgreSQL query: SELECT * FROM auth_user WHERE username = %s
            user = authenticate(
                request=self.context.get('request'),
                username=username,
                password=password
            )
            
            if not user:
                # Log failed authentication attempt for security monitoring
                # Sanitize username to prevent log injection
                safe_username = str(username).replace('\n', '').replace('\r', '').replace('\t', '')
                logger.warning(f"Failed login attempt for username: {safe_username}")
                raise serializers.ValidationError(
                    {
                        'detail': 'Invalid credentials. Please check your username and password.',
                        'code': 'invalid_credentials'
                    }
                )
            
            if not user.is_active:
                # Log attempt to login with inactive account
                # Sanitize username to prevent log injection
                safe_username = str(username).replace('\n', '').replace('\r', '').replace('\t', '')
                logger.warning(f"Login attempt for inactive user: {safe_username}")
                raise serializers.ValidationError(
                    {
                        'detail': 'User account is disabled.',
                        'code': 'account_disabled'
                    }
                )
            
            # Log successful authentication
            # Sanitize username to prevent log injection
            safe_username = str(username).replace('\n', '').replace('\r', '').replace('\t', '')
            logger.info(f"Successful login for user: {safe_username} (ID: {user.id})")
            attrs['user'] = user
            
        else:
            raise serializers.ValidationError(
                {
                    'detail': 'Both username and password are required.',
                    'code': 'missing_credentials'
                }
            )
        
        return attrs
    
    def get_tokens_for_user(self, user):
        """
        Generate JWT tokens for authenticated user using SimpleJWT.
        
        Args:
            user (User): Django User instance from PostgreSQL
            
        Returns:
            dict: Dictionary containing access and refresh tokens
        """
        refresh = RefreshToken.for_user(user)
        
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for Django User model with clean JSON output for Angular frontend.
    
    This serializer provides user data without exposing sensitive information.
    Optimized for PostgreSQL queries and Angular 18+ consumption.
    """
    
    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name',
            'is_staff', 'is_active', 'date_joined', 'last_login'
        )
        read_only_fields = ('id', 'date_joined', 'last_login')
