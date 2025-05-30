# livreurs/models.py
from django.db import models
from users.models import Utilisateur
from django.utils import timezone

class Livreur(models.Model):
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE, related_name='livreur_profile')
    type_vehicule = models.CharField(max_length=50, default='Moto')
    numero_immatriculation = models.CharField(max_length=50)
    photo_moto = models.TextField(blank=True, null=True)
    photo_livreur = models.TextField(blank=True, null=True)
    disponibilite = models.BooleanField(default=True)
    nombre_livraisons = models.IntegerField(default=0)
    statut = models.CharField(max_length=20, default='en attente')
    date_creation = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.utilisateur.email} - {self.numero_immatriculation}"
