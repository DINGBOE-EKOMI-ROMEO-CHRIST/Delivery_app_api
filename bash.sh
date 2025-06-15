#!/bin/bash

echo "🔧 Initialisation de l'application Django..."

python manage.py makemigrations
python manage.py migrate

# Création du superutilisateur si inexistant
python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@gamil.com', 'motdepasse123')
"

echo "✅ Initialisation terminée."
