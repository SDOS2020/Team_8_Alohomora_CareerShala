from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import Model, Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ParseError, NotFound
from rest_framework.request import Request
from rest_framework.response import Response

from blog.forms import PostCreationForm, SubmissionForm
from blog.models import Post, Submission
import users.permissions as user_permissions
from blog.paginations import CustomPageNumberPagination
from blog.serializers import PostSerializer, PostMiniSerializer
from blog.validators import validate_post_type
from errors.views import error
from questionnaire.models import QuestionnaireResponse, Option
import tagulous.models

from tag.models import Tag
from users.decorators import user_verification_required, profile_completion_required, expert_only, student_only
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
        context = {'post': post}
        if not request.user.is_expert:
            if Submission.objects.filter(student_profile=request.user.student_profile, post=post).exists():
                last_uploaded_url = Submission.objects.get(student_profile=request.user.student_profile, post=post).uploaded_file.url
                context['last_uploaded_url'] = last_uploaded_url
        return render(request, 'blog/post.html', context=context)
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
        return error(request, error_dict={'title': 'Bad Request', 'body': ''})  # TODO replace with error 404
    post_type = int(post_type)
    post_category = ""
    for allowed_posts in Post.POST_TYPE:
        if post_type == allowed_posts[0]:
            post_category = f'{allowed_posts[1]}s'
            break
    return render(request, 'blog/posts.html', context={'post_type': post_type, 'post_category': post_category})


@login_required
@user_verification_required
@profile_completion_required
@expert_only
def add_post(request):
    status_code = status.HTTP_200_OK
    if request.method == 'POST':
        form = PostCreationForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            messages.success(request, 'Post has been added successfully!')
            form = PostCreationForm()
            status_code = status.HTTP_201_CREATED
        else:
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    else:
        post_type = request.GET.get('post_type', None)
        try:
            validate_post_type(post_type)
        except ValidationError:
            return error(request, error_dict={'title': 'Bad Request', 'body': ''})
        form = PostCreationForm(initial={'type': post_type})
    return render(request, 'blog/add_post.html', context={'form': form}, status=status_code)


@login_required
@user_verification_required
@profile_completion_required
@student_only
def upload_submission(request):
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            post = Post.objects.get(identifier=form.cleaned_data.get('post_identifier'))
            if Submission.objects.filter(student_profile=request.user.student_profile, post=post).exists():
                form = SubmissionForm(request.POST, request.FILES, instance=Submission.objects.get(student_profile=request.user.student_profile, post=post))
                messages.success(request, 'Submission updated')
            else:
                submission = form.save(commit=False)
                submission.student_profile = request.user.student_profile
                submission.post = post
                messages.success(request, 'Submission uploaded')
            submission = form.save()
            return HttpResponseRedirect(reverse('blog-post',  # TODO check if this is standard practice or not
                                                kwargs={
                                                    'slug': submission.post.slug
                                                }))
        else:
            messages.error(request, 'Cannot submit, please try again later.')
            return redirect('dashboard-home')  # TODO redirect to the same page
