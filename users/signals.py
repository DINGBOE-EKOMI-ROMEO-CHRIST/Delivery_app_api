from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.hashers import make_password
from .models import Utilisateur

@receiver(pre_save, sender=Utilisateur)
def hash_password(sender, instance, **kwargs):
    if not instance.password.startswith('pbkdf2_sha256$'):
        instance.password = make_password(instance.password)
