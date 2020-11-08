from datetime import date

from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from users.models import CustomUser


# Essential Forms

class LoginForm(forms.Form):
    email = forms.EmailField(label="Email", widget=forms.EmailInput, max_length=50, required=True)
    password = forms.CharField(label="Password", widget=forms.PasswordInput, required=True)


class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput, required=True)

    # By default, all fields are required as in the fields below

    class Meta:
        model = CustomUser  # TODO for some reason, cannot be replaced with settings.AUTH_USER_MODEL
        fields = ('email', 'first_name', 'phone_number', 'date_of_birth', 'last_name', 'is_expert')

    def clean_date_of_birth(self):
        # date of birth check TODO which code is checking for non-nullity of date-of-birth then?
        date_of_birth = self.cleaned_data.get("date_of_birth")  # TODO is_valid is called before clean?
        date_today = date.today()
        age = date_today.year - date_of_birth.year - \
              ((date_today.month, date_today.day) < (date_of_birth.month, date_of_birth.day))
        if age <= 13:
            raise ValidationError("You are too young to join this site. Only 14 years and older allowed.")
        return date_of_birth

    def clean_password(self):
        password: str = self.cleaned_data.get("password")
        validate_password(password=password)
        return password

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


# Trivial Forms

class ErrorForm(forms.Form):
    title = forms.CharField(label="Title", max_length=100, required=True)
    body = forms.CharField(label="Body", max_length=1000, required=False)
