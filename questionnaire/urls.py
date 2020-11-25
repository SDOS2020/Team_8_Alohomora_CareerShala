from django.urls import path, include
from . import views

urlpatterns = [
    path('next_questionnaire/', views.next_questionnaire, name='api-questionnaire-next-questionnaire'),
]
