# otp/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import OTP
from .utils import generate_otp, send_otp_email

User = get_user_model()

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from users.models import Utilisateur
from otp.models import OTP
from livreurs.models import Livreur

@api_view(['POST'])
@permission_classes([AllowAny])
def verify_otp(request):
    try:
        data = request.data
        email = data.get('email')
        otp_code = data.get('otp')

        # Récupérer l'utilisateur
        user = Utilisateur.objects.get(email=email)

        # Vérifier l'OTP
        otp = OTP.objects.filter(user=user, code=otp_code).first()

        if otp:
            # Activer le compte utilisateur
            user.is_active = True

            # Vérifier le rôle de l'utilisateur et mettre à jour les champs appropriés
            if user.role == 'livreur':
                # Mettre à jour le statut du livreur
                livreur_profile = Livreur.objects.get(utilisateur=user)
                livreur_profile.statut_livreur = 'actif'
                livreur_profile.save()
            elif user.role == 'client':  # ou tout autre rôle nécessitant is_staff
                user.is_staff = True

            user.save()

            return Response({'message': 'Compte activé. Bienvenue !'})
        else:
            return Response({'error': 'OTP invalide.'}, status=status.HTTP_400_BAD_REQUEST)

    except Utilisateur.DoesNotExist:
        return Response({'error': 'Utilisateur non trouvé.'}, status=status.HTTP_404_NOT_FOUND)
    except Livreur.DoesNotExist:
        return Response({'error': 'Profil de livreur non trouvé.'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_otp(request):
    try:
        data = request.data
        email = data.get('email')

        # Vérifie si l'utilisateur existe
        user = User.objects.get(email=email)

        # Supprime l'ancien OTP s'il existe
        OTP.objects.filter(user=user).delete()

        # Génère et envoie un nouvel OTP
        otp = generate_otp()
        send_otp_email(user.email, otp)
        OTP.objects.create(user=user, code=otp)

        return Response({'message': 'Un nouvel OTP a été envoyé à votre email.'})

    except User.DoesNotExist:
        return Response({'error': 'Utilisateur non trouvé.'}, status=status.HTTP_404_NOT_FOUND)
