from django.contrib import admin, messages

# Register your models here.
from questionnaire.forms import QuestionnaireCreationForm
from questionnaire.models import Questionnaire, Question, Option


class QuestionInline(admin.TabularInline):
    model = Question
    show_change_link = True


class OptionInline(admin.TabularInline):
    model = Option
    show_change_link = True


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


admin.site.register(Questionnaire, QuestionnaireAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Option)
