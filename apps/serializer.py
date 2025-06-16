from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from apps.models import Assignment, Submission


class AssignmentsSerializer(ModelSerializer):
    class Meta:
        model = Assignment
        fields = ('id', 'title', 'course', 'description', 'difficulty', 'deadline', 'assignment_type', 'max_points',
                  'requirements', 'resources')
        read_only_field = ('id',)


class SubmissionModelSerialize(ModelSerializer):
    class Meta:
        model = Submission
        fields = ('student', 'assignment', 'submission_type', 'github_link', 'description', 'notes')

    def validate_github_link(self, value):
        if value.startswith('https://github.com/'):
            return value
        else:
            raise ValidationError('Its not git hub project')
