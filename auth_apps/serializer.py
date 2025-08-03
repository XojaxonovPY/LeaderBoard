from django.contrib.auth.hashers import make_password
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from auth_apps.models import User, Group, Sessions, Course


class UserProfileSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'full_name', 'phone', 'group', 'date_joined', 'last_login', 'role', 'password')
        read_only_fields = ('id', 'date_joined', 'last_login')

    def validate_phone(self, value):
        if len(value) >= 10:
            return value
        else:
            raise ValidationError("Phone number is wrong")

    def validate_password(self, value):
        return make_password(value)


class GroupUpdateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'group')
        read_only_fields = ('id',)


class GroupModelSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name', 'teacher', 'course')
        read_only_fields = ('id',)


class TeacherUserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()


class CourseModelSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'name')
        read_only_fields = ('id',)


class SessionModelSerializer(ModelSerializer):
    class Meta:
        model = Sessions
        fields = ('id', 'device_name', 'ip_address', 'user')
        read_only_fields = ('id',)
