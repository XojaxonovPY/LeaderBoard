from datetime import datetime

import pytest
from django.contrib.auth.hashers import make_password
from rest_framework.test import APIClient

from apps.models import Assignment, Course
from auth_apps.models import User


class TestAuth:
    @pytest.fixture  # clone database
    def api_client(self):
        course = Course.objects.create(pk=2, name='Python')
        User.objects.create(pk=3, full_name='ali', course=course,
                            password=make_password("1"),
                            phone="993583234", role="teacher")
        return APIClient()

    @pytest.fixture
    def api_assignment(self):
        course = Course.objects.create(pk=3, name="Django Web")  # Kurs yaratish yoki mavjudini olish

        Assignment.objects.create(
            title="HTML/CSS Portfolio Loyihasi",
            description="Personal portfolio website yarating...",
            course=course,
            difficulty=Assignment.DifficultyLevel.MEDIUM,
            deadline=datetime(2024, 12, 25, 23, 59, 59),
            assignment_type=Assignment.AssignmentType.PROJECT,
            max_points=100,
            requirements=[
                "Responsive design bo'lishi kerak",
                "Kamida 3 ta sahifa",
                "GitHub'ga yuklash"
            ],
            resources=[
                "https://example.com/tutorial",
                "https://example.com/documentation"
            ]
        )

        return APIClient()

    @pytest.mark.django_db
    def test_save_assignment(self, api_client, api_assignment):
        response = api_client.post("http://localhost:8000/api/v1/login/", {
            "phone": "993583234",
            "password": "1"
        }, format="json")

        data = response.json()
        access_token = data.get("access")
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        response = api_assignment.post(
            'http://localhost:8000/api/v1/save/assignments/',
            headers=headers,
            data={
                'title': "HTML/CSS Portfolio Loyihasi",
                'description': "Personal portfolio website yarating...",
                'course': 3,
                'difficulty': "medium",
                'deadline': "2024-12-25T23:59:59+05:00",
                'assignment_type': "project",
                'max_points': 100,
                'requirements': [
                    "Responsive design bo'lishi kerak",
                    "Kamida 3 ta sahifa",
                    "GitHub'ga yuklash"
                ],
                'resources': [
                    "https://example.com/tutorial",
                    "https://example.com/documentation"
                ]
            },
            format='json'
        )
        assert 200 <= response.status_code < 300, 'Bad Request'

    @pytest.mark.django_db
    def test_get_assignment(self, api_client, api_assignment):
        response = api_client.post("http://localhost:8000/api/v1/login/", {
            "phone": "993583234",
            "password": "1"
        }, format="json")

        data = response.json()
        access_token = data.get("access")
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        response = api_assignment.get('http://localhost:8000/api/v1/assignments/student/',
            headers=headers,format='json')
        assert 200 <= response.status_code < 300, 'Bad Request'
