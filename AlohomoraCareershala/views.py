from django.conf import settings
from django.shortcuts import render

from errors.views import error


def homepage(request):
    return render(request, 'homepage/homepage.html')


def dummy(request):
    if settings.DEBUG:
        return render(request, 'dummy.html')
    else:
        return error(request, error_dict={'title': 'Bad Request', 'body': ''})
