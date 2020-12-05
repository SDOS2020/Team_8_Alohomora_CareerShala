import logging
import threading

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render
from django.utils.crypto import get_random_string

# from users.forms import CustomUserCreationForm  # do not import this! https://stackoverflow.com/a/16975976/5394180
from sendgrid import Mail, SendGridAPIClient


def generate_token():
    return get_random_string(length=32)


def send_mail_async(sender: str, receivers, subject, dynamic_template_data: dict, template_id):
    message = Mail(
        from_email=sender,
        to_emails=receivers,
        subject=subject,
    )
    message.dynamic_template_data = dynamic_template_data
    message.template_id = template_id
    sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
    t = threading.Thread(target=sg.send, args=(message,), name=f'email to {receivers}')
    t.setDaemon(True)
    t.start()
