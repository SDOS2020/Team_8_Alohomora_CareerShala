from django.urls import path

from . import views

urlpatterns = [
    path('register_student/', views.register_student, name='users-register-student'),
    path('register_expert/', views.register_expert, name='users-register-student'),
]
