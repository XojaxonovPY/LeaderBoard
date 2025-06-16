import re

from django.contrib.auth.hashers import make_password
from rest_framework.serializers import ModelSerializer

from apps.models import Submission
from auth_apps.models import User, UserBadge, Group


class RegisterModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'full_name', 'password', 'phone', 'course', 'role')
        read_only_fields = ('id', 'role')

    def validate_password(self, value):
        return make_password(value)

    def validate_phone(self, value):
        return re.sub(r'\D', '', value)


class BadgeSerializer(ModelSerializer):
    class Meta:
        model = UserBadge
        fields = ('badge',)


class SubmissionSerializer(ModelSerializer):
    class Meta:
        model = Submission
        fields = ('score',)


class UserProfileSerializer(ModelSerializer):
    submissions = SubmissionSerializer(many=True, read_only=True)
    badges = BadgeSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'full_name',
            'phone',
            'course',
            'level',
            'badges',
            'date_joined',
            'last_login',
            'submissions'
        )



class GroupModelSerializer(ModelSerializer):
    class Meta:
        model=Group
        fields=('name','teacher')