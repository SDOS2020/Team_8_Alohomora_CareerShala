import threading

from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render
from django.utils.crypto import get_random_string

from users.forms import CustomUserCreationForm


def generate_token():
    return get_random_string(length=32)


def send_mail_async(sender: str, receivers, subject, body):
    t = threading.Thread(target=send_mail, kwargs={
        'subject': subject,
        'message': body,
        'from_email': sender,
        'recipient_list': receivers
    })
    t.setDaemon(True)
    t.start()  # TODO log this


def registration_basic(request, is_expert: bool):
    if request.method == 'POST':
        user_creation_form_filled = CustomUserCreationForm(request.POST)
        if user_creation_form_filled.is_valid():
            user_creation_form_filled.save()
            messages.success(request, "Registration successful, check your email inbox to verify your email.")
            # I am not refreshing upon success, just showing a message.
        else:
            return render(request, 'registration/signup.html',
                          {'form': user_creation_form_filled, 'is_expert': False})  # should contain errors
    else:
        user_creation_form_empty = CustomUserCreationForm()
        return render(request, 'registration/signup.html', {'form': user_creation_form_empty, 'is_expert': False})
