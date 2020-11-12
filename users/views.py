from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login as builtin_login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.http import is_safe_url

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
            request.user.profile_completed = True
            request.user.save()
            success_message = "Profile successfully updated!"
            if request.user.is_expert:
                success_message += " Please wait for expert-profile verification by admin."
            messages.success(request, "Profile successfully updated!")
    else:
        if request.user.is_expert:
            profile_form = ExpertProfileForm(instance=request.user.expert_profile)
        else:
            profile_form = StudentProfileForm(instance=request.user.student_profile)
    return render(request, 'users/profile.html', {'form': profile_form})


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
                return error(request, error_dict={'title': 'Please verify your email first!',
                                                  'body': ''})

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
