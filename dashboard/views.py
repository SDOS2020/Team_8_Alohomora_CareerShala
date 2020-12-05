from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from users.decorators import user_verification_required, profile_completion_required


@login_required
@user_verification_required
@profile_completion_required
def home(request):
    if not request.user.is_expert:
        return render(request, 'dashboard/home_student.html')
    else:
        return render(request, 'dashboard/home_expert.html')


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
