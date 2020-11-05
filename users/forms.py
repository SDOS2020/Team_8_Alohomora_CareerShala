from datetime import date

from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from users.models import CustomUser


class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput, required=True)
    password_confirmation = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput, required=True)

    # By default, all fields are required as in the fields below

    class Meta:
        model = CustomUser  # TODO for some reason, cannot be replaced with settings.AUTH_USER_MODEL
        fields = ('email', 'first_name', 'phone_number', 'date_of_birth', 'last_name', 'is_expert')

    def clean_date_of_birth(self):
        # date of birth check TODO which code is checking for non-nullity of date-of-birth then?
        date_of_birth = self.cleaned_data.get("date_of_birth")  # TODO is_valid is called before clean?
        print(date_of_birth, type(date_of_birth))
        date_today = date.today()
        age = date_today.year - date_of_birth.year - \
              ((date_today.month, date_today.day) < (date_of_birth.month, date_of_birth.day))
        if age <= 13:
            self.add_error('date_of_birth', 'You are too young to join this site.')

    def clean_password_confirmation(self):
        # password confirmation
        password = self.cleaned_data.get("password")
        password_confirmation = self.cleaned_data.get("password_confirmation")
        if password and password_confirmation and password != password_confirmation:
            self.add_error('password', 'Passwords do not match.')
            self.add_error('password_confirmation', 'Passwords do not match.')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class CustomUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser  # TODO for some reason, cannot be replaced with settings.AUTH_USER_MODEL
        fields = (
            'email', 'password', 'first_name', 'last_name', 'phone_number', 'date_of_birth', 'is_active', 'is_admin',)

    def clean_password(self):
        return self.initial['password']
