from rest_framework.exceptions import ValidationError, APIException

from .models import Client
from users.services import create_user
from users.services import deactivate_user


def get_super_admin(client):
    return list(filter(lambda user: user.is_super_admin, client.users))[0]


def create_client(data):
    validated_data = data.copy()
    client = Client.objects.create(client_name=validated_data.get('client_name'))
    validated_data.pop('client_name')
    validated_data['client_id'] = client.id
    create_user(data=validated_data, role=2)
    return client


def get_client_by(**kwargs):
    client = Client.objects.get(**kwargs)
    if not client:
        raise APIException(code=200, detail='object not found')
    return client


def get_deleted_client_by(**kwargs):
    client = Client.objects.deleted_only().get(**kwargs)
    if not client:
        raise APIException(code=200, detail='object not found')
    return client


def update_client(client, data):
    if not any(data.values()):
        raise ValidationError
    client.client_name = data.get('client_name')
    client.save(update_fields=['client_name'])


def deactivate_client(client):
    for user in client.users.all():
        deactivate_user(user=user)
    client.is_active = False
    client.save(update_fields=['is_active'])
    client.delete()


def activate_client(client):
    client.is_active = True
    client.save(update_fields=['is_active'])
