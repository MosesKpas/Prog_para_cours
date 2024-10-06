from django.http import HttpResponse
from django.core.mail import send_mail

def simple_mail(request):

    send_mail(subject='C est le sujet',
        message='C est le corps du message',
        from_email='hi@demomailtrap.com',
        recipient_list=['moisekapend80@gmail.com'])

    return HttpResponse()
