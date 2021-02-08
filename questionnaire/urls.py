from django.urls import path, include
from . import views

urlpatterns = [
    path('next_questionnaire/', views.next_questionnaire, name='api-questionnaire-next-questionnaire'),
    path('submit_questionnaire_response/', views.submit_questionnaire_response,
         name='api-questionnaire-submit-questionnaire-response'),
    path('reset_questionnaire_responses/', views.reset_questionnaire_responses,
         name='api-questionnaire-reset-questionnaire-responses'),
    path('get_all_questionnaires/', views.get_all_questionnaires,
         name='api-questionnaire-get-all-questionnaires'),
]
