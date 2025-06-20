from rest_framework import viewsets
from rest_framework.serializers import ModelSerializer

from auth_apps.models import User, Group


class UserProfileSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'full_name', 'phone', 'group', 'level', 'date_joined', 'last_login')


class GroupUpdateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('group',)


class GroupModelSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = ('name', 'teacher', 'course')
        read_only_fields = ('id',)


class TeacherUserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()  # Asosiy queryset

