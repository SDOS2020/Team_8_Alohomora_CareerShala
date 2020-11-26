from django.urls import path, include
from . import views

urlpatterns = [
    path('next_questionnaire/', views.next_questionnaire, name='api-questionnaire-next-questionnaire'),
    path('submit_questionnaire_response/', views.submit_questionnaire_response,
         name='api-questionnaire-submit-questionnaire-response'),
]
