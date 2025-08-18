"""
Views for user authentication and management.

This module contains API views for handling user login using Django's built-in User model
with PostgreSQL backend. Optimized for Angular 18+ frontend consumption.
"""

from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth import authenticate
from django.db import IntegrityError
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_framework_simplejwt.settings import api_settings
from .authentication import CustomJWTAuthentication
from datetime import datetime, timedelta
import logging

from .serializers import (LoginSerializer, 
                          UserSerializer, 
                          UserProfileSerializer, 
                          UserDetailsSerializer,
                          SignUpSerializer, 
                          InstructionsSerializer, OfflineSerializer, DownloadsSerializer, PublicationsSerializer, 
                          FeedbackSerializer,
                          RoleMasterSerializer)

from .models import (HomePageInformation, Feedback, UserDetails, RoleMaster)
from django.db import transaction

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

        userlogin = request.data.get('userlogin')
        password = request.data.get('password')

        
        try:
            user = UserDetails.objects.get(userlogin=userlogin, status='1')
            
            
            
            if check_password(password, user.password):
                class CustomUser:
                    def __init__(self, userlogin, role):
                        self.userlogin = userlogin
                        self.role = role
                        self.id = f"{userlogin}-{role}"  # Unique identifier

                    def __str__(self):
                        return self.id

                custom_user = CustomUser(user.userlogin, user.role)

                # Generate token manually
                refresh = RefreshToken()
                refresh['userlogin'] = custom_user.userlogin
                refresh['role'] = custom_user.role

                
                OutstandingToken.objects.create(
                    user=None,  # You can leave this as None or link to a dummy Django User if needed
                    jti=refresh['jti'],
                    token=str(refresh),
                    created_at=datetime.utcnow(),
                    expires_at=datetime.utcnow() + api_settings.REFRESH_TOKEN_LIFETIME
                )


                access_token = refresh.access_token
                access_token['userlogin'] = custom_user.userlogin
                access_token['role'] = custom_user.role

                tokens = {
                    "access": str(access_token),
                    "refresh": str(refresh)
                }

                return Response({
                    "success": True,
                    "message": "Login successful",
                    "data": {
                        "user": UserDetailsSerializer(user).data,
                        "tokens": tokens
                    }
                }, status=status.HTTP_200_OK)

            else:
                return Response({
                    "success": False,
                    "message": "Invalid credentials",
                    "errors": {"detail": "Incorrect password"}
                }, status=status.HTTP_401_UNAUTHORIZED)

        except UserDetails.DoesNotExist:
            return Response({
                "success": False,
                "message": "Invalid credentials",
                "errors": {"detail": "User not found"}
            }, status=status.HTTP_401_UNAUTHORIZED)



    
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
    permission_classes = [AllowAny]  
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

            
            outstanding = OutstandingToken.objects.filter(jti=token["jti"]).first()
            if outstanding:
                BlacklistedToken.objects.get_or_create(token=outstanding)
                logger.info(f"Token {token['jti']} blacklisted successfully")
                return Response({
                    "success": True,
                    "message": "Logout successful"
                }, status=status.HTTP_200_OK)
            else:
                logger.warning("Token not found in OutstandingToken table")
                return Response({
                    "success": False,
                    "message": "Token not found",
                    "errors": {
                        "detail": "Token not registered",
                        "code": "token_not_found"
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
    Production-ready API View for authenticated user profile management.
    
    This view handles both retrieving and updating user profile information
    with comprehensive validation, error handling, and PostgreSQL optimization.
    
    Frontend Integration (Angular 18+):
    ```typescript
    // TypeScript interfaces
    interface ProfileResponse {
      success: boolean;
      message: string;
      data: {
        user: UserProfile;
      };
    }
    
    interface UserProfile {
      id: number;
      username: string;
      email: string;
      first_name: string;
      last_name: string;
      full_name: string;
      initials: string;
      is_staff: boolean;
      is_active: boolean;
      date_joined: string;
      last_login: string;
    }
    
    // Service methods
    getUserProfile(): Observable<ProfileResponse> {
      return this.http.get<ProfileResponse>('/api/v1/auth/profile/', {
        headers: { Authorization: `Bearer ${this.getAccessToken()}` }
      });
    }
    
    updateProfile(profileData: Partial<UserProfile>): Observable<ProfileResponse> {
      return this.http.put<ProfileResponse>('/api/v1/auth/profile/', profileData, {
        headers: { 
          Authorization: `Bearer ${this.getAccessToken()}`,
          'Content-Type': 'application/json'
        }
      });
    }
    ```
    
    Methods:
        GET: Retrieve authenticated user's profile
        PUT: Update authenticated user's profile
    """
    
    # Authentication is required (configured globally in settings.py)
    # permission_classes = [IsAuthenticated]  # Default from settings
    # authentication_classes = [JWTAuthentication]  # Default from settings

    
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    
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
                        "username": "testuser1",
                        "email": "test@example.com",
                        "first_name": "Test",
                        "last_name": "User",
                        "full_name": "Test User",
                        "initials": "TU",
                        "is_staff": false,
                        "is_active": true,
                        "date_joined": "2025-01-01T12:00:00Z",
                        "last_login": "2025-08-15T10:30:00Z"
                    }
                }
            }
            
        Error Response (401):
            {
                "success": false,
                "message": "Authentication required",
                "errors": {
                    "detail": "Authentication credentials were not provided.",
                    "code": "not_authenticated"
                }
            }
        """
        
        try:
            user = request.user 

            if not isinstance(user, UserDetails):
                return Response({
                    "success": False,
                    "message": "Invalid user type",
                    "errors": {"detail": "Authenticated user is not valid"}
                }, status=status.HTTP_401_UNAUTHORIZED)

            serializer = UserDetailsSerializer(user)
            return Response({
                "success": True,
                "message": "Profile retrieved successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "success": False,
                "message": "An error occurred while retrieving profile",
                "errors": {"detail": str(e)}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
    def put(self, request, *args, **kwargs):
        """
        Update authenticated user's profile in PostgreSQL.
        
        Args:
            request: HTTP request with JWT authentication and profile data
            
        Returns:
            Response: Clean JSON response with updated user profile data
            
        Request Body:
            {
                "email": "newemail@example.com",
                "first_name": "Updated",
                "last_name": "Name"
            }
            
        Success Response (200):
            {
                "success": true,
                "message": "Profile updated successfully",
                "data": {
                    "user": {
                        "id": 1,
                        "username": "testuser1",
                        "email": "newemail@example.com",
                        "first_name": "Updated",
                        "last_name": "Name",
                        "full_name": "Updated Name",
                        "initials": "UN",
                        "is_staff": false,
                        "is_active": true,
                        "date_joined": "2025-01-01T12:00:00Z",
                        "last_login": "2025-08-15T10:30:00Z"
                    }
                }
            }
            
        Error Response (400):
            {
                "success": false,
                "message": "Validation failed",
                "errors": {
                    "email": ["A user with this email address already exists."],
                    "first_name": ["First name can only contain letters, spaces, and hyphens."]
                }
            }
        """
        
        try:
            # Use enhanced UserDetailsSerializer for validation and updates
            serializer = UserDetailsSerializer(
                request.user, 
                data=request.data, 
                partial=True  # Allow partial updates
            )
            
            if serializer.is_valid():
                # Save updated user data to PostgreSQL
                updated_user = serializer.save()
                
                # Log successful profile update
                logger.info(
                    f"User ID {updated_user.id} updated profile fields: {len(request.data)} fields"
                )
                
                return Response({
                    'success': True,
                    'message': 'Profile updated successfully',
                    'data': {
                        'user': serializer.data
                    }
                }, status=status.HTTP_200_OK)
            
            else:
                # Log validation errors for debugging
                logger.warning(
                    f"Profile update validation failed for user {request.user.id}: "
                    f"{serializer.errors}"
                )
                
                return Response({
                    'success': False,
                    'message': 'Validation failed',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            logger.error(f"Error updating user profile for user {request.user.id}: {str(e)}")
            return Response({
                'success': False,
                'message': 'An error occurred while updating profile',
                'errors': {
                    'detail': 'Internal server error',
                    'code': 'server_error'
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SignUpAPIView(APIView):
    """
    User registration endpoint with profile fields.
    
    This view handles user signup with comprehensive validation,
    password confirmation, and profile data creation in PostgreSQL.
    Optimized for Angular 18+ frontend integration.
    
    Methods:
        POST: Create new user account with profile
    
    Frontend Integration (Angular 18+):
    ```typescript
    // TypeScript interface for signup
    interface SignUpRequest {
      username: string;
      password: string;
      confirm_password: string;
      email: string;
      rank: string;
      unitname: string;
      mobileNo: string;
      personalNo: string;
      designation: string;
      phoneNo: string;
      status: boolean;
    }
    
    // Service method
    signup(userData: SignUpRequest): Observable<ApiResponse> {
      return this.http.post<ApiResponse>('/auth/signup/', userData);
    }
    ```
    
    Database Operations:
    - Creates User record in auth_user table
    - Creates UserProfile record in users_userprofile table
    - Uses atomic transactions for data consistency
    - Implements proper foreign key relationships
    """
    
    permission_classes = [AllowAny]
    serializer_class = SignUpSerializer
    
    def post(self, request, *args, **kwargs):
        """
        Create new user account with profile.
        
        Args:
            request: Django HTTP request with user signup data
            
        Returns:
            Response: JSON response with user data or validation errors
            
        Request Body:
        ```json
        {
            "username": "john.doe",
            "password": "StrongPassw0rd!",
            "confirm_password": "StrongPassw0rd!",
            "email": "john.doe@example.com",
            "rank": "Officer1",
            "unitname": "IGD",
            "mobileNo": "+919595422695",
            "personalNo": "+919863758455",
            "designation": "sr eng",
            "phoneNo": "+95867816686",
            "status": true
        }
        ```
        
        Success Response (201):
        ```json
        {
            "success": true,
            "message": "User created successfully",
            "data": {
                "user": {
                    "userId": "550e8400-e29b-41d4-a716-446655440000",
                    "username": "john.doe",
                    "email": "john.doe@example.com",
                    "rank": "Officer1",
                    "unitname": "IGD",
                    "mobileNo": "+919595422695",
                    "personalNo": "+919863758455",
                    "designation": "sr eng",
                    "phoneNo": "+95867816686",
                    "status": "ACTIVE",
                    "message": "User created successfully."
                }
            }
        }
        ```
        
        Validation Error Response (400):
        ```json
        {
            "success": false,
            "message": "Validation failed",
            "errors": {
                "username": [
                    {
                        "message": "Username already exists",
                        "code": "username_conflict"
                    }
                ],
                "email": [
                    {
                        "message": "Email already registered",
                        "code": "email_conflict"
                    }
                ],
                "confirm_password": [
                    {
                        "message": "Passwords do not match",
                        "code": "password_mismatch"
                    }
                ]
            }
        }
        ```
        """


        data = request.data
        required_fields = [
            "userlogin", "role", "rank", "username", "personal_no", "designation",
            "ship_name", "password", "confirm_password", "employee_type", "establishment",
            "nudemail", "phone_no", "mobile_no", "status", "sso_user", "H", "L", "E", "X"
        ]
        missing = [f for f in required_fields if f not in data]
        if missing:
            return Response({
                "success": False,
                "message": "Missing required fields",
                "errors": {field: ["This field is required."] for field in missing}
            }, status=status.HTTP_400_BAD_REQUEST)
        if data["password"] != data["confirm_password"]:
            return Response({
                "success": False,
                "message": "Passwords do not match",
                "errors": {"password": ["Passwords do not match."], "confirm_password": ["Passwords do not match."]}
            }, status=status.HTTP_400_BAD_REQUEST)
        if UserDetails.objects.filter(userlogin=data["userlogin"]).exists():
            return Response({
                "success": False,
                "message": "Userlogin already exists",
                "errors": {"userlogin": ["This userlogin is already taken."]}
            }, status=status.HTTP_400_BAD_REQUEST)
        try:
            with transaction.atomic():
                profile = UserDetails.objects.create(
                    role=data["role"],
                    rank=data["rank"],
                    username=data["username"],
                    userlogin=data["userlogin"],
                    password=make_password(data["password"]),
                    confirm_password=make_password(data["confirm_password"]),
                    personal_no=data["personal_no"],
                    designation=data["designation"],
                    ship_name=data["ship_name"],
                    employee_type=data["employee_type"],
                    establishment=data["establishment"],
                    nudemail=data["nudemail"],
                    phone_no=data["phone_no"],
                    mobile_no=data["mobile_no"],
                    H=data["H"],
                    L=data["L"],
                    E=data["E"],
                    X=data["X"],
                    sso_user=data["sso_user"],
                    status=data["status"]
                )
            return Response({
                "success": True,
                "message": "User created successfully",
                "data": {
                    "id": profile.id,
                    "user_login": profile.userlogin,
                    "role": profile.role,
                    "rank": profile.rank,
                    "name": profile.username,
                    "personal_no": profile.personal_no,
                    "designation": profile.designation,
                    "ship": profile.ship_name,
                    "employee_type": profile.employee_type,
                    "establishment": profile.establishment,
                    "nudemail": profile.nudemail,
                    "phone_no": profile.phone_no,
                    "mobile_no": profile.mobile_no,
                    "H": profile.H,
                    "L": profile.L,
                    "E": profile.E,
                    "X": profile.X,
                    "sso_user": profile.sso_user,
                    "status": profile.status,
                }
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")
            return Response({
                "success": False,
                "message": "User creation failed",
                "errors": {"system": [{"message": str(e), "code": "server_error"}]}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def get_client_ip(self, request):
        """
        Get client IP address from request headers.
        
        Args:
            request: Django HTTP request
            
        Returns:
            str: Client IP address
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

class HomePageView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        tab_type = request.data.get('tab_type')
        if not tab_type:
            return Response({"error": "tab_type is required"}, status=status.HTTP_400_BAD_REQUEST)
        queryset = HomePageInformation.objects.filter(tab_type=tab_type)
        if tab_type == 'Instructions':
            serializer = InstructionsSerializer(queryset, many=True)
        elif tab_type == 'CMMS Offline':
            serializer = OfflineSerializer(queryset, many=True)
        elif tab_type == 'Downloads':
            serializer = DownloadsSerializer(queryset, many=True)
        elif tab_type == 'Publications':
            serializer = PublicationsSerializer(queryset, many=True)
        else:
            return Response({"error": "Invalid tab_type"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data)
    
class FeedbackAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        feedbacks = Feedback.objects.all()
        serializer = FeedbackSerializer(feedbacks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RoleMasterAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        roles = RoleMaster.objects.filter(status=1)
        serializer = RoleMasterSerializer(roles, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RoleMasterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EditRoleAPIView(APIView):
    permission_classes = [AllowAny]

    def put(self, request):
        role_id = request.data.get('role_id')   # take from body

        if not role_id:
            return Response({'error': 'role_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            role = RoleMaster.objects.get(role_id=role_id)
        except RoleMaster.DoesNotExist:
            return Response({'error': 'Role not found'}, status=status.HTTP_404_NOT_FOUND)

        # fields to update
        name = request.data.get('name')
        level = request.data.get('level')

        if name is not None:
            role.name = name
        if level is not None:
            role.level = level

        role.save()
        serializer = RoleMasterSerializer(role)
        return Response(serializer.data, status=status.HTTP_200_OK)

class DeleteRoleAPIView(APIView):
    permission_classes = [AllowAny]

    def delete(self, request):
        role_id = request.data.get('role_id')

        if not role_id:
            return Response({'error': 'role_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            role = RoleMaster.objects.get(role_id=role_id)
        except RoleMaster.DoesNotExist:
            return Response({'error': 'Role not found'}, status=status.HTTP_404_NOT_FOUND)
        
        role.status = 0
        role.save()
        return Response({'message': 'Role deleted (status set to 0)'}, status=status.HTTP_200_OK)

class UserManagementAPIView(APIView):
    """
    Admin-only API for user CRUD operations.
    GET: List all users
    POST: Add a new user
    PUT: Edit user
    DELETE: Delete user
    """
    
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]


    def get(self, request, *args, **kwargs):
        try:
            # details = UserDetails.objects.all()
            details = UserDetails.objects.filter(status=1)
            data = []
            for detail in details:
                data.append({
                    "id": detail.id,
                    "user_login": detail.userlogin,
                    "role": detail.role,
                    "rank": detail.rank,
                    "name": detail.username,
                    "personal_no": detail.personal_no,
                    "designation": detail.designation,
                    "ship": detail.ship_name,
                    "employee_type": detail.employee_type,
                    "establishment": detail.establishment,
                    "nudemail": detail.nudemail,
                    "phone_no": detail.phone_no,
                    "sso_user": detail.sso_user,
                    "H": detail.H,
                    "L": detail.L,
                    "E": detail.E,
                    "X": detail.X,
                    "status": detail.status,
                })
            return Response({
                "success": True,
                "message": "Users fetched successfully",
                "data": data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error fetching users: {str(e)}")
            return Response({
                "success": False,
                "message": "User fetch failed",
                "errors": {"system": [{"message": str(e), "code": "server_error"}]}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def post(self, request, *args, **kwargs):
        required_fields = [
            "userlogin", "role", "rank", "username", "personal_no", "designation",
            "ship_name", "password", "confirm_password", "employee_type", "establishment", "nudemail", "phone_no", "status","sso_user", "H", "L", "E", "X",
            ]

        data = request.data
        missing = [f for f in required_fields if f not in data]
        if missing:
            return Response({
                "success": False,
                "message": "Missing required fields",
                "errors": {field: ["This field is required."] for field in missing}
            }, status=status.HTTP_400_BAD_REQUEST)
        if data["password"] != data["confirm_password"]:
            return Response({
                "success": False,
                "message": "Passwords do not match",
                "errors": {"password": ["Passwords do not match."], "confirm_password": ["Passwords do not match."]}
            }, status=status.HTTP_400_BAD_REQUEST)
        try:
            with transaction.atomic():
                user = User.objects.create_user(
                    username=data["username"],
                    password=data["password"]
                )
                profile = UserDetails.objects.create(
                    role=data["role"],
                    rank=data["rank"],
                    username=data["username"],
                    userlogin=data["personal_no"],
                    password=make_password(data["password"]),
                    confirm_password=make_password(data["confirm_password"]),
                    personal_no=data["personal_no"],
                    designation=data["designation"],
                    ship_name=data["ship_name"],
                    employee_type=data["employee_type"],
                    establishment=data["establishment"],
                    nudemail=data["nudemail"],
                    phone_no=data["phone_no"],
                    H=data["H"],
                    L=data["L"],
                    E=data["E"],
                    X=data["X"],
                    sso_user=data["sso_user"],
                    status=data["status"]
                )
            return Response({
                "success": True,
                "message": "User created successfully",
                "data": {
                    "id": profile.id,
                    "user_login": profile.personal_no,
                    "role": profile.role,
                    "rank": profile.rank,
                    "name": profile.username,
                    "personal_no": profile.personal_no,
                    "designation": profile.designation,
                    "ship": profile.ship_name,
                    "employee_type": profile.employee_type,
                    "establishment": profile.establishment,
                    "nudemail": profile.nudemail,
                    "phone_no": profile.phone_no,
                    "H": profile.H,
                    "L": profile.L,
                    "E": profile.E,
                    "X": profile.X,
                    "sso_user": profile.sso_user,
                    "status": profile.status,
                }
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")
            return Response({
                "success": False,
                "message": "User creation failed",
                "errors": {"system": [{"message": str(e), "code": "server_error"}]}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



    def put(self, request, *args, **kwargs):
        user_id = request.data.get('id')
        if not user_id:
            return Response({
                "success": False,
                "message": "User ID is required for update",
                "errors": {"id": ["This field is required."]}
            }, status=status.HTTP_400_BAD_REQUEST)
        try:
            profile = UserDetails.objects.get(id=user_id)
        except UserDetails.DoesNotExist:
            return Response({
                "success": False,
                "message": "User not found",
                "errors": {"id": ["User does not exist."]}
            }, status=status.HTTP_404_NOT_FOUND)
        data = request.data
        # Update password if provided and matches confirm_password
        if "password" in data and "confirm_password" in data:
            if data["password"] != data["confirm_password"]:
                return Response({
                    "success": False,
                    "message": "Passwords do not match",
                    "errors": {"password": ["Passwords do not match."], "confirm_password": ["Passwords do not match."]}
                }, status=status.HTTP_400_BAD_REQUEST)
            profile.password = make_password(data["password"])
            profile.confirm_password = make_password(data["confirm_password"])
            
        for field in [
                "role", "rank", "username", "userlogin", "personal_no", "designation", "ship_name",
                "employee_type", "establishment", "nudemail", "phone_no", "mobile_no", "status","sso_user", "H", "L", "E", "X"
        ]:
                if field in data:
                    setattr(profile, field, data[field])
        profile.save()
        return Response({
            "success": True,
            "message": "User updated successfully",
            "data": {
            "id": profile.id,
            "user_login": profile.userlogin,
            "role": profile.role,
            "rank": profile.rank,
            "name": profile.username,
            "personal_no": profile.personal_no,
            "designation": profile.designation,
            "ship": profile.ship_name,
            "employee_type": profile.employee_type,
            "establishment": profile.establishment,
            "nudemail": profile.nudemail,
            "phone_no": profile.phone_no,
            "mobile_no": profile.mobile_no,
            "sso_user": profile.sso_user,
            "H": profile.H,
            "L": profile.L,
            "E": profile.E,
            "E": profile.X,
            "status": profile.status,
        }
        }, status=status.HTTP_200_OK)


    def delete(self, request, *args, **kwargs):
        user_id = request.data.get('id')
        if not user_id:
            return Response({
                "success": False,
                "message": "User ID is required for deletion",
                "errors": {"id": ["This field is required."]}
            }, status=status.HTTP_400_BAD_REQUEST)
        try:
            profile = UserDetails.objects.get(id=user_id)
            profile.status = 0
            profile.save()
            return Response({
                "success": True,
                "message": "User deleted successfully"
            }, status=status.HTTP_200_OK)
        except UserDetails.DoesNotExist:
            return Response({
                "success": False,
                "message": "User not found",
                "errors": {"id": ["User does not exist."]}
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error deleting user: {str(e)}")
            return Response({
                "success": False,
                "message": "User deletion failed",
                "errors": {"system": [{"message": str(e), "code": "server_error"}]}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
