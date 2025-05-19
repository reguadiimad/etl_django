from django.contrib.auth.hashers import make_password
from django.db import models
from .inscription import Inscription


class Admin(models.Model):
    CIVILITE_CHOICES = [
        ('Mr', 'Mr'),
        ('Mme', 'Mme'),
    ]

    civilite = models.CharField(max_length=3, choices=CIVILITE_CHOICES, default='Mr')
    admin_id = models.CharField(max_length=50, unique=True, editable=False)
    prenom = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    telephone = models.CharField(max_length=20)
    role = models.CharField(max_length=100)
    adresse = models.CharField(max_length=255)
    birthday = models.DateField()
    picture = models.URLField(max_length=1000, blank=True, null=True)
    isSuperAdmin = models.BooleanField(default=False)
    must_change_password = models.BooleanField(default=False)

    def save(self, *args, **kwargs):

        if not self.pk:
            last_admin = Admin.objects.order_by('-id').first()
            next_id = 1 if not last_admin else last_admin.id + 1
            self.admin_id = f'adm_id_{next_id}'

        if not self.pk or Admin.objects.get(pk=self.pk).password != self.password:
            self.password = make_password(self.password)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.civilite} {self.prenom} {self.nom}"


