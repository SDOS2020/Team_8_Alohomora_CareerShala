from rest_framework import serializers

from questionnaire.models import Questionnaire, Question, Option


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['body']


class QuestionSerializer(serializers.ModelSerializer):
    option = OptionSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['body', 'multiselect', 'option']


class QuestionnaireSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Questionnaire
        fields = ['name', 'phase', 'question']
