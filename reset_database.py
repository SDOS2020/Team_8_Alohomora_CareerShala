"""
WARNING:    THIS WILL DELETE ALL MIGRATION FILES AND THE SQLITE DATABASE.
            To be used as a utility script.
            No main function so that user doesn't delete files by mistake.
"""
import os
from datetime import date
from glob import glob

from questionnaire.models import Questionnaire, Question, Option
from users.models import CustomUser, Interest, Specialisation


def reset():
    confirm = input("Are you sure to continue? (y/n)")
    if confirm.lower() == "y":
        for file in glob('*/migrations/000*.py'):
            print("removing", str(file))
            os.remove(file)

        db_path = "db.sqlite3"
        if os.path.isfile(db_path):
            print("removing", db_path)
            os.remove(db_path)

        print("Initiating database...")
        os.system("python manage.py makemigrations")
        os.system("python manage.py migrate")

        root_questionnaire_name = "Root questionnaire"
        question_one_name = "Aap Alohomora ke CareerShala se kya chahte ho?"
        option_one_name = "Mujhe apne interest/ talent se jude career opportunities ke baare mein janna hain"
        option_two_name = "Main apne career ko lekar confused hoon aur mujhe seekhna hain ki mere liye kya sahi career option ho sakti hain"
        option_three_name = "Mujhe turant hi job lekar apne family ko support karna hain"

        questionnaire = Questionnaire.objects.create(name=root_questionnaire_name, root=True)
        question1 = Question.objects.create(body=question_one_name, questionnaire=questionnaire)
        option1 = Option.objects.create(body=option_one_name, question=question1)
        option2 = Option.objects.create(body=option_two_name, question=question1)
        option3 = Option.objects.create(body=option_three_name, question=question1)
        print(f"Created a root questionnaire with name: {root_questionnaire_name}")

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
