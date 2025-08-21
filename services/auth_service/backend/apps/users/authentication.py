import jwt
import logging
from rest_framework import authentication, exceptions
from django.conf import settings
from apps.users.models import UserDetails

logger = logging.getLogger(__name__)


# Constants
ACTIVE_USER_STATUS = '1'
BEARER_PREFIX = 'Bearer '

class CustomJWTAuthentication(authentication.BaseAuthentication):
    """
    Custom JWT Authentication class for microservices.
    
    Validates JWT tokens and authenticates users based on the 'userlogin' claim.
    """
    
    def authenticate(self, request):
        """
        Authenticate the request and return a two-tuple of (user, token_payload).
        
        Returns None if authentication is not attempted.
        Raises AuthenticationFailed for explicit authentication failures.
        """
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith(BEARER_PREFIX):
            return None
            
        # Safely extract token from Authorization header
        parts = auth_header.split(' ')
        if len(parts) != 2:
            logger.warning(f"Malformed Authorization header received")
            return None
        token = parts[1]
        
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            logger.warning("Expired token used for authentication")
            raise exceptions.AuthenticationFailed('Authentication credentials have expired')
        except jwt.InvalidTokenError:
            logger.warning("Invalid token used for authentication")
            raise exceptions.AuthenticationFailed('Invalid authentication credentials')
            
        userlogin = payload.get('userlogin')
        if not userlogin:
            logger.warning("Token missing userlogin claim")
            raise exceptions.AuthenticationFailed('Invalid authentication credentials')
            
        try:
            user = UserDetails.objects.get(userlogin=userlogin, status=ACTIVE_USER_STATUS)
            logger.info(f"Successful authentication for user: {userlogin}")
        except UserDetails.DoesNotExist:
            logger.warning(f"Authentication failed - user not found or inactive")
            raise exceptions.AuthenticationFailed('Authentication credentials are invalid')
            
        return (user, payload)