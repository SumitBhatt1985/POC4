import jwt
from rest_framework import authentication, exceptions
from django.conf import settings
from apps.users.models import UserDetails


# class CustomJWTAuthentication(JWTAuthentication):
#     def get_user(self, validated_token):
#         userlogin = validated_token.get("userlogin", None)
#         if not userlogin:
#             raise InvalidToken("Token missing 'userlogin' claim")

#         try:
#             user = UserDetails.objects.get(userlogin=userlogin, status='1')
#             user.is_authenticated = True
#             return user
#         except UserDetails.DoesNotExist:
#             raise InvalidToken("User not found for given userlogin")

class CustomJWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None
        token = auth_header.split(' ')[1]
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token expired')
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed('Invalid token')
        userlogin = payload.get('userlogin')
        if not userlogin:
            raise exceptions.AuthenticationFailed('Token missing userlogin')
        try:
            user = UserDetails.objects.get(userlogin=userlogin, status='1')
        except UserDetails.DoesNotExist:
            raise exceptions.AuthenticationFailed('User not found')
        return (user, payload)