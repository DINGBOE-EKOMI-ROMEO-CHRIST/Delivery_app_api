#!/bin/bash

echo "🔧 Initialisation de l'application Django..."

python manage.py makemigrations
python manage.py migrate

# Créer le superutilisateur s'il n'existe pas (vérifie par email)
python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(email='admin@example.com').exists():
    User.objects.create_superuser('admin@example.com', 'motdepasse123')
"

echo "✅ Initialisation terminée."
