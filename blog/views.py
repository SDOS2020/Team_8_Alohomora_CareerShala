from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import Model
from django.shortcuts import render

# Create your views here.
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ParseError, NotFound
from rest_framework.request import Request
from rest_framework.response import Response

from blog.models import Post
import users.permissions as user_permissions
from blog.paginations import CustomPageNumberPagination
from blog.serializers import PostSerializer, PostMiniSerializer
from errors.views import error
from questionnaire.models import QuestionnaireResponse, Option
import tagulous.models

from tag.models import Tag
from users.decorators import user_verification_required, profile_completion_required
from users.models import CustomUser


@api_view(['GET', ])
@permission_classes([permissions.IsAuthenticated, user_permissions.EmailVerified, user_permissions.ProfileCompleted])
def view_all_posts(request):
    query_set = Post.objects.all()
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


@api_view(['GET', ])
@permission_classes([permissions.IsAuthenticated, user_permissions.IsStudent, user_permissions.EmailVerified,
                     user_permissions.ProfileCompleted])
def view_tagged_posts(request: Request):
    query_set = Post.objects.filter(
        tags__options__option_responses__questionnaire_response__student_profile=request.user.student_profile)
    paginator = CustomPageNumberPagination()
    result_set = paginator.paginate_queryset(query_set, request)
    serializer = PostMiniSerializer(result_set, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
