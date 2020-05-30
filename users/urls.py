from django.urls import path
from .apis import SignInApi, UserDetailApi, UserUpdateApi, UserDeactivateApi, \
    UserChangePasswordApi, UserRequestResetPasswordApi, UserResetPassword

urlpatterns = [
    path('auth/sign_in', SignInApi.as_view(), name='sign_in'),
    path('users/<int:user_id>', UserDetailApi.as_view(), name='user_detail'),
    path('users/<int:user_id>/update', UserUpdateApi.as_view(), name='user_update'),
    path('users/<int:user_id>/deactivate', UserDeactivateApi.as_view(), name='user_deactivate'),
    path('users/<int:user_id>/change_password', UserChangePasswordApi.as_view(), name='user_change_password'),
    path('users/req_reset_password', UserRequestResetPasswordApi.as_view(), name='user_req_reset_password'),
    path('users/reset_password', UserResetPassword.as_view(), name='user_reset_password')
]
