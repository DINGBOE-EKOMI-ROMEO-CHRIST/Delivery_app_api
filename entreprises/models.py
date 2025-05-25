from django.db import models

class Entreprise(models.Model):
    nom = models.CharField(max_length=255)
    domaine_activite = models.CharField(max_length=255)
    localisation = models.TextField()
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=20, unique=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom
