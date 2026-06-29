from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

def send_email_template(subject, template, context, recipient_list):
    message = render_to_string(template, context)

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        recipient_list,
        fail_silently=False
    )