# Generated by Django 5.2.1 on 2025-06-17 19:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demande', '0004_alter_demande_photo_colis'),
        ('reclamation', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reclamation',
            name='demande',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='demande.demande'),
        ),
        migrations.AlterField(
            model_name='retour',
            name='demande',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='demande.demande'),
        ),
        migrations.DeleteModel(
            name='Demande',
        ),
    ]
