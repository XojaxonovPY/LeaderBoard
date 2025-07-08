from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.views import TeacherModelViewSet, TeacherGroupListAPIView, TeacherSubmissionsListAPIView
from apps.views import LeaderboardAPIView, TeacherSubmissionsUpdateAPIView

router = DefaultRouter()

router.register(r'homework', TeacherModelViewSet, basename='homework')

urlpatterns = [
    path('teacher/groups/', TeacherGroupListAPIView.as_view(), name='teacher-groups'),
    path('teacher/groups/<int:pk>/submissions/', TeacherSubmissionsListAPIView.as_view(), name='teacher-submissions'),
    path('teacher/submissions/update/<int:pk>/', TeacherSubmissionsUpdateAPIView.as_view(), name='update-submissions'),
    path('teacher/groups/<int:pk>/leaderboard/', LeaderboardAPIView.as_view(), name='teacher-groups'),
    path('teachers/', include(router.urls))
]
