from rest_framework import generics
from .models import Entreprise
from .serializers import EntrepriseSerializer

class EntrepriseListCreate(generics.ListCreateAPIView):
    queryset = Entreprise.objects.all()
    serializer_class = EntrepriseSerializer

class EntrepriseRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Entreprise.objects.all()
    serializer_class = EntrepriseSerializer
