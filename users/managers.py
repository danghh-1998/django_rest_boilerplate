from django.contrib.auth.base_user import BaseUserManager
from safedelete.managers import SafeDeleteManager


class UserManager(BaseUserManager, SafeDeleteManager):
    pass
