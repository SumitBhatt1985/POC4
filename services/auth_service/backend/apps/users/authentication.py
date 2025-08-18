from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from .models import UserDetails

class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        userlogin = validated_token.get("userlogin", None)
        if not userlogin:
            raise InvalidToken("Token missing 'userlogin' claim")

        try:
            user = UserDetails.objects.get(userlogin=userlogin, status='1')
            user.is_authenticated = True
            return user
        except UserDetails.DoesNotExist:
            raise InvalidToken("User not found for given userlogin")
