from django.http import JsonResponse
from .settings import API_KEY


class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        api_key = request.headers.get("Authorization")
        if api_key != API_KEY:
            return JsonResponse(
                {"success": False, "error": "Invalid API Key."}, status=401
            )

        response = self.get_response(request)
        return response
