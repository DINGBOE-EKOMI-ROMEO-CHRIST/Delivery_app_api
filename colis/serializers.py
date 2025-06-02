# colis/serializers.py
from rest_framework import serializers
from .models import Colis

class ColisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Colis
        fields = ['expediteur', 'destinataire', 'dimensions', 'poids', 'type_marchandise', 'adresse_depart', 'adresse_destination', 'mode_livraison']

class Colislist(serializers.ModelSerializer):
    class Meta:
        model = Colis
        fields = ['id','expediteur', 'destinataire', 'dimensions', 'poids', 'type_marchandise', 'adresse_depart', 'adresse_destination', 'mode_livraison']
