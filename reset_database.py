"""
WARNING:    THIS WILL DELETE ALL MIGRATION FILES AND THE SQLITE DATABASE.
            To be used as a utility script.
            No main function so that user doesn't delete files by mistake.
"""
import os
from datetime import date
from glob import glob

from users.models import CustomUser, Interest, Specialisation


def reset():
    confirm = input("Are you sure to continue? (y/n)")
    if confirm.lower() == "y":
        for file in glob('*/migrations/000*.py'):
            print("removing", str(file))
            os.remove(file)

        db_path = "db.sqlite3"
        print("removing", db_path)
        os.remove(db_path)

        print("Initiating database...")
        os.system("python manage.py makemigrations")
        os.system("python manage.py migrate")

        superuser_email = "reeshabhkumarranjan@gmail.com"
        superuser_password = "reeshabh@123"
        superuser_first_name = "Reeshabh"
        superuser_last_name = "Admin"
        superuser_dob = date(1998, 12, 4)
        print(f"Creating superuser with \nemail   : {superuser_email}\npassword: {superuser_password}")

        CustomUser.objects.create_superuser(email=superuser_email,
                                            first_name=superuser_first_name,
                                            last_name=superuser_last_name,
                                            password=superuser_password,
                                            date_of_birth=superuser_dob)

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
