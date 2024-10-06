from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_client, name='login_client'),
    #path('creer-compte/', views.creer_compte, name='creer_compte'),
    path('accueil/', views.accueil_client, name='accueil_client'),
    path('', views.accueil, name='accueil'),
    path('ajouter-livre/', views.ajouter_livre, name='ajouter_livre'),
    path('modifier/<int:id>/', views.modifier_livre, name='modifier_livre'),
    path('supprimer/<int:id>/', views.supprimer_livre, name='supprimer_livre'),
    path('clients/', views.liste_client, name='liste_clients'),
    path('livres/', views.liste_livres, name='liste_livres'),
    path('commander/<int:livre_id>/', views.commande_livre, name='commande_livre'),
    path('liste_client/', views.liste_client, name='liste_client'),
    path('signup/', views.signup, name='signup'),
]
