from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView, ListAPIView

from apps.models import Homework, Submission
from apps.serializer import SubmissionModelSerialize, HomeworkModelSerializer


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

