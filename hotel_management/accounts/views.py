from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password
from .models import User
from .permissions import IsAdmin ,IsReceptionist  , IsHR ,IsManager
from .serializers import UserSerializer
from .serializers import CustomTokenSerializer

class TestAdminView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        return Response({"msg": "Admin access only"})

class TestReceptionistView(APIView):
    permission_classes = [IsAuthenticated, IsReceptionist]

    def get(self, request):
        return Response({"msg": "Receptionist access"})
    
class TestHRView(APIView):
    permision_classes = [IsAuthenticated , IsHR]

    def get(self, request):
        return Response({"msg": "HR access"})

class TestManagerView(APIView):
    permision_classes = [IsAuthenticated , IsManager]

    def get(self, request):
        return Response({"msg": "Manager access"})




class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenSerializer

class UserListCreateView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "User created"})
        return Response(serializer.errors, status=400)
    
class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def put(self, request, pk):
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "User updated"})
        return Response(serializer.errors, status=400)
    
class UserDeactivateView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def patch(self, request, pk):
        try:
            user = User.objects.get(id=pk)
            user.status = not user.status
            user.save()
            return Response({"msg": "User deactivated"})
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)