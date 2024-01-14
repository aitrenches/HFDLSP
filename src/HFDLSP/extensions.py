from drf_spectacular.authentication import OpenApiAuthenticationExtension


class CustomOpenApiAuthenticationExtension(OpenApiAuthenticationExtension):
    name = "ApiKeyAuth"

    def get_security_definition(self, auto_schema):
        return {
            "type": "apiKey",
            "in": "header",
            "name": "apiKeyAuth",
        }
