# users/views.py
from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from .models import Utilisateur
from django.http import HttpResponse
from otp.models import OTP
from livreurs.models import Livreur
from .serializers import UtilisateurSerializer, EmailAuthTokenSerializer, LocationUpdateSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from otp.utils import generate_otp, send_otp_email

class UtilisateurListCreate(generics.ListCreateAPIView):
    queryset = Utilisateur.objects.all()
    serializer_class = UtilisateurSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(is_active=False)  # Désactive le compte jusqu'à vérification OTP

        # Génère et envoie l'OTP
        otp = generate_otp()
        send_otp_email(user.email, otp)
        OTP.objects.create(user=user, code=otp)

        headers = self.get_success_headers(serializer.data)
        return Response(
            {"message": "Compte créé, veuillez entrer l'OTP envoyé par email.", "user_id": user.id},
            status=status.HTTP_201_CREATED,
            headers=headers
        )

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


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_location(request):
    user = request.user
    serializer = LocationUpdateSerializer(user, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_location(request):
    user = request.user

    if user.role == 'livreur':
        try:
            livreur = user.livreur_profile
            data = {
                'latitude': user.latitude,
                'longitude': user.longitude,
                'livreur_info': {
                    'type_vehicule': livreur.type_vehicule,
                    'statut': livreur.statut
                }
            }
        except Livreur.DoesNotExist:
            return Response({'error': 'Livreur profile not found.'}, status=status.HTTP_404_NOT_FOUND)
    else:
        data = {
            'latitude': user.latitude,
            'longitude': user.longitude
        }

    return Response(data)



def salut(request):
    return HttpResponse("Salut !")