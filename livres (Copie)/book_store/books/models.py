from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.nom
class Livre(models.Model):
    titre = models.CharField(max_length=200)
    auteur = models.CharField(max_length=200)
    prix = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.titre

class Commande(models.Model):
    livre = models.ForeignKey(Livre, on_delete=models.CASCADE)
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    email_client = models.EmailField()
    prix = models.DecimalField(max_digits=6, decimal_places=2)
    date_commande = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commande de {self.client.email} pour {self.livre.titre}"