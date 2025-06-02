# utilisateurs/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class Utilisateur(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('client', 'Client'),
        ('livreur', 'Livreur'),
    ]

    # Supprimer le champ username hérité d'AbstractUser
    username = None

    # Champs de base
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=20, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    secret_code = models.CharField(max_length=10, null=True, blank=True)
    points_fidelite = models.IntegerField(default=0)
    entreprise = models.ForeignKey('entreprises.Entreprise', on_delete=models.SET_NULL, null=True, blank=True)

    # Champ pour la date d'inscription
    date_inscription = models.DateTimeField(default=timezone.now)

    # Utiliser l'email comme identifiant unique pour l'authentification
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # Redéfinir les relations inverses pour éviter les conflits
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='utilisateur_groups',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='utilisateur_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.email
