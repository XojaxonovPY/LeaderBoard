from drf_spectacular.utils import extend_schema
from rest_framework.viewsets import ModelViewSet

from apps.serializer import GradeModelSerializer
from auth_apps.models import User, Group
from auth_apps.permissions import IsAdmin
from auth_apps.serializer import UserProfileSerializer, GroupModelSerializer, GroupUpdateSerializer
from rest_framework.generics import RetrieveAPIView, UpdateAPIView, ListAPIView


@extend_schema(tags=['admin-teachers'])
class TeacherModelViewSet(ModelViewSet):
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()


@extend_schema(tags=['admin-students'])
class StudentModelViewSet(ModelViewSet):
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdmin]


@extend_schema(tags=['admin-groups'])
class GroupModelViewSet(ModelViewSet):
    serializer_class = GroupModelSerializer
    queryset = Group.objects.all()
    permission_classes = [IsAdmin]


@extend_schema(tags=['admin'])
class GroupRetrieveAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = GradeModelSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'pk'

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(group=self.kwargs['pk'])
        return query

@extend_schema(tags=['admin'])
class TeacherUpdateAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = GroupUpdateSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'pk'


@extend_schema(tags=['admin'])
class StudentUpdateAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = GroupUpdateSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'pk'
