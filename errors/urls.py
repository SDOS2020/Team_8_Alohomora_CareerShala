from django.urls import path

from . import views

urlpatterns = [
    path('error/', views.error, name='errors-error'),
]
