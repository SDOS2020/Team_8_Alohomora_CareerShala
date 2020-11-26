from django.shortcuts import render

# Create your views here.
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from questionnaire.models import QuestionnaireResponse
from questionnaire.permissions import IsStudent
from questionnaire.serializers import QuestionnaireSerializer, QuestionnaireResponseSerializer
from users.models import CustomUser


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
    return Response(serializer.data)


@api_view(['POST', ])
@permission_classes([permissions.IsAuthenticated, IsStudent])
def submit_questionnaire_response(request):
    serializer = QuestionnaireResponseSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        questionnaire_response = serializer.save()
        if questionnaire_response:
            return Response(status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', ])
# @permission_classes([])
# def get_questionnaire_response(request):
#     questionnaire_response = QuestionnaireResponse.objects.get()
#     serializer = QuestionnaireResponseSerializer(questionnaire_response)
#     return Response(serializer.data)
