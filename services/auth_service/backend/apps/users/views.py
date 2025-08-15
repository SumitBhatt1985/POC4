"""
Views for user authentication and management.

This module contains API views for handling user login using Django's built-in User model
with PostgreSQL backend. Optimized for Angular 18+ frontend consumption.
"""

from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
import logging

from .serializers import LoginSerializer, UserSerializer

logger = logging.getLogger(__name__)


class LoginAPIView(APIView):
    """
    API View for user authentication using username and password.
    
    This view handles user login by validating credentials against Django's User model
    stored in PostgreSQL and returns JWT tokens following SimpleJWT specification.
    
    Frontend Integration (Angular 18+):
    ```typescript
    // Login service method
    login(username: string, password: string): Observable<LoginResponse> {
      const loginData = { username, password };
      return this.http.post<LoginResponse>('/api/v1/auth/login/', loginData);
    }
    
    // Response interface
    interface LoginResponse {
      success: boolean;
      message: string;
      data: {
        user: UserData;
        tokens: {
          access: string;
          refresh: string;
        };
      };
    }
    ```
    
    Methods:
        POST: Authenticate user and return JWT tokens
    """
    
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        """
        Authenticate user with username and password against PostgreSQL.
        
        Args:
            request: HTTP request containing username and password
            
        Returns:
            Response: Clean JSON response optimized for Angular frontend
            
        Request Body:
            {
                "username": "[username]",
                "password": "[password]"
            }
            
        Success Response (200):
            {
                "success": true,
                "message": "Login successful",
                "data": {
                    "user": {
                        "id": 1,
                        "username": "[username]",
                        "email": "[email]",
                        "first_name": "[first_name]",
                        "last_name": "[last_name]",
                        "is_staff": false,
                        "is_active": true,
                        "date_joined": "2024-01-01T12:00:00Z",
                        "last_login": "2024-01-15T10:30:00Z"
                    },
                    "tokens": {
                        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
                    }
                }
            }
            
        Error Response (400):
            {
                "success": false,
                "message": "Invalid credentials",
                "errors": {
                    "detail": "Invalid credentials. Please check your username and password.",
                    "code": "invalid_credentials"
                }
            }
        """
        
        serializer = LoginSerializer(
            data=request.data, 
            context={'request': request}
        )
        
        if serializer.is_valid():
            try:
                # Get validated user from serializer (PostgreSQL query completed)
                user = serializer.validated_data['user']
                
                # Generate JWT tokens using SimpleJWT
                tokens = serializer.get_tokens_for_user(user)
                
                # Update last login timestamp (PostgreSQL UPDATE query)
                user.last_login = timezone.now()
                user.save(update_fields=['last_login'])
                
                # Serialize user data for clean JSON response
                user_serializer = UserSerializer(user)
                
                # Log successful login with client IP for security monitoring
                client_ip = self.get_client_ip(request)
                # Sanitize username to prevent log injection
                safe_username = user.username.replace('\n', '').replace('\r', '').replace('\t', '')
                logger.info(
                    f"User {safe_username} (ID: {user.id}) logged in successfully from IP: {client_ip}"
                )
                
                # Return clean JSON response for Angular frontend
                return Response({
                    'success': True,
                    'message': 'Login successful',
                    'data': {
                        'user': user_serializer.data,
                        'tokens': tokens
                    }
                }, status=status.HTTP_200_OK)
                
            except Exception as e:
                # Log unexpected errors for debugging
                logger.error(f"Unexpected error during login: {str(e)}")
                return Response({
                    'success': False,
                    'message': 'An error occurred during authentication',
                    'errors': {
                        'detail': 'Internal server error',
                        'code': 'server_error'
                    }
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        else:
            # Log failed login attempt for security monitoring
            username = request.data.get('username', 'unknown')
            client_ip = self.get_client_ip(request)
            # Sanitize username to prevent log injection
            safe_username = str(username).replace('\n', '').replace('\r', '').replace('\t', '')
            logger.warning(
                f"Failed login attempt for username: {safe_username} from IP: {client_ip}"
            )
            
            # Return standardized error response for Angular frontend
            return Response({
                'success': False,
                'message': 'Authentication failed',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
    
    def get_client_ip(self, request):
        """
        Extract client IP address from request headers.
        
        Args:
            request: HTTP request object
            
        Returns:
            str: Client IP address
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', 'unknown')
        return ip


class LogoutAPIView(APIView):
    """
    API View for user logout with JWT token blacklisting.
    
    This view handles user logout by blacklisting the refresh token in PostgreSQL
    to prevent further use, following SimpleJWT specification.
    
    Frontend Integration (Angular 18+):
    ```typescript
    logout(): Observable<LogoutResponse> {
      const refreshToken = localStorage.getItem('refresh_token');
      return this.http.post<LogoutResponse>('/api/v1/auth/logout/', {
        refresh: refreshToken
      });
    }
    ```
    
    Methods:
        POST: Logout user and blacklist refresh token
    """
    
    def post(self, request, *args, **kwargs):
        """
        Logout user by blacklisting refresh token in PostgreSQL.
        
        Args:
            request: HTTP request containing refresh token
            
        Returns:
            Response: Clean JSON response for Angular frontend
            
        Request Body:
            {
                "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
            }
            
        Success Response (200):
            {
                "success": true,
                "message": "Logout successful"
            }
            
        Error Response (400):
            {
                "success": false,
                "message": "Invalid token",
                "errors": {
                    "detail": "Token is invalid or expired",
                    "code": "invalid_token"
                }
            }
        """
        
        try:
            refresh_token = request.data.get('refresh')
            
            if not refresh_token:
                return Response({
                    'success': False,
                    'message': 'Refresh token is required',
                    'errors': {
                        'detail': 'Refresh token not provided',
                        'code': 'missing_token'
                    }
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Blacklist token in PostgreSQL using SimpleJWT
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            # Log successful logout
            username = request.user.username if request.user.is_authenticated else 'unknown'
            # Sanitize username to prevent log injection
            safe_username = str(username).replace('\n', '').replace('\r', '').replace('\t', '')
            logger.info(f"User {safe_username} logged out successfully")
            
            return Response({
                'success': True,
                'message': 'Logout successful'
            }, status=status.HTTP_200_OK)
            
        except TokenError as e:
            logger.warning(f"Invalid token during logout: {str(e)}")
            return Response({
                'success': False,
                'message': 'Invalid token',
                'errors': {
                    'detail': 'Token is invalid or expired',
                    'code': 'invalid_token'
                }
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            logger.error(f"Unexpected error during logout: {str(e)}")
            return Response({
                'success': False,
                'message': 'An error occurred during logout',
                'errors': {
                    'detail': 'Internal server error',
                    'code': 'server_error'
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserProfileAPIView(APIView):
    """
    API View for retrieving authenticated user's profile from PostgreSQL.
    
    This view returns the profile information of the currently authenticated user
    with clean JSON output for Angular 18+ frontend consumption.
    
    Frontend Integration (Angular 18+):
    ```typescript
    getUserProfile(): Observable<ProfileResponse> {
      const token = localStorage.getItem('access_token');
      const headers = { Authorization: `Bearer ${token}` };
      return this.http.get<ProfileResponse>('/api/v1/auth/profile/', { headers });
    }
    ```
    
    Methods:
        GET: Retrieve authenticated user's profile
    """
    
    def get(self, request, *args, **kwargs):
        """
        Retrieve authenticated user's profile from PostgreSQL.
        
        Args:
            request: HTTP request with JWT authentication
            
        Returns:
            Response: Clean JSON response with user profile data
            
        Success Response (200):
            {
                "success": true,
                "message": "Profile retrieved successfully",
                "data": {
                    "user": {
                        "id": 1,
                        "username": "[username]",
                        "email": "[email]",
                        "first_name": "[first_name]",
                        "last_name": "[last_name]",
                        "is_staff": false,
                        "is_active": true,
                        "date_joined": "2024-01-01T12:00:00Z",
                        "last_login": "2024-01-15T10:30:00Z"
                    }
                }
            }
        """
        
        try:
            # Serialize user data from PostgreSQL for clean JSON output
            serializer = UserSerializer(request.user)
            
            return Response({
                'success': True,
                'message': 'Profile retrieved successfully',
                'data': {
                    'user': serializer.data
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error retrieving user profile: {str(e)}")
            return Response({
                'success': False,
                'message': 'An error occurred while retrieving profile',
                'errors': {
                    'detail': 'Internal server error',
                    'code': 'server_error'
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
