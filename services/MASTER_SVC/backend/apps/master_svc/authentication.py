from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken

from types import SimpleNamespace

class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        userlogin = validated_token.get("userlogin", None)
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
