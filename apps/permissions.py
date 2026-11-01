from rest_framework.permissions import BasePermission

from users.models import User


class IsTeacher(BasePermission):
    message = 'You are not a teacher'

    def has_permission(self, request, view):
        user = request.user
        if not user:
            return False
        token = getattr(user, "token", None)
        if not token:
            return False
        return bool(token.get("role") == User.RoleType.Teacher)
