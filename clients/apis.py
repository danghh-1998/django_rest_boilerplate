from rest_framework import serializers
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from users.models import User
from .services import *
from .models import Client
from .permissions import SuperAdminPermission, SystemAdminPermission


class SignUpApi(APIView):
    permission_classes = [AllowAny, ]

    class InputSerializer(serializers.Serializer):
        email = serializers.CharField(required=True, max_length=255)
        client_name = serializers.CharField(required=True, max_length=255)
        name = serializers.CharField(required=True, max_length=255)
        tel = serializers.CharField(required=True, max_length=255)

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        create_client(data=serializer.validated_data)
        return Response(status=status.HTTP_200_OK)


class ClientDetailApi(APIView):
    permission_classes = [SuperAdminPermission, ]

    class OutputSerializer(serializers.ModelSerializer):
        user_num = serializers.ReadOnlyField()

        class Meta:
            model = Client
            fields = ['id', 'client_name', 'created_at', 'user_num']

    def get(self, request, client_id):
        client = get_client_by(id=client_id)
        self.check_object_permissions(request=request, obj=client)
        serializer = self.OutputSerializer(client)
        return Response({'client': serializer.data}, status=status.HTTP_200_OK)


class ClientUpdateApi(APIView):
    permission_classes = [SuperAdminPermission, ]

    class InputSerializer(serializers.Serializer):
        client_name = serializers.CharField(required=True, max_length=255)

    def put(self, request, client_id):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        client = get_client_by(id=client_id)
        self.check_object_permissions(request=request, obj=client)
        update_client(client=client, data=serializer.validated_data)
        return Response(status=status.HTTP_200_OK)


class ClientDeactivateApi(APIView):
    permission_classes = [SuperAdminPermission, ]

    def delete(self, request, client_id):
        client = get_client_by(id=client_id)
        self.check_object_permissions(request=request, obj=client)
        deactivate_client(client=client)
        return Response(status=status.HTTP_200_OK)


class ClientActivateApi(APIView):
    permission_classes = [SystemAdminPermission, ]

    def put(self, request, client_id):
        client = get_deleted_client_by(id=client_id)
        self.check_object_permissions(request=request, obj=client)
        activate_client(client=client)
        return Response(status=status.HTTP_200_OK)


class ClientListUsersApi(APIView):
    permission_classes = [SuperAdminPermission, ]

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ('id', 'email', 'name', 'tel', 'role', 'created_at')

    def get(self, request, client_id):
        client = get_client_by(id=client_id)
        self.check_object_permissions(request=request, obj=client)
        users = list(client.users.all())
        serializer = self.OutputSerializer(users, many=True)
        return Response({'user': serializer.data}, status=status.HTTP_200_OK)
