from rest_framework.permissions import BasePermission


class SuperAdminPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        current_user = request.user
        if current_user.client == obj and current_user.role == 2:
            return True
        elif current_user.role == 3:
            return True
        else:
            return False


class SystemAdminPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        current_user = request.user
        return current_user.role == 3
