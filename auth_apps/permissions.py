from rest_framework.permissions import BasePermission

from auth_apps.models import User


class IsAdmin(BasePermission):
    message = 'You are not an admin'

    def has_permission(self, request, view):
        if not request.user:
            return False
        return bool(request.user and request.user.role == User.RoleType.Admin)
