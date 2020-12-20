import logging

from django.db.models import signals
from django.test import TestCase

# Create your tests here.
from rest_framework import status

from AlohomoraCareershala.tests import TestCaseWithRegisteredUsers
from users.data import VALID_STUDENT_REGISTRATION_FORM_DATA, VALID_EXPERT_REGISTRATION_FORM_DATA, EMAILS
from users.models import CustomUser
from users.signals import send_verification_email


class RegistrationTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        logging.disable(logging.CRITICAL)
        signals.post_save.disconnect(receiver=send_verification_email, sender=CustomUser)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        logging.disable(logging.NOTSET)
        signals.post_save.connect(receiver=send_verification_email, sender=CustomUser)

    def test_valid_student_registration(self):
        data = VALID_STUDENT_REGISTRATION_FORM_DATA.copy()
        response = self.client.post('/users/register/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_student_registration(self):
        data = VALID_STUDENT_REGISTRATION_FORM_DATA.copy()
        data['email'] = data['email'].replace("@", "")
        response = self.client.post('/users/register/', data=data)
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_incomplete_student_registration(self):
        data = VALID_STUDENT_REGISTRATION_FORM_DATA.copy()
        del data['email']
        response = self.client.post('/users/register/', data=data)
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_valid_expert_registration(self):
        data = VALID_EXPERT_REGISTRATION_FORM_DATA.copy()
        response = self.client.post('/users/register/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_expert_registration(self):
        data = VALID_EXPERT_REGISTRATION_FORM_DATA.copy()
        data['email'] = data['email'].replace("@", "")
        response = self.client.post('/users/register/', data=data)
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_incomplete_expert_registration(self):
        data = VALID_EXPERT_REGISTRATION_FORM_DATA.copy()
        del data['email']
        response = self.client.post('/users/register/', data=data)
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)


class LoginTestCase(TestCaseWithRegisteredUsers):

    @classmethod
    def setUpClass(cls):
        logging.disable(logging.CRITICAL)
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        logging.disable(logging.NOTSET)
        super().tearDownClass()

    def test_verified_student_login(self):
        data = {
            'email': EMAILS['student_verified_profile_incomplete'],
            'password': VALID_STUDENT_REGISTRATION_FORM_DATA['password']
        }
        response = self.client.post('/users/login/', data=data, follow=True)
        self.assertEqual(response.context['user'].is_authenticated, True)

    def test_unverified_student_login(self):
        data = {
            'email': EMAILS['student_unverified'],
            'password': VALID_STUDENT_REGISTRATION_FORM_DATA['password']
        }
        response = self.client.post('/users/login/', data=data, follow=True)
        self.assertEqual(response.context['user'].is_authenticated, False)

    def test_verified_expert_login(self):
        data = {
            'email': EMAILS['expert_verified_profile_incomplete'],
            'password': VALID_EXPERT_REGISTRATION_FORM_DATA['password']
        }
        response = self.client.post('/users/login/', data=data, follow=True)
        self.assertEqual(response.context['user'].is_authenticated, True)

    def test_unverified_expert_login(self):
        data = {
            'email': EMAILS['expert_unverified'],
            'password': VALID_EXPERT_REGISTRATION_FORM_DATA['password']
        }
        response = self.client.post('/users/login/', data=data, follow=True)
        self.assertEqual(response.context['user'].is_authenticated, False)

    def test_invalid_credentials(self):
        data = {
            'email': EMAILS['student_verified_profile_incomplete'],
            'password': 'b@d p@$$w0rd'
        }
        response = self.client.post('/users/login/', data=data, follow=True)
        self.assertEqual(response.context['user'].is_authenticated, False)

    def test_non_exiting_account_login(self):
        data = {
            'email': 'unregistered@iiitd.ac.in',
            'password': 'p@$$w0rd'
        }
        response = self.client.post('/users/login/', data=data, follow=True)
        self.assertEqual(response.context['user'].is_authenticated, False)
