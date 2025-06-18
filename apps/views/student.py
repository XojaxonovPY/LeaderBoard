from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView, ListAPIView

from apps.models import Homework, Submission, Grade
from apps.serializer import SubmissionModelSerialize, HomeworkModelSerializer, GradeModelSerializer
from auth_apps.models import User


@extend_schema(tags=['students'])
class SubmissionCreatAPIView(CreateAPIView):
    serializer_class = SubmissionModelSerialize


@extend_schema(tags=['students'])
class SubmissionListAPIView(ListAPIView):
    serializer_class = SubmissionModelSerialize
    queryset = Submission.objects.all()


@extend_schema(tags=['students'])
class HomeworkListAPIView(ListAPIView):
    serializer_class = HomeworkModelSerializer
    queryset = Homework.objects.all()



@extend_schema(tags=['admin'])
class StudentLeaderboardAPIView(ListAPIView):
    serializer_class = GradeModelSerializer # yoki IsTeacher

    def get_queryset(self):
        return Grade.objects.filter(submission__student_id=self.request.user)


