import pytest
from django.contrib.auth.hashers import make_password
from rest_framework.test import APIClient

from apps.models import Course
from auth_apps.models import User


class TestAuth:
    @pytest.fixture  # clone database
    def api_client(self):
        course=Course.objects.create(pk=2,name='Python')
        User.objects.create(pk=3, full_name='ali', course=course,
                            password=make_password("1"),
                            phone="993583234", role="admin")
        return APIClient()

    # ====================================================auth
    @pytest.mark.django_db
    def test_login(self, api_client):
        response = api_client.post("http://localhost:8000/api/v1/login/", {
            "phone": "993583234",
            "password": "1"
        }, format="json")
        assert 300 > response.status_code >= 200, "Bad Request"
        assert "access" in response.json().keys()
        assert "refresh" in response.json().keys()

    @pytest.mark.django_db
    def test_register(self, api_client):
        response = api_client.post('http://localhost:8000/api/v1/register/', {
            'full_name': 'ali',
            'password': '2',
            'phone': '999432923929',
            'course':2
        }, format='json')
        assert 300 > response.status_code >= 200, "Bad Request"
