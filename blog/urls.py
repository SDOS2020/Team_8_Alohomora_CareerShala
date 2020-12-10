from django.urls import path, include
from . import views

urlpatterns = [
    path('posts/', views.view_all_posts, name='api-blog-posts'),
    path('post/', views.view_post, name='api-blog-post'),
    path('tagged_posts/', views.view_tagged_posts, name='api-blog-tagged-posts'),
]
