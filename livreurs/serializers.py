from rest_framework import serializers
from .models import Livreur

class LivreurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Livreur
        fields = [
            'type_vehicule',
            'immatriculation_moto',
            'photo_moto',
            'photo_livreur',
            'statut_livreur'
        ]

class LivreurListSerializer(serializers.ModelSerializer):
    utilisateur_id = serializers.IntegerField(source='utilisateur.id', read_only=True)
    utilisateur_email = serializers.EmailField(source='utilisateur.email', read_only=True)
    utilisateur_telephone = serializers.CharField(source='utilisateur.telephone', read_only=True)
    utilisateur_role = serializers.CharField(source='utilisateur.role', read_only=True)

    class Meta:
        model = Livreur
        fields = [
            'id',
            'utilisateur_id',
            'utilisateur_email',
            'utilisateur_telephone',
            'utilisateur_role',
            'type_vehicule',
            'immatriculation_moto',
            'photo_moto',
            'photo_livreur',
            'statut_livreur'
        ]

class LivreurDetailSerializer(serializers.ModelSerializer):
    utilisateur_id = serializers.IntegerField(source='utilisateur.id', read_only=True)
    utilisateur_email = serializers.EmailField(source='utilisateur.email', read_only=True)
    utilisateur_telephone = serializers.CharField(source='utilisateur.telephone', read_only=True)
    utilisateur_role = serializers.CharField(source='utilisateur.role', read_only=True)
    utilisateur_date_inscription = serializers.DateTimeField(source='utilisateur.date_inscription', read_only=True)

    class Meta:
        model = Livreur
        fields = [
            'id',
            'utilisateur_id',
            'utilisateur_email',
            'utilisateur_telephone',
            'utilisateur_role',
            'utilisateur_date_inscription',
            'type_vehicule',
            'immatriculation_moto',
            'photo_moto',
            'photo_livreur',
            'statut_livreur',
            'date_creation'
        ]
