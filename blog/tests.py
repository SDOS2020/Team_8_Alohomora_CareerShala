import logging

from django.test import TestCase

# Create your tests here.
from rest_framework import status

from AlohomoraCareershala.tests import TestCaseWithRegisteredUsers
from users.data import EMAILS, VALID_EXPERT_REGISTRATION_FORM_DATA


class BlogAdditionTestCase(TestCaseWithRegisteredUsers):

    @classmethod
    def setUpClass(cls):
        logging.disable(logging.CRITICAL)
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        logging.disable(logging.NOTSET)
        super().tearDownClass()

    def test_verified_and_completed_profile_expert_can_add_blog(self):
        data = {
            'email': EMAILS['expert_verified_profile_complete'],
            'password': VALID_EXPERT_REGISTRATION_FORM_DATA['password']
        }
        logged_in = self.client.login(**data)
        self.assertTrue(logged_in)

        response = self.client.get('/blog/add_post/?post_type=1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_verified_and_incomplete_profile_expert_cannot_add_blog(self):
        data = {
            'email': EMAILS['expert_verified_profile_incomplete'],
            'password': VALID_EXPERT_REGISTRATION_FORM_DATA['password']
        }
        logged_in = self.client.login(**data)
        self.assertTrue(logged_in)

        response = self.client.get('/blog/add_post/?post_type=1')
        self.assertTrue(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response['location'], '/users/profile/')
