import re

from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from root.serializers import CustomModelSerializer
from users.models import User, Group, Sessions, Course


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = getattr(user, 'role', None)
        token['is_superuser'] = getattr(user, 'is_superuser', False)
        return token


class UserModelSerializer(CustomModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'full_name', 'phone_number', 'group', 'date_joined', 'last_login', 'role', 'password', "avatar")
        read_only_fields = ('id', 'date_joined', 'last_login', "group")
        extra_kwargs = {
            'password': {"write_only": True}
        }

    def validate_phone_number(self, value):
        clean_phone = re.sub(r'\D', "", value)
        if 9 <= len(clean_phone) <= 15:
            return clean_phone
        else:
            raise ValidationError("Phone number is wrong")

    def validate_password(self, value):
        return make_password(value)


class UserUpdateModelSerializer(CustomModelSerializer):
    class Meta:
        model = User
        fields = ("id", "full_name", "phone_number", "group", "is_active", "role", "avatar")
        read_only_fields = ("id",)
        extra_kwargs = {
            "phone_number": {"required": False}
        }


class GroupUpdateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'group')
        read_only_fields = ('id',)


class GroupModelSerializer(CustomModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name', 'teacher', 'course')
        read_only_fields = ('id',)


class CourseModelSerializer(CustomModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'name')
        read_only_fields = ('id',)


class SessionModelSerializer(ModelSerializer):
    class Meta:
        model = Sessions
        fields = ('id', 'device_name', 'ip_address', 'user')
        read_only_fields = ('id',)
