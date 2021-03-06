from django.urls import path

from . import views

urlpatterns = [
    path('home/', views.home, name='dashboard-home'),
    path('opportunities/', views.opportunities, name='dashboard-opportunities'),  # TODO remove this
    path('courses/', views.courses, name='dashboard-courses'),
    path('admin/', views.home_admin, name='admin-dashboard'),
]
