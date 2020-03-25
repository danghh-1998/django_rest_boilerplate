from datetime import timedelta

from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate
from django.utils import timezone

from auth_tokens.models import AuthToken


def expires_in(auth_token):
    return auth_token.expired_at - timezone.now()


def is_token_expired(auth_token):
    return expires_in(auth_token) < timedelta(seconds=0)


def token_expire_handler(auth_token):
    is_expired = is_token_expired(auth_token)
    if is_expired:
        auth_token = AuthToken.objects.create(user=auth_token.user)
    return is_expired, auth_token


def get_token(user):
    return user.auth_tokens.latest('created_at')


def expire_token(user):
    try:
        auth_token = get_token(user)
        auth_token.expired_at = timezone.now()
        auth_token.save(update_fields=['expired_at'])
    except AuthToken.DoesNotExist:
        pass


def authenticate_user(email, password):
    user = authenticate(email=email, password=password)
    if not user:
        return None, None

    expire_token(user)
    auth_token = AuthToken.objects.create(user=user)
    return user, auth_token


class ExpiringTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        try:
            auth_token = AuthToken.objects.get(key=key)
        except AuthToken.DoesNotExist:
            raise AuthenticationFailed('Invalid Token')
        if not auth_token.user.is_active:
            raise AuthenticationFailed('User is not active')

        is_expired, auth_token = token_expire_handler(auth_token)

        if is_expired:
            raise AuthenticationFailed('Token is expired')
        return auth_token.user, auth_token
