# users/views.py
from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import Utilisateur
from .serializers import UtilisateurSerializer, EmailAuthTokenSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UtilisateurListCreate(generics.ListCreateAPIView):
    queryset = Utilisateur.objects.all()
    serializer_class = UtilisateurSerializer

class UtilisateurRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Utilisateur.objects.all()
    serializer_class = UtilisateurSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Ajouter les champs personnalisés
        token['email'] = user.email
        token['role'] = user.role
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        utilisateur = self.user
        data['user'] = {
            'id': utilisateur.id,
            'email': utilisateur.email,
            'role': utilisateur.role,
        }
        # Ajouter profil livreur si applicable
        if utilisateur.role == 'client' and hasattr(utilisateur, 'livreur_profile'):
            livreur = utilisateur.livreur_profile
            data['livreur'] = {
                'type_vehicule': livreur.type_vehicule,
                'statut': livreur.statut,
                'disponibilite': livreur.disponibilite,
            }
        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
        
class UtilisateurLoginView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]

class UtilisateurRefreshView(TokenRefreshView):
    permission_classes = [permissions.AllowAny]

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_user_info(request):
    serializer = UtilisateurSerializer(request.user)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_user_role(request, user_id):
    try:
        utilisateur = Utilisateur.objects.get(id=user_id)
        if utilisateur.role == 'livreur':
            return Response({"message": "L'utilisateur est un livreur."})
        else:
            return Response({"message": f"L'utilisateur a le rôle {utilisateur.role}."})
    except Utilisateur.DoesNotExist:
        return Response({"error": "Utilisateur non trouvé."}, status=404)