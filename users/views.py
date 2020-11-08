from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login as builtin_login
from django.http import HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect

from users.forms import CustomUserCreationForm, LoginForm, ErrorForm
from users.models import CustomUser


def registration_basic(request, is_expert: bool):
    if request.method == 'POST':

        user_creation_form_filled = CustomUserCreationForm(request.POST)
        if user_creation_form_filled.is_valid():
            user_creation_form_filled.save()
            messages.success(request, "Registration successful, check your email inbox to verify your email.")
            if is_expert:
                return redirect('users-register-expert')
            else:
                return redirect('users-register-student')
        else:
            return render(request, 'registration/signup.html',
                          {'form': user_creation_form_filled, 'is_expert': is_expert})  # should contain errors
    else:
        user_creation_form_empty = CustomUserCreationForm()
        return render(request, 'registration/signup.html', {'form': user_creation_form_empty, 'is_expert': is_expert})


def register_student(request):
    return registration_basic(request, is_expert=False)


def register_expert(request):
    return registration_basic(request, is_expert=True)


def login(request):
    if request.method == 'POST':
        login_form_filled = LoginForm(request.POST)
        if login_form_filled.is_valid():
            email = login_form_filled.cleaned_data["email"]
            password = login_form_filled.cleaned_data["password"]
            user: CustomUser = authenticate(request, email=email, password=password)
            if user is not None:
                if user.is_expert:
                    if user.expert_profile.verified:
                        builtin_login(request, user)
                        # TODO redirect to expert's dashboard
                    else:
                        return error(request,
                                     error_dict={'title': "Profile verification pending by admin.",
                                                 'body': "Contact us to know more."})
                else:
                    builtin_login(request, user)
                    # TODO redirect to student's dashboard
            else:
                return render(request, 'users/login.html', {'form': login_form_filled})
        else:
            return error(request,
                         error_dict={'title': "Bad request"})

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
