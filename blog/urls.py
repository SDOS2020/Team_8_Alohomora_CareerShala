from django.urls import path, include
from . import views

urlpatterns = [
    path('posts_api/', views.view_all_posts_api_endpoint, name='api-blog-posts'),
    path('post/<slug:slug>', views.view_post, name='blog-post'),
    path('tagged_posts/', views.view_tagged_posts, name='api-blog-tagged-posts'),
    path('add_post/', views.add_post, name='blog-add-post'),
    path('posts/', views.view_all_posts, name='blog-posts'),
]
