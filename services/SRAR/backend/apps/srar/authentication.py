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
