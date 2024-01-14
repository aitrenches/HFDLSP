from django.http import JsonResponse
from functools import wraps
from .settings import API_KEY


def api_key_auth(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.headers.get("Authorization") != API_KEY:
            return JsonResponse({"error": "Invalid API Key."}, status=401)
        return view_func(request, *args, **kwargs)

    return _wrapped_view
