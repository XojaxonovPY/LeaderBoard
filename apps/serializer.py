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






