from datetime import date

from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.auth import authenticate
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from users.models import CustomUser, StudentProfile, ExpertProfile, Interest, Specialisation


# Essential Forms

class LoginForm(forms.Form):
    email = forms.EmailField(label="Email", widget=forms.EmailInput, max_length=50, required=True)
    password = forms.CharField(label="Password", widget=forms.PasswordInput, required=True)

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        if authenticate(email=cleaned_data.get("email"),
                        password=cleaned_data.get("password")) is None:
            raise ValidationError("Incorrect credentials")
        return cleaned_data


class StudentProfileForm(forms.ModelForm):
    interests = forms.ModelMultipleChoiceField(queryset=Interest.objects.all(),
                                               widget=forms.CheckboxSelectMultiple,
                                               required=False)

    class Meta:
        model = StudentProfile
        fields = ('interests',)


class ExpertProfileForm(forms.ModelForm):
    specialisations = forms.ModelMultipleChoiceField(queryset=Specialisation.objects.all(),
                                                     widget=forms.CheckboxSelectMultiple,
                                                     required=True)

    class Meta:
        model = ExpertProfile
        fields = ('specialisations', 'associated_institute',)


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

    def clean_name(self, name: str):
        cond1 = ' ' in name
        cond2 = any(not ch.isalpha() for ch in name)
        if cond1 or cond2:
            raise ValidationError("Invalid name")

    def clean_first_name(self):
        first_name: str = self.cleaned_data.get("first_name")
        self.clean_name(first_name)
        return first_name

    def clean_last_name(self):
        last_name: str = self.cleaned_data.get("last_name")
        self.clean_name(last_name)
        return last_name

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
