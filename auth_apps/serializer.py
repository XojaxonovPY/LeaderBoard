import re

from django.contrib.auth.hashers import make_password
from rest_framework.serializers import ModelSerializer
from .models import User


class RegisterModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = 'username', 'email', 'password', 'phone', 'first_name'

    def validate_password(self, value):
        return make_password(value)

    def validate_phone(self, value):
        return re.sub(r'\D', '',value)  # re kutubxona D = Digit , '' = bosh joy faqat sonlar qoladi
