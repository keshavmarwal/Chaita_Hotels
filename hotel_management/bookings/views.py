from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsAdmin, IsReceptionist, IsRestaurant
from .serializers import BookingSerializer
from .models import Booking
from guests.models import Guest

class BookingCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role not in ["ADMIN", "RECEPTIONIST"]:
            return Response({"error": "Permission denied"}, status=403)

        data = request.data

        try:
            guest_id = data.get("guest_id")

            if guest_id:
                guest = Guest.objects.get(id=guest_id)
            else:
                guest = Guest.objects.create(
                    name=data.get("guest_name"),
                    phone=data.get("guest_phone")
                )

            booking = Booking.objects.create(
                user=request.user,
                room_id=data.get("room"),
                guest=guest,
                check_in_date=data.get("check_in_date"),
                check_out_date=data.get("check_out_date"),
                total_amount=data.get("total_amount")
            )

            booking.room.is_available = False
            booking.room.save()

            return Response({"msg": "Booking created", "booking_id": booking.id})

        except Exception as e:
            return Response({"error": str(e)}, status=400)


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

            return Response({"msg": "Check-out successful", "total_bill": booking.total_amount})

        except Booking.DoesNotExist:
            return Response({"error": "Booking not found"}, status=404)


class BookingListView(APIView):
    permission_classes = [IsAuthenticated]  # ✅ FIXED

    def get(self, request):
        try:
            # ✅ RESTAURANT ko checked_in bookings milti hain
            if request.user.role == "RESTAURANT":
                bookings = Booking.objects.select_related('room', 'guest').filter(
                    status="checked_in"
                )
            elif request.user.role in ["ADMIN", "RECEPTIONIST"]:
                bookings = Booking.objects.select_related('room', 'guest', 'user').all()
            else:
                return Response({"error": "Permission denied"}, status=403)

            data = []
            for b in bookings:
                data.append({
                    "id": b.id,
                    "guest_name": b.guest.name,
                    "guest_id": b.guest.id,  # ✅ ADDED
                    "room_number": b.room.room_number,
                    "status": b.status
                })

            return Response(data)

        except Exception as e:
            return Response({"error": str(e)}, status=500)