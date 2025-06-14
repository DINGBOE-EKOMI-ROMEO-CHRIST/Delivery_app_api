from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.validators import RegexValidator

# Validateur personnalisé pour l'email
def validate_custom_email(value):
    email_validator = RegexValidator(
        regex=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
        message='Entrez une adresse email valide.'
    )
    email_validator(value)

# Validateur personnalisé pour le numéro de téléphone
def validate_phone_number(value):
    phone_validator = RegexValidator(
        regex=r'^01[0-9]{8}$',
        message='Le numéro de téléphone doit commencer par 01 et contenir exactement 10 chiffres.'
    )
    phone_validator(value)

class Utilisateur(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('client', 'Client'),
        ('livreur', 'Livreur'),
    ]

    # Supprimer le champ username hérité d'AbstractUser
    username = None

    # Champs de base
    email = models.EmailField(
        unique=True,
        validators=[validate_custom_email]
    )

    telephone = models.CharField(
        max_length=10,  # 10 chiffres au total
        unique=True,
        validators=[validate_phone_number]
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='client'
    )

    points_fidelite = models.IntegerField(default=0)
    site_id = models.IntegerField(null=True, blank=True)
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
