# delivery_api/urls.py
from django.urls import path
from livreurs.views import create_livreur_profile,update_livreur_profile, livreur_list

urlpatterns = [
    path('api/livreurs/create-profile/', create_livreur_profile, name='create_livreur_profile'),
    path('api/livreurs/update-profile/', update_livreur_profile, name='update_livreur_profile'),
    path('api/livreurs/', livreur_list, name='livreur_list'),
]
