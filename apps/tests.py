from datetime import datetime, timedelta

import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from apps.models import Grade, SubmissionFile, Homework, Submission
from auth_apps.models import Course, User, Group


class TestAuth:
    @pytest.fixture
    def api_client(self):
        # 1. Teacher va Admin user
        teacher = User.objects.create_user(
            pk=4, full_name='Teacher One', phone='991000000', password='1', role='teacher'
        )
        admin = User.objects.create_user(
            pk=2, full_name='Admin', phone='992000000', password='1', role='admin'
        )

        # 2. Group & Course
        course = Course.objects.create(name='Backend')
        group = Group.objects.create(name='G-1', teacher=teacher, course=course)

        # 3. Student
        student = User.objects.create_user(
            pk=3, full_name='Student One', phone='993000000', password='1', role='student', group=group
        )

        # 4. Homework
        homework = Homework.objects.create(
            pk=2,
            title='OOP Homework',
            description='Test Description',
            points=100,
            start_date=datetime.today().date(),
            deadline=datetime.now() + timedelta(days=2),
            line_limit=50,
            teacher=teacher,
            group=group,
            file_extensions='py,txt',
            ai_grading_prompt='Evaluate this homework.'
        )

        # 5. Submission
        submission = Submission.objects.create(
            pk=2,
            homework=homework,
            student=student,
            ai_grade=75,
            final_grade=85,
            ai_feedback='Good job!'
        )

        # 6. SubmissionFile
        submission_file = SubmissionFile.objects.create(
            pk=2,
            submission=submission,
            file_name='solution.py',
            content='print("Hello World")',
            line_count=1
        )

        # 7. Grade
        grade = Grade.objects.create(
            pk=2,
            submission=submission,
            ai_task_completeness=25.00,
            ai_code_quality=25.00,
            ai_correctness=25.00,
            ai_total=75.00,
            final_task_completeness=30.00,
            final_code_quality=30.00,
            final_correctness=25.00,
            teacher_total=85.00,
            ai_feedback='AI: Good.',
            task_completeness_feedback='Complete',
            code_quality_feedback='Clean',
            correctness_feedback='Correct',
            modified_by_teacher=teacher
        )
        return APIClient()

    def login_admin(self, client):
        response = client.post("http://localhost:8000/api/v1/login/", {
            "phone": "991000000",
            "password": "1"
        }, format="json")
        token = response.json().get("access")
        return {"Authorization": f"Bearer {token}"}

    # ============================ STUDENT ============================

    @pytest.mark.django_db
    def test_homework_list(self, api_client):
        headers = self.login_admin(api_client)
        url = reverse('homework-list')
        response = api_client.get(url, headers=headers)
        assert 300 >= response.status_code >= 200, 'Bad request'

    @pytest.mark.django_db
    def test_homework_create(self, api_client):
        headers = self.login_admin(api_client)
        url = reverse('homework-list')
        response = api_client.post(url, headers=headers, format="json", data={
            "title": "Homework 1",
            "description": "Birinchi uyga vazifa",
            "points": 100,
            "start_date": "2025-06-14",
            "deadline": "2025-06-20T23:59:00Z",
            "line_limit": 50,
            "teacher": 4,
            "group": 1,
            "file_extensions": "py,txt",
            "ai_grading_prompt": "Evaluate code readability and logic."
        })
        assert 200 <= response.status_code < 300, 'POST create failed'

    @pytest.mark.django_db
    def test_homework_update(self, api_client):
        headers = self.login_admin(api_client)
        url = reverse('homework-detail', kwargs={'pk': 2})
        response = api_client.patch(url, headers=headers, format="json", data={
            "title": "Yangi sarlavha"
        })
        assert 200 <= response.status_code < 300, 'PATCH update failed'

    @pytest.mark.django_db
    def test_homework_delete(self, api_client):
        headers = self.login_admin(api_client)
        url = reverse('homework-detail', kwargs={'pk': 2})
        response = api_client.delete(url, headers=headers)
        assert response.status_code == 204, 'DELETE failed'