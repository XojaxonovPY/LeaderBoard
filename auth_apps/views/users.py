from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView, RetrieveAPIView
from auth_apps.models import User
from auth_apps.serializer import UserProfileSerializer


@extend_schema(tags=['User'])
class StudentsListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer



@extend_schema(tags=['User'])
class UserProfileRetrieveAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user
