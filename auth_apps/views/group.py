from drf_spectacular.utils import extend_schema
from rest_framework.generics import UpdateAPIView, RetrieveAPIView
from rest_framework.viewsets import ModelViewSet

from auth_apps.models import User, Group
from auth_apps.permissions import IsAdmin
from auth_apps.serializer import UserProfileSerializer, GroupModelSerializer


@extend_schema(tags=['groups'])
class StudentModelViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAdmin]

@extend_schema(tags=['groups'])
class GroupUpdateAPIView(UpdateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupModelSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'pk'

@extend_schema(tags=['groups'])
class TeacherUpdateAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'pk'



class GroupRetrieveView(RetrieveAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupModelSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'pk'
