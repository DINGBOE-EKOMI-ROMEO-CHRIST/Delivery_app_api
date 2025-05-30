# livreurs/signals.py
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Livreur

@receiver(pre_save, sender=Livreur)
def hash_password(sender, instance, **kwargs):
    if instance.pk is None:
        instance.set_password(instance.password)
