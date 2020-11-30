from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.register, name='users-register'),
    path('login/', views.login, name='users-login'),
    path('verify/', views.verify, name='users-verify'),
    path('profile/', views.profile, name='users-profile'),
    path('logout/', views.logout, name='users-logout'),
]
