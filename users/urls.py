from django.urls import path
from .views import UtilisateurListCreate, UtilisateurRetrieveUpdateDestroy,UtilisateurLoginView, UtilisateurRefreshView

urlpatterns = [
    path('utilisateurs/', UtilisateurListCreate.as_view(), name='utilisateur-list-create'),
    path('utilisateurs/<int:pk>/', UtilisateurRetrieveUpdateDestroy.as_view(), name='utilisateur-retrieve-update-destroy'),
    path('login/', UtilisateurLoginView.as_view(), name='utilisateur-login'),
    path('refresh/', UtilisateurRefreshView.as_view(), name='token-refresh'),
]
