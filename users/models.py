import binascii
import os
from datetime import timedelta

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.conf import settings
from model_utils import Choices

from .managers import UserManager

GENDER = Choices('Male', 'Female')


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    gender = models.CharField(choices=GENDER, default=GENDER.Male, max_length=10)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    verify_email_token = models.CharField(max_length=40, default=binascii.hexlify(os.urandom(20)).decode())
    verify_email_token_expired_at = models.DateTimeField(
        default=timezone.now() + timedelta(seconds=settings.VERIFY_EMAIL_TOKEN_EXPIRED_AFTER))
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        app_label = 'users'
        db_table = 'user'

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def __str__(self):
        return self.email
