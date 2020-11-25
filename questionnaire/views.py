from django.shortcuts import render

# Create your views here.
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from questionnaire.permissions import IsStudent
from questionnaire.serializers import QuestionnaireSerializer
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
