import uuid

import tagulous.models
from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.

from users.models import CustomUser


class Questionnaire(models.Model):
    PHASE_CHOICES = (
        (1, 'Phase-1'),
        (2, 'Phase-2'),
        (3, 'Phase-3'),
        (4, 'Phase-4'),
    )

    identifier = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=500)
    phase = models.PositiveSmallIntegerField(choices=PHASE_CHOICES, default=1)
    root = models.BooleanField(default=False, help_text='Note that you cannot delete the root questionnaire.')

    def __str__(self):
        return self.name

    # TODO needed? (already enforced in forms.py)
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None, *args, **kwargs):
        root_field = self.root
        if Questionnaire.objects.filter(root=True).exists():
            invalid = False
            if self.pk is None:  # if new questionnaire is being added
                if root_field is True:
                    invalid = True
            else:  # if existing questionnaire is being edited
                if Questionnaire.objects.get(root=True).pk != self.pk:
                    if root_field is True:
                        invalid = True
            if invalid:
                raise ValidationError('You already have a root questionnaire!')
        super(Questionnaire, self).save(force_insert=force_insert,
                                        force_update=force_update,
                                        using=using,
                                        update_fields=update_fields,
                                        *args,
                                        **kwargs)

    # TODO needed? (already enforced in admin.py)
    def delete(self, using=None, keep_parents=False):
        if self.root:
            raise ValidationError('You cannot delete a root question! Consider editing it instead.')
        super(Questionnaire, self).delete(using=using, keep_parents=keep_parents)


class Question(models.Model):
    identifier = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    body = models.CharField(max_length=1000)
    questionnaire = models.ForeignKey('Questionnaire', related_name='question', on_delete=models.CASCADE)
    multiselect = models.BooleanField(default=False)
    position = models.PositiveSmallIntegerField("position", null=True)

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.body


class Option(models.Model):
    identifier = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    body = models.CharField(max_length=1000)
    question = models.ForeignKey('Question', related_name='option', on_delete=models.CASCADE)
    continuation_questionnaire = models.ForeignKey('Questionnaire', related_name='from_options', null=True,
                                                   blank=True,
                                                   on_delete=models.SET_NULL)
    tags = tagulous.models.TagField()

    def clean(self):
        if self.continuation_questionnaire == self.question.questionnaire:
            raise ValidationError('Continuation questionnaire cannot point to the current one!')

    def __str__(self):
        return self.body


class QuestionnaireResponse(models.Model):
    questionnaire = models.ForeignKey('questionnaire.Questionnaire', on_delete=models.RESTRICT,
                                      related_name='questionnaire_responses')
    student_profile = models.ForeignKey('users.StudentProfile', on_delete=models.CASCADE,
                                        related_name='student_profile_responses')


class Answer(models.Model):
    questionnaire_response = models.ForeignKey('questionnaire.QuestionnaireResponse', on_delete=models.CASCADE,
                                               related_name='answers')
    question = models.ForeignKey('questionnaire.Question', on_delete=models.RESTRICT, related_name='question_responses')
    option = models.ForeignKey('questionnaire.Option', on_delete=models.RESTRICT, related_name='option_responses')
