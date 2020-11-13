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
        if request.user.is_expert and not request.user.expert_profile.verified:
            messages.warning(request, "Please wait for expert-profile verification by admin before accessing the "
                                      "platform.")
            return redirect('users-profile')
        return function(request, *args, **kwargs)

    return check
