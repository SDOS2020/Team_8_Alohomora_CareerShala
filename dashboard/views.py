from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from users.decorators import user_verification_required, profile_completion_required, admin_only


@login_required
@user_verification_required
@profile_completion_required
def home(request):
    if not request.user.is_expert:
        return render(request, 'dashboard/home_student.html')
    else:
        return render(request, 'dashboard/home_expert.html')


# TODO remove this
@login_required
@user_verification_required
@profile_completion_required
def opportunities(request):
    return render(request, 'dashboard/opportunities.html')


@login_required
@user_verification_required
@profile_completion_required
def courses(request):
    return render(request, 'dashboard/courses.html')


@login_required
@admin_only
def home_admin(request):
    return render(request, 'dashboard/home_admin.html')