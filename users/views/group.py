from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView, ListAPIView

from root.api_views import CustomUpdateAPIView, CustomDestroyAPIView
from users.models import Group
from users.permissions import IsSuperAdmin, IsAdmin
from users.serializer import GroupModelSerializer


@extend_schema(tags=['group'])
class GroupCreateAPIView(CreateAPIView):
    serializer_class = GroupModelSerializer
    permission_classes = [IsSuperAdmin | IsAdmin]


@extend_schema(tags=['group'])
class GroupListAPIView(ListAPIView):
    queryset = Group.objects.all().select_related("school", "teacher")
    serializer_class = GroupModelSerializer
    permission_classes = [IsSuperAdmin | IsAdmin]


@extend_schema(tags=['group'])
class GroupUpdateAPIView(CustomUpdateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupModelSerializer
    permission_classes = [IsSuperAdmin | IsAdmin]
    lookup_field = 'pk'


@extend_schema(tags=['group'])
class GroupDestroyAPIView(CustomDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupModelSerializer
    permission_classes = [IsSuperAdmin | IsAdmin]
