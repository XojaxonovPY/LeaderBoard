from django.db.models import Sum
from drf_spectacular.utils import extend_schema
from rest_framework.generics import UpdateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from apps.models import Submission
from auth_apps.models import User, Group, Course
from auth_apps.permissions import IsAdmin
from auth_apps.serializer import CourseModelSerializer, GroupUpdateSerializer
from auth_apps.serializer import UserProfileSerializer, GroupModelSerializer


@extend_schema(tags=['admin-teachers'])
class TeacherModelViewSet(ModelViewSet):
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdmin]

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(role=User.RoleType.Teacher)
        return query


@extend_schema(tags=['admin-students'])
class StudentModelViewSet(ModelViewSet):
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdmin]

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(role=User.RoleType.Student)
        return query


@extend_schema(tags=['admin-groups'])
class GroupModelViewSet(ModelViewSet):
    serializer_class = GroupModelSerializer
    queryset = Group.objects.all()
    permission_classes = [IsAdmin]


@extend_schema(tags=['admin-course'])
class CourseModelViewSet(ModelViewSet):
    queryset = Course.objects.all()
    http_method_names = ['get', 'post', 'delete']
    serializer_class = CourseModelSerializer
    permission_classes = [IsAdmin]


# ===========================================================================

@extend_schema(tags=['admin'])
class TeacherUpdateAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = GroupUpdateSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'pk'


@extend_schema(tags=['admin'])
class StudentUpdateAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = GroupUpdateSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'pk'


@extend_schema(tags=['admin'])
class LeaderboardAPIView(APIView):
    def get(self, request, pk):
        leaderboard = (
            Submission.objects
            .filter(student__group_id=pk)
            .values('student__id', 'student__full_name')
            .annotate(total_score=Sum('final_grade'))
            .order_by('-total_score')
        )
        return Response(leaderboard)
