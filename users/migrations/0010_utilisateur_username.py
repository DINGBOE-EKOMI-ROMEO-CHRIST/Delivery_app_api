# Generated by Django 5.2.1 on 2025-06-10 07:23

import django.contrib.auth.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_alter_utilisateur_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='utilisateur',
            name='username',
            field=models.CharField(default='romei', error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username'),
            preserve_default=False,
        ),
    ]
