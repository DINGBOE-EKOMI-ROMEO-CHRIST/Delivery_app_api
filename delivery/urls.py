from django.urls import path
from .views import create_livraison, get_livraison, update_livraison, delete_livraison, list_livraisons, livraisons_en_attente,assigner_livraison

urlpatterns = [
    path('livraisons/create/', create_livraison, name='create_livraison'),
    path('livraisons/<int:livraison_id>/', get_livraison, name='get_livraison'),
    path('livraisons/update/<int:livraison_id>/', update_livraison, name='update_livraison'),
    path('livraisons/delete/<int:livraison_id>/', delete_livraison, name='delete_livraison'),
    path('livraisons/', list_livraisons, name='list_livraisons'),
    path('livraisons/assignable/', livraisons_en_attente, name='livraisons_en_attente'),  # Ajoutez cette ligne
    path('livraisons/assigner-livreur/', assigner_livraison, name='assigner_livraison'),
]

