from rest_framework.permissions import BasePermission

from auth_apps.models import User


class IsTeacher(BasePermission):
    message = 'You are not a teacher'

    def has_permission(self, request, view):
        return bool(request.user and request.user.role == User.RoleType.Teacher)
