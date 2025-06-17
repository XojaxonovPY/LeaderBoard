# import pytest
# from django.urls import reverse
# from rest_framework.test import APIClient
# from auth_apps.models import Course, User, Group
#
#
# class TestAuth:
#     @pytest.fixture
#     def api_client(self):
#         course = Course.objects.create(pk=2, name='Python')
#         teacher = User.objects.create_user(pk=6, full_name='Ali', password='1', role='teacher', phone='993583235')
#         group = Group.objects.create(pk=1, name='p_29', teacher=teacher, course=course)
#         admin = User.objects.create_user(pk=3, full_name='Admin', password='1', phone='993583234', role='admin',
#                                          group=group)
#
#         return APIClient()
#
#     def login_admin(self, client):
#         response = client.post("http://localhost:8000/api/v1/login/", {
#             "phone": "993583234",
#             "password": "1"
#         }, format="json")
#         token = response.json().get("access")
#         return {"Authorization": f"Bearer {token}"}
#
#     # ============================ AUTH =============================
#     @pytest.mark.django_db
#     def test_login(self, api_client):
#         response = api_client.post("http://localhost:8000/api/v1/login/", {
#             "phone": "993583234",
#             "password": "1"
#         }, format="json")
#         assert 200 <= response.status_code < 300, "Login failed"
#         assert "access" in response.data
#         assert "refresh" in response.data
#
#     # ============================ STUDENT ============================
#     @pytest.mark.django_db
#     def test_student_list(self, api_client):
#         headers = self.login_admin(api_client)
#         url = reverse('student-list')
#         response = api_client.get(url, headers=headers)
#         assert 300 >= response.status_code >= 200, 'Bad request'
#
#     @pytest.mark.django_db
#     def test_student_create(self, api_client):
#         headers = self.login_admin(api_client)
#         url = reverse('student-list')
#         response = api_client.post(url, headers=headers, data={
#             "full_name": "Student1",
#             "phone": "998001122",
#             "password": "1234",
#             "role": "student",
#             "group": 1
#         }, format="json")
#         assert 300 >= response.status_code >= 200, 'Bad request'
#
#     @pytest.mark.django_db
#     def test_student_update(self, api_client):
#         headers = self.login_admin(api_client)
#         url = reverse('student-detail', args=['3'])
#         response = api_client.patch(url, headers=headers, data={
#             "full_name": "aziz",
#         }, format="json")
#         assert 300 >= response.status_code >= 200, 'Bad request'
#
#     # ============================ TEACHER ============================
#     @pytest.mark.django_db
#     def test_teacher_list(self, api_client):
#         headers = self.login_admin(api_client)
#         url = reverse('teacher-list')
#         response = api_client.get(url, headers=headers)
#         assert 300 >= response.status_code >= 200, 'Bad request'
#
#     @pytest.mark.django_db
#     def test_teacher_create(self, api_client):
#         headers = self.login_admin(api_client)
#         url = reverse('teacher-list')
#         response = api_client.post(url, headers=headers, data={
#             "full_name": "Teacher1",
#             "phone": "998001123",
#             "password": "1234",
#             "role": "teacher",
#             "group": 1
#         }, format="json")
#         assert 300 >= response.status_code >= 200, 'Bad request'
#
#     @pytest.mark.django_db
#     def test_teacher_delete(self, api_client):
#         headers = self.login_admin(api_client)
#         url = reverse('teacher-detail', args=['6'])
#         response = api_client.delete(url, headers=headers, format="json")
#         assert 300 >= response.status_code >= 200, 'Bad request'
#
#     # ============================ GROUP ============================
#     @pytest.mark.django_db
#     def test_group_list(self, api_client):
#         headers = self.login_admin(api_client)
#         url = reverse('group-list')
#         response = api_client.get(url, headers=headers)
#         assert 300 >= response.status_code >= 200, 'Bad request'
#
#     @pytest.mark.django_db
#     def test_group_create(self, api_client):
#         headers = self.login_admin(api_client)
#         url = reverse('group-list')
#         response = api_client.post(url, headers=headers, data={
#             "name": "p_30",
#             "teacher": 6,
#             "course": 2
#         }, format="json")
#         assert 300 >= response.status_code >= 200, 'Bad request'
#
#     @pytest.mark.django_db
#     def test_group_detail(self, api_client):
#         headers = self.login_admin(api_client)
#         url = reverse('group-detail', args=['1'])
#         response = api_client.get(url, headers=headers, format="json")
#         assert 300 >= response.status_code >= 200, 'Bad request'
#
#     # ======================================student-change
#     @pytest.mark.django_db
#     def test_student_group_update(self, api_client):
#         headers = self.login_admin(api_client)
#         response = api_client.patch('http://localhost:8000/api/v1/admin/students/group/3/', data={
#             "group": 1
#         }, headers=headers, format='json')
#         assert 300 >= response.status_code >= 200, 'Bad request'
#
#     # ======================================teacher-change
#     @pytest.mark.django_db
#     def test_teacher_group_update(self, api_client):
#         headers = self.login_admin(api_client)
#         response = api_client.patch('http://localhost:8000/api/v1/admin/groups/teacher/6/', data={
#             "group": 1
#         }, headers=headers, format='json')
#         assert 300 >= response.status_code >= 200, 'Bad request'
