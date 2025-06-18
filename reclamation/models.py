# models.py
from django.db import models
from demande.models import Demande  # Assurez-vous que le chemin d'importation est correct

class Reclamation(models.Model):
    demande = models.ForeignKey(Demande, on_delete=models.CASCADE)
    description = models.TextField()
    statut_choices = [
        ('en attente', 'En attente'),
        ('résolu', 'Résolu'),
        ('refusé', 'Refusé'),
    ]
    statut = models.CharField(max_length=20, choices=statut_choices, default='en attente')
    date_reclamation = models.DateTimeField(auto_now_add=True)

class Retour(models.Model):
    demande = models.ForeignKey(Demande, on_delete=models.CASCADE)
    motif = models.TextField()
    statut_choices = [
        ('en cours', 'En cours'),
        ('terminé', 'Terminé'),
    ]
    statut = models.CharField(max_length=20, choices=statut_choices, default='en cours')
    date_retour = models.DateTimeField(auto_now_add=True)
