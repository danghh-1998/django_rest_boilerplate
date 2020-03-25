from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK
from rest_framework.response import Response

from .serializers import *
from .authentication import get_token
from .permissions import UserPermission


@api_view(('POST',))
@permission_classes((AllowAny,))
def sign_in(request):
    sign_in_serializer = SigninSerializer(data=request.data)
    if not sign_in_serializer.is_valid():
        return Response(sign_in_serializer.errors, status=HTTP_400_BAD_REQUEST)
    token = sign_in_serializer.authenticate()
    if not token:
        return Response({
            'detail': 'Unauthenticated'
        }, status=HTTP_400_BAD_REQUEST)
    return Response({
        'token': token.key
    }, status=HTTP_200_OK)


@api_view(('POST',))
@permission_classes((AllowAny,))
def sign_up(request):
    sign_up_serializer = SignupSerializer(data=request.data)
    if not sign_up_serializer.is_valid():
        return Response(sign_up_serializer.errors, status=HTTP_400_BAD_REQUEST)
    sign_up_serializer.create(validated_data=request.data)
    return Response({
        'detail': 'Sign up successfully'
    }, status=HTTP_200_OK)


@api_view(('GET', 'PUT', 'DELETE'))
@permission_classes((UserPermission,))
def profiles(request):
    user = request.user
    if request.method == 'GET':
        user_serialized = UserSerializer(user)
        token = get_token(user)
        return Response({
            'user': user_serialized.data,
            'token': token.key
        }, status=HTTP_200_OK)
    elif request.method == 'PUT':
        update_profile_serializer = UpdateProfileSerializer(data=request.data)
        if not update_profile_serializer.is_valid():
            return Response(update_profile_serializer.errors, status=HTTP_400_BAD_REQUEST)
        user = update_profile_serializer.update(instance=request.user, validated_data=request.data)
        user_serialized = UserSerializer(user)
        return Response({
            'user': user_serialized.data
        }, status=HTTP_200_OK)
    elif request.method == 'DELETE':
        user_serializer = UserSerializer(user)
        user_serializer.deactivate_user()
        return Response({
            'detail': 'Deactivate user successfully'
        }, status=HTTP_200_OK)


@api_view(('POST',))
@permission_classes((AllowAny,))
def verify_email(request):
    verify_email_serializer = VerifyEmailSerializer(data=request.data)
    if not verify_email_serializer.is_valid():
        return Response(verify_email_serializer.errors, status=HTTP_400_BAD_REQUEST)
    verify_email_serializer.active_user()
    return Response({
        'detail': 'Active user successfully'
    }, status=HTTP_200_OK)


@api_view(('POST',))
@permission_classes((UserPermission,))
def change_password(request):
    change_password_serializer = ChangePasswordSerializer(data=request.data, context=request.user)
    if not change_password_serializer.is_valid():
        return Response(change_password_serializer.errors, status=HTTP_400_BAD_REQUEST)
    change_password_serializer.change_password()
    return Response({
        'detail': 'Change password successfully'
    }, status=HTTP_200_OK)
