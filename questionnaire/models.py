from django.db import models


# Create your models here.
class Questionnaire(models.Model):
    name = models.CharField(max_length=500)
    continuation_questionnaire = models.ForeignKey('self', related_name='previous_questionnaire', null=True, blank=True,
                                                   on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class Question(models.Model):
    body = models.CharField(max_length=1000)
    questionnaire = models.ForeignKey('Questionnaire', related_name='question', on_delete=models.CASCADE)

    def __str__(self):
        return self.body


class Option(models.Model):
    body = models.CharField(max_length=1000)
    question = models.ForeignKey('Question', related_name='option', on_delete=models.CASCADE)

    def __str__(self):
        return self.body
