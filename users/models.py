from django.db import models
from django.contrib.auth.models import AbstractUser
from entreprises.models import Entreprise


class Utilisateur(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('client', 'Client'),
        ('livreur', 'Livreur'),
    ]

    telephone = models.CharField(max_length=20, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    entreprise = models.ForeignKey(Entreprise, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.username
