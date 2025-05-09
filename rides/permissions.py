from rest_framework.permissions import BasePermission

class IsDriver(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_driver
    
class IsPassenger(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and not request.user.is_driver