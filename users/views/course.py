from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView, ListAPIView

from root.api_views import CustomUpdateAPIView, CustomDestroyAPIView
from users.models import Course
from users.permissions import IsSuperAdmin, IsAdmin
from users.serializer import CourseModelSerializer


@extend_schema(tags=['course'])
class CourseCreateAPIView(CreateAPIView):
    serializer_class = CourseModelSerializer
    permission_classes = [IsSuperAdmin | IsAdmin]


@extend_schema(tags=['course'])
class CourseListAPIView(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseModelSerializer
    permission_classes = [IsSuperAdmin | IsAdmin]


@extend_schema(tags=['course'])
class CourseUpdateAPIView(CustomUpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseModelSerializer
    permission_classes = [IsSuperAdmin | IsAdmin]
    lookup_field = 'pk'


@extend_schema(tags=['course'])
class CourseDestroyAPIView(CustomDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseModelSerializer
    permission_classes = [IsSuperAdmin | IsAdmin]
