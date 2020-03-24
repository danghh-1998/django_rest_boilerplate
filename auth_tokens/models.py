import binascii
import os
from datetime import timedelta

from django.db import models
from django.conf import settings
from django.utils import timezone

from users.models import User


class AuthToken(models.Model):
    key = models.CharField(max_length=40, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='auth_tokens')
    created_at = models.DateTimeField(auto_now_add=False)
    expired_at = models.DateTimeField(auto_now_add=False)

    class Meta:
        db_table = 'auth_token'

    def save(self, *args, **kwargs):
        self.created_at = timezone.now()
        if not self.key:
            self.key = self.generate_key()
            self.expired_at = self.created_at + timedelta(seconds=settings.TOKEN_EXPIRED_AFTER_SECONDS)
        return super().save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()
