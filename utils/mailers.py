from django.template.loader import render_to_string
from django.conf import settings
from sendgrid.helpers.mail import Mail
from sendgrid import SendGridAPIClient


def send_verify_email(user):
    email_template = render_to_string('send_verify_email.html', context={'user': user, 'site_name': settings.APP_NAME,
                                                                         'token': user.verify_email_token})
    message = Mail(from_email=settings.DEFAULT_FROM_EMAIL, to_emails=user.email, subject='Verify email',
                   html_content=email_template)
    sender = SendGridAPIClient(settings.SENDGRID_API_KEY)
    sender.send(message=message)


def send_reset_password_token(user):
    email_template = render_to_string('send_reset_pwd_token.html',
                                      context={'user': user, 'site_name': settings.APP_NAME,
                                               'token': user.reset_password_token})
    message = Mail(from_email=settings.DEFAULT_FROM_EMAIL, to_emails=user.email, subject='Reset password',
                   html_content=email_template)
    sender = SendGridAPIClient(settings.SENDGRID_API_KEY)
    sender.send(message=message)
