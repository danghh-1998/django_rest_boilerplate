from rest_framework.permissions import BasePermission


class OwnerPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        current_user = request.user
        return current_user == obj


class UserPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        current_user = request.user
        if current_user == obj:
            return True
        elif current_user.role == 3:
            return True
        else:
            return current_user.role >= obj.role and current_user.client == obj.client


class AdminPermission(BasePermission):
    def has_permission(self, request, view):
        current_user = request.user
        return current_user.role > 0


class SuperAdminPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        current_user = request.user
        if current_user.role == 3:
            return True
        elif current_user.role == 2 and current_user.client == obj.client:
            return True
        else:
            return False
