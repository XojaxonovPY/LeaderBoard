from django.urls import path
from apps.views import SubmissionCreatAPIView, SubmissionListAPIView, HomeworkListAPIView

urlpatterns = [
    path('save/submissions/', SubmissionCreatAPIView.as_view(), name='submission-save'),
    path('student/submissions/', SubmissionListAPIView.as_view(), name='submission-list'),
    path('student/homework/', HomeworkListAPIView.as_view(), name='homework-list'),
]
