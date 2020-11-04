from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group

from .models import CustomUser


# Register your models here.

# TODO understand all the fields here

class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput, required=True)
    password_confirmation = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput, required=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'phone_number', 'last_name', 'date_of_birth',)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.get("password_confirmation")
        if password and password_confirmation and password != password_confirmation:
            self.add_error('password', 'Passwords do not match.')
            self.add_error('password_confirmation', 'Passwords do not match.')
            # raise ValidationError("Passwords do not match.")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class CustomUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = (
            'email', 'password', 'first_name', 'last_name', 'phone_number', 'date_of_birth', 'is_active', 'is_admin',)

    def clean_password(self):
        return self.initial['password']


class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    list_display = ('email', 'password', 'first_name', 'last_name', 'phone_number', 'date_of_birth', 'is_admin')
    list_filter = ('is_admin',)
    exclude = ['verified', ]  # TODO is this required if readonly_fields is present?
    readonly_fields = ('verified',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone_number', 'date_of_birth')}),
        ('Permissions', {'fields': ('is_admin', 'verified')}),
    )
    add_fieldsets = (  # TODO why this if we have fieldsets?
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'password', 'password_confirmation', 'first_name', 'last_name', 'phone_number',
                'date_of_birth',),
        }),
    )

    search_fields = ('email', 'first_name')
    ordering = ('email', 'first_name')
    filter_horizontal = ()


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.unregister(Group)
