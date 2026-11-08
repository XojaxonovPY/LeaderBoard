from django.db.models import Sum, F, Q
from django.db.models.functions import Coalesce
from django.http.response import JsonResponse
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.models import Submission
from root.api_views import CustomUpdateAPIView, CustomDestroyAPIView
from users.models import User
from users.permissions import IsAdmin, IsSuperAdmin
from users.serializer import UserModelSerializer
from users.serializer import UserUpdateModelSerializer


@extend_schema(tags=["admin"])
class UserCreateAPIView(CreateAPIView):
    serializer_class = UserModelSerializer
    permission_classes = [IsSuperAdmin | IsAdmin]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        role = serializer.validated_data.get('role')
        if role == User.RoleType.Admin.value:
            if not request.user.token.get("is_superuser"):
                return JsonResponse(
                    status=status.HTTP_403_FORBIDDEN,
                    data={
                        "success": False,
                        "message": "You are not create admin or super admin",
                        "errors": f"The error role is {role}"
                    }
                )
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


@extend_schema(tags=["admin"])
class UserListAPIView(ListAPIView):
    queryset = User.objects.all().defer("is_staff", "is_superuser", "user_permissions")
    serializer_class = UserModelSerializer
    permission_classes = [IsAdmin | IsSuperAdmin]

    def get_queryset(self):
        query = super().get_queryset()
        if self.request.user.token.get("is_superuser") == False:
            query = query.filter(Q(role=User.RoleType.Teacher.value) | Q(role=User.RoleType.Student.value))
            return query
        return query


@extend_schema(tags=["admin"])
class UserRetrieveAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    permission_classes = [IsAdmin | IsSuperAdmin]
    lookup_field = 'pk'


@extend_schema(tags=["admin"])
class UserUpdateAPIView(CustomUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateModelSerializer
    permission_classes = [IsAdmin | IsSuperAdmin]


@extend_schema(tags=["admin"])
class UserDestroyAPIView(CustomDestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsSuperAdmin]


# ===========================================================================