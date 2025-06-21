from django.db import models

class Inscription(models.Model):
    date = models.DateField()
    school_year = models.CharField(max_length=9)

    # Responsable
    responsable_nom = models.CharField(max_length=100)
    responsable_prenom = models.CharField(max_length=100)
    responsable_lien = models.CharField(max_length=50)
    responsable_email = models.EmailField(blank=True, null=True)
    responsable_telephone = models.CharField(max_length=20)

    # Élève
    eleve_prenom = models.CharField(max_length=100)
    eleve_nom = models.CharField(max_length=100)
    eleve_date_naissance = models.DateField()
    niveau_scolaire = models.CharField(max_length=50)
    classe = models.CharField(max_length=20, blank=True, null=True)
    institut = models.CharField(max_length=200, blank=True, null=True)
    province = models.CharField(max_length=100)
    branch = models.CharField(max_length=100, blank=True, null=True)

    # Confirmation
    confirmed = models.BooleanField(default=False)
    confirmed_by = models.CharField(max_length=100, blank=True, null=True)
