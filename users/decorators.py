from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect

from errors.views import error


def user_verification_required(function):
    @wraps(function)
    def check(request, *args, **kwargs):
        if not request.user.verified:
            return error(request, error_dict={'title': "Please verify your email first.", 'body': ""})
        return function(request, *args, **kwargs)

    return check


def profile_completion_required(function):
    @wraps(function)
    def check(request, *args, **kwargs):
        if not request.user.profile_completed:
            messages.error(request, "Please fill out your profile first!")
            return redirect('users-profile')
        return function(request, *args, **kwargs)

    return check
