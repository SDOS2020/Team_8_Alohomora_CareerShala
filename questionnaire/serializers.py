from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from questionnaire.models import Questionnaire, Question, Option, Answer, QuestionnaireResponse
from users.models import StudentProfile


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['body', 'identifier', ]


class QuestionSerializer(serializers.ModelSerializer):
    option = OptionSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['body', 'multiselect', 'option', 'identifier', ]


class QuestionnaireSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Questionnaire
        fields = ['name', 'phase', 'question', 'identifier']


class AnswerSerializer(serializers.ModelSerializer):
    question = serializers.SlugRelatedField(slug_field='identifier', queryset=Question.objects.all())
    option = serializers.SlugRelatedField(slug_field='identifier', queryset=Option.objects.all())

    class Meta:
        model = Answer
        fields = ['question', 'option']

    def validate(self, attrs):
        request_user = self.context['request'].user
        cond1 = attrs['question'].questionnaire = request_user.student_profile.next_questionnaire
        cond2 = attrs['option'].question = attrs['question']
        #  TODO will the following query be expensive?
        cond3 = (not attrs['question'].multiselect and not Answer.objects.filter(
            questionnaire_response__student_profile=request_user.student_profile,
            question=attrs['question']).exists()) or attrs['question'].multiselect

        if not cond1:
            raise serializers.ValidationError(f'You cannot respond to question: {attrs["question"].identifier}')

        if not cond2:
            raise serializers.ValidationError(
                f'Option: {attrs["option"]} does not match with Question: {attrs["question"].identifier}')

        if not cond3:
            raise serializers.ValidationError(
                f'You cannot select multiple options for a non-multiselect question ({attrs["question"].identifier})')

        return attrs


class CurrentStudentProfile(object):
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context['request'].user.student_profile

    def __repr__(self):
        return '%s()' % self.__class__.__name__


class QuestionnaireResponseSerializer(serializers.ModelSerializer):
    questionnaire = serializers.SlugRelatedField(slug_field='identifier',
                                                 queryset=Questionnaire.objects.all())

    # I finally created my own default class
    student_profile = serializers.HiddenField(default=CurrentStudentProfile, write_only=True)
    answers = AnswerSerializer(many=True)

    class Meta:
        model = QuestionnaireResponse
        fields = ['questionnaire', 'student_profile', 'answers']

    def get_student_profile(self):
        return self.context['request'].user.student_profile

    def validate(self, attrs):
        cond1 = self.context['request'].user.student_profile.next_questionnaire = attrs['questionnaire']
        if not cond1:
            raise serializers.ValidationError("Wrong questionnaire specified.")
        return attrs

    # why we need custom create: https://www.django-rest-framework.org/api-guide/relations/#writable-nested-serializers
    def create(self, validated_data):
        answers = validated_data.pop('answers')
        questionnaire_response = QuestionnaireResponse.objects.create(**validated_data, student_profile=self.context[
            'request'].user.student_profile)
        for answer in answers:
            Answer.objects.create(questionnaire_response=questionnaire_response, **answer)
        return questionnaire_response
