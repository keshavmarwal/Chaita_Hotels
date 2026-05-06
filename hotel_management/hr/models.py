from django.db import models
from accounts.models import User

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=50)  # Receptionist, Chef, etc.
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    joining_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Shift(models.Model):
    SHIFT_CHOICES = [
        ("morning", "Morning"),
        ("evening", "Evening"),
        ("night", "Night"),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="shifts")
    shift_type = models.CharField(max_length=20, choices=SHIFT_CHOICES)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.employee.name} - {self.shift_type} - {self.date}"


class Attendance(models.Model):
    STATUS_CHOICES = [
        ("present", "Present"),
        ("absent", "Absent"),
        ("late", "Late"),
        ("half_day", "Half Day"),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="attendance")
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ["employee", "date"]  # ek din mein ek hi record

    def __str__(self):
        return f"{self.employee.name} - {self.date} - {self.status}"