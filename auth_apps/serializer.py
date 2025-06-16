from rest_framework import viewsets
from rest_framework.serializers import ModelSerializer

from apps.models import Submission
from auth_apps.models import User, Group


class SubmissionSerializer(ModelSerializer):
    class Meta:
        model = Submission
        fields = ('score',)


class UserProfileSerializer(ModelSerializer):
    submissions = SubmissionSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'full_name',
            'phone',
            'group',
            'level',
            'date_joined',
            'last_login',
            'submissions'
        )


class GroupModelSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = ('name', 'teacher')


class TeacherUserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()  # Asosiy queryset
