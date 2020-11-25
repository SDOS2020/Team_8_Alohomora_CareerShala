from django.conf import settings
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
from django.db import models

from users.methods import generate_token


class Interest(models.Model):
    label = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=2000, null=True, blank=True)

    def __str__(self):
        return self.label


class Specialisation(models.Model):
    label = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=2000, null=True, blank=True)

    def __str__(self):
        return self.label


class StudentProfile(models.Model):
    user = models.OneToOneField('users.CustomUser', on_delete=models.CASCADE, related_name="student_profile")
    interests = models.ManyToManyField('users.Interest', blank=True)
    next_questionnaire = models.ForeignKey('questionnaire.Questionnaire', on_delete=models.PROTECT,
                                           related_name='pending_student', null=True, blank=True)

    def __str__(self):
        return f"{self.user.email}'s profile"


class ExpertProfile(models.Model):
    user = models.OneToOneField('users.CustomUser', on_delete=models.CASCADE, related_name="expert_profile")
    verified = models.BooleanField(default=False)
    specialisations = models.ManyToManyField('users.Specialisation')
    associated_institute = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.user.email}'s profile"


# Refer: https://docs.djangoproject.com/en/3.1/topics/auth/customizing/#a-full-example
class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, date_of_birth, password=None):
        if not email:
            raise ValueError('Email is a required field.')
        if not date_of_birth:
            raise ValueError('Date of birth is a required field.')
        user = self.model(email=self.normalize_email(email),
                          first_name=first_name,
                          last_name=last_name,
                          date_of_birth=date_of_birth)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, date_of_birth, password=None):
        user = self.create_user(email=email, first_name=first_name, last_name=last_name, password=password,
                                date_of_birth=date_of_birth)
        user.is_admin = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    # General fields
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True,
                              error_messages={'unique': 'A user with this email already exists.'})
    first_name = models.CharField(verbose_name='first name', max_length=255)
    last_name = models.CharField(verbose_name='last name', max_length=255)
    phone_number = models.CharField(verbose_name='phone number', max_length=14, unique=True, blank=True, null=True)
    date_of_birth = models.DateField(verbose_name='date of birth')
    is_expert = models.BooleanField(verbose_name='is expert', default=False)

    # Fields related to auth, profile
    email_verification_token = models.CharField(max_length=32,
                                                default=generate_token)  # TODO Remove this hardcoded value
    verified = models.BooleanField(default=False, verbose_name='Email Verified?')
    profile_completed = models.BooleanField(default=False)

    # Django-specific fields
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'date_of_birth']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
