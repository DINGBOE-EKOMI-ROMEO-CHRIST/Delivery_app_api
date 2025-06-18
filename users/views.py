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
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from reclamation.models import Reclamation,Retour
from django.contrib import messages
import logging

logger = logging.getLogger(__name__)

class UtilisateurListCreate(generics.ListCreateAPIView):
    queryset = Utilisateur.objects.all()
    serializer_class = UtilisateurSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Récupérez le rôle de l'utilisateur à partir des données de la requête
        role = serializer.validated_data.get('role', '')

        # Créez l'utilisateur avec is_active=False par défaut
        user = serializer.save(is_active=False)

        # Si le rôle est admin, définissez is_staff à True
        if role == 'admin':
            user.is_staff = True
            user.save()

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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_user_role_and_redirect(request):
    user = request.user
    if user.role == 'admin':
        return redirect('admin_page')
    elif user.role == 'livreur':
        return redirect('livreur_page')
    elif user.role == 'client':
        return redirect('client_page')
    else:
        return Response({"message": "Accès non autorisé."}, status=403)




def custom_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            logger.info(f"User authenticated: {user.email}")
            if user.role == 'admin':
                login(request, user)
                logger.info("Admin logged in, redirecting to admin page.")
                return redirect('admin_page')
            else:
                error_message = "Désolé, cette page de connexion est réservée aux administrateurs."
                logger.warning("Non-admin user attempted to log in.")
                messages.error(request, error_message)
        else:
            error_message = "Désolé, les informations d'identification que vous avez fournies ne sont pas valides."
            logger.warning("Failed login attempt.")
            messages.error(request, error_message)

    return render(request, 'login.html')


@login_required
def admin_page(request):
    if request.user.role != 'admin':
        return render(request, 'login.html', {'error': 'Accès non autorisé. Seuls les administrateurs peuvent accéder à cette page.'})

    utilisateurs = Utilisateur.objects.filter(role='client')
    livreurs = Livreur.objects.all()
    reclamations = Reclamation.objects.select_related('demande', 'demande__utilisateur').all()
    # retours = Retour.objects.select_related('demande', 'demande__utilisateur').all()  # Commenté pour le moment
    return render(request, 'admin.html', {
        'utilisateurs': utilisateurs,
        'livreurs': livreurs,
        'reclamations': reclamations,
        # 'retours': retours,  # Commenté pour le moment
    })

@login_required
def toggle_utilisateur(request, utilisateur_id):
    utilisateur = get_object_or_404(Utilisateur, id=utilisateur_id)
    utilisateur.is_active = not utilisateur.is_active
    utilisateur.save()
    return redirect('admin_page')

@login_required
def toggle_livreur(request, livreur_id):
    if request.method == 'POST':
        livreur = get_object_or_404(Livreur, id=livreur_id)
        new_status = request.POST.get('statut_livreur')
        if new_status in ['actif', 'bloqué', 'en révision']:
            livreur.statut_livreur = new_status
            livreur.save()
    return redirect('admin_page')

@login_required
def update_reclamation_status(request, reclamation_id):
    if request.method == 'POST':
        reclamation = get_object_or_404(Reclamation, id=reclamation_id)
        new_status = request.POST.get('statut')
        if new_status in ['en attente', 'résolu', 'refusé']:
            reclamation.statut = new_status
            reclamation.save()
    return redirect('admin_page')