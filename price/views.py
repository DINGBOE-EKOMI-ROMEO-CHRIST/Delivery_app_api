import json
import uuid
import time
import base64
import logging
import requests

from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings
from .models import Paiement
from .serializers import PaiementSerializer

logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name='dispatch')
class InitiateMomoPayment(View):
    def post(self, request, *args, **kwargs):
        try:
            logger.info("Demande de paiement MoMo reçue.")

            if not request.body:
                return JsonResponse({"error": "Le corps de la requête est vide."}, status=400)

            try:
                data = json.loads(request.body)
            except json.JSONDecodeError as e:
                return JsonResponse({"error": f"JSON invalide : {str(e)}"}, status=400)

            numero_telephone = data.get('numero_telephone')
            montant = data.get('montant')
            livraison_id = data.get('livraison_id')

            if not all([numero_telephone, montant, livraison_id]):
                return JsonResponse({"error": "Données manquantes (numero_telephone, montant, livraison_id)"}, status=400)

            reference_id = str(uuid.uuid4())

            # Construction des headers avec Basic Auth encodé
            token_url = f"https://{settings.MOMO_TARGET_ENVIRONMENT}/collection/token/"
            auth_string = f"{settings.MOMO_API_USER}:{settings.MOMO_API_KEY}"
            encoded_auth = base64.b64encode(auth_string.encode()).decode()
            token_headers = {
                "Ocp-Apim-Subscription-Key": settings.MOMO_SUBSCRIPTION_KEY,
                "Authorization": f"Basic {encoded_auth}",
            }

            token_resp = requests.post(token_url, headers=token_headers)
            if token_resp.status_code != 200:
                return JsonResponse({"error": "Erreur lors de l'obtention du token", "details": token_resp.text}, status=500)

            token = token_resp.json().get("access_token")

            payment_url = f"https://{settings.MOMO_TARGET_ENVIRONMENT}/collection/v1_0/requesttopay"
            headers = {
                "X-Reference-Id": reference_id,
                "X-Target-Environment": "sandbox",
                "Ocp-Apim-Subscription-Key": settings.MOMO_SUBSCRIPTION_KEY,
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }

            payload = {
                "amount": str(montant),
                "currency": "EUR",
                "externalId": reference_id,
                "payer": {
                    "partyIdType": "MSISDN",
                    "partyId": numero_telephone
                },
                "payerMessage": "Paiement pour livraison",
                "payeeNote": "Merci pour votre commande"
            }

            resp = requests.post(payment_url, headers=headers, json=payload)
            if resp.status_code != 202:
                return JsonResponse({"error": "Paiement échoué", "details": resp.text}, status=resp.status_code)

            time.sleep(3)  # attente avant vérification du statut

            status_url = f"https://{settings.MOMO_TARGET_ENVIRONMENT}/collection/v1_0/requesttopay/{reference_id}"
            status_headers = {
                "X-Target-Environment": "sandbox",
                "Ocp-Apim-Subscription-Key": settings.MOMO_SUBSCRIPTION_KEY,
                "Authorization": f"Bearer {token}"
            }
            status_resp = requests.get(status_url, headers=status_headers)
            status_data = status_resp.json()

            if status_data.get("status") == "SUCCESSFUL":
                paiement_data = {
                    'livraison': livraison_id,
                    'montant': montant,
                    'mode_paiement': 'Mobile Money',
                }

                serializer = PaiementSerializer(data=paiement_data)
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse({"success": True, "message": "Paiement confirmé", "details": status_data})
                else:
                    return JsonResponse({"error": "Paiement OK, mais erreur de sauvegarde", "details": serializer.errors}, status=400)

            return JsonResponse({"error": "Paiement non abouti", "details": status_data}, status=400)

        except Exception as e:
            logger.error(f"Erreur serveur : {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)


class ListPaiements(View):
    def get(self, request, *args, **kwargs):
        paiements = Paiement.objects.all()
        serializer = PaiementSerializer(paiements, many=True)
        return JsonResponse(serializer.data, safe=False)

@method_decorator(csrf_exempt, name='dispatch')
class CheckMomoPaymentStatus(View):
    def get(self, request, *args, **kwargs):
        reference_id = request.GET.get('reference_id')
        if not reference_id:
            return JsonResponse({"error": "reference_id manquant"}, status=400)

        # Obtenir token comme dans InitiateMomoPayment
        token_url = f"https://{settings.MOMO_TARGET_ENVIRONMENT}/collection/token/"
        auth_string = f"{settings.MOMO_API_USER}:{settings.MOMO_API_KEY}"
        encoded_auth = base64.b64encode(auth_string.encode()).decode()
        token_headers = {
            "Ocp-Apim-Subscription-Key": settings.MOMO_SUBSCRIPTION_KEY,
            "Authorization": f"Basic {encoded_auth}",
        }
        token_resp = requests.post(token_url, headers=token_headers)
        if token_resp.status_code != 200:
            return JsonResponse({"error": "Erreur lors de l'obtention du token", "details": token_resp.text}, status=500)

        token = token_resp.json().get("access_token")

        status_url = f"https://{settings.MOMO_TARGET_ENVIRONMENT}/collection/v1_0/requesttopay/{reference_id}"
        status_headers = {
            "X-Target-Environment": "sandbox",
            "Ocp-Apim-Subscription-Key": settings.MOMO_SUBSCRIPTION_KEY,
            "Authorization": f"Bearer {token}"
        }
        status_resp = requests.get(status_url, headers=status_headers)
        if status_resp.status_code != 200:
            return JsonResponse({"error": "Erreur lors de la récupération du statut", "details": status_resp.text}, status=500)

        return JsonResponse(status_resp.json())
