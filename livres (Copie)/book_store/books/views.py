from datetime import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .models import Livre, Client, Commande
from .forms import LivreForm, SignupForm
from books.utils import envoyer_mail

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            if User.objects.filter(username=email).exists():
                return render(request, 'books/signup.html', {'form': form, 'error': 'Cet email est déjà utilisé.'})

            user = User(username=email, email=email)
            user.set_password(password)
            user.save()
            bienvenue_mail(request)
            return redirect('login_client')
    else:
        form = SignupForm()
    return render(request, 'books/signup.html', {'form': form})

def liste_client(request):
    clients = User.objects.all()
    commandes = Commande.objects.select_related('livre', 'client').all()
    context = {
        'clients': clients,
        'commandes': commandes
    }
    return render(request, 'books/liste_clients.html', context)

@login_required
def commande_livre(request, livre_id):
    livre = get_object_or_404(Livre, id=livre_id)

    if request.method == 'POST':
        commande = Commande(
            livre=livre,
            client=request.user,
            email_client=request.user.email,
            prix=livre.prix
        )
        commande.save()
        commande_mail(request, commande)
        messages.success(request, "Votre commande a été passée avec succès !")
        return redirect('commande_livre', livre_id=livre_id)

    return render(request, 'books/commande_livre.html', {'livre': livre})

def accueil_client(request):
    livres = Livre.objects.all()
    return render(request, 'books/accueil_client.html', {'livres': livres})

def login_client(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        if email=='admin@gmail.com' and password =='admin':
            return redirect('liste_livres')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('accueil_client')
        else:
            error_message = "Identifiants invalides. Veuillez réessayer."
            return render(request, 'books/login_client.html', {'error_message': error_message})

    return render(request, 'books/login_client.html')

def accueil(request):
    return render(request, 'books/accueil.html')

def liste_livres(request):
    livres = Livre.objects.all()
    return render(request, 'books/liste_livre.html', {'livres': livres})

def ajouter_livre(request):
    if request.method == 'POST':
        form = LivreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_livres')
    else:
        form = LivreForm()
    return render(request, 'books/ajouter_livre.html', {'form': form})

def modifier_livre(request, id):
    livre = get_object_or_404(Livre, id=id)
    if request.method == 'POST':
        form = LivreForm(request.POST, instance=livre)
        if form.is_valid():
            form.save()
            return redirect('liste_livres')
    else:
        form = LivreForm(instance=livre)
    return render(request, 'books/modifier_livre.html', {'form': form})

def supprimer_livre(request, id):
    livre = get_object_or_404(Livre, id=id)
    livre.delete()
    return redirect('liste_livres')

def bienvenue_mail(request, *args, **kwargs):
    if request.method == "POST":
        email = request.POST.get('email')

        sujet = "LIBRAIRIE"
        template = 'books/bienvenue_email.html'
        context = {
            'date': datetime.today().date(),
            'email': email
        }

        receivers = [email]
        envoyer = envoyer_mail(
            sujet=sujet,
            receveurs=receivers,
            email_expediteur="Force.oneLib@gmail.com",
            template=template,
            context=context
        )
        if envoyer:
            messages.success(request, "Email de bienvenue envoyé avec succès.")
            return redirect('login_client')
        else:
            messages.error(request, "Échec de l'envoi de l'email de bienvenue.")
    return render(request, 'books/login_client.html')

def commande_mail(request, commande):
    email = commande.email_client
    sujet = "LIBRAIRIE"
    template = 'books/commande_email.html'
    context = {
        'date': datetime.today().date(),
        'email': email,
        'livre': commande.livre.titre,
        'prix': commande.prix
    }

    receivers = [email]
    envoyer = envoyer_mail(
        sujet=sujet,
        receveurs=receivers,
        email_expediteur="FORCE.oneLib@gmail.com",
        template=template,
        context=context
    )
    if envoyer:
        messages.success(request, "Commande réussie.")
    else:
        messages.error(request, "Échec de la commande.")
