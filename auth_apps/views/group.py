from drf_spectacular.utils import extend_schema
from rest_framework.viewsets import ModelViewSet

from auth_apps.models import User, Group
from auth_apps.permissions import IsAdmin
from auth_apps.serializer import UserProfileSerializer, GroupModelSerializer
from rest_framework.generics import RetrieveAPIView, UpdateAPIView


@extend_schema(tags=['admin'])
class TeacherModelViewSet(ModelViewSet):
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()


@extend_schema(tags=['admin'])
class StudentModelViewSet(ModelViewSet):
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdmin]


@extend_schema(tags=['admin'])
class GroupModelViewSet(ModelViewSet):
    serializer_class = GroupModelSerializer
    queryset = Group.objects.all()
    permission_classes = [IsAdmin]


@extend_schema(tags=['admin'])
class GroupRetrieveAPIView(RetrieveAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupModelSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'pk'


@extend_schema(tags=['admin'])
class TeacherUpdateAPIView(UpdateAPIView):
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdmin]
    lookup_field = 'pk'


@extend_schema(tags=['admin'])
class GroupUpdateAPIView(UpdateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupModelSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'pk'
