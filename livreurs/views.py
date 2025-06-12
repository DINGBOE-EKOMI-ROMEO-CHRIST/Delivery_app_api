from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Livreur
from .serializers import LivreurSerializer, LivreurListSerializer, LivreurDetailSerializer
from users.models import Utilisateur

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_livreur_profile(request):
    if hasattr(request.user, 'livreur_profile'):
        return Response(
            {'error': 'Un profil de livreur existe déjà pour cet utilisateur.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    request.user.role = 'livreur'
    request.user.save()

    serializer = LivreurSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(utilisateur=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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