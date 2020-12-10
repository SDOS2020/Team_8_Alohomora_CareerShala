from django.urls import path, include
from . import views

urlpatterns = [
    path('posts/', views.view_all_posts, name='blog-posts'),
    path('post/', views.view_post, name='blog-post'),
]
