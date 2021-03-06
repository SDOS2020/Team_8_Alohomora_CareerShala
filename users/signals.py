import logging

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from questionnaire.models import Questionnaire
from users.methods import send_mail_async
from users.models import CustomUser, ExpertProfile, StudentProfile


@receiver(post_save, sender=CustomUser)
def send_verification_email(sender, instance: CustomUser, created=False,
                            **kwargs):  # TODO send email on background thread
    user = instance
    if created:
        if settings.PRODUCTION_SERVER:
            server_base_url = settings.PRODUCTION_SERVER_URL
        else:
            server_base_url = "http://127.0.0.1:8000"
        email_verification_link = f'{server_base_url}/users/verify/?email={user.email}&email_verification_token={user.email_verification_token}'
        sender = 'sdosg8dev@gmail.com'
        receivers = [user.email]
        subject = 'CareerShala Account Email Verification'
        dynamic_template_data = {'email_verification_url': email_verification_link}
        template_id = 'd-c5740219251a4be390c34e9386f1e4b8'  # TODO move this into environment variables
        logger = logging.getLogger('app.email.verification')
        logger.info(f'Sending verification email to {receivers} (sender={sender})')
        send_mail_async(sender=sender,
                        receivers=receivers,
                        subject=subject,
                        dynamic_template_data=dynamic_template_data,
                        template_id=template_id)


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance: CustomUser, created=False, **kwargs):
    if created and not instance.is_admin:
        logger = logging.getLogger('app.accounts.register')
        if instance.is_expert:
            ExpertProfile.objects.create(user=instance)
            logger.info(f'Created expert-user with email {instance.email}')
        else:
            root_questionnaire = Questionnaire.objects.get(root=True)
            StudentProfile.objects.create(user=instance, next_questionnaire=root_questionnaire)
            logger.info(f'Created student-user with email {instance.email}')


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance: CustomUser, created=False, **kwargs):
    if not instance.is_admin:
        if instance.is_expert:
            instance.expert_profile.save()
        else:
            instance.student_profile.save()
