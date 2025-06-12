from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Demande
from .serializers import DemandeSerializer, DemandeListSerializer 
from delivery.serializers import LivraisonSerializer
from .serializers import DemandeListSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_colis(request):
    # Vérifier si l'utilisateur a une demande en cours qui n'est pas livrée
    last_undelivered_demande = Demande.objects.filter(
        utilisateur=request.user,
        statut_demande__in=['en attente', 'pris en charge', 'en transit']
    ).order_by('-date_creation').first()

    if last_undelivered_demande:
        return Response(
            {'error': 'Vous avez déjà une demande en cours qui n\'est pas encore livrée.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Étape 1: Créer la demande
    demande_data = {
        'utilisateur': request.user.id,
        'nature_colis': request.data.get('nature_colis'),
        'dimensions': request.data.get('dimensions'),
        'poids': request.data.get('poids'),
        'photo_colis': request.data.get('photo_colis'),
        'mode_livraison': request.data.get('mode_livraison'),
    }

    demande_serializer = DemandeSerializer(data=demande_data)
    if not demande_serializer.is_valid():
        return Response(demande_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    demande = demande_serializer.save()

    # Étape 2: Créer la livraison associée
    livraison_data = {
        'demande': demande.id,
        'livreur': request.data.get('livreur_id'),  # Assurez-vous que le livreur est spécifié
        'longitude_depart': request.data.get('longitude_depart'),
        'latitude_depart': request.data.get('latitude_depart'),
        'longitude_arrivee': request.data.get('longitude_arrivee'),
        'latitude_arrivee': request.data.get('latitude_arrivee'),
        'numero_depart': request.data.get('numero_depart'),
        'numero_arrivee': request.data.get('numero_arrivee'),
        'statut': 'en attente',  # Statut initial
    }

    livraison_serializer = LivraisonSerializer(data=livraison_data)
    if not livraison_serializer.is_valid():
        # Si la livraison n'est pas valide, supprimez la demande créée précédemment
        demande.delete()
        return Response(livraison_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    livraison_serializer.save()

    return Response({
        'demande_id': demande.id,
        'livraison_id': livraison_serializer.data['id'],
        'message': 'Demande et livraison créées avec succès.'
    }, status=status.HTTP_201_CREATED)


def calculate_estimated_price(weight, delivery_type):
    base_price = 200.0
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
    # Filtrer les colis de l'utilisateur connecté qui sont en cours
    last_colis_in_progress = Demande.objects.filter(
        utilisateur=request.user,
        statut_demande__in=['en attente', 'pris en charge', 'en transit']
    ).order_by('-date_creation').first()

    # Vérifier si un colis en cours a été trouvé
    if not last_colis_in_progress:
        return Response(
            {'message': 'Aucun colis en cours trouvé.'},
            status=status.HTTP_404_NOT_FOUND
        )

    # Sérialiser et retourner le colis trouvé
    serializer = DemandeListSerializer(last_colis_in_progress)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_colis(request):
    # Récupérer la dernière demande de l'utilisateur
    last_colis_in_progress = Demande.objects.filter(
        utilisateur=request.user,
        statut_demande='en attente'
    ).order_by('-date_creation').first()

    if not last_colis_in_progress:
        return Response(
            {'error': 'Aucune demande en attente trouvée pour cet utilisateur.'},
            status=status.HTTP_404_NOT_FOUND
        )

    # Vérifier si la demande est supprimable
    if last_colis_in_progress.statut_demande != 'en attente':
        return Response(
            {'error': 'La demande ne peut être supprimée que si elle est en attente.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Autoriser la suppression
    last_colis_in_progress.delete()
    return Response(
        {'message': 'Demande supprimée avec succès.'},
        status=status.HTTP_204_NO_CONTENT
    )

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def patch_colis(request):
    # Récupérer la dernière demande de l'utilisateur
    last_colis_in_progress = Demande.objects.filter(
        utilisateur=request.user,
        statut_demande='en attente'
    ).order_by('-date_creation').first()

    if not last_colis_in_progress:
        return Response(
            {'error': 'Aucune demande en attente trouvée pour cet utilisateur.'},
            status=status.HTTP_404_NOT_FOUND
        )

    # Vérifier si la demande est modifiable
    if last_colis_in_progress.statut_demande != 'en attente':
        return Response(
            {'error': 'La demande ne peut être modifiée que si elle est en attente.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Autoriser la modification
    serializer = DemandeSerializer(last_colis_in_progress, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_all_demandes_public(request):
    # Récupérer toutes les demandes
    demandes = Demande.objects.all().order_by('-date_creation')

    # Sérialiser les demandes
    serializer = DemandeListSerializer(demandes, many=True)

    # Retourner les demandes sérialisées
    return Response(serializer.data)

@api_view(['DELETE'])
def delete_demande_by_id(request, demande_id):
    try:
        # Récupérer la demande par son ID
        demande = Demande.objects.get(id=demande_id)
    except Demande.DoesNotExist:
        # Retourner une erreur si la demande n'existe pas
        return Response(
            {'error': 'Demande non trouvée.'},
            status=status.HTTP_404_NOT_FOUND
        )

    # Supprimer la demande
    demande.delete()

    # Retourner un message de succès
    return Response(
        {'message': 'Demande supprimée avec succès.'},
        status=status.HTTP_204_NO_CONTENT
    )
    
    """
    nature_colis : Texte, valeur : "Livre"
    dimensions : Texte, valeur : "30x20x10"
    poids : Texte, valeur : "1.5"
    photo_colis : Fichier, sélectionnez le fichier image colis.jpg depuis votre système de fichiers.
    adresse_depart : Texte, valeur : "123 Rue de Départ"
    adresse_destination : Texte, valeur : "456 Rue de Destination"
    mode_livraison : Texte, valeur : "standard"
    livreur_id : Texte, valeur : "1"
    longitude_depart : Texte, valeur : "2.3522"
    latitude_depart : Texte, valeur : "48.8566"
    longitude_arrivee : Texte, valeur : "-73.5673"
    latitude_arrivee : Texte, valeur : "45.5017"
    numero_depart : Texte, valeur : "123456789"
    numero_arrivee : Texte, valeur : "987654321"

    """