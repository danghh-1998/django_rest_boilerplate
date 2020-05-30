import binascii
from datetime import timedelta
import os

from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError, APIException, AuthenticationFailed
from django.utils import timezone
from django.conf import settings

from auth_tokens.services import expire_token, create_token
from utils.mailers import send_init_pwd
from .models import User


def create_user(data, **kwargs):
    for key, value in kwargs.items():
        data[key] = value
    init_password = binascii.hexlify(os.urandom(10)).decode()
    data['password'] = init_password
    user = User.objects.create_user(**dict(data))
    send_init_pwd(user=user, password=init_password)
    return user, init_password


def update_user(user, data):
    if not any(data.values()):
        raise ValidationError
    user.name = data.get('name') or user.name
    user.tel = data.get('tel') or user.tel
    user.save(update_fields=['name', 'tel'])


def deactivate_user(user):
    expire_token(user=user)
    user.is_active = False
    user.save(update_fields=['is_active'])
    user.delete()


def activate_user(user):
    user.is_active = True
    user.save(update_fields=['is_active'])


def change_password(user, data):
    if data.get('password') != data.get('password_confirmation'):
        raise ValidationError
    authenticate_user(email=user.email, password=data.get('old_password'))
    user.set_password(data.get('new_password'))
    user.change_init_password = True
    user.save(update_fields=['password', 'change_init_password'])


def generate_password_token(data):
    email = data.get('email')
    user = get_user_by(email=email)
    user.reset_password_token = binascii.hexlify(os.urandom(20)).decode()
    user.reset_password_token_expired_at = timezone.now() + timedelta(
        seconds=settings.RESET_PASSWORD_TOKEN_EXPIRED_AFTER)
    user.save(update_fields=['reset_password_token', 'reset_password_token_expired_at'])


def reset_password(data):
    if data.get('password') != data.get('password_confirmation'):
        raise ValidationError
    user = get_user_by(reset_password_token=data.get('reset_password_token'))
    if not user:
        raise APIException('Invalid token')
    elif user.reset_password_token_expired_at < timezone.now():
        raise APIException('Token expired')
    user.set_password(data.get('password'))
    user.save(update_fields=['password'])


def authenticate_user(email, password):
    user = authenticate(email=email, password=password)
    if not user.change_init_password:
        raise APIException('You must change initial password')
    if not user:
        raise AuthenticationFailed
    expire_token(user=user)
    auth_token = create_token(user=user)
    return auth_token.key


def get_user_by(**kwargs):
    user = User.objects.get(**kwargs)
    if not user:
        raise APIException(code=200, detail='object not found')
    return user


def get_deleted_user_by(**kwargs):
    user = User.objects.deleted_only().get(**kwargs)
    if not user:
        raise APIException(code=200, detail='object not found')
    return user
