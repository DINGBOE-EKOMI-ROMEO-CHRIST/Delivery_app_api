from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone
from users.models import Utilisateur
from django.core.exceptions import ValidationError

def validate_vehicle_type(value):
    valid_types = ['Moto', 'Voiture', 'Camion']
    if value not in valid_types:
        raise ValidationError(f"{value} n'est pas un type de véhicule valide.")

class Livreur(models.Model):
    STATUT_CHOICES = [
        ('actif', 'Actif'),
        ('bloqué', 'Bloqué'),
        ('en révision', 'En révision'),
    ]

    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE, related_name='livreur_profile', unique=True)
    type_vehicule = models.CharField(max_length=50, default='Moto', validators=[validate_vehicle_type])
    immatriculation_moto = models.CharField(
        max_length=50,
        unique=True,
        validators=[RegexValidator(
            regex='^[A-Z0-9-]+$',
            message='Le numéro d\'immatriculation doit contenir uniquement des lettres majuscules, des chiffres et des tirets.'
        )]
    )
    photo_moto = models.ImageField(upload_to='photos_motos/', blank=True, null=True)
    photo_livreur = models.ImageField(upload_to='photos_livreurs/', blank=True, null=True)
    statut_livreur = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en révision')
    date_creation = models.DateTimeField(default=timezone.now)

    def clean(self):
        super().clean()
        # Ajoutez ici d'autres validations personnalisées si nécessaire

    def __str__(self):
        return f"{self.utilisateur.email} - {self.immatriculation_moto}"
