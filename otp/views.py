# otp/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model
from .models import OTP
from .utils import generate_otp, send_otp_email
from django.utils import timezone
import json

User = get_user_model()

@csrf_exempt
@require_POST
def login_with_otp(request):
    try:
        data = json.loads(request.body)
        email = data.get('email')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            otp = generate_otp()
            send_otp_email(email, otp)
            OTP.objects.create(user=user, code=otp)
            return JsonResponse({'status': 'OTP sent'})
        else:
            return JsonResponse({'status': 'User not found'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'Invalid JSON'}, status=400)

@csrf_exempt
@require_POST
def verify_otp(request):
    try:
        data = json.loads(request.body)
        otp_code = data.get('otp')

        if OTP.objects.filter(code=otp_code, is_used=False).exists():
            otp_obj = OTP.objects.get(code=otp_code, is_used=False)

            # Vérifier l'expiration de l'OTP
            if otp_obj.expires_at < timezone.now():
                return JsonResponse({'status': 'OTP expired'}, status=400)

            otp_obj.is_used = True
            otp_obj.save()
            return JsonResponse({'status': 'OTP verified'})
        else:
            return JsonResponse({'status': 'Invalid OTP'}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'Invalid JSON'}, status=400)

