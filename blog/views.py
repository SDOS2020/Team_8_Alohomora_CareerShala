from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, ValidationError
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
from users.models import CustomUser


@api_view(['GET', ])
@permission_classes([permissions.IsAuthenticated, user_permissions.EmailVerified, user_permissions.ProfileCompleted])
def view_all_posts(request):
    query_set = Post.objects.all()
    paginator = CustomPageNumberPagination()
    result_set = paginator.paginate_queryset(query_set, request)
    serializer = PostMiniSerializer(result_set, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes([permissions.IsAuthenticated, user_permissions.EmailVerified, user_permissions.ProfileCompleted])
def view_post(request: Request):
    if 'identifier' not in request.query_params:
        raise ParseError(detail='"identifier" parameter missing.')
    try:
        identifier = request.query_params.get('identifier')
        post = Post.objects.get(identifier=identifier)
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        raise NotFound(detail="Requested post doesn't exist.")
    except ValidationError:
        raise ParseError(detail="Invalid identifier passed.")
