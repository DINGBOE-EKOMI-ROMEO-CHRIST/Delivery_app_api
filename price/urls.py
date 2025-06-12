from django.urls import path
from .views import InitiateMomoPayment, ListPaiements,CheckMomoPaymentStatus

urlpatterns = [
    path('initiate-payment/', InitiateMomoPayment.as_view(), name='initiate-payment'),
    path('ListPaiements/', ListPaiements.as_view(), name='ListPaiements'),
    path('paiements/status/', CheckMomoPaymentStatus.as_view(), name='status_paiement'),
]
