from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView, ListAPIView

from root.api_views import CustomUpdateAPIView, CustomDestroyAPIView
from users.models import School
from users.permissions import IsSuperAdmin, IsAdmin
from users.serializer import SchoolModelSerializer


@extend_schema(tags=['course'])
class SchoolCreateAPIView(CreateAPIView):
    serializer_class = SchoolModelSerializer
    permission_classes = [IsSuperAdmin | IsAdmin]


@extend_schema(tags=['course'])
class SchoolListAPIView(ListAPIView):
    queryset = School.objects.all()
    serializer_class = SchoolModelSerializer
    permission_classes = [IsSuperAdmin | IsAdmin]


@extend_schema(tags=['course'])
class SchoolUpdateAPIView(CustomUpdateAPIView):
    queryset = School.objects.all()
    serializer_class = SchoolModelSerializer
    permission_classes = [IsSuperAdmin | IsAdmin]
    lookup_field = 'pk'


@extend_schema(tags=['course'])
class SchoolDestroyAPIView(CustomDestroyAPIView):
    queryset = School.objects.all()
    serializer_class = SchoolModelSerializer
    permission_classes = [IsSuperAdmin | IsAdmin]
