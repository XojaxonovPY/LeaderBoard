from datetime import datetime, timedelta

import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from apps.models import SubmissionFile, Grade, Submission, Homework
from auth_apps.models import Course, User, Group


class TestAuth:
    @pytest.fixture
    def api_client(self):
        course = Course.objects.create(name='Python')
        teacher = User.objects.create_user(full_name='Ali', password='1', role='teacher', phone='993583235')
        group = Group.objects.create(name='p_29', teacher=teacher, course=course)
        admin = User.objects.create_user(full_name='Admin', password='1', phone='993583234', role='admin', group=group)

        homework = Homework.objects.create(
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

        submission = Submission.objects.create(
            homework=homework,
            student=admin,
            ai_grade=75,
            final_grade=85,
            ai_feedback='Good job!'
        )

        SubmissionFile.objects.create(
            submission=submission,
            file_name='solution.py',
            content='print("Hello World")',
            line_count=1
        )

        Grade.objects.create(
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
        response = client.post("/api/v1/login/", {
            "phone": "993583234",
            "password": "1"
        }, format="json")
        token = response.json().get("access")
        return {"Authorization": f"Bearer {token}"}

    @pytest.mark.django_db
    def test_login(self, api_client):
        response = api_client.post("/api/v1/login/", {
            "phone": "993583234",
            "password": "1"
        }, format="json")
        assert 200 <= response.status_code < 300
        assert "access" in response.data
        assert "refresh" in response.data

    @pytest.mark.django_db
    def test_student_list(self, api_client):
        headers = self.login_admin(api_client)
        url = reverse('student-list')
        response = api_client.get(url, headers=headers)
        assert 200 <= response.status_code < 300

    @pytest.mark.django_db
    def test_student_create(self, api_client):
        headers = self.login_admin(api_client)
        url = reverse('student-list')
        response = api_client.post(url, headers=headers, data={
            "full_name": "Student1",
            "phone": "998001122",
            "password": "1234",
            "role": "student",
            "group": Group.objects.first().id
        }, format="json")
        assert 200 <= response.status_code < 300

    @pytest.mark.django_db
    def test_student_update(self, api_client):
        headers = self.login_admin(api_client)
        url = reverse('student-detail', args=[User.objects.get(phone="993583234").id])
        response = api_client.patch(url, headers=headers, data={"full_name": "Aziz"}, format="json")
        assert 200 <= response.status_code < 300

    @pytest.mark.django_db
    def test_teacher_list(self, api_client):
        headers = self.login_admin(api_client)
        url = reverse('teacher-list')
        response = api_client.get(url, headers=headers)
        assert 200 <= response.status_code < 300

    @pytest.mark.django_db
    def test_teacher_create(self, api_client):
        headers = self.login_admin(api_client)
        url = reverse('teacher-list')
        response = api_client.post(url, headers=headers, data={
            "full_name": "Teacher1",
            "phone": "998001123",
            "password": "1234",
            "role": "teacher",
            "group": Group.objects.first().id
        }, format="json")
        assert 200 <= response.status_code < 300

    @pytest.mark.django_db
    def test_teacher_delete(self, api_client):
        headers = self.login_admin(api_client)
        teacher = User.objects.get(role='teacher')
        url = reverse('teacher-detail', args=[teacher.id])
        response = api_client.delete(url, headers=headers)
        assert 200 <= response.status_code < 300

    @pytest.mark.django_db
    def test_group_list(self, api_client):
        headers = self.login_admin(api_client)
        url = reverse('group-list')
        response = api_client.get(url, headers=headers)
        assert 200 <= response.status_code < 300

    @pytest.mark.django_db
    def test_group_create(self, api_client):
        headers = self.login_admin(api_client)
        teacher = User.objects.get(role='teacher')
        course = Course.objects.first()
        url = reverse('group-list')
        response = api_client.post(url, headers=headers, data={
            "name": "p_30",
            "teacher": teacher.id,
            "course": course.id
        }, format="json")
        assert 200 <= response.status_code < 300

    @pytest.mark.django_db
    def test_group_detail(self, api_client):
        headers = self.login_admin(api_client)
        group = Group.objects.first()
        url = reverse('group-detail', args=[group.id])
        response = api_client.get(url, headers=headers)
        assert 200 <= response.status_code < 300

    @pytest.mark.django_db
    def test_student_group_update(self, api_client):
        headers = self.login_admin(api_client)
        student = User.objects.get(role='admin')
        group = Group.objects.first()
        response = api_client.patch(f'/api/v1/admin/students/group/{student.id}/', data={
            "group": group.id
        }, headers=headers, format='json')
        assert 200 <= response.status_code < 300

    @pytest.mark.django_db
    def test_teacher_group_update(self, api_client):
        headers = self.login_admin(api_client)
        teacher = User.objects.get(role='teacher')
        group = Group.objects.first()
        response = api_client.patch(f'/api/v1/admin/groups/teacher/{teacher.id}/', data={
            "group": group.id
        }, headers=headers, format='json')
        assert 200 <= response.status_code < 300

    @pytest.mark.django_db
    def test_teacher_group_detail(self, api_client):
        headers = self.login_admin(api_client)
        group = Group.objects.first()
        response = api_client.get(f'/api/v1/admin/groups/leaderboard/{group.id}/', headers=headers)
        assert 200 <= response.status_code < 300
