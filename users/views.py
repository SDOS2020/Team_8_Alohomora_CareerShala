from django.contrib.auth import get_user_model
from django.http import HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404

from users.methods import registration_basic
from users.models import CustomUser


def register_student(request):
    registration_basic(request, is_expert=False)


def register_expert(request):
    registration_basic(request, is_expert=True)


def login(request):
    return render(request, 'users/login.html')


def verify(request):
    if request.method == 'GET':
        message = ""
        if request.user.is_authenticated:
            message = "You cannot verify an account when you are logged in."
        else:
            try:
                email = request.GET.get("email")
                email_verification_token = request.GET.get("email_verification_token")
                user: CustomUser = get_object_or_404(get_user_model(), email=email)
                if user.verified:
                    message = "Your account is already verified!"
                else:
                    if email_verification_token == user.email_verification_token:
                        user.verified = True
                        user.save()
                        message = "Your account has been verified, proceed to login."
                    else:
                        message = "Email verification failed."
            except KeyError as e:
                return HttpResponseBadRequest()
        context = {
            'message': message
        }
        return render(request, 'users/verify.html', context=context)
    else:
        return HttpResponseBadRequest()
