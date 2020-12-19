import os

if __name__ == '__main__':
    confirm = input("Are you sure to continue? (y/n).")
    if confirm.lower() == "y":
        os.system('git push heroku release-heroku:master --force')
        confirm = input("Reset Heroku database? (y/n).")
        if confirm.lower() == "y":
            os.system("heroku pg:reset DATABASE")
        os.system("heroku run python manage.py migrate")
        print("Done!")
