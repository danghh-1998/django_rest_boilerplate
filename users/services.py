from datetime import timedelta

from django.utils import timezone
from django.conf import settings

from auth_tokens.services import expire_token
from utils.token_maker import generate_token
from utils.exceptions import *
from .models import User


def get_user_by(raise_exception=True, with_deleted=False, **kwargs):
    user = User.objects.all_with_deleted().filter(**kwargs).first() if with_deleted else User.objects.all().filter(
        **kwargs).first()
    if not user and raise_exception:
        raise ObjectNotFound
    return user


def create_user(**kwargs):
    password = kwargs.pop('password')
    password_confirm = kwargs.pop('password_confirm')
    email = kwargs.get('email')
    user = get_user_by(email=email, raise_exception=False, with_deleted=True)
    if user:
        raise DuplicateEntry(key='email', entry=email)
    if password != password_confirm:
        raise ValidationError(message='password and password_confirm must be the same')
    user = User.objects.create(**kwargs)
    user.set_password(password)
    user.verify_email_token = generate_token(length=settings.TOKEN_LENGTH)
    user.verify_email_token_expired_at = timezone.now() + timedelta(
        seconds=settings.TOKEN_EXPIRED_AFTER_SECONDS)
    user.save()
    return user


def authenticate_user(email, password):
    user = get_user_by(email=email)
    if not user.check_password(password):
        raise Unauthenticated(message='Incorrect email or password')
    return user


def verify_email(**kwargs):
    email_token = kwargs.get('email_token')
    user = get_user_by(verify_email_token=email_token)
    if user.is_active:
        raise ValidationError('Account already verified')
    user.is_active = True
    user.save()
    return user


def change_password(user, **kwargs):
    old_password = kwargs.pop('old_password')
    authenticate_user(email=user.email, password=old_password)
    password = kwargs.pop('password')
    password_confirm = kwargs.pop('password_confirm')
    if password != password_confirm:
        raise ValidationError('password and password_confirm must be the same')
    user.set_password(raw_password=password)
    user.save()
    return user


def gen_reset_password_token(**kwargs):
    email = kwargs.pop('email')
    user = get_user_by(email=email)
    user.reset_password_token = generate_token(length=settings.TOKEN_LENGTH)
    user.reset_password_token_expired_at = timezone.now() + timedelta(
        seconds=settings.TOKEN_EXPIRED_AFTER_SECONDS)
    user.save()
    return user


def reset_password(**kwargs):
    reset_password_token = kwargs.get('reset_password_token')
    user = get_user_by(reset_password_token=reset_password_token, raise_exception=False)
    if not user:
        raise InvalidToken
    elif user.reset_password_token_expired_at < timezone.now():
        raise TokenExpired(message='Token expired')
    password = kwargs.pop('password')
    password_confirm = kwargs.pop('password_confirm')
    if password != password_confirm:
        raise ValidationError(message='password and password_confirm must be the same')
    user.set_password(password)
    user.reset_password_token_expired_at = timezone.now()
    user.save()
    return user


def update_user(user, **kwargs):
    for (key, value) in kwargs.items():
        setattr(user, key, value)
    user.save()
    return user


def deactivate_user(user):
    user.delete()
    return user
