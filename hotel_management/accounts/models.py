from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('RECEPTIONIST', 'Receptionist'),
        ('MANAGER', 'Manager'),
        ('RESTAURANT', 'Restaurant'),
        ('HR', 'HR'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    status = models.BooleanField(default=True)  # active/inactive

    def __str__(self):
        return self.username
