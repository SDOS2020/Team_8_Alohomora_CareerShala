from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
from django.db import models

from users.methods import generate_token


# Refer: https://docs.djangoproject.com/en/3.1/topics/auth/customizing/#a-full-example
class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, date_of_birth, password=None):
        if not email:
            raise ValueError('Email is a required field.')
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
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    first_name = models.CharField(verbose_name='first name', max_length=255)
    last_name = models.CharField(verbose_name='last name', max_length=255)
    phone_number = models.CharField(verbose_name='phone number', max_length=14, unique=True, blank=True, null=True)
    date_of_birth = models.DateField(verbose_name='date of birth')

    # Fields related to email verification
    email_verification_token = models.CharField(max_length=32,
                                                default=generate_token)  # TODO Remove this hardcoded value
    verified = models.BooleanField(default=False, verbose_name='Verified')

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
