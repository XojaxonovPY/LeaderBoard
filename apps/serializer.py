from rest_framework.serializers import ModelSerializer

from apps.models import Submission


class LeadrModelSerializer(ModelSerializer):
    class Meta:
        model=Submission
        fields=('student_id','files','')
from rest_framework import serializers
from apps.models import Assignments, Course


class AssignmentsSerializer(serializers.ModelSerializer):


    class Meta:
        model = Assignments
        fields = [
            'id',
            'title',
            'description',
            'course_id',
            'difficulty',
            'deadline',
            'assignment_type',
        ]
