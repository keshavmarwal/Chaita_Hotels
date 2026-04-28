from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from .models import Guest
from .serializers import GuestSerializer
from .serializers import GuestDetailSerializer



# Create your views here.
class GuestViewSet(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    
class GuestDetailView(APIView):
    def get(self, request, pk):
        guest = Guest.objects.get(id=pk)
        serializer = GuestDetailSerializer(guest)
        return Response(serializer.data)