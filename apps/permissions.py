from rest_framework.permissions import BasePermission

from users.models import User


class IsTeacher(BasePermission):
    message = 'You are not a teacher'

    def has_permission(self, request, view):
        return bool(request.user and request.user.role == User.RoleType.Teacher)
