from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from blog.models import Post
from users.decorators import user_verification_required, profile_completion_required


@login_required
@user_verification_required
@profile_completion_required
def all_posts(request):
    posts = Post.objects.all()
    return render(request, 'blog/posts.html', {'posts': posts})


@login_required
@user_verification_required
@profile_completion_required
def view_post(request, slug):
    post = Post.objects.get(slug=slug)
    return render(request, 'blog/post.html', {'post': post})
