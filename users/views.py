from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .models import Utilisateur
from .serializers import UtilisateurSerializer

class UtilisateurListCreate(generics.ListCreateAPIView):
    queryset = Utilisateur.objects.all()
    serializer_class = UtilisateurSerializer

class UtilisateurRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Utilisateur.objects.all()
    serializer_class = UtilisateurSerializer

class UtilisateurLoginView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]

class UtilisateurRefreshView(TokenRefreshView):
    permission_classes = [permissions.AllowAny]

