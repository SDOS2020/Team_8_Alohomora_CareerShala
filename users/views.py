from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.

def register(request):
    a = "Reeshabh"
    context1 = {'variable' : a}
    return render(request, 'registration/signup.html', context=context1)
