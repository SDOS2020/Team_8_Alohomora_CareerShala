from django.contrib import admin

# Register your models here.
from questionnaire.models import Questionnaire, Question, Option


class QuestionInline(admin.TabularInline):
    model = Question
    show_change_link = True


class OptionInline(admin.TabularInline):
    model = Option
    show_change_link = True


class QuestionnaireAdmin(admin.ModelAdmin):
    inlines = [
        QuestionInline,
    ]


class QuestionAdmin(admin.ModelAdmin):
    inlines = [
        OptionInline
    ]


admin.site.register(Questionnaire, QuestionnaireAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Option)
