# Generated by Django 5.2.1 on 2025-06-14 13:17

import users.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_alter_utilisateur_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='utilisateur',
            name='telephone',
            field=models.CharField(max_length=10, unique=True, validators=[users.models.validate_phone_number]),
        ),
    ]
