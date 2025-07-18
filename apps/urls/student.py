from django.urls import path
from apps.views import SubmissionCreatAPIView, SubmissionListAPIView, HomeworkListAPIView,LeaderBoardAPIView

urlpatterns = [
    path('save/submissions/', SubmissionCreatAPIView.as_view(), name='submission-save'),
    path('student/submissions/', SubmissionListAPIView.as_view(), name='submission-list'),
    path('student/homework/', HomeworkListAPIView.as_view(), name='homework-list'),
    path('student/leaderboard/', LeaderBoardAPIView.as_view(), name='leader-board'),
]
