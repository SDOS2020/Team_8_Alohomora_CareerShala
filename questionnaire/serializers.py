from rest_framework import serializers

from questionnaire.models import Questionnaire, Question, Option


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
        fields = ['name', 'phase', 'question']
