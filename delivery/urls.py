from django.urls import path
from .views import create_livraison, get_livraison, update_livraison, delete_livraison, list_livraisons

urlpatterns = [
    path('livraisons/create/', create_livraison, name='create_livraison'),
    path('livraisons/<int:livraison_id>/', get_livraison, name='get_livraison'),
    path('livraisons/update/<int:livraison_id>/', update_livraison, name='update_livraison'),
    path('livraisons/delete/<int:livraison_id>/', delete_livraison, name='delete_livraison'),
    path('livraisons/', list_livraisons, name='list_livraisons'),
]
