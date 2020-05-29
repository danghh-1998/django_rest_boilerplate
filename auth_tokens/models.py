from datetime import timedelta

from django.db import models
from django.conf import settings
from django.utils import timezone
from safedelete.models import SafeDeleteModel, SOFT_DELETE

from users.models import User
from .managers import AuthTokenManager
from utils.token_maker import generate_token


class AuthToken(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE

    key = models.CharField(max_length=40, primary_key=True)
    expired_at = models.DateTimeField()
    user = models.ForeignKey(User, related_name='auth_tokens', on_delete=models.SET_NULL, null=True, unique=False)
    created_at = models.DateTimeField(auto_now_add=False)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AuthTokenManager()

    class Meta:
        app_label = 'auth_tokens'
        db_table = 'auth_token'

    @property
    def is_expired(self):
        return self.expired_at < timezone.now()

    def save(self, *args, **kwargs):
        self.created_at = timezone.now()
        if not self.key:
            self.key = generate_token(settings.TOKEN_LENGTH)
            self.expired_at = self.created_at + timedelta(seconds=settings.TOKEN_EXPIRED_AFTER_SECONDS)
        return super().save(*args, **kwargs)
