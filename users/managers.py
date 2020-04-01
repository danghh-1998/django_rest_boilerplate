from django.contrib.auth.base_user import BaseUserManager
from safedelete.managers import SafeDeleteManager


class UserManager(BaseUserManager, SafeDeleteManager):
    def create_user(self, email, password, **kwargs):
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user
