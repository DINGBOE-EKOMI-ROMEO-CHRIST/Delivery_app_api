# Generated by Django 5.2.1 on 2025-06-10 10:42

import django.core.validators
import livreurs.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('livreurs', '0004_remove_livreur_latitude_remove_livreur_longitude'),
    ]

    operations = [
        migrations.AlterField(
            model_name='livreur',
            name='numero_immatriculation',
            field=models.CharField(max_length=50, validators=[django.core.validators.RegexValidator(message="Le numéro d'immatriculation doit contenir uniquement des lettres majuscules, des chiffres et des tirets.", regex='^[A-Z0-9-]+$')]),
        ),
        migrations.AlterField(
            model_name='livreur',
            name='type_vehicule',
            field=models.CharField(default='Moto', max_length=50, validators=[livreurs.models.validate_vehicle_type]),
        ),
    ]
