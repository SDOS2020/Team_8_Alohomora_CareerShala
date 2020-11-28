from django.contrib import admin, messages

# Register your models here.
from grappelli.forms import GrappelliSortableHiddenMixin

from questionnaire.forms import QuestionnaireCreationForm, OptionCreationForm, QuestionCreationForm
from questionnaire.models import Questionnaire, Question, Option, Answer, QuestionnaireResponse


class QuestionInline(GrappelliSortableHiddenMixin, admin.TabularInline):
    model = Question
    show_change_link = True


class OptionInline(admin.TabularInline):
    model = Option
    show_change_link = True
    form = OptionCreationForm


class AnswerInline(admin.TabularInline):
    model = Answer


class QuestionnaireResponseAdmin(admin.ModelAdmin):
    inlines = [
        AnswerInline
    ]
    # readonly_fields = ('questionnaire', 'student_profile', 'answers')


class QuestionnaireAdmin(admin.ModelAdmin):
    form = QuestionnaireCreationForm
    inlines = [
        QuestionInline,
    ]
    list_filter = ('root',)
    list_display = ('name', 'root',)
    readonly_fields = ('root',)

    def has_delete_permission(self, request, obj: Questionnaire = None):
        if obj is not None and obj.root:
            error_message = 'Note that you cannot delete this questionnaire because this is the root questionnaire.'
            self.message_user(request, error_message, messages.WARNING)
            return False
        return super(QuestionnaireAdmin, self).has_delete_permission(request, obj)


class QuestionAdmin(admin.ModelAdmin):
    inlines = [
        OptionInline
    ]
    form = QuestionCreationForm

    exclude = ('position',)


class OptionAdmin(admin.ModelAdmin):
    form = OptionCreationForm


admin.site.register(Questionnaire, QuestionnaireAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Option, OptionAdmin)
admin.site.register(Answer)
admin.site.register(QuestionnaireResponse, QuestionnaireResponseAdmin)
