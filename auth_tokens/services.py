from django.utils import timezone
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .models import AuthToken


def expire_token(user):
    try:
        auth_token = user.auth_token
        auth_token.expired_at = timezone.now()
        auth_token.user_id = None
        auth_token.save(update_fields=['expired_at', 'user_id'])
        auth_token.delete()
    except AuthToken.DoesNotExist:
        pass


def create_token(user):
    auth_token = AuthToken.objects.create(user=user)
    return auth_token


def token_expire_handler(auth_token):
    if auth_token.is_expired:
        auth_token = create_token(user=auth_token.user)
    return auth_token.is_expired, auth_token


class ExpiringTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        try:
            auth_token = AuthToken.objects.get(key=key)
        except AuthToken.DoesNotExist:
            raise AuthenticationFailed
        if not auth_token.user.is_active:
            raise AuthenticationFailed

        is_expired, auth_token = token_expire_handler(auth_token)

        if is_expired:
            raise AuthenticationFailed
        return auth_token.user, auth_token
