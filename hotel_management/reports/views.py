from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from Backend.Chaita_Hotels.hotel_management.rooms.models import Room
from Backend.Chaita_Hotels.hotel_management.bookings.models import Booking
from django.db.models import Sum
from Backend.Chaita_Hotels.hotel_management.accounts.permissions import IsAdminOrManager
# Create your views here.
class DashboardView(APIView):
    permission_classes= [IsAdminOrManager]
    def get(self, request):
        total_rooms = Room.objects.count()
        total_bookings = Booking.objects.count()
        active_bookings = Booking.objects.filter(status='booked').count()

        total_revenue = Booking.objects.filter(
            status='booked'
        ).aggregate(total=Sum('total_amount'))['total'] or 0

        return Response({
            "total_rooms": total_rooms,
            "total_bookings": total_bookings,
            "active_bookings": active_bookings,
            "total_revenue": total_revenue
        })