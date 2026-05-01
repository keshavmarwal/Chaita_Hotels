from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Guest
from .serializers import GuestSerializer
from .serializers import GuestDetailSerializer


class GuestViewSet(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    permission_classes = [IsAuthenticated]  # ✅ sabko allow karo


class GuestDetailView(APIView):
    permission_classes = [IsAuthenticated]  # ✅ yeh bhi

    def get(self, request, pk):
        try:
            guest = Guest.objects.get(id=pk)
            serializer = GuestDetailSerializer(guest)
            return Response(serializer.data)
        except Guest.DoesNotExist:
            return Response({"error": "Guest not found"}, status=404)