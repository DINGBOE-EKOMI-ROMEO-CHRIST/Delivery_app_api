# serializers.py
from rest_framework import serializers
from .models import Reclamation,Retour

class ReclamationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reclamation
        fields = '__all__'

class RetourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Retour
        fields = '__all__'