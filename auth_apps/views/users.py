from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.generics import ListAPIView, RetrieveAPIView
from auth_apps.models import User
from auth_apps.serializer import UserProfileSerializer, TeacherUserProfileViewSet


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

@extend_schema(tags=['parking-zones'])
class TeacherModelViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = TeacherUserProfileViewSet



