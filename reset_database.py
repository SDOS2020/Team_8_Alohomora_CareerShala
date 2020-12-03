"""
WARNING:    THIS WILL DELETE ALL MIGRATION FILES AND THE SQLITE DATABASE.
            To be used as a utility script.
            No main function so that user doesn't delete files by mistake.
"""
import json
import os
from datetime import date
from glob import glob
from urllib.parse import urlparse

import psycopg2

from questionnaire.models import Questionnaire, Question, Option
from users.models import CustomUser, Interest, Specialisation


def reset():
    confirm = input("Are you sure to continue? (y/n). Select 'n' if you are doing this on Heroku!")
    if confirm.lower() == "y":
        for file in glob('*/migrations/000*.py'):
            print("removing", str(file))
            os.remove(file)

        print("Resetting database...")
        os.system("python manage.py reset_db --noinput")
        os.system("python manage.py makemigrations")
        os.system("python manage.py migrate")

        questionnaires_json_file_name = 'questionnaires.json'
        with open(questionnaires_json_file_name) as f:
            root_questionnaire_json = json.load(f)
            load_questionnaire_from_json(root_questionnaire_json, None)

        print(f"Created questionnaires from file {questionnaires_json_file_name}")

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
        expert_password = "reesh@123"
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

        print("Verified all the accounts.")

        interest_labels = ["Medicine", "Engineering", "Law", "Art", "Science"]
        specialisation_labels = ["Medicine", "Engineering", "Law", "Art", "Science"]

        for interest_label in interest_labels:
            Interest.objects.create(label=interest_label, description="")
        print(f"Created interests with labels: {interest_labels}")

        for specialisation_label in specialisation_labels:
            Specialisation.objects.create(label=specialisation_label, description="")
        print(f"Created specialisations with labels: {specialisation_labels}")

    else:
        print("Canceling operation")


def load_option_from_json(option_json, from_question):
    option = Option.objects.create(body=option_json["body"], question=from_question)
    option.save()
    if option_json["continuation_questionnaire"] is not None:
        questionnaire_json = option_json["continuation_questionnaire"]
        load_questionnaire_from_json(questionnaire_json, option)


def load_question_from_json(question_json, from_questionnaire: Questionnaire):
    question = Question.objects.create(body=question_json["body"], multiselect=question_json["multiselect"],
                                       questionnaire=from_questionnaire)
    question.save()
    for option_json in question_json["option"]:
        load_option_from_json(option_json, question)


def load_questionnaire_from_json(questionnaire_json, from_option: Option):
    questionnaire = Questionnaire.objects.create(name=questionnaire_json["name"], root=questionnaire_json["root"])
    if from_option is not None:
        from_option.continuation_questionnaire = questionnaire
        from_option.save()
    for question_json in questionnaire_json["question"]:
        load_question_from_json(question_json, questionnaire)
