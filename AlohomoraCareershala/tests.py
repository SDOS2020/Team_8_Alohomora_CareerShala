import logging

from django.db.models import signals
from django.test import TestCase

from users.data import VALID_STUDENT_REGISTRATION_FORM_DATA, VALID_EXPERT_REGISTRATION_FORM_DATA
from users.models import CustomUser
from users.signals import send_verification_email


class TestCaseWithRegisteredUsers(TestCase):
    registered_student_verified: CustomUser = None
    registered_student_unverified: CustomUser = None
    registered_expert_verified: CustomUser = None
    registered_expert_unverified: CustomUser = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        signals.post_save.disconnect(receiver=send_verification_email, sender=CustomUser)

        verified_student_registration_data = VALID_STUDENT_REGISTRATION_FORM_DATA.copy()
        verified_expert_registration_data = VALID_EXPERT_REGISTRATION_FORM_DATA.copy()
        unverified_student_registration_data = VALID_STUDENT_REGISTRATION_FORM_DATA.copy()
        unverified_expert_registration_data = VALID_EXPERT_REGISTRATION_FORM_DATA.copy()

        verified_student_registration_data['email'] = 'verified_student@iiitd.ac.in'
        unverified_student_registration_data['email'] = 'unverified_student@iiitd.ac.in'
        verified_expert_registration_data['email'] = 'verified_expert@iiitd.ac.in'
        unverified_expert_registration_data['email'] = 'unverified_expert@iiitd.ac.in'

        cls.registered_student_verified = CustomUser.objects.create_user(**verified_student_registration_data)
        cls.registered_student_unverified = CustomUser.objects.create_user(**unverified_student_registration_data)
        cls.registered_expert_verified = CustomUser.objects.create_user(**verified_expert_registration_data)
        cls.registered_expert_unverified = CustomUser.objects.create_user(**unverified_expert_registration_data)

        cls.registered_student_verified.verified = True
        cls.registered_student_verified.save()

        cls.registered_expert_verified.verified = True
        cls.registered_expert_verified.save()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        signals.post_save.connect(receiver=send_verification_email, sender=CustomUser)
        cls.registered_student_verified: CustomUser = None
        cls.registered_student_unverified: CustomUser = None
        cls.registered_expert_verified: CustomUser = None
        cls.registered_expert_unverified: CustomUser = None
