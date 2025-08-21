# import jwt
# import logging
# from rest_framework import authentication, exceptions
# from django.conf import settings
# from apps.users.models import UserDetails

# logger = logging.getLogger(__name__)


# # Constants
# ACTIVE_USER_STATUS = '1'
# BEARER_PREFIX = 'Bearer '

# class CustomJWTAuthentication(authentication.BaseAuthentication):
#     """
#     Custom JWT Authentication class for microservices.
    
#     Validates JWT tokens and authenticates users based on the 'userlogin' claim.
#     """
    
#     def authenticate(self, request):
#         """
#         Authenticate the request and return a two-tuple of (user, token_payload).
        
#         Returns None if authentication is not attempted.
#         Raises AuthenticationFailed for explicit authentication failures.
#         """
#         auth_header = request.headers.get('Authorization')
#         if not auth_header or not auth_header.startswith(BEARER_PREFIX):
#             return None
            
#         # Safely extract token from Authorization header
#         parts = auth_header.split(' ')
#         if len(parts) != 2:
#             logger.warning(f"Malformed Authorization header received")
#             return None
#         token = parts[1]
        
#         try:
#             payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
#         except jwt.ExpiredSignatureError:
#             logger.warning("Expired token used for authentication")
#             raise exceptions.AuthenticationFailed('Authentication credentials have expired')
#         except jwt.InvalidTokenError:
#             logger.warning("Invalid token used for authentication")
#             raise exceptions.AuthenticationFailed('Invalid authentication credentials')
            
#         userlogin = payload.get('userlogin')
#         if not userlogin:
#             logger.warning("Token missing userlogin claim")
#             raise exceptions.AuthenticationFailed('Invalid authentication credentials')
            
#         try:
#             user = UserDetails.objects.get(userlogin=userlogin, status=ACTIVE_USER_STATUS)
#             logger.info(f"Successful authentication for user: {userlogin}")
#         except UserDetails.DoesNotExist:
#             logger.warning(f"Authentication failed - user not found or inactive")
#             raise exceptions.AuthenticationFailed('Authentication credentials are invalid')
            
#         return (user, payload)




from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken

from types import SimpleNamespace

class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):   
        userlogin = validated_token.get("userlogin", None)
        user_role = validated_token.get("role", None)
        print(f"\n\nUser login: {userlogin}, User role: {user_role}")
        print(f"\n\nToken claims: {validated_token}")

        # Print key values from validated_token (SimpleJWT returns a Token object, use .payload)
        token_dict = dict(getattr(validated_token, 'payload', validated_token))
        for key, value in token_dict.items():
            print(f"Token claim - {key}: {value}")

        if not userlogin:
            raise InvalidToken("Token missing 'userlogin' claim")

        # Create a dummy user object with userlogin as username
        user = SimpleNamespace()
        user.username = userlogin
        
        user.userlogin = userlogin
        user.pk = userlogin  # Add pk attribute for DRF compatibility
        user.is_authenticated = True
        user.is_superuser = False  # Set as needed, or extract from token if present
        return user
