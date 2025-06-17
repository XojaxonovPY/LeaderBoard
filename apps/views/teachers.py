from drf_spectacular.utils import extend_schema
from rest_framework.viewsets import ModelViewSet

from apps.models import Homework
from apps.permissions import IsTeacher
from apps.serializer import HomeworkModelSerializer


@extend_schema(tags=['teachers-homework'])
class TeacherModelViewSet(ModelViewSet):
    queryset = Homework.objects.all()
    serializer_class = HomeworkModelSerializer
    permission_classes = [IsTeacher]



