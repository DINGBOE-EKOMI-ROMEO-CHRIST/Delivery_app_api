# otp/signals.py
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(pre_save, sender=User)
def validate_user_email(sender, instance, **kwargs):
    try:
        validate_email(instance.email)
    except ValidationError:
        raise ValidationError("L'adresse email n'est pas valide.")
