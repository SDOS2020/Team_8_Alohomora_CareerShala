import logging

from django.test import TestCase

# Create your tests here.
from rest_framework import status

from users.data import VALID_STUDENT_REGISTRATION_FORM_DATA, VALID_EXPERT_REGISTRATION_FORM_DATA


class RegistrationTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        logging.disable(logging.CRITICAL)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        logging.disable(logging.NOTSET)

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
