from rest_framework import serializers
from .models import Booking
from guests.models import Guest

class BookingSerializer(serializers.ModelSerializer):
    
    name = serializers.CharField(write_only=True)
    phone = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)

    class Meta:
        model = Booking
        fields = '__all__'

    def validate(self, data):
        room = data['room']
        check_in = data['check_in_date']
        check_out = data['check_out_date']

        if check_in >= check_out:
            raise serializers.ValidationError("Check-out must be after check-in")

        
        if Booking.objects.filter(
            room=room,
            check_in_date__lt=check_out,
            check_out_date__gt=check_in,
            status='booked'
        ).exists():
            raise serializers.ValidationError("Room already booked for these dates")

        return data

    def create(self, validated_data):
        
        name = validated_data.pop('name')
        phone = validated_data.pop('phone')
        email = validated_data.pop('email')

        room = validated_data['room']
        check_in = validated_data['check_in_date']
        check_out = validated_data['check_out_date']

       
        guest, _ = Guest.objects.get_or_create(
            phone=phone,
            defaults={
                "name": name,
                "email": email
            }
        )

        
        days = (check_out - check_in).days
        total_amount = days * float(room.price)

        
        booking = Booking.objects.create(
            guest=guest,
            total_amount=total_amount,
            **validated_data
        )

        return booking