from django.urls import path
from . import views
from django.urls import path
from .views import liste_client, login_client
from .views import login_client, creer_compte
from .views import login_client, creer_compte, accueil_client
from .views import commande_livre

urlpatterns = [
 path('login/', login_client, name='login_client'),
    path('creer-compte/', creer_compte, name='creer_compte'),
    path('accueil/', accueil_client, name='accueil_client'),
    path('', views.accueil, name='accueil'),  # Route pour la page d'accueil
     path('ajouter-livre/', views.ajouter_livre, name='ajouter_livre'),
    path('modifier/<int:id>/', views.modifier_livre, name='modifier_livre'),  # Route pour modifier un livre
    path('supprimer/<int:id>/', views.supprimer_livre, name='supprimer_livre'),  # Route pour supprimer un livre
    path('clients/', views.liste_clients, name='liste_clients'),  # Route pour voir les clients
    path('livres/', views.liste_livres, name='liste_livres'),  # Route pour voir la liste des livres
    path('commander/<int:livre_id>/', commande_livre, name='commande_livre'),
    path('liste_client/', liste_client, name='liste_client'),
    

]

