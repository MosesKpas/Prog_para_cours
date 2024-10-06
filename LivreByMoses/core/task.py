from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_welcome_email(user_email):
    subject = 'Welcome to LivreByMoses'
    message = 'Thank you for registering with us!'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user_email]
    send_mail(subject, message, email_from, recipient_list)

@shared_task
def send_order_notification(user_email, book_title):
    subject = 'Order Confirmation'
    message = f'Your order for the book "{book_title}" has been received.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user_email]
    send_mail(subject, message, email_from, recipient_list)
