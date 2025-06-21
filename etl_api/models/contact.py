from django.db import models

class ContactForm(models.Model):
    is_parent = models.BooleanField(default=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    message = models.TextField()

    def __str__(self):
        return f"{self.name} {self.surname}"
