from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Bill
from .serializers import BillSerializer

# ✅ Existing ViewSet (rakhlo as is)
class BillViewSet(ModelViewSet):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    permission_classes = [IsAuthenticated]

# ✅ Generate bill for a booking
class GenerateBillView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, booking_id):
        try:
            # Pehle check karo bill already exist karta hai kya
            bill, created = Bill.objects.get_or_create(booking_id=booking_id)
            bill.calculate_bill()
            bill.save()

            return Response({
                "msg": "Bill generated successfully",
                "bill_id": bill.id,
                "room_charges": bill.room_charges,
                "food_charges": bill.food_charges,
                "tax": bill.tax,
                "total_amount": bill.total_amount,
            })

        except Exception as e:
            return Response({"error": str(e)}, status=400)

# ✅ Get bill details
class BillDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, booking_id):
        try:
            bill = Bill.objects.get(booking_id=booking_id)

            return Response({
                "bill_id": bill.id,
                "booking_id": booking_id,
                "room_charges": bill.room_charges,
                "food_charges": bill.food_charges,
                "tax": bill.tax,
                "total_amount": bill.total_amount,
            })

        except Bill.DoesNotExist:
            return Response({"error": "Bill not found"}, status=404)