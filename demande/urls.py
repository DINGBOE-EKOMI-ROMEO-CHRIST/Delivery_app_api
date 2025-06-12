from django.urls import path
from demande.views import create_colis, delete_colis, patch_colis, get_last_colis_in_progress, get_all_demandes_public,delete_demande_by_id
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('demande/create/', create_colis, name='create_colis'),
    path('demandes/patch/', patch_colis, name='patch_colis'),
    path('demandes/delete/', delete_colis, name='delete_colis'),
    path('demandes/last-in-progress/', get_last_colis_in_progress, name='get_last_colis_in_progress'),
    path('demandes/all/public/', get_all_demandes_public, name='get_all_demandes_public'),
    path('demandes/delete/<int:demande_id>/', delete_demande_by_id, name='delete_demande_by_id'),
    ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)