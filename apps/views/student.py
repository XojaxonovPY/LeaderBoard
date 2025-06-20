from http import HTTPStatus

from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response

from apps.models import Homework, Submission, Grade
from apps.serializer import SubmissionModelSerialize, HomeworkModelSerializer, GradeModelSerializer,SubmissionFileModelSerializer
from auth_apps.models import User


@extend_schema(tags=['students'])
class SubmissionCreatAPIView(CreateAPIView):
    serializer_class = SubmissionModelSerialize

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(student=request.user)
        return Response(serializer.data, status=HTTPStatus.CREATED)


@extend_schema(tags=['students'])
class SubmissionListAPIView(ListAPIView):
    serializer_class = SubmissionModelSerialize
    queryset = Submission.objects.all()


@extend_schema(tags=['students'])
class HomeworkListAPIView(ListAPIView):
    serializer_class = HomeworkModelSerializer
    queryset = Homework.objects.all()



@extend_schema(tags=['students'])
class StudentLeaderboardAPIView(ListAPIView):
    serializer_class = GradeModelSerializer # yoki IsTeacher

    def get_queryset(self):
        return Grade.objects.filter(submission__student_id=self.request.user)


