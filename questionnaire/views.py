import logging

from django.shortcuts import render

# Create your views here.
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from questionnaire.models import QuestionnaireResponse, Questionnaire
from questionnaire.permissions import IsStudent
from questionnaire.serializers import QuestionnaireSerializer, QuestionnaireResponseSerializer
from users.models import CustomUser, StudentProfile


@api_view(['GET', ])
@permission_classes([permissions.IsAuthenticated, IsStudent])
def next_questionnaire(request):
    """
    Returns the next questionnaire that needs to be answered by the requested student.
    :param request:
    :return:
    """

    user: CustomUser = request.user
    questionnaire = user.student_profile.next_questionnaire
    serializer = QuestionnaireSerializer(questionnaire)
    logger = logging.getLogger('app.questionnaire.next_questionnaire')
    logger.info(f'{request.user} has requested the next questionnaire ({questionnaire.identifier})')
    return Response(serializer.data)


@api_view(['POST', ])
@permission_classes([permissions.IsAuthenticated, IsStudent])
def submit_questionnaire_response(request):
    # why I need to send request in context explicitly? Because it is sent automatically in some
    # other class based view: https://stackoverflow.com/a/33550228/5394180
    serializer = QuestionnaireResponseSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        questionnaire_response: QuestionnaireResponse = serializer.save()
        answers_queryset = questionnaire_response.answers.filter(option__continuation_questionnaire__isnull=False)
        if answers_queryset.exists():
            last_answer = answers_queryset.first()
            request.user.student_profile.next_questionnaire = last_answer.option.continuation_questionnaire
        else:
            request.user.student_profile.next_questionnaire = None
        request.user.student_profile.save()
        logger = logging.getLogger('app.questionnaire.submit_questionnaire_response')
        logger.info(
            f'{request.user} has submitted responses to questionnaire: {questionnaire_response.questionnaire.identifier}')
        if questionnaire_response:
            return Response(status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', ])
@permission_classes([permissions.IsAuthenticated, IsStudent])
def reset_questionnaire_responses(request):
    student_profile: StudentProfile = request.user.student_profile
    student_profile.student_profile_responses.all().delete()
    student_profile.next_questionnaire = Questionnaire.objects.get(root=True)
    student_profile.save()
    logger = logging.getLogger('app.questionnaire.reset_questionnaire_response')
    logger.info(f'{request.user} has reset their responses')
    return Response(status=status.HTTP_200_OK)
