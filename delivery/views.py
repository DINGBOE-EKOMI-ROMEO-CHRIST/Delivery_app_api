from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Livraison
from .serializers import LivraisonSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_livraison(request):
    serializer = LivraisonSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_livraison(request, livraison_id):
    try:
        livraison = Livraison.objects.get(id=livraison_id)
    except Livraison.DoesNotExist:
        return Response({'error': 'Livraison non trouvée.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = LivraisonSerializer(livraison)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_livraison(request, livraison_id):
    try:
        livraison = Livraison.objects.get(id=livraison_id)
    except Livraison.DoesNotExist:
        return Response({'error': 'Livraison non trouvée.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = LivraisonSerializer(livraison, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_livraison(request, livraison_id):
    try:
        livraison = Livraison.objects.get(id=livraison_id)
    except Livraison.DoesNotExist:
        return Response({'error': 'Livraison non trouvée.'}, status=status.HTTP_404_NOT_FOUND)

    livraison.delete()
    return Response({'message': 'Livraison supprimée avec succès.'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_livraisons(request):
    livraisons = Livraison.objects.all()
    serializer = LivraisonSerializer(livraisons, many=True)
    return Response(serializer.data)
