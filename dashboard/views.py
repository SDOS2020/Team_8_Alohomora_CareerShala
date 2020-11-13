from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from users.decorators import user_verification_required, profile_completion_required


@login_required
@user_verification_required
@profile_completion_required
def home(request):
    return render(request, 'dashboard/home.html')
