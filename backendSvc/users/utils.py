from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.settings import api_settings


def get_token(user=None, refresh_token_str=None):
    if not user and not refresh_token_str:
        raise ValueError("Either 'user' or 'refresh_token_str' must be provided.")
    try:
        if user:
            refresh_token = RefreshToken.for_user(user=user)
        elif refresh_token_str:
            refresh_token = RefreshToken(token=refresh_token_str)
    except TokenError:
        raise ValueError("Invalid or expired token.")
    access_token = refresh_token.access_token
    token_lifetime = api_settings.ACCESS_TOKEN_LIFETIME
    expires_in = int(token_lifetime.total_seconds())
    token_type = api_settings.AUTH_HEADER_TYPES[0]

    data = {
        'token_type': token_type,
        'refresh_token': refresh_token,
        'access_token': access_token,
        'expiration': expires_in,
    }
    return data