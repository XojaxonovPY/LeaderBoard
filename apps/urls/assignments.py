from django.urls import path
from apps.views import AssignmentCreateView, StudentAssignmentsListAPIView

urlpatterns = [
    path('save/assignments', AssignmentCreateView.as_view(), name='assignment-save'),
    path('assignments/student/', StudentAssignmentsListAPIView.as_view(), name='student-assigment'),
]
