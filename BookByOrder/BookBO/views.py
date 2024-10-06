from django.shortcuts import render
from datetime import datetime
from BookBO.utils import envoyer_mail

# Créer un compte pour tester l'envoi des mails
def create_view(request, *args, **kwargs):
    cxt = {}
    if request.method == "POST":
        email = request.POST.get('email')

        sujet = "Django_Projet"  # Correction du nom de variable
        template = 'email.html'
        context = {
            'date': datetime.today().date(),  # Correction pour obtenir la date
            'email': email
        }

        receivers = [email]

        envoyer = envoyer_mail(
            sujet=sujet,  # Correction du nom de variable
            receveurs=receivers,
            email_expediteur="moisekapend80@gmail.com",
            template=template,
            context=context
        )

        if envoyer:
            cxt = {"msg": "Mail envoyé avec succès."}
        else:
            cxt = {'msg': 'Envoi de l\'email échoué.'}

    return render(request, 'index.html', cxt)
