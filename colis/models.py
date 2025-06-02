# colis/models.py
from django.db import models
from django.contrib.auth import get_user_model

Utilisateur = get_user_model()

class Colis(models.Model):
    MODE_LIVRAISON_CHOICES = [
        ('express', 'Express'),
        ('standard', 'Standard'),
        ('economique', 'Économique'),
    ]

    STATUT_CHOICES = [
        ('en attente', 'En attente'),
        ('pris en charge', 'Pris en charge'),
        ('en transit', 'En transit'),
        ('livré', 'Livré'),
    ]

    expediteur = models.ForeignKey(Utilisateur, related_name='colis_envoyes', on_delete=models.CASCADE)
    destinataire = models.ForeignKey(Utilisateur, related_name='colis_recus', on_delete=models.CASCADE)
    dimensions = models.CharField(max_length=100, blank=True, null=True)
    poids = models.DecimalField(max_digits=10, decimal_places=2)
    type_marchandise = models.CharField(max_length=255, blank=True, null=True)
    adresse_depart = models.TextField()
    adresse_destination = models.TextField()
    mode_livraison = models.CharField(max_length=20, choices=MODE_LIVRAISON_CHOICES)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en attente')
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Colis {self.id} - {self.statut}"
