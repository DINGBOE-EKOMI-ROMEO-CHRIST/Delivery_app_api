# livreurs/serializers.py
from rest_framework import serializers
from .models import Livreur

class LivreurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Livreur
        fields = ['type_vehicule', 'numero_immatriculation', 'photo_moto', 'photo_livreur', 'disponibilite', 'nombre_livraisons', 'statut']

class LivreurListSerializer(serializers.ModelSerializer):
    utilisateur_id = serializers.IntegerField(source='utilisateur.id', read_only=True)
    utilisateur_nom = serializers.CharField(source='utilisateur.get_full_name', read_only=True)
    utilisateur_email = serializers.EmailField(source='utilisateur.email', read_only=True)

    class Meta:
        model = Livreur
        fields = [
            'id', 'utilisateur_id', 'utilisateur_nom', 'utilisateur_email',
            'type_vehicule', 'numero_immatriculation', 'photo_moto',
            'photo_livreur', 'disponibilite', 'nombre_livraisons', 'statut'
        ]
