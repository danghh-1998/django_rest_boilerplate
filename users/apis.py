from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.conf import settings

from users.permissions import *
from .services import *
from .models import User
from auth_tokens.services import create_token
from utils.serializer_validator import validate_serializer
from utils.mailers import send_verify_email, send_reset_password_token


class UserSignInApi(APIView):
    permission_classes = [AllowAny, ]

    class RequestSerializer(serializers.Serializer):
        email = serializers.EmailField(required=True, max_length=settings.CHARFIELD_LENGTH)
        password = serializers.CharField(required=True, max_length=settings.CHARFIELD_LENGTH)

    class ResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ['id', 'name', 'email', 'tel', 'created_at', 'updated_at']

    def post(self, request):
        request_serializer = self.RequestSerializer(data=request.data)
        validate_serializer(serializer=request_serializer)
        user = authenticate_user(**request_serializer.validated_data)
        token = create_token(user)
        response_serializer = self.ResponseSerializer(user)
        return Response({
            'user': response_serializer.data,
            'token': token
        }, status=status.HTTP_200_OK)


class UserSignUpApi(APIView):
    permission_classes = [AllowAny, ]

    class RequestSerializer(serializers.Serializer):
        email = serializers.CharField(required=True, max_length=settings.CHARFIELD_LENGTH)
        name = serializers.CharField(required=True, max_length=settings.CHARFIELD_LENGTH)
        tel = serializers.CharField(required=True, max_length=settings.CHARFIELD_LENGTH)
        password = serializers.CharField(required=True, max_length=settings.CHARFIELD_LENGTH)
        password_confirm = serializers.CharField(required=True, max_length=settings.CHARFIELD_LENGTH)

    class ResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ['id', 'name', 'email', 'tel', 'created_at', 'updated_at']

    def post(self, request):
        request_serializer = self.RequestSerializer(data=request.data)
        validate_serializer(serializer=request_serializer)
        user = create_user(**request_serializer.validated_data)
        send_verify_email(user)
        response_serializer = self.ResponseSerializer(user)
        return Response({
            'user': response_serializer.data
        }, status=status.HTTP_201_CREATED)


class UserVerification(APIView):
    permission_classes = [AllowAny, ]

    class RequestSerializer(serializers.Serializer):
        email_token = serializers.CharField(required=True, max_length=settings.CHARFIELD_LENGTH)

    class ResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ['id', 'is_active']

    def post(self, request):
        request_serializer = self.RequestSerializer(data=request.data)
        validate_serializer(serializer=request_serializer)
        user = verify_email(**request_serializer.validated_data)
        response_serializer = self.ResponseSerializer(user)
        return Response({
            'user': response_serializer.data
        }, status=status.HTTP_200_OK)


class UserDetailApi(APIView):
    permission_classes = [UserPermission, ]

    class ResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ['id', 'name', 'email', 'tel', 'created_at', 'updated_at']

    def get(self, request, user_id):
        user = get_user_by(id=user_id)
        self.check_object_permissions(request, obj=user)
        serializer = self.ResponseSerializer(user)
        return Response({
            'user': serializer.data
        }, status=status.HTTP_200_OK)


class UserUpdateApi(APIView):
    permission_classes = [UserPermission, ]

    class RequestSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=255)
        tel = serializers.CharField(max_length=255)

    class ResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ['id', 'name', 'email', 'tel', 'created_at', 'updated_at']

    def put(self, request, user_id):
        request_serializer = self.RequestSerializer(data=request.data)
        validate_serializer(serializer=request_serializer)
        user = get_user_by(id=user_id)
        self.check_object_permissions(request=request, obj=user)
        user = update_user(user=user, **request_serializer.validated_data)
        response_serializer = self.ResponseSerializer(user)
        return Response({
            'user': response_serializer.data
        }, status=status.HTTP_200_OK)


class UserChangePasswordApi(APIView):
    permission_classes = [UserPermission, ]

    class RequestSerializer(serializers.Serializer):
        old_password = serializers.CharField(required=True, max_length=settings.CHARFIELD_LENGTH)
        password = serializers.CharField(required=True, max_length=settings.CHARFIELD_LENGTH)
        password_confirm = serializers.CharField(required=True, max_length=settings.CHARFIELD_LENGTH)

    class ResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ['id', 'name', 'email', 'tel', 'created_at', 'updated_at']

    def put(self, request, user_id):
        request_serializer = self.RequestSerializer(data=request.data)
        validate_serializer(serializer=request_serializer)
        user = get_user_by(id=user_id)
        self.check_object_permissions(request=request, obj=user)
        user = change_password(user=user, **request_serializer.validated_data)
        response_serializer = self.ResponseSerializer(user)
        return Response({
            'user': response_serializer.data
        }, status=status.HTTP_200_OK)


class UserRequestResetPasswordApi(APIView):
    permission_classes = [AllowAny, ]

    class RequestSerializer(serializers.Serializer):
        email = serializers.EmailField(required=True, max_length=settings.CHARFIELD_LENGTH)

    def post(self, request):
        serializer = self.RequestSerializer(data=request.data)
        validate_serializer(serializer=serializer)
        user = gen_reset_password_token(**serializer.validated_data)
        send_reset_password_token(user=user)
        return Response({

        }, status=status.HTTP_200_OK)


class UserResetPasswordApi(APIView):
    permission_classes = [AllowAny, ]

    class RequestSerializer(serializers.Serializer):
        reset_password_token = serializers.CharField(required=True, max_length=settings.CHARFIELD_LENGTH)
        password = serializers.CharField(required=True, max_length=settings.CHARFIELD_LENGTH)
        password_confirm = serializers.CharField(required=True, max_length=settings.CHARFIELD_LENGTH)

    class ResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ['id', 'name', 'email', 'tel', 'created_at', 'updated_at']

    def put(self, request):
        request_serializer = self.RequestSerializer(data=request.data)
        validate_serializer(serializer=request_serializer)
        user = reset_password(**request_serializer.validated_data)
        response_serializer = self.ResponseSerializer(user)
        return Response({
            'user': response_serializer.data
        }, status=status.HTTP_200_OK)


class UserDeactivateApi(APIView):
    permission_classes = [UserPermission, ]

    class ResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ['id', 'name', 'email', 'tel', 'created_at', 'updated_at']

    def delete(self, request, user_id):
        user = get_user_by(id=user_id)
        self.check_object_permissions(request=request, obj=user)
        deactivate_user(user)
        response_serializer = self.ResponseSerializer(user)
        return Response({
            'user': response_serializer.data
        }, status=status.HTTP_200_OK)
