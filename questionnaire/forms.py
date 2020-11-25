from django import forms
from django.core.exceptions import ValidationError

from questionnaire.models import Questionnaire


class QuestionnaireCreationForm(forms.ModelForm):
    class Meta:
        model = Questionnaire
        fields = ('phase', 'name', 'continuation_questionnaire', 'root')

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
