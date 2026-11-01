from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.views import LeaderboardAPIView, TeacherSubmissionsUpdateAPIView, LessonCreateAPIView, LessonListAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView, LessonRetrieveAPIView, SourceCreateAPIView
from apps.views import TeacherModelViewSet, TeacherGroupListAPIView, TeacherSubmissionsListAPIView

router = DefaultRouter()

router.register(r'homework', TeacherModelViewSet, basename='homework')

urlpatterns = [
    path('teacher/groups/', TeacherGroupListAPIView.as_view(), name='teacher-groups'),
    path('teacher/groups/<int:pk>/submissions/', TeacherSubmissionsListAPIView.as_view(), name='teacher-submissions'),
    path('teacher/submissions/update/<int:pk>/', TeacherSubmissionsUpdateAPIView.as_view(), name='update-submissions'),
    path('teacher/groups/<int:pk>/leaderboard/', LeaderboardAPIView.as_view(), name='teacher-groups'),
    path('teachers/', include(router.urls))
]

urlpatterns += [
    path("lesson/create/", LessonCreateAPIView.as_view()),
    path("lessons/list/", LessonListAPIView.as_view()),
    path("lesson/update/<int:pk>/", LessonUpdateAPIView.as_view()),
    path("lesson/delete/<int:pk>/", LessonDestroyAPIView.as_view()),
    path("lesson/detail/<int:pk>/", LessonRetrieveAPIView.as_view()),
    path("source/create", SourceCreateAPIView.as_view()),
]
