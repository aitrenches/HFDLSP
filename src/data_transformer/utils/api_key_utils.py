import secrets


def generate_api_key():
    return secrets.token_hex(16)  # Generates a 32-character hexadecimal key
