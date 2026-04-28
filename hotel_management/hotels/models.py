from django.db import models

# Create your models here.

class Hotel(models.Model):
        
    name = models.CharField(max_length=101)
    address = models.TextField()
    phone = models.CharField(max_length=21)
    email = models.EmailField()
    max_rooms = models.IntegerField(default=106)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name