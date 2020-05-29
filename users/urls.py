from django.urls import path
from .apis import UserSignInApi, UserDetailApi, UserSignUpApi, UserChangePasswordApi, UserRequestResetPasswordApi, \
    UserResetPasswordApi, UserUpdateApi, UserDeactivateApi, UserVerification

urlpatterns = [
    path('sign_in', UserSignInApi.as_view(), name='sign_in'),
    path('sign_up', UserSignUpApi.as_view(), name='sign_up'),
    path('<int:user_id>', UserDetailApi.as_view(), name='user_detail'),
    path('<int:user_id>/update', UserUpdateApi.as_view(), name='user_update'),
    path('<int:user_id>/deactivate', UserDeactivateApi.as_view(), name='user_deactivate'),
    path('<int:user_id>/change_password', UserChangePasswordApi.as_view(), name='user_change_password'),
    path('req_reset_password', UserRequestResetPasswordApi.as_view(), name='user_req_reset_password'),
    path('reset_password', UserResetPasswordApi.as_view(), name='user_reset_password'),
    path('verify_email', UserVerification.as_view(), name='user_verify_email'),
]
