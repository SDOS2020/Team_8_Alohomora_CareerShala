import io
import logging

from django.db.models import Q, F, RestrictedError
from django.shortcuts import render

# Create your views here.
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from questionnaire.models import QuestionnaireResponse, Questionnaire, Question, Option
import users.permissions as user_permissions
from questionnaire.serializers import QuestionnaireSerializer, QuestionnaireResponseSerializer, \
    QuestionnaireSerializer, QuestionSerializer, OptionSerializer
from users.models import CustomUser, StudentProfile


@api_view(['GET', ])
@permission_classes([permissions.IsAuthenticated, user_permissions.IsStudent, user_permissions.EmailVerified,
                     user_permissions.ProfileCompleted])
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
    if questionnaire is not None:
        logger.info(f'{request.user} has requested the next questionnaire ({questionnaire.identifier})')
    return Response(serializer.data)


@api_view(['POST', ])
@permission_classes([permissions.IsAuthenticated, user_permissions.IsStudent, user_permissions.EmailVerified,
                     user_permissions.ProfileCompleted])
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
        if request.user.student_profile.next_questionnaire is None:
            logger.info(f'{request.user} has completed the questionnaire')
        if questionnaire_response:
            return Response(status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', ])
@permission_classes([permissions.IsAuthenticated, user_permissions.IsStudent, user_permissions.EmailVerified,
                     user_permissions.ProfileCompleted])
def reset_questionnaire_responses(request):
    student_profile: StudentProfile = request.user.student_profile
    student_profile.student_profile_responses.all().delete()
    student_profile.next_questionnaire = Questionnaire.objects.get(root=True)
    student_profile.save()
    logger = logging.getLogger('app.questionnaire.reset_questionnaire_response')
    logger.info(f'{request.user} has reset their responses')
    return Response(status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes([permissions.IsAuthenticated, user_permissions.IsAdmin])
def get_all_questionnaires(request):
    questionnaires = Questionnaire.objects.all()
    serializer = QuestionnaireSerializer(questionnaires, many=True)
    logger = logging.getLogger('app.questionnaire.get_all_questionnaires')
    logger.info(f'Admin: {request.user.email} requested the list of all questionnaires.')
    return Response(serializer.data)


@api_view(['POST', ])
@permission_classes([permissions.IsAuthenticated, user_permissions.IsAdmin])
def update_questionnaire(request):
    serializer = QuestionnaireSerializer(data=request.data)
    questionnaire_identifier = request.GET['identifier']
    if serializer.is_valid():
        if not Questionnaire.objects.filter(identifier=questionnaire_identifier).exists():
            return Response(data={'detail': 'Questionnaire does not exist.'},
                            status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        questionnaire = Questionnaire.objects.get(identifier=questionnaire_identifier)
        serializer.update(questionnaire, serializer.validated_data)
        return_dict = {'identifier': questionnaire.identifier, 'phase': questionnaire.phase, 'name': questionnaire.name}
        return Response(data=return_dict, status=status.HTTP_200_OK)
    return Response(data={'detail': 'Invalid request'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


@api_view(['POST', ])
@permission_classes([permissions.IsAuthenticated, user_permissions.IsAdmin])
def add_questionnaire(request):
    serializer = QuestionnaireSerializer(data=request.data)
    if serializer.is_valid():
        questionnaire = serializer.create(serializer.validated_data)
        return_dict = {'identifier': questionnaire.identifier, 'phase': questionnaire.phase, 'name': questionnaire.name}
        return Response(data=return_dict, status=status.HTTP_200_OK)
    return Response(data=serializer.errors,
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY)  # TODO is it safe to send serializer.errors field?


@api_view(['POST', ])
@permission_classes([permissions.IsAuthenticated, user_permissions.IsAdmin])
def delete_questionnaire(request):
    identifier = request.GET['identifier']
    if not Questionnaire.objects.filter(identifier=identifier).exists():
        return Response(data={'detail': 'Questionnaire does not exist.'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    questionnaire = Questionnaire.objects.get(identifier=identifier)
    try:
        questionnaire.delete()
    except RestrictedError as e:
        return Response(data={'detail': 'Deletion restricted'},
                        status=status.HTTP_409_CONFLICT)
    return Response(status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([permissions.IsAuthenticated, user_permissions.IsAdmin])
def update_question(request):
    serializer = QuestionSerializer(data=request.data)
    question_identifier = request.GET['identifier']
    if serializer.is_valid():
        if not Question.objects.filter(identifier=question_identifier).exists():
            return Response(data={'detail': 'Question does not exist.'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        question = Question.objects.get(identifier=question_identifier)
        serializer.update(question, serializer.validated_data)
        return_dict = {'identifier': question.identifier, 'body': question.body}
        return Response(data=return_dict, status=status.HTTP_200_OK)
    return Response(data={'detail': 'Invalid request'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


@api_view(['POST', ])
@permission_classes([permissions.IsAuthenticated, user_permissions.IsAdmin])
def add_question(request):
    serializer = QuestionSerializer(data=request.data)
    if serializer.is_valid():
        question = serializer.create(serializer.validated_data)
        position = question.position
        questions_below = Question.objects.filter(Q(position__gte=position) & ~Q(identifier=question.identifier))
        questions_below.update(position=F('position')+1)
        return_dict = {'identifier': question.identifier, 'body': question.body}
        return Response(data=return_dict, status=status.HTTP_200_OK)
    return Response(data=serializer.errors,
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY)  # TODO is it safe to send serializer.errors field?


@api_view(['POST', ])
@permission_classes([permissions.IsAuthenticated, user_permissions.IsAdmin])
def delete_question(request):
    identifier = request.GET['identifier']
    if not Question.objects.filter(identifier=identifier).exists():
        return Response(data={'detail': 'Question does not exist.'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    question = Question.objects.get(identifier=identifier)
    position = question.position
    try:
        question.delete()
    except RestrictedError as e:
        return Response(data={'detail': 'Deletion restricted'},
                        status=status.HTTP_409_CONFLICT)
    questions_below = Question.objects.filter(position__gt=position)
    questions_below.update(position=F('position')-1)
    return Response(status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([permissions.IsAuthenticated, user_permissions.IsAdmin])
def update_option(request):
    serializer = OptionSerializer(data=request.data)
    option_identifier = request.GET['identifier']
    if serializer.is_valid():
        if not Option.objects.filter(identifier=option_identifier).exists():
            return Response(data={'detail': 'Option does not exist.'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        option = Option.objects.get(identifier=option_identifier)

        # if adding a continuation questionnaire
        if serializer.validated_data.get('continuation_questionnaire', None) is not None:
            # continuation questionnaire should only be added to the last question's options
            if Question.objects.filter(questionnaire=option.question.questionnaire).order_by('-position').first().identifier != option.question.identifier:
                return Response(data={'detail': 'You can only add continuation questionnaire on the last question of a '
                                                'questionnaire.'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

            # any other question should not have continuation_questionnaire in any of their options
            other_options = Option.objects.filter(
                Q(question__questionnaire=option.question.questionnaire) & ~Q(question=option.question)
                & Q(continuation_questionnaire__isnull=False))
            if other_options.exists():
                return Response(data={'detail': 'Another question in this questionnaire has options with continuation'
                                                'questionnaire.'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

            # if the option corresponds to a multi-select question, then do not allow
            if option.question.multiselect:
                return Response(data={'detail': 'You are trying to add continuation-questionnaire to the last question '
                                                'which is also a multiselect question, which is not allowed.'},
                                status=status.HTTP_422_UNPROCESSABLE_ENTITY)

            # check if there exists a valid continuation questionnaire
            if not Questionnaire.objects.filter(identifier=serializer.validated_data['continuation_questionnaire']).exists():  # TODO check if validated_data['con_qnr'] returns identifier or the actual Questionnaire
                return Response(data={'detail': 'Invalid continuation questionnaire identifier supplied.'},
                                status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        serializer.update(option, serializer.validated_data)
        return_dict = {'identifier': option.identifier, 'body': option.body}
        return Response(data=return_dict, status=status.HTTP_200_OK)
    return Response(data={'detail': 'Invalid request'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


@api_view(['POST', ])
@permission_classes([permissions.IsAuthenticated, user_permissions.IsAdmin])
def add_option(request):
    serializer = OptionSerializer(data=request.data)
    if serializer.is_valid():
        validated_data = serializer.validated_data
        if serializer.validated_data.get('continuation_questionnaire', None) is not None:
            validated_data = serializer.validated_data.pop('continuation_questionnaire')  # Do not allow entering continuation questionnaire while creating option to to simplify checks
        option = serializer.create(validated_data)
        return_dict = {'identifier': option.identifier, 'body': option.body}
        return Response(data=return_dict, status=status.HTTP_200_OK)
    return Response(data=serializer.errors,
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY)  # TODO is it safe to send serializer.errors field?


@api_view(['POST', ])
@permission_classes([permissions.IsAuthenticated, user_permissions.IsAdmin])
def delete_option(request):
    identifier = request.GET['identifier']
    if not Option.objects.filter(identifier=identifier).exists():
        return Response(data={'detail': 'Option does not exist.'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    option = Option.objects.get(identifier=identifier)
    try:
        option.delete()
    except RestrictedError as e:
        return Response(data={'detail': 'Deletion restricted'},
                        status=status.HTTP_409_CONFLICT)
    return Response(status=status.HTTP_200_OK)
