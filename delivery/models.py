from django.db import models
from django.core.exceptions import ValidationError
from demande.models import Demande
class Livraison(models.Model):
    STATUT_CHOICES = [
        ('en attente', 'En attente'),
        ('en cours', 'En cours'),
        ('livré', 'Livré'),
        ('annulé', 'Annulé'),
    ]

    id = models.AutoField(primary_key=True)
    demande = models.OneToOneField(Demande, on_delete=models.CASCADE, related_name='livraison_delivery')
    livreur = models.ForeignKey('livreurs.Livreur', on_delete=models.CASCADE,null=True)
    date_prise_en_charge = models.DateTimeField(auto_now_add=True)
    longitude_depart = models.DecimalField(max_digits=10, decimal_places=8)
    latitude_depart = models.DecimalField(max_digits=11, decimal_places=8)
    longitude_arrivee = models.DecimalField(max_digits=10, decimal_places=8)
    latitude_arrivee = models.DecimalField(max_digits=11, decimal_places=8)
    numero_depart = models.IntegerField()
    numero_arrivee = models.IntegerField()
    date_livraison = models.DateTimeField(null=True, blank=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en attente')

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=~models.Q(latitude_depart=models.F('latitude_arrivee')) | ~models.Q(longitude_depart=models.F('longitude_arrivee')),
                name='check_lat_long_distinct'
            )
        ]

    def clean(self):
        super().clean()
        if self.longitude_depart == self.longitude_arrivee and self.latitude_depart == self.latitude_arrivee:
            raise ValidationError("Les coordonnées de départ et d'arrivée ne peuvent pas être identiques.")

    def __str__(self):
        return f"Livraison {self.id} - Statut: {self.statut}"
