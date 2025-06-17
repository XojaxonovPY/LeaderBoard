from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from apps.models import  Submission




class SubmissionModelSerialize(ModelSerializer):
    class Meta:
        model = Submission
        fields = ('student', )

