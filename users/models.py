# votre_application/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from entreprises.models import Entreprise

class Utilisateur(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('client', 'Client'),
        ('livreur', 'Livreur'),
    ]

    username = None  # Supprimez le champ username
    email = models.EmailField(_('email address'), unique=True)  # Redéfinissez le champ email pour le rendre unique
    telephone = models.CharField(max_length=20, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    entreprise = models.ForeignKey(Entreprise, on_delete=models.SET_NULL, null=True, blank=True)
    localisation = models.TextField(blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
