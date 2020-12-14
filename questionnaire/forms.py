from django import forms
from django.core.exceptions import ValidationError

from questionnaire.models import Questionnaire, Question, Option


class QuestionnaireCreationForm(forms.ModelForm):
    class Meta:
        model = Questionnaire
        fields = ('phase', 'name', 'root')

    # enforcing single root
    def clean_root(self):
        root_field = self.cleaned_data.get('root')
        invalid = False
        if Questionnaire.objects.filter(root=True).exists():
            if self.instance.pk is None:  # if new questionnaire is being added
                if root_field is True:
                    invalid = True
            else:  # if existing questionnaire is being edited
                if Questionnaire.objects.get(root=True).pk != self.instance.pk:
                    if root_field is True:
                        invalid = True
            if invalid:
                raise ValidationError('You already have a root questionnaire!')

        return self.cleaned_data.get('root')

    # enforcing non-continuation of a multiselect last question
    def clean(self):
        cleaned_data = super().clean()
        questions_queryset = self.instance.question.order_by('-position')
        if questions_queryset.exists():
            last_question: Question = questions_queryset.first()
            if last_question.multiselect:
                options_queryset = Option.objects.filter(question=last_question,
                                                         continuation_questionnaire__isnull=False)
                if options_queryset.exists():
                    raise ValidationError(
                        "If the last question is multiselect, it's options cannot lead to any continuation "
                        "questionnaire. You can reorder the questions accordingly.")
        return cleaned_data


class OptionCreationForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ('body', 'question', 'continuation_questionnaire', 'tags')

    def clean_continuation_questionnaire(self):
        continuation_questionnaire = self.cleaned_data['continuation_questionnaire']
        if continuation_questionnaire is not None:
            question = self.cleaned_data['question']
            parent_questionnaire = question.questionnaire
            if parent_questionnaire is not None:
                if parent_questionnaire.question.order_by(
                        '-position').first().pk == question.pk and question.multiselect:
                    raise ValidationError(
                        "If the last question of a questionnaire is multiselect, it's options cannot lead to "
                        "continuation questionnaire. "
                        "You can also reorder the questions related to this options accordingly.")
        return self.cleaned_data['continuation_questionnaire']


class QuestionCreationForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('body', 'questionnaire')

    def clean(self):
        cleaned_data = super().clean()
        parent_questionnaire: Questionnaire = self.instance.questionnaire
        if parent_questionnaire is not None:
            if parent_questionnaire.question.order_by('-position').first().pk == self.instance.pk:
                if self.instance.multiselect:
                    if self.instance.option.filter(continuation_questionnaire__isnull=False):
                        raise ValidationError("This question is multiselect as well as the last question of this "
                                              "questionnaire. One of its options have a continuation questionnaire. "
                                              "Such questions cannot have options that lead to a continuation "
                                              "questionnaire.")
        return cleaned_data
