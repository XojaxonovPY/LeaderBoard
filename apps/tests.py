from datetime import datetime, timedelta
from wsgiref import headers

import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from apps.models import SubmissionFile, Homework, Submission
from auth_apps.models import Course, User, Group


class TestAuth:
    @pytest.fixture
    def api_client(self):
        # 1. Teacher va Admin user
        teacher = User.objects.create_user(
            pk=4, full_name='Teacher One', phone='991000000', password='1', role='teacher'
        )
        admin = User.objects.create_user(
            pk=1, full_name='Admin', phone='992000000', password='1', role='admin'
        )

        # 2. Group & Course
        course = Course.objects.create(name='Backend')
        group = Group.objects.create(name='G-1', teacher=teacher, course=course)

        # 3. Student
        student = User.objects.create_user(
            pk=1, full_name='Student One', phone='993000000', password='1', role='student', group=group
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
            file_extensions='txt',
            ai_grading_prompt='Evaluate this homework.'
        )

        # 5. Submission
        submission = Submission.objects.create(
            pk=4,
            homework=homework,
            student=student,
            ai_grade=75,
            final_grade=85,
            ai_feedback='Good job!'
        )

        # 6. SubmissionFile
        submission_file = SubmissionFile.objects.create(
            submission=submission,
            file_name='solution.py',
            content='print("Hello World")',
            line_count=1
        )
        return APIClient()

    def login_admin(self, client):
        response = client.post("http://localhost:8000/api/v1/login/", {
            "phone": "991000000",
            "password": "1"
        }, format="json")
        token = response.json().get("access")
        return {"Authorization": f"Bearer {token}"}

    # ============================ teacher ============================

    @pytest.mark.django_db
    def test_teacher__homework_list(self, api_client):
        headers = self.login_admin(api_client)
        url = reverse('homework-list')
        response = api_client.get(url, headers=headers)
        assert 300 >= response.status_code >= 200, 'Bad request'

    @pytest.mark.django_db
    def test_teacher__homework_create(self, api_client):
        headers = self.login_admin(api_client)

        # Test uchun group mavjud bo‘lishi shart
        teacher = User.objects.get(phone='991000000')
        course = Course.objects.create(name='Test Course')
        group = Group.objects.create(name='Test Group', teacher=teacher, course=course)

        url = reverse('homework-list')
        response = api_client.post(url, headers=headers, format="json", data={
            "title": "Homework 1",
            "description": "Birinchi uyga vazifa",
            "points": 100,
            "start_date": "2025-06-14",
            "deadline": "2025-06-20T23:59:00Z",
            "line_limit": 50,
            "group": group.id,
            "file_extensions": Homework.FileType.TXT,
            "ai_grading_prompt": "Evaluate code readability and logic."
        })
        assert 200 <= response.status_code < 300, f'POST create failed: {response.status_code} {response.content}'

    @pytest.mark.django_db
    def test_teacher__homework_update(self, api_client):
        headers = self.login_admin(api_client)
        url = reverse('homework-detail', kwargs={'pk': 2})
        response = api_client.patch(url, headers=headers, format="json", data={
            "title": "Yangi sarlavha"
        })
        assert 200 <= response.status_code < 300, 'PATCH update failed'

    @pytest.mark.django_db
    def test_teacher__homework_delete(self, api_client):
        headers = self.login_admin(api_client)
        url = reverse('homework-detail', kwargs={'pk': 2})
        response = api_client.delete(url, headers=headers)
        assert response.status_code == 204, 'DELETE failed'

    # =================================teacher-group==============================
    @pytest.mark.django_db
    def test_teacher_group(self, api_client):
        headers = self.login_admin(api_client)
        response = api_client.get('http://localhost:8000/api/v1/teacher/groups/', headers=headers, format='json')
        assert 300 >= response.status_code >= 200, 'Bad request'

    @pytest.mark.django_db
    def test_teacher__submission(self, api_client):
        headers = self.login_admin(api_client)
        response = api_client.get('http://localhost:8000/api/v1/teacher/groups/1/submissions/', headers=headers,
                                  format='json')
        assert 300 >= response.status_code >= 200, 'Bad request'

    @pytest.mark.django_db
    def test_teacher_leaderboard(self, api_client):
        headers = self.login_admin(api_client)
        response = api_client.get('http://localhost:8000/api/v1/teacher/groups/1/leaderboard/', headers=headers,
                                  format='json')
        assert 300 >= response.status_code >= 200, "Bad request"

    @pytest.mark.django_db
    def test_teacher_submission_update(self, api_client):
        headers = self.login_admin(api_client)
        response = api_client.patch('http://localhost:8000/api/v1/teacher/submissions/update/4/', headers=headers,
                                    data={
                                        'final_grade': 80,
                                    }, format='json')
        assert 300 >= response.status_code >= 200, "Bad request"

    # =================================================student============
    # @pytest.mark.django_db
    # def test_submission_save(self, api_client):
    #     headers = self.login_admin(api_client)
    #     response = api_client.post('http://localhost:8000/api/v1/save/submissions/', headers=headers, format='json',
    #                                data={
    #                                    "homework": 2,
    #                                    "ai_grade": 80,
    #                                    "final_grade": 90,
    #                                    "ai_feedback": "good",
    #                                    "files": [
    #                                        {
    #                                            "file_name": "py file",
    #                                            "content": "file.txt",
    #                                            "line_count": 200
    #                                        }
    #                                    ]
    #                                }
    #                                )
    #     assert 300 >= response.status_code >= 200, 'Bad request'

    @pytest.mark.django_db
    def test_student_submission_list(self, api_client):
        headers = self.login_admin(api_client)

        response = api_client.get(
            'http://localhost:8000/api/v1/student/submissions/', headers=headers, format='json'
        )

        assert 300 >= response.status_code >= 200, "Bad request"

    @pytest.mark.django_db
    def test_student_homework_list(self, api_client):
        headers = self.login_admin(api_client)

        response = api_client.get('http://localhost:8000/api/v1/student/homework/', headers=headers, format='json')

        assert 300 >= response.status_code >= 200, "Bad request"

    @pytest.mark.django_db
    def test_student_student_leaderboard(self, api_client):
        headers = self.login_admin(api_client)
        response = api_client.get('http://localhost:8000/api/v1/student/leaderboard/', headers=headers, format='json')
        assert 200 <= response.status_code < 300, "Bad request"
