from rest_framework import serializers
from .models import Livraison

class LivraisonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Livraison
        fields = [
            'id',
            'demande',
            'livreur',
            'date_prise_en_charge',
            'longitude_depart',
            'latitude_depart',
            'longitude_arrivee',
            'latitude_arrivee',
            'numero_depart',
            'numero_arrivee',
            'date_livraison',
            'statut'
        ]
