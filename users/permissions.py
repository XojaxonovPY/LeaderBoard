from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView

from users.models import User


class IsAdmin(BasePermission):
    message = 'You are not an admin'

    def has_permission(self, request: Request, view: APIView):
        user = request.user
        if not user:
            return False
        token = getattr(user, "token", None)
        if not token:
            return False
        return bool(token.get("role") == User.RoleType.Admin)


class IsSuperAdmin(BasePermission):
    message = 'You are not a super admin'

    def has_permission(self, request: Request, view: APIView):
        user = request.user
        if not user:
            return False
        token = getattr(user, "token", None)
        if not token:
            return False
        return bool(token.get("is_superuser", False))
