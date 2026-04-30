from django.db import models
from decimal import Decimal
from django.db.models import Sum, F
from restaurant.models import OrderItem

class Bill(models.Model):
    booking = models.ForeignKey("bookings.Booking", on_delete=models.CASCADE)

    room_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    food_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def calculate_bill(self):
        booking = self.booking

        # 👉 correct fields
        days = (booking.check_out_date - booking.check_in_date).days
        if days <= 0:
            days = 1

        # 👉 room charges
        price_per_day = booking.room.price
        self.room_charges = days * price_per_day

        # 👉 food charges (FIXED)
        food_total = OrderItem.objects.filter(
            order__booking=booking
        ).aggregate(
            total=Sum(F("quantity") * F("menu_item__price"))
        )["total"] or Decimal('0.00')

        self.food_charges = food_total

        # 👉 tax
        self.tax = Decimal('0.1') * (self.room_charges + self.food_charges)

        # 👉 total
        self.total_amount = self.room_charges + self.food_charges + self.tax

    def save(self, *args, **kwargs):
        self.calculate_bill()
        super().save(*args, **kwargs)