from typing import Any

from django.db import transaction
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.request import Request

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


@extend_schema(tags=['group'], parameters=[OpenApiParameter(name='action', enum=["append", "replace"])])
class GroupUpdateAPIView(CustomUpdateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupModelSerializer
    permission_classes = [IsSuperAdmin | IsAdmin]
    lookup_field = 'pk'

    @transaction.atomic
    def update(self: Any, request: Request, *args: Any, **kwargs: Any):
        response = super().update(request, *args, **kwargs)
        if "student" in request.data:
            ThroughModel = Group.student.through
            lookup_value = kwargs[self.lookup_field]
            student_ids = request.data.get("student") or []
            action = request.query_params.get("action", "replace").lower()
            through_data = [
                ThroughModel(group_id=lookup_value, user_id=student_id)
                for student_id in student_ids
            ]
            if action == "replace":
                ThroughModel.objects.filter(group_id=lookup_value).delete()
                if through_data:
                    ThroughModel.objects.bulk_create(through_data)
            elif action == "append" and through_data:
                ThroughModel.objects.bulk_create(through_data, ignore_conflicts=True)
        return response


@extend_schema(tags=['group'])
class GroupDestroyAPIView(CustomDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupModelSerializer
    permission_classes = [IsSuperAdmin | IsAdmin]
