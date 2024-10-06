# books/tasks.py

from celery import shared_task
from django.core.mail import send_mail

@shared_task
def envoyer_email(sujet, message, destinataires):
    send_mail(sujet, message, 'FORCE.oneLib@gmail.com', destinataires)
