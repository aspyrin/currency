from celery import shared_task
from settings import settings
from django.core.mail import send_mail
from time import sleep


@shared_task
def slow_func():
    print('START')
    sleep(10)
    print('END')


@shared_task
def send_contact_us_email(subject, email_from):
    email_subject = 'ContactUs From Currency Project'
    body = f"""
    Subject From Client: {subject}
    Email: {email_from}
    Wants to contact
    """
    sleep(10)
    send_mail(
        subject,
        body,
        settings.EMAIL_HOST_USER,
        [settings.EMAIL_HOST_USER],
        fail_silently=False,
    )
