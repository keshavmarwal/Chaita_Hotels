from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from Backend.Chaita_Hotels.hotel_management.accounts.permissions import IsAdmin, IsReceptionist
from .serializers import BookingSerializer
from .models import Booking

class BookingCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        
        if request.user.role not in ["ADMIN", "RECEPTIONIST"]:
            return Response({"error": "Permission denied"}, status=403)

        serializer = BookingSerializer(data=request.data)

        if serializer.is_valid():
            
            serializer.save(user=request.user)
            return Response({
                "msg": "Booking created",
                "data": serializer.data
            })

        return Response(serializer.errors, status=400)
    
class CheckInView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        if request.user.role not in ["ADMIN", "RECEPTIONIST"]:
            return Response({"error": "Permission denied"}, status=403)

        try:
            booking = Booking.objects.get(id=pk)

            if booking.status != "booked":
                return Response({"error": "Invalid booking status"}, status=400)

            
            booking.status = "checked_in"
            booking.room.is_available = False

            booking.room.save()
            booking.save()

            return Response({"msg": "Check-in successful"})

        except Booking.DoesNotExist:
            return Response({"error": "Booking not found"}, status=404)
        
class CheckOutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        if request.user.role not in ["ADMIN", "RECEPTIONIST"]:
            return Response({"error": "Permission denied"}, status=403)

        try:
            booking = Booking.objects.get(id=pk)

            if booking.status != "checked_in":
                return Response({"error": "Guest not checked-in"}, status=400)

            
            booking.status = "completed"
            booking.room.is_available = True

            booking.room.save()
            booking.save()

            return Response({
                "msg": "Check-out successful",
                "total_bill": booking.total_amount
            })

        except Booking.DoesNotExist:
            return Response({"error": "Booking not found"}, status=404)
        
class BookingListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            print("USER:", request.user)
            print("ROLE:", request.user.role)

            if request.user.role not in ["ADMIN", "RECEPTIONIST"]:
                return Response({"error": "Permission denied"}, status=403)

            bookings = Booking.objects.select_related('room', 'guest', 'user').all()

            data = []
            for b in bookings:
                data.append({
                    "id": b.id,
                    "guest_name": b.guest.name,
                    "room_number": b.room.room_number,
                    "status": b.status
                })

            return Response(data)

        except Exception as e:
            return Response({"error": str(e)}, status=500)