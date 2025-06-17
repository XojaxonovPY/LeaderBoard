from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from apps.models import Submission, Homework


class SubmissionModelSerialize(ModelSerializer):
    class Meta:
        model = Submission
        fields = ('student', 'homework', 'student', 'submitted_at', 'ai_grade', 'final_grade', 'ai_feedback',
                  'created_at')


class HomeworkModelSerializer(ModelSerializer):
    class Meta:
        model = Homework
        fields = ('id', 'title', 'description', 'points', 'start_date', 'deadline', 'line_limit', 'teacher', 'group',
                  'file_extensions', 'ai_grading_prompt', 'created_at')
        read_only_fields = ('id', 'created_at', 'teacher')
