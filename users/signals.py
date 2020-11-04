from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import CustomUser


@receiver(post_save, sender=get_user_model())
def send_verification_email(sender, instance: CustomUser, created=False, **kwargs):
    user = instance
    if created:
        email_verification_link = f'http://localhost:8000/verify/?email={user.email}&email_verification_token={user.email_verification_token}'
        send_mail('CareerShala Account Email Verification', email_verification_link, 'noreply@careershala.com',
                  [user.email])
