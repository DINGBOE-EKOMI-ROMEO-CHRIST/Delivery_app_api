from django.urls import path
from .views import UtilisateurListCreate, UtilisateurRetrieveUpdateDestroy, get_user_info, CustomTokenObtainPairView, update_location, get_location

urlpatterns = [
    path('utilisateurs/', UtilisateurListCreate.as_view(), name='utilisateur-list-create'),
    path('utilisateurs/<int:pk>/', UtilisateurRetrieveUpdateDestroy.as_view(), name='utilisateur-retrieve-update-destroy'),
    path('me/', get_user_info, name='get_user_info'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('update-location/', update_location, name='update_location'),
    path('get-location/', get_location, name='get_location'),
]
