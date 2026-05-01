from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import MenuItem, Order
from .serializers import MenuItemSerializer, OrderSerializer



# 🔹 Menu CRUD
class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated]


# 🔹 Create Order
class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = OrderSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "Order created", "data": serializer.data})

        return Response(serializer.errors, status=400)


# 🔹 Get All Orders
class OrderListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.prefetch_related("items__menu_item").all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


# 🔹 Generate Bill
class GenerateBillView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        try:
            order = Order.objects.prefetch_related("items__menu_item").get(id=order_id)

            total = 0
            items_data = []

            for item in order.items.all():
                item_total = item.menu_item.price * item.quantity
                total += item_total

                items_data.append({
                    "name": item.menu_item.name,
                    "price": item.menu_item.price,
                    "quantity": item.quantity,
                    "total": item_total
                })

            return Response({
                "order_id": order.id,
                "items": items_data,
                "total_bill": total
            })

        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=404)