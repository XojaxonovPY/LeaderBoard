import re

from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from apps.models import Submission
from auth_apps.models import User


class RegisterModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'full_name', 'password', 'phone', 'course', 'role')
        read_only_fields = ('id', 'role')

    def validate_password(self, value):
        return make_password(value)

    def validate_phone(self, value):
        return re.sub(r'\D', '', value)


class StudentListSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='full_name', read_only=True)
    course = serializers.CharField(source='course.name', read_only=True)
    total_points = serializers.SerializerMethodField()
    completed_assignments = serializers.SerializerMethodField()
    rank = serializers.SerializerMethodField()
    last_activity = serializers.DateTimeField(source='last_login', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'name', 'phone', 'course', 'total_points', 'completed_assignments', 'rank', 'last_activity']

    def get_total_points(self, obj):
        submissions = Submission.objects.filter(student_id=obj, status='graded')
        total = 0
        for sub in submissions:
            if sub.score and sub.score.isdigit():
                total += int(sub.score)
        return total

    def get_completed_assignments(self, obj):
        return Submission.objects.filter(student_id=obj, status='graded').count()

    def get_rank(self, obj):
        all_students = User.objects.filter(role='student')
        user_points = self.get_total_points(obj)
        better_count = 0

        for student in all_students:
            student_submissions = Submission.objects.filter(student_id=student, status='graded')
            student_points = 0
            for sub in student_submissions:
                if sub.score and sub.score.isdigit():
                    student_points += int(sub.score)
            if student_points > user_points:
                better_count += 1

        return better_count + 1


class UserProfileSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='full_name', read_only=True)
    course = serializers.CharField(source='course.name', read_only=True)
    total_points = serializers.SerializerMethodField()
    level = serializers.SerializerMethodField()
    badges = serializers.SerializerMethodField()
    join_date = serializers.DateField(source='date_joined', read_only=True)
    completion_rate = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'name', 'course', 'total_points', 'level', 'badges', 'join_date', 'completion_rate']






