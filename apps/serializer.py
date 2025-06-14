from rest_framework.serializers import ModelSerializer
from apps.models import Assignment
from apps.models import Submission


# class LeadrModelSerializer(ModelSerializer):
#     class Meta:
#         model = Submission
#         fields = ('student_id', 'files', '')


class AssignmentsSerializer(ModelSerializer):
    class Meta:
        model = Assignment
        fields = ('id', 'title','course', 'description', 'difficulty', 'deadline', 'assignment_type', 'max_points',
                  'requirements', 'resources')
        read_only_field=('id',)
