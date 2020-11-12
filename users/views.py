from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login as builtin_login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.http import is_safe_url

from users.forms import CustomUserCreationForm, LoginForm, ErrorForm
from users.models import CustomUser


@login_required
def profile(request):
    return render(request, 'users/profile.html')


def register(request):
    if request.method == 'POST':

        user_creation_form_filled = CustomUserCreationForm(request.POST)
        if user_creation_form_filled.is_valid():
            user_creation_form_filled.save()
            messages.success(request, "Registration successful, check your email inbox to verify your email.")
            return redirect('users-register')
        else:
            return render(request, 'registration/signup.html',
                          {'form': user_creation_form_filled})  # should contain errors
    else:
        user_creation_form_empty = CustomUserCreationForm()
        return render(request, 'registration/signup.html', {'form': user_creation_form_empty})


def login(request):
    if request.method == 'POST':
        login_form_filled = LoginForm(request.POST)
        if login_form_filled.is_valid():
            success_redirect_url = request.GET.get('next', 'dashboard-home')
            if not is_safe_url(url=success_redirect_url,
                               allowed_hosts=settings.ALLOWED_HOSTS):  # TODO what is this allowed_hosts?
                return error(request,
                             error_dict={'title': 'Invalid Request',
                                         'body': ''})
            email = login_form_filled.cleaned_data["email"]
            password = login_form_filled.cleaned_data["password"]
            user: CustomUser = authenticate(request, email=email,
                                            password=password)  # TODO duplicate in form validation
            if user.is_expert:
                if user.expert_profile.verified:
                    builtin_login(request, user)
                    return redirect(success_redirect_url)
                else:
                    return error(request,
                                 error_dict={'title': "Profile verification pending by admin.",
                                             'body': "Contact us to know more."})
            else:
                builtin_login(request, user)
                return redirect(success_redirect_url)
        else:
            return render(request, 'users/login.html', {'form': login_form_filled})

    else:
        login_form_empty = LoginForm()
        return render(request, 'users/login.html', {'form': login_form_empty})


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


def error(request, error_dict=None):  # TODO can we make it a POST redirect?
    if error_dict is None:
        error_dict = {}
    error_form = ErrorForm(error_dict)
    error_object = {}
    if error_form.is_valid():
        error_object['title'] = error_form.cleaned_data['title']
        error_object['body'] = error_form.cleaned_data['body']
    else:
        error_object['title'] = "Bad Request"
        error_object['body'] = ""
    return render(request, 'common/error.html', context={'error': error_object})
