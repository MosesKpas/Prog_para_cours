import logging
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail

logger = logging.getLogger(__name__)

#fonction pour envoyer des mails 
def envoyer_mail(sujet:str, receveurs:list, template:str,context:dict,email_expediteur:str):
    try:
        message = render_to_string(template,context)
        send_mail(
            sujet,
            message,
            email_expediteur,
            receveurs,
            fail_silently=True,
            html_message=message
        )
        return True
        
    except Exception as e:
        logger.error(e)
    return False