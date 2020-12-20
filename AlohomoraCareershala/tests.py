import logging
import uuid

from django.db.models import signals
from django.test import TestCase

from users.data import VALID_STUDENT_REGISTRATION_FORM_DATA, VALID_EXPERT_REGISTRATION_FORM_DATA, EMAILS
from users.models import CustomUser
from users.signals import send_verification_email


class TestCaseWithRegisteredUsers(TestCase):
    registered_student_verified_profile_incomplete: CustomUser = None
    registered_student_verified_profile_complete: CustomUser = None
    registered_student_unverified: CustomUser = None
    registered_expert_verified_profile_incomplete: CustomUser = None
    registered_expert_verified_profile_complete: CustomUser = None
    registered_expert_unverified: CustomUser = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        signals.post_save.disconnect(receiver=send_verification_email, sender=CustomUser)

        verified_incomplete_profile_student_registration_data = VALID_STUDENT_REGISTRATION_FORM_DATA.copy()
        verified_incomplete_profile_expert_registration_data = VALID_EXPERT_REGISTRATION_FORM_DATA.copy()
        verified_complete_profile_student_registration_data = VALID_STUDENT_REGISTRATION_FORM_DATA.copy()
        verified_complete_profile_expert_registration_data = VALID_EXPERT_REGISTRATION_FORM_DATA.copy()
        unverified_student_registration_data = VALID_STUDENT_REGISTRATION_FORM_DATA.copy()
        unverified_expert_registration_data = VALID_EXPERT_REGISTRATION_FORM_DATA.copy()

        verified_incomplete_profile_student_registration_data['email'] = EMAILS['student_verified_profile_incomplete']
        verified_complete_profile_student_registration_data['email'] = EMAILS['student_verified_profile_complete']
        unverified_student_registration_data['email'] = EMAILS['student_unverified']
        verified_incomplete_profile_expert_registration_data['email'] = EMAILS['expert_verified_profile_incomplete']
        verified_complete_profile_expert_registration_data['email'] = EMAILS['expert_verified_profile_complete']
        unverified_expert_registration_data['email'] = EMAILS['expert_unverified']

        cls.registered_student_verified_profile_incomplete = CustomUser.objects.create_user(
            **verified_incomplete_profile_student_registration_data)
        cls.registered_student_verified_profile_complete = CustomUser.objects.create_user(
            **verified_complete_profile_student_registration_data)
        cls.registered_student_unverified = CustomUser.objects.create_user(**unverified_student_registration_data)

        cls.registered_expert_verified_profile_incomplete = CustomUser.objects.create_user(
            **verified_incomplete_profile_expert_registration_data)
        cls.registered_expert_verified_profile_complete = CustomUser.objects.create_user(
            **verified_complete_profile_expert_registration_data)
        cls.registered_expert_unverified = CustomUser.objects.create_user(**unverified_expert_registration_data)

        cls.registered_student_verified_profile_complete.verified = True
        cls.registered_student_verified_profile_complete.profile_completed = True
        cls.registered_student_verified_profile_complete.save()

        cls.registered_expert_verified_profile_complete.verified = True
        cls.registered_expert_verified_profile_complete.profile_completed = True
        cls.registered_expert_verified_profile_complete.save()

        cls.registered_student_verified_profile_incomplete.verified = True
        cls.registered_student_verified_profile_incomplete.save()

        cls.registered_expert_verified_profile_incomplete.verified = True
        cls.registered_expert_verified_profile_incomplete.save()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        signals.post_save.connect(receiver=send_verification_email, sender=CustomUser)
        cls.registered_student_verified_profile_incomplete: CustomUser = None
        cls.registered_student_unverified: CustomUser = None
        cls.registered_expert_verified_profile_incomplete: CustomUser = None
        cls.registered_expert_unverified: CustomUser = None
