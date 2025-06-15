from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import Livreur
from .serializers import LivreurSerializer, LivreurListSerializer, LivreurDetailSerializer
from users.models import Utilisateur
from livreurs.serializers import LivreurSerializer
from users.serializers import UtilisateurSerializer
from otp.utils import generate_otp, send_otp_email
from otp.models import OTP
from delivery.models import Livraison
from delivery.serializers import LivraisonSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def create_user_and_livreur_profile(request):
    # Créer l'utilisateur
    user_serializer = UtilisateurSerializer(data=request.data)

    if not user_serializer.is_valid():
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Sauvegarder l'utilisateur avec is_active=False
    user = user_serializer.save(is_active=False)
    user.role = 'livreur'
    user.save()

    # Préparer les données pour le profil de livreur
    livreur_data = request.data.copy()
    livreur_data['utilisateur'] = user.id
    livreur_data['statut_livreur'] = 'en révision'  # Définir le statut à "en révision"

    # Créer le profil de livreur
    livreur_serializer = LivreurSerializer(data=livreur_data)

    if not livreur_serializer.is_valid():
        user.delete()  # Supprimer l'utilisateur si la création du profil échoue
        return Response(livreur_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    livreur_serializer.save(utilisateur=user)

    # Générer et envoyer l'OTP
    otp = generate_otp()
    send_otp_email(user.email, otp)
    OTP.objects.create(user=user, code=otp)

    return Response(
        {
            "message": "Compte créé, veuillez entrer l'OTP envoyé par email.",
            "user_id": user.id,
            "user": user_serializer.data,
            "livreur": livreur_serializer.data
        },
        status=status.HTTP_201_CREATED
    )
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_livreur_profile(request):
    try:
        livreur = request.user.livreur_profile
    except Livreur.DoesNotExist:
        return Response(
            {'error': 'Aucun profil de livreur trouvé pour cet utilisateur.'},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = LivreurSerializer(livreur, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def livreur_list(request):
    livreurs = Livreur.objects.all()
    serializer = LivreurListSerializer(livreurs, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def livreur_detail(request):
    try:
        # Récupère le profil de livreur de l'utilisateur connecté
        livreur = request.user.livreur_profile
    except Livreur.DoesNotExist:
        return Response(
            {'error': 'Aucun profil de livreur trouvé pour cet utilisateur.'},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = LivreurDetailSerializer(livreur)
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_livreur_profile(request):
    try:
        # Vérifie si l'utilisateur a un profil de livreur
        livreur = request.user.livreur_profile
    except Livreur.DoesNotExist:
        return Response(
            {'error': 'Aucun profil de livreur trouvé pour cet utilisateur.'},
            status=status.HTTP_404_NOT_FOUND
        )

    # Supprime le profil de livreur
    livreur.delete()

    # Optionnel : Changez le rôle de l'utilisateur en "client" ou un autre rôle par défaut
    request.user.role = 'client'
    request.user.save()

    return Response(
        {'message': 'Le profil de livreur a été supprimé avec succès.'},
        status=status.HTTP_204_NO_CONTENT
    )
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def livraison_actuelle(request):
    try:
        # Récupère le profil de livreur de l'utilisateur connecté
        livreur = request.user.livreur_profile
    except Livreur.DoesNotExist:
        return Response(
            {'error': 'Aucun profil de livreur trouvé pour cet utilisateur.'},
            status=status.HTTP_404_NOT_FOUND
        )

    # Récupère la livraison actuelle du livreur
    try:
        livraison = Livraison.objects.get(livreur=livreur, statut='en cours')
    except Livraison.DoesNotExist:
        return Response(
            {'message': 'Aucune livraison actuelle trouvée pour ce livreur.'},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = LivraisonSerializer(livraison)
    return Response(serializer.data)