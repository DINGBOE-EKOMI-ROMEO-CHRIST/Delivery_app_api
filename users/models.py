# utilisateurs/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class Utilisateur(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('client', 'Client'),
        ('livreur', 'Livreur'),
    ]

    username = None
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=20, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    entreprise = models.ForeignKey('entreprises.Entreprise', on_delete=models.SET_NULL, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # Spécifier des noms de relations inverses uniques
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='utilisateur_groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
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
