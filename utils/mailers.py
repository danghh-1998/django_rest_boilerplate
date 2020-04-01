from django.template.loader import render_to_string
from django.conf import settings
from sendgrid.helpers.mail import Mail
from sendgrid import SendGridAPIClient


def send_init_pwd(user, password):
    email_template = render_to_string('send_init_pwd.html',
                                      context={'user': user, 'site_name': settings.APP_NAME, 'password': password})
    message = Mail(from_email=settings.DEFAULT_FROM_EMAIL, to_emails=user.email, subject='Verify email',
                   html_content=email_template)
    sender = SendGridAPIClient(settings.SENDGRID_API_KEY)
    sender.send(message=message)
