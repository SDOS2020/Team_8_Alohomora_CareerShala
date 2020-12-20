"""
WARNING:    THIS WILL DELETE ALL MIGRATION FILES AND THE SQLITE DATABASE.
            To be used as a utility script.
            No main function so that user doesn't delete files by mistake.
"""
import json
import os
from datetime import date
from glob import glob

from django.conf import settings
from django.contrib.sites.models import Site

from questionnaire.models import Questionnaire, Question, Option
from users.models import CustomUser, Interest, Specialisation


def reset():
    if settings.PRODUCTION_SERVER:
        print("This file should not be executed on the production server. Please use migrations/fixtures instead.")
        print("Exiting...")
        return

    confirm = input("Do you want to clear the existing database? This operation will fail on Heroku. (y/n).")
    if confirm.lower() == "y":
        print("Resetting database...")
        os.system("python manage.py reset_db --noinput")
        os.system("python manage.py migrate")

        superuser_email = "reeshabhkumarranjan@gmail.com"
        superuser_password = "reeshabh@123"
        superuser_first_name = "Reeshabh"
        superuser_last_name = "Admin"
        superuser_dob = date(1998, 12, 4)

        superuser = CustomUser.objects.create_superuser(email=superuser_email,
                                                        first_name=superuser_first_name,
                                                        last_name=superuser_last_name,
                                                        password=superuser_password,
                                                        date_of_birth=superuser_dob)
        print(f"Created superuser with \nemail   : {superuser_email}\npassword: {superuser_password}")

        student_email = "wlccpnas@gmail.com"
        student_password = "prince@123"
        student_first_name = "Prince"
        student_last_name = "Sachdeva"
        student_dob = date(1999, 2, 4)

        student1 = CustomUser.objects.create_user(email=student_email,
                                                  first_name=student_first_name,
                                                  last_name=student_last_name,
                                                  password=student_password,
                                                  date_of_birth=student_dob,
                                                  is_expert=False)

        print(f"Created student with \nemail   : {student_email}\npassword: {student_password}")

        student_email2 = "gaurav17288@iiitd.ac.in"
        student_password2 = "gaurav@123"
        student_first_name2 = "Gaurav"
        student_last_name2 = "Aggarwal"
        student_dob2 = date(1999, 3, 15)

        student2 = CustomUser.objects.create_user(email=student_email2,
                                                  first_name=student_first_name2,
                                                  last_name=student_last_name2,
                                                  password=student_password2,
                                                  date_of_birth=student_dob2,
                                                  is_expert=False)

        print(f"Created student with \nemail   : {student_email2}\npassword: {student_password2}")

        expert_email = "reeshabh17086@iiitd.ac.in"
        expert_password = "reeshabh@123"
        expert_first_name = "Reeshabh"
        expert_last_name = "Ranjan"
        expert_dob = date(1998, 12, 4)

        expert = CustomUser.objects.create_user(email=expert_email,
                                                first_name=expert_first_name,
                                                last_name=expert_last_name,
                                                password=expert_password,
                                                date_of_birth=expert_dob,
                                                is_expert=True)

        print(f"Created expert with \nemail   : {expert_email}\npassword: {expert_password}")

        superuser.verified = True
        superuser.save()

        student1.verified = True
        student1.save()

        student2.verified = True
        student2.save()

        expert.verified = True
        expert.save()
        expert.expert_profile.verified = True
        expert.expert_profile.save()

        print("Verified all the accounts.")

        interest_labels = ["Medicine", "Engineering", "Law", "Art", "Science"]
        specialisation_labels = ["Medicine", "Engineering", "Law", "Art", "Science"]

        for interest_label in interest_labels:
            Interest.objects.create(label=interest_label, description="")
        print(f"Created interests with labels: {interest_labels}")

        for specialisation_label in specialisation_labels:
            Specialisation.objects.create(label=specialisation_label, description="")
        print(f"Created specialisations with labels: {specialisation_labels}")

        current_site = Site.objects.get_current()
        current_site.domain = "127.0.0.1:8000"
        current_site.name = "127.0.0.1:8000"
        current_site.save()
        print(f"Set the current site as {current_site.domain}")

    else:
        print("Canceling operation")
