from django.urls import path

from auth_apps.views import TeacherUpdateAPIView,GroupUpdateAPIView,GroupRetrieveView

urlpatterns=[
    path('admin/student/group/<int:pk>/',GroupUpdateAPIView.as_view()),
    path('admin/groups/teacher/<int:pk>/',TeacherUpdateAPIView.as_view()),
    path('admin/groups/leaderboard/<int:pk>/',GroupRetrieveView.as_view())
]