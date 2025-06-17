from rest_framework.generics import CreateAPIView, ListAPIView

from apps.models import Homework, Submission
from apps.serializer import SubmissionModelSerialize, HomeworkModelSerializer


class SubmissionCreatAPIView(CreateAPIView):
    serializer_class = SubmissionModelSerialize


class SubmissionListAPIView(ListAPIView):
    serializer_class = SubmissionModelSerialize
    queryset = Submission.objects.all()

class HomeworkListAPIView(ListAPIView):
    serializer_class = HomeworkModelSerializer
    queryset = Homework.objects.all()

