from http import HTTPStatus

from django.db.models import Sum, F
from django.db.models.functions import Coalesce
from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from apps.models import Homework, Submission
from apps.permissions import IsTeacher
from apps.serializer import HomeworkModelSerializer, SubmissionModelSerializer
from auth_apps.models import Group
from auth_apps.serializer import GroupModelSerializer


@extend_schema(tags=['teachers-homework'])
class TeacherModelViewSet(ModelViewSet):
    queryset = Homework.objects.all()
    serializer_class = HomeworkModelSerializer
    permission_classes = [IsTeacher]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(teacher=request.user)
        return Response(serializer.data, status=HTTPStatus.CREATED)


# ============================================================================
@extend_schema(tags=['teachers'])
class TeacherGroupListAPIView(ListAPIView):
    serializer_class = GroupModelSerializer
    queryset = Group.objects.all()
    permission_classes = [IsTeacher]

    def get_queryset(self):
        return self.queryset.filter(teacher=self.request.user)


@extend_schema(tags=['teachers'])
class TeacherSubmissionsListAPIView(ListAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionModelSerializer
    permission_classes = [IsTeacher]

    def get_queryset(self):
        group_id = self.kwargs.get('pk')
        return Submission.objects.filter(homework__group_id=group_id)


@extend_schema(tags=['teachers'])
class TeacherSubmissionsUpdateAPIView(UpdateAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionModelSerializer
    permission_classes = [IsTeacher]
    lookup_field = 'pk'


@extend_schema(tags=['teachers'])
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
