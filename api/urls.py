from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('questionnaire/', include('questionnaire.urls')),
    path('blog/', include('blog.urls')),
]
