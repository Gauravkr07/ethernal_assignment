from rest_framework.permissions import BasePermission

class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Manager').exists()

class IsSupervisor(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Supervisor').exists()

class IsOperator(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Operator').exists()
