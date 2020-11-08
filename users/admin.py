from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    list_display = ('email', 'password', 'first_name', 'last_name', 'phone_number', 'date_of_birth', 'is_expert',
                    'is_admin')  # columns of users table
    list_filter = ('is_admin', 'is_expert')
    # exclude = ['verified', ]  # TODO is this required if readonly_fields is present?
    readonly_fields = ('verified',)  # TODO add is_expert to readonly_fields before production
    fieldsets = (  # Fields shown when viewing an account from admin site
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone_number', 'date_of_birth')}),
        ('Permissions', {'fields': ('is_expert', 'is_admin', 'verified')}),
    )
    add_fieldsets = (  # Fields shown on adding an account from admin site
        (None, {
            'classes': ('wide',),
            'fields': (  # TODO group fields as in fieldsets
                'email', 'password', 'first_name', 'last_name', 'phone_number',
                'date_of_birth', 'is_expert'),
        }),
    )

    search_fields = ('email', 'first_name')
    ordering = ('email', 'first_name')
    filter_horizontal = ()


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.unregister(Group)
