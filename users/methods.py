import threading

from django.core.mail import send_mail
from django.utils.crypto import get_random_string


def generate_token():
    return get_random_string(length=32)


def send_mail_async(sender: str, receivers, subject, body):
    t = threading.Thread(target=send_mail, args=(subject, body, sender, receivers))
    t.setDaemon(True)
    t.start()
