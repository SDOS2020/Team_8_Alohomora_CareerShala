import logging
import uuid

from django.db.models import signals
from django.test import TestCase
from rest_framework import status

from blog.models import Post
from users.data import VALID_STUDENT_REGISTRATION_FORM_DATA, VALID_EXPERT_REGISTRATION_FORM_DATA, EMAILS
from users.models import CustomUser, Interest, Specialisation
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

        unverified_student_registration_data = VALID_STUDENT_REGISTRATION_FORM_DATA.copy()
        verified_incomplete_profile_student_registration_data = VALID_STUDENT_REGISTRATION_FORM_DATA.copy()
        verified_complete_profile_student_registration_data = VALID_STUDENT_REGISTRATION_FORM_DATA.copy()

        unverified_expert_registration_data = VALID_EXPERT_REGISTRATION_FORM_DATA.copy()
        verified_incomplete_profile_expert_registration_data = VALID_EXPERT_REGISTRATION_FORM_DATA.copy()
        verified_complete_profile_expert_registration_data = VALID_EXPERT_REGISTRATION_FORM_DATA.copy()

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

        cls.registered_expert_verified_profile_incomplete.expert_profile.verified = True
        cls.registered_expert_verified_profile_complete.expert_profile.verified = True
        cls.registered_expert_verified_profile_incomplete.expert_profile.save()
        cls.registered_expert_verified_profile_complete.expert_profile.save()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        signals.post_save.connect(receiver=send_verification_email, sender=CustomUser)
        cls.registered_student_verified_profile_incomplete: CustomUser = None
        cls.registered_student_unverified: CustomUser = None
        cls.registered_expert_verified_profile_incomplete: CustomUser = None
        cls.registered_expert_unverified: CustomUser = None


class SystemTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        logging.disable(logging.CRITICAL)
        signals.post_save.disconnect(receiver=send_verification_email, sender=CustomUser)

        interest_labels = ["Medicine", "Engineering", "Law", "Art", "Science"]
        specialisation_labels = ["Medicine", "Engineering", "Law", "Art", "Science"]

        for interest_label in interest_labels:
            Interest.objects.create(label=interest_label, description="")

        for specialisation_label in specialisation_labels:
            Specialisation.objects.create(label=specialisation_label, description="")

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        logging.disable(logging.NOTSET)
        signals.post_save.connect(receiver=send_verification_email, sender=CustomUser)

    def test_expert_student_interaction_via_posts(self):
        student_registration_data = VALID_STUDENT_REGISTRATION_FORM_DATA.copy()
        expert_registration_data = VALID_EXPERT_REGISTRATION_FORM_DATA.copy()
        student_registration_data['email'] = EMAILS['student_verified_profile_complete']
        expert_registration_data['email'] = EMAILS['expert_verified_profile_complete']

        student_login_data = {
            'email': student_registration_data['email'],
            'password': student_registration_data['password']
        }

        expert_login_data = {
            'email': expert_registration_data['email'],
            'password': expert_registration_data['password']
        }

        # register student
        response = self.client.post('/users/register/', data=student_registration_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # register expert
        response = self.client.post('/users/register/', data=expert_registration_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # verify their accounts
        student_user = CustomUser.objects.get(email=student_registration_data['email'])
        student_user.verified = True
        student_user.save()

        expert_user = CustomUser.objects.get(email=expert_registration_data['email'])
        expert_user.verified = True
        expert_user.save()
        expert_user.expert_profile.verified = True
        expert_user.expert_profile.save()

        # expert login
        response = self.client.post('/users/login/', data=expert_login_data, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)

        # expert profile updation
        expert_profile_data = {
            'specialisations': ['1', '2'],
            'associated_institute': ['']  # TODO
        }
        response = self.client.post('/users/profile/', data=expert_profile_data, follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # post-creation by expert
        post_creation_data = {
            'title': 'ProjectTitle',
            'body': '<p>ProjectBody</p>\r\n',
            'preview': 'ProjectPreview',
            'type': 4,
            'tags': ['project'],
            'allow_comments': True
        }

        response = self.client.post('/blog/add_post/?post_type=4', data=post_creation_data, follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # logout expert
        response = self.client.post('/users/logout/', follow=True)
        self.assertFalse(response.context['user'].is_authenticated)

        # student login
        response = self.client.post('/users/login/', data=student_login_data, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)

        # update profile
        student_profile_data = {
            'interests': ['1', '2']
        }
        response = self.client.post('/users/profile/', data=student_profile_data, follow=True)
        self.assertTrue(response.status_code, status.HTTP_200_OK)

        # access project post
        project_post = Post.objects.get()
        project_slug = project_post.slug
        response = self.client.get(f'/blog/post/{project_slug}')
        self.assertEqual(response.context['post'], project_post)

        # logout student
        response = self.client.post('/users/logout/', follow=True)
        self.assertFalse(response.context['user'].is_authenticated)
