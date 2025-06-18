from django.urls import path
from .views import UtilisateurListCreate, UtilisateurRetrieveUpdateDestroy, get_user_info, CustomTokenObtainPairView, update_location, get_location, check_user_role_and_redirect
from .views import custom_login, admin_page, toggle_livreur,toggle_utilisateur, update_reclamation_status  
urlpatterns = [
    path('utilisateurs/', UtilisateurListCreate.as_view(), name='utilisateur-list-create'),
    path('utilisateurs/<int:pk>/', UtilisateurRetrieveUpdateDestroy.as_view(), name='utilisateur-retrieve-update-destroy'),
    path('me/', get_user_info, name='get_user_info'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('update-location/', update_location, name='update_location'),
    path('get-location/', get_location, name='get_location'),
    path('check-role/', check_user_role_and_redirect, name='check_role_and_redirect'),
    
    path('login-page/', custom_login, name='login'),
    path('admin-page/', admin_page, name='admin_page'),
    path('toggle-utilisateur/<int:utilisateur_id>/', toggle_utilisateur, name='toggle_utilisateur'),
    path('toggle-livreur/<int:livreur_id>/', toggle_livreur, name='toggle_livreur'),
    path('update-reclamation/<int:reclamation_id>/', update_reclamation_status, name='update_reclamation_status'),
]
