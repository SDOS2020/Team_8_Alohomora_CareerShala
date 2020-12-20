import logging

from django.test import TestCase

# Create your tests here.
from rest_framework import status

from AlohomoraCareershala.tests import TestCaseWithRegisteredUsers
from users.data import VALID_STUDENT_REGISTRATION_FORM_DATA, EMAILS


class DashboardAccessTestCase(TestCaseWithRegisteredUsers):

    @classmethod
    def setUpClass(cls):
        logging.disable(logging.CRITICAL)
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        logging.disable(logging.NOTSET)
        super().tearDownClass()

    def test_profile_completed_user_access_dashboard(self):
        data = {
            'email': EMAILS['student_verified_profile_complete'],
            'password': VALID_STUDENT_REGISTRATION_FORM_DATA.get('password')
        }
        logged_in = self.client.login(**data)
        self.assertTrue(logged_in)

        response = self.client.get('/dashboard/home/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_profile_incomplete_user_access_dashboard(self):
        data = {
            'email': EMAILS['student_verified_profile_incomplete'],
            'password': VALID_STUDENT_REGISTRATION_FORM_DATA.get('password')
        }
        logged_in = self.client.login(**data)
        self.assertTrue(logged_in)

        response = self.client.get('/dashboard/home/')
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
