from django.shortcuts import render, redirect, get_object_or_404
from .models import Livre, Client
from .forms import LivreForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Commande, Livre
from django.shortcuts import render
from django.contrib.auth.models import User

def liste_client(request):
    clients = User.objects.all()
    commandes = Commande.objects.select_related('livre', 'client').all()
    context = {
        'clients': clients,
        'commandes': commandes
    }
    return render(request, 'books/liste_clients.html', context)

def liste_clients(request):
    clients = User.objects.all()  # Récupère tous les clients
    commandes = Commande.objects.all()  # Récupère toutes les commandes
    return render(request, 'books/liste_clients.html', {'clients': clients, 'commandes': commandes})
from .models import Livre, Commande
@login_required
def commande_livre(request, livre_id):
    livre = Livre.objects.get(id=livre_id)
    
    if request.method == 'POST':
        # Créer la commande
        commande = Commande(
            livre=livre,
            client=request.user,
            email_client=request.user.email,
            prix=livre.prix
        )
        commande.save()

        # Ajouter un message de succès
        messages.success(request, "Votre commande a été passée avec succès !")

        return redirect('commande_livre', livre_id=livre_id)  # Rediriger après la soumission pour afficher le message

    return render(request, 'books/commande_livre.html', {'livre': livre})

def accueil_client(request):
    livres = Livre.objects.all()  # Récupère tous les livres
    return render(request, 'books/accueil_client.html', {'livres': livres})

def creer_compte(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        # Créer un nouvel utilisateur
        user = User.objects.create_user(username=email, email=email, password=password)
        messages.success(request, "Votre compte a été créé avec succès.")
        return redirect('login_client')  # Redirigez vers la page de connexion
    return render(request, 'books/creer_compte.html')
def login_client(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('accueil_client')  # Redirigez vers la liste des livres après connexion
        else:
            # Gérer l'échec de la connexion
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

# def liste_clients(request):
#     clients = Client.objects.all()
#     return render(request, 'books/liste_clients.html', {'clients': clients})


