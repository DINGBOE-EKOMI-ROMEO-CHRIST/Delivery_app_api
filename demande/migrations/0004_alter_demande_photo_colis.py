# Generated by Django 5.2.1 on 2025-06-10 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demande', '0003_remove_demande_adresse_depart_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='demande',
            name='photo_colis',
            field=models.ImageField(default='colis.jpg', upload_to='photos_colis/'),
            preserve_default=False,
        ),
    ]
