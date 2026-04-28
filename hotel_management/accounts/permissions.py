from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.role == "ADMIN"


class IsReceptionist(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.role == "RECEPTIONIST"


class IsManager(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.role == "MANAGER"
    

class IsHR(BasePermission):
    def has_permission(self,request ,view):
        if not request.user.is_authenticated:
            return False
        return request.user.role == "HR"
    

class IsAdminOrReceptionist(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.role in ['ADMIN', 'RECEPTIONIST']
    
class IsAdminOrManager(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.role in ['ADMIN', 'MANAGER']