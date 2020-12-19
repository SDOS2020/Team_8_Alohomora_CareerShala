VALID_STUDENT_REGISTRATION_FORM_DATA = {
    'email': 'reeshabh17086@iiitd.ac.in',
    'password': 'reeshabh@123',
    'first_name': 'Reeshabh',
    'last_name': 'Ranjan',
    'date_of_birth': '1998-12-04',
    'is_expert': False
}

VALID_EXPERT_REGISTRATION_FORM_DATA = VALID_STUDENT_REGISTRATION_FORM_DATA.copy()  # shallow
VALID_EXPERT_REGISTRATION_FORM_DATA['is_expert'] = True
