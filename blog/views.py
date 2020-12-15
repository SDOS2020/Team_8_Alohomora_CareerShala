from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import Model, Q
from django.shortcuts import render

# Create your views here.
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ParseError, NotFound
from rest_framework.request import Request
from rest_framework.response import Response

from blog.forms import PostCreationForm
from blog.models import Post
import users.permissions as user_permissions
from blog.paginations import CustomPageNumberPagination
from blog.serializers import PostSerializer, PostMiniSerializer
from blog.validators import validate_post_type
from errors.views import error
from questionnaire.models import QuestionnaireResponse, Option
import tagulous.models

from tag.models import Tag
from users.decorators import user_verification_required, profile_completion_required, expert_only
from users.models import CustomUser


@api_view(['GET', ])
@permission_classes([permissions.IsAuthenticated, user_permissions.EmailVerified, user_permissions.ProfileCompleted])
def view_all_posts_api_endpoint(request: Request):
    post_type = request.query_params.get("post_type", None)

    if post_type is not None:
        try:
            validate_post_type(post_type)
        except ValidationError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        query_set = Post.objects.filter(type=post_type)
    else:
        query_set = Post.objects.all()

    paginator = CustomPageNumberPagination()
    result_set = paginator.paginate_queryset(query_set, request)
    serializer = PostMiniSerializer(result_set, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes([permissions.IsAuthenticated, user_permissions.IsStudent, user_permissions.EmailVerified,
                     user_permissions.ProfileCompleted])
def view_tagged_posts(request: Request):
    post_type = request.query_params.get("post_type", None)
    if post_type is not None:
        try:
            validate_post_type(post_type)
        except ValidationError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        query_set = Post.objects.filter(
            Q(tags__options__option_responses__questionnaire_response__student_profile=request.user.student_profile) &
            Q(type=post_type))
    else:
        query_set = Post.objects.filter(
            tags__options__option_responses__questionnaire_response__student_profile=request.user.student_profile)

    paginator = CustomPageNumberPagination()
    result_set = paginator.paginate_queryset(query_set, request)
    serializer = PostMiniSerializer(result_set, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@login_required
@user_verification_required
@profile_completion_required
def view_post(request, slug):
    try:
        post = Post.objects.get(slug=slug)
        return render(request, 'blog/post.html', {'post': post})
    except ObjectDoesNotExist:
        return error(request, error_dict={'title': "Requested post doesn't exist", 'body': ""})


@login_required
@user_verification_required
@profile_completion_required
def view_all_posts(request):
    post_type = request.GET.get('post_type', None)
    try:
        validate_post_type(post_type)
    except ValidationError:
        return error(request, error_dict={'title': 'Bad Request', 'body': ''})
    return render(request, 'blog/posts.html', context={'post_type': post_type})


@login_required
@user_verification_required
@profile_completion_required
@expert_only
def add_post(request):
    if request.method == 'POST':
        form = PostCreationForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            messages.success(request, 'Post has been added successfully!')
            form = PostCreationForm()
    else:
        post_type = request.GET.get('post_type', None)
        try:
            validate_post_type(post_type)
        except ValidationError:
            return error(request, error_dict={'title': 'Bad Request', 'body': ''})
        form = PostCreationForm(initial={'type': post_type})
    return render(request, 'blog/add_post.html', context={'form': form})
