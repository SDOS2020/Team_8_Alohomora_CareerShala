from django.core.exceptions import ValidationError
from django.db import models


# Create your models here.
class Questionnaire(models.Model):
    PHASE_CHOICES = (
        (1, 'Phase-1'),
        (2, 'Phase-2'),
        (3, 'Phase-3'),
        (4, 'Phase-4'),
    )
    name = models.CharField(max_length=500)
    continuation_questionnaire = models.OneToOneField('self', related_name='previous_questionnaire', null=True,
                                                      blank=True,
                                                      on_delete=models.SET_NULL)
    phase = models.PositiveSmallIntegerField(choices=PHASE_CHOICES, default=1)
    root = models.BooleanField(default=False, help_text='Note that you cannot delete the root questionnaire.')

    def __str__(self):
        return self.name

    def clean(self):
        if self.continuation_questionnaire == self:
            raise ValidationError('Continuation questionnaire cannot point to the current one!')

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
    body = models.CharField(max_length=1000)
    questionnaire = models.ForeignKey('Questionnaire', related_name='question', on_delete=models.CASCADE)
    multiselect = models.BooleanField(default=False)

    def __str__(self):
        return self.body


class Option(models.Model):
    body = models.CharField(max_length=1000)
    question = models.ForeignKey('Question', related_name='option', on_delete=models.CASCADE)

    def __str__(self):
        return self.body
