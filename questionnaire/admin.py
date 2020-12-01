import io

import xlsxwriter
from django.contrib import admin, messages

# Register your models here.
from django.http import HttpResponse
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
    actions = ['export']

    def has_delete_permission(self, request, obj: Questionnaire = None):
        if obj is not None and obj.root:
            error_message = 'Note that you cannot delete this questionnaire because this is the root questionnaire.'
            self.message_user(request, error_message, messages.WARNING)
            return False
        return super(QuestionnaireAdmin, self).has_delete_permission(request, obj)

    def get_table_data(self, questionnaire: Questionnaire):
        data = []
        # headers
        header = ['Student']
        for question in questionnaire.question.order_by('position'):
            header.append(question.body)
        data.append(header)
        for response in questionnaire.questionnaire_responses.all():
            response: QuestionnaireResponse
            row = [response.student_profile.user.email]
            for answer in response.answers.order_by('question__position'):
                row.append(str(answer.option))
            data.append(row)
        return data

    def export(self, request, queryset):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        for questionnaire in queryset:
            worksheet = workbook.add_worksheet(name=str(questionnaire))
            data = self.get_table_data(questionnaire)
            for row_num, columns in enumerate(data):
                for col_num, cell_data in enumerate(columns):
                    worksheet.write(row_num, col_num, cell_data)
        workbook.close()
        output.seek(0)
        filename = 'responses.xlsx'
        response = HttpResponse(output,
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f"attachment; filename={filename}"
        return response

    export.short_description = "Export selected questionnaire as excel file."


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
