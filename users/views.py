import logging

from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login as builtin_login, logout as builtin_logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.http import is_safe_url
from rest_framework import status

from errors.views import error
from users.decorators import user_verification_required
from users.forms import CustomUserCreationForm, LoginForm, ExpertProfileForm, StudentProfileForm
from users.models import CustomUser


@login_required
@user_verification_required
def profile(request):
    if request.method == 'POST':
        if request.user.is_expert:
            profile_form = ExpertProfileForm(request.POST, instance=request.user.expert_profile)
        else:
            profile_form = StudentProfileForm(request.POST, instance=request.user.student_profile)
        if profile_form.is_valid():
            profile_form.save()
            first_time = not request.user.profile_completed
            if first_time:
                logger = logging.getLogger('app.accounts.profile')
                logger.info(f'{request.user} has completed their profile.')
            request.user.profile_completed = True
            request.user.save()
            success_message = "Profile successfully updated!"
            if request.user.is_expert and not request.user.expert_profile.verified:
                success_message += " Please wait for expert-profile verification by admin."
            messages.success(request, success_message)
            if first_time and not request.user.is_expert:
                return redirect('dashboard-home')
    else:
        if request.user.is_expert:
            profile_form = ExpertProfileForm(instance=request.user.expert_profile)
        else:
            profile_form = StudentProfileForm(instance=request.user.student_profile)
    return render(request, 'users/profile.html', {'form': profile_form})


def register(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in. Logout to register another user.')
        return redirect('dashboard-home')
    if request.method == 'POST':

        user_creation_form_filled = CustomUserCreationForm(request.POST)
        if user_creation_form_filled.is_valid():
            user_creation_form_filled.save()
            messages.success(request, "Registration successful, check your email inbox to verify your email.")
            return render(request, 'registration/signup.html', context={'form': CustomUserCreationForm()},
                          status=status.HTTP_201_CREATED)
        else:
            return render(request, 'registration/signup.html',
                          {'form': user_creation_form_filled},
                          status=status.HTTP_422_UNPROCESSABLE_ENTITY)  # should contain errors
    else:
        user_creation_form_empty = CustomUserCreationForm()
        return render(request, 'registration/signup.html', {'form': user_creation_form_empty})


def login(request):
    if request.user.is_authenticated:
        return redirect('dashboard-home')
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
            if not user.verified:
                messages.error(request, "Please verify your email first")
            else:
                builtin_login(request, user)
                logger = logging.getLogger('app.accounts.login')
                logger.info(f'{user} has logged into the site')
                return redirect(success_redirect_url)
        return render(request, 'users/login.html', {'form': login_form_filled})

    else:
        login_form_empty = LoginForm()
        return render(request, 'users/login.html', {'form': login_form_empty})


@login_required
def logout(request):
    request_user = str(request.user)
    builtin_logout(request)
    logger = logging.getLogger('app.accounts.logout')
    logger.info(f'{request_user} has logged out from the site')
    return redirect('homepage')


def verify(request):
    if request.method == 'GET':
        message = ""
        if request.user.is_authenticated:
            message = "You cannot verify an account when you are logged in."
            messages.error(request, message)
        else:
            try:
                email = request.GET.get("email")
                email_verification_token = request.GET.get("email_verification_token")
                user: CustomUser = get_object_or_404(get_user_model(), email=email)
                if user.verified:
                    message = "Your account is already verified!"
                    messages.warning(request, message)
                else:
                    if email_verification_token == user.email_verification_token:
                        user.verified = True
                        user.save()
                        message = "Your account has been verified, proceed to login."
                        logger = logging.getLogger('app.accounts.verification')
                        logger.info(f'{user} has verified their email')
                        messages.success(request, message)
                    else:
                        message = "Email verification failed."
                        messages.error(request, message)
            except KeyError as e:
                return HttpResponseBadRequest()  # TODO pretty print
        return redirect('users-login')
    else:
        return HttpResponseBadRequest()
