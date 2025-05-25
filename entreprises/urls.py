from django.urls import path
from .views import EntrepriseListCreate, EntrepriseRetrieveUpdateDestroy

urlpatterns = [
    path('entreprises/', EntrepriseListCreate.as_view(), name='entreprise-list-create'),
    path('entreprises/<int:pk>/', EntrepriseRetrieveUpdateDestroy.as_view(), name='entreprise-retrieve-update-destroy'),
]
