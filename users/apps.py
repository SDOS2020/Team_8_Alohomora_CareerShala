from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):
        import users.signals  # make sure IDE doesn't replace this whole line with "pass" to optimise imports
