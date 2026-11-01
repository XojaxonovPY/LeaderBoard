from http import HTTPStatus

from django.db.models import Sum, F
from django.db.models.functions import Coalesce
from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView, UpdateAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from apps.models import Assignment, Submission, Lesson
from apps.permissions import IsTeacher
from apps.serializer import HomeworkModelSerializer, SubmissionModelSerializer, LessonModelSerializer, \
    LessonUpdateSerializer, SourceModelSerializer
from root.api_views import CustomUpdateAPIView, CustomDestroyAPIView
from users.models import Group, User
from users.serializer import GroupModelSerializer


@extend_schema(tags=["teacher-lessons"])
class LessonCreateAPIView(CreateAPIView):
    serializer_class = LessonModelSerializer
    permission_classes = [IsTeacher]

    def perform_create(self, serializer):
        serializer.validated_data["teacher_id"] = self.request.user.id
        serializer.save()


@extend_schema(tags=["teacher-lessons"])
class LessonListAPIView(ListAPIView):
    queryset = Lesson.objects.all().prefetch_related("group", "sources").select_related("teacher")
    serializer_class = LessonModelSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.token.get("role") == User.RoleType.Student.value:
            queryset = queryset.exclude(status=Lesson.StatusTextChoices.DRAFT.value)
        return queryset


@extend_schema(tags=["teacher-lessons"])
class LessonUpdateAPIView(CustomUpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonUpdateSerializer
    permission_classes = [IsTeacher]
    lookup_field = 'pk'


@extend_schema(tags=["teacher-lessons"])
class LessonDestroyAPIView(CustomDestroyAPIView):
    queryset = Lesson.objects.all()
    lookup_field = 'pk'
    permission_classes = [IsTeacher]


@extend_schema(tags=["teacher-lessons"])
class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonModelSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.token.get("role") == User.RoleType.Student.value:
            queryset = queryset.exclude(status=Lesson.StatusTextChoices.DRAFT.value)
        return queryset


@extend_schema(tags=["teacher-lessons"])
class SourceCreateAPIView(CreateAPIView):
    serializer_class = SourceModelSerializer


# ============================================================================

@extend_schema(tags=['teachers-homework'])
class TeacherModelViewSet(ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = HomeworkModelSerializer
    permission_classes = [IsTeacher]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(teacher=request.user)
        return Response(serializer.data, status=HTTPStatus.CREATED)


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
