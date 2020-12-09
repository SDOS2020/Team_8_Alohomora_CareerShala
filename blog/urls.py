from django.urls import path, include
from . import views

urlpatterns = [
    path('posts/', views.all_posts, name='blog-posts'),
    path('post/<slug:slug>', views.view_post, name='blog-post'),
]
