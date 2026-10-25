from django.db.models import Sum, F, Q
from django.db.models.functions import Coalesce
from django.http.response import JsonResponse
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from apps.models import Submission
from root.api_views import CustomUpdateAPIView, CustomDestroyAPIView
from users.models import User, Group
from users.permissions import IsAdmin, IsSuperAdmin
from users.serializer import UserModelSerializer, GroupModelSerializer
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
            if request.user.token.get("is_superuser") != User.is_superuser:
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
    permission_classes = [IsAdmin]

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
    permission_classes = [IsAdmin]
    lookup_field = 'pk'


@extend_schema(tags=["admin"])
class UserUpdateAPIView(CustomUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateModelSerializer
    permission_classes = [IsAdmin]


@extend_schema(tags=["admin"])
class UserDestroyAPIView(CustomDestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsSuperAdmin]


@extend_schema(tags=['groups'])
class GroupModelViewSet(ModelViewSet):
    serializer_class = GroupModelSerializer
    queryset = Group.objects.all()
    permission_classes = [IsAdmin]


# ===========================================================================


@extend_schema(tags=['admin-user'])
class LeaderboardAPIView(APIView):
    def get(self, request, pk):
        leaderboard = (
            Submission.objects
            .filter(student__group_id=pk)
            .values('student__id', 'student__full_name')
            .annotate(
                final_score=Coalesce(Sum('final_grade'), 0),
                ai_score=Coalesce(Sum('ai_grade'), 0),
                total_score=F('final_score') + F('ai_score')
            )
            .order_by('-total_score')
        )
        return Response(leaderboard)
