from django.db import models

class Inscription(models.Model):
    date = models.DateField()
    school_year = models.CharField(max_length=9)

    # Responsable
    responsable_nom = models.CharField(max_length=100)
    responsable_prenom = models.CharField(max_length=100)
    responsable_lien = models.CharField(max_length=50)
    responsable_email = models.EmailField()
    responsable_telephone = models.CharField(max_length=20)

    # Élève
    eleve_prenom = models.CharField(max_length=100)
    eleve_nom = models.CharField(max_length=100)
    eleve_date_naissance = models.DateField()
    niveau_scolaire = models.CharField(max_length=50)
    classe = models.CharField(max_length=20)
    institut = models.CharField(max_length=200)
    province = models.CharField(max_length=100)
