from rest_framework.serializers import ModelSerializer
from apps.models import Assignment
from apps.models import Submission



class AssignmentsSerializer(ModelSerializer):
    class Meta:
        model = Assignment
        fields = ('id', 'title','course', 'description', 'difficulty', 'deadline', 'assignment_type', 'max_points',
                  'requirements', 'resources')
        read_only_field=('id',)
