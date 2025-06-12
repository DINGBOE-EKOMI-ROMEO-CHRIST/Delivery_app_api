# models.py
from django.db import models
from django.contrib.auth import get_user_model

Utilisateur = get_user_model()

class Demande(models.Model):
    MODE_LIVRAISON_CHOICES = [
        ('express', 'Express'),
        ('standard', 'Standard'),
        ('economique', 'Économique'),
    ]

    STATUT_DEMANDE_CHOICES = [
        ('en attente', 'En attente'),
        ('pris en charge', 'Pris en charge'),
        ('en transit', 'En transit'),
        ('livré', 'Livré'),
    ]

    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    nature_colis = models.CharField(max_length=255, blank=True, null=True)
    dimensions = models.CharField(max_length=100, blank=True, null=True)
    poids = models.DecimalField(max_digits=10, decimal_places=2)
    photo_colis = models.ImageField(upload_to='photos_colis/')
    mode_livraison = models.CharField(max_length=20, choices=MODE_LIVRAISON_CHOICES)
    statut_demande = models.CharField(max_length=20, choices=STATUT_DEMANDE_CHOICES, default='en attente')
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Demande {self.id} - {self.statut_demande}"

class Livraison(models.Model):
    demande = models.OneToOneField(Demande, on_delete=models.CASCADE, related_name='livraison_demande')
    # autres champs de livraison

    def __str__(self):
        return f"Livraison {self.id}"
