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

    def __str__(self):
        return self.name


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
