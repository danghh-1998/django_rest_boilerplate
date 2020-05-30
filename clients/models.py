from django.db import models
from safedelete.models import SafeDeleteModel, SOFT_DELETE

from .managers import ClientManager


class Client(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE

    client_name = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = ClientManager()

    class Meta:
        app_label = 'clients'
        db_table = 'client'

    def __str__(self):
        return self.client_name

    @property
    def user_num(self):
        return len(self.users.all())
