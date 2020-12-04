import os

if __name__ == '__main__':
    confirm = input("Are you sure to continue? (y/n).")
    if confirm.lower() == "y":
        for directory in os.listdir():
            if "venv" not in directory:
                os.system(f"git add --force {directory}/migrations/*.py$")
        os.system('git commit -am "Add migrations"')
        os.system('git push heroku release-heroku:master --force')
        os.system('git rm --cached */migrations/*.py')
        os.system('git reset --hard HEAD~1')
        print("Done!")
