from django.urls import path
from livreurs.views import create_livreur_profile, update_livreur_profile, livreur_list, livreur_detail,delete_livreur_profile
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('livreurs/create-profile/', create_livreur_profile, name='create_livreur_profile'),
    path('livreurs/update-profile/', update_livreur_profile, name='update_livreur_profile'),
    path('livreurs/', livreur_list, name='livreur_list'),
    path('livreurs/me', livreur_detail, name='livreur_detail'),
    path('livreurs/delete-profile/', delete_livreur_profile, name='delete_livreur_profile'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
