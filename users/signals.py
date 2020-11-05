from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from users.methods import send_mail_async
from users.models import CustomUser


@receiver(post_save, sender=CustomUser)
def send_verification_email(sender, instance: CustomUser, created=False,
                            **kwargs):  # TODO send email on background thread
    user = instance
    if created:
        email_verification_link = f'http://localhost:8000/users/verify/?email={user.email}&email_verification_token={user.email_verification_token}'
        sender = 'noreply@careershala.com'
        receivers = [user.email]
        subject = 'CareerShala Account Email Verification'
        body = email_verification_link

        send_mail_async(sender=sender,
                        receivers=receivers,
                        subject=subject,
                        body=body)
