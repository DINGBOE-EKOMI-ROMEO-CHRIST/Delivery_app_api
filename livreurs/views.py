# livreurs/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Livreur
from .serializers import LivreurSerializer, LivreurListSerializer
from users.models import Utilisateur

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_livreur_profile(request):
    # Vérifie si l'utilisateur a déjà un profil de livreur
    if hasattr(request.user, 'livreur_profile'):
        return Response(
            {'error': 'Un profil de livreur existe déjà pour cet utilisateur.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Change le rôle de l'utilisateur en "livreur"
    request.user.role = 'livreur'
    request.user.save()

    # Crée un sérialiseur avec les données de la requête
    serializer = LivreurSerializer(data=request.data)

    if serializer.is_valid():
        # Associe le profil de livreur à l'utilisateur authentifié
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
