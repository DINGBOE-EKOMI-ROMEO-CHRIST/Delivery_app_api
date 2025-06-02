# delivery_api/urls.py
from django.urls import path
from colis.views import create_colis, get_last_colis_in_progress, delete_colis, patch_colis,get_all_colis_admin

urlpatterns = [
    path('colis/create/', create_colis, name='create_colis'),
    path('colis/waiting/', get_last_colis_in_progress, name='get_last_colis_in_progress'),
    path('colis/delete/<int:colis_id>/', delete_colis, name='delete_colis'),
    path('colis/patch/<int:colis_id>/', patch_colis, name='patch_colis'),
    path('colis/', get_all_colis_admin, name='get_all_colis_admin'),
]
