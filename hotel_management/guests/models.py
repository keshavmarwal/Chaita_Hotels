from django.db import models

class Guest(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, unique=True)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return self.name
