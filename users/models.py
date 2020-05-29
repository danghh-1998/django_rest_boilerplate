from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE
from django.conf import settings

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin, SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    email = models.EmailField(max_length=settings.CHARFIELD_LENGTH, unique=True)
    name = models.CharField(max_length=settings.CHARFIELD_LENGTH)
    tel = models.CharField(max_length=settings.CHARFIELD_LENGTH)
    verify_email_token = models.CharField(max_length=settings.CHARFIELD_LENGTH)
    verify_email_token_expired_at = models.DateTimeField(null=True)
    is_active = models.BooleanField(default=False)
    reset_password_token = models.CharField(max_length=settings.CHARFIELD_LENGTH)
    reset_password_token_expired_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    class Meta:
        app_label = 'users'
        db_table = 'user'

    @property
    def full_name(self):
        return self.name

    @property
    def short_name(self):
        return self.name

    def __str__(self):
        return self.email
