EMAILS = {
    'student_verified_profile_incomplete': 'student_verified_profile_incomplete@iiitd.ac.in',
    'student_verified_profile_complete': 'student_verified_profile_complete@iiitd.ac.in',
    'student_unverified': 'student_unverified@iiitd.ac.in',
    'expert_verified_profile_incomplete': 'expert_verified_profile_incomplete@iiitd.ac.in',
    'expert_verified_profile_complete': 'expert_verified_profile_complete@iiitd.ac.in',
    'expert_unverified': 'expert_unverified@iiitd.ac.in',
}

VALID_STUDENT_REGISTRATION_FORM_DATA = {
    'email': EMAILS['student_unverified'],
    'password': 'p@$$w0rd-',
    'first_name': 'Student',
    'last_name': 'Student',
    'date_of_birth': '1998-12-04',
    'is_expert': False
}

VALID_EXPERT_REGISTRATION_FORM_DATA = VALID_STUDENT_REGISTRATION_FORM_DATA.copy()  # shallow
VALID_EXPERT_REGISTRATION_FORM_DATA['email'] = EMAILS['expert_unverified']
VALID_EXPERT_REGISTRATION_FORM_DATA['first_name'] = 'Expert'
VALID_EXPERT_REGISTRATION_FORM_DATA['last_name'] = 'Expert'
VALID_EXPERT_REGISTRATION_FORM_DATA['is_expert'] = True
