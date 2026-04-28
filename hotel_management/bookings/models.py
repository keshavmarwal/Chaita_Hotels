from django.db import models
from Backend.Chaita_Hotels.hotel_management.accounts.models import User
from Backend.Chaita_Hotels.hotel_management.rooms.models import Room
from Backend.Chaita_Hotels.hotel_management.guests.models import Guest
# Create your models here.
class Booking(models.Model):
    STATUS_CHOICES = (
        ('booked', 'Booked'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, related_name='bookings',null=False, blank=True)

    check_in_date = models.DateField()
    check_out_date = models.DateField()

    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='booked')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - Room {self.room.room_number}"