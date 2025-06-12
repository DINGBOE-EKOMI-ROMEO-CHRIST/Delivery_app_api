from rest_framework import serializers
from .models import Demande

class DemandeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Demande
        fields = ['id', 'utilisateur', 'nature_colis', 'dimensions', 'poids', 'photo_colis','mode_livraison', 'statut_demande']

class DemandeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Demande
        fields = ['id', 'utilisateur', 'nature_colis', 'dimensions', 'poids', 'photo_colis','mode_livraison', 'statut_demande']
