from rest_framework import serializers
from .models import Guest
from bookings.serializers import BookingSerializer



class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = '__all__'


class GuestDetailSerializer(serializers.ModelSerializer):
    bookings = BookingSerializer(many=True, read_only=True)

    class Meta:
        model = Guest
        fields = ['id', 'name', 'phone', 'email', 'bookings']
