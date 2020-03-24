from django.urls import path
from .views import sign_in, sign_up, profiles, verify_email, change_password

urlpatterns = [
    path('api/users/sign_in', sign_in),
    path('api/users/sign_up', sign_up),
    path('api/users', profiles),
    path('api/users/verify_email', verify_email),
    path('api/users/change_password', change_password)
]
