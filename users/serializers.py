from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import authenticate

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from .models import GENDER, User
from .authentication import expire_token, authenticate_user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'gender', 'is_superuser', 'is_active', 'created_at')

    def deactivate_user(self):
        user = self.instance
        user.is_active = False
        expire_token(user)
        user.save(update_fields=['is_active'])


class SigninSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=255)
    password = serializers.CharField(required=True, max_length=255)

    def authenticate(self):
        user, token = authenticate_user(**self.data)
        return token


class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=255)
    name = serializers.CharField(required=True, max_length=255)
    gender = serializers.ChoiceField(choices=GENDER)
    password = serializers.CharField(max_length=255, required=True)
    password_confirmation = serializers.CharField(max_length=255, required=True)

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirmation']:
            raise ValidationError('Password and password confirmation don\'t match')
        return attrs

    def create(self, validated_data):
        data = validated_data.copy()
        data.pop('password_confirmation')
        user = User.objects.create_user(**data.dict())
        self.send_email(user)
        return user

    def send_email(self, user):
        email_template = render_to_string('verify_email.html', context={'user': user, 'site_name': settings.APP_NAME})
        message = Mail(from_email=settings.DEFAULT_FROM_EMAIL, to_emails=user.email, subject='Verify email',
                       html_content=email_template)
        sender = SendGridAPIClient(settings.SENDGRID_API_KEY)
        sender.send(message=message)


class UpdateProfileSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False, max_length=255)
    name = serializers.CharField(required=False, max_length=255)
    gender = serializers.ChoiceField(choices=GENDER)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.name = validated_data.get('name', instance.name)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.save(update_fields=['email', 'name', 'gender'])
        return instance


class VerifyEmailSerializer(serializers.Serializer):
    token = serializers.CharField(required=True, max_length=40)

    def get_user(self, token):
        return User.objects.filter(verify_email_token__exact=token).first()

    def validate(self, attrs):
        user = self.get_user(attrs['token'])
        if not user:
            raise ValidationError('Invalid token')
        elif user.verify_email_token_expired_at < timezone.now():
            raise ValidationError('Token expired')
        return attrs

    def active_user(self):
        user = self.get_user(self.data['token'])
        user.is_active = True
        user.save(update_fields=['is_active'])


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, max_length=255)
    password = serializers.CharField(required=True, max_length=255)
    password_confirmation = serializers.CharField(required=True, max_length=255)

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirmation']:
            raise ValidationError('Password and password confirmation don\'t match')
        user = authenticate(email=self.context.email, password=attrs['old_password'])
        if not user:
            raise ValidationError('Unauthenticated')
        return attrs

    def change_password(self):
        user = self.context
        user.set_password(self.data.get('password'))
        user.save(update_fields=['password'])
        return user
