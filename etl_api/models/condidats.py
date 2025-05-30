from django.db import models

class Condidats(models.Model):
    prenom = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    email = models.EmailField()
    cvLink = models.URLField()
    dateApply = models.DateField()

    def __str__(self):
        return f"{self.prenom} {self.nom}"