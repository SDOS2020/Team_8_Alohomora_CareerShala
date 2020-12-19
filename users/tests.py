from django.test import TestCase


# Create your tests here.
class RegistrationTestCase(TestCase):

    def test_valid_student_registration(self):
        data = {
            'email': 'reeshabh17086@iiitd.ac.in',
            'password': 'reeshabh@123',
            'first_name': 'Reeshabh',
            'last_name': 'Ranjan',
            'date_of_birth': '1998-12-04',
            'is_expert': False
        }

        response = self.client.post('/users/register/', data=data)
        self.assertEqual(response.status_code, 200)

    def test_valid_expert_registration(self):
        data = {
            'email': 'reeshabh17086@iiitd.ac.in',
            'password': 'reeshabh@123',
            'first_name': 'Reeshabh',
            'last_name': 'Ranjan',
            'date_of_birth': '1998-12-04',
            'is_expert': True
        }

        response = self.client.post('/users/register/', data=data)
        self.assertEqual(response.status_code, 200)
