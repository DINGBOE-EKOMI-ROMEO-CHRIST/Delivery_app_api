# Generated by Django 5.2.1 on 2025-05-30 08:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('otp', '0023_alter_otp_expires_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otp',
            name='expires_at',
            field=models.DateTimeField(verbose_name=datetime.datetime(2025, 5, 30, 9, 24, 52, 942643, tzinfo=datetime.timezone.utc)),
        ),
    ]
