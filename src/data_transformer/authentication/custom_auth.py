# your_app/authentication/custom_auth.py
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed


class ApiKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        api_key = request.META.get('HTTP_API_KEY')

        if not api_key:
            return None

        # Add your logic to validate the API key
        valid_api_keys = ['your_api_key_1', 'your_api_key_2']
        if api_key not in valid_api_keys:
            raise AuthenticationFailed('Invalid API key')

        # If the API key is valid, you can return a dummy user
        # You may customize this part based on your user model
        user = None

        return user, None
