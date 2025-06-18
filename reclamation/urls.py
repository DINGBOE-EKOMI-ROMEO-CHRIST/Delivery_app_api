# urls.py
from django.urls import path
from .views import CreateReclamationView, RetourListCreateView

urlpatterns = [
    path('reclamations/', CreateReclamationView.as_view(), name='create_reclamation'),
    path('retours/', RetourListCreateView.as_view(), name='retour-list-create'),
]
