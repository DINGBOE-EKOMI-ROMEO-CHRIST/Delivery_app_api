# colis/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Colis
from .serializers import ColisSerializer, Colislist
from users.models import Utilisateur

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_colis(request):
    expediteur = request.user

    receiver_email = request.data.get('receiver_email')
    try:
        destinataire = Utilisateur.objects.get(email=receiver_email)
    except Utilisateur.DoesNotExist:
        return Response({'error': 'Destinataire non trouvé.'}, status=status.HTTP_404_NOT_FOUND)

    # Vérifie si l'expéditeur est le même que le destinataire
    if expediteur == destinataire:
        return Response({'error': 'L\'expéditeur ne peut pas être le même que le destinataire.'}, status=status.HTTP_400_BAD_REQUEST)

    # Vérifie si l'expéditeur ou le destinataire a des colis en cours
    colis_en_cours_expediteur = Colis.objects.filter(expediteur=expediteur, statut__in=['en attente', 'pris en charge', 'en transit']).exists()
    colis_en_cours_destinataire = Colis.objects.filter(destinataire=destinataire, statut__in=['en attente', 'pris en charge', 'en transit']).exists()

    if colis_en_cours_expediteur or colis_en_cours_destinataire:
        return Response({'error': 'L\'expéditeur ou le destinataire a déjà un colis en cours.'}, status=status.HTTP_400_BAD_REQUEST)

    # Vérifie s'il existe déjà un colis entre l'expéditeur et le destinataire avec un statut non livré
    colis_existant = Colis.objects.filter(
        expediteur=expediteur,
        destinataire=destinataire,
        statut__in=['en attente', 'pris en charge', 'en transit']
    ).exists()

    if colis_existant:
        return Response({'error': 'Il existe déjà une livraison en cours entre l\'expéditeur et le destinataire.'}, status=status.HTTP_400_BAD_REQUEST)

    colis_data = {
        'expediteur': expediteur.id,
        'destinataire': destinataire.id,
        'dimensions': request.data.get('dimensions'),
        'poids': request.data.get('poids'),
        'type_marchandise': request.data.get('type_marchandise'),
        'adresse_depart': request.data.get('adresse_depart'),
        'adresse_destination': request.data.get('adresse_destination'),
        'mode_livraison': request.data.get('mode_livraison'),
    }

    serializer = ColisSerializer(data=colis_data)

    if serializer.is_valid():
        colis = serializer.save()
        estimated_price = calculate_estimated_price(colis.poids, colis.mode_livraison)

        return Response({
            'id': colis.id,
            'estimated_price': estimated_price,
            'status': colis.statut
        }, status=status.HTTP_201_CREATED)

    return Response({'error': 'Champs invalides', 'details': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

def calculate_estimated_price(weight, delivery_type):
    # Prix de base en FCFA
    base_price = 200.0  # Assure-toi que c'est un float

    # Convertir le poids en float
    weight_float = float(weight)

    if delivery_type == 'express':
        return base_price * weight_float * 1.5
    elif delivery_type == 'standard':
        return base_price * weight_float
    else:
        return base_price * weight_float * 0.8


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_last_colis_in_progress(request):
    # Récupère le dernier colis en cours pour l'utilisateur connecté
    last_colis_in_progress = Colis.objects.filter(
        expediteur=request.user,
        statut__in=['en attente', 'pris en charge', 'en transit']
    ).order_by('-date_creation').first()

    if not last_colis_in_progress:
        return Response({'message': 'Aucun colis en cours trouvé.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = Colislist(last_colis_in_progress)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_colis(request, colis_id):
    try:
        colis = Colis.objects.get(id=colis_id)

        # Vérifie si l'utilisateur est l'expéditeur du colis
        if request.user != colis.expediteur:
            return Response({'error': 'Non autorisé à supprimer ce colis.'}, status=status.HTTP_403_FORBIDDEN)

        # Vérifie si le colis est déjà pris en charge, en transit ou livré
        if colis.statut in ['pris en charge', 'en transit', 'livré']:
            return Response({'error': 'Impossible de supprimer un colis déjà pris en charge, en transit ou livré.'}, status=status.HTTP_400_BAD_REQUEST)

        colis.delete()
        return Response({'message': 'Colis supprimé avec succès.'}, status=status.HTTP_204_NO_CONTENT)

    except Colis.DoesNotExist:
        return Response({'error': 'Colis non trouvé.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def patch_colis(request, colis_id):
    try:
        colis = Colis.objects.get(id=colis_id)

        # Vérifie si l'utilisateur est l'expéditeur du colis
        if request.user != colis.expediteur:
            return Response({'error': 'Non autorisé à mettre à jour ce colis.'}, status=status.HTTP_403_FORBIDDEN)

        # Vérifie si le colis est déjà pris en charge, en transit ou livré
        if colis.statut in ['pris en charge', 'en transit', 'livré']:
            return Response({'error': 'Impossible de mettre à jour un colis déjà pris en charge, en transit ou livré.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ColisSerializer(colis, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Colis.DoesNotExist:
        return Response({'error': 'Colis non trouvé.'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_all_colis_admin(request):
    # Récupère tous les colis
    colis_list = Colis.objects.all()

    # Crée un sérialiseur avec la liste des colis
    serializer = Colislist(colis_list, many=True)

    # Renvoie les données sérialisées
    return Response(serializer.data)
   
