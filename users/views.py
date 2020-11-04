from django.shortcuts import render


# Create your views here.

def register_student(request):
    return render(request, 'registration/signup.html')


def register_expert(request):
    return render(request, 'registration/signup.html')
