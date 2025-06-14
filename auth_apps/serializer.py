import re

from django.contrib.auth.hashers import make_password
from rest_framework.serializers import ModelSerializer
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
