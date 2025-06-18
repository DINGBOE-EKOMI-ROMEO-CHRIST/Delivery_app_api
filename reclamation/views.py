from rest_framework import generics, status, permissions
from rest_framework.response import Response
from demande.models import Demande
from .models import Reclamation
from .serializers import ReclamationSerializer, RetourSerializer
from rest_framework import generics, permissions
from .models import Retour


class CreateReclamationView(generics.CreateAPIView):
    serializer_class = ReclamationSerializer
    permission_classes = [permissions.IsAuthenticated]  # Assurez-vous que l'utilisateur est authentifié

    def create(self, request, *args, **kwargs):
        reclamation_data = {
            'demande': request.data.get('demande_id'),
            'description': request.data.get('description'),
            'statut': request.data.get('statut', 'en attente'),
        }

        try:
            demande = Demande.objects.get(id=reclamation_data['demande'])
        except Demande.DoesNotExist:
            return Response({"error": "Demande not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=reclamation_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class RetourListCreateView(generics.ListCreateAPIView):
    queryset = Retour.objects.all()
    serializer_class = RetourSerializer
    #permission_classes = [permissions.IsAuthenticated]  # Assurez-vous que l'utilisateur est authentifié
