from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets , status
from .models import Room
from .serializers import RoomSerializer
from accounts.permissions import IsAdminOrManager , IsReceptionist

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAdminOrManager | IsReceptionist]
    def create(self, request, *args, **kwargs):
        total_rooms = Room.objects.count()

        if total_rooms >106:
            return Response(
                {"error": "Maximum 106 rooms allowed"},
                status=status.HTTP_400_BAD_REQUEST)
        
        return super().create(request, *args, **kwargs)
    
    
# Create your views here. 
