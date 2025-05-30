# otp/apps.py
from django.apps import AppConfig

class OtpConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'otp'

    def ready(self):
        import otp.signals
