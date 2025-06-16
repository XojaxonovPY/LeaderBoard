from rest_framework.generics import CreateAPIView

from apps.serializer import SubmissionModelSerialize


class SubmissionCreatAPIView(CreateAPIView):
    serializer_class = SubmissionModelSerialize
