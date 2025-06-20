# Generated by Django 5.2.1 on 2025-06-09 18:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Demande',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Livreur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Livraison',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_prise_en_charge', models.DateTimeField(auto_now_add=True)),
                ('longitude_depart', models.DecimalField(decimal_places=8, max_digits=10)),
                ('latitude_depart', models.DecimalField(decimal_places=8, max_digits=11)),
                ('longitude_arrivee', models.DecimalField(decimal_places=8, max_digits=10)),
                ('latitude_arrivee', models.DecimalField(decimal_places=8, max_digits=11)),
                ('numero_depart', models.IntegerField()),
                ('numero_arrivee', models.IntegerField()),
                ('date_livraison', models.DateTimeField(blank=True, null=True)),
                ('statut', models.CharField(choices=[('en attente', 'En attente'), ('en cours', 'En cours'), ('livré', 'Livré'), ('annulé', 'Annulé')], default='en attente', max_length=20)),
                ('demande', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='delivery.demande')),
                ('livreur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='delivery.livreur')),
            ],
            options={
                'constraints': [models.CheckConstraint(condition=models.Q(models.Q(('latitude_depart', models.F('latitude_arrivee')), _negated=True), models.Q(('longitude_depart', models.F('longitude_arrivee')), _negated=True), _connector='OR'), name='check_lat_long_distinct')],
            },
        ),
    ]
