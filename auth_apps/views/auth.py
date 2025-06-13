from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView

from auth_apps.models import User
from auth_apps.serializer import RegisterModelSerializer


@extend_schema(tags=['Auth'])
class RegisterCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterModelSerializer









