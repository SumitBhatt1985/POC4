import jwt
import logging
from rest_framework import authentication, exceptions
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache

logger = logging.getLogger(__name__)
UserDetails = get_user_model()

# Constants
ACTIVE_USER_STATUS = '1'
BEARER_PREFIX = 'Bearer '
TOKEN_BLACKLIST_PREFIX = 'blacklisted_token:'


class CustomJWTAuthentication(authentication.BaseAuthentication):
    """
    Custom JWT Authentication class for microservices.
    
    Validates JWT tokens and authenticates users based on the 'userlogin' claim.
    """
    
    def authenticate(self, request):
        """
        Authenticate the request and return a two-tuple of (user, token_payload).
        
        Returns None if authentication is not attempted or fails silently.
        Raises AuthenticationFailed for explicit authentication failures.
        """
        auth_header = self._get_auth_header(request)
        if not auth_header:
            return None
            
        token = self._extract_token(auth_header)
        if not token:
            return None
            
        # Check if token is blacklisted
        if self._is_token_blacklisted(token):
            raise exceptions.AuthenticationFailed('Token has been revoked')
            
        payload = self._decode_token(token)
        user = self._get_user_from_payload(payload)
        
        # Log successful authentication
        logger.info(f"Successful authentication for user: {user.userlogin}")
        
        return (user, payload)
    
    def _get_auth_header(self, request):
        """Extract Authorization header from request."""
        return request.headers.get('Authorization')
    
    def _extract_token(self, auth_header):
        """Extract JWT token from Authorization header."""
        if not auth_header or not auth_header.startswith(BEARER_PREFIX):
            return None
            
        parts = auth_header.split(' ')
        if len(parts) != 2:
            logger.warning(f"Malformed Authorization header: {auth_header[:50]}...")
            return None
            
        return parts[1]
    
    def _is_token_blacklisted(self, token):
        """Check if token is in the blacklist."""
        blacklist_key = f"{TOKEN_BLACKLIST_PREFIX}{token}"
        return cache.get(blacklist_key) is not None
    
    def _decode_token(self, token):
        """Decode and validate JWT token."""
        try:
            payload = jwt.decode(
                token, 
                settings.SECRET_KEY, 
                algorithms=["HS256"],
                options={"verify_exp": True}  # Explicitly verify expiration
            )
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("Expired token used for authentication")
            raise exceptions.AuthenticationFailed('Authentication credentials have expired')
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid token used for authentication: {str(e)}")
            raise exceptions.AuthenticationFailed('Invalid authentication credentials')
    
    def _get_user_from_payload(self, payload):
        """Extract and validate user from token payload."""
        userlogin = payload.get('userlogin')
        if not userlogin:
            logger.warning("Token missing userlogin claim")
            raise exceptions.AuthenticationFailed('Invalid authentication credentials')
        
        try:
            # Use select_related if user model has foreign key relationships
            user = UserDetails.objects.get(
                userlogin=userlogin, 
                status=ACTIVE_USER_STATUS
            )
            return user
        except UserDetails.DoesNotExist:
            logger.warning(f"Authentication failed for userlogin: {userlogin}")
            raise exceptions.AuthenticationFailed('Authentication credentials are invalid')
    
    @staticmethod
    def blacklist_token(token, expiration_time=None):
        """
        Add token to blacklist.
        
        Args:
            token (str): JWT token to blacklist
            expiration_time (int): TTL for the blacklist entry (defaults to token exp)
        """
        blacklist_key = f"{TOKEN_BLACKLIST_PREFIX}{token}"
        
        if expiration_time is None:
            try:
                # Decode without verification to get expiration
                payload = jwt.decode(token, options={"verify_signature": False})
                exp = payload.get('exp')
                if exp:
                    import time
                    expiration_time = max(0, exp - int(time.time()))
                else:
                    expiration_time = 3600  # Default 1 hour
            except:
                expiration_time = 3600  # Default 1 hour
        
        cache.set(blacklist_key, True, timeout=expiration_time)
        logger.info(f"Token blacklisted successfully")


class TokenBlacklistMixin:
    """
    Mixin to add token blacklisting capability to views.
    """
    
    def blacklist_current_token(self, request):
        """Blacklist the token used in the current request."""
        auth_header = request.headers.get('Authorization', '')
        if auth_header.startswith(BEARER_PREFIX):
            token = auth_header.split(' ')[1]
            CustomJWTAuthentication.blacklist_token(token)
