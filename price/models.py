from django.db import models

class Paiement(models.Model):
    MODE_PAIEMENT_CHOICES = [
        ('carte bancaire', 'Carte Bancaire'),
        ('PayPal', 'PayPal'),
        ('portefeuille électronique', 'Portefeuille Électronique'),
        ('Mobile Money', 'Mobile Money'),
    ]
    livraison = models.ForeignKey('delivery.Livraison', on_delete=models.CASCADE)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    mode_paiement = models.CharField(max_length=25, choices=MODE_PAIEMENT_CHOICES)
    date_paiement = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Paiement {self.id} pour la livraison {self.livraison_id}"
